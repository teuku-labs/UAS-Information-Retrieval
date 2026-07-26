# app.py
import streamlit as st
import json
import os

DATA_PATH = "data/books.json"

# Konfigurasi Halaman
st.set_page_config(
    page_title="Book Crawler Search", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 10px;
        font-size: 16px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
        padding: 20px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }

    hr {
        margin-top: 0px !important;
        margin-bottom: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Aplikasi
st.markdown("# 📚 Book Crawler Search")
st.markdown("Temukan dan jelajahi koleksi buku dari hasil crawling web.")
st.markdown("---")

# Load data
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    st.error("⚠️ **Data belum tersedia.** Pastikan file `data/books.json` sudah ada.")
    st.info("💡 Jalankan script crawler terlebih dahulu untuk mengambil data.")
    st.stop()

# --- AREA PENCARIAN & FILTER ---
col_search, col_sort = st.columns([3, 1])

with col_search:
    query = st.text_input(
        "Cari buku", 
        placeholder="Ketik judul buku di sini...", 
        label_visibility="collapsed"
    )

with col_sort:
    sort_option = st.selectbox(
        "Urutkan", 
        ["Default", "Harga Terendah", "Harga Tertinggi", "Rating Tertinggi"],
        label_visibility="collapsed"
    )

# --- LOGIKA FILTER & SORTING ---
if query:
    filtered = [item for item in data if query.lower() in item.get("title", "").lower()]
else:
    filtered = data.copy()

# Sorting
if sort_option == "Harga Terendah":
    filtered.sort(key=lambda x: float(x.get("price", "0").replace("£", "").replace("$", "").replace(",", "")))
elif sort_option == "Harga Tertinggi":
    filtered.sort(key=lambda x: float(x.get("price", "0").replace("£", "").replace("$", "").replace(",", "")), reverse=True)
elif sort_option == "Rating Tertinggi":
    filtered.sort(key=lambda x: float(x.get("rating", "0")), reverse=True)

# --- STATUS HASIL ---
st.markdown(f"##### Menampilkan **{len(filtered)}** dari {len(data)} buku")
st.markdown("") # Spacing

# --- TAMPILKAN HASIL (GRID LAYOUT) ---
if not filtered:
    st.warning("🔍 Tidak ada buku yang cocok dengan pencarian Anda. Coba kata kunci lain.")
else:
    # Membuat grid 2 kolom
    cols = st.columns(2)
    
    for index, item in enumerate(filtered):
        col = cols[index % 2]
        
        with col:
            # Card dengan border
            with st.container(border=True):
                # Judul Buku
                st.markdown(f"### {item.get('title', 'Judul Tidak Diketahui')}")
                
                # Metrik Harga dan Rating
                metric_col1, metric_col2 = st.columns(2)
                metric_col1.metric("💰 Harga", item.get('price', 'N/A'))
                metric_col2.metric("⭐ Rating", f"{item.get('rating', '0')} / 5")
                
                # Info Stok
                availability = item.get('availability', 'Unknown')
                if 'in stock' in availability.lower():
                    st.success(f"📦 {availability}", icon=None)
                else:
                    st.error(f"📦 {availability}", icon=None)
                
                st.markdown("") 
                
                # Tombol Link
                st.link_button(
                    "Lihat Detail Buku 🔗", 
                    item.get('link', '#'), 
                    use_container_width=True,
                    type="primary"
                )