import streamlit as st
import os
from rdflib import Graph

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Naskah Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
)

# --- CSS ARCHITECTURE & STYLING ---
# Mengikuti prinsip: Max 200 baris, CSS variables, mobile-first, WCAG compliance
st.markdown("""
<style>
    /* CSS Custom Properties untuk Theming yang Konsisten */
    :root {
        --primary-color: #8B4513;  /* SaddleBrown */
        --secondary-color: #2C3E50;/* Dark Blue-Gray */
        --accent-color: #E67E22;   /* Carrot Orange */
        --bg-color: #FDFEFE;       /* Latar belakang sangat terang */
        --font-color: #34495E;     /* Warna font utama */
        --light-gray: #ECF0F1;     /* Abu-abu terang untuk border/bg */
        --font-family: 'Georgia', 'serif';
        --line-height: 1.6;
    }

    /* General Body & Typography */
    .stApp { 
        background-color: var(--bg-color); 
    }
    h1, h2, h3 {
        color: var(--secondary-color);
        font-family: var(--font-family);
    }
    p, li, label {
        color: var(--font-color);
        font-family: var(--font-family);
        line-height: var(--line-height);
    }
    .block-container {
        padding: 1rem 2rem;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid var(--light-gray);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        display: block;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 0.5rem 0;
        transition: background-color 0.2s ease;
        border-left: 4px solid transparent;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background-color: var(--light-gray);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > div:has(input:checked) label {
        background-color: #EAE3DC; /* Warna coklat muda untuk background aktif */
        border-left: 4px solid var(--primary-color);
        font-weight: 700;
        color: var(--primary-color) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div > div:has(input:checked) label p {
        color: var(--primary-color) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] input {
        display: none;
    }

    /* Halaman Transliterasi */
    .image-container {
        position: sticky; /* Membuat gambar "menempel" saat scroll */
        top: 2rem;
    }
    .transliterasi-wrapper {
        height: 80vh; /* Tinggi panel utama */
        display: flex;
        flex-direction: column;
    }
    .transliterasi-content {
        overflow-y: auto;
        padding-right: 1rem;
    }
    .transliterasi-item {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--light-gray);
    }

    /* Pagination */
    .pagination-desktop { display: flex; }
    .pagination-mobile { display: none; }

    /* Halaman Pencarian */
    .search-result {
        border: 1px solid var(--light-gray);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .search-result:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .highlight {
        background-color: #FDEBD0; /* Highlight oranye muda */
        padding: 0 4px;
        border-radius: 3px;
    }

    /* Responsive Design - Mobile First */
    @media (max-width: 768px) {
        .block-container { padding: 1rem; }
        .pagination-desktop { display: none; }
        .pagination-mobile { display: block; }
        h1 { font-size: 2rem; }
    }
</style>
""", unsafe_allow_html=True)


# --- DATA LOADING & STATE MANAGEMENT ---
@st.cache_data
def load_rdf_data(ttl_file="naskah_bhakti_final.ttl"):
    """Memuat dan mem-parsing file TTL.
    Returns: List of dictionaries atau None jika gagal."""
    g = Graph()
    if not os.path.exists(ttl_file):
        st.error(f"File data '{ttl_file}' tidak ditemukan. Pastikan file berada di direktori yang benar.")
        return None
    try:
        g.parse(ttl_file, format="turtle")
        query = "..." # Query seperti sebelumnya
        results = g.query(query)
        return [{"uri": str(r.kalimat_uri), "latin": str(r.latin), "terjemahan": str(r.terjemahan)} for r in results]
    except Exception as e:
        st.error(f"Gagal mem-parsing file TTL: {e}")
        return None

