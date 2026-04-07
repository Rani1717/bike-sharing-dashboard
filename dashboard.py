import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
sns.set_theme(style="whitegrid")

# 1. Optimasi Load Data dengan Cache
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    
    # Mapping label langsung di dalam cache
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {1: "Clear", 2: "Mist", 3: "Light Snow/Rain", 4: "Heavy Rain/Snow"}
    
    df["season"] = df["season"].map(season_map)
    df["weathersit"] = df["weathersit"].map(weather_map)
    return df

df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logistics/logo.png", width=100) # Contoh Logo
    st.title("🚲 Bike Sharing Analytics")
    
    # Filter Interaktif
    selected_season = st.multiselect(
        "Pilih Musim:",
        options=df["season"].unique(),
        default=df["season"].unique()
    )

# Filter Data Berdasarkan Sidebar
main_df = df[df["season"].isin(selected_season)]

# --- MAIN PAGE ---
st.header("Dashboard Analisis Penyewaan Sepeda ✨")
st.markdown("Menampilkan insight dari dataset bike sharing untuk optimasi bisnis.")

# 2. Layouting KPI (Metrics)
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df["cnt"].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")

with col2:
    avg_rentals = round(main_df["cnt"].mean(), 2)
    st.metric("Rata-rata per Jam", value=avg_rentals)

with col3:
    max_rentals = main_df["cnt"].max()
    st.metric("Penyewaan Tertinggi", value=max_rentals)

st.divider()

# 3. Bar Chart: Musim & Cuaca (Berdampingan)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Penyewaan per Musim")
    season_rental = main_df.groupby("season")["cnt"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=season_rental, x="season", y="cnt", palette="viridis", ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

with col_right:
    st.subheader("Penyewaan per Kondisi Cuaca")
    weather_rental = main_df.groupby("weathersit")["cnt"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weather_rental, x="weathersit", y="cnt", palette="magma", ax=ax)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

# 4. Line Chart: Tren Jam (Full Width)
st.subheader("📈 Tren Rata-rata Penyewaan per Jam")
hourly_rental = main_df.groupby("hr")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(16, 6))
sns.lineplot(data=hourly_rental, x="hr", y="cnt", marker="o", color="#2E86C1", linewidth=2.5, ax=ax)
ax.set_title("Puncak penyewaan biasanya terjadi di jam sibuk", fontsize=12, color="grey")
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

st.caption(f"Copyright © 2026 | Bike Sharing Project | User ID: {st.session_state.get('user_id', 'Student')}")