import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Gambar toko
st.image("assets/toko.webp", use_container_width=150)

# Judul aplikasi
st.title("Prediksi Tarif Perbaikan Laptop dan Komputer --Yidz Computer--")

# Daftar deskripsi kode
kode_dict = {
    0: 'Cleaning Unit / Repasta',
    1: 'Install ulang OS / App',
    2: 'Instalasi Ram',
    3: 'Instalasi Storage SSD/ HDD',
    4: 'Instalasi PC',
    5: 'Service Keyboard',
    6: 'Service LCD',
    7: 'Unit Mati Total',
    8: 'Service Kerusakan Mayor',
    9: 'Service Kerusakan Minor'
}

# Input data dari pengguna
kode_label = st.selectbox("Jenis Servis", options=list(kode_dict.values()))

kode = list(kode_dict.keys())[list(kode_dict.values()).index(kode_label)]


# Input lainnya
#tingkat_kerusakan = st.selectbox("Tingkat Kerusakan", [1, 2, 3, 4, 5])
tingkat_kerusakan = st.selectbox("Tingkat Kerusakan",("Ringan","Sedang","Sukar","Sulit","Berat"))
if "Ringan" in tingkat_kerusakan :
    tingkat_kerusakan = 1
elif "Sedang" in tingkat_kerusakan :
    tingkat_kerusakan = 2
elif "Sukar" in tingkat_kerusakan :
    tingkat_kerusakan = 3
elif "Sulit" in tingkat_kerusakan :
    tingkat_kerusakan = 4
elif "Berat" in tingkat_kerusakan :
    tingkat_kerusakan = 5

#st.write(tingkat_kerusakan)

harga_sparepart = st.number_input("Harga Sparepart (Rp)", min_value=0)

lama_perbaikan = st.number_input("Lama Perbaikan (hari)", min_value=0)
#garansi = st.selectbox("Garansi (0: Tidak, 1: Ya)", [0, 1])
garansi = st.selectbox("Garansi :", ("Ya", "Tidak"))
if "Ya" in garansi :
    garansi = 1
elif "Tidak" in garansi :
    garansi = 0

#st.write(garansi)
    

# Dataset untuk pelatihan model
dataservis = pd.read_csv("laporan_perbaikan.csv")
dataservis.dropna(inplace=True)

# Fitur dan target
X = dataservis[['kode', 'tingkat_kerusakan', 'harga_sparepart', 'lama_perbaikan', 'garansi']]
y = dataservis['tarif_perbaikan']

# Pelatihan model tanpa scaler
model = LinearRegression()
model.fit(X, y)

# Prediksi jika tombol ditekan
if st.button("Prediksi Tarif Perbaikan"):
    input_data = np.array([[kode, tingkat_kerusakan, harga_sparepart, lama_perbaikan, garansi]])
    prediction = model.predict(input_data)[0]
    st.success(f"Perkiraan Tarif Perbaikan: Rp {prediction:,.0f}")

st.write("---") # Membuat garis pemisah

# --- Widget Tombol WhatsApp ---
st.header("Butuh Bantuan?")

# Ganti dengan nomor WA admin Anda (format internasional, tanpa '+' atau spasi)
nomor_admin_wa = "6283895316302"  
url_wa = f"https://wa.me/{nomor_admin_wa}"

st.link_button("💬 Hubungi Admin via WhatsApp", url=url_wa)