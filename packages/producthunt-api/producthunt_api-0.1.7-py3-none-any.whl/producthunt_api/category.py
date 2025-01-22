import os
import json
import requests
import shutil

from .utils.logger_config import get_logger

logger = get_logger(__name__)


class ProductHuntFetcher:
    """
    A class to fetch and process data from the Product Hunt GraphQL API.
    """

    def __init__(self, save_path, cookie, sha256_hash, slug):
        """
        Initialize the fetcher with a directory path to save JSON files, a cookie, a sha256Hash, and a slug.

        :param save_path: Directory path where JSON files will be saved.
        :param cookie: Cookie string for authentication.
        :param sha256_hash: SHA256 hash for the persisted query.
        :param slug: The slug of the category to fetch products from.
        """
        self.url = "https://www.producthunt.com/frontend/graphql"
        self.headers = {
            "accept": "*/*",
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-ph-timezone": "Asia/Makassar",
            "cookie": cookie,
        }
        self.save_path = save_path
        self.sha256_hash = sha256_hash
        self.slug = slug

        if os.path.exists(self.save_path):
            logger.info(f"Removing existing directory: {self.save_path}")
            shutil.rmtree(self.save_path)
        os.makedirs(self.save_path, exist_ok=True)

    def fetch_graphql_data(self, cursor=None):
        """
        Fetch data from the Product Hunt GraphQL API for the specified category.

        :param cursor: Cursor for pagination (default is None).
        :return: JSON response from the API.
        """
        payload = {
            "operationName": "CategoryPageQuery",
            "variables": {
                "featuredOnly": False,
                "slug": self.slug,
                "cursor": cursor,
                "order": "highest_rated",
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": self.sha256_hash,
                }
            },
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info("Successfully fetched data from Product Hunt API.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error occurred: {e}")
            return None

    def save_to_json(self, cursor, data):
        """
        Save the fetched data to a JSON file in the specified directory.

        :param cursor: The cursor used to fetch this data.
        :param data: The JSON data to save.
        """
        file_name = f"{cursor or 'start'}.json"
        file_path = os.path.join(self.save_path, file_name)

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logger.info(f"Saved data for cursor {cursor or 'start'} to {file_path}")

    def process_products(self, data):
        """
        Process and print product information from the API response.

        :param data: JSON response containing product data.
        """
        products = data.get("data", {}).get("productCategory", {}).get("products", {}).get("edges", [])
        for product in products:
            node = product.get("node", {})
            logger.info(f"Product: {node.get('name')} - Tagline: {node.get('tagline')} - Rating: {node.get('reviewsRating')}")

    def fetch_all_products(self, start_cursor=None, limit=None):
        """
        Fetch all products in the specified category by handling pagination, with an optional limit on the number of products.

        :param start_cursor: Initial cursor for fetching data (default is None).
        :param limit: Maximum number of products to fetch (default is None, meaning no limit).
        """
        cursor = start_cursor
        total_fetched = 0

        while True:
            logger.info(f"Fetching page with cursor: {cursor or 'start'}")
            data = self.fetch_graphql_data(cursor)

            if not data:
                logger.warning("No data received. Stopping pagination.")
                break

            # Process the products in the current response
            products = data.get("data", {}).get("productCategory", {}).get("products", {}).get("edges", [])
            self.process_products(data)

            # Save the data to a JSON file
            self.save_to_json(cursor, data)

            # Update the total fetched count
            total_fetched += len(products)

            if limit is not None and total_fetched >= limit:
                logger.info(f"Limit of {limit} products reached. Stopping fetch.")
                break

            # Extract pagination information
            page_info = data.get("data", {}).get("productCategory", {}).get("products", {}).get("pageInfo", {})
            cursor = page_info.get("endCursor")

            if not page_info.get("hasNextPage"):
                logger.info("No more pages to fetch.")
                break


if __name__ == "__main__":
    save_directory = os.path.join(os.getcwd(), "downloads", "pages")
    cookie_value = "_ga=GA1.1.660153458.1733116004; ajs_anonymous_id=6e0a9dd4-91ff-4476-bd63-58de4f020ab9; visitor_id=8d3991f1-624f-4b56-aea1-fc4f44bcb326; track_code=7e715c9281; intercom-id-fe4ce68d4a8352909f553b276994db414d33a55c=74febd74-bf6c-4e40-ae7c-f2dd9ca5a1d8; intercom-device-id-fe4ce68d4a8352909f553b276994db414d33a55c=25491d58-d2a8-434e-96a1-d955c20ab7e6; __cf_bm=khpmWkEdYt97.33A75rF__NQF5p_ll2h4.hnuiyZZVE-1737445741-1.0.1.1-3__mz8Vs.hT_XPsEHFBE.bfUXro3ce_IUxcRfZztZrxLVXwC9nUXK.CYqqzCKzYZ3C0Ojg0ljPrWN3rjNoq9iQ; first_visit=1737445743; first_referer=; intercom-session-fe4ce68d4a8352909f553b276994db414d33a55c=; _ga_WZ46833KH9=GS1.1.1737445743.8.1.1737445921.60.0.0; csrf_token=hMRSIEYtCiYBrGrTyPNE3ZCHU-7QXqPVP3fCK44icbzKYuP0tBfxovCPEw62qE9JiLWNWY5r-P3hfXM1DuWbRw; _producthunt_session_production=IRk58oWhvq%2FBL0fHqyy94jY5vod0i%2FgMHXHLaT3fHHGbPrigssSr7P3kIEMUaH8yfGpf4X5IaBYfwk%2B5FXt2ckqVI1hY2GwsZ%2Fx3LYz8Ldb%2FFnA4KQps1lhjCRhMjM8vKhCzWJZs7SQstMvMh1THoAudtXeDOiUQg%2BLGnSBO5SgqgPyUV9XbI6kOhKC1cV34XFl3CcBiavWcg%2F4%2FzE70u%2BfYPwRkvNngBCEt8OYpelnD1v1PJyyD%2FFqCtXIeT97FatwdhZwtUsg%2B7J2iPF%2BRNouS438SHpb%2Bxn81YaEXQpeY%2BfpDigxMI9pF47tga4tw2ANdzmIeQe0bOX3ltw%3D%3D--CRpZJN%2B3F8xgVzdE--imS5GSij5r0hJJHYCFwWVQ%3D%3D"
    sha256_hash_value = "76e07923b064b4b128aff46af2fd3b72eed611dbd588f161aa02091d4e87517e"
    slug_value = "ai-software"

    fetcher = ProductHuntFetcher(save_directory, cookie_value, sha256_hash_value, slug_value)
    fetcher.fetch_all_products(limit=50)
