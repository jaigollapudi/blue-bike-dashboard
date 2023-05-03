"""
Jai Gollapudi
main.py: individual file used to run the app
Github repo: https://github.com/jaigollapudi/blue-bike-dashboard
"""

# Importing libraries
import pandas as pd
import dash
from dash import dcc, html
import folium
from folium.plugins import MarkerCluster
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


# Reading the CSV file
df_data = pd.read_csv('/Users/jaigollapudi/Downloads/blue-bike-dashboard/bluebikes_tripdata_2020.csv', low_memory=False)
# Converting the start and stop times to datetime format
df_data['starttime'] = pd.to_datetime(df_data['starttime'])
df_data['stoptime'] = pd.to_datetime(df_data['stoptime'])


# Initializing the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,
                                                'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])


def create_map(df_data_filtered):
    """
    Takes in a dataset, filtered by the start station and time period,
    extracts end station data, initializes a map, and adds markers and ride lines
    to start and end stations.

    :param df_data_filtered: The dataset filtered by start station and time period
    :return: The map with the filtered data
    """
    start_station = df_data_filtered[
        ['start station latitude', 'start station longitude', 'start station name']].drop_duplicates().iloc[0]
    end_stations = df_data_filtered[
        ['end station latitude', 'end station longitude', 'end station name']].drop_duplicates()

    m = folium.Map(location=[start_station['start station latitude'], start_station['start station longitude']],
                   zoom_start=11, tiles='Stamen Toner')

    # Add start station marker
    folium.Marker([start_station['start station latitude'], start_station['start station longitude']],
                  popup=start_station['start station name'], icon=folium.Icon(color='blue')).add_to(m)

    # Add end station markers
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in end_stations.iterrows():
        end_location_name = row['end station name']
        end_location_count = len(df_data_filtered[df_data_filtered['end station name'] == end_location_name])
        popup_text = f"<b>Station Name:</b> {end_location_name}<br><b>Number of rides:</b> {end_location_count}"
        folium.Marker([row['end station latitude'], row['end station longitude']], popup=popup_text,
                      icon=folium.Icon(color='red')).add_to(marker_cluster)

    # Add ride lines
    for _, ride in df_data_filtered.iterrows():
        start_lat, start_lon = ride['start station latitude'], ride['start station longitude']
        end_lat, end_lon = ride['end station latitude'], ride['end station longitude']
        ride_line = folium.PolyLine(
            locations=[[start_lat, start_lon], [end_lat, end_lon]],
            color='blue',
            weight=3
        )
        ride_line.add_to(m)

    return m


# Setting the app layout
app.layout = html.Div([
    html.Br(),
    # Title
    html.H1('Boston Blue Bike Travel Dashboard (2020)', className="text-center", style={'color': 'white'}),
    html.Hr(style={'borderTop': '2px solid white', 'width': '50%', 'margin': '0 auto',
                   'backgroundColor': 'white', 'border': 'none', 'height': '2px'}),
    html.Br(),
    dbc.Row([
        dbc.Col([
            # Visualization dropdown
            html.Div([
                html.Label('Select a visualization:', style={'color': 'white', 'paddingLeft': '10px'}),
                dcc.Dropdown(id='visualization-dropdown',
                             options=[
                                 {'label': 'Monthly Trend Analysis', 'value': 'monthly-trend'},
                                 {'label': 'Trip Duration Analysis', 'value': 'trip-duration'},
                                 {'label': 'Customer vs. Subscriber Analysis', 'value': 'customer-subscriber'},
                                 {'label': 'Heatmap of Trips per Hour and Day of the Week',
                                  'value': 'hourly-weekly-heatmap'},
                                 {'label': 'Top Start and End Stations', 'value': 'top-stations'},
                                 {'label': 'Postal Code Analysis', 'value': 'postal-code'}
                             ],
                             value='monthly-trend',
                             style={'width': '100%', 'color': 'black'}
                             ),
                html.Br(),
                # Visualization graph
                dcc.Graph(id='visualization-graph'),
                html.Br(),
                # Visualization message
                html.Div(id='visualization-message'),
            ], style={'width': '100%', 'height': '100px', 'margin': '0 auto'}),
        ], width=6),
        dbc.Col([
            # Start station dropdown
            html.Label('Select a blue bike station:', style={'color': 'white'}),
            dcc.Dropdown(id='start-station-dropdown',
                         options=[{'label': i, 'value': i} for i in sorted(df_data['start station name'].unique())],
                         value=sorted(df_data['start station name'].unique())[0],
                         style={'width': '100%', 'color': 'black'}
                         ),
            html.Br(),
            # Time period date range picker
            html.Label('Select a time period:', style={'color': 'white'}),
            dcc.DatePickerRange(
                id='starttime-picker',
                start_date=df_data['starttime'].min().date(),
                end_date=df_data['starttime'].max().date(),
                style={'width': '100%', 'color': 'black'}
            ),
            html.Br(),
            html.Br(),
            # Folium map
            html.Iframe(id='map', style={'width': '100%', 'height': '500px', 'margin': '0 auto'}),
            html.Div(
                [
                    html.Div(
                        [
                            # Legend for map (markers and path line)
                            html.B('MapBox Legend:'),
                            html.Br(),
                            html.I(className="fas fa-map-marker-alt", style={'color': 'blue'}),
                            " Start Station",
                            html.Br(),
                            html.I(className="fas fa-map-marker-alt", style={'color': 'red'}),
                            " End Stations",
                            html.Br(),
                            html.Div(style={'display': 'inline-block', 'width': '10px', 'height': '3px',
                                            'background-color': 'blue'}),
                            " Path",
                        ],
                        style={
                            'border': '2px solid grey',
                            'padding': '10px',
                            'background-color': 'white',
                            'opacity': 1
                        }
                    ),
                ],
                style={
                    'position': 'absolute',
                    'bottom': '10px',
                    'left': '10px'
                }
            ),
        ], style={'text-align': 'left', 'position': 'relative'}, width=6)
    ], style={'text-align': 'left'}),
], style={'backgroundColor': 'black', 'paddingLeft': '20px'})


