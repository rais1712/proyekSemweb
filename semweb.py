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
# Fungsi untuk meng-encode gambar menjadi base64
def get_image_as_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# --- CSS & STYLING MODERN ---
# Didesain ulang sepenuhnya berdasarkan requirements Anda
def load_custom_styling():
    
    # Mengambil gambar background dan mengubahnya menjadi base64 untuk CSS
    bg_image_base64 = get_image_as_base64('images/paper_texture.png')
    if bg_image_base64:
        bg_image_style = f"background-image: linear-gradient(rgba(254, 253, 248, 0.92), rgba(254, 253, 248, 0.92)), url(data:image/png;base64,{bg_image_base64});"
    else:
        bg_image_style = "background-color: var(--bg-paper);" # Fallback jika gambar tidak ada

    st.markdown(f"""
    <style>
    /* Step 1 & 2: Color System, Variables & Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

    :root {{
        --primary-gold: #BFA15A;
        --primary-brown: #5D4037;
        --secondary-cream: #FDF5E6;
        --text-dark: #3E2723;
        --text-light: #F5F5F5;
        --accent-orange: #AF642D;
        --bg-paper: #FEFDF8;
        --shadow-soft: 0 4px 12px rgba(44, 24, 16, 0.08);
        --shadow-medium: 0 8px 24px rgba(44, 24, 16, 0.12);
        --border-color: rgba(93, 64, 55, 0.2);
        --spacing-unit: 8px;
        --font-serif: 'Crimson Pro', serif;
        --font-sans: 'Inter', sans-serif;
        --transition-smooth: all 0.3s ease-in-out;
    }}

    /* Global Reset & Font Setup */
    .stApp {{
        {bg_image_style}
        background-attachment: fixed;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: var(--font-serif);
        color: var(--primary-brown);
    }}

    p, div, span, label, input, button, ::-webkit-scrollbar-thumb {{
        font-family: var(--font-sans);
        color: var(--text-dark);
    }}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(93, 64, 55, 0.3); border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--primary-brown); }}

    /* Step 3: Layout Components */
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: var(--primary-brown);
        padding: calc(var(--spacing-unit) * 2);
    }}
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {{
        color: var(--secondary-cream) !important;
    }}
    [data-testid="stSidebar"] .stRadio > div {{
        gap: var(--spacing-unit);
    }}
    [data-testid="stSidebar"] .stRadio label {{
        display: flex;
        align-items: center;
        padding: calc(var(--spacing-unit) * 1.5) calc(var(--spacing-unit) * 2);
        border-radius: var(--spacing-unit);
        transition: var(--transition-smooth);
        cursor: pointer;
        font-weight: 500;
        color: var(--text-light) !important;
        border-left: 4px solid transparent;
    }}
    [data-testid="stSidebar"] .stRadio label:hover {{
        background-color: rgba(255, 255, 255, 0.08);
        border-left: 4px solid var(--primary-gold);
    }}
    [data-testid="stSidebar"] .stRadio > div > div:has(input:checked) label {{
        background-color: rgba(0,0,0, 0.2);
        border-left: 4px solid var(--primary-gold);
        color: var(--primary-gold) !important;
        font-weight: 700;
    }}
    [data-testid="stSidebar"] .stRadio input {{
        display: none;
    }}

    /* Step 4 & 5: Interactive & Content-Specific Styling */
    /* Page Header */
    .page-header {{
        padding-bottom: calc(var(--spacing-unit) * 2);
        border-bottom: 1px solid var(--border-color);
        margin-bottom: calc(var(--spacing-unit) * 4);
    }}
    .page-header p {{
        opacity: 0.8;
    }}

    /* Manuscript Image Container */
    .manuscript-image-container {{
        background: white;
        border: 1px solid var(--border-color);
        padding: var(--spacing-unit);
        border-radius: var(--spacing-unit);
        box-shadow: var(--shadow-soft);
        transition: var(--transition-smooth);
    }}
    .manuscript-image-container:hover {{
        box-shadow: var(--shadow-medium);
        transform: translateY(-4px);
    }}
    .manuscript-image-container img {{
        border-radius: calc(var(--spacing-unit) / 2);
    }}
    
    /* Search Box */
    .search-container div[data-baseweb="input"] > div {{
        border-radius: var(--spacing-unit);
        border-color: var(--border-color);
        transition: var(--transition-smooth);
    }}
    .search-container div[data-baseweb="input"] > div:focus-within {{
        border-color: var(--primary-gold);
        box-shadow: 0 0 0 3px rgba(191, 161, 90, 0.3);
    }}
    
    /* Transliteration & Search Result Container */
    .results-container {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(2px);
        border: 1px solid var(--border-color);
        border-radius: var(--spacing-unit);
        padding: calc(var(--spacing-unit) * 2);
        height: 75vh;
        overflow-y: auto;
    }}
    .result-item {{
        padding: calc(var(--spacing-unit) * 2) 0;
        border-bottom: 1px solid var(--border-color);
    }}
    .result-item:last-child {{ border-bottom: none; }}
    .latin-text {{
        font-family: var(--font-serif);
        font-style: italic;
        font-size: 1.15rem;
        margin-bottom: var(--spacing-unit);
        color: var(--primary-brown);
    }}
    .highlight {{
        background-color: rgba(191, 161, 90, 0.3);
        padding: 0 4px;
        border-radius: 3px;
    }}

    /* Pagination */
    .pagination-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: calc(var(--spacing-unit) * 2);
    }}
    .pagination-container .stButton > button {{
        background-color: white;
        color: var(--primary-brown);
        border: 1px solid var(--border-color);
        border-radius: var(--spacing-unit);
        transition: var(--transition-smooth);
        font-weight: 500;
    }}
    .pagination-container .stButton > button:hover {{
        border-color: var(--primary-gold);
        background-color: var(--bg-paper);
        color: var(--primary-brown);
    }}
    .pagination-container .stButton > button:disabled {{
        background-color: #f0f2f6;
        color: #ababab;
        border-color: var(--border-color);
        cursor: not-allowed;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        [data-testid="stSidebar"] {{
            padding: var(--spacing-unit);
        }}
    }}
    </style>
    """, unsafe_allow_html=True)


