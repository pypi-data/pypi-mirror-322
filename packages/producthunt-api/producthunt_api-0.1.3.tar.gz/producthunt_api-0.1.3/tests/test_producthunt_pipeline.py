import os
import pytest
from unittest.mock import MagicMock, patch
from producthunt_api import ProductHuntPipeline

@pytest.fixture
def pipeline():
    """
    Pytest fixture to create a ProductHuntPipeline instance with mock directories and parameters.
    """
    test_directory = os.path.join(os.getcwd(), "test_downloads")
    cookie = "test_cookie"
    sha256_hash = "test_sha256_hash"
    slug = "test-slug"
    pipeline_instance = ProductHuntPipeline(
        directory=test_directory,
        cookie=cookie,
        sha256_hash=sha256_hash,
        slug=slug
    )
    yield pipeline_instance
    # Cleanup after the test
    if os.path.exists(test_directory):
        import shutil
        shutil.rmtree(test_directory)

@patch("producthunt_api.ProductHuntFetcher.fetch_all_products")
@patch("producthunt_api.ProductInfoManager.process_pages_and_fetch_products")
@patch("producthunt_api.JSONToCSVConverter.run")
def test_pipeline_run(mock_csv_run, mock_process_pages, mock_fetch_products, pipeline):
    """
    Test the full pipeline to ensure each component is called correctly.
    """
    # Mock methods
    mock_fetch_products.return_value = None
    mock_process_pages.return_value = None
    mock_csv_run.return_value = None

    # Run the pipeline
    pipeline.run(limit=10, max_threads=5)

    # Assert each component is called
    mock_fetch_products.assert_called_once_with(limit=10)
    mock_process_pages.assert_called_once_with(max_threads=5)
    mock_csv_run.assert_called_once()

def test_directories_creation(pipeline):
    """
    Test that directories are created during pipeline initialization.
    """
    assert os.path.exists(pipeline.pages_dir)
    assert os.path.exists(pipeline.products_dir)

if __name__ == "__main__":
    pytest.main(["-v", "test_producthunt_pipeline.py"])
