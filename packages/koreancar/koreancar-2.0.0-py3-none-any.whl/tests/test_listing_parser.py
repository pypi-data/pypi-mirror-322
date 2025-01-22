import os
import shutil
import pytest
from koreancar.main import CarListingParser

def test_parse_pages():
    # Define the path for the data/list directory
    data_dir = "data/list"

    # Clean up the directory before the test
    if os.path.exists("data"):
        shutil.rmtree("data")

    # Instantiate the parser
    parser = CarListingParser(output_dir=data_dir, items_per_page=12)
    
    pages = 2
    # Run the method to fetch and save 3 pages (This will simulate fetching 3 pages)
    parser.parse_pages(pages)  # This will fetch 3 pages (page_0, page_1, page_2)

    # Check if the files have been created in the "data/list" directory
    for i in range(pages):
        file_path = os.path.join(data_dir, f"page_{i}.json")
        assert os.path.exists(file_path), f"File {file_path} was not created"
