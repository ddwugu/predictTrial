import pickle
import streamlit as st
import requests
import pandas as pd
import time  # Import the time module

# Load the model
try:
    with open('Pred_lokasi11.sav', 'rb') as file:
        LokasiKM = pickle.load(file)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    LokasiKM = None  # Assign None if there is an error loading the model

# Web Title
st.title('Pertamina Field Jambi')
st.subheader('Prediksi Lokasi Kebocoran Line BJG-TPN')

# Masukkan API key dan Channel ID
READ_API_KEY = 'SPYMD6ONS3YT6HKN'
CHANNEL_ID = '2405457'
FIELD_ID_1 = '1'
FIELD_ID_2 = '3'

# URL untuk mengakses data dari ThingSpeak untuk field 1
url_field_1 = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD_ID_1}.csv?api_key={READ_API_KEY}'

# URL untuk mengakses data dari ThingSpeak untuk field 2
url_field_2 = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD_ID_2}.csv?api_key={READ_API_KEY}'

# Function to fetch data
def fetch_data():
    response_field_1 = requests.get(url_field_1)
    response_field_2 = requests.get(url_field_2)
    if response_field_1.status_code == 200 and response_field_2.status_code == 200:
        data_field_1 = pd.read_csv(url_field_1)
        data_field_2 = pd.read_csv(url_field_2)
        Titik_1_PSI = data_field_1['field1'].iloc[0] if not data_field_1.empty else None
        Titik_2_PSI = data_field_2['field3'].iloc[0] if not data_field_2.empty else None
        return Titik_1_PSI, Titik_2_PSI
    else:
        return None, None

# Function to predict location
def predict_location(Titik_1_PSI, Titik_2_PSI):
    if Titik_1_PSI is not None and Titik_2_PSI is not None:
        try:
            a = 135 - float(Titik_1_PSI)
            b = 86 - float(Titik_2_PSI)
            prediksi_lokasi = LokasiKM.predict([[a, b]])
            if prediksi_lokasi[0] == 0: # titik nol
                suspect_loct = 'It is safe that there is no fluid flowing'
            elif prediksi_lokasi[0] >= 26.3: # total panjang trunkline
                suspect_loct = 'Safe, there are no'
            else:
                suspect_loct = f'!!!estimated  location {prediksi_lokasi[0]} KM'
            return suspect_loct
        except Exception as e:
            return f"Error predicting location: {e}"
    else:
        return "Nilai 'Titik_1_PSI' atau 'Titik_2_PSI' tidak tersedia, menggunakan nilai sebelumnya jika ada."

# Placeholder for real-time updates
placeholder = st.empty()

# Initial values for Titik_1_PSI and Titik_2_PSI
prev_Titik_1_PSI = None
prev_Titik_2_PSI = None

# Continuously update the predictions
while True:
    # Fetch data
    Titik_1_PSI, Titik_2_PSI = fetch_data()

    # If both values are not None, update the placeholder
    if Titik_1_PSI is not None and Titik_2_PSI is not None:
        # Clear placeholder
        placeholder.empty()

        # Write new values to placeholder
        placeholder.write(f'Nilai Titik_1_PSI: {Titik_1_PSI}')
        placeholder.write(f'Nilai Titik_2_PSI: {Titik_2_PSI}')

        # Update previous values
        prev_Titik_1_PSI = Titik_1_PSI
        prev_Titik_2_PSI = Titik_2_PSI
    else:
        # If any value is None, use previous values
        if prev_Titik_1_PSI is not None and prev_Titik_2_PSI is not None:
            Titik_1_PSI = prev_Titik_1_PSI
            Titik_2_PSI = prev_Titik_2_PSI
        else:
            # If previous values are also None, show warning
            st.warning("Nilai 'Titik_1_PSI' atau 'Titik_2_PSI' tidak tersedia, menggunakan nilai sebelumnya jika ada.")

    # Predict location
    location_prediction = predict_location(Titik_1_PSI, Titik_2_PSI)
    placeholder.write(location_prediction)

    # Delay for 6 seconds
    time.sleep(6)
