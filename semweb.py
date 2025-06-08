import streamlit as st
import os
from rdflib import Graph

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Naskah Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ENHANCED CSS STYLING ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables - Color System */
    :root {
        --primary-gold: #D4AF37;
        --primary-brown: #8B4513;
        --secondary-cream: #F5F5DC;
        --text-dark: #2C1810;
        --text-medium: #5D4E37;
        --text-light: #8B7355;
        --accent-orange: #CD853F;
        --bg-paper: #FEFDF8;
        --bg-parchment: #F7F3E9;
        --shadow-soft: 0 4px 12px rgba(139, 69, 19, 0.08);
        --shadow-medium: 0 8px 24px rgba(139, 69, 19, 0.12);
        --shadow-strong: 0 16px 48px rgba(139, 69, 19, 0.16);
        --border-light: rgba(139, 69, 19, 0.1);
        --border-medium: rgba(139, 69, 19, 0.2);
        --gradient-primary: linear-gradient(135deg, var(--bg-paper) 0%, var(--bg-parchment) 100%);
        --gradient-gold: linear-gradient(135deg, #FFD700 0%, var(--primary-gold) 100%);
    }

    /* Global Reset & Base Styles */
    .stApp {
        background: var(--gradient-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stDeployButton {display: none;}
    .stDecoration {display: none;}

    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Custom Main Container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }

    /* Enhanced Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2C1810 0%, #1A0F08 100%);
        border-right: 2px solid var(--primary-gold);
    }

    .css-1d391kg .css-17eq0hr {
        color: var(--secondary-cream);
    }

    /* Sidebar Title */
    .css-1d391kg h2 {
        color: var(--primary-gold) !important;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    /* Sidebar Navigation */
    .css-1d391kg .stRadio > div {
        background: rgba(212, 175, 55, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .css-1d391kg .stRadio label {
        color: var(--secondary-cream) !important;
        font-weight: 500;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        display: block;
        margin-bottom: 0.5rem;
    }

    .css-1d391kg .stRadio label:hover {
        background: rgba(212, 175, 55, 0.2);
        transform: translateX(4px);
    }

    /* Sidebar Image Container */
    .css-1d391kg .stImage {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-medium);
        margin-top: 2rem;
    }

    /* Typography Hierarchy */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--text-dark);
        font-weight: 600;
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        background: var(--gradient-gold);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
    }

    h2 {
        font-size: 2rem;
        margin-bottom: 1.25rem;
        color: var(--primary-brown);
        border-bottom: 2px solid var(--primary-gold);
        padding-bottom: 0.5rem;
    }

    h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: var(--text-dark);
    }

    /* Enhanced Transliterasi Container */
    .transliterasi-container {
        background: var(--bg-paper);
        border: 2px solid var(--border-light);
        border-radius: 16px;
        padding: 2rem;
        height: 70vh;
        overflow-y: auto;
        box-shadow: var(--shadow-medium);
        position: relative;
    }

    .transliterasi-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(139, 69, 19, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(212, 175, 55, 0.03) 0%, transparent 50%);
        pointer-events: none;
        border-radius: 16px;
    }

    /* Custom Scrollbar */
    .transliterasi-container::-webkit-scrollbar {
        width: 8px;
    }

    .transliterasi-container::-webkit-scrollbar-track {
        background: var(--bg-parchment);
        border-radius: 10px;
    }

    .transliterasi-container::-webkit-scrollbar-thumb {
        background: var(--primary-gold);
        border-radius: 10px;
        transition: background 0.3s ease;
    }

    .transliterasi-container::-webkit-scrollbar-thumb:hover {
        background: var(--accent-orange);
    }

    /* Transliterasi Items */
    .transliterasi-item {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }

    .transliterasi-item:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        border-color: var(--primary-gold);
    }

    .transliterasi-item:last-child {
        margin-bottom: 0;
    }

    .transliterasi-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--gradient-gold);
        border-radius: 2px 0 0 2px;
    }

    /* Text Styling */
    .latin-text {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 1.25rem;
        color: var(--text-dark);
        margin-bottom: 1rem;
        line-height: 1.6;
        font-weight: 500;
    }

    .translation-text {
        font-family: 'Inter', sans-serif;
        color: var(--text-medium);
        font-size: 1rem;
        line-height: 1.7;
        font-weight: 400;
    }

    .translation-text strong {
        color: var(--primary-brown);
        font-weight: 600;
    }

    /* Manuscript Image Container */
    .manuscript-image-container {
        background: var(--bg-paper);
        border: 2px solid var(--border-light);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: var(--shadow-medium);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .manuscript-image-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--gradient-gold);
        border-radius: 18px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .manuscript-image-container:hover::before {
        opacity: 1;
    }

    .manuscript-image-container:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-strong);
    }

    .manuscript-image-container img {
        width: 100%;
        border-radius: 8px;
        transition: transform 0.3s ease;
    }

    .manuscript-image-container:hover img {
        transform: scale(1.02);
    }

    /* Enhanced Button Styling */
    .stButton > button {
        background: var(--gradient-gold);
        color: var(--text-dark);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-soft);
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    .stButton > button:disabled {
        background: var(--border-light);
        color: var(--text-light);
        cursor: not-allowed;
        transform: none;
    }

    /* Enhanced Input Styling */
    .stTextInput input {
        background: var(--bg-paper);
        border: 2px solid var(--border-light);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-family: 'Inter', sans-serif;
        color: var(--text-dark);
        transition: all 0.3s ease;
        box-shadow: var(--shadow-soft);
    }

    .stTextInput input:focus {
        border-color: var(--primary-gold);
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
        outline: none;
    }

    .stTextInput input::placeholder {
        color: var(--text-light);
        font-style: italic;
    }

    /* Search Results Highlighting */
    .search-highlight {
        background: linear-gradient(120deg, #FFF3CD 0%, #FFEAA7 100%);
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        color: var(--primary-brown);
    }

    /* Success/Info/Warning Messages */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 12px;
        border: none;
        padding: 1rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }

    .stSuccess {
        background: linear-gradient(135deg, #D4F1D4 0%, #A8E6A8 100%);
        color: #2E7D2E;
    }

    .stInfo {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        color: #1565C0;
    }

    .stWarning {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        color: #E65100;
    }

    /* Navigation Indicators */
    .page-indicator {
        text-align: center;
        margin-top: 0.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--primary-brown);
        background: var(--bg-paper);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 2px solid var(--primary-gold);
        display: inline-block;
    }

    /* Columns Gap Enhancement */
    .element-container .stColumn {
        background: transparent;
    }

    /* About Page Content */
    .about-content {
        background: var(--bg-paper);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: var(--shadow-medium);
        border: 1px solid var(--border-light);
    }

    .about-content h3 {
        color: var(--primary-brown);
        border-left: 4px solid var(--primary-gold);
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
    }

    .about-content ul {
        list-style: none;
        padding-left: 0;
    }

    .about-content li {
        position: relative;
        padding-left: 2rem;
        margin-bottom: 0.75rem;
        color: var(--text-medium);
    }

    .about-content li::before {
        content: '◆';
        position: absolute;
        left: 0;
        color: var(--primary-gold);
        font-size: 0.8rem;
        top: 0.2rem;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main-container {
            padding: 0 0.5rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .transliterasi-container {
            height: 60vh;
            padding: 1rem;
        }
        
        .transliterasi-item {
            padding: 1rem;
        }
        
        .manuscript-image-container {
            padding: 1rem;
        }
        
        .latin-text {
            font-size: 1.1rem;
        }
    }

    /* Animation Keyframes */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Apply Animations */
    .transliterasi-item {
        animation: fadeInUp 0.6s ease forwards;
    }

    .manuscript-image-container {
        animation: slideInLeft 0.8s ease forwards;
    }

    /* Loading States */
    .loading-shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }

    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- PEMUATAN DATA (DATA LOADING & CACHING) ---
