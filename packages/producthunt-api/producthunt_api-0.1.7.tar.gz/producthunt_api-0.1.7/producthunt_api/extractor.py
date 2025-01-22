import os
import json

from .utils.logger_config import get_logger

logger = get_logger(__name__)

class DataExtractor:
    def __init__(self, output_dir):
        """
        Initialize the extractor for handling product JSON data.

        :param output_dir: Directory where JSON files are stored.
        """
        self.output_dir = output_dir
        self.products_dir = os.path.join(output_dir, "products")
        self.output_json = os.path.join(output_dir, "products.json")

    def extract_data_from_file(self, filepath):
        """
        Extract the first valid product details from a JSON file.

        :param filepath: Path to the JSON file.
        :return: The first valid product data or None if not found.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Look for the first valid "data" event with the correct product structure
            events = data.get("events", [])
            for event in events:
                if event.get("type") == "data":
                    product = event.get("result", {}).get("data", {}).get("product")
                    if product and product.get("__typename") == "Product":
                        return product  # Return immediately upon finding a valid product

            logger.warning(f"No valid product data found in {filepath}")
            return None

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Error reading JSON file {filepath}: {e}")
            return None

    def process_json_files(self):
        """
        Process all JSON files in the products directory and collect the first valid product data.

        :return: List of the first valid product data from each file.
        """
        if not os.path.exists(self.products_dir):
            logger.error(f"Products directory {self.products_dir} does not exist.")
            return []

        files = [
            os.path.join(self.products_dir, f)
            for f in os.listdir(self.products_dir)
            if f.endswith(".json")
        ]

        all_data = []
        for file in files:
            logger.info(f"Processing file: {file}")
            product = self.extract_data_from_file(file)
            if product:  # If a valid product is found, add it
                all_data.append(product)

        return all_data

    def save_to_json(self, product_data):
        """
        Save all extracted product data to a single JSON file.

        :param product_data: List of extracted product data.
        """
        if not product_data:
            logger.info("No data to save to JSON.")
            return

        try:
            with open(self.output_json, "w", encoding="utf-8") as f:
                json.dump(product_data, f, indent=4)
            logger.info(f"Data successfully saved to {self.output_json}")
        except Exception as e:
            logger.error(f"Error writing to JSON file: {e}")

    def run(self):
        """
        Extract data from JSON files and save it as a consolidated JSON.
        """
        extracted_data = self.process_json_files()
        self.save_to_json(extracted_data)



if __name__ == "__main__":
    output_dir = os.path.join(os.getcwd(), "downloads")

    extractor = DataExtractor(output_dir)
    extractor.run()
