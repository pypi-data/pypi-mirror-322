import os
import json
import re
import shutil
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

from .utils.logger_config import get_logger

logger = get_logger(__name__)

class ProductInfoManager:
    def __init__(self, pages_dir, products_dir):
        """
        Initialize the manager with custom directories for pages and products.

        :param pages_dir: Directory where the page JSON files are stored.
        :param products_dir: Directory where the product JSON files will be saved.
        """
        self.pages_dir = pages_dir
        self.products_dir = products_dir
        if os.path.exists(self.products_dir):
            logger.info(f"Removing existing directory: {self.products_dir}")
            shutil.rmtree(self.products_dir)
        os.makedirs(self.products_dir, exist_ok=True)

    def load_pages_files(self):
        """Load all JSON files from the 'pages' directory."""
        files = [
            os.path.join(self.pages_dir, file)
            for file in os.listdir(self.pages_dir)
            if file.endswith(".json")
        ]
        if not files:
            logger.info(f"No JSON files found in the '{self.pages_dir}' directory.")
        return files

    def parse_product_urls(self, filepath):
        """Extract product URLs and IDs from a single JSON file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            urls = []
            edges = (
                data.get("data", {})
                .get("productCategory", {})
                .get("products", {})
                .get("edges", [])
            )

            for edge in edges:
                node = edge.get("node", {})
                if "slug" in node and "id" in node:
                    urls.append({
                        "url": f"https://www.producthunt.com/products/{node['slug']}",
                        "id": node["id"],
                    })

            return urls

        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON in file {filepath}")
        except Exception as e:
            logger.error(f"Error processing file {filepath}: {e}")
        return []

    def fetch_html(self, url):
        """Fetch HTML content from a given URL."""
        try:
            logger.info(f"Fetching HTML from URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching HTML from {url}: {e}")
            return None

    def extract_embedded_json(self, html_content, marker="window[Symbol.for"):
        """Extract JSON data embedded in the HTML content."""
        logger.info("Extracting JSON from HTML content.")
        soup = BeautifulSoup(html_content, "html.parser")
        scripts = soup.find_all("script")

        for script in scripts:
            if marker in script.text:  # Look for marker in the script
                json_match = re.search(r"{.*}", script.text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    json_str = json_str.replace("undefined", "null")
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON decoding error: {e}")
                        return None
        logger.warning("No JSON found with the given marker.")
        return None

    def save_json_to_file(self, data, file_name):
        """Save extracted JSON to a file in the 'products' directory."""
        output_path = os.path.join(self.products_dir, file_name)
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            logger.info(f"Saved JSON data to {output_path}")
        except Exception as e:
            logger.error(f"Error saving JSON to file {output_path}: {e}")

    def process_url(self, url, product_id):
        """Process a single URL: fetch HTML, extract JSON, and save it."""
        file_name = f"{product_id}.json"
        output_path = os.path.join(self.products_dir, file_name)

        # Skip processing if file already exists
        if os.path.exists(output_path):
            logger.info(f"File already exists for product ID {product_id}. Skipping.")
            return

        html_content = self.fetch_html(url)
        if not html_content:
            return

        extracted_json = self.extract_embedded_json(html_content)
        if extracted_json:
            self.save_json_to_file(extracted_json, file_name)
        else:
            logger.warning(f"No JSON extracted from {url}")

    def process_pages_and_fetch_products(self, max_threads=3):
        """Process 'pages' JSON files and fetch product data using threads."""
        page_files = self.load_pages_files()
        all_urls = []

        # Parse product URLs from all page files
        for file in page_files:
            logger.info(f"Parsing file: {file}")
            urls = self.parse_product_urls(file)
            if urls:
                all_urls.extend(urls)

        if not all_urls:
            logger.info("No product URLs found.")
            return

        # Fetch and save product data for each URL using multithreading
        with ThreadPoolExecutor(max_threads) as executor:
            future_to_url = {
                executor.submit(self.process_url, item["url"], item["id"]): item
                for item in all_urls
            }
            for future in as_completed(future_to_url):
                try:
                    future.result()  # Retrieve the result to handle exceptions
                except Exception as e:
                    item = future_to_url[future]
                    logger.error(f"Error processing URL {item['url']}: {e}")


if __name__ == "__main__":
    pages_directory = os.path.join(os.getcwd(), "downloads", "pages")
    products_directory = os.path.join(os.getcwd(), "downloads", "products")

    manager = ProductInfoManager(pages_directory, products_directory)
    manager.process_pages_and_fetch_products(max_threads=10)
