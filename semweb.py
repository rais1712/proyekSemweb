import streamlit as st
import os
from rdflib import Graph
import streamlit.components.v1 as components

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Naskah Kakawin Ramayana",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GAYA CSS & TAMPILAN ---
# Menambahkan gaya untuk kontainer yang bisa di-scroll dan perbaikan lainnya
st.markdown("""
<style>
    /* Gaya untuk membungkus konten utama agar tidak terlalu lebar di layar besar */
    .main-container {
        max-width: 1200px;
        margin: auto;
    }

    /* Gaya untuk kontainer transliterasi yang dapat di-scroll */
    .transliterasi-container {
        background-color: #f8f9fa; /* Warna latar sedikit berbeda */
        border: 1px solid #e9ecef; /* Border tipis */
        border-radius: 8px;
        padding: 1rem;
        height: 70vh; /* Tinggi tetap untuk kontainer */
        overflow-y: auto; /* Scroll vertikal otomatis jika konten melebihi tinggi */
    }
    
    .transliterasi-item {
        padding-bottom: 1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #ddd;
    }
    
    .transliterasi-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }

    .latin-text {
        font-family: 'Georgia', serif;
        font-style: italic;
        font-size: 1.1rem;
        color: #2C3E50;
        margin-bottom: 0.5rem;
    }

    .translation-text {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #2C3E50;
    }

    /* Gaya untuk gambar agar ukurannya lebih konsisten */
    .manuscript-image-container {
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .manuscript-image-container img {
        width: 100%;
        border-radius: 4px;
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
        
        # Query SPARQL untuk mengambil semua data kalimat
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
    
    # Memulai kontainer yang bisa di-scroll
    st.markdown('<div class="transliterasi-container">', unsafe_allow_html=True)
    
    for item in data:
        st.markdown(f"""
        <div class="transliterasi-item">
            <div class="latin-text">{item['latin']}</div>
            <div class="translation-text"><strong>Terjemahan:</strong> {item['terjemahan']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Menutup kontainer
    st.markdown('</div>', unsafe_allow_html=True)

def render_search_results(results, query):
    """Menampilkan hasil pencarian dengan format yang lebih baik."""
    if not results:
        st.info("Tidak ada hasil yang cocok ditemukan.")
        return
    
    st.success(f"Ditemukan {len(results)} hasil untuk '{query}'")
    
    # Menggunakan kontainer yang sama dengan halaman transliterasi
    st.markdown('<div class="transliterasi-container">', unsafe_allow_html=True)
    
    highlight_class = "background-color: #FDEBD0; padding: 0 4px; border-radius: 3px;"
    for item in results:
        latin_highlighted = item['latin'].replace(query, f"<span style='{highlight_class}'>{query}</span>")
        translation_highlighted = item['terjemahan'].replace(query, f"<span style='{highlight_class}'>{query}</span>")
        
        st.markdown(f"""
        <div class="transliterasi-item">
            <div class="latin-text">{latin_highlighted}</div>
            <div class="translation-text"><strong>Terjemahan:</strong> {translation_highlighted}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def render_about_page():
    st.markdown("""
    ## Sejarah Naskah
    **Kakawin Ramayana** adalah salah satu karya sastra Jawa Kuno yang paling penting, diperkirakan ditulis pada abad ke-9 atau ke-10 Masehi. Naskah ini merupakan adaptasi dari epos Ramayana Sanskrit karya Valmiki, namun diresapi dengan nilai-nilai, budaya, dan bahasa lokal Jawa Kuno.
    
    ### Karakteristik Utama:
    - **Bahasa**: Jawa Kuno (Kawi)
    - **Bentuk**: Puisi Kakawin (memiliki aturan metrum yang ketat)
    - **Periode**: Kerajaan Medang (Mataram Kuno)
    - **Isi**: Mengisahkan perjalanan hidup Sang Rama dalam mencari dan menyelamatkan istrinya, Sita, dengan nuansa filosofis Hindu-Jawa yang kental.

    ## Tentang Proyek Digitalisasi Ini
    Proyek ini bertujuan untuk melestarikan warisan budaya takbenda ini dan membuatnya lebih mudah diakses oleh para peneliti, mahasiswa, serta masyarakat umum melalui teknologi digital.
    
    ### Teknologi yang Digunakan:
    - **RDF (Resource Description Framework)**: Data naskah distrukturkan secara semantik menggunakan format Turtle (`.ttl`) untuk mendefinisikan hubungan antar entitas seperti cerita, kalimat, dan terjemahan.
    - **Streamlit**: Kerangka kerja Python yang digunakan untuk membangun antarmuka web interaktif ini dengan cepat.
    - **Python**: Bahasa pemrograman utama yang digunakan untuk memproses data RDF dan menjalankan aplikasi.
    """)

def render_visualization_page():
    """Menampilkan halaman visualisasi RDF dari file HTML."""
    try:
        with open("visualization.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            components.html(html_content, height=620, scrolling=False)
    except FileNotFoundError:
        st.error("File 'visualization.html' tidak ditemukan. Pastikan file tersebut berada di direktori yang sama dengan `semweb.py`.")
    except Exception as e:
        st.error(f"Gagal memuat halaman visualisasi: {e}")

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
            ["📖 Transliterasi", "🔍 Pencarian", "🕸️ Visualisasi RDF", "ℹ️ Tentang Naskah"],
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
    
    # Memuat data sekali saja
    rdf_data = load_rdf_data()
    if rdf_data is None:
        st.stop() # Menghentikan eksekusi jika data gagal dimuat

    # --- Routing Halaman ---
    if page == "📖 Transliterasi":
        st.header("Transliterasi & Terjemahan Naskah")
        
        # Layout dua kolom: Kiri untuk gambar, Kanan untuk teks
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

            # Kontrol navigasi di bawah gambar
            TOTAL_PAGES = 20
            nav_cols = st.columns([2, 1, 2])
            if nav_cols[0].button("← Sebelumnya", use_container_width=True, disabled=(st.session_state.page_num == 1)):
                st.session_state.page_num -= 1
                st.rerun()
            
            nav_cols[1].markdown(f"<div style='text-align: center; margin-top: 0.5rem;'>{st.session_state.page_num}/{TOTAL_PAGES}</div>", unsafe_allow_html=True)
            
            if nav_cols[2].button("Selanjutnya →", use_container_width=True, disabled=(st.session_state.page_num == TOTAL_PAGES)):
                st.session_state.page_num += 1
                st.rerun()

        with col2:
            st.subheader("Teks & Terjemahan")
            if st.session_state.page_num == 3:
                # Menampilkan data yang tersedia untuk halaman 3
                render_transliterasi_content(rdf_data)
            else:
                st.info(f"Data transliterasi untuk halaman {st.session_state.page_num} sedang dalam proses digitalisasi.")

    elif page == "🔍 Pencarian":
        st.header("Pencarian Teks")
        
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

    elif page == "🕸️ Visualisasi RDF":
        st.header("Visualisasi Hubungan Data RDF")
        st.markdown("Graf berikut memvisualisasikan hubungan antara entitas cerita utama dengan setiap kalimat yang menjadi bagiannya, sesuai dengan data pada file `naskah_bhakti_final.ttl`.")
        render_visualization_page()

    elif page == "ℹ️ Tentang Naskah":
        st.header("Tentang Naskah Kakawin Ramayana")
        render_about_page()
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()