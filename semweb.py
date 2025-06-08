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

# --- CSS ARCHITECTURE & STYLING ---
st.markdown("""
<style>
    /* CSS Custom Properties untuk Theming yang Konsisten */
    :root {
        --primary-color: #8B4513;      /* Warm brown untuk budaya Jawa */
        --secondary-color: #2C3E50;    /* Dark blue-gray untuk text */
        --accent-color: #DAA520;       /* Golden accent */
        --bg-color: #FEFEFE;           /* Clean white background */
        --text-color: #2C3E50;         /* Primary text color */
        --text-muted: #6C757D;         /* Muted text */
        --border-color: #E9ECEF;       /* Light border */
        --hover-bg: #F8F9FA;          /* Subtle hover background */
        --font-family: 'Georgia', serif;
        --font-family-ui: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --line-height: 1.6;
        --border-radius: 8px;
        --spacing-xs: 4px;
        --spacing-sm: 8px;
        --spacing-md: 16px;
        --spacing-lg: 24px;
        --spacing-xl: 32px;
    }

    /* Reset dan Base Styles */
    .stApp {
        background-color: var(--bg-color);
        font-family: var(--font-family-ui);
    }

    /* Typography Hierarchy */
    h1 {
        color: var(--primary-color);
        font-family: var(--font-family);
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: var(--spacing-lg);
    }

    h2 {
        color: var(--secondary-color);
        font-family: var(--font-family);
        font-size: 1.75rem;
        font-weight: 600;
        line-height: 1.3;
        margin-bottom: var(--spacing-md);
    }

    h3 {
        color: var(--secondary-color);
        font-family: var(--font-family);
        font-size: 1.25rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: var(--spacing-sm);
    }

    p, li, label {
        color: var(--text-color);
        font-family: var(--font-family-ui);
        font-size: 1rem;
        line-height: var(--line-height);
    }

    /* Layout Container */
    .block-container {
        padding: var(--spacing-lg) var(--spacing-xl);
        max-width: 1200px;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: var(--spacing-xs);
    }

    [data-testid="stSidebar"] .stRadio label {
        display: flex;
        align-items: center;
        padding: var(--spacing-md) var(--spacing-lg);
        border-radius: var(--border-radius);
        margin: var(--spacing-xs) 0;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
        cursor: pointer;
        font-family: var(--font-family-ui);
        font-weight: 500;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: var(--hover-bg);
        border-left-color: var(--accent-color);
    }

    [data-testid="stSidebar"] .stRadio > div > div:has(input:checked) label {
        background-color: rgba(139, 69, 19, 0.1);
        border-left-color: var(--primary-color);
        color: var(--primary-color);
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stRadio input {
        display: none;
    }

    /* Content Cards */
    .content-card {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-lg);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .content-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: box-shadow 0.2s ease;
    }

    /* Transliterasi Styles */
    .transliterasi-item {
        padding: var(--spacing-lg);
        border-bottom: 1px solid var(--border-color);
        margin-bottom: var(--spacing-lg);
    }

    .transliterasi-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }

    .latin-text {
        font-family: var(--font-family);
        font-style: italic;
        font-size: 1.1rem;
        color: var(--secondary-color);
        margin-bottom: var(--spacing-sm);
        line-height: 1.5;
    }

    .translation-text {
        font-family: var(--font-family-ui);
        color: var(--text-color);
        font-size: 1rem;
        line-height: var(--line-height);
    }

    /* Search Results */
    .search-result {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: var(--spacing-lg);
        margin-bottom: var(--spacing-md);
        transition: all 0.2s ease;
    }

    .search-result:hover {
        border-color: var(--accent-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    .highlight {
        background-color: rgba(218, 165, 32, 0.3);
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: 600;
    }

    /* Navigation Controls */
    .nav-controls {
        display: flex;
        align-items: center;
        gap: var(--spacing-md);
        padding: var(--spacing-md) 0;
        border-top: 1px solid var(--border-color);
        margin-top: var(--spacing-lg);
    }

    .page-indicator {
        font-weight: 600;
        color: var(--secondary-color);
        font-size: 0.9rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        font-family: var(--font-family-ui);
        font-weight: 500;
        transition: all 0.2s ease;
        min-height: 44px; /* Touch-friendly */
    }

    .stButton > button:hover {
        border-color: var(--primary-color);
        color: var(--primary-color);
    }

    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: var(--border-radius);
        border: 1px solid var(--border-color);
        font-family: var(--font-family-ui);
        font-size: 1rem;
        padding: var(--spacing-md);
        min-height: 44px;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(139, 69, 19, 0.1);
    }

    /* Loading States */
    .loading-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--spacing-xl);
        color: var(--text-muted);
    }

    /* Image Container */
    .image-container {
        position: sticky;
        top: var(--spacing-lg);
        background: white;
        border-radius: var(--border-radius);
        overflow: hidden;
        border: 1px solid var(--border-color);
    }

    .image-container img {
        width: 100%;
        height: auto;
        display: block;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .block-container {
            padding: var(--spacing-md);
        }

        h1 {
            font-size: 2rem;
        }

        h2 {
            font-size: 1.5rem;
        }

        .nav-controls {
            flex-direction: column;
            gap: var(--spacing-sm);
        }

        .content-card {
            padding: var(--spacing-md);
        }

        .transliterasi-item {
            padding: var(--spacing-md);
        }

        [data-testid="stSidebar"] .stRadio label {
            padding: var(--spacing-sm) var(--spacing-md);
        }
    }

    @media (max-width: 480px) {
        .block-container {
            padding: var(--spacing-sm);
        }

        h1 {
            font-size: 1.75rem;
        }

        .latin-text {
            font-size: 1rem;
        }
    }

    /* Accessibility Improvements */
    .stButton > button:focus,
    .stTextInput > div > div > input:focus {
        outline: 2px solid var(--primary-color);
        outline-offset: 2px;
    }

    /* Skip to content link for screen readers */
    .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary-color);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1000;
    }

    .skip-link:focus {
        top: 6px;
    }

    /* Print Styles */
    @media print {
        .stButton, .nav-controls, [data-testid="stSidebar"] {
            display: none !important;
        }
        
        .content-card {
            box-shadow: none;
            border: 1px solid #ccc;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING & CACHING ---
@st.cache_data
def load_rdf_data(ttl_file="naskah_bhakti_final.ttl"):
    """Memuat dan mem-parsing file TTL dengan error handling yang robust."""
    if not os.path.exists(ttl_file):
        st.error(f"📁 File data '{ttl_file}' tidak ditemukan.")
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
        
        return data
        
    except Exception as e:
        st.error(f"❌ Gagal memuat data: {str(e)}")
        return None

# --- UI HELPER FUNCTIONS ---
def render_navigation_controls(current_page, total_pages):
    """Render navigation controls yang responsive dan accessible."""
    
    st.markdown('<div class="nav-controls">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2, 3, 2, 3])
    
    with col1:
        if st.button("← Sebelumnya", 
                    disabled=(current_page == 1),
                    use_container_width=True,
                    key="prev_btn"):
            st.session_state.page_num = max(1, current_page - 1)
            st.rerun()
    
    with col2:
        st.markdown(f'<div class="page-indicator">Halaman {current_page} dari {total_pages}</div>', 
                   unsafe_allow_html=True)
    
    with col3:
        if st.button("Selanjutnya →", 
                    disabled=(current_page == total_pages),
                    use_container_width=True,
                    key="next_btn"):
            st.session_state.page_num = min(total_pages, current_page + 1)
            st.rerun()
    
    with col4:
        new_page = st.number_input(
            "Lompat ke halaman:",
            min_value=1,
            max_value=total_pages,
            value=current_page,
            key="page_jump"
        )
        if new_page != current_page:
            st.session_state.page_num = new_page
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_transliterasi_content(data):
    """Render konten transliterasi dengan typography yang optimal."""
    if not data:
        st.info("📝 Data transliterasi untuk halaman ini belum tersedia.")
        return
    
    for i, item in enumerate(data, 1):
        st.markdown(f"""
        <div class="transliterasi-item">
            <div class="latin-text">{item['latin']}</div>
            <div class="translation-text"><strong>Terjemahan:</strong> {item['terjemahan']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_search_results(results, query):
    """Render hasil pencarian dengan highlighting yang subtle."""
    if not results:
        st.info("🔍 Tidak ada hasil yang ditemukan.")
        return
    
    st.success(f"✅ Ditemukan {len(results)} hasil untuk '{query}'")
    
    for item in results:
        # Simple highlighting tanpa regex untuk performa
        latin_highlighted = item['latin'].replace(
            query, f"<span class='highlight'>{query}</span>"
        )
        translation_highlighted = item['terjemahan'].replace(
            query, f"<span class='highlight'>{query}</span>"
        )
        
        st.markdown(f"""
        <div class="search-result">
            <div class="latin-text">{latin_highlighted}</div>
            <div class="translation-text"><strong>Terjemahan:</strong> {translation_highlighted}</div>
        </div>
        """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# --- MAIN APPLICATION ---
def main():
    # Skip to content link untuk accessibility
    st.markdown('<a href="#main-content" class="skip-link">Skip to main content</a>', 
               unsafe_allow_html=True)
    
    # Load data
    with st.spinner("📚 Memuat data naskah..."):
        rdf_data = load_rdf_data()
    
    if rdf_data is None:
        st.error("❌ Aplikasi tidak dapat berjalan karena data naskah tidak berhasil dimuat.")
        st.stop()
    
    # Constants
    TOTAL_PAGES = 20
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("# 📜 Kakawin Ramayana")
        st.markdown("---")
        
        page = st.radio(
            "Navigasi Utama",
            ["📖 Transliterasi", "🔍 Pencarian", "ℹ️ Tentang Naskah"],
            key="main_nav"
        )
        
        st.markdown("---")
        
        # Sidebar image dengan proper alt text
        st.image(
            "https://images.pexels.com/photos/8828489/pexels-photo-8828489.jpeg?auto=compress&cs=tinysrgb&w=400",
            caption="Ilustrasi Wayang Kulit",
            use_container_width=True
        )
        
        st.markdown("---")
        st.markdown("**📚 Preservasi Budaya Digital**")
        st.markdown("Naskah kuno untuk generasi masa depan")
    
    # Main content area
    st.markdown('<div id="main-content">', unsafe_allow_html=True)
    
    # Page routing dengan improved UX
    if page == "📖 Transliterasi":
        st.title("📖 Transliterasi Naskah")
        
        # Two-column layout untuk desktop, stack untuk mobile
        col1, col2 = st.columns([5, 7], gap="large")
        
        with col1:
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.subheader(f"Halaman {st.session_state.page_num}")
            
            # Image dengan fallback
            image_path = f"images/page_{st.session_state.page_num}.png"
            if os.path.exists(image_path):
                st.image(image_path, 
                        caption=f"Naskah halaman {st.session_state.page_num}",
                        use_container_width=True)
            else:
                st.warning(f"🖼️ Gambar halaman {st.session_state.page_num} tidak tersedia.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Navigation controls
            render_navigation_controls(st.session_state.page_num, TOTAL_PAGES)
        
        with col2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("Transliterasi & Terjemahan")
            
            # Show content hanya untuk halaman 3 (sesuai data yang tersedia)
            if st.session_state.page_num == 3:
                render_transliterasi_content(rdf_data)
            else:
                st.info("📝 Data transliterasi untuk halaman ini sedang dalam proses digitalisasi.")
                st.markdown("""
                **Catatan:** Proyek digitalisasi naskah ini sedang berlangsung. 
                Halaman lain akan segera tersedia.
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif page == "🔍 Pencarian":
        st.title("🔍 Pencarian Teks")
        
        # Search interface
        search_query = st.text_input(
            "Cari dalam naskah:",
            placeholder="Masukkan kata kunci untuk mencari dalam transliterasi atau terjemahan...",
            help="Pencarian akan mencari di teks latin dan terjemahan Indonesia"
        )
        
        if search_query:
            # Perform search
            query_lower = search_query.lower()
            results = [
                item for item in rdf_data 
                if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()
            ]
            
            # Display results
            render_search_results(results, search_query)
        else:
            st.info("💡 Masukkan kata kunci di atas untuk memulai pencarian.")
            
            # Show example searches
            st.markdown("### Contoh Pencarian:")
            example_col1, example_col2 = st.columns(2)
            
            with example_col1:
                if st.button("🏹 Cari 'panah'", use_container_width=True):
                    st.session_state.search_example = "panah"
                    st.rerun()
            
            with example_col2:
                if st.button("🙏 Cari 'bhakti'", use_container_width=True):
                    st.session_state.search_example = "bhakti"
                    st.rerun()
            
            # Handle example searches
            if hasattr(st.session_state, 'search_example'):
                query = st.session_state.search_example
                results = [
                    item for item in rdf_data 
                    if query.lower() in item['latin'].lower() or query.lower() in item['terjemahan'].lower()
                ]
                st.markdown(f"### Hasil untuk '{query}':")
                render_search_results(results, query)
                del st.session_state.search_example
    
    elif page == "ℹ️ Tentang Naskah":
        st.title("ℹ️ Tentang Naskah Kakawin Ramayana")
        
        # About content dalam cards
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("""
        ## Sejarah Naskah
        
        **Kakawin Ramayana** adalah salah satu karya sastra Jawa Kuno yang paling penting, 
        ditulis pada abad ke-9 atau ke-10 Masehi. Naskah ini merupakan adaptasi dari 
        epos Ramayana Sanskrit karya Valmiki ke dalam bahasa dan budaya Jawa.
        
        ### Karakteristik Naskah:
        - **Bahasa**: Jawa Kuno (Kawi)
        - **Metrum**: Kakawin (puisi dengan metrum tertentu)
        - **Periode**: Abad ke-9-10 M
        - **Tema**: Kisah Rama dan Sita dengan nuansa budaya Jawa
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("""
        ## Tentang Proyek Digitalisasi
        
        Proyek ini bertujuan untuk melestarikan dan membuat naskah kuno lebih accessible 
        bagi peneliti, mahasiswa, dan masyarakat umum melalui teknologi digital.
        
        ### Fitur Aplikasi:
        - 📖 **Transliterasi**: Konversi aksara Jawa ke Latin
        - 🔍 **Pencarian**: Cari kata atau frasa dalam naskah
        - 📱 **Responsive**: Dapat diakses di berbagai perangkat
        - ♿ **Accessible**: Mendukung pembaca layar dan navigasi keyboard
        
        ### Teknologi yang Digunakan:
        - **RDF/Turtle**: Untuk struktur data semantik
        - **Streamlit**: Interface web interaktif
        - **Python**: Backend processing
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Contact/Credits
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("""
        ## Kredit & Kontak
        
        Proyek ini dikembangkan sebagai bagian dari upaya preservasi budaya digital.
        
        **Kontribusi:**
        - Digitalisasi naskah
        - Pengembangan aplikasi web
        - Penelitian dan transliterasi
        
        Untuk informasi lebih lanjut atau kontribusi, silakan hubungi tim pengembang.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()