import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi Halaman (Agar layout melebar dan lebih modern)
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
sns.set_theme(style="whitegrid")

# 1. Optimasi Load Data dengan Cache
@st.cache_data
def load_data():
    # Menggunakan path relatif agar aman saat di-deploy
    file_path = "dashboard/main_data.csv"
    if not os.path.exists(file_path):
        file_path = "main_data.csv" # Backup jika file di root
        
    df = pd.read_csv(file_path)
    
    # Mapping label (Pastikan nama kolom di CSV adalah 'season' dan 'weathersit')
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {1: "Clear", 2: "Mist", 3: "Light Snow/Rain", 4: "Heavy Rain/Snow"}
    
    # Mengubah tipe data dan mapping dengan aman
    if 'season' in df.columns:
        df["season"] = df["season"].map(season_map)
    if 'weathersit' in df.columns:
        df["weathersit"] = df["weathersit"].map(weather_map)
    
    # Memastikan kolom 'hr' ada untuk grafik jam
    return df

try:
    df = load_data()

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🚲 Bike Sharing Analytics")
        st.markdown("Analisis data penyewaan sepeda untuk proyek akhir.")
        
        # Filter Interaktif
        if 'season' in df.columns:
            selected_season = st.multiselect(
                "Pilih Musim:",
                options=df["season"].unique(),
                default=df["season"].unique()
            )
            main_df = df[df["season"].isin(selected_season)]
        else:
            main_df = df

    # --- MAIN PAGE ---
    st.header("Dashboard Analisis Penyewaan Sepeda ✨")
    
    # 2. Layouting KPI (Metrics) - Menampilkan angka besar di atas
    col1, col2, col3 = st.columns(3)
    with col1:
        total_rentals = main_df["cnt"].sum()
        st.metric("Total Penyewaan", value=f"{total_rentals:,}")
    with col2:
        avg_rentals = round(main_df["cnt"].mean(), 2)
        st.metric("Rata-rata per Jam", value=avg_rentals)
    with col3:
        max_rentals = main_df["cnt"].max()
        st.metric("Puncak Penyewaan", value=f"{max_rentals:,}")

    st.divider()

    # 3. Grafik Bar: Musim & Cuaca (Berdampingan)
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Penyewaan per Musim")
        if 'season' in main_df.columns:
            season_rental = main_df.groupby("season")["cnt"].sum().reset_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=season_rental, x="season", y="cnt", palette="viridis", ax=ax)
            ax.set_ylabel("Jumlah Rental")
            ax.set_xlabel(None)
            st.pyplot(fig)

    with col_right:
        st.subheader("Penyewaan per Kondisi Cuaca")
        if 'weathersit' in main_df.columns:
            weather_rental = main_df.groupby("weathersit")["cnt"].sum().reset_index()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=weather_rental, x="weathersit", y="cnt", palette="rocket", ax=ax)
            ax.set_ylabel("Jumlah Rental")
            ax.set_xlabel(None)
            st.pyplot(fig)

    # 4. Line Chart: Tren Jam (Full Width)
    st.subheader("📈 Tren Rata-rata Penyewaan per Jam")
    if 'hr' in main_df.columns:
        hourly_rental = main_df.groupby("hr")["cnt"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(16, 6))
        sns.lineplot(data=hourly_rental, x="hr", y="cnt", marker="o", color="#2E86C1", linewidth=2.5, ax=ax)
        ax.set_xlabel("Jam (0-23)")
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)

    st.caption("Dashboard Analisis Bike Sharing Dataset - Proyek Dicoding")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.info("Pastikan file 'main_data.csv' berada di folder yang sama dengan script ini.")