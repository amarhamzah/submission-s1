import pickle
import streamlit as st

#load save model
model = pickle.load(open('dummyservis_model.sav','rb'))

#judul aplikasi
st.logo('lapservice.jpg')
st.header("Aplikasi Estimasi Harga Servis Laptop")
st.image('lapservice.jpg')
st.divider()

#membagi kolom
col1,col2,col3 = st.columns(3)
with col1:
    jenis_kerusakan = st.selectbox("Jenis Kerusakan",('RAM','HDD','SSD','Baterai','Motherboard'))

    if 'RAM' in jenis_kerusakan: # If user selects RAM  do 👇
        jenis_kerusakan = 1
    elif 'HDD' in jenis_kerusakan: # If user selects HDD  do 👇
        jenis_kerusakan = 2
    elif 'SSD' in jenis_kerusakan: # If user selects SSD  do 👇
        jenis_kerusakan = 3
    elif 'Baterai' in jenis_kerusakan: # If user selects Baterai  do 👇
        jenis_kerusakan = 4
    elif 'Motherboard' in jenis_kerusakan: # If user selects Motherboard  do 👇
        jenis_kerusakan = 5
        
#st.write(kerusakan)

with col2:
    lama_perbaikan = st.selectbox("Lama Perbaikan (Hari)",('1','2','3','4','5','6','7'))

    if '1' in lama_perbaikan:
        lama_perbaikan = 1
    elif '2' in lama_perbaikan:
        lama_perbaikan = 2
    elif '3' in lama_perbaikan:
        lama_perbaikan = 3
    elif '4' in lama_perbaikan:
        lama_perbaikan = 4
    elif '5' in lama_perbaikan:
        lama_perbaikan = 5
    elif '6' in lama_perbaikan:
        lama_perbaikan = 6
    elif '7' in lama_perbaikan:
        lama_perbaikan = 7
        
#st.write(lama_perbaikan)

with col3:
    biaya_sparepart = st.number_input("Biaya Sparepart")

prediksi_harga_jasa=''

#Membuat tombol prediksi harga servis laptop
if st.button('Prediksi Harga Jasa Servis'):
    with st.spinner ('Please Wait...'):
        prediksi_harga_jasa = model.predict([[jenis_kerusakan,lama_perbaikan,biaya_sparepart]])
st.divider()

st.write ('Estimasi Harga Jasa Servis Laptop (Rp.) :', prediksi_harga_jasa)