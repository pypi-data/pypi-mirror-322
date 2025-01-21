import os
import shutil

from .category import ProductHuntFetcher
from .product import ProductInfoManager
from .csv_converter import JSONToCSVConverter
from .utils.logger_config import get_logger

logger = get_logger(__name__)

class ProductHuntPipeline:
    """
    A unified pipeline class to manage fetching, processing, and converting Product Hunt data.
    """
    def __init__(self, directory, cookie, sha256_hash, slug):
        """
        Initialize the pipeline with directories and API parameters.

        :param directory: Base directory where all data will be stored.
        :param cookie: Cookie string for API authentication.
        :param sha256_hash: SHA256 hash for the persisted query.
        :param slug: Category slug to fetch data for.
        """
        self.directory = directory
        self.pages_dir = os.path.join(directory, "pages")
        self.products_dir = os.path.join(directory, "products")
        self.output_csv = os.path.join(directory, "products.csv")
        self.cookie = cookie
        self.sha256_hash = sha256_hash
        self.slug = slug

        # Clean and recreate the base directory
        if os.path.exists(self.directory):
            logger.info(f"Removing existing directory: {self.directory}")
            shutil.rmtree(self.directory)
        os.makedirs(self.pages_dir, exist_ok=True)
        os.makedirs(self.products_dir, exist_ok=True)

    def run(self, limit=None, max_threads=10):
        """
        Run the pipeline: Fetch data, process products, and convert to CSV.

        :param limit: Maximum number of products to fetch (default is None).
        :param max_threads: Number of threads to use for processing (default is 10).
        """
        logger.info("Starting Product Hunt pipeline.")

        # Step 1: Fetch data
        logger.info("Fetching data from Product Hunt API.")
        fetcher = ProductHuntFetcher(self.pages_dir, self.cookie, self.sha256_hash, self.slug)
        fetcher.fetch_all_products(limit=limit)

        # Step 2: Process pages and fetch product data
        logger.info("Processing pages and fetching product details.")
        manager = ProductInfoManager(self.pages_dir, self.products_dir)
        manager.process_pages_and_fetch_products(max_threads=max_threads)

        # Step 3: Convert JSON data to CSV
        logger.info("Converting product data to CSV.")
        converter = JSONToCSVConverter(self.products_dir, self.output_csv)
        converter.run()

        logger.info("Product Hunt pipeline completed successfully.")

if __name__ == "__main__":
    directory = os.path.join(os.getcwd(), "downloads")

    cookie_value = "_ga=GA1.1.660153458.1733116004; ajs_anonymous_id=6e0a9dd4-91ff-4476-bd63-58de4f020ab9; visitor_id=8d3991f1-624f-4b56-aea1-fc4f44bcb326; track_code=7e715c9281; intercom-id-fe4ce68d4a8352909f553b276994db414d33a55c=74febd74-bf6c-4e40-ae7c-f2dd9ca5a1d8; intercom-device-id-fe4ce68d4a8352909f553b276994db414d33a55c=25491d58-d2a8-434e-96a1-d955c20ab7e6; __cf_bm=khpmWkEdYt97.33A75rF__NQF5p_ll2h4.hnuiyZZVE-1737445741-1.0.1.1-3__mz8Vs.hT_XPsEHFBE.bfUXro3ce_IUxcRfZztZrxLVXwC9nUXK.CYqqzCKzYZ3C0Ojg0ljPrWN3rjNoq9iQ; first_visit=1737445743; first_referer=; intercom-session-fe4ce68d4a8352909f553b276994db414d33a55c=; _ga_WZ46833KH9=GS1.1.1737445743.8.1.1737445921.60.0.0; csrf_token=hMRSIEYtCiYBrGrTyPNE3ZCHU-7QXqPVP3fCK44icbzKYuP0tBfxovCPEw62qE9JiLWNWY5r-P3hfXM1DuWbRw; _producthunt_session_production=IRk58oWhvq%2FBL0fHqyy94jY5vod0i%2FgMHXHLaT3fHHGbPrigssSr7P3kIEMUaH8yfGpf4X5IaBYfwk%2B5FXt2ckqVI1hY2GwsZ%2Fx3LYz8Ldb%2FFnA4KQps1lhjCRhMjM8vKhCzWJZs7SQstMvMh1THoAudtXeDOiUQg%2BLGnSBO5SgqgPyUV9XbI6kOhKC1cV34XFl3CcBiavWcg%2F4%2FzE70u%2BfYPwRkvNngBCEt8OYpelnD1v1PJyyD%2FFqCtXIeT97FatwdhZwtUsg%2B7J2iPF%2BRNouS438SHpb%2Bxn81YaEXQpeY%2BfpDigxMI9pF47tga4tw2ANdzmIeQe0bOX3ltw%3D%3D--CRpZJN%2B3F8xgVzdE--imS5GSij5r0hJJHYCFwWVQ%3D%3D"
    sha256_hash_value = "76e07923b064b4b128aff46af2fd3b72eed611dbd588f161aa02091d4e87517e"
    slug_value = "ai-software"

    pipeline = ProductHuntPipeline(
        directory=directory,
        cookie=cookie_value,
        sha256_hash=sha256_hash_value,
        slug=slug_value
    )

    pipeline.run(limit=50, max_threads=10)