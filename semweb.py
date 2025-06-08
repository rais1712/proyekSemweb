import streamlit as st
import os
from rdflib import Graph
import base64
import html
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Digitalisasi Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNGSI PEMUATAN ASET (CSS, JS, GAMBAR) ---
def load_asset(file_path):
    """Fungsi untuk memuat file CSS atau JS eksternal"""
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Peringatan: File aset tidak ditemukan di '{file_path}'. Beberapa fitur mungkin tidak berfungsi.")
        return ""

def get_image_as_base64(file_path):
    """Fungsi untuk mengonversi gambar menjadi base64 untuk injeksi HTML"""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

# --- PEMUATAN DATA RDF ---
@st.cache_data
def load_rdf_data(ttl_file="naskah_bhakti_final.ttl"):
    if not os.path.exists(ttl_file):
        st.error(f"Berkas data '{ttl_file}' tidak ditemukan.")
        return None
    try:
        g = Graph()
        g.parse(ttl_file, format="turtle")
        query = """
        PREFIX jawa: <http://example.org/jawa#>
        SELECT ?kalimat_uri ?latin ?terjemahan WHERE {
            ?kalimat_uri a jawa:Kalimat ;
                         jawa:latin ?latin ;
                         jawa:terjemahan ?terjemahan .
        } ORDER BY ?kalimat_uri
        """
        results = g.query(query)
        data = [{"uri": str(r.kalimat_uri), "latin": str(r.latin), "terjemahan": str(r.terjemahan)} for r in results]
        if not data:
            st.warning("Tidak ada data transliterasi yang dimuat dari file TTL.")
        return data
    except Exception as e:
        st.error(f"Gagal memuat data RDF: {e}")
        return None

# --- FUNGSI RENDER KOMPONEN UI ---
def render_hero_section():
    """Merender Hero Section yang modern (Req 1)"""
    st.markdown("""
        <section class="hero-section">
            <h1 class="hero-title">Kakawin Ramayana</h1>
            <p class="hero-subtitle">Menjelajahi Kekayaan Sastra Jawa Kuno Melalui Digitalisasi Interaktif</p>
        </section>
    """, unsafe_allow_html=True)

def render_breadcrumb(page_name, page_num=None):
    """Merender breadcrumb untuk navigasi (Req 3)"""
    base = "Beranda"
    if page_num:
        trail = f" > Transliterasi > <span>Halaman {page_num}</span>"
    else:
        trail = f" > <span>{page_name}</span>"
    st.markdown(f'<div class="breadcrumb">{base}{trail}</div>', unsafe_allow_html=True)

def render_search_results(results, query):
    """Merender hasil pencarian dengan highlight (Req 4)"""
    if not results:
        st.info("Tidak ada hasil yang cocok ditemukan.")
        return
    
    st.success(f"Ditemukan {len(results)} hasil untuk '{html.escape(query)}'")
    
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    
    for item in results:
        latin_escaped = html.escape(item['latin'])
        translation_escaped = html.escape(item['terjemahan'])
        
        latin_highlighted = pattern.sub(
            lambda m: f"<span class='search-highlight'>{m.group(0)}</span>", 
            latin_escaped
        )
        translation_highlighted = pattern.sub(
            lambda m: f"<span class='search-highlight'>{m.group(0)}</span>", 
            translation_escaped
        )
        
        st.markdown(f"""
            <div class="transliterasi-item">
                <div class="latin-text">{latin_highlighted}</div>
                <div class="translation-text"><strong>Terjemahan:</strong> {translation_highlighted}</div>
            </div>
        """, unsafe_allow_html=True)

