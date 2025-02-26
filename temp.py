import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from geopy.distance import geodesic

# ----------------------------------------------------------------------------
# 1) LOAD & CLEAN DATA
# ----------------------------------------------------------------------------

# Adjust file paths for your local environment
SCHOOLS_FILE = r"C:\Users\User\My_programs\Conn\data\School_report_page_10_out_of_293_dated_26022025_023330.csv"
TOWERS_FILE = r"C:\Users\User\My_programs\Conn\data\641.csv"
OUTPUT_FILE = r"C:\Users\User\My_programs\Conn\schools_with_connectivity_status.csv"

# Load schools
schools_df = pd.read_csv(SCHOOLS_FILE)

# Load towers - provide column names if missing
cell_towers_df = pd.read_csv(
    TOWERS_FILE, 
    names=[
        "radio", "mcc", "mnc", "area", "cell", "unit", "lon", "lat",
        "range", "samples", "changeable", "created", "updated", "averageSignal"
    ],
    # If your CSV includes headers, remove `names=...` and let pandas auto-detect
    # header=0
)

# Ensure lat/lon/range are numeric
for col in ["Latitude", "Longitude"]:
    if col in schools_df.columns:
        schools_df[col] = pd.to_numeric(schools_df[col], errors="coerce")

for col in ["lat", "lon", "range"]:
    if col in cell_towers_df.columns:
        cell_towers_df[col] = pd.to_numeric(cell_towers_df[col], errors="coerce")

# Drop rows with invalid lat/lon
schools_df.dropna(subset=["Latitude", "Longitude"], inplace=True)
cell_towers_df.dropna(subset=["lat", "lon", "range"], inplace=True)

# ----------------------------------------------------------------------------
# 2) (OPTIONAL) FILTER TOWERS TO UGANDA'S BOUNDING BOX
#    Use this if you suspect your towers might be outside Uganda
# ----------------------------------------------------------------------------
UGANDA_LAT_MIN, UGANDA_LAT_MAX = -1, 4
UGANDA_LON_MIN, UGANDA_LON_MAX = 29, 36

# Uncomment to apply bounding box filtering
"""
cell_towers_df = cell_towers_df[
    (cell_towers_df["lat"] >= UGANDA_LAT_MIN) & (cell_towers_df["lat"] <= UGANDA_LAT_MAX) &
    (cell_towers_df["lon"] >= UGANDA_LON_MIN) & (cell_towers_df["lon"] <= UGANDA_LON_MAX)
]
"""

# ----------------------------------------------------------------------------
# 3) CHECK FOR DUPLICATE TOWER COORDINATES & REMOVE IF NEEDED
# ----------------------------------------------------------------------------
cell_towers_df.drop_duplicates(subset=["lat", "lon"], inplace=True)

# ----------------------------------------------------------------------------
# 4) BUILD KDTree FOR FAST NEAREST-NEIGHBOR LOOKUP
# ----------------------------------------------------------------------------
if len(schools_df) == 0:
    print("❌ No valid schools found. Exiting.")
    exit()

if len(cell_towers_df) == 0:
    print("❌ No valid towers found. Exiting.")
    exit()

tower_coords = cell_towers_df[["lat", "lon"]].to_numpy()
school_coords = schools_df[["Latitude", "Longitude"]].to_numpy()

tree = cKDTree(tower_coords)

# ----------------------------------------------------------------------------
# 5) FIND NEAREST TOWER FOR EACH SCHOOL
# ----------------------------------------------------------------------------
distances, indices = tree.query(school_coords, k=1)

# Retrieve matching tower data
nearest_tower_ids = cell_towers_df.iloc[indices]["cell"].values
nearest_tower_lats = cell_towers_df.iloc[indices]["lat"].values
nearest_tower_lons = cell_towers_df.iloc[indices]["lon"].values
nearest_tower_ranges = cell_towers_df.iloc[indices]["range"].values / 1000.0  # Convert to km

# ----------------------------------------------------------------------------
# 6) DETERMINE IF SCHOOL IS WITHIN TOWER RANGE
# ----------------------------------------------------------------------------
# If distance <= tower range => Well Connected
is_covered = distances <= nearest_tower_ranges

# Add columns to schools_df
schools_df["Nearest Tower"] = nearest_tower_ids
schools_df["Nearest Tower Lat"] = nearest_tower_lats
schools_df["Nearest Tower Lon"] = nearest_tower_lons
schools_df["Distance to Nearest Tower (km)"] = [
    geodesic((lat, lon), (tower_lat, tower_lon)).km
    for lat, lon, tower_lat, tower_lon in zip(
        schools_df["Latitude"], schools_df["Longitude"],
        nearest_tower_lats, nearest_tower_lons
    )
]
is_covered = schools_df["Distance to Nearest Tower (km)"] <= (nearest_tower_ranges)

schools_df["Connectivity Status"] = np.where(is_covered, "Well Connected", "Poorly Connected")

# ----------------------------------------------------------------------------
# 7) SAVE RESULTS
# ----------------------------------------------------------------------------
schools_df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Updated school connectivity data saved to {OUTPUT_FILE}")

# ----------------------------------------------------------------------------
# 8) DEBUGGING HELPER PRINTS
# ----------------------------------------------------------------------------
print("\n=== SAMPLE OUTPUT ===")
print(schools_df[[
    'School Name', 'Latitude', 'Longitude',
    'Nearest Tower', 'Nearest Tower Lat', 'Nearest Tower Lon',
    'Distance to Nearest Tower (km)', 'Connectivity Status'
]].head(10))

