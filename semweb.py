import streamlit as st
import os
from rdflib import Graph

# --- KONFIGURASI HALAMAN & GAYA (CSS) ---
st.set_page_config(
    page_title="Naskah Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
)

# CSS Kustom untuk semua permintaan UI baru
st.markdown("""
<style>
    /* [UMUM] */
    .block-container {
        padding-top: 2rem;
    }
    .stApp { 
        background-color: #f0f2f6; 
    }

    /* [C. Navbar] */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        display: block;
        width: 100%;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.75rem;
        padding: 12px 20px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        font-weight: 500;
        color: #495057;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background-color: #e9ecef;
        border-color: #dee2e6;
    }
    /* [IMPROV 3] Gaya untuk tombol navbar yang SEDANG AKTIF (selected) */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > div:has(input:checked) label {
        background-color: rgba(30, 60, 114, 0.15); /* Background biru transparan */
        border-color: #1e3c72; /* Border biru tua */
        color: #1e3c72 !important; /* Warna font biru tua */
        font-weight: 700; /* Font lebih tebal */
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > div:has(input:checked) label p {
        color: #1e3c72 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] input {
        display: none;
    }

    /* [B. Halaman Transliterasi] */
    /* [IMPROV 1] Membuat kolom gambar fixed saat sidebar buka-tutup */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) {
        flex: 0 0 40%; /* Menetapkan lebar kolom pertama (gambar) sebesar 40% dan tidak bisa menyusut */
        min-width: 400px; /* Lebar minimum agar tidak terlalu kecil di layar besar */
    }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
        flex-grow: 1; /* Membiarkan kolom kedua (teks) mengisi sisa ruang */
    }

    .pagination-container {
        text-align: center;
        margin-top: 1.5rem;
    }
    .pagination-container .stButton > button {
        border-radius: 0.5rem !important;
        width: 45px;
        height: 45px;
    }
    .nav-buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
    }
    .nav-buttons .stButton > button {
        background-color: transparent;
        border: none;
        font-size: 1.5rem;
    }
    .page-indicator {
        font-weight: bold;
        color: #1e3c72;
    }

    .transliterasi-wrapper {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 70vh;
        display: flex;
        flex-direction: column;
    }
    .transliterasi-content {
        overflow-y: auto;
        flex-grow: 1;
    }
    .transliterasi-item {
        margin-bottom: 1.5rem;
        border-left: 4px solid #a6caff;
        padding-left: 1rem;
    }

    /* [A. Halaman Pencarian] */
    div[data-testid="stTextInput"] > div {
        background-color: rgba(222, 226, 230, 0.5);
        border: 2px solid #ced4da;
    }
    div[data-testid="stTextInput"] > div:focus-within {
        border-color: #1e3c72;
        box-shadow: none;
    }
    .search-result-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }

    /* [D. Tambahan] */
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
    except Exception:
        return []

# --- DATA & STATE ---
rdf_data = load_rdf_data("naskah_bhakti_final.ttl")
TOTAL_PAGES = 20
if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# --- UI UTAMA ---

st.title("Naskah Kakawin Ramayana")

# Navigasi di Sidebar
with st.sidebar:
    st.markdown("##")
    page = st.radio(
        "Navigasi", 
        ["📖 Transliterasi", "🔍 Pencarian", "ℹ️ Tentang Naskah"],
        key="nav"
    )
    st.markdown("---")
    st.info("Aplikasi web semantik untuk eksplorasi naskah kakawin ramayana.")

# --- KONTEN HALAMAN ---
if page == "📖 Transliterasi":
    col1, col2 = st.columns([2, 3], gap="large")

    with col1:
        st.header(f"Halaman Naskah {st.session_state.page_num}")
        image_path = os.path.join("images", f"page_{st.session_state.page_num}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning(f"Gambar 'page_{st.session_state.page_num}.png' tidak ditemukan.")

        st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
        if st.button("⬅️", key="prev_button"):
            if st.session_state.page_num > 1:
                st.session_state.page_num -= 1
                st.rerun()
        # [IMPROV 2] Mengubah format indikator halaman
        st.markdown(f'<span class="page-indicator">{st.session_state.page_num}/{TOTAL_PAGES}</span>', unsafe_allow_html=True)
        if st.button("➡️", key="next_button"):
            if st.session_state.page_num < TOTAL_PAGES:
                st.session_state.page_num += 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
        st.write("Lompat ke Halaman:")
        page_cols = st.columns(10)
        for i in range(20):
            col_index = i % 10
            if page_cols[col_index].button(f"{i+1}", key=f"page_{i+1}"):
                st.session_state.page_num = i + 1
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.header("Transliterasi & Terjemahan")
        st.markdown('<div class="transliterasi-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="transliterasi-content">', unsafe_allow_html=True)
        
        if st.session_state.page_num == 3:
            for item in rdf_data:
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
        
        st.markdown('</div></div>', unsafe_allow_html=True)

elif page == "🔍 Pencarian":
    st.header("Pencarian Teks")
    search_query = st.text_input("Cari kata kunci", placeholder="Contoh: rama, bhakti, prajurit...", label_visibility="collapsed")
    
    st.markdown("---")

    if search_query:
        query_lower = search_query.lower()
        results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
        st.subheader(f"Ditemukan {len(results)} hasil untuk '{search_query}'")
        
        for item in results:
            st.markdown(f"""
            <div class="search-result-container">
                <strong>Transliterasi Latin</strong>
                <p style="font-style: italic;">{item['latin']}</p>
                <hr>
                <strong>Terjemahan Indonesia</strong>
                <p>{item['terjemahan']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Masukkan kata kunci untuk mencari di semua data transliterasi yang tersedia.")

elif page == "ℹ️ Tentang Naskah":
    st.header("Tentang Naskah Kakawin Ramayana")
    st.image("https://images.unsplash.com/photo-1618335914367-523a1d355050?q=80&w=1932&auto=format&fit=crop", use_container_width=True)
    st.markdown("""
    **Kakawin Ramayana** adalah sebuah karya sastra Jawa Kuno yang adiluhung, diperkirakan digubah pada masa Kerajaan Medang (Mataram Kuno) sekitar abad ke-9 Masehi. Karya ini merupakan adaptasi dari epos Ramayana karya Walmiki dari India, namun tidak sekadar terjemahan. Sang pujangga Jawa Kuno berhasil menyuntikkan nilai-nilai lokal, pandangan hidup, dan keindahan bahasa yang khas, menjadikannya sebuah mahakarya yang berdiri sendiri.

    Secara garis besar, naskah kakawin ramayana ini menceritakan kisah **Sang Rama**, seorang pangeran dari Ayodhya, yang harus menjalani pengasingan di hutan selama 14 tahun bersama istrinya, **Sita**, dan adiknya, **Laksmana**. Puncak konflik terjadi ketika Sita diculik oleh Rahwana, raja raksasa dari Alengka. Peperangan besar pun tak terelakkan, di mana Rama dibantu oleh pasukan kera yang dipimpin oleh Hanuman dan Sugriwa.

    Aplikasi ini bertujuan untuk melestarikan dan memudahkan akses terhadap naskah kakawin ramayana, menyajikan transliterasi dan terjemahan agar dapat dipelajari oleh generasi masa kini.
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Naskah Kakawin Ramayana | Proyek Web Semantik © 2025</p>
</div>
""", unsafe_allow_html=True)