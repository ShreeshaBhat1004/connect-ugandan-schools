from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

poorly_connected_schools = pd.read_csv(r"C:\Users\User\My_programs\Conn\poorly_connected_schools.csv")
# Convert school locations to a NumPy array
school_locations = poorly_connected_schools[["Latitude", "Longitude"]].to_numpy()

# Define the number of new towers needed
num_clusters = max(1, len(school_locations) // 5)  # One new tower per 5 disconnected schools

# Run K-Means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
kmeans.fit(school_locations)

# Get the optimal new tower locations
new_tower_locations = kmeans.cluster_centers_

# Convert to a DataFrame
new_towers_df = pd.DataFrame(new_tower_locations, columns=["Latitude", "Longitude"])
new_towers_df.to_csv(r"C:\Users\User\My_programs\Conn\new_suggested_towers.csv", index=False)

print(f"✅ Suggested {num_clusters} new tower locations.")
