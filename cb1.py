import pickle
import streamlit as st

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
# User Inputs

import requests
import pandas as pd

# Masukkan API key dan Channel ID
READ_API_KEY = 'SPYMD6ONS3YT6HKN'
CHANNEL_ID = '2405457'
FIELD_ID_1 = '1'
FIELD_ID_2 = '3'

# URL untuk mengakses data dari ThingSpeak untuk field 1
url_field_1 = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD_ID_1}.csv?api_key={READ_API_KEY}'

# URL untuk mengakses data dari ThingSpeak untuk field 2
url_field_2 = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD_ID_2}.csv?api_key={READ_API_KEY}'

# Mendownload data CSV untuk field 1
response_field_1 = requests.get(url_field_1)

# Mendownload data CSV untuk field 2
response_field_2 = requests.get(url_field_2)

# Menyimpan data CSV ke dalam DataFrame
if response_field_1.status_code == 200 and response_field_2.status_code == 200:
    data_field_1 = pd.read_csv(url_field_1)
    data_field_2 = pd.read_csv(url_field_2)
    print("Data berhasil diunduh")
else:
    print("Gagal mengunduh data. Periksa kembali API key dan Channel ID Anda.")

# Ambil nilai pertama dari kolom 'field1' dan 'field3'
Titik_1_PSI = data_field_1['field1'].iloc[0] if not data_field_1.empty else None
Titik_2_PSI = data_field_2['field3'].iloc[0] if not data_field_2.empty else None

# Menampilkan nilai "Titik_1_PSI" dan "Titik_2_PSI"
if Titik_1_PSI is not None and Titik_2_PSI is not None:
    st.write(f'Nilai Titik_1_PSI: {Titik_1_PSI}')
    st.write(f'Nilai Titik_2_PSI: {Titik_2_PSI}')

# Code prediction
suspect_loct = ''

# JavaScript to automatically click the "Prediksi Lokasi" button
auto_click_script = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    const button = document.querySelector("button[data-testid='stStreamlitButton']");
    button.click();
});
</script>
"""

# Prediction Button (hidden)
if LokasiKM is not None and Titik_1_PSI is not None and Titik_2_PSI is not None:
    try:
        a = 135 - float(Titik_1_PSI)
        b = 86 - float(Titik_2_PSI)
        if st.button('Prediksi Lokasi', key='predict_button'):
            if a is not None and b is not None:
                prediksi_lokasi = LokasiKM.predict([[a, b]])
                if prediksi_lokasi[0] == 0: # titik nol
                    suspect_loct = 'It is safe that there is no fluid flowing'
                elif prediksi_lokasi[0] >= 26.3: # total panjang trunkline
                    suspect_loct = 'Safe, there are no leaks'
                else:
                    suspect_loct = f'!!!estimated leak location {prediksi_lokasi[0]} KM'
                st.success(suspect_loct)
            else:
                st.warning("Masukkan tekanan yang valid untuk kedua titik.")
    except Exception as e:
        st.error(f"Error predicting location: {e}")

# Execute the JavaScript to automatically click the button
st.script(auto_click_script)
