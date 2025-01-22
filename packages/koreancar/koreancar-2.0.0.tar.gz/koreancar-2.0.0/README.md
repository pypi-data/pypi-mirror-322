# Koreancar: Python Module for Encar.com Integration

**Koreancar** is a Python library designed for seamless interaction with [Encar.com](https://www.encar.com), a leading automotive marketplace in Korea. Developed by [Unrealos](https://unrealos.com), this library simplifies fetching and processing car listings, vehicle details, and related automotive data, making it an ideal solution for dealerships, analytics platforms, and developers working on car-related SaaS, PaaS, and web services.

---

## Features

- **Retrieve Car Listings**: Easily fetch paginated car listings with comprehensive details such as price, mileage, year, and model.
- **Detailed Vehicle Data**: Extract performance inspections, diagnostic information, warranty options, and more.
- **Structured JSON Data**: Organizes fetched data into easy-to-access JSON files for seamless integration into your projects.
- **Robust and Scalable**: Handles large datasets with error handling and retry mechanisms for reliable data fetching.
- **Customizable Workflow**: Tailor the library to meet your specific business needs, whether for SEO, analytics, or marketplace integration.

---

## Installation

Install the module via [PyPI](https://pypi.org/project/koreancar/):

```bash
pip install koreancar
```

---

## Quick Start Guide

### Fetch Car Listings and Detailed Vehicle Data

```python
import os
import json
from koreancar.main import CarListingParser, VehicleMainFetcher, VehicleDataFetcher

# Define directories for storing data
data_list_dir = "data/list"
data_vehicles_dir = "data/vehicles"

# Step 1: Fetch car listings
parser = CarListingParser(output_dir=data_list_dir, items_per_page=10)
parser.parse_pages(3)  # Fetch 3 pages of car listings

# Step 2: Process car listings to fetch main vehicle data
fetcher = VehicleMainFetcher(input_dir=data_list_dir, output_dir=data_vehicles_dir)
fetcher.process_all_files()

# Step 3: Fetch additional details for each listing dynamically
with open(os.path.join(data_list_dir, "page_0.json"), "r", encoding="utf-8") as f:
    listings = json.load(f)["SearchResults"]
    for listing in listings:
        listing_id = listing.get("Id")
        if listing_id:
            print(f"Processing vehicle data for listing ID: {listing_id}")
            vehicle_data_fetcher = VehicleDataFetcher(output_dir=data_vehicles_dir)
            vehicle_data_fetcher.process_vehicle_data(listing_id)

print("Data fetching and processing completed.")
```

---

## Directory Structure

After running the module, data is organized into the following directories:

- **`data/list`**: Contains paginated car listing files (`page_0.json`, `page_1.json`, etc.).
- **`data/vehicles`**: Contains directories for individual vehicles, identified by their listing ID, with the following files:
  - **`main.json`**: Core vehicle details.
  - **`history.json`**: Vehicle history records.
  - **`inspection.json`**: Performance inspection data.
  - **`diagnosis.json`**: Diagnostic details.
  - **`clean_encar.json`**: Cleaned Encar data.
  - **`vehicle_options.json`**: Available vehicle options.
  - **`extend_warranty.json`**: Extended warranty information.
  - **`vehicle_category.json`**: Category and manufacturer data.

---

## Use Cases

- **Automotive Marketplaces**: Build and maintain dynamic, up-to-date car listings.
- **Analytics Platforms**: Aggregate and analyze automotive data for market research and insights.
- **Car Dealership SaaS**: Automate inventory management with detailed vehicle information.
- **SEO Optimization**: Enhance automotive content with rich, structured data to improve search engine visibility.

---

## About Unrealos

[Koreancar](https://github.com/markolofsen/koreancar) was developed by **[Unrealos](https://unrealos.com)**, a company specializing in SaaS, PaaS, and web services. Unrealos integrates AI and cutting-edge technologies to deliver innovative solutions for businesses. For inquiries, contact us at [m@unrealos.com](mailto:m@unrealos.com).

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/markolofsen/koreancar/blob/main/LICENSE) file for details.