# California Wildfire Dashboard (2014-2024)
## Overview
This project provides an interactive dashboard to explore trends, financial losses, and the human impact of wildfires in California from 2014 to 2024. The dashboard offers various visualizations to help users better understand wildfire frequency, area burned, financial losses, and fatalities across different counties and years.

The key metrics are displayed on the main page, offering insights into the scale of the wildfires over the past decade, while the other pages provide more in-depth analysis of seasonal trends, monthly and yearly wildfire data, and specific county-based statistics.

The source data can be found at [kaggle](https://www.kaggle.com/datasets/vivekattri/california-wildfire-damage-2014-feb2025).

* Source data was preprocessed & cleaned. Process can be seen in `preprocess.ipynb` 

# Running the Dashboard localy(Linux)
1. Clone the project and cd into it
2. If not installed, install uv
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
3. Initialize project & create virtual environment using uv 
```
uv init
```
```
uv venv
```
4. Sync venv with project dependencies(from pyproject.toml)
```
uv sync
```
6. Activate virtual environment
```
source .venv/bin/activate
```
5. Run streamlit localy
```
streamlit run Hello.py
```
# Deployment
1. Create requirements.txt for streamlit
```
uv pip compile pyproject.toml -o requirements.txt
```
2. Deploy on streamlit using streamlit GUI