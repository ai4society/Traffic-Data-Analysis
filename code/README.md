# Traffic Data Analysis Code

This directory contains scripts for the 3 different analysis:

## Alive@25 Analysis
- `road_type.ipynb`: Python script to generate the traffic way class distribution across county categories for 2018.
- `injury_costs.ipynb`: iPython notebook to analyze the injury costs and generate visualizations.


## Collision Analysis
This directory contains scripts for the data analysis. The files are as follows:

- `2018_frequency_plots.ipynb`: iPython notebook to get the frequency of all the variables and then plot them.
- `injury_cost.ipynb`: iPython notebook to calculate the total cost of collision.
- `opening_files.ipynb` and `internship.ipynb`: iPython notebooks for preliminary data exploration before the analysis takes place.
- `rural_vs_urban.ipynb`: iPython notebook to plot cost of collisions based off rural, mostly rural, and urban classifications.

## Map Visualization

This directory contains scripts for plotting maps and other visualizations of the data. The files are as follows:

- `scatter.py`: A script for plotting scatter plot of the data.
    - Required files (_paths from the root folder of this repository_): 
      - `data/south carolina.geojson`: [download link](https://github.com/glynnbird/usstatesgeojson/blob/master/south%20carolina.geojson)
      - `data/South Carolina County Boundaries.geojson`: [download link](https://cartographyvectors.com/map/1123-south-carolina-with-county-boundaries)
    - Command Line Arguments:
        - `csv_file`: The path to the CSV file containing the data to be plotted.
        - `--print_stats`: An optional flag indicating whether to print the statistics of the data. Default is `False`.
    - Usage: `python scatter.py <csv_file> [--print_stats]`
    - Output: A scatter plot of the data and a statistics markdown file (if the `--print_stats` flag is used) under the `output/map-visualization/` directory of this repository.

- `choropleth.py`: A script for plotting choropleth map of the data.
    - Required files (_paths from the root folder of this repository_): 
      - `data/South Carolina County Boundaries.geojson`: [download link](https://cartographyvectors.com/map/1123-south-carolina-with-county-boundaries)
    - Command Line Arguments:
        - `csv_file`: The path to the CSV file containing the data to be plotted.
    - Usage: `python choropleth.py <csv_file>`
    - Output: A choropleth map of the data under the `output/map-visualization/` directory of this repository. 
