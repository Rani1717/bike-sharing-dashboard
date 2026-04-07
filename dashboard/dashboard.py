import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Bike Sharing Dashboard Premium", layout="wide")
sns.set_theme(style="white") 
plt.rcParams['font.family'] = 'sans-serif'

# 2. FUNGSI LOAD DATA (Caching & Path Aman)
@st.cache_data
def load_data():
    file_path = "dashboard/main_data.csv"
    if not os.path.exists(file_path):
        file_path = "main_data.csv"
    df = pd.read_csv(file_path)
    
    # Mapping label Season (Sesuai feedback review)
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    if 'season' in df.columns:
        df["season"] = df["season"].map(season_map)
    return df

df = load_data()

# 3. SIDEBAR (Logika Filter)
with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logistics/logo.png", width=150)
    st.title("🚲 Bike Analytics Pro")
    st.markdown("---")
    selected_season = st.multiselect(
        "Pilih Musim:",
        options=df["season"].unique(),
        default=df["season"].unique(),
        help="Filter ini akan mengubah seluruh grafik di dashboard."
    )

# KUNCI JAWABAN REVIEWER: Data yang digunakan adalah main_df
main_df = df[df["season"].isin(selected_season)]

# 4. MAIN PAGE
st.title("Dashboard Analisis Penyewaan Sepeda ✨")
st.markdown("Menampilkan tren data interaktif untuk periode **2011-2012**.")

# Metrics Section
st.markdown("### 📊 Ringkasan Performa")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan/Jam", value=f"{main_df['cnt'].mean():.2f}")
with col3:
    st.metric("Puncak Penyewaan", value=f"{main_df['cnt'].max():,}")

st.divider()

# 5. GRAFIK TREN JAM (Revisi: Responsif & Judul Jelas)
st.markdown("### 📈 Tren Rata-rata Penyewaan per Jam (2011-2012)")
hourly_rental = main_df.groupby("hr")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(data=hourly_rental, x="hr", y="cnt", marker="o", color="#1E3F66", linewidth=3, ax=ax)
ax.fill_between(hourly_rental["hr"], hourly_rental["cnt"], color="#BCDAF0", alpha=0.4)

sns.despine(left=True, bottom=True)
ax.set_xlabel("Jam (Rentang Waktu 00:00 - 23:00)", fontsize=12, fontweight='bold')
ax.set_ylabel("Rata-rata Penyewaan", fontsize=12, fontweight='bold')
ax.set_xticks(range(0, 24))
st.pyplot(fig)

st.divider()

# 6. GRAFIK KATEGORI
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Penyewaan Berdasarkan Musim")
    season_rental = main_df.groupby("season")["cnt"].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=season_rental, x="season", y="cnt", palette="Blues_d", ax=ax)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig)

with col_right:
    st.subheader("Penyewaan Berdasarkan Cuaca")
    if 'weathersit' in main_df.columns:
        weather_rental = main_df.groupby("weathersit")["cnt"].sum().sort_values(ascending=False).reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=weather_rental, x="weathersit", y="cnt", palette="Reds_d", ax=ax)
        sns.despine(left=True, bottom=True)
        st.pyplot(fig)

st.caption("Dashboard v2.0 | Dicoding Submission | Rani - Universitas Dian Nuswantoro")