# Initialize session state
if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# --- UI HELPER FUNCTIONS (SEPARATION OF CONCERNS) ---
def render_pagination(total_pages):
    """Menampilkan komponen navigasi halaman yang responsif."""
    
    # Navigasi Mobile (Dropdown)
    with st.expander("Navigasi Halaman"):
        st.selectbox(
            "Pilih Halaman",
            options=range(1, total_pages + 1),
            key="mobile_nav",
            on_change=lambda: st.session_state.update(page_num=st.session_state.mobile_nav)
        )

    # Navigasi Desktop (Next/Prev + Input)
    st.write("") # Memberi sedikit spasi
    prev_col, indicator_col, next_col, jump_col = st.columns([2, 3, 2, 3])
    
    if prev_col.button("⬅️ Sebelumnya", use_container_width=True, disabled=(st.session_state.page_num == 1)):
        st.session_state.page_num -= 1
        
    indicator_col.markdown(f"**Halaman {st.session_state.page_num} / {total_pages}**")

    if next_col.button("Selanjutnya ➡️", use_container_width=True, disabled=(st.session_state.page_num == total_pages)):
        st.session_state.page_num += 1

    jump_col.number_input(
        "Lompat ke", min_value=1, max_value=total_pages, 
        key="jump_nav",
        on_change=lambda: st.session_state.update(page_num=st.session_state.jump_nav)
    )

# --- MAIN APP LOGIC ---
# Data loaded once
rdf_data = load_rdf_data()
TOTAL_PAGES = 20

# Sidebar Navigation
with st.sidebar:
    st.header("Kakawin Ramayana")
    page = st.radio(
        "Navigasi", 
        ["📖 Transliterasi", "🔍 Pencarian", "ℹ️ Tentang Naskah"],
        key="nav_main"
    )
    st.markdown("---")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg/800px-Garin_Workshop_of_Character_Animation_-_Wayang_Kulit_Rama.jpg",
             caption="Sang Rama")

if rdf_data is None:
    st.warning("Aplikasi tidak dapat berjalan karena data naskah tidak berhasil dimuat.")
else:
    # Page Routing
    if page == "📖 Transliterasi":
        col1, col2 = st.columns([5, 6], gap="large") # Kolom gambar sedikit lebih kecil

        with col1:
            with st.container(border=False):
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.subheader(f"Tampilan Naskah Halaman {st.session_state.page_num}")
                image_path = os.path.join("images", f"page_{st.session_state.page_num}.png")
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.warning(f"Gambar 'page_{st.session_state.page_num}.png' tidak ditemukan.")
                
                render_pagination(TOTAL_PAGES)
                st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.subheader("Transliterasi & Terjemahan")
            st.markdown('<div class="transliterasi-wrapper">', unsafe_allow_html=True)
            st.markdown('<div class="transliterasi-content">', unsafe_allow_html=True)
            
            if st.session_state.page_num == 3:
                for item in rdf_data:
                    st.markdown(f"""
                    <div class="transliterasi-item">
                        <p><strong>Latin:</strong> <em>{item['latin']}</em></p>
                        <p><strong>Terjemahan:</strong> {item['terjemahan']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Data transliterasi untuk halaman ini belum tersedia.")
            
            st.markdown('</div></div>', unsafe_allow_html=True)

    elif page == "🔍 Pencarian":
        st.subheader("Pencarian Teks dalam Naskah")
        search_query = st.text_input("Cari kata kunci", placeholder="Cari dalam transliterasi atau terjemahan...")

        st.markdown("---")
        if not search_query:
            st.info("Masukkan kata kunci untuk memulai pencarian.")
        else:
            query_lower = search_query.lower()
            results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
            
            st.write(f"Menampilkan **{len(results)}** hasil untuk '{search_query}':")
            st.markdown("---")
            
            for item in results:
                # Highlight aringan
                display_latin = item['latin'].replace(search_query, f"<span class='highlight'>{search_query}</span>")
                display_terjemahan = item['terjemahan'].replace(search_query, f"<span class='highlight'>{search_query}</span>")

                with st.container():
                    st.markdown(f"""
                    <div class="search-result">
                        <p><strong>Latin:</strong> <em>{display_latin}</em></p>
                        <p><strong>Terjemahan:</strong> {display_terjemahan}</p>
                    </div>
                    """, unsafe_allow_html=True)

    elif page == "ℹ️ Tentang Naskah":
        st.subheader("Tentang Naskah Kakawin Ramayana")
        # Konten halaman "Tentang Naskah" seperti sebelumnya