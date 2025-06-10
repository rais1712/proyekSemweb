import streamlit as st
import os
from rdflib import Graph
import base64
import html
import re
import json
from datetime import datetime
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Digitalisasi Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INISIALISASI SESSION STATE ---
def init_session_state():
    """Inisialisasi state untuk personalisasi dan tracking"""
    if 'page_num' not in st.session_state:
        st.session_state.page_num = 1
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'font_size' not in st.session_state:
        st.session_state.font_size = 'medium'
    if 'reading_mode' not in st.session_state:
        st.session_state.reading_mode = False
    if 'bookmarks' not in st.session_state:
        st.session_state.bookmarks = []
    if 'recent_pages' not in st.session_state:
        st.session_state.recent_pages = []
    if 'user_annotations' not in st.session_state:
        st.session_state.user_annotations = {}
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []

# --- FUNGSI PEMUATAN ASET ---
def load_asset(file_path):
    """Fungsi untuk memuat file CSS atau JS eksternal"""
    try:
        # Menambahkan argumen encoding='utf-8' untuk memastikan file dibaca dengan benar
         with open(file_path, mode="r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
         st.error(f"Peringatan: File aset tidak ditemukan di '{file_path}'.")
         return ""

def get_image_as_base64(file_path):
    """Fungsi untuk mengonversi gambar menjadi base64"""
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
        return data
    except Exception as e:
        st.error(f"Gagal memuat data RDF: {e}")
        return None

# --- FUNGSI UTILITY ---
def add_to_recent_pages(page_num):
    """Menambahkan halaman ke recent activity"""
    if page_num not in st.session_state.recent_pages:
        st.session_state.recent_pages.insert(0, page_num)
        if len(st.session_state.recent_pages) > 5:
            st.session_state.recent_pages.pop()

def add_to_search_history(query):
    """Menambahkan query ke search history"""
    if query and query not in st.session_state.search_history:
        st.session_state.search_history.insert(0, query)
        if len(st.session_state.search_history) > 10:
            st.session_state.search_history.pop()

def toggle_bookmark(page_num):
    """Toggle bookmark untuk halaman"""
    if page_num in st.session_state.bookmarks:
        st.session_state.bookmarks.remove(page_num)
    else:
        st.session_state.bookmarks.append(page_num)

def get_jawa_kuno_glossary():
    """Mendefinisikan glossary untuk istilah Jawa Kuno"""
    return {
        "bhakti": "Pengabdian atau pemujaan kepada Tuhan",
        "prajurit": "Prajurit atau tentara",
        "ratu": "Raja atau pemimpin",
        "mantra": "Doa atau jampi-jampi suci",
        "dharma": "Kewajiban moral dan spiritual"
    }

# --- KOMPONEN UI UTAMA ---
def render_hero_section():
    """Hero Section dengan animasi dan background batik"""
    st.markdown("""
        <section class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Kakawin Ramayana</h1>
                <p class="hero-subtitle">Menjelajahi Kekayaan Sastra Jawa Kuno Melalui Digitalisasi Interaktif</p>
                <div class="hero-stats">
                    <div class="stat-item">
                        <span class="stat-number">20</span>
                        <span class="stat-label">Halaman</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">500+</span>
                        <span class="stat-label">Baris Teks</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">1000+</span>
                        <span class="stat-label">Kata Unik</span>
                    </div>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

def render_personalization_panel():
    """Panel personalisasi untuk user preferences"""
    with st.expander("⚙️ Pengaturan Tampilan", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🌓 Toggle Dark Mode"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
        with col2:
            font_size = st.selectbox(
                "Ukuran Font:",
                ["small", "medium", "large"],
                index=["small", "medium", "large"].index(st.session_state.font_size)
            )
            st.session_state.font_size = font_size
        
        with col3:
            if st.button("📖 Mode Baca"):
                st.session_state.reading_mode = not st.session_state.reading_mode
                st.rerun()

def render_advanced_navigation(total_pages=20):
    """Advanced Navigation System dengan timeline dan progress"""
    st.markdown('<div class="navigation-container">', unsafe_allow_html=True)
    
    # Timeline Navigation dengan thumbnail preview
    st.markdown("### 🗺️ Navigasi Timeline")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Slider dengan custom styling
        page_num = st.slider(
            "Pilih Halaman", 
            min_value=1, 
            max_value=total_pages, 
            value=st.session_state.page_num,
            key="main_slider"
        )
        
        if page_num != st.session_state.page_num:
            st.session_state.page_num = page_num
            add_to_recent_pages(page_num)
    
    with col2:
        # Quick jump buttons
        st.markdown("**Quick Jump:**")
        if st.button("⏮️ Awal"):
            st.session_state.page_num = 1
            st.rerun()
        if st.button("⏭️ Akhir"):
            st.session_state.page_num = total_pages
            st.rerun()
    
    with col3:
        # Bookmark toggle
        is_bookmarked = st.session_state.page_num in st.session_state.bookmarks
        bookmark_label = "⭐ Hapus Bookmark" if is_bookmarked else "☆ Tambah Bookmark"
        if st.button(bookmark_label):
            toggle_bookmark(st.session_state.page_num)
            st.rerun()
    
    # Progress dan breadcrumb
    progress_val = st.session_state.page_num / total_pages
    st.progress(progress_val, text=f"Progres: {int(progress_val*100)}% • Halaman {st.session_state.page_num}/{total_pages}")
    
    # Breadcrumb
    st.markdown(f"""
        <div class="breadcrumb">
            <span>Beranda</span> › <span>Transliterasi</span> › <span class="current">Halaman {st.session_state.page_num}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Recent pages
    if st.session_state.recent_pages:
        st.markdown("**Halaman Terakhir:** " + " | ".join([
            f"[{p}]" for p in st.session_state.recent_pages[:3]
        ]))
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_enhanced_search(rdf_data):
    """Enhanced Search dengan suggestions dan filters"""
    st.markdown("### 🔍 Pencarian Lanjutan")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Cari dalam naskah:",
            placeholder="Ketik kata kunci...",
            help="Gunakan 'AND', 'OR' untuk pencarian boolean"
        )
    
    with col2:
        search_type = st.selectbox(
            "Jenis Pencarian:",
            ["Semua", "Latin", "Terjemahan"]
        )
    
    # Search suggestions dari history
    if st.session_state.search_history:
        st.markdown("**Pencarian Terkini:** " + " | ".join([
            f"`{q}`" for q in st.session_state.search_history[:5]
        ]))
    
    if search_query:
        add_to_search_history(search_query)
        
        if rdf_data:
            # Boolean search logic
            if " AND " in search_query.upper():
                terms = [t.strip().lower() for t in search_query.upper().split(" AND ")]
                results = [
                    item for item in rdf_data 
                    if all(term in item['latin'].lower() or term in item['terjemahan'].lower() for term in terms)
                ]
            elif " OR " in search_query.upper():
                terms = [t.strip().lower() for t in search_query.upper().split(" OR ")]
                results = [
                    item for item in rdf_data 
                    if any(term in item['latin'].lower() or term in item['terjemahan'].lower() for term in terms)
                ]
            else:
                query_lower = search_query.lower()
                if search_type == "Latin":
                    results = [item for item in rdf_data if query_lower in item['latin'].lower()]
                elif search_type == "Terjemahan":
                    results = [item for item in rdf_data if query_lower in item['terjemahan'].lower()]
                else:
                    results = [
                        item for item in rdf_data 
                        if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()
                    ]
            
            render_search_results(results, search_query)
        else:
            st.error("Data tidak tersedia untuk pencarian.")

def render_search_results(results, query):
    """Render hasil pencarian dengan highlighting"""
    if not results:
        st.info("Tidak ada hasil yang cocok.")
        return
    
    st.success(f"Ditemukan {len(results)} hasil untuk '{query}'")
    
    # Multiple term highlighting
    terms = re.findall(r'\b\w+\b', query.lower())
    
    for i, item in enumerate(results):
        with st.expander(f"Hasil {i+1}: {item['latin'][:50]}...", expanded=i<3):
            latin_text = item['latin']
            translation_text = item['terjemahan']
            
            # Highlight multiple terms
            for term in terms:
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                latin_text = pattern.sub(f"<mark>{term}</mark>", latin_text)
                translation_text = pattern.sub(f"<mark>{term}</mark>", translation_text)
            
            st.markdown(f"""
                <div class="search-result">
                    <div class="latin-text">{latin_text}</div>
                    <div class="translation-text"><strong>Terjemahan:</strong> {translation_text}</div>
                </div>
            """, unsafe_allow_html=True)

def render_dual_pane_layout(page_num, rdf_data):
    """Dual-pane layout dengan synchronization"""
    st.markdown('<div class="dual-pane-container">', unsafe_allow_html=True)
    
    if not st.session_state.reading_mode:
        col1, col2 = st.columns([1, 1], gap="large")
    else:
        # Reading mode - fokus pada teks
        col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown(f"### 📜 Naskah Asli - Halaman {page_num}")
        
        # Image dengan enhancement
        # Membuat path yang robust dan tidak bergantung pada direktori kerja
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "images", f"page_{page_num}.png")
        if os.path.exists(image_path):
            # Thumbnail untuk navigation
            st.markdown("**Navigasi Halaman:**")
            thumb_cols = st.columns(5)
            for i, col in enumerate(thumb_cols):
                with col:
                    thumb_page = max(1, page_num - 2 + i)
                    if thumb_page <= 20:
                        if st.button(f"{thumb_page}", key=f"thumb_{thumb_page}"):
                            st.session_state.page_num = thumb_page
                            st.rerun()
            
            # Main image dengan zoom functionality
            image_b64 = get_image_as_base64(image_path)
            if image_b64:
                st.markdown(f"""
            <div class="manuscript-panel">
                <img id="manuscriptImage" 
                    src="data:image/png;base64,{image_b64}" 
                    class="manuscript-image" 
                    alt="Naskah halaman {page_num}">
                <div class="image-controls">
                    <button id="zoomInBtn" title="Perbesar">🔍+</button>
                    <button id="zoomOutBtn" title="Perkecil">🔍-</button>
                    <button id="downloadBtn" title="Unduh Gambar">💾</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        else:
            st.warning(f"Gambar tidak ditemukan untuk halaman {page_num}")
    
    with col2:
        st.markdown(f"### 📖 Transliterasi - Halaman {page_num}")
        
        # Floating information panel
        with st.expander("ℹ️ Konteks Sejarah", expanded=False):
            st.markdown(f"""
                **Halaman {page_num} - Konteks:**
                - Bagian dari episode penting dalam Ramayana
                - Menggunakan meter Sloka tradisional
                - Mengandung ajaran moral dan spiritual
                - Ditulis dalam bahasa Jawa Kuno (Kawi)
            """)
        
        # Main transliteration content
        st.markdown('<div class="transliterasi-panel">', unsafe_allow_html=True)
        
        if page_num == 3 and rdf_data:
            glossary = get_jawa_kuno_glossary()
            
            for i, item in enumerate(rdf_data):
                # Annotation system
                annotation_key = f"annotation_{page_num}_{i}"
                user_note = st.session_state.user_annotations.get(annotation_key, "")
                
                # Tooltip untuk istilah Jawa Kuno
                latin_text = item['latin']
                for term, definition in glossary.items():
                    if term in latin_text.lower():
                        latin_text = latin_text.replace(
                            term, 
                            f'<span class="tooltip">{term}<span class="tooltiptext">{definition}</span></span>'
                        )
                
                st.markdown(f"""
                    <div class="transliterasi-item" id="item_{i}">
                        <div class="latin-text">{latin_text}</div>
                        <div class="translation-text">
                            <strong>Terjemahan:</strong> {html.escape(item['terjemahan'])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Annotation input
                with st.expander(f"📝 Catatan untuk baris {i+1}", expanded=False):
                    new_note = st.text_area(
                        "Tambahkan catatan:",
                        value=user_note,
                        key=f"note_input_{i}",
                        height=100
                    )
                    if st.button(f"Simpan Catatan", key=f"save_note_{i}"):
                        st.session_state.user_annotations[annotation_key] = new_note
                        st.success("Catatan disimpan!")
        else:
            st.info(f"Data transliterasi untuk halaman {page_num} belum tersedia.")
            
            # Simulasi data untuk demo
            if page_num != 3:
                st.markdown("""
                    <div class="transliterasi-item">
                        <div class="latin-text">Data transliterasi akan segera tersedia</div>
                        <div class="translation-text">
                            <strong>Status:</strong> Sedang dalam proses digitalisasi
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_export_panel():
    """Panel untuk export dan sharing"""
    st.markdown("### 📤 Export & Sharing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export PDF"):
            st.info("Fitur export PDF akan segera tersedia")
    
    with col2:
        if st.button("📝 Export Text"):
            st.info("Fitur export text akan segera tersedia")
    
    with col3:
        if st.button("🔗 Share Link"):
            st.info(f"Link: https://app.com/page/{st.session_state.page_num}")

def render_bookmarks_sidebar():
    """Sidebar untuk bookmarks dan recent activity"""
    if st.session_state.bookmarks:
        st.sidebar.markdown("### ⭐ Halaman Favorit")
        for bookmark in st.session_state.bookmarks:
            if st.sidebar.button(f"Halaman {bookmark}", key=f"bookmark_{bookmark}"):
                st.session_state.page_num = bookmark
                st.rerun()
    
    if st.session_state.recent_pages:
        st.sidebar.markdown("### 🕐 Terakhir Dibaca")
        for recent in st.session_state.recent_pages:
            if st.sidebar.button(f"Halaman {recent}", key=f"recent_{recent}"):
                st.session_state.page_num = recent
                st.rerun()

# --- FUNGSI UTAMA ---
def main():
    """
    Fungsi utama untuk menjalankan aplikasi Streamlit.
    Menginisialisasi state, memuat aset, dan merender semua komponen UI.
    """
    init_session_state()

    # --- MEMUAT ASET EKSTERNAL ---
    # Memuat file CSS eksternal untuk menjaga kode Python tetap bersih.
    st.markdown(f'<style>{load_asset("assets/style.css")}</style>', unsafe_allow_html=True)

    # Menentukan tema (terang/gelap) dan ukuran font berdasarkan session state.
    # Menggunakan atribut data-theme yang sesuai dengan standar di style.css.
    theme_attribute = "dark" if st.session_state.dark_mode else "light"
    font_class = f"font-{st.session_state.font_size}"

    # --- CONTAINER UTAMA APLIKASI ---
    st.markdown(f'<div data-theme="{theme_attribute}" class="app-container {font_class}">', unsafe_allow_html=True)

    # --- RENDER KOMPONEN UI ---
    render_hero_section()
    render_personalization_panel()
    render_bookmarks_sidebar()

    # Membuat tab untuk konten utama.
    tab1, tab2, tab3 = st.tabs(["📖 Transliterasi", "🔍 Pencarian", "📊 Statistik"])

    # Memuat data RDF (di-cache untuk performa).
    rdf_data = load_rdf_data()

    # Konten untuk Tab 1: Transliterasi
    with tab1:
        render_advanced_navigation()
        render_dual_pane_layout(st.session_state.page_num, rdf_data)
        render_export_panel()

    # Konten untuk Tab 2: Pencarian
    with tab2:
        render_enhanced_search(rdf_data)

    # Konten untuk Tab 3: Statistik
    with tab3:
        st.markdown("### 📊 Statistik Digitalisasi")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Halaman", "20", "100%")
        with col2:
            st.metric("Halaman Terdigitalisasi", "1", "5%")
        with col3:
            st.metric("Total Pengunjung", "1,234", "+12%")

        # Contoh grafik progres.
        st.markdown("**Progress Digitalisasi per Bulan:**")
        st.bar_chart({"Jan": 0, "Feb": 0, "Mar": 1, "Apr": 0})

    # --- ELEMEN HTML UNTUK LIGHTBOX ---
    # Struktur HTML untuk lightbox. Fungsionalitasnya dikontrol oleh assets/script.js.
    # Inline style dan onclick telah dihapus.
    st.markdown("""
        <div id="imageLightbox" class="lightbox">
            <span class="lightbox-close">&times;</span>
            <img class="lightbox-content" id="lightboxImage">
        </div>
    """, unsafe_allow_html=True)

    # Menutup container utama aplikasi.
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MEMUAT JAVASCRIPT EKSTERNAL ---
    # Memuat file JavaScript di akhir halaman.
    # Ini memastikan semua elemen HTML sudah ada sebelum skrip mencoba mengaksesnya.
    st.components.v1.html(f'<script>{load_asset("assets/script.js")}</script>', height=0)


if __name__ == "__main__":
    main()