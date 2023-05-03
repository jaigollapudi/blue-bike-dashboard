# Boston Blue Bike Travel Dashboard (2020)

This is a dashboard application built with Dash and Folium libraries, displaying the blue bike travel data in Boston in 2020. The app provides an interactive map that shows the start and end stations of bike trips, along with the number of rides taken at each end station. The app allows the user to filter the data by start station and time period. Additionally, there is a visualization feature implemented that allows the user to explore six different visualizations relevant to the dataset to further their understanding on Blue Bike data.


## Getting Started

To run the application, you need to install the following libraries:

- **pandas:** For data processing and analysis
- **dash:** For building the web-based dashboard
- **folium:** For creating the map and visualizing geographic data
- **folium.plugins.MarkerCluster:** For clustering multiple markers on the map
- **dash.dependencies:** For handling user input and updating the dashboard output
- **dash_bootstrap_components:** For using Bootstrap components to style the dashboard
- **plotly.express:** For user selected visualizations
- **plotly.graph_objects:** For user selected visualizations

You can install these libraries by running the following command in your terminal:

```
pip install pandas dash folium dash_bootstrap_components plotly
```

## Files

- **bluebikes_tripdata_2020.csv:** The dataset used in the dashboard
- **main.py:** The Python code for the dashboard
- **README.md:** This README file


## How to Use the App

Run the main.py file by running the following command in your terminal:
```
python main.py
```
1. Visualizations: Users can select from a dropdown menu to view different visualizations of the Blue Bike trip data from 2020. The available visualizations are:
- Monthly Trend Analysis
- Trip Duration Analysis
- Customer vs. Subscriber Analysis
- Heatmap of Trips per Hour and Day of the Week
- Top Start and End Stations
- Postal Code Analysis
2. Map: Users can select a Blue Bike station and a time period to view a map of the station and the end stations of all the trips that started at that station during the selected time period. 
- The map will display the selected data, showing the start station as a blue marker and the end stations as red markers. The lines connecting the start and end stations represent bike trips taken between those stations.
- You can click on the markers to see the name of the station and the number of rides taken at that station.
- You can also zoom in and out of the map to explore the data further.
