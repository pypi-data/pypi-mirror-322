import os
import pytest
import json
from koreancar.main import VehicleMainFetcher, VehicleDataFetcher

def test_vehicle_data_fetcher():
    # Define the paths for the directories
    data_list_dir = "data/list"
    data_vehicles_dir = "data/vehicles"

    # Check that `page_0.json` exists
    page_0_path = os.path.join(data_list_dir, "page_0.json")
    assert os.path.exists(page_0_path), f"{page_0_path} does not exist!"

    # Instantiate the VehicleMainFetcher
    fetcher = VehicleMainFetcher(input_dir=data_list_dir, output_dir=data_vehicles_dir)

    # Process all files in the `data/list` directory
    fetcher.process_all_files()

    # Dynamically read IDs from `page_0.json` and validate the output
    with open(page_0_path, "r", encoding="utf-8") as f:
        page_data = json.load(f)

        for item in page_data.get("SearchResults", []):
            listing_id = item.get("Id")
            assert listing_id is not None, "Listing ID is missing in SearchResults."

            # Check if the folder and main.json file exist for each listing_id
            vehicle_folder = os.path.join(data_vehicles_dir, listing_id)
            main_file_path = os.path.join(vehicle_folder, "main.json")

            assert os.path.exists(vehicle_folder), f"Folder {vehicle_folder} was not created."
            assert os.path.exists(main_file_path), f"File {main_file_path} was not created."

            # Instantiate the VehicleDataFetcher
            vehicle_data_fetcher = VehicleDataFetcher(output_dir=data_vehicles_dir)

            # Process additional data only after confirming `main.json` exists
            vehicle_data_fetcher.process_vehicle_data(listing_id)

            # Validate additional files generated for the vehicle
            additional_files = [
                "history.json",
                "inspection.json",
                "diagnosis.json",
                "clean_encar.json",
                "vehicle_options.json",
                "extend_warranty.json",
                "vehicle_category.json",
            ]
            for file_name in additional_files:
                file_path = os.path.join(vehicle_folder, file_name)
                assert os.path.exists(file_path), f"File {file_path} was not created."

            # Break after validating the first listing ID to keep the test efficient
            break
