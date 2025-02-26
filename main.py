
import pandas as pd
import geopandas as gpd
import folium

# Load School Data
schools_df = pd.read_csv(r"C:\Users\User\My_programs\Conn\data\School_report_page_10_out_of_293_dated_26022025_023330.csv")

# Load Cell Towers Data
cell_towers_df = pd.read_csv(r"C:\Users\User\My_programs\Conn\data\641.csv", names=[
    "radio", "mcc", "mnc", "area", "cell", "unit", "lat", "lon", 
    "range", "samples", "changeable", "created", "updated", "averageSignal"
])

# Load Buildings Data
buildings_gdf = gpd.read_file(r"C:\Users\User\My_programs\Conn\data\output.geojson")

# Create an interactive map centered in Uganda
uganda_map = folium.Map(location=[1.5, 32.5], zoom_start=7)

### 🔵 Add Schools (Blue Markers)
for index, row in schools_df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"School: {row['School Name']}",
        icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa")
    ).add_to(uganda_map)

### 🟢 Add Cell Towers (Green Circles with Range Radius)
for index, row in cell_towers_df.iterrows():
    folium.Circle(
        location=[row["lon"], row["lat"]],
        radius=row["range"],  # Adjusted to actual tower range
        popup=f"Cell Tower ID: {row['cell']}<br>Network: {row['radio']}<br>Range: {row['range']}m",
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=0.3
    ).add_to(uganda_map)

### 🟠 Add Buildings (Orange Polygons)
for _, building in buildings_gdf.iterrows():
    folium.GeoJson(building.geometry, style_function=lambda x: {
        'fillColor': 'orange',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5
    }).add_to(uganda_map)

# Save and open the interactive map
uganda_map.save("uganda_connectivity_map.html")
print("Map saved as uganda_connectivity_map.html. Open in a browser to view.")