# Callback to update the visualization message
@app.callback(
    Output('visualization-message', 'children'),
    [Input('visualization-dropdown', 'value')]
)
def update_visualization_message(selected_visualization):
    """
    Takes in the user selected visualization and gives a message
    on what the visualization is and observations from the visualization

    :param selected_visualization: The visualization the user selected
    :return: The associated visualization message
    """
    if selected_visualization == 'monthly-trend':
        message = "The Monthly Trend Analysis visualization shows the number of trips per month in 2020. " \
                  "The monthly trend data reveals a seasonal pattern in bike-sharing usage, with higher numbers of " \
                  "trips occurring during the warmer months and lower numbers during the colder months. A " \
                  "significant dip in April 2020 is likely due to the impact of COVID-19 lockdowns. The peak usage " \
                  "occurs in August and September 2020, which can be attributed to favorable weather conditions. " \
                  "Overall, bike-sharing usage is heavily influenced by seasonal weather patterns"
    elif selected_visualization == 'trip-duration':
        message = "The Trip Duration Analysis visualization shows the distribution of trip durations in seconds " \
                  "(0-2000). The trip duration data shows that the distribution of bike trips is right skewed, with " \
                  "most trips being of shorter durations. The highest number of trips fall within the 300-349 " \
                  "seconds range, followed by a gradual decline in frequency. The majority of users seem to prefer " \
                  "shorter trips, possibly for commuting or leisure purposes, indicating that bike-sharing is " \
                  "primarily utilized for shorter, more convenient journeys."
    elif selected_visualization == 'customer-subscriber':
        message = "The Customer vs Subscriber Analysis visualization shows the proportion of trips made by customers " \
                  "and subscribers. The data from the customer vs. subscriber analysis indicates that a significant " \
                  "majority (72%) of bike-sharing users are subscribers, while the remaining 28% are customers. " \
                  "This suggests that bike-sharing services are popular among regular users who find value in " \
                  "subscribing to the service, possibly for daily commutes or frequent short trips."
    elif selected_visualization == 'hourly-weekly-heatmap':
        message = "The Heatmap of Trips per Hour and Day of the Week shows the number of trips per hour and day of " \
                  "the week. Weekdays experience the highest number of trips during morning (7-9 AM) and evening " \
                  "(5-7 PM) commute hours, suggesting that the service is primarily used for work commutes. On " \
                  "weekends, there is slightly higher usage during the daytime and evenings, likely due to " \
                  "recreational and social activities. Early mornings (0-4) across all days witness the lowest " \
                  "number of trips, with a sharp decline in trips after 10 PM."
    elif selected_visualization == 'top-stations':
        message = "The Top Start and End Stations visualization shows the top 10 start and end stations by number of " \
                  "trips. The data highlights the top 10 start and end stations, with Central Square at " \
                  "Mass Ave / Essex St and Charles Circle - Charles St at Cambridge St being the most popular. Other " \
                  "significant stations, such as MIT at Mass Ave/Amherst St and Christian Science Plaza, are " \
                  "also popular. Some stations, like Cross St at Hanover St, are more popular start stations, and " \
                  "others, like Nashua Street at Red Auerbach Way, are popular end stations."
    elif selected_visualization == 'postal-code':
        message = "The Postal Code Analysis visualization shows the top 10 postal codes by the number of trips. " \
                  "The postal code analysis shows that the highest number of trips are concentrated in the 02139 " \
                  "postal code (Cambridge, MA), with more than double the trips compared to the second highest, " \
                  "02215. Given that the highest concentration is in 02139, it suggests that the Cambridge area is " \
                  "a crucial region for the service. This could be due to the presence of key locations, such as " \
                  "educational institutions, businesses, or popular destinations."
    else:
        message = ""

    return html.P(message, style={'color': 'white'})


