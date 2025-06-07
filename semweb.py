import streamlit as st
from rdflib import Graph
import os

# --- KONFIGURASI HALAMAN & GAYA (CSS) ---
st.set_page_config(
    page_title="Naskah Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
)

# CSS Kustom untuk semua permintaan UI baru
st.markdown("""
<style>
    /* 1. Navbar dengan kotak yang bisa di-select */
    .stRadio > div {
        display: flex;
        flex-direction: column;
    }
    .stRadio > div > label {
        background-color: #e8f0fe;
        border: 1px solid #d6e4ff;
        border-radius: 0.5rem;
        padding: 10px 15px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    /* Warna saat di-hover */
    .stRadio > div > label:hover {
        background-color: #d6e4ff;
        border-color: #a6caff;
    }
    /* Warna saat radio button terpilih (selected) */
    .stRadio > div > label[data-baseweb="radio"] > div:first-child[aria-checked="true"] + div {
        color: #1e3c72;
        font-weight: bold;
    }
    .stRadio > div > label[data-baseweb="radio"] > div:first-child[aria-checked="true"] + div > p {
        color: #1e3c72;
        font-weight: bold;
    }
    /* Menyembunyikan radio button asli */
    .stRadio > div > label > div:first-child {
        display: none;
    }

    /* 2. Tombol Navigasi Halaman (Next/Prev) */
    .nav-buttons {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
    }
    .page-indicator {
        font-weight: bold;
        color: #1e3c72;
    }

    /* 3. Panel Transliterasi yang bisa di-scroll */
    .scrollable-panel {
        background-color: #f8f9fa;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        height: 60vh; /* Sesuaikan tinggi sesuai kebutuhan */
        overflow-y: auto;
    }
    /* 3. Tampilan teks transliterasi baru */
    .transliterasi-item {
        margin-bottom: 1.5rem;
        border-left: 4px solid #a6caff;
        padding-left: 1rem;
    }

    /* 4. Box Pencarian */
    div[data-testid="stTextInput"] > div {
        background-color: rgba(232, 240, 254, 0.5);
    }
    div[data-testid="stTextInput"] > div:focus-within {
        border-color: #1e3c72;
        box-shadow: 0 0 0 2px rgba(30, 60, 114, 0.3);
    }

    /* 4. Hasil Pencarian ala referensi */
    .search-result-container {
        display: flex;
        flex-direction: row;
        gap: 2rem;
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .search-result-col1 {
        flex-basis: 40%;
    }
    .search-result-col2 {
        flex-basis: 60%;
        border-left: 1px solid #e9ecef;
        padding-left: 2rem;
    }
    
    /* 5. Improvisasi Tampilan */
    .stApp { background-color: #f0f2f6; }
    .block-container { padding-top: 2rem; }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6c757d;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# --- FUNGSI HELPER ---
@st.cache_data
def load_rdf_data(ttl_file):
    g = Graph()
    try:
        g.parse(ttl_file, format="turtle")
        query = "PREFIX jawa: <http://example.org/jawa#> SELECT ?kalimat_uri ?latin ?terjemahan WHERE { ?kalimat_uri a jawa:Kalimat ; jawa:latin ?latin ; jawa:terjemahan ?terjemahan . } ORDER BY ?kalimat_uri"
        results = g.query(query)
        data = [{"uri": str(r.kalimat_uri), "latin": str(r.latin), "terjemahan": str(r.terjemahan)} for r in results]
        return data
    except Exception as e:
        st.error(f"Gagal memuat atau mem-parsing file TTL: {e}")
        return []

# --- Memuat Data ---
rdf_data = load_rdf_data("naskah_bhakti_final.ttl")
TOTAL_PAGES = 20

# --- UI UTAMA ---

st.title("Naskah Kakawin Ramayana")

# --- NAVIGASI ---
with st.sidebar:
    st.markdown("##")
    # 1. Navbar dalam kotak
    page = st.radio(
        "Navigasi", 
        ["📖 Transliterasi", "🔍 Pencarian"],
        label_visibility="collapsed" # Sembunyikan label "Navigasi"
    )
    st.markdown("---")
    st.info("Aplikasi web semantik untuk eksplorasi naskah kuno.")

# Inisialisasi session state untuk nomor halaman
if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# --- KONTEN HALAMAN ---

if page == "📖 Transliterasi":
    col1, col2 = st.columns([2, 3], gap="large")

    # Kolom Kiri: Gambar Naskah dan Navigasi
    with col1:
        st.header(f"Halaman Naskah {st.session_state.page_num}")
        image_path = os.path.join("images", f"page_{st.session_state.page_num}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning(f"Gambar 'page_{st.session_state.page_num}.png' tidak ditemukan.")

        # 2. Tombol Navigasi Halaman (Next/Prev)
        st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
        nav_cols = st.columns([1, 2, 1])
        if nav_cols[0].button("⬅️ Sebelumnya", use_container_width=True, disabled=(st.session_state.page_num == 1)):
            st.session_state.page_num -= 1
            st.rerun()
        
        nav_cols[1].markdown(f'<div class="page-indicator">Halaman {st.session_state.page_num} dari {TOTAL_PAGES}</div>', unsafe_allow_html=True)

        if nav_cols[2].button("Selanjutnya ➡️", use_container_width=True, disabled=(st.session_state.page_num == TOTAL_PAGES)):
            st.session_state.page_num += 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Kolom Kanan: Transliterasi & Terjemahan
    with col2:
        st.header("Transliterasi & Terjemahan")
        # 3. Panel yang bisa di-scroll
        with st.container():
            st.markdown('<div class="scrollable-panel">', unsafe_allow_html=True)
            if st.session_state.page_num == 3:
                if not rdf_data:
                    st.warning("Data RDF tidak berhasil dimuat.")
                else:
                    for item in rdf_data:
                        # 3. Tampilan teks baru
                        st.markdown(f"""
                        <div class="transliterasi-item">
                            <strong>Latin:</strong>
                            <p><em>{item['latin']}</em></p>
                            <strong>Terjemahan:</strong>
                            <p>{item['terjemahan']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Data transliterasi untuk halaman ini belum tersedia.")
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "🔍 Pencarian":
    st.header("Pencarian Semantik")
    # 4. Box pencarian dengan style baru
    search_query = st.text_input("Cari kata kunci dalam data yang tersedia", placeholder="Contoh: rama, bhakti, prajurit...", label_visibility="collapsed")

    st.markdown("---")

    if search_query:
        query_lower = search_query.lower()
        results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
        
        st.subheader(f"Ditemukan {len(results)} hasil untuk '{search_query}'")
        
        # 4. Hasil pencarian dengan desain referensi
        for item in results:
            st.markdown(f"""
            <div class="search-result-container">
                <div class="search-result-col1">
                    <strong>Aksara Sunda (Contoh)</strong>
                    <div style="font-size: 24px; background: #f8f9fa; padding: 10px; border-radius: 8px; font-family: 'Noto Sans Sundanese', serif;">
                        ᮕᮢᮏᮥᮛᮤᮒ᮪
                    </div>
                    <br>
                    <strong>Transliterasi Latin</strong>
                    <p style="font-style: italic;">{item['latin']}</p>
                </div>
                <div class="search-result-col2">
                    <strong>Terjemahan Indonesia</strong>
                    <p>{item['terjemahan']}</p>
                    <hr>
                    <strong>Metadata (Contoh)</strong>
                    <p style="font-size: 0.9em; color: #6c757d;">
                        ID Naskah: P1<br>
                        ID Baris: {item['uri'].split('#')[-1]}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # 5. Improvisasi: Tampilan lebih berisi saat belum ada pencarian
        st.info("Silakan masukkan kata kunci untuk memulai pencarian pada data yang tersedia (saat ini hanya data di Halaman 3).")
        st.image("https://images.unsplash.com/photo-1583361248329-01114b0976d0?q=80&w=2070&auto=format&fit=crop", 
                 caption="Eksplorasi Naskah Kuno", use_container_width=True)

# 5. Improvisasi: Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Naskah Kakawin Ramayana | Proyek Web Semantik © 2025</p>
</div>
""", unsafe_allow_html=True)