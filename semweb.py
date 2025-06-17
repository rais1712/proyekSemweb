import streamlit as st
import os
from rdflib import Graph
import base64
import html
import re
from SPARQLWrapper import SPARQLWrapper, JSON

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Digitalisasi Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNGSI PEMUATAN ASET ---
def load_asset(file_path):
    """Fungsi untuk memuat file CSS atau JS eksternal dengan encoding UTF-8."""
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Peringatan: File aset tidak ditemukan di '{file_path}'.")
        return ""

def get_image_as_base64(file_path):
    """Fungsi untuk mengonversi gambar menjadi base64."""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

# Ganti fungsi load_rdf_data dengan versi ini
@st.cache_data
def load_rdf_data(page_num, fuseki_endpoint="http://localhost:3030/kakawin/query"):
    """Mengambil data transliterasi dari SPARQL endpoint Fuseki UNTUK HALAMAN TERTENTU."""
    query = f"""
    PREFIX jawa: <http://example.org/jawa#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?kalimat_uri ?latin ?terjemahan WHERE {{
        ?kalimat_uri a jawa:Kalimat ;
                     jawa:latin ?latin ;
                     jawa:terjemahan ?terjemahan ;
                     jawa:halaman ?halaman .
        FILTER(?halaman = {page_num})
    }} ORDER BY ?kalimat_uri
    """
    try:
        sparql = SPARQLWrapper(fuseki_endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = [
            {
                "uri": r["kalimat_uri"]["value"],
                "latin": r["latin"]["value"],
                "terjemahan": r["terjemahan"]["value"]
            }
            for r in results["results"]["bindings"]
        ]
        return data
    except Exception as e:
        st.error(f"Gagal terhubung atau mengambil data dari server Fuseki: {e}")
        st.info("Pastikan server Apache Jena Fuseki Anda sedang berjalan di http://localhost:3030")
        return None
    
# Tambahkan fungsi BARU ini di bawah fungsi load_rdf_data
@st.cache_data
def load_all_rdf_data(fuseki_endpoint="http://localhost:3030/kakawin/query"):
    """Mengambil SEMUA data transliterasi dari Fuseki untuk keperluan pencarian."""
    # Query ini tidak memiliki FILTER halaman
    query = """
    PREFIX jawa: <http://example.org/jawa#>
    SELECT ?kalimat_uri ?latin ?terjemahan WHERE {
        ?kalimat_uri a jawa:Kalimat ;
                     jawa:latin ?latin ;
                     jawa:terjemahan ?terjemahan .
    } ORDER BY ?kalimat_uri
    """
    try:
        sparql = SPARQLWrapper(fuseki_endpoint)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        data = [
            {
                "uri": r["kalimat_uri"]["value"],
                "latin": r["latin"]["value"],
                "terjemahan": r["terjemahan"]["value"]
            }
            for r in results["results"]["bindings"]
        ]
        return data
    except Exception as e:
        st.error(f"Gagal terhubung atau mengambil data dari server Fuseki: {e}")
        st.info("Pastikan server Apache Jena Fuseki Anda sedang berjalan di http://localhost:3030")
        return None

# --- INISIALISASI SESSION STATE ---
def init_session_state():
    """Inisialisasi state yang dibutuhkan."""
    if 'page_num' not in st.session_state:
        query_params = st.query_params.to_dict()
        st.session_state.page_num = int(query_params.get("page", [1])[0])

# --- KOMPONEN UI UTAMA ---
def render_hero_section():
    """Merender Hero Section dengan animasi dan efek visual yang menarik."""
    st.markdown("""
        <section class="hero-section">
            <div class="hero-background-pattern"></div>
            <div class="hero-content">
                <div class="hero-icon">📜</div>
                <h1 class="hero-title">Kakawin Ramayana</h1>
                <p class="hero-subtitle">Menjelajahi Kekayaan Sastra Jawa Kuno</p>
                <div class="hero-decorative-line"></div>
            </div>
        </section>
    """, unsafe_allow_html=True)

def render_transliteration_page(rdf_data, total_pages=20):
    """Merender halaman transliterasi dengan tampilan Kawi dan Interpretasi disatukan."""
    st.markdown('<h2 class="page-title">📖 Transliterasi Naskah</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="transliteration-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1], gap="large")

    # --- Kolom Kiri (Gambar Naskah & Navigasi) - Tidak ada perubahan ---
    with col1:
        st.markdown(f"""
            <div class="panel-header manuscript-header">
                <div class="panel-header-icon">📜</div>
                <div class="panel-header-text">
                    <h3>Naskah Asli</h3>
                    <span class="panel-header-subtitle">Halaman {st.session_state.page_num}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
        image_path = os.path.join(script_dir, "images", f"page_{st.session_state.page_num}.png")
        
        if os.path.exists(image_path):
            image_b64 = get_image_as_base64(image_path)
            if image_b64:
                st.markdown(f'<div class="manuscript-panel"><div class="manuscript-frame"><img id="manuscriptImage" src="data:image/png;base64,{image_b64}" class="manuscript-image"></div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="manuscript-panel"><div class="manuscript-placeholder"><div class="placeholder-icon">📜</div><p>Gambar naskah untuk halaman {st.session_state.page_num} tidak ditemukan.</p></div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="page-nav-container"><div class="page-nav-bar-st">', unsafe_allow_html=True)
        nav_cols = st.columns([1, 3, 1])
        with nav_cols[0]:
            if st.button("◀", key="prev_page_btn", use_container_width=True, disabled=(st.session_state.page_num <= 1)):
                st.session_state.page_num -= 1
                st.rerun()
        with nav_cols[1]:
            st.markdown(f'<div class="page-indicator-nav"><div class="page-info"><span class="current-page">{st.session_state.page_num}</span><span class="page-separator">dari</span><span class="total-pages">{total_pages}</span></div><div class="page-progress"><div class="progress-bar" style="width: {(st.session_state.page_num/total_pages)*100}%"></div></div></div>', unsafe_allow_html=True)
        with nav_cols[2]:
            if st.button("▶", key="next_page_btn", use_container_width=True, disabled=(st.session_state.page_num >= total_pages)):
                st.session_state.page_num += 1
                st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

    # --- Kolom Kanan (Transliterasi) - LOGIKA BARU ---
    with col2:
        st.markdown(f"""
            <div class="panel-header transliteration-header">
                <div class="panel-header-icon">📖</div>
                <div class="panel-header-text">
                    <h3>Transliterasi</h3>
                    <span class="panel-header-subtitle">Halaman {st.session_state.page_num}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="transliteration-content">', unsafe_allow_html=True)
        with st.container(height=650):
            if rdf_data and len(rdf_data) % 8 == 0: # Pastikan data valid (kelipatan 8 baris per stanza)
                st.markdown('<div class="transliteration-items">', unsafe_allow_html=True)
                
                num_stanzas = len(rdf_data) // 8
                num_lines_per_stanza = 4

                for i in range(num_stanzas * num_lines_per_stanza):
                    kawi_item = rdf_data[i]
                    modern_item = rdf_data[i + (num_stanzas * num_lines_per_stanza)]

                    st.markdown(f"""
                        <div class="transliterasi-item" data-item="{i+1}">
                            <div class="item-number">{i % 4 + 1}</div>
                            <div class="item-content">
                                <div class="unified-text-block">
                                    <span class="text-label">Teks Kawi:</span>
                                    <span class="latin-text-kawi">{kawi_item['latin']}</span>
                                </div>
                                <div class="unified-text-block">
                                    <span class="text-label">Interpretasi:</span>
                                    <span class="latin-text-modern">{modern_item['latin']}</span>
                                </div>
                                <div class="translation-divider"></div>
                                <div class="translation-text">
                                    <span class="translation-label">Terjemahan:</span>
                                    <span class="translation-content">{html.escape(kawi_item['terjemahan'])}</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="no-data-placeholder">
                        <div class="placeholder-icon">📖</div>
                        <h4>Data Belum Tersedia</h4>
                        <p>Data transliterasi untuk halaman {st.session_state.page_num} sedang dalam proses digitalisasi atau tidak ditemukan.</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_search_page(rdf_data):
    """Merender halaman pencarian yang dipercantik."""
    st.markdown('<h2 class="page-title">🔍 Pencarian Teks</h2>', unsafe_allow_html=True)
    st.markdown('<div class="search-page-container">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="search-panel">
            <div class="search-header">
                <div class="search-icon">🔍</div>
                <h3>Cari dalam Naskah</h3>
                <p>Temukan teks dalam transliterasi Latin atau terjemahan Bahasa Indonesia</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    search_query = st.text_input("Cari...", placeholder="Ketik kata kunci yang ingin dicari...", label_visibility="collapsed")

    if search_query:
        st.markdown('<div class="search-results-section">', unsafe_allow_html=True)
        
        if rdf_data:
            query_lower = search_query.lower()
            results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
            
            if not results:
                st.markdown(f"""<div class="no-results">...</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="results-header">
                        <div class="results-count">
                            <span class="results-icon">✨</span>
                            <span class="results-text">Ditemukan <strong>{len(results)} hasil</strong> untuk "<strong>{search_query}</strong>"</span>
                        </div>
                    </div>""", unsafe_allow_html=True)
                
                st.markdown('<div class="search-results-container">', unsafe_allow_html=True)
                # Ganti blok 'for' di render_search_page dengan ini
                for i, item in enumerate(results):
                    highlighted_latin = re.sub(f'({re.escape(search_query)})', r'<mark>\1</mark>', item['latin'], flags=re.IGNORECASE)
                    highlighted_translation = re.sub(f'({re.escape(search_query)})', r'<mark>\1</mark>', item['terjemahan'], flags=re.IGNORECASE)

                    expander_title = item['latin'].replace(search_query, f"<mark>{search_query}</mark>")
                    
                    with st.expander(f"📝 Hasil {i+1}: {item['latin'][:70]}{'...' if len(item['latin']) > 70 else ''}", expanded=(i < 3)):
                        # KODE YANG DIPERBAIKI
                        st.markdown(f"""
                            <div class="item-content" style="padding-top: 10px;">
                                <div class="latin-text">{highlighted_latin}</div>
                                <div class="translation-divider"></div>
                                <div class="translation-text">
                                    <span class="translation-label">Terjemahan:</span>
                                    <span class="translation-content">{highlighted_translation}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
        else:
            st.markdown("""<div class="error-state">...</div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_about_page():
    """Merender halaman 'Tentang Naskah' dengan konten yang informatif."""
    st.markdown('<h2 class="page-title">📜 Tentang Naskah Kakawin Ramayana</h2>', unsafe_allow_html=True)

    with st.expander("🚪 Pendahuluan: Membuka Gerbang Kakawin Ramayana", expanded=True):
        st.markdown("""
        Proyek digitalisasi ini bertujuan untuk melestarikan dan memperkenalkan kembali **Kakawin Ramayana**, salah satu karya sastra terbesar dalam sejarah Jawa Kuno. Melalui platform ini, kami menyajikan naskah asli, transliterasi teks, serta terjemahannya untuk menjembatani kekayaan masa lalu dengan generasi masa kini.
        """)

    with st.expander("🏛️ Jejak Sejarah: Asal-Usul dan Konteks Penciptaan"):
        st.markdown("""
        Kakawin Ramayana diperkirakan digubah pada masa Kerajaan Medang (Mataram Kuno) sekitar abad ke-9 Masehi. Karya ini merupakan adaptasi dari epos Ramayana karya Walmiki dari India, namun dengan sentuhan lokal yang kental, baik dari segi bahasa, budaya, maupun nilai-nilai filosofis yang diusung.
        """)

    with st.expander("⚔️ Kisah Abadi Sang Rama: Alur Cerita Kakawin Ramayana"):
        st.markdown("""
        Cerita berpusat pada perjalanan **Rama**, seorang pangeran dari Ayodhya, yang harus menjalani pengasingan di hutan selama 14 tahun bersama istrinya, **Sita**, dan adiknya, **Laksmana**. Konflik memuncak ketika Sita diculik oleh Rahwana, raja raksasa dari Alengka, yang memicu perang besar antara pasukan Rama yang dibantu oleh wanara (manusia kera) melawan pasukan raksasa.
        """)

    with st.expander("🎨 Gubahan Jawa: Perbedaan dengan Epos India"):
        st.markdown("""
        Meskipun alur utamanya sama, Kakawin Ramayana memiliki perbedaan signifikan dengan versi India. Para pujangga Jawa tidak hanya menerjemahkan, tetapi juga menggubah kembali cerita dengan memasukkan unsur-unsur lokal, metrum kakawin yang khas, dan interpretasi filosofis yang lebih mendalam sesuai dengan kearifan lokal pada masanya.
        """)

    with st.expander("🌟 Warisan Budaya Tak Ternilai: Pengaruh Kakawin Ramayana"):
        st.markdown("""
        Karya ini memiliki pengaruh yang luar biasa dalam kebudayaan Jawa dan Nusantara. Kisahnya diadaptasi ke dalam berbagai bentuk seni seperti relief candi (terutama Candi Prambanan), seni pertunjukan wayang kulit, sendratari, hingga menjadi inspirasi bagi karya-karya sastra setelahnya.
        """)

# --- FUNGSI UTAMA ---
def main():
    """Fungsi utama untuk menjalankan aplikasi Streamlit."""
    init_session_state()
    st.markdown(f'<style>{load_asset("assets/style.css")}</style>', unsafe_allow_html=True)
    st.markdown('<div class="app-container">', unsafe_allow_html=True)

    # --- Blok Sidebar ---
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-header">
                <div class="sidebar-logo">📜</div>
                <h2 class="sidebar-title">Navigasi</h2>
                <div class="sidebar-subtitle">Kakawin Ramayana</div>
            </div>""", unsafe_allow_html=True)
        app_page = st.radio("Pilih Halaman:", ["Transliterasi & Naskah", "Pencarian", "Tentang Naskah"], label_visibility="collapsed")
        st.markdown("---")
        st.markdown("""
            <div class="sidebar-footer">
                <div class="footer-content">
                    <div class="footer-icon">🌟</div>
                    <div class="footer-text">
                        <strong>Digitalisasi Kakawin Ramayana</strong>
                        <br><small>Preservasi Warisan Budaya, 2025</small>
                    </div>
                </div>
                <div class="footer-stats">
                    <div class="stat-item"><span class="stat-number">20</span><span class="stat-label">Halaman</span></div>
                    <div class="stat-item"><span class="stat-number">∞</span><span class="stat-label">Makna</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

    # --- Blok Konten Utama ---
    # Pastikan blok ini berada DI LUAR 'with st.sidebar:'
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    if app_page == "Transliterasi & Naskah":
        # Muat data hanya untuk halaman saat ini
        rdf_data = load_rdf_data(page_num=st.session_state.page_num)
        render_hero_section()
        render_transliteration_page(rdf_data)
    elif app_page == "Pencarian":
        # Muat SEMUA data untuk pencarian
        all_data = load_all_rdf_data()
        render_hero_section()
        render_search_page(all_data)
    elif app_page == "Tentang Naskah":
        # Tidak perlu memuat data RDF untuk halaman ini
        render_hero_section()
        render_about_page()
    
    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()