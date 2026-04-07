import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. KONFIGURASI HALAMAN (Tampilan Wide & Tema Modern)
st.set_page_config(page_title="Bike Sharing Dashboard Premium", layout="wide")

# Mengatur tema global Seaborn agar bersih (Tanpa Grid)
sns.set_theme(style="white") 
# Mengatur font default agar lebih rapi
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#333333'

# 2. FUNGSI LOAD DATA (Dengan Caching & Path Aman)
@st.cache_data
def load_data():
    # Menangani path file agar aman di lokal maupun Streamlit Cloud
    file_path = "dashboard/main_data.csv"
    if not os.path.exists(file_path):
        file_path = "main_data.csv"
        
    df = pd.read_csv(file_path)
    
    # Mapping label Season agar informatif (Penting untuk Reviewer)
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    if 'season' in df.columns:
        df["season"] = df["season"].map(season_map)
        
    return df

# Memanggil data ke dalam variabel df
df = load_data()

# 3. SIDEBAR (Styling Kontrol)
with st.sidebar:
    # Menambah Logo Dicoding (Contoh profesional)
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logistics/logo.png", width=150)
    st.title("🚲 Bike Analytics Pro")
    st.markdown("---")
    st.markdown("### 🛠️ Filter Panel")
    
    # Filter Multiselect: User bisa pilih musim apa saja
    selected_season = st.multiselect(
        "Pilih Musim:",
        options=df["season"].unique(),
        default=df["season"].unique(),
        help="Pilih satu atau lebih musim untuk memperbarui dashboard."
    )
    st.markdown("---")
    st.caption("Dashboard v2.0 | User ID: Student")

# LOGIKA FILTER: 'main_df' adalah data yang sudah responsif
main_df = df[df["season"].isin(selected_season)]

# 4. MAIN PAGE (Header & KPI)
st.title("Dashboard Analisis Penyewaan Sepeda ✨")
st.markdown("Menampilkan tren data interaktif untuk periode **2011-2012**.")
st.markdown("---")

# Menampilkan Ringkasan Angka (Metrics dengan Warna)
st.markdown("### 📊 Ringkasan Performa")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan (Sesuai Filter)", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Penyewaan per Jam", value=f"{main_df['cnt'].mean():.2f}")
with col3:
    st.metric("Puncak Penyewaan", value=f"{main_df['cnt'].max():,}", delta="Angka Tertinggi")

st.markdown("---")

# 5. GRAFIK TREN JAM (Highlight Utama - Responsif & Estetik)
st.markdown("### 📈 Tren Rata-rata Penyewaan per Jam")
st.markdown("*Kunci Keberhasilan Bisnis: Memahami kapan permintaan mencapai puncaknya.*")

# Menghitung rata-rata menggunakan data yang SUDAH DIFILTER (main_df)
hourly_rental = main_df.groupby("hr")["cnt"].mean().reset_index()

# Membuat Grafik Garis Modern
fig, ax = plt.subplots(figsize=(16, 6))

# Menggunakan warna biru premium (#2E86C1) dan garis yang lebih tebal
sns.lineplot(
    data=hourly_rental, 
    x="hr", 
    y="cnt", 
    marker="o", 
    markersize=8,
    color="#1E3F66", # Biru Tua Modern
    linewidth=3, 
    ax=ax
)

# Menambahkan Area Fill di bawah garis agar lebih dramatis
ax.fill_between(hourly_rental["hr"], hourly_rental["cnt"], color="#BCDAF0", alpha=0.4)

# Menghapus Outline Box agar bersih (Chart Junk Reduction)
sns.despine(left=True, bottom=True)

# Memperjelas Label & Judul (Feedback Reviewer)
ax.set_title("Puncak Penyewaan Terjadi di Jam Sibuk (Pagi & Sore)", fontsize=16, fontweight='bold', loc='left', pad=20)
ax.set_xlabel("Jam (Rentang Waktu 00:00 - 23:00)", fontsize=13, fontweight='bold', labelpad=15)
ax.set_ylabel("Rata-rata Penyewaan", fontsize=13, fontweight='bold', labelpad=15)

# Mengatur Ticks agar rapi
ax.set_xticks(range(0, 24))
ax.tick_params(axis='both', which='major', labelsize=11)

st.pyplot(fig)

st.markdown("---")

# 6. GRAFIK KATEGORI (Bar Chart Musim & Cuaca Berdampingan)
st.markdown("### 🏛️ Analisis Berdasarkan Faktor Eksternal")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Penyewaan Berdasarkan Musim")
    season_rental = main_df.groupby("season")["cnt"].sum().reset_index()
    # Mengurutkan berdasarkan jumlah rental tertinggi
    season_rental = season_rental.sort_values(by="cnt", ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Menggunakan palet warna konsisten ('Blues_d' untuk gradasi)
    sns.barplot(data=season_rental, x="season", y="cnt", palette="Blues_d", ax=ax)
    
    # Despine & Label Rapi
    sns.despine(left=True, bottom=True)
    ax.set_ylabel("Total Jumlah Rental (Juta)", fontsize=12, labelpad=10)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=12)
    
    # Menghapus Tick Marks di sumbu Y agar bersih
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x/1000000)) + "M"))
    
    st.pyplot(fig)

with col_right:
    st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")
    if 'weathersit' in main_df.columns:
        weather_rental = main_df.groupby("weathersit")["cnt"].sum().reset_index()
        weather_rental = weather_rental.sort_values(by="cnt", ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Menggunakan palet warna hangat ('Reds_d') agar kontras dengan musim
        sns.barplot(data=weather_rental, x="weathersit", y="cnt", palette="Reds_d", ax=ax)
        
        # Despine & Label Rapi
        sns.despine(left=True, bottom=True)
        ax.set_ylabel(None)
        ax.set_xlabel("Kategori Cuaca", fontsize=12, labelpad=10)
        ax.tick_params(axis='x', labelsize=11)
        
        # Menghapus Tick Marks di sumbu Y (karena sudah ada di sebelah kiri)
        ax.set_yticks([])
        
        st.pyplot(fig)

# 7. FOOTER
st.markdown("---")
st.caption("Dashboard Analisis Bike Sharing Dataset | Submission Akhir Dicoding | Oleh: Rani Student")