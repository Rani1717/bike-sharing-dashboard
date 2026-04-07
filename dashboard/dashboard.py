import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Konfigurasi Halaman (Wajib di baris pertama setelah import)
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
sns.set_theme(style="whitegrid")

# 2. Fungsi Load Data dengan Cache agar Cepat
@st.cache_data
def load_data():
    # Menangani path file agar aman di lokal maupun Streamlit Cloud
    file_path = "dashboard/main_data.csv"
    if not os.path.exists(file_path):
        file_path = "main_data.csv"
        
    df = pd.read_csv(file_path)
    
    # Mapping label Season agar informatif (Sesuai saran reviewer)
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    if 'season' in df.columns:
        df["season"] = df["season"].map(season_map)
        
    return df

# Memanggil data ke dalam variabel df
df = load_data()

# 3. SIDEBAR (Filter Utama)
with st.sidebar:
    st.title("🚲 Bike Sharing Analytics")
    st.markdown("### Filter Musim")
    
    # Filter Multiselect: User bisa pilih musim apa saja
    selected_season = st.multiselect(
        "Pilih Musim:",
        options=df["season"].unique(),
        default=df["season"].unique()
    )

# LOGIKA FILTER: 'main_df' adalah data yang sudah difilter oleh user
# Ini kunci agar grafik JAM tidak statis (Sesuai revisi reviewer)
main_df = df[df["season"].isin(selected_season)]

# 4. MAIN PAGE
st.header("Dashboard Analisis Penyewaan Sepeda ✨")
st.markdown("Menampilkan tren data penyewaan sepeda periode 2011-2012.")

# Menampilkan Ringkasan Angka (Metrics)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata per Jam", value=f"{main_df['cnt'].mean():.2f}")
with col3:
    st.metric("Puncak Penyewaan", value=f"{main_df['cnt'].max():,}")

st.divider()

# Bar Chart Musim & Cuaca
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Penyewaan per Musim")
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
        sns.barplot(data=weather_rental, x="weathersit", y="cnt", palette="magma", ax=ax)
        ax.set_ylabel("Jumlah Rental")
        ax.set_xlabel("Kategori Cuaca")
        st.pyplot(fig)

# 5. GRAFIK TREN JAM (Poin Utama Revisi)
# Judul diperjelas dengan rentang waktu
st.subheader("📈 Tren Rata-rata Penyewaan per Jam (2011-2012)")

# Menghitung rata-rata menggunakan data yang SUDAH DIFILTER (main_df)
hourly_rental = main_df.groupby("hr")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(data=hourly_rental, x="hr", y="cnt", marker="o", color="#2E86C1", linewidth=2.5, ax=ax)

# Memperjelas Label Sumbu (Sesuai kotak merah reviewer)
ax.set_xlabel("Jam (Rentang Waktu 00:00 - 23:00)", fontsize=12)
ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
ax.set_xticks(range(0, 24))

st.pyplot(fig)

st.caption("Dicoding Data Analysis Project - 2026")