# --- FUNGSI PEMUATAN DATA (DATA LOADING & CACHING) ---
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
        return data
    except Exception as e:
        st.error(f"Gagal memuat data RDF: {e}")
        return None

# --- FUNGSI TAMPILAN (UI RENDER FUNCTIONS) ---
def render_content_items(items_data, search_query=""):
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    if not items_data:
        st.info("Tidak ada data yang cocok untuk ditampilkan.")
    else:
        highlight_style = "background-color: rgba(191, 161, 90, 0.3); padding: 0 4px; border-radius: 3px;"
        for item in items_data:
            latin_display = item['latin']
            terjemahan_display = item['terjemahan']
            
            if search_query:
                latin_display = latin_display.replace(search_query, f"<span style='{highlight_style}'>{search_query}</span>")
                terjemahan_display = terjemahan_display.replace(search_query, f"<span style='{highlight_style}'>{search_query}</span>")
                
            st.markdown(f"""
            <div class="result-item">
                <div class="latin-text">{latin_display}</div>
                <div class="translation-text"><strong>Terjemahan:</strong> {terjemahan_display}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- APLIKASI UTAMA ---
def main():
    load_custom_styling()
    
    # --- Sidebar ---
    with st.sidebar:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg/400px-Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg",
            use_container_width=True
        )
        st.markdown("## 📜 Kakawin Ramayana")
        st.markdown("---")
        
        page = st.radio(
            "Navigasi",
            ["📖 Transliterasi", "🔍 Pencarian", "ℹ️ Tentang Naskah"],
            key="main_nav"
        )
        st.markdown("---")
        st.info("Aplikasi digitalisasi dan eksplorasi naskah kuno.")

    # --- Memuat Data ---
    rdf_data = load_rdf_data()
    if rdf_data is None:
        st.stop()

    # --- Konten Halaman ---
    if page == "📖 Transliterasi":
        st.markdown('<div class="page-header"><h1>Transliterasi & Terjemahan</h1><p>Eksplorasi naskah Kakawin Ramayana halaman per halaman.</p></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([5, 6], gap="large")
        
        with col1:
            if 'page_num' not in st.session_state:
                st.session_state.page_num = 1
            
            TOTAL_PAGES = 20
            st.subheader(f"Tampilan Naskah Halaman {st.session_state.page_num}")

            image_path = f"images/page_{st.session_state.page_num}.png"
            if os.path.exists(image_path):
                st.markdown('<div class="manuscript-image-container">', unsafe_allow_html=True)
                st.image(image_path, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Gambar tidak tersedia.")
            
            st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1,1,1])
            if c1.button("← Sebelumnya", use_container_width=True, disabled=(st.session_state.page_num == 1)):
                st.session_state.page_num -= 1
                st.rerun()
            c2.markdown(f"<div style='text-align: center; margin-top: 0.5rem;'>{st.session_state.page_num} / {TOTAL_PAGES}</div>", unsafe_allow_html=True)
            if c3.button("Selanjutnya →", use_container_width=True, disabled=(st.session_state.page_num == TOTAL_PAGES)):
                st.session_state.page_num += 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.subheader("Teks & Terjemahan")
            if st.session_state.page_num == 3:
                render_content_items(rdf_data)
            else:
                st.markdown('<div class="results-container">', unsafe_allow_html=True)
                st.info(f"Data transliterasi untuk halaman {st.session_state.page_num} belum tersedia. Silakan pilih Halaman 3 untuk melihat data yang ada.")
                st.markdown('</div>', unsafe_allow_html=True)

    elif page == "🔍 Pencarian":
        st.markdown('<div class="page-header"><h1>Pencarian Teks</h1><p>Cari kata kunci dalam transliterasi Latin atau terjemahan Indonesia.</p></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        search_query = st.text_input("Cari dalam naskah:", placeholder="Contoh: bhakti, panah, ...", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if search_query:
            query_lower = search_query.lower()
            results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
            render_content_items(results, search_query)
        else:
            st.info("Silakan masukkan kata kunci untuk memulai pencarian.")

    elif page == "ℹ️ Tentang Naskah":
        st.markdown('<div class="page-header"><h1>Tentang Naskah Kakawin Ramayana</h1></div>', unsafe_allow_html=True)
        st.markdown("""
        **Kakawin Ramayana** adalah salah satu karya sastra Jawa Kuno yang paling agung, diperkirakan ditulis pada abad ke-9 atau ke-10 Masehi pada masa Kerajaan Medang (Mataram Kuno). Karya ini merupakan adaptasi mahakarya Ramayana dari India, namun telah diresapi secara mendalam dengan kearifan lokal, filosofi, dan budaya Jawa.

        ### Ciri Khas
        - **Bahasa:** Ditulis dalam bahasa Jawa Kuno (Kawi), bahasa sastra yang kaya dan kompleks.
        - **Bentuk:** Disusun dalam bentuk puisi *kakawin*, yang terikat oleh aturan metrum (guru-laghu) yang ketat, menunjukkan tingkat keahlian sastra yang tinggi.
        - **Isi:** Meskipun alur utamanya mengikuti kisah Sang Rama, Sita, dan Hanuman, banyak bagian yang diperkaya dengan ajaran moral, etika kepemimpinan, dan perenungan filosofis yang khas Hindu-Jawa.

        ### Proyek Digitalisasi
        Proyek ini merupakan upaya untuk melestarikan warisan budaya takbenda ini dalam format digital. Tujuannya adalah untuk membuat naskah ini dapat diakses dengan lebih mudah oleh para peneliti, akademisi, mahasiswa, dan masyarakat umum yang tertarik pada kekayaan sastra Nusantara.
        """)

if __name__ == "__main__":
    main()