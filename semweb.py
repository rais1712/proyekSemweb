import streamlit as st
from rdflib import Graph
import os

# --- KONFIGURASI HALAMAN & GAYA (CSS) ---
st.set_page_config(
    page_title="Naskah Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
)

# CSS Kustom untuk layout, sidebar ramping, dan tombol halaman
st.markdown("""
<style>
    /* Mengubah warna latar belakang utama */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Membuat sidebar lebih ramping */
    [data-testid="stSidebar"] > div:first-child {
        width: 250px;
    }

    /* Menghilangkan padding atas agar judul lebih nempel ke atas */
    .block-container {
        padding-top: 2rem;
    }

    /* Gaya untuk panel utama */
    .panel {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 70vh; /* Tinggi panel agar konsisten */
        overflow-y: auto; /* Tambahkan scroll jika konten panjang */
    }
    .panel-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2a5298;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- FUNGSI HELPER ---
@st.cache_data
def load_rdf_data(ttl_file):
    """Memuat data dari file TTL dan mengubahnya jadi list of dictionary."""
    g = Graph()
    try:
        g.parse(ttl_file, format="turtle")
        query = """
        PREFIX jawa: <http://example.org/jawa#>
        SELECT ?kalimat_uri ?latin ?terjemahan
        WHERE { ?kalimat_uri a jawa:Kalimat ; jawa:latin ?latin ; jawa:terjemahan ?terjemahan . }
        ORDER BY ?kalimat_uri
        """
        results = g.query(query)
        data = [{"uri": str(r.kalimat_uri), "latin": str(r.latin), "terjemahan": str(r.terjemahan)} for r in results]
        return data
    except Exception as e:
        st.error(f"Gagal memuat atau mem-parsing file TTL: {e}")
        return []

# --- Memuat Data Sekali di Awal ---
rdf_data = load_rdf_data("naskah_bhakti_final.ttl")

# --- UI UTAMA APLIKASI ---

# 1. Judul di header kiri atas
st.title("Naskah Kakawin Ramayana")

# Navigasi di Sidebar
with st.sidebar:
    # Menggunakan markdown untuk memberi sedikit ruang di atas
    st.markdown("##") 
    page = st.radio("Pilih Halaman", ["📖 Transliterasi", "🔍 Pencarian"])
    st.markdown("---")

# Inisialisasi session state untuk halaman
if 'page_num' not in st.session_state:
    st.session_state.page_num = 1

# Logika untuk setiap halaman
if page == "📖 Transliterasi":
    # 2. Tombol Halaman (Pagination)
    st.write("Pilih Halaman:")
    # Membuat 4 baris tombol, masing-masing 5 tombol
    for i in range(4):
        cols = st.columns(5)
        for j in range(5):
            page_index = i * 5 + j + 1
            with cols[j]:
                if st.button(f"{page_index}", key=f"page_{page_index}", use_container_width=True):
                    st.session_state.page_num = page_index
    
    st.markdown("---")
    
    st.header(f"Naskah Halaman {st.session_state.page_num}")
    
    col1, col2 = st.columns(2, gap="large")

    # Panel Kiri: Gambar Naskah Asli
    with col1:
        st.markdown('<div class="panel-title">Naskah Asli</div>', unsafe_allow_html=True)
        # 6. Menggunakan gambar yang diupload manual
        image_path = os.path.join("images", f"page_{st.session_state.page_num}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning(f"Gambar 'page_{st.session_state.page_num}.png' tidak ditemukan di folder 'images/'.")

    # Panel Kanan: Transliterasi & Terjemahan
    with col2:
        st.markdown('<div class="panel-title">Transliterasi & Terjemahan</div>', unsafe_allow_html=True)
        
        # 7. Menampilkan data TTL hanya di halaman 3
        if st.session_state.page_num == 3:
            # 5. Menampilkan semua 8 bait di halaman 3
            if not rdf_data:
                st.warning("Data RDF tidak berhasil dimuat.")
            else:
                for item in rdf_data:
                    st.markdown(f"**Latin:**\n> *{item['latin']}*")
                    st.markdown(f"**Terjemahan:**\n> {item['terjemahan']}")
                    st.markdown("---")
        else:
            st.info("Data transliterasi untuk halaman ini belum tersedia.")

elif page == "🔍 Pencarian":
    st.header("🔍 Pencarian Teks dalam Naskah")
    search_query = st.text_input("Cari kata kunci dalam data yang tersedia", placeholder="Contoh: rama, bhakti, prajurit...")

    if search_query:
        query_lower = search_query.lower()
        # Pencarian hanya akan efektif pada data yang ada (saat ini hanya di hal. 3)
        results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
        
        st.markdown("---")
        st.subheader(f"Ditemukan {len(results)} hasil untuk '{search_query}'")
        
        for item in results:
            st.markdown(f"""
            <div style="background-color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 5px solid #1e3c72;">
                <p><strong>Lokasi:</strong> Halaman 3</p>
                <p><strong>Latin:</strong><br><em>{item['latin']}</em></p>
                <p><strong>Terjemahan:</strong><br>{item['terjemahan']}</p>
            </div>
            """, unsafe_allow_html=True)