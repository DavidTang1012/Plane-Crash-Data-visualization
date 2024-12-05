import pandas as pd
from geopy.geocoders import Nominatim
import folium

# Load the dataset
file_path = 'data.csv'  # Replace with your dataset file path
data = pd.read_csv(file_path)

# Initialize the geocoder
geolocator = Nominatim(user_agent="geo_locator")


# Function to geocode a location
def geocode_location(location):
    try:
        geo = geolocator.geocode(location, timeout=10)
        if geo:
            return geo.latitude, geo.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {location}: {e}")
        return None, None


# Limit the dataset to the first 200 rows
subset = data.head(200).copy()

# Ensure 'Route' column exists and handle missing values
if 'Route' not in subset.columns or subset['Route'].isnull().all():
    raise ValueError("The 'Route' column is missing or empty in the dataset.")

# Split 'Route' into Departure and Destination, handling errors gracefully
split_routes = subset['Route'].str.split(' - ', expand=True)
subset['Departure'] = split_routes[0]
subset['Destination'] = split_routes[1]

# Filter out rows with missing departure or destination
subset = subset.dropna(subset=['Departure', 'Destination'])

# Geocode departure and destination locations
print("Geocoding departure locations...")
subset['Departure_Latitude'], subset['Departure_Longitude'] = zip(*subset['Departure'].map(geocode_location))
print("Geocoding destination locations...")
subset['Destination_Latitude'], subset['Destination_Longitude'] = zip(*subset['Destination'].map(geocode_location))

# Filter rows with valid coordinates for both departure and destination
valid_routes = subset.dropna(
    subset=['Departure_Latitude', 'Departure_Longitude', 'Destination_Latitude', 'Destination_Longitude'])

# Initialize a folium map centered on the average coordinates
route_map = folium.Map(location=[valid_routes['Departure_Latitude'].mean(), valid_routes['Departure_Longitude'].mean()],
                       zoom_start=2)

# Add routes to the map
for _, row in valid_routes.iterrows():
    # Add markers for departure and destination
    folium.Marker(location=(row['Departure_Latitude'], row['Departure_Longitude']),
                  popup=f"Departure: {row['Departure']}", icon=folium.Icon(color='blue')).add_to(route_map)
    folium.Marker(location=(row['Destination_Latitude'], row['Destination_Longitude']),
                  popup=f"Destination: {row['Destination']}", icon=folium.Icon(color='green')).add_to(route_map)

    # Draw a line between departure and destination
    folium.PolyLine([(row['Departure_Latitude'], row['Departure_Longitude']),
                     (row['Destination_Latitude'], row['Destination_Longitude'])],
                    color="red", weight=2.5, opacity=0.7).add_to(route_map)

# Save the map to an HTML file
map_output_path = "airplane_routes_map_200.html"
route_map.save(map_output_path)
print(f"Interactive route map saved to '{map_output_path}'. Open this file in a browser to view the routes.")