# Callback to update the visualization graph
@app.callback(
    Output('visualization-graph', 'figure'),
    [Input('visualization-dropdown', 'value')]
)
def update_visualization(selected_visualization):
    """
    Takes in the user selected visualization and generates
    the selected visualization graph

    :param selected_visualization: The visualization the user selected
    :return: The associated visualization graph
    """
    # Monthly ride trend line graph
    if selected_visualization == 'monthly-trend':
        monthly_data = df_data.groupby(
            df_data['starttime'].dt.to_period('M').astype('datetime64[ns]')).size().reset_index(name='trips')
        fig = px.line(monthly_data, x='starttime', y='trips', title='Monthly Trend Analysis')
        fig.update_layout(xaxis_title='Month',
                          yaxis_title='Number of Trips')

    # Trip Duration Histogram
    elif selected_visualization == 'trip-duration':
        # Filter data for trip durations between 0 and 2,000 seconds
        filtered_data = df_data[df_data['tripduration'].between(0, 2000)]
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=filtered_data['tripduration'], nbinsx=50,
                                   marker=dict(color='blue', line=dict(color='black', width=1))))
        fig.update_layout(title='Trip Duration Analysis',
                          xaxis_title='Trip Duration (seconds)',
                          yaxis_title='Number of Trips')

    # Customer vs Subscriber Pie chart
    elif selected_visualization == 'customer-subscriber':
        user_type_data = df_data['usertype'].value_counts().reset_index(name='count')
        fig = px.pie(user_type_data, names='index', values='count', title='Customer vs. Subscriber Analysis')

        # Heatmap of trips per hour and day of the week
    elif selected_visualization == 'hourly-weekly-heatmap':
        df_data['hour'] = df_data['starttime'].dt.hour
        df_data['day_of_week'] = df_data['starttime'].dt.dayofweek
        hourly_weekly_data = df_data.groupby(['hour', 'day_of_week']).size().reset_index(name='trips')

        fig = px.density_heatmap(hourly_weekly_data, x='day_of_week', y='hour', z='trips',
                                 title='Heatmap of Trips per Hour and Day of the Week')
        fig.update_xaxes(title='Day of the Week', ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                         tickvals=list(range(0, 7)))
        fig.update_yaxes(title='Hour of the Day')

    # Top start and end stations bar diagram
    elif selected_visualization == 'top-stations':
        top_start_stations = df_data['start station name'].value_counts().head(10).reset_index(name='count')
        top_end_stations = df_data['end station name'].value_counts().head(10).reset_index(name='count')

        fig = go.Figure()
        fig.add_trace(go.Bar(x=top_start_stations['index'], y=top_start_stations['count'], name='Start Stations',
                             marker=dict(color='blue')))
        fig.add_trace(go.Bar(x=top_end_stations['index'], y=top_end_stations['count'], name='End Stations',
                             marker=dict(color='green')))
        fig.update_layout(title='Top Start and End Stations', xaxis_title='Station Name', yaxis_title='Number of Trips',
                          barmode='group')

    # Postal code bar diagram
    elif selected_visualization == 'postal-code':
        postal_data = df_data['postal code'].value_counts().head(10).reset_index(name='count')
        fig = px.bar(postal_data, x='index', y='count', title='Postal Code Analysis')
        fig.update_xaxes(title='Postal Code')
        fig.update_yaxes(title='Number of Trips')

    return fig


# Callback to update the time period selector
@app.callback(
    [Output('starttime-picker', 'min_date_allowed'),
     Output('starttime-picker', 'max_date_allowed')],
    [Input('start-station-dropdown', 'value')]
)
def update_date_picker(selected_start_station):
    """
    Takes un a start station and returns the max and min date
    within which data is present

    :param selected_start_station: The start station the user selected
    :return: The min and max date in the dataframe within which data is present
    """
    filtered_data = df_data[df_data['start station name'] == selected_start_station]
    min_date = filtered_data['starttime'].min().date()
    max_date = filtered_data['starttime'].max().date()
    return min_date, max_date

# Callback to update the map
@app.callback(
    Output('map', 'srcDoc'),
    Input('start-station-dropdown', 'value'),
    Input('starttime-picker', 'start_date'),
    Input('starttime-picker', 'end_date')
)
def update_map(selected_start_station, start_date, end_date):
    """

    :param selected_start_station:  The start station the user selected
    :param start_date: The start date selected
    :param end_date: The end date selected
    :return:
    """
    if start_date is None:
        start_date = df_data['starttime'].min().date()
    else:
        start_date = pd.to_datetime(start_date).date()

    if end_date is None:
        end_date = df_data['starttime'].max().date()
    else:
        end_date = pd.to_datetime(end_date).date()

    # Filtering the required data
    df_data_filtered = df_data.loc[
        (df_data['starttime'].dt.date >= start_date) &
        (df_data['starttime'].dt.date <= end_date) &
        (df_data['start station name'] == selected_start_station)]

    # Creating map
    m = create_map(df_data_filtered)

    # Saving map to HTML string and returning it
    html_string = m.get_root().render()
    return html_string


if __name__ == '__main__':
    app.run_server(debug=True)




