import pandas as pd
import json
import folium
from datetime import datetime

#File Path and read
csv_file_path = 'src/Mapping/map_data.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Filepath
json_file_path = 'src/Mapping/map_data.json'  # Desired JSON file name

# DF -> JSON
markers = df.apply(lambda row: {
    "location": [row['latitude'], row['longitude']],
    "tooltip": row['tooltip'],
    "popup": row['popup'],
    "icon_color": 'red' if datetime.strptime(row['date'], '%Y-%m-%d') < datetime(2024, 1, 1) else 'green'  # Assuming the 'date' column exists
}, axis=1).tolist()

# Write to JSON
with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(markers, jsonfile, indent=4)
print("CSV data has been written to JSON file.")

# Reading the JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    markers_data = json.load(file)
print(json.dumps(markers_data, indent=4))

# Init Folium Map
map = folium.Map(location=[43.70876, -79.6954], zoom_start=10)

#Name the feature groups
red_group = folium.FeatureGroup(name='Before 2024')
green_group = folium.FeatureGroup(name='2024 and Later')

#Markers, Tooltips, Icon Colors
for marker_data in markers_data:
    marker = folium.Marker(
        location=marker_data['location'],
        tooltip=marker_data['tooltip'],
        popup=marker_data['popup'],
        icon=folium.Icon(color=marker_data['icon_color'])
    )
    if marker_data['icon_color'] == 'red':
        marker.add_to(red_group)
    elif marker_data['icon_color'] == 'green':
        marker.add_to(green_group)

# Draw/Render to Map
red_group.add_to(map)
green_group.add_to(map)
#Layer control
folium.LayerControl().add_to(map)
# Save -> HTML
map.save("src/Mapping/map.html")

print("Map with markers has been created.")
print(markers_data[:1])