@st.cache_data
def load_rdf_data(ttl_file="naskah_bhakti_final.ttl"):
    """Memuat dan mem-parsing file TTL dengan penanganan error yang lebih baik."""
    if not os.path.exists(ttl_file):
        st.error(f"Berkas data '{ttl_file}' tidak ditemukan di direktori proyek.")
        return None
    
    try:
        g = Graph()
        g.parse(ttl_file, format="turtle")
        
        query = """
        PREFIX jawa: <http://example.org/jawa#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?kalimat_uri ?latin ?terjemahan WHERE {
            ?kalimat_uri a jawa:Kalimat ;
                         jawa:latin ?latin ;
                         jawa:terjemahan ?terjemahan .
        }
        ORDER BY ?kalimat_uri
        """
        
        results = g.query(query)
        data = []
        for r in results:
            data.append({
                "uri": str(r.kalimat_uri),
                "latin": str(r.latin),
                "terjemahan": str(r.terjemahan)
            })
            
        if not data:
            st.warning("Tidak ada data transliterasi yang berhasil dimuat dari file TTL.")
            return []
            
        return data
        
    except Exception as e:
        st.error(f"Gagal memuat atau mem-parsing data RDF: {str(e)}")
        return None

# --- FUNGSI BANTUAN TAMPILAN (UI HELPER FUNCTIONS) ---
def render_transliterasi_content(data):
    """Menampilkan konten transliterasi di dalam kontainer yang bisa di-scroll."""
    if not data:
        st.info("Data transliterasi untuk halaman ini belum tersedia.")
        return
    
    st.markdown('<div class="transliterasi-container">', unsafe_allow_html=True)
    
    for item in data:
        st.markdown(f"""
        <div class="transliterasi-item">
            <div class="latin-text">{item['latin']}</div>
            <div class="translation-text"><strong>Terjemahan:</strong> {item['terjemahan']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_search_results(results, query):
    """Menampilkan hasil pencarian dengan format yang lebih baik."""
    if not results:
        st.info("Tidak ada hasil yang cocok ditemukan.")
        return
    
    st.success(f"Ditemukan {len(results)} hasil untuk '{query}'")
    
    st.markdown('<div class="transliterasi-container">', unsafe_allow_html=True)
    
    for item in results:
        latin_highlighted = item['latin'].replace(query, f"<span class='search-highlight'>{query}</span>")
        translation_highlighted = item['terjemahan'].replace(query, f"<span class='search-highlight'>{query}</span>")
        
        st.markdown(f"""
        <div class="transliterasi-item">
            <div class="latin-text">{latin_highlighted}</div>
            <div class="translation-text"><strong>Terjemahan:</strong> {translation_highlighted}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_about_page():
    st.markdown("""
    <div class="about-content">
        <h2>🏛️ Sejarah Naskah</h2>
        <p><strong>Kakawin Ramayana</strong> adalah salah satu karya sastra Jawa Kuno yang paling penting, diperkirakan ditulis pada abad ke-9 atau ke-10 Masehi. Naskah ini merupakan adaptasi dari epos Ramayana Sanskrit karya Valmiki, namun diresapi dengan nilai-nilai, budaya, dan bahasa lokal Jawa Kuno.</p>
        
        <h3>📚 Karakteristik Utama</h3>
        <ul>
            <li><strong>Bahasa:</strong> Jawa Kuno (Kawi)</li>
            <li><strong>Bentuk:</strong> Puisi Kakawin (memiliki aturan metrum yang ketat)</li>
            <li><strong>Periode:</strong> Kerajaan Medang (Mataram Kuno)</li>
            <li><strong>Isi:</strong> Mengisahkan perjalanan hidup Sang Rama dalam mencari dan menyelamatkan istrinya, Sita, dengan nuansa filosofis Hindu-Jawa yang kental</li>
        </ul>

        <h2>💻 Tentang Proyek Digitalisasi Ini</h2>
        <p>Proyek ini bertujuan untuk melestarikan warisan budaya takbenda ini dan membuatnya lebih mudah diakses oleh para peneliti, mahasiswa, serta masyarakat umum melalui teknologi digital.</p>
        
        <h3>🛠️ Teknologi yang Digunakan</h3>
        <ul>
            <li><strong>RDF (Resource Description Framework):</strong> Data naskah distrukturkan secara semantik menggunakan format Turtle (.ttl) untuk mendefinisikan hubungan antar entitas seperti cerita, kalimat, dan terjemahan</li>
            <li><strong>Streamlit:</strong> Kerangka kerja Python yang digunakan untuk membangun antarmuka web interaktif ini dengan cepat</li>
            <li><strong>Python:</strong> Bahasa pemrograman utama yang digunakan untuk memproses data RDF dan menjalankan aplikasi</li>
        </ul>
        
        <h3>🎯 Fitur Utama</h3>
        <ul>
            <li><strong>Navigasi Interaktif:</strong> Jelajahi halaman-halaman naskah dengan mudah</li>
            <li><strong>Pencarian Semantik:</strong> Cari teks dalam bahasa Latin dan terjemahan Indonesia</li>
            <li><strong>Tampilan Responsif:</strong> Optimal di berbagai perangkat dan ukuran layar</li>
            <li><strong>Desain Otentik:</strong> Tema visual yang menghormati karakteristik naskah kuno</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE ---
if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# --- APLIKASI UTAMA (MAIN APPLICATION) ---
def main():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("## 📜 Kakawin Ramayana")
        st.markdown("---")
        
        page = st.radio(
            "Navigasi",
            ["📖 Transliterasi", "🔍 Pencarian", "ℹ️ Tentang Naskah"],
            key="main_nav"
        )
        
        st.markdown("---")
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg/400px-Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg",
            caption="Ilustrasi Sang Rama",
            use_container_width=True
        )

    # --- Konten Halaman ---
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    rdf_data = load_rdf_data()
    if rdf_data is None:
        st.stop()

    # --- Routing Halaman ---
    if page == "📖 Transliterasi":
        st.markdown("<h1>📜 Transliterasi & Terjemahan Naskah</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.subheader(f"Halaman Naskah {st.session_state.page_num}")
            
            image_path = f"images/page_{st.session_state.page_num}.png"
            if os.path.exists(image_path):
                st.markdown('<div class="manuscript-image-container">', unsafe_allow_html=True)
                st.image(image_path, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(f"Gambar untuk halaman {st.session_state.page_num} tidak tersedia.")

            TOTAL_PAGES = 20
            nav_cols = st.columns([2, 1, 2])
            if nav_cols[0].button("← Sebelumnya", use_container_width=True, disabled=(st.session_state.page_num == 1)):
                st.session_state.page_num -= 1
                st.rerun()
            
            nav_cols[1].markdown(f"<div class='page-indicator'>{st.session_state.page_num}/{TOTAL_PAGES}</div>", unsafe_allow_html=True)
            
            if nav_cols[2].button("Selanjutnya →", use_container_width=True, disabled=(st.session_state.page_num == TOTAL_PAGES)):
                st.session_state.page_num += 1
                st.rerun()

        with col2:
            st.subheader("Teks & Terjemahan")
            if st.session_state.page_num == 3:
                render_transliterasi_content(rdf_data)
            else:
                st.info(f"Data transliterasi untuk halaman {st.session_state.page_num} belum tersedia.")
                st.markdown("""
                **Catatan:** Proyek digitalisasi naskah ini sedang berlangsung. Saat ini, data RDF yang tersedia hanya untuk **halaman 3**.
                """)

    elif page == "🔍 Pencarian":
        st.markdown("<h1>🔍 Pencarian Teks</h1>", unsafe_allow_html=True)
        
        search_query = st.text_input(
            "Cari dalam naskah:",
            placeholder="Masukkan kata kunci dalam teks Latin atau terjemahan..."
        )
        
        if search_query:
            query_lower = search_query.lower()
            results = [
                item for item in rdf_data 
                if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()
            ]
            render_search_results(results, search_query)
        else:
            st.info("Masukkan kata kunci di atas untuk memulai pencarian di dalam data yang tersedia.")

    elif page == "ℹ️ Tentang Naskah":
        st.markdown("<h1>ℹ️ Tentang Naskah Kakawin Ramayana</h1>", unsafe_allow_html=True)
        render_about_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()