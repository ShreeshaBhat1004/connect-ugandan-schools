import pandas as pd

# Load the schools connectivity dataset
schools_file = r"C:\Users\User\My_programs\Conn\schools_with_connectivity_status.csv"
schools_df = pd.read_csv(schools_file)

# Extract only the poorly connected schools
poorly_connected_schools = schools_df[schools_df["Connectivity Status"] == "Poorly Connected"]

# Save this subset for verification
poorly_connected_schools.to_csv(r"C:\Users\User\My_programs\Conn\poorly_connected_schools.csv", index=False)

print(f"✅ Found {len(poorly_connected_schools)} poorly connected schools.")
