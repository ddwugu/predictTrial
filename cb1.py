def predict_location(Titik_1_PSI, Titik_2_PSI):
    if Titik_1_PSI is not None and Titik_2_PSI is not None:
        try:
            a = 135 - float(Titik_1_PSI)
            b = 86 - float(Titik_2_PSI)
            prediksi_lokasi = LokasiKM.predict([[a, b]])
            if prediksi_lokasi[0] == 0: # titik nol
                Nilai Titik_1_PSI: {Titik_1_PSI}
                Nilai Titik_1_PSI: {Titik_2_PSI}
                suspect_loct = 'It is safe that there is no fluid flowing'
                
            elif prediksi_lokasi[0] >= 26.3: # total panjang trunkline
                Nilai Titik_1_PSI: {Titik_1_PSI}
                Nilai Titik_1_PSI: {Titik_2_PSI}
                suspect_loct = 'Safe, there are no'
            else:
                Nilai Titik_1_PSI: {Titik_1_PSI}
                Nilai Titik_1_PSI: {Titik_2_PSI}
                suspect_loct = f'!!!estimated  location {prediksi_lokasi[0]} KM'
            return suspect_loct
        except Exception as e:
            return f"Error predicting location: {e}"
    else:
        return "Nilai 'Titik_1_PSI' atau 'Titik_2_PSI' tidak tersedia, menggunakan nilai sebelumnya jika ada."
