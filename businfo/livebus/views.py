import requests
from datetime import datetime
import pytz
from django.shortcuts import render

def get_next_bus():
    # Define the endpoint and parameters
    url = 'http://transport.opendata.ch/v1/connections'
    params = {
        'from': 'Zweiackerstrasse',  # Departure station
        'to': 'Zurich HB',  # Arrival station
        'transportations[]': 'bus',  # We are interested in bus transport
        'limit': 1  # We want only the next connection
    }
    
    # Send the request to the API
    response = requests.get(url, params=params)
    data = response.json()

    if "connections" in data and data["connections"]:
        # Extract the departure time, line, and destination of the first connection
        departure_time_str = data["connections"][0]["from"]["departure"]
        
        # Extract bus number and direction
        bus_number = data["connections"][0]["sections"][0]["journey"]["number"]
        direction = data["connections"][0]["sections"][0]["journey"]["to"]

        # Parse the departure time and calculate the difference in minutes
        departure_time = datetime.strptime(departure_time_str, "%Y-%m-%dT%H:%M:%S%z")  # Handle timezone offset
        
        # Make current time timezone-aware (assuming it's in Zurich's timezone)
        zurich_tz = pytz.timezone('Europe/Zurich')
        current_time = datetime.now(zurich_tz)  # Now is localized to Zurich timezone

        # Calculate the time difference in seconds
        time_diff = departure_time - current_time
        seconds_left = time_diff.total_seconds()
        
        # Calculate minutes and seconds
        minutes_left = int(seconds_left // 60)
        seconds_left = int(seconds_left % 60)

        # Convert departure time to a format that JavaScript can use (full date and time)
        departure_time_js = departure_time.strftime("%Y-%m-%dT%H:%M:%S")

        # Format the exact departure time for displaying in HH:MM format
        departure_time_formatted = departure_time.strftime("%H:%M")

        return {
            'bus_number': bus_number,
            'direction': direction,
            'minutes_left': minutes_left,
            'seconds_left': seconds_left,
            'departure_time': departure_time_js,  # Pass full date/time to JavaScript
            'formatted_departure_time': departure_time_formatted  # Pass formatted HH:MM for display
        }
    else:
        return None

def live_bus_info(request):
    # Fetch live bus info
    bus_data = get_next_bus()
    
    return render(request, 'livebus/bus_info.html', {'bus_data': bus_data})