import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler # Added based on notebook context, though not used in the final X_train
import pickle # Though not used in the notebook for saving, it's good practice for models

# --- Page Configuration ---
st.set_page_config(
    page_title="Prediksi Tarif Servis Laptop",
    layout=wide
)

# --- Model Training Function (with caching) ---
@st.cache_data
def train_model():
    # Membaca dataset
    try:
        dataservis = pd.read_csv('laporan_perbaikan.csv') #
    except FileNotFoundError:
        st.error(File 'laporan_perbaikan.csv' tidak ditemukan. Pastikan file berada di direktori yang sama dengan aplikasi.)
        return None, None

    # Handle missing values by dropping rows with NaNs
    dataservis.dropna(inplace=True) #

    if dataservis.empty
        st.error(Dataset kosong setelah menghapus baris dengan nilai yang hilang.)
        return None, None

    # Definisikan variabel independen dan dependen
    X = dataservis[['kode', 'tingkat_kerusakan', 'harga_sparepart', 'lama_perbaikan', 'garansi']] #
    Y = dataservis['tarif_perbaikan'] #

    # Split data (though not strictly necessary if we retrain on full data for deployment)
    # For consistency with the notebook, we'll keep the split and train on X_train, Y_train
    # However, for a production model, training on all available data (X, Y) is common.
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42) #

    # Buat dan latih model regresi linear
    regression_model = LinearRegression() #
    regression_model.fit(X_train, Y_train) #

    # Store feature names for consistent input order
    feature_names = X_train.columns.tolist()

    return regression_model, feature_names

# --- Load Model ---
model, feature_names = train_model()

# --- Main Application ---
st.title(Prediksi Tarif Servis Laptop)
st.markdown(Aplikasi ini memprediksi tarif servis laptop berdasarkan beberapa faktor menggunakan model Regresi Linear.)
st.markdown(---)

if model and feature_names
    st.sidebar.header(Input Fitur untuk Prediksi)

    # --- User Inputs ---
    # Using feature_names to ensure correct order and naming
    inputs = {}
    # The notebook uses specific values for prediction example. We'll make them inputs.
    # kode = 6
    # tingkat_kerusakan = 5
    # harga_sparepart = 450000
    # lama_perbaikan = 1
    # garansi = 1

    # Example unique values from the notebook's dataframe summary for better sliderselect options if needed
    # kode 0.0 to 9.0
    # tingkat_kerusakan 1.0 to 5.0
    # lama_perbaikan 1.0 to 3.0
    # garansi 0.0 to 1.0

    inputs['kode'] = st.sidebar.slider(
        Kode Jenis Servis,
        min_value=0, # Based on dataservis['kode'].min()
        max_value=9, # Based on dataservis['kode'].max()
        value=6,
        step=1,
        help=Pilih kode jenis servis (0-9)
    )
    inputs['tingkat_kerusakan'] = st.sidebar.slider(
        Tingkat Kerusakan,
        min_value=1, # Based on dataservis['tingkat_kerusakan'].min()
        max_value=5, # Based on dataservis['tingkat_kerusakan'].max()
        value=5,
        step=1,
        help=Pilih tingkat kerusakan (1-5, semakin tinggi semakin parah)
    )
    inputs['harga_sparepart'] = st.sidebar.number_input(
        Harga Sparepart (Rp),
        min_value=0,
        value=450000,
        step=10000,
        help=Masukkan estimasi harga sparepart jika ada
    )
    inputs['lama_perbaikan'] = st.sidebar.slider(
        Lama Perbaikan (Hari),
        min_value=1, # Based on dataservis['lama_perbaikan'].min()
        max_value=3, # Based on dataservis['lama_perbaikan'].max()
        value=1,
        step=1,
        help=Estimasi lama perbaikan dalam hari
    )
    inputs['garansi'] = st.sidebar.selectbox(
        'Garansi',
        options=['Ya', 'Tidak'],
        index=0,  # Default ke 'Ya'
        help='Apakah servis ini bergaransi?'
)

    # --- Prediction ---
    if st.sidebar.button(Hitung Prediksi Tarif, type=primary)
        # Prepare input for prediction, ensuring correct order
        input_df = pd.DataFrame([inputs], columns=feature_names)

        try
            prediksi_tarif = model.predict(input_df) #
            st.subheader(Hasil Prediksi)
            st.metric(label="Estimasi Tarif Perbaikan", value=f"Rp {prediksi_tarif[0],.2f}")

            st.markdown(---)
            st.subheader(Detail Model (Informasi dari Notebook))

            # Displaying coefficients and intercept from the notebook
            # These are fixed based on the last training in the notebook
            # For a dynamic display, these would be properties of the 'model' object.
            # For example model.coef_[0], model.coef_[1], etc. and model.intercept_

            # Coefficients as per the notebook's output
            # Koefisien Regresi
            # Kode -1968.198351447694
            # Tingkat Kerusakan 75059.55585971421
            # Harga Sparepart -0.02150429258472286
            # Lama Perbaikan 24267.572798443987
            # Garansi 3538.503858229751
            # Intercept -67030.92146278647

            coef_data = {
                'Fitur' feature_names + ['Intercept'],
                'Koefisien' list(model.coef_) + [model.intercept_]
            }
            coef_df = pd.DataFrame(coef_data)
            st.write(Koefisien Regresi)
            st.dataframe(coef_df.set_index('Fitur'))

            # Displaying MSE and R2 Score from the notebook
            # MSE (Mean Square Error) 944448621.686632
            # R2 Score 0.7493209178082458
            # For a live calculation, you would need X_test and Y_test from the split
            # and then recalculate
            # from sklearn.metrics import mean_squared_error, r2_score
            # Y_pred_test = model.predict(X_test)
            # mse_val = mean_squared_error(Y_test, Y_pred_test)
            # r2_val = r2_score(Y_test, Y_pred_test)
            # For now, showing the values from the notebook as static info.
            st.write(Evaluasi Model (berdasarkan data test dari notebook))
            col1, col2 = st.columns(2)
            col1.metric(MSE (Mean Squared Error), 944,448,621.69)
            col2.metric(R² Score, 0.749)
            st.caption(Catatan MSE dan R² Score di atas adalah hasil dari training di notebook dan mungkin berbeda jika model dilatih ulang pada data yang berbeda atau dengan split yang berbeda.)

        except Exception as e
            st.error(fTerjadi kesalahan saat melakukan prediksi {e})
    else
        st.info(Masukkan fitur di sidebar kiri dan klik 'Hitung Prediksi Tarif'.)

    st.markdown(---)
    st.sidebar.markdown(---)
    if st.sidebar.checkbox(Tampilkan Data Sampel (dari laporan_perbaikan.csv))
        try
            sample_data = pd.read_csv('laporan_perbaikan.csv').head() #
            st.subheader(Sampel Data Awal)
            st.dataframe(sample_data)
        except FileNotFoundError
            st.warning(File 'laporan_perbaikan.csv' tidak ditemukan untuk menampilkan sampel.)
        except Exception as e
            st.error(fTidak dapat memuat sampel data {e})

else
    st.warning(Model tidak berhasil dilatih. Harap periksa file dataset dan konfigurasi.)

st.markdown(
    
    style
        .stButtonbutton {
            width 100%;
        }
    style
    ,
    unsafe_allow_html=True
)