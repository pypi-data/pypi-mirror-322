import os
import json
import csv

from .utils.logger_config import get_logger

logger = get_logger(__name__)


class JSONToCSVConverter:
    def __init__(self, input_dir, output_csv):
        """
        Initialize the converter with input directory and output CSV file.

        :param input_dir: Directory where JSON files are stored.
        :param output_csv: Path to the output CSV file.
        """
        self.input_dir = input_dir
        self.output_csv = output_csv
        if not os.path.exists(self.input_dir):
            logger.warning(f"Input directory {self.input_dir} does not exist.")
            os.makedirs(self.input_dir, exist_ok=True)

    def extract_data_from_file(self, filepath):
        """Extract relevant product details from a JSON file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Locate the product information dynamically in the JSON
            rehydrate_data = data.get("rehydrate", {})
            product_data = None

            for key, value in rehydrate_data.items():
                # Ensure value is a dictionary before accessing keys
                if isinstance(value, dict):
                    data_field = value.get("data", {})
                    if isinstance(data_field, dict) and "product" in data_field:
                        product_data = data_field["product"]
                        break

            if not product_data:
                logger.warning(f"No product data found in {filepath}")
                return None

            # Extract relevant fields
            return {
                "name": product_data.get("name"),
                "tagline": product_data.get("tagline"),
                "followers_count": product_data.get("followersCount"),
                "reviews_count": product_data.get("reviewsCount"),
                "reviews_rating": product_data.get("reviewsRating"),
                "website_url": product_data.get("websiteUrl"),
                "facebook_url": product_data.get("facebookUrl"),
                "twitter_url": product_data.get("twitterUrl"),
                "linkedin_url": product_data.get("linkedinUrl"),
                "github_url": product_data.get("githubUrl"),
                "instagram_url": product_data.get("instagramUrl"),
            }

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Error reading JSON file {filepath}: {e}")
            return None

    def process_json_files(self):
        """Process all JSON files in the input directory."""
        if not os.path.exists(self.input_dir):
            logger.error(f"Input directory {self.input_dir} does not exist.")
            return []

        all_files = [os.path.join(self.input_dir, f) for f in os.listdir(self.input_dir) if f.endswith('.json')]
        all_data = []

        for file in all_files:
            logger.info(f"Processing file: {file}")
            data = self.extract_data_from_file(file)
            if data:
                all_data.append(data)

        return all_data

    def save_to_csv(self, data):
        """Save extracted data to a CSV file."""
        if not data:
            logger.info("No data to save to CSV.")
            return

        # Define the CSV headers
        headers = [
            "name",
            "tagline",
            "followers_count",
            "reviews_count",
            "reviews_rating",
            "website_url",
            "facebook_url",
            "twitter_url",
            "linkedin_url",
            "github_url",
            "instagram_url",
        ]

        try:
            with open(self.output_csv, 'w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Data successfully saved to {self.output_csv}")
        except Exception as e:
            logger.error(f"Error writing to CSV file: {e}")

    def run(self):
        """Run the JSON to CSV conversion process."""
        extracted_data = self.process_json_files()
        self.save_to_csv(extracted_data)


if __name__ == "__main__":
    input_directory = os.path.join(os.getcwd(), "downloads", "products")
    output_csv_file = os.path.join(os.getcwd(), "products.csv")

    converter = JSONToCSVConverter(input_directory, output_csv_file)
    converter.run()
