import argparse
import os
import fiona.errors
import pandas as pd
import geopandas as gpd
import plotly.express as px


def object_to_int(df: pd.DataFrame, col_name: str, print_string: str) -> pd.DataFrame:
    """
    Convert an object column to int64
    @param df: The DataFrame
    @param col_name: The column name
    @param print_string: The string that will contain the data statistics
    @return: The DataFrame with the column converted to int64
    """
    # Since the lat column is of type object, we need to check if it contains any non-numeric values
    print_string += (f"\n\nNumber of rows with non-numeric lat : "
                     f"{pd.to_numeric(df[col_name], errors='coerce').isnull().sum():,}")

    # Get the rows with non-numeric lat
    print_string += (f"\nRows with non-numeric lat : "
                     f"{df[pd.to_numeric(df[col_name], errors='coerce').isnull()][col_name].to_dict()}")

    # Convert the lat column to numeric
    # Remove hyphens from the column
    df[col_name] = df[col_name].str.replace('-', '')

    # Step 3: Convert the column to integer type
    df[col_name] = df[col_name].astype(int)

    return df


def check_cols(col1: str, col2: str, df: pd.DataFrame, print_string: str) -> tuple[str, pd.DataFrame]:
    """
    Check the columns and convert them to int64 if necessary.
    @param col1: The first column
    @param col2: The second column
    @param df: The DataFrame
    @param print_string: The string that will contain the data statistics
    @return: The print string and the DataFrame
    """

    # Perform checks for both columns
    if df[col1].dtype == 'int64' and df[col2].dtype == 'int64':
        print_string += f"\n\n<br>Both {col1} and {col2} columns are of type int64."

    elif df[col1].dtype == 'object':
        print_string += f"\n\n<br>The {col1} column is of type object. Converting it to int64."
        df = object_to_int(df, col1, print_string)  # Convert the `col1` column to int64

    elif df[col2].dtype == 'object':
        print_string += f"\n\n<br>The {col2} column is of type object. Converting it to int64."
        df = object_to_int(df, col2, print_string)  # Convert the `col2` column to int64

    elif df[col1].dtype == 'object' and df[col2].dtype == 'object':
        print_string += f"\n\n<br>Both {col1} and {col2} columns are of type object. Converting them to int64."
        df = object_to_int(object_to_int(df, col1, print_string), col2, print_string)

    else:
        print_string += f"\n\n<br>The {col1} and {col2} columns are of type object"
        print_string += f"\n<br>Type of {col1} column : {df[col1].dtype}"
        print_string += f"\n<brType of {col2} column : {df[col2].dtype}"

    return print_string, df


def main():
    # Initialize command line arguments
    parser = argparse.ArgumentParser(description="Create scatter maps for South Carolina")
    parser.add_argument("csv_file", type=str, help="The path to the csv file")
    args = parser.parse_args()

    year: str = os.path.basename(args.csv_file).split('.')[-2][-4:]

    df = pd.read_csv(args.csv_file, low_memory=False)
    df['year'] = year

    # Check if the columns are consistent
    _, data = check_cols('lat', 'lon', df, "")

    # Group by county and year, count accidents
    accidents_by_county_year = df.groupby(['cty', 'year']).size().reset_index(name='accidents')

    county_dict = {
        1: 'Abbeville', 2: 'Aiken', 3: 'Allendale', 4: 'Anderson', 5: 'Bamberg',
        6: 'Barnwell', 7: 'Beaufort', 8: 'Berkeley', 9: 'Calhoun', 10: 'Charleston',
        11: 'Cherokee', 12: 'Chester', 13: 'Chesterfield', 14: 'Clarendon', 15: 'Colleton',
        16: 'Darlington', 17: 'Dillon', 18: 'Dorchester', 19: 'Edgefield', 20: 'Fairfield',
        21: 'Florence', 22: 'Georgetown', 23: 'Greenville', 24: 'Greenwood', 25: 'Hampton',
        26: 'Horry', 27: 'Jasper', 28: 'Kershaw', 29: 'Lancaster', 30: 'Laurens',
        31: 'Lee', 32: 'Lexington', 33: 'McCormick', 34: 'Marion', 35: 'Marlboro',
        36: 'Newberry', 37: 'Oconee', 38: 'Orangeburg', 39: 'Pickens', 40: 'Richland',
        41: 'Saluda', 42: 'Spartanburg', 43: 'Sumter', 44: 'Union', 45: 'Williamsburg',
        46: 'York'
    }

    # Replace the numerical representation with county names
    accidents_by_county_year['cty'] = accidents_by_county_year['cty'].replace(county_dict)

    # Try adding the county boundaries from the GeoJSON file
    file_name: str = "data/South Carolina County Boundaries.geojson"
    try:
        counties_gdf = gpd.read_file(file_name)
    except (fiona.errors.DriverError, FileNotFoundError):
        print(f"The '{file_name}' file was not found. Exiting...")
        exit()

    # Merge accident data with geospatial data
    merged_data = counties_gdf.merge(accidents_by_county_year, left_on='name', right_on='cty')

    # Calculate the center of South Carolina
    center_lat, center_lon = 33.8361, -81.1637

    # Create the Mapbox choropleth map
    fig = px.choropleth_mapbox(
        merged_data,
        geojson=merged_data.geometry,
        locations=merged_data.index,
        color='accidents',
        animation_frame='year',
        color_continuous_scale="Viridis",
        range_color=(0, merged_data['accidents'].max()),
        mapbox_style="carto-positron",
        zoom=6.5,
        center={"lat": center_lat, "lon": center_lon},
        opacity=0.7,
        labels={'accidents': 'Number of Accidents'},
        hover_name='name',  # Add county name to hover info
        hover_data={'accidents': True, 'name': False},  # Show accidents, hide redundant name
        title='Traffic Accidents in South Carolina Counties Over Time'
    )

    # Show the figure
    save_file: str = f"./output/choropleth_{year}.html"
    fig.write_html(save_file)
    print(f"The choropleth map has been saved to '{save_file}'.")


if __name__ == "__main__":
    main()
