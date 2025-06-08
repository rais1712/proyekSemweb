import streamlit as st
import os
from rdflib import Graph
import html
import re

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
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

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

    .stApp {
        background: var(--gradient-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
            Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    /* Hide default Streamlit elements safely */
    #MainMenu, footer, header {
        display: none !important;
    }
    .stDeployButton, .stDecoration {
        display: none !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Sidebar styling with stable selector */
    div[data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #2C1810 0%, #1A0F08 100%);
        border-right: 3px solid var(--primary-gold);
        box-shadow: 4px 0 20px rgba(139, 69, 19, 0.15);
        padding: 1rem 1.5rem 2rem 1.5rem;
        height: 100vh;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }

    div[data-testid="stSidebar"] h2 {
        color: var(--primary-gold) !important;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 3px 6px rgba(0,0,0,0.4);
        font-size: 1.8rem;
        background: var(--gradient-gold);
        background-clip: text;
        -webkit-background-clip: text;
        -moz-background-clip: text;
        color: transparent;
        -webkit-text-fill-color: transparent;
        -moz-text-fill-color: transparent;
        -webkit-mask-image: linear-gradient(#000 0 0);
        mask-image: linear-gradient(#000 0 0);
        padding: 1rem 0;
        border-bottom: 2px solid rgba(212, 175, 55, 0.3);
    }

    div[data-testid="stSidebar"] .stRadio > div {
        background: rgba(212, 175, 55, 0.08);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }

    div[data-testid="stSidebar"] .stRadio label {
        color: var(--secondary-cream) !important;
        font-weight: 500;
        font-size: 1.1rem;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        display: block;
        margin-bottom: 0.8rem;
        position: relative;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.05);
    }

    div[data-testid="stSidebar"] .stRadio label::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.3), transparent);
        transition: left 0.6s ease;
    }

    div[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(212, 175, 55, 0.25);
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
    }

    div[data-testid="stSidebar"] .stRadio label:hover::before {
        left: 100%;
    }

    div[data-testid="stSidebar"] .stRadio input[type="radio"]:checked + label {
        background: var(--gradient-gold);
        color: var(--text-dark) !important;
        font-weight: 600;
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 6px 16px rgba(212, 175, 55, 0.4);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--text-dark);
        font-weight: 600;
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        background: var(--gradient-gold);
        background-clip: text;
        -webkit-background-clip: text;
        -moz-background-clip: text;
        color: transparent;
        -webkit-text-fill-color: transparent;
        -moz-text-fill-color: transparent;
        -webkit-mask-image: linear-gradient(#000 0 0);
        mask-image: linear-gradient(#000 0 0);
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

    .manuscript-image {
        background: transparent;
        border: none;
        padding: 0;
        border-radius: 0;
        box-shadow: none;
        transition: none;
    }

    .manuscript-image:hover {
        transform: none;
        box-shadow: none;
    }

    .transliterasi-container {
        background: var(--bg-paper);
        border: 2px solid var(--border-light);
        border-radius: 16px;
        padding: 1.5rem;
        height: 600px;
        overflow-y: auto;
        box-shadow: var(--shadow-medium);
        position: relative;
    }

    .transliterasi-container::-webkit-scrollbar {
        width: 8px;
    }

    .transliterasi-container::-webkit-scrollbar-track {
        background: var(--bg-parchment);
        border-radius: 4px;
    }

    .transliterasi-container::-webkit-scrollbar-thumb {
        background: var(--primary-gold);
        border-radius: 4px;
    }

    .transliterasi-container::-webkit-scrollbar-thumb:hover {
        background: var(--primary-brown);
    }

    .transliterasi-item {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--primary-gold);
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease;
        width: 100%;
        box-sizing: border-box;
    }

    .transliterasi-item:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        border-color: var(--primary-gold);
        background: rgba(255, 255, 255, 0.9);
    }

    .latin-text {
        font-family: 'Playfair Display', serif;
        font-style: normal;
        font-size: 1.25rem;
        color: var(--text-dark);
        margin-bottom: 1rem;
        line-height: 1.6;
        font-weight: 500;
        word-wrap: break-word;
    }

    .translation-text {
        font-family: 'Inter', sans-serif;
        color: var(--text-medium);
        font-size: 1rem;
        line-height: 1.7;
        font-weight: 400;
        word-wrap: break-word;
    }

    .translation-text strong {
        color: var(--primary-brown);
        font-weight: 600;
    }

    .search-highlight {
        background: linear-gradient(120deg, #FFF3CD 0%, #FFEAA7 100%);
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        color: var(--primary-brown);
    }

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

    .about-content {
        background: var(--bg-paper);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: var(--shadow-medium);
        border: 1px solid var(--border-light);
        font-family: 'Inter', sans-serif;
        color: var(--text-dark);
        line-height: 1.7;
    }

    .about-content h3 {
        color: var(--primary-brown);
        border-left: 4px solid var(--primary-gold);
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
        font-family: 'Playfair Display', serif;
    }

    .about-content p {
        margin-bottom: 1.5rem;
        color: var(--text-medium);
    }

    .about-content strong {
        color: var(--primary-brown);
        font-weight: 600;
    }

    .about-list {
        list-style: none;
        padding-left: 0;
        margin: 1rem 0;
    }

    .about-list li {
        position: relative;
        padding-left: 2rem;
        margin-bottom: 0.75rem;
        color: var(--text-medium);
    }

    .about-list li::before {
        content: '◆';
        position: absolute;
        left: 0;
        color: var(--primary-gold);
        font-size: 0.8rem;
        top: 0.2rem;
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .transliterasi-item {
            padding: 1rem;
        }
        
        .latin-text {
            font-size: 1.1rem;
        }

        div[data-testid="stSidebar"] h2 {
            font-size: 1.5rem;
        }

        div[data-testid="stSidebar"] .stRadio label {
            font-size: 1rem;
            padding: 0.8rem 1.2rem;
        }

        .transliterasi-container {
            height: 400px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- PEMUATAN DATA ---
@st.cache_data
def load_rdf_data(ttl_file="naskah_bhakti_final.ttl"):
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

# --- FUNGSI BANTUAN ---
def render_transliterasi_content(data):
    if not data:
        st.info("Data transliterasi untuk halaman ini belum tersedia.")
        return
    
    # Gunakan st.container() untuk memastikan rendering yang konsisten
    with st.container():
        # Render setiap item secara terpisah menggunakan st.markdown
        for i, item in enumerate(data):
            # Buat HTML untuk setiap item secara terpisah
            item_html = f'''
            <div class="transliterasi-item" style="
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(139, 69, 19, 0.1);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                border-left: 4px solid #D4AF37;
                box-shadow: 0 4px 12px rgba(139, 69, 19, 0.08);
                transition: all 0.3s ease;
                width: 100%;
                box-sizing: border-box;
            ">
                <div class="latin-text" style="
                    font-family: 'Playfair Display', serif;
                    font-style: normal;
                    font-size: 1.25rem;
                    color: #2C1810;
                    margin-bottom: 1rem;
                    line-height: 1.6;
                    font-weight: 500;
                    word-wrap: break-word;
                ">{html.escape(item["latin"])}</div>
                <div class="translation-text" style="
                    font-family: 'Inter', sans-serif;
                    color: #5D4E37;
                    font-size: 1rem;
                    line-height: 1.7;
                    font-weight: 400;
                    word-wrap: break-word;
                "><strong style="color: #8B4513; font-weight: 600;">Terjemahan:</strong> {html.escape(item["terjemahan"])}</div>
            </div>
            '''
            
            # Render setiap item secara individual
            st.markdown(item_html, unsafe_allow_html=True)

def render_search_results(results, query):
    if not results:
        st.info("Tidak ada hasil yang cocok ditemukan.")
        return
    
    st.success(f"Ditemukan {len(results)} hasil untuk '{html.escape(query)}'")
    
    # Gunakan st.container() untuk konsistensi
    with st.container():
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        
        for i, item in enumerate(results):
            # Escape HTML terlebih dahulu
            latin_escaped = html.escape(item['latin'])
            translation_escaped = html.escape(item['terjemahan'])
            
            # Tambahkan highlight
            latin_highlighted = pattern.sub(
                lambda m: f"<span style='background: linear-gradient(120deg, #FFF3CD 0%, #FFEAA7 100%); padding: 2px 6px; border-radius: 4px; font-weight: 600; color: #8B4513;'>{m.group(0)}</span>", 
                latin_escaped
            )
            translation_highlighted = pattern.sub(
                lambda m: f"<span style='background: linear-gradient(120deg, #FFF3CD 0%, #FFEAA7 100%); padding: 2px 6px; border-radius: 4px; font-weight: 600; color: #8B4513;'>{m.group(0)}</span>", 
                translation_escaped
            )
            
            # Render setiap hasil pencarian secara individual
            result_html = f'''
            <div style="
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(139, 69, 19, 0.1);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                border-left: 4px solid #D4AF37;
                box-shadow: 0 4px 12px rgba(139, 69, 19, 0.08);
                transition: all 0.3s ease;
                width: 100%;
                box-sizing: border-box;
            ">
                <div style="
                    font-family: 'Playfair Display', serif;
                    font-style: normal;
                    font-size: 1.25rem;
                    color: #2C1810;
                    margin-bottom: 1rem;
                    line-height: 1.6;
                    font-weight: 500;
                    word-wrap: break-word;
                ">{latin_highlighted}</div>
                <div style="
                    font-family: 'Inter', sans-serif;
                    color: #5D4E37;
                    font-size: 1rem;
                    line-height: 1.7;
                    font-weight: 400;
                    word-wrap: break-word;
                "><strong style="color: #8B4513; font-weight: 600;">Terjemahan:</strong> {translation_highlighted}</div>
            </div>
            '''
            
            st.markdown(result_html, unsafe_allow_html=True)

def render_about_page():
    st.markdown("## 🏛️ Sejarah Naskah")
    st.markdown("""
    **Kakawin Ramayana** adalah salah satu karya sastra Jawa Kuno yang paling penting, diperkirakan 
    ditulis pada abad ke-9 atau ke-10 Masehi. Naskah ini merupakan adaptasi dari epos Ramayana Sanskrit 
    karya Valmiki, namun diresapi dengan nilai-nilai, budaya, dan bahasa lokal Jawa Kuno.
    """)
    
    st.markdown("### 📚 Karakteristik Utama")
    st.markdown("**Bahasa:** Jawa Kuno (Kawi)")
    st.markdown("**Bentuk:** Puisi Kakawin (memiliki aturan metrum yang ketat)")
    st.markdown("**Periode:** Kerajaan Medang (Mataram Kuno)")
    st.markdown("**Isi:** Mengisahkan perjalanan hidup Sang Rama dalam mencari dan menyelamatkan istrinya, Sita, dengan nuansa filosofis Hindu-Jawa yang kental")

    st.markdown("## 💻 Tentang Proyek Digitalisasi Ini")
    st.markdown("""
    Proyek ini bertujuan untuk melestarikan warisan budaya takbenda ini dan membuatnya lebih mudah 
    diakses oleh para peneliti, mahasiswa, serta masyarakat umum melalui teknologi digital.
    """)
    
    st.markdown("### 🛠️ Teknologi yang Digunakan")
    st.markdown("**RDF (Resource Description Framework):** Data naskah distrukturkan secara semantik menggunakan format Turtle (.ttl) untuk mendefinisikan hubungan antar entitas seperti cerita, kalimat, dan terjemahan")
    st.markdown("**Streamlit:** Kerangka kerja Python yang digunakan untuk membangun antarmuka web interaktif ini dengan cepat")
    st.markdown("**Python:** Bahasa pemrograman utama yang digunakan untuk memproses data RDF dan menjalankan aplikasi")
    
    st.markdown("### 🎯 Fitur Utama")
    st.markdown("**Navigasi Interaktif:** Jelajahi halaman-halaman naskah dengan mudah")
    st.markdown("**Pencarian Semantik:** Cari teks dalam bahasa Latin dan terjemahan Indonesia")
    st.markdown("**Tampilan Responsif:** Optimal di berbagai perangkat dan ukuran layar")
    st.markdown("**Desain Otentik:** Tema visual yang menghormati karakteristik naskah kuno")

# --- INISIALISASI SESSION STATE ---
if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# --- APLIKASI UTAMA ---
def main():
    with st.sidebar:
        st.markdown('<div class="custom-sidebar">', unsafe_allow_html=True)
        st.markdown("## 📜 Kakawin Ramayana")
        st.markdown("---")
        
        page = st.radio(
            "Navigasi",
            ["📖 Transliterasi", "🔍 Pencarian", "ℹ️ Tentang Naskah"],
            key="main_nav"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    rdf_data = load_rdf_data()
    if rdf_data is None:
        st.stop()

    if page == "📖 Transliterasi":
        st.markdown("<h1>📜 Transliterasi & Terjemahan Naskah</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.subheader(f"Halaman Naskah {st.session_state.page_num}")
            
            image_path = f"images/page_{st.session_state.page_num}.png"
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.warning(f"Gambar untuk halaman {st.session_state.page_num} tidak tersedia.")

            TOTAL_PAGES = 20
            nav_cols = st.columns([2, 1, 2])
            
            # Tombol Sebelumnya dengan key unik dan disabled sesuai kondisi
            if nav_cols[0].button("← Sebelumnya", use_container_width=True, disabled=(st.session_state.page_num == 1), key="prev_button"):
                if st.session_state.page_num > 1:
                    st.session_state.page_num -= 1
                    st.rerun()
            
            # Indikator halaman
            nav_cols[1].markdown(f"<div class='page-indicator'>{st.session_state.page_num}/{TOTAL_PAGES}</div>", unsafe_allow_html=True)
            
            # Tombol Selanjutnya dengan key unik dan disabled sesuai kondisi
            if nav_cols[2].button("Selanjutnya →", use_container_width=True, disabled=(st.session_state.page_num == TOTAL_PAGES), key="next_button"):
                if st.session_state.page_num < TOTAL_PAGES:
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


if __name__ == "__main__":
    main()