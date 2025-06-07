<<<<<<< HEAD
import streamlit as st
from rdflib import Graph
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

# --- KONFIGURASI HALAMAN & GAYA (CSS) ---
st.set_page_config(
    page_title="Kakawin Semantik",
    page_icon="📜",
    layout="wide",
)

# CSS Kustom untuk layout ala Google Translate dan warna baru
st.markdown("""
<style>
    /* Mengubah warna latar belakang utama */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Kustomisasi sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    /* Gaya untuk panel utama */
    .panel {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 75vh; /* Tinggi panel agar konsisten */
        overflow-y: auto; /* Tambahkan scroll jika konten panjang */
    }
    .panel-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3c72; /* Warna biru tua untuk judul */
        margin-bottom: 1rem;
        border-bottom: 2px solid #2a5298;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- FUNGSI HELPER (DENGAN CACHING UNTUK PERFORMA) ---

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

@st.cache_data
def create_visualization(_data):
    """Membuat visualisasi jaringan sederhana dari data yang ada."""
    net = Network(height="600px", width="100%", bgcolor="#f0f2f6", font_color="#333333", directed=True)
    g = Graph()
    try:
        g.parse("naskah_bhakti_final.ttl", format="turtle")
        
        cerita_query = g.query("PREFIX jawa: <http://example.org/jawa#> SELECT ?uri ?judul WHERE { ?uri a jawa:Cerita; jawa:judul ?judul . }")
        cerita_uri, cerita_judul = next(iter(cerita_query))
        
        net.add_node(str(cerita_uri), label=str(cerita_judul), color="#e63946", size=30, shape="star", title="Cerita Utama")
        
        for item in _data:
            kalimat_id = item['uri'].split('#')[-1]
            net.add_node(item['uri'], label=kalimat_id, color="#457b9d", title=item['latin'])
            net.add_edge(str(cerita_uri), item['uri'], color="#a8dadc")
            
        vis_path = "visualization.html"
        net.save_graph(vis_path)
        return vis_path
    except Exception as e:
        st.warning(f"Gagal membuat visualisasi: {e}")
        return None


# --- Memuat Data Sekali di Awal ---
rdf_data = load_rdf_data("naskah_bhakti_final.ttl")

# --- UI UTAMA APLIKASI ---

# Navigasi di Sidebar
with st.sidebar:
    st.title("📜 Kakawin Semantik")
    page = st.radio("Pilih Halaman", ["📖 Transliterasi", "🔍 Pencarian", "🕸️ Visualisasi"])
    st.markdown("---")
    
    # Menempatkan slider halaman di sidebar hanya jika halaman Transliterasi dipilih
    page_num = 1
    if page == "📖 Transliterasi":
        page_num = st.slider("Pilih Halaman Naskah", min_value=1, max_value=20, value=1, step=1)

# Logika untuk setiap halaman
if page == "📖 Transliterasi":
    st.header(f"Naskah Halaman {page_num}")
    
    col1, col2 = st.columns(2, gap="large")

    # Panel Kiri: Gambar Naskah Asli
    with col1:
        st.markdown('<div class="panel-title">Naskah Asli</div>', unsafe_allow_html=True)
        image_path = os.path.join("images", f"page_{page_num}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True) # <-- PERBAIKAN DI SINI
        else:
            st.warning(f"File gambar 'page_{page_num}.png' tidak ditemukan di folder 'images/'.")

    # Panel Kanan: Transliterasi & Terjemahan
    with col2:
        st.markdown('<div class="panel-title">Transliterasi & Terjemahan</div>', unsafe_allow_html=True)
        
        # Asumsi 4 kalimat per halaman untuk demo
        start_index = (page_num - 1) * 4
        end_index = start_index + 4
        page_data = rdf_data[start_index:end_index]

        if not page_data:
            st.info("Tidak ada data transliterasi untuk halaman ini atau halaman terakhir.")
        else:
            for item in page_data:
                st.markdown(f"**Latin:**\n> *{item['latin']}*")
                st.markdown(f"**Terjemahan:**\n> {item['terjemahan']}")
                st.markdown("---")

elif page == "🔍 Pencarian":
    st.header("🔍 Pencarian Teks dalam Naskah")
    search_query = st.text_input("Cari kata kunci", placeholder="Contoh: rama, bhakti, prajurit...")

    if search_query:
        query_lower = search_query.lower()
        results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
        
        st.markdown("---")
        st.subheader(f"Ditemukan {len(results)} hasil untuk '{search_query}'")
        
        for item in results:
            st.markdown(f"""
            <div style="background-color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 5px solid #1e3c72;">
                <p><strong>Latin:</strong><br><em>{item['latin']}</em></p>
                <p><strong>Terjemahan:</strong><br>{item['terjemahan']}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "🕸️ Visualisasi":
    st.header("🕸️ Visualisasi Jaringan Semantik")
    st.markdown("Grafik ini menunjukkan hubungan antara cerita utama dengan kalimat-kalimatnya.")
    
    with st.spinner("Menggambar grafik..."):
        vis_path = create_visualization(rdf_data)
        if vis_path:
            with open(vis_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=610, scrolling=True)
=======
import streamlit as st
from rdflib import Graph
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

# --- KONFIGURASI HALAMAN & GAYA (CSS) ---
st.set_page_config(
    page_title="Kakawin Semantik",
    page_icon="📜",
    layout="wide",
)

# CSS Kustom untuk layout ala Google Translate dan warna baru
st.markdown("""
<style>
    /* Mengubah warna latar belakang utama */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Kustomisasi sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    /* Gaya untuk panel kiri dan kanan */
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
        color: #1e3c72; /* Warna biru tua untuk judul */
        margin-bottom: 1rem;
        border-bottom: 2px solid #2a5298;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# --- FUNGSI HELPER (DENGAN CACHING UNTUK PERFORMA) ---

@st.cache_data
def load_rdf_data(ttl_file):
    """Memuat data dari file TTL dan mengubahnya jadi list of dictionary."""
    g = Graph()
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

@st.cache_data
def create_visualization(_data):
    """Membuat visualisasi jaringan sederhana dari data yang ada."""
    net = Network(height="600px", width="100%", bgcolor="#f0f2f6", font_color="#333333", directed=True)
    g = Graph()
    g.parse("naskah_bhakti_final.ttl", format="turtle")
    
    cerita_uri, cerita_judul = next(iter(g.query("PREFIX jawa: <http://example.org/jawa#> SELECT ?uri ?judul WHERE { ?uri a jawa:Cerita; jawa:judul ?judul . }")))
    
    net.add_node(str(cerita_uri), label=str(cerita_judul), color="#e63946", size=30, shape="star", title="Cerita Utama")
    
    for item in _data:
        kalimat_id = item['uri'].split('#')[-1]
        net.add_node(item['uri'], label=kalimat_id, color="#457b9d", title=item['latin'])
        net.add_edge(str(cerita_uri), item['uri'], color="#a8dadc")
        
    vis_path = "visualization.html"
    net.save_graph(vis_path)
    return vis_path

# --- Memuat Data Sekali di Awal ---
rdf_data = load_rdf_data("naskah_bhakti_final.ttl")

# --- UI UTAMA APLIKASI ---

# Navigasi di Sidebar
with st.sidebar:
    st.title("📜 Kakawin Semantik")
    page = st.radio("Pilih Halaman", ["📖 Transliterasi", "🔍 Pencarian", "🕸️ Visualisasi"])
    st.markdown("---")
    # Pindah slider halaman ke sidebar agar lebih bersih
    page_num = st.slider("Pilih Halaman Naskah", min_value=1, max_value=20, value=1, step=1)

# Logika untuk setiap halaman
if page == "📖 Transliterasi":
    st.header(f"Naskah Halaman {page_num}")
    
    col1, col2 = st.columns(2, gap="large")

    # Panel Kiri: Gambar Naskah Asli
    with col1:
        st.markdown('<div class="panel-title">Naskah Asli</div>', unsafe_allow_html=True)
        image_path = os.path.join("images", f"page_{page_num}.png")
        if os.path.exists(image_path):
            st.image(image_path, use_column_width=True)
        else:
            st.warning(f"File gambar 'page_{page_num}.png' tidak ditemukan di folder 'images/'.")

    # Panel Kanan: Transliterasi & Terjemahan
    with col2:
        st.markdown('<div class="panel-title">Transliterasi & Terjemahan</div>', unsafe_allow_html=True)
        # Asumsi 4 kalimat per halaman untuk demo
        start_index = (page_num - 1) * 4
        end_index = start_index + 4
        page_data = rdf_data[start_index:end_index]

        if not page_data:
            st.info("Tidak ada data transliterasi untuk halaman ini.")
        else:
            for item in page_data:
                st.markdown(f"**Latin:**\n> *{item['latin']}*")
                st.markdown(f"**Terjemahan:**\n> {item['terjemahan']}")
                st.markdown("---")

elif page == "🔍 Pencarian":
    st.header("🔍 Pencarian Teks dalam Naskah")
    search_query = st.text_input("Cari kata kunci", placeholder="Contoh: rama, bhakti, prajurit...")

    if search_query:
        query_lower = search_query.lower()
        results = [item for item in rdf_data if query_lower in item['latin'].lower() or query_lower in item['terjemahan'].lower()]
        
        st.markdown("---")
        st.subheader(f"Ditemukan {len(results)} hasil untuk '{search_query}'")
        
        for item in results:
            st.markdown(f"""
            <div style="background-color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 5px solid #1e3c72;">
                <p><strong>Latin:</strong><br><em>{item['latin']}</em></p>
                <p><strong>Terjemahan:</strong><br>{item['terjemahan']}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "🕸️ Visualisasi":
    st.header("🕸️ Visualisasi Jaringan Semantik")
    st.markdown("Grafik ini menunjukkan hubungan antara cerita utama dengan kalimat-kalimatnya.")
    
    with st.spinner("Menggambar grafik..."):
        vis_path = create_visualization(rdf_data)
        with open(vis_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=610, scrolling=True)
>>>>>>> b601046522298730404d808ea7943c073a6e2d47
