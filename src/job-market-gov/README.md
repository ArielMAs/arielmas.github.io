# Job Market Gov
Job Market Gov is a data processing tool designed to fetch, process, and store job market data from the USAJobs API. This project extracts relevant job listings from the API, including position details, location information, and remuneration data, then stores the data in Parquet files for further analysis. The project is modular, allowing for easy updates and integration with other data sources.

## Features
* Fetch job listings from the USAJobs API with configurable parameters for date range and pagination.
* Extract key job details, such as position title, location, salary range, and duties.
* Store processed data in Parquet format for efficient querying and analysis.
* Use Docker for easy deployment and reproducibility.

## Requirements
* Python 3.12 or later
* Docker (for containerized deployment)
* API credentials from the [USAJobs API](https://developer.usajobs.gov/)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/ArielMAs/arielmas.github.io/job-market-gov
    cd job-market-gov
    ```
2. Build the Docker image:
    ```bash
    sudo docker build --build-arg API_EMAIL=<api_email> --build-arg API_AUTH=<api_auth> -t <image_name> .
    ```
3. Run the Docker container:
    ```bash
    docker run <image_name_or_id>
    ```
## Local development
To run the job listing fetch and processing manually (outside of Docker on Linux):
1. Install uv (if not installed)
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2. Install bash dependencies
    ```bash
    apt-get update && apt-get install -y curl \
                                         jq \
                                         python3.12
    ```
3. Export enviroment variables 
    ```bash
    export API_AUTH=<api_auth>
    export API_EMAIL=<api_email>
    ```
4. Run API pull script
    ```bash
    chmod +x ./run.sh && ./run.sh
    ```
5. Initiate uv virtual environment and run structured data processor script
    ```bash
    uv venv && \
    source .venv/bin/activate && \
    uv sync --frozen && \
    python3 job_listing.py main.json --first_run True
    ```

* Make sure you provide the necessary API credentials as environment variables:

Once the Docker container is running, the script fetches job listings from the USAJobs API and processes them into structured data files. You can configure the API to fetch job listings for the last 0-60 days and store them in Parquet files for later analysis.

# Next steps
* Automate this process to run every X amount of days.
* Explore, clean, and analyse data