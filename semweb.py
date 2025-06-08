import streamlit as st
import os
from rdflib import Graph
import base64

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Naskah Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNGSI BANTUAN ---
# Fungsi untuk meng-encode gambar menjadi base64 (jika diperlukan untuk background)
@st.cache_data
def get_image_as_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# --- CSS & STYLING MODERN ---
def load_custom_styling():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables - Color System (Sesuai Pilihan Anda) */
    :root {
        --primary-gold: #D4AF37;
        --primary-brown: #8B4513;
        --secondary-cream: #F5F5DC;
        --text-dark: #2C1810;
        --text-medium: #5D4E37;
        --text-light: #F5F5F5; /* Teks terang untuk sidebar gelap */
        --accent-orange: #CD853F;
        --bg-paper: #FEFDF8;
        --bg-parchment: #F7F3E9;
        --shadow-soft: 0 4px 12px rgba(139, 69, 19, 0.08);
        --shadow-medium: 0 8px 24px rgba(139, 69, 19, 0.12);
        --border-light: rgba(139, 69, 19, 0.1);
        --font-serif: 'Playfair Display', serif;
        --font-sans: 'Inter', sans-serif;
        --transition-smooth: all 0.3s ease;
    }

    /* Global Reset & Base Styles */
    .stApp {
        background-color: var(--bg-paper);
    }
    #MainMenu, footer, header, .stDeployButton, .stDecoration { visibility: hidden; }

    /* Main Container */
    .main .block-container {
        padding: 2rem;
        max-width: 1400px;
    }

    /* === PERBAIKAN NAVBAR (Permintaan #2) === */
    [data-testid="stSidebar"] {
        background-color: var(--primary-brown);
    }
    [data-testid="stSidebar"] h2 {
        color: var(--primary-gold) !important;
        font-family: var(--font-serif);
        text-align: center;
    }
    [data-testid="stSidebar"] .stRadio > div {
        gap: 8px; /* Jarak antar item nav */
    }
    [data-testid="stSidebar"] .stRadio label {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        border-radius: 8px;
        transition: var(--transition-smooth);
        cursor: pointer;
        font-weight: 500;
        color: var(--text-light) !important;
        border-left: 4px solid transparent; /* Border non-aktif */
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.08);
    }
    [data-testid="stSidebar"] .stRadio > div > div:has(input:checked) label {
        background-color: rgba(0,0,0, 0.2);
        border-left: 4px solid var(--primary-gold); /* Border aktif */
        color: var(--primary-gold) !important;
        font-weight: 700;
    }
    [data-testid="stSidebar"] .stRadio input { display: none; }
    [data-testid="stSidebar"] .stImage { border-radius: 12px; overflow: hidden; }

    h1 {
        font-family: var(--font-serif);
        font-size: 2.5rem; color: var(--primary-brown);
        text-align: center; margin-bottom: 2rem;
    }
    h2, h3 { font-family: var(--font-serif); color: var(--primary-brown); }

    /* === PERBAIKAN KONTAINER (Permintaan #3 & #4) === */
    .results-container {
        background: var(--bg-parchment);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 2rem;
        height: 75vh;
        overflow-y: auto;
        box-shadow: var(--shadow-soft);
    }
    .result-item { padding-bottom: 1.5rem; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-light); }
    .result-item:last-child { border-bottom: none; margin-bottom: 0; }
    .latin-text { font-family: var(--font-serif); font-style: italic; font-size: 1.2rem; color: var(--text-dark); margin-bottom: 0.5rem; }
    .translation-text { font-family: var(--font-sans); color: var(--text-medium); }
    .translation-text strong { color: var(--primary-brown); font-weight: 600; }
    .search-highlight { background-color: #FFF3CD; padding: 2px 6px; border-radius: 4px; }
    
    /* Manuscript Image Styling */
    .manuscript-image-container {
        border: 1px solid var(--border-light);
        border-radius: 12px; padding: 1rem;
        box-shadow: var(--shadow-medium);
    }
    .manuscript-image-container img { width: 100%; border-radius: 8px; }

    /* Pagination Styling */
    .page-indicator { text-align: center; margin-top: 0.5rem; font-weight: 600; }
    
    /* === PERBAIKAN HALAMAN TENTANG (Permintaan #5) === */
    .about-content { background-color: var(--bg-parchment); padding: 2rem; border-radius: 12px; }
    .about-content ul { list-style: none; padding-left: 0; }
    .about-content li { position: relative; padding-left: 2rem; margin-bottom: 0.75rem; }
    .about-content li::before { content: '📜'; position: absolute; left: 0; }
    
    </style>
    """, unsafe_allow_html=True)


# --- PEMUATAN DATA (DATA LOADING & CACHING) ---
@st.cache_data
def load_rdf_data(ttl_file="naskah_bhakti_final.ttl"):
    if not os.path.exists(ttl_file):
        st.error(f"Berkas data '{ttl_file}' tidak ditemukan.")
        return None
    try:
        g = Graph()
        g.parse(ttl_file, format="turtle")
        query = "PREFIX jawa: <http://example.org/jawa#> SELECT ?s ?latin ?terjemahan WHERE { ?s a jawa:Kalimat; jawa:latin ?latin; jawa:terjemahan ?terjemahan .} ORDER BY ?s"
        results = g.query(query)
        data = [{"latin": str(r.latin), "terjemahan": str(r.terjemahan)} for r in results]
        return data
    except Exception as e:
        st.error(f"Gagal memuat data RDF: {e}")
        return None

# --- FUNGSI TAMPILAN ---
def render_content_items(items_data, search_query=""):
    # Membangun string HTML di dalam Python
    html_content = ""
    if not items_data:
        html_content = "<p>Tidak ada data yang cocok untuk ditampilkan.</p>"
    else:
        highlight_class = "search-highlight"
        for item in items_data:
            latin_display = item['latin']
            terjemahan_display = item['terjemahan']
            
            if search_query:
                # Menggunakan string replace sederhana untuk highlight
                latin_display = latin_display.replace(search_query, f"<span class='{highlight_class}'>{search_query}</span>")
                terjemahan_display = terjemahan_display.replace(search_query, f"<span class='{highlight_class}'>{search_query}</span>")
            
            html_content += f"""
            <div class="result-item">
                <div class="latin-text">{latin_display}</div>
                <div class="translation-text"><strong>Terjemahan:</strong> {terjemahan_display}</div>
            </div>
            """
    # Menampilkan semua konten dalam satu kontainer dengan satu panggilan st.markdown
    st.markdown(f'<div class="results-container">{html_content}</div>', unsafe_allow_html=True)


def render_about_page():
    st.markdown("""
    <div class="about-content">
        <h2>Sejarah Naskah</h2>
        <p><strong>Kakawin Ramayana</strong> adalah salah satu karya sastra Jawa Kuno yang paling penting, diperkirakan ditulis pada abad ke-9 atau ke-10 Masehi.</p>
        
        <h3>Karakteristik Utama</h3>
        <ul>
            <li><strong>Bahasa:</strong> Jawa Kuno (Kawi)</li>
            <li><strong>Bentuk:</strong> Puisi Kakawin (memiliki aturan metrum yang ketat)</li>
            <li><strong>Isi:</strong> Mengisahkan perjalanan hidup Sang Rama dengan nuansa filosofis Hindu-Jawa yang kental.</li>
        </ul>

        <h2>Tentang Proyek Digitalisasi</h2>
        <p>Proyek ini bertujuan untuk melestarikan warisan budaya ini dan membuatnya lebih mudah diakses oleh para peneliti, mahasiswa, serta masyarakat umum.</p>
    </div>
    """, unsafe_allow_html=True) # Menambahkan unsafe_allow_html=True

# --- APLIKASI UTAMA ---
def main():
    load_custom_styling()
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg/400px-Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg", use_container_width=True)
        st.markdown("<h2>Kakawin Ramayana</h2>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("Navigasi", ["📖 Transliterasi", "🔍 Pencarian", "ℹ️ Tentang Naskah"], key="main_nav")
        st.markdown("---")

    rdf_data = load_rdf_data()
    if rdf_data is None:
        st.stop()

    # Konten Halaman
    if page == "📖 Transliterasi":
        st.markdown("<h1>Transliterasi & Terjemahan</h1>", unsafe_allow_html=True)
        
        # Mengubah rasio kolom agar gambar lebih dominan dan stabil ukurannya
        col1, col2 = st.columns([6, 5], gap="large")
        
        with col1:
            if 'page_num' not in st.session_state:
                st.session_state.page_num = 1
            
            st.subheader(f"Halaman Naskah {st.session_state.page_num}")
            
            image_path = f"images/page_{st.session_state.page_num}.png"
            if os.path.exists(image_path):
                st.markdown('<div class="manuscript-image-container">', unsafe_allow_html=True)
                st.image(image_path, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Gambar tidak tersedia.")

            TOTAL_PAGES = 20
            c1, c2, c3 = st.columns([2, 1, 2])
            if c1.button("← Sebelumnya", use_container_width=True, disabled=(st.session_state.page_num == 1)):
                st.session_state.page_num -= 1; st.rerun()
            c2.markdown(f"<div class='page-indicator'>{st.session_state.page_num}/{TOTAL_PAGES}</div>", unsafe_allow_html=True)
            if c3.button("Selanjutnya →", use_container_width=True, disabled=(st.session_state.page_num == TOTAL_PAGES)):
                st.session_state.page_num += 1; st.rerun()

        with col2:
            st.subheader("Teks & Terjemahan")
            if st.session_state.page_num == 3:
                render_content_items(rdf_data)
            else:
                st.info(f"Data transliterasi untuk halaman {st.session_state.page_num} belum tersedia.")

    elif page == "🔍 Pencarian":
        st.markdown("<h1>Pencarian Teks</h1>", unsafe_allow_html=True)
        search_query = st.text_input("Cari dalam naskah:", placeholder="Cari dalam teks Latin atau terjemahan...")
        
        if search_query:
            results = [item for item in rdf_data if search_query.lower() in item['latin'].lower() or search_query.lower() in item['terjemahan'].lower()]
            render_content_items(results, search_query)
        else:
            st.info("Masukkan kata kunci untuk memulai pencarian.")

    elif page == "ℹ️ Tentang Naskah":
        st.markdown("<h1>Tentang Naskah</h1>", unsafe_allow_html=True)
        render_about_page()

if __name__ == "__main__":
    main()