# Digitalisasi dan Eksplorasi Semantik Kakawin Ramayana

Sebuah portal web interaktif yang dibangun menggunakan teknologi web semantik untuk menjelajahi naskah kuno Kakawin Ramayana. Proyek ini memungkinkan pengguna untuk melihat gambar naskah asli, membaca transliterasi teks Latin, memahami terjemahannya dalam Bahasa Indonesia, serta melakukan pencarian teks secara efisien.

Aplikasi ini dikembangkan sebagai bagian dari proyek mata kuliah Web Semantik.

## Fitur Utama

-   **Penampil Naskah Terpadu**: Menampilkan gambar naskah asli berdampingan dengan data transliterasi dan terjemahan per halaman.
-   **Navigasi Halaman**: Antarmuka yang mudah digunakan untuk berpindah antar halaman naskah dengan tombol navigasi dan indikator kemajuan.
-   **Pencarian Teks Cerdas**: Fitur pencarian kata kunci pada seluruh data teks (transliterasi dan terjemahan).
-   **Antarmuka Web Modern**: Dibangun dengan Streamlit untuk pengalaman pengguna yang responsif dan modern.

## Teknologi yang Digunakan

-   **Frontend**: Streamlit
-   **Backend**: Python
-   **Database**: Apache Jena Fuseki (sebagai RDF Triplestore)
-   **Pemodelan Data**: RDF dengan sintaks Turtle (`.ttl`)
-   **Interaksi Kueri**: SPARQLWrapper

## Panduan Instalasi dan Penyiapan

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

### Langkah 1: Prasyarat

Pastikan perangkat Anda telah terinstal:
-   **Python 3.7+**
-   [cite_start]**Java 17+**: Sangat penting, karena Apache Jena Fuseki versi terbaru memerlukannya. Anda bisa cek versi dengan `java -version`.
-   **Git** (opsional, jika Anda ingin *clone* repositori).

### Langkah 2: Dapatkan File Proyek

Unduh atau *clone* repositori ini ke mesin lokal Anda:
```bash
git clone <URL_REPOSITORI_ANDA>
cd <NAMA_FOLDER_PROYEK>
Langkah 3: Instalasi Dependensi Python
Buka terminal di direktori proyek dan jalankan perintah berikut untuk menginstal semua pustaka yang diperlukan:

Bash

pip install -r requirements.txt
Langkah 4: Siapkan Apache Jena Fuseki
Unduh Fuseki: Kunjungi situs resmi Apache Jena dan unduh Apache Jena Fuseki.
Ekstrak File: Ekstrak file ZIP/TAR yang telah diunduh ke lokasi yang mudah diakses.
Jalankan Server Fuseki:
Buka terminal atau Command Prompt.
Navigasikan ke dalam direktori Fuseki yang telah diekstrak. Contoh:
Bash

cd C:\path\to\your\apache-jena-fuseki-5.4.0
Jalankan server dengan perintah:
Bash

./fuseki-server # Untuk Linux/macOS
# atau
fuseki-server.bat # Untuk Windows
Buat Dataset:
Buka browser dan akses http://localhost:3030.
Klik "New Dataset".
Beri nama dataset: kakawin.
Pilih tipe dataset: "Persistent (TDB2)".
Klik "Create Dataset".
Unggah Data RDF:
Klik nama dataset kakawin yang baru saja Anda buat.
Pilih tab "upload data".
Klik "Select Files..." dan pilih file naskah_bhakti_final.ttl dari direktori proyek Anda.
Klik "upload". Data naskah kini siap diakses.
Cara Menjalankan Aplikasi
Pastikan server Fuseki Anda sudah berjalan dari langkah sebelumnya.

Buka Terminal Baru: Buka jendela terminal atau Command Prompt yang baru.
Navigasi ke Direktori Proyek: Arahkan terminal ke folder tempat semweb.py berada.
Jalankan Aplikasi Streamlit: Eksekusi perintah berikut:
Bash

streamlit run semweb.py

Akses Aplikasi: Aplikasi akan otomatis terbuka di browser Anda pada alamat http://localhost:8501.
Panduan Penggunaan Aplikasi
Sidebar: Gunakan sidebar di sebelah kiri untuk berpindah antara tiga menu utama:
Transliterasi & Naskah: Halaman utama untuk melihat naskah dan teksnya. Gunakan tombol ◀ dan ▶ untuk navigasi halaman.
Pencarian: Masukkan kata kunci untuk mencari teks di seluruh naskah.
Tentang Naskah: Membaca informasi latar belakang mengenai Kakawin Ramayana.
Halaman Transliterasi: Di halaman ini, Anda akan melihat gambar naskah di sebelah kiri dan daftar transliterasi serta terjemahannya di sebelah kanan.
Halaman Pencarian: Ketik kata atau frasa yang ingin Anda cari. Hasil akan ditampilkan secara dinamis di bawahnya, lengkap dengan teks Latin, terjemahan, dan sorotan pada kata kunci yang cocok.
Struktur Proyek
.
├── assets/
│   ├── style.css         # File styling untuk antarmuka
│   └── script.js         # File JavaScript (jika ada fungsionalitas tambahan)
├── images/
│   ├── page_1.png        # Gambar naskah halaman 1
│   └── ...               # Gambar naskah halaman lainnya
├── naskah_bhakti_final.ttl # File data RDF utama
├── semweb.py               # Kode utama aplikasi Streamlit
├── requirements.txt      # Daftar dependensi Python
└── README.md             # File panduan ini
Tim Pengembang
Proyek ini dikembangkan oleh:

Ecki Fawwaz (140810220063) 
Rais ABiyyu Putra (140810220069) 
Novem romadhofi Kika (140810220083)
