import folium
import pandas as pd
# Load cell towers dataset (used previously)
cell_towers_file = r"C:\Users\User\My_programs\Conn\data\641.csv"
cell_towers_df = pd.read_csv(cell_towers_file, names=[
    "radio", "mcc", "mnc", "area", "cell", "unit", "lat", "lon",
    "range", "samples", "changeable", "created", "updated", "averageSignal"
])

poorly_connected_schools = pd.read_csv(r"C:\Users\User\My_programs\Conn\poorly_connected_schools.csv")
# Convert school locations to a NumPy array


# Load new tower locations
new_towers_df = pd.read_csv(r"C:\Users\User\My_programs\Conn\new_suggested_towers.csv")

# Create an interactive map centered on Uganda
uganda_map = folium.Map(location=[1.5, 32.5], zoom_start=7)

# 🔵 Add Poorly Connected Schools (Red)
for _, row in poorly_connected_schools.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"School: {row['School Name']}",
        icon=folium.Icon(color="red", icon="times-circle", prefix="fa")
    ).add_to(uganda_map)

# 🟢 Add Existing Cell Towers (Green)
for _, row in cell_towers_df.iterrows():
    folium.Circle(
        location=[row["lat"], row["lon"]],
        radius=row["range"],
        popup=f"Cell Tower ID: {row['cell']}<br>Range: {row['range']}m",
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=0.3
    ).add_to(uganda_map)

# ⚡ Add New Suggested Towers (Black)
for _, row in new_towers_df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup="Suggested New Tower Location",
        icon=folium.Icon(color="black", icon="bolt", prefix="fa")
    ).add_to(uganda_map)

# Save and open the interactive map
uganda_map.save(r"C:\Users\User\My_programs\Conn\uganda_optimized_connectivity_map.html")
print("✅ Optimized connectivity map saved as uganda_optimized_connectivity_map.html.")
