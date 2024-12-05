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

# Limit to the first 200 rows for demonstration
subset = data.head(200).copy()
subset['Latitude'], subset['Longitude'] = zip(*subset['Location'].map(geocode_location))

# Save the geocoded subset to avoid repeating API calls
subset.to_csv('geocoded_crashes_200.csv', index=False)
print("Geocoded subset saved to 'geocoded_crashes_200.csv'.")

# Filter rows with valid coordinates
geocoded_data = subset.dropna(subset=['Latitude', 'Longitude'])

# Initialize a folium map centered on the average coordinates of the geocoded data
crash_map = folium.Map(location=[geocoded_data['Latitude'].mean(), geocoded_data['Longitude'].mean()], zoom_start=2)

# Add crash points to the map
for _, row in geocoded_data.iterrows():
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=5,
        popup=f"Location: {row['Location']}<br>Fatalities: {row['Fatalities']}",
        color="red",
        fill=True,
        fill_opacity=0.7
    ).add_to(crash_map)

# Save the map to an HTML file
map_output_path = "airplane_crashes_map_200.html"
crash_map.save(map_output_path)
print(f"Interactive map saved to '{map_output_path}'. Open this file in a browser to view the map.")
