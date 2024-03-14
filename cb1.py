import streamlit as st
import requests

# Set the title and subheader
st.title('Pertamina Field Jambi')
st.subheader('Monitoring Pressure')

# User Inputs
READ_API_KEY = 'SPYMD6ONS3YT6HKN'
CHANNEL_ID = '2405457'

# Define the URLs for fetching data from ThingSpeak
field_ids = ['1', '2', '3', '4', '5', '6']
url_base = 'https://api.thingspeak.com/channels/{}/fields/{}.json?api_key={}'
urls = [url_base.format(CHANNEL_ID, field_id, READ_API_KEY) for field_id in field_ids]

# Function to fetch latest data for each field
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['feeds'][0]['field' + data['feeds'][0]['field'].split('field')[-1]], data['feeds'][0]['created_at']
    else:
        return None, None

# Display gauges for each field
for i, url in enumerate(urls, start=1):
    value, timestamp = fetch_data(url)
    if value is not None:
        st.subheader(f'Field {i}')
        st.text(f'Last updated: {timestamp}')
        st.text(f'Current value: {value}')
        # Customize min and max values as needed
        st.gauge(f'Pressure ({value})', min_value=0, max_value=100, current_value=float(value))
    else:
        st.warning(f"Failed to fetch data for Field {i}")

