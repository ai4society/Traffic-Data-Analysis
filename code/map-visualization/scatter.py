from pathlib import Path
import pandas as pd
import folium as fm
from folium.plugins import MarkerCluster
from random import sample
import json
from shapely.geometry import Point, Polygon
import os.path
import argparse


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


def filter_points(df: pd.DataFrame, len_0: int, print_string: str, year: str, print_stats: bool) -> tuple[str, pd.DataFrame]:
    """
    Filter points and calculate exclusion percentage.
    @param df: The DataFrame
    @param len_0: The initial length of the data
    @param print_string: The string that will contain the data statistics
    @param year: The year of the data
    @param print_stats: Whether to print the statistics file or not
    @return: The print string and the DataFrame
    """

    # Load the GeoJSON file in a try-except block
    file_name: str = "data/south carolina.geojson"
    try:
        with open(file_name, 'r') as f:
            sc_geojson = json.load(f)
    except FileNotFoundError:
        print(f"The '{file_name}' was not found. Exiting...")
        # Remove the data_statistics file if args.print_stats is True
        if print_stats:
            os.remove(f"./output/data_statistics_{year}.md")
        exit()

    # Extract coordinates and create a Shapely polygon
    sc_coords = sc_geojson['geometry']['coordinates'][0]
    sc_polygon = Polygon(sc_coords)

    # Filter points and calculate exclusion percentage
    len_1 = df.shape[0]  # New length

    df['in_sc'] = df.apply(lambda row: sc_polygon.contains(Point(row['lon'], row['lat'])), axis=1)
    df = df[df['in_sc']]  # Keep only points within South Carolina

    print_string += f"\n\nPoints after pre-processing : {len_1:,}"
    print_string += f"\n<br>Points within SC            : {df.shape[0]:,}"
    print_string += f"\n<br>Excluded points             : {(len_1 - df.shape[0]):,}"
    print_string += f"\n<br>Exclusion percentage        : {(len_1 - df.shape[0]) / len_1:.2%}"

    print_string += (f"\n\n<br>Total reduction (after pre-processing & state filtering)            : "
                     f"{(len_0 - df.shape[0]):,}")
    print_string += (f"\n<br>Total reduction percentage (after pre-processing & state filtering) : "
                     f"{(len_0 - df.shape[0]) / len_0:.2%}")

    return print_string, df


def create_map(df: pd.DataFrame, year: str, color_map: dict[int, str]) -> None:
    """
    Create a map using Folium.
    @param df: The DataFrame
    @param year: The year of the data
    @param color_map: The color mapping for the `tway` column
    """
    # Create a map centered on South Carolina
    sc_center_lat, sc_center_lon = 33.8361, -81.1637  # Approximate center of SC
    m = fm.Map(location=[sc_center_lat, sc_center_lon], zoom_start=7)

    # # Create a MarkerCluster
    # marker_cluster = MarkerCluster().add_to(m)

    # Create a MarkerCluster with custom options
    marker_cluster = MarkerCluster(
        options={
            'maxClusterRadius': 50,  # Maximum radius of a cluster in pixels
            # 'spiderfyOnMaxZoom': False,  # Disable spiderifying (spreading out markers) on max zoom
        }
    ).add_to(m)

    # Create mapping for the `tway` column:
    tway_map = {1: 'Two-way, not divided',
                2: 'Two-way, divided, unprotected median',
                3: 'Two-way, divided, barrier',
                4: 'One way',
                8: 'Other'}

    # Create mapping for the `day` column:
    day_map = {1: 'Sunday',
               2: 'Monday',
               3: 'Tuesday',
               4: 'Wednesday',
               5: 'Thursday',
               6: 'Friday',
               7: 'Saturday'}

    # Add markers to the cluster
    for idx, row in df.iterrows():
        fm.Marker(
            popup=fm.Popup(f"""
            <b>Accident Number:</b> {row['ano']}<br>
            <b>Trafficway:</b> {tway_map.get(row['tway'], 'Other')}<br>
            <b>Day:</b> {day_map.get(row['day'], 'Unknown')}<br>
            """, max_width="100%"),
            location=[row['lat'], row['lon']],
            icon=fm.Icon(color=color_map.get(row['tway'], 'gray')),
            lazy=True
        ).add_to(marker_cluster)

    # Create a list to hold each line of the legend
    legend_lines = []

    # Iterate over the color_map dictionary
    for tway, color in color_map.items():
        # Create a line for the legend
        line = (f'&nbsp; <i class="fa fa-map-marker fa-2x" style="color:{color}"></i>&nbsp; '
                f'{tway_map.get(tway, "Other")} <br>')
        # Add the line to the list
        legend_lines.append(line)

    # Join all the lines together to form the complete legend
    legend_content = '\n'.join(legend_lines)

    # Create the legend HTML
    legend_html = f'''
    <div style="position: fixed; bottom: 20px; left: 50px; width: auto; height: auto;
        border:2px solid grey; z-index:9999; font-size:14px; background-color:white;
        padding: 10px;">&nbsp; <b> Type of Way </b><br>
        {legend_content}
    </div>
    '''
    m.get_root().html.add_child(fm.Element(legend_html))  # Add the legend to the map

    # Add borders to the map for South Carolina
    # Source: https://nagasudhir.blogspot.com/2021/07/draw-borders-from-geojson-paths-in.html
    # style options - https://leafletjs.com/reference-1.7.1.html#path
    bordersStyle = {
        'color': 'green',
        'weight': 2,
        'fillColor': 'blue',
        'fillOpacity': 0.1
    }

    # Try adding the county boundaries from the GeoJSON file
    file_name: str = "data/South Carolina County Boundaries.geojson"
    try:
        fm.GeoJson(
            data=(open(file_name, 'r').read()),
            name="South Carolina",
            style_function=lambda x: bordersStyle).add_to(m)
    except FileNotFoundError:
        print(f"The '{file_name}' file was not found. Exiting...")
        exit()

    # Save the map
    f_name: str = f"./output/sc_incidents_{year}.html"
    m.save(f_name)
    print(f"Map has been saved as '{f_name}'")


def mapping(file_path: str, year: str, print_stats: bool) -> None:
    """
    Process the data and create the map.
    :param file_path: The path to the csv file
    :param year: The year of the data
    :param print_stats: Whether to print the statistics file or not
    """
    print(f"Processing data for the year {year}...")

    # Load the data
    df = pd.read_csv(file_path, low_memory=False)
    len_0: int = df.shape[0]

    # Define string that will contain the data statistics
    print_string: str = ""
    print_string += f"Initial length of the data for the year {year} : {len_0:,}"

    print_string, df = check_cols('lat', 'lon', df, print_string)

    # Check for rows with lat = 0 or lon = 0
    print_string += f"\n\nNumber of rows with lat = 0               : {(df['lat'] == 0).sum():,}"
    print_string += f"\n<br>Number of rows with lon = 0               : {(df['lon'] == 0).sum():,}"
    print_string += f"\n<br>Number of rows with lat and lon = 0       : {((df['lat'] == 0) & (df['lon'] == 0)).sum():,}"
    print_string += f"\n<br>Number of rows with either lat or lon = 0 : {((df['lat'] == 0) | (df['lon'] == 0)).sum():,}"

    # Remove rows with lat = 0 or lon = 0
    df = df[(df['lat'] != 0) & (df['lon'] != 0)]
    print_string += f"\n\nLength of data after removing rows with lat = 0 or lon = 0 : {df.shape[0]:,}"
    print_string += (f"\n<br>Percentage of rows removed                                 :"
                     f" {((len_0 - df.shape[0]) / len_0):.2%}")

    # Convert lat and lon to correct decimal degrees
    df['lat'] = df['lat'] / 1_000_000
    df['lon'] = - (df['lon'] / 1000000)  # Note the negative sign for longitude

    # Filter data
    print("Filtering data...")
    print_string, df = filter_points(df, len_0, print_string, year, print_stats)
    print_string += "\n---"

    # Save the data statistics to a file if args.print_stats is True
    if print_stats:
        file_name: str = f"./output/data_statistics_{year}.md"
        print(f"Saving data statistics to '{file_name}'")

        with open(file_name, 'a') as f:
            f.write(f"\n\n## Data Statistics for the year {year}\n")
            f.write(print_string)

    # 5 of the possible colors for Folium
    possible_colors = ['blue', 'darkgreen', 'purple', 'orange', 'red']

    # Define color mapping for 'tway'
    color_map = {num: col for num, col in zip(df['tway'].unique(), sample(possible_colors, len(df['tway'].unique())))}

    # Create the map
    print("Creating the map...")
    create_map(df, year, color_map)


def main():
    # Initialize command line arguments
    parser = argparse.ArgumentParser(description="Create scatter maps for South Carolina")

    # Add an argument for the csv file path
    # Add an argument flag whether to print the statistics file or not
    parser.add_argument("csv_file", type=str, help="The path to the csv file")
    parser.add_argument("--print_stats", action="store_true",
                        help="Print the statistics file. Default is False. To print, use this flag.")
    args = parser.parse_args()

    year: str = os.path.basename(args.csv_file).split('.')[-2][-4:]
    Path("./output").mkdir(parents=True, exist_ok=True)

    # If printing stats, the reinitialize the data_stats file
    if args.print_stats:
        print("Since the print_stats flag is True, the data statistics file will be initialized.")
        with open(f"./output/data_statistics_{year}.md", 'w') as f:
            f.write("# Data Statistics\n")
    else:
        print("Printing data statistics is turned off.")

    mapping(args.csv_file, year, print_stats=args.print_stats)


if __name__ == "__main__":
    main()