# --- HALAMAN UTAMA: TRANSLITERASI ---
def page_transliterasi(rdf_data):
    TOTAL_PAGES = 20 # Total halaman naskah
    
    # --- Advanced Navigation System (Req 3) ---
    with st.container():
        st.markdown('<div class="navigation-container">', unsafe_allow_html=True)
        
        # Quick Jump Slider
        page_num = st.slider(
            "Lompat ke Halaman", 
            min_value=1, 
            max_value=TOTAL_PAGES, 
            value=st.session_state.get('page_num', 1),
            key="page_slider"
        )
        st.session_state.page_num = page_num
        
        # Progress Indicator & Breadcrumb
        col_prog, col_crumb = st.columns([1,2])
        with col_prog:
            st.progress(page_num / TOTAL_PAGES, text=f"Progres Menjelajah: {int((page_num/TOTAL_PAGES)*100)}%")
        with col_crumb:
             render_breadcrumb("Transliterasi", page_num)
        
        st.markdown('</div>', unsafe_allow_html=True)


    # --- Dual-Pane Layout Revolution (Req 2) & Image Lightbox (Req 6) ---
    st.markdown('<div class="dual-pane-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 4], gap="large")

    with col1:
        st.subheader(f"Naskah Asli: Halaman {page_num}")
        image_path = f"images/page_{page_num}.png"
        if os.path.exists(image_path):
            st.markdown(f"""
                <div class="manuscript-panel">
                    <img id="manuscriptImage" src="data:image/png;base64,{get_image_as_base64(image_path)}" class="manuscript-image" alt="Naskah halaman {page_num}">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Gambar naskah untuk halaman {page_num} tidak ditemukan di folder 'images'.")

    with col2:
        st.subheader("Teks & Terjemahan")
        st.markdown('<div class="transliterasi-panel">', unsafe_allow_html=True)
        
        # Saat ini data RDF hanya untuk halaman 3
        if page_num == 3 and rdf_data:
            for item in rdf_data:
                st.markdown(f"""
                <div class="transliterasi-item">
                    <div class="latin-text">{html.escape(item['latin'])}</div>
                    <div class="translation-text"><strong>Terjemahan:</strong> {html.escape(item['terjemahan'])}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"Data transliterasi untuk halaman {page_num} belum tersedia dalam file RDF.")
            st.markdown("""
            **Catatan:** Proyek digitalisasi ini sedang berjalan. Saat ini, data RDF yang tersedia secara semantik hanya untuk **halaman 3** sebagai percontohan.
            """)

        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- HALAMAN PENCARIAN ---
def page_pencarian(rdf_data):
    render_breadcrumb("Pencarian")
    st.subheader("🔍 Pencarian Teks Lanjutan")
    
    search_query = st.text_input(
        "Cari dalam naskah (Latin atau Terjemahan):",
        placeholder="Contoh: 'bhakti' atau 'prajurit'"
    )
    
    if search_query:
        if rdf_data:
            query_lower = search_query.lower()
            results = [
                item for item in rdf_data 
                if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()
            ]
            render_search_results(results, search_query)
        else:
            st.error("Data RDF tidak dapat dimuat, fitur pencarian tidak tersedia.")
    else:
        st.info("Masukkan kata kunci untuk memulai pencarian pada data yang tersedia (Halaman 3).")

# --- APLIKASI UTAMA ---
def main():
    # Muat CSS & JS sekali saja
    css = load_asset("assets/style.css")
    js = load_asset("assets/script.js")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    # Inisialisasi state jika belum ada
    if 'page_num' not in st.session_state:
        st.session_state.page_num = 1
    
    # Render Hero Section
    render_hero_section()

    # Navigasi utama dengan tab
    page_transliterasi_tab, page_pencarian_tab = st.tabs(["📖 Transliterasi Naskah", "🔍 Pencarian"])

    # Muat data RDF
    rdf_data = load_rdf_data()

    with page_transliterasi_tab:
        page_transliterasi(rdf_data)

    with page_pencarian_tab:
        if rdf_data:
            page_pencarian(rdf_data)
        else:
            st.error("Data tidak dapat dimuat. Fitur pencarian tidak bisa digunakan.")

    # Lightbox HTML structure (ditaruh di akhir agar tidak mengganggu layout)
    # ID ini dicari oleh script.js
    st.markdown("""
        <div id="imageLightbox" class="lightbox">
            <span class="lightbox-close">&times;</span>
            <img class="lightbox-content" id="lightboxImage">
        </div>
    """, unsafe_allow_html=True)
    
    # Injeksi Javascript di akhir body
    st.components.v1.html(f"<script>{js}</script>", height=0)


if __name__ == "__main__":
    main()