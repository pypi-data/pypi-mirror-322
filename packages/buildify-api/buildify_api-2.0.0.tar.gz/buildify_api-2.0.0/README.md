# Buildify API Library: The Ultimate Guide for Developers

## Overview

The **Buildify API Library** is a powerful Python package tailored for developers looking to seamlessly integrate with the **[Buildify API](https://www.getbuildify.com/)**. It simplifies the process of accessing, parsing, and processing data for **real estate projects**, making it an essential tool for those building applications in real estate analytics, property management, or related industries.

This library provides an end-to-end solution for developers, encompassing data extraction, normalization, and processing. With built-in utilities for handling associated project assets like floor plans and photos, the library bridges the gap between raw API data and actionable insights.

---

## Why Use Buildify API Library?

- **Simplified API Integration**: Automates the fetching of real estate project data directly from the Buildify API.  
- **Data Processing Tools**: Handles deposit schedules, occupancy dates, and project structures effortlessly.  
- **File Management**: Automates downloading and organizing project files such as images and floor plans.  
- **Customizable**: Easily adaptable to meet the unique needs of your application.

Here's an improved version of the **Key Takeaways** block, with clear and concise points:

---

### Key Takeaways:

- **`ProjectDataReader`**: Dynamically scans the specified directory for project folders and identifies valid structures. It initializes `SchemaProject` instances for each folder, streamlining the processing pipeline.  
- **`SchemaProject`**: Simplifies access to project-related data (e.g., `data.json`, `map.json`) by abstracting file-specific logic, ensuring developers can focus on higher-level workflows instead of low-level file handling.  
- **`ProjectDataImporter`**: Demonstrates how `SchemaProject` can be utilized to build custom workflows. This class offers flexibility for extending the library's core functionality to meet unique project requirements.  
- **Scalable Workflow**: The combination of `ProjectDataReader` and `SchemaProject` provides a modular, scalable way to parse and process real estate data, making the library suitable for projects of any size.  

---

## Step-by-Step Workflow: Parse, Process, and Generate

---

## Installation

1. Install the package and its dependencies:
   ```bash
   pip install buildify-api
   ```

2. Ensure you have an API key from [Buildify API](https://buildify.readme.io/reference/welcome-api) to access the data.

---

## Workflow

The library's workflow consists of multiple sequential steps. Below is a detailed explanation of each step:

### 1. Define API Key and Output Directory
Before starting, you need to specify your API key and the directory where the data will be stored.

```python
api_key = "YOUR_API_KEY"
output_directory = "./data/projects"
```

This directory will hold all processed files, including:
- **Raw project data**: Saved as `data.json`.
- **Associated files**: Photos, floor plans, etc., saved in `files/`.

---

### 2. Parse and Save Project Data

The `BuildifyApiParser` fetches project data from the API and saves it in a structured format. Each project is stored in its own folder, with raw data saved as `data.json`.

```python
from buildify_api import BuildifyApiParser

parser = BuildifyApiParser(
    api_key=api_key,
    provinces=['on', 'bc'],  # Specify provinces to parse
    page_start=0,            # Starting page for API pagination
    limit=None,              # Maximum number of projects (None for no limit)
    output_dir=output_directory,
    clean_output_dir=True    # Clear the directory before parsing
)

def process_project_callback(project_data):
    print(f"Processed project: {project_data['name']}")

parser.parse(process_project_callback)
```

**Generated Files:**
- `data.json`: Raw project data fetched from the API.

---

### 3. Download and Process Related Files

Use the `DataDownloader` to download associated files, such as photos and floor plans. These are saved in organized directories with metadata stored in `map.json`.

```python
from buildify_api import DataDownloader

processor = DataDownloader(
    output_directory=output_directory,
    download_files=True  # Set to True to download files
)
processor.process()
```

**Generated Files:**
- `files/`: Folder containing downloaded assets (e.g., photos, floor plans).
- `map.json`: Metadata file mapping assets to their respective projects.

---

### 4. Process Deposit Data

The `DepositParser` parses deposit structures from `data.json` and generates a `deposits.json` file with structured information.

```python
from buildify_api import DepositParser

processor = DepositParser(output_directory)
processor.process_all_object_folders()
```

**Generated Files:**
- `deposits.json`: Contains structured deposit data and original milestones.

---

### 5. Generate Deposits for Projects and Suites

Deposit schedules can be generated for both projects and individual suites using the `ProjectDepositsGenerator` and `SuiteDepositsGenerator`.

#### Project Deposits
```python
from buildify_api import ProjectDepositsGenerator

ProjectDepositsGenerator.test_method()
```

#### Suite Deposits
```python
from buildify_api import SuiteDepositsGenerator

SuiteDepositsGenerator.test_method()
```

**Generated Files:**
- `deposits_project.json`: Contains generated project-level deposit schedules.
- `deposits_suites.json`: Contains generated suite-level deposit schedules.

---

### 6. Parse Occupancy Dates

Normalize occupancy-related dates using `OccupancyDateParser`. Dates like `firstOccupancyDate` and `estimatedCompletionDate` are processed and saved as `parsed_date.json`.

```python
from buildify_api import OccupancyDateParser

occupancy_parser = OccupancyDateParser(output_directory)
occupancy_parser.parse()
```

**Generated Files:**
- `parsed_date.json`: Contains normalized occupancy dates.

---

### 7. Process Final Deposits

Consolidate all processed data, including deposit schedules and occupancy dates, into final deposit files for integration or reporting.

```python
from buildify_api import DepositsFinal

final_processor = DepositsFinal(output_directory)
final_processor.process()
```

**Generated Files:**
- `deposits_project.json`: Consolidated project-level deposit data.
- `deposits_suites.json`: Consolidated suite-level deposit data.

---

## File Structure

After completing the workflow, the output directory will look like this:
```
./data/projects/
├── PROJECT_ID/
│   ├── data.json             # Raw project data
│   ├── deposits.json         # Structured deposit data
│   ├── deposits_project.json # Project-level deposit schedules
│   ├── deposits_suites.json  # Suite-level deposit schedules
│   ├── files/
│   │   ├── photos/           # Downloaded photos
│   │   └── floorPlans/       # Downloaded floor plans
│   ├── map.json              # Metadata for associated files
│   └── parsed_date.json      # Normalized occupancy dates
```

---

## Example Code

Here’s the full workflow combined:

```python
from buildify_api import (
    BuildifyApiParser,
    DataDownloader,
    DepositParser,
    ProjectDepositsGenerator,
    SuiteDepositsGenerator,
    OccupancyDateParser,
    DepositsFinal
)

# Define API key and output directory
api_key = "YOUR_API_KEY"
output_directory = "./data/projects"

# Step 1: Parse project data
parser = BuildifyApiParser(
    api_key=api_key,
    provinces=['on', 'bc'],
    output_dir=output_directory,
    clean_output_dir=True
)
parser.parse(lambda project: print(f"Processed: {project['name']}"))

# Step 2: Download associated files
downloader = DataDownloader(output_directory, download_files=True)
downloader.process()

# Step 3: Parse deposit data
deposit_parser = DepositParser(output_directory)
deposit_parser.process_all_object_folders()

# Step 4: Generate deposits for projects and suites
ProjectDepositsGenerator.test_method()
SuiteDepositsGenerator.test_method()

# Step 5: Parse occupancy dates
occupancy_parser = OccupancyDateParser(output_directory)
occupancy_parser.parse()

# Step 6: Process final deposits
final_processor = DepositsFinal(output_directory)
final_processor.process()
```

---

### Output Example

Given a `data` directory structured like this:
```
data/
├── project_1/
│   ├── data.json
│   ├── deposits_project.json
│   ├── deposits_suites.json
│   ├── map.json
│   ├── parsed_date.json
├── project_2/
│   ├── data.json
│   ├── deposits_project.json
│   ├── map.json
│   ├── parsed_date.json
```

---

# Data Reader

The **Data Reader** module provides a streamlined way to parse, process, and load real estate project data stored in a directory structure. The workflow is built around two primary classes:

1. **`ProjectDataReader`**:
   - Reads and validates project directories from the specified `data` folder.
   - Returns a list of `SchemaProject` instances, each representing a single project's data.

2. **`SchemaProject`**:
   - Provides methods to access key project files (e.g., `data.json`, `map.json`, etc.).
   - Simplifies file handling by abstracting JSON file reads and error handling.

---

# ProjectDataReader

### 1. **ProjectDataReader**: Scanning the Data Directory
The `ProjectDataReader` initializes with the path to a `data` folder. It scans for subdirectories, each representing a project. For every valid project directory, a `SchemaProject` instance is created.

### 2. **SchemaProject**: Accessing Project Files
The `SchemaProject` class provides methods to retrieve data from key JSON files in a project folder, such as:
- `data.json`: General project information.
- `map.json`: Metadata for associated files like photos and floor plans.
- `deposits_project.json`: Deposit schedules at the project level.
- `parsed_date.json`: Normalized occupancy and completion dates.

---

## Example Usage

### Full Workflow Example

```python
import os
from buildify_api import ProjectDataReader, SchemaProject, get_logger

# Configure logger
logger = get_logger(__name__)

# Define ProjectDataImporter class
class ProjectDataImporter:
    def __init__(self, project: SchemaProject):
        """
        Initializes the ProjectDataImporter with the data extracted from a SchemaProject instance.

        Args:
            project (SchemaProject): An instance of SchemaProject containing project data.
        """
        self.project_id = project.project_id
        self.data = project.get_data()
        self.parsed_date = project.get_parsed_date()
        self.deposits_project = project.get_deposits_project()
        self.deposits_suites = project.get_deposits_suites()
        self.map_data = project.get_map()

    def process(self):
        """
        Processes and returns the data for the project.
        """
        return {
            "project_id": self.project_id,
            "data": self.data,
            "parsed_date": self.parsed_date,
            "deposits_project": self.deposits_project,
            "deposits_suites": self.deposits_suites,
            "map_data": self.map_data,
        }

# Define the main function
if __name__ == "__main__":
    # Define the directory containing project data
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(base_dir, "data")

    # Initialize ProjectDataReader
    reader = ProjectDataReader(data_directory)
    projects = reader.process_projects()

    # Process each project
    processed_projects = []
    for project in projects:
        try:
            importer = ProjectDataImporter(project)
            processed_project = importer.process()
            processed_projects.append(processed_project)
            logger.info(f"Successfully processed project: {project.project_id}")
        except Exception as e:
            logger.error(f"Failed to process project {project.project_id}: {e}")

    # Final summary
    logger.info(f"Processed {len(processed_projects)} projects successfully.")
```

---

## About Developer

The **Buildify API Library** is developed by [Unrealos](https://unrealos.com)  , a leading software development company specializing in **PaaS**, **SaaS**, and **web services**. Our expertise lies in integrating advanced AI solutions into business processes to create robust tools for real estate, finance, and other complex industries.

---

## License

This library is licensed under the MIT License. See [LICENSE](./LICENSE) for more details.
