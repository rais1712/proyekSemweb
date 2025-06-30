# 🌸 Digitalisasi dan Eksplorasi Semantik Kakawin Ramayana

Proyek ini adalah sebuah **portal web interaktif** yang dibangun menggunakan teknologi **web semantik** untuk menjelajahi naskah kuno *Kakawin Ramayana*. Aplikasi ini memungkinkan pengguna:

- Melihat gambar naskah asli
- Membaca transliterasi teks Latin
- Memahami terjemahannya dalam Bahasa Indonesia
- Melakukan pencarian teks yang efisien

> Dibuat untuk memenuhi tugas mata kuliah **Web Semantik** di Program Studi Teknik Informatika, Universitas Padjadjaran.

---

## ✨ Fitur Utama

- **📖 Penampil Naskah Terpadu**  
  Menampilkan gambar naskah berdampingan dengan transliterasi dan terjemahan per halaman.
  
- **➡️ Navigasi Halaman**  
  Tombol ◀ dan ▶ untuk berpindah antar halaman naskah.

- **🔍 Pencarian Teks Cerdas**  
  Pencarian kata kunci pada transliterasi dan terjemahan naskah.

- **💻 Antarmuka Web Modern**  
  Dibuat menggunakan Streamlit, ringan dan mudah digunakan.

---

## 🛠️ Teknologi yang Digunakan

| Komponen        | Teknologi                       |
|-------------    |---------------------------------|
| Frontend        | Streamlit                       |
| Backend         | Python                          |
| Database        | Apache Jena Fuseki              |
| Pemodelan Data  | RDF (Turtle `.ttl`)             |
| Kueri           | SPARQL via `SPARQLWrapper`      |

---

## 🗂️ Struktur Proyek

````
├── assets/
│   ├── style.css          # Styling antarmuka
│   └── script.js          # Script tambahan (opsional)
├── images/
│   ├── page\_1.png         # Gambar naskah per halaman
│   └── ...
├── naskah\_bhakti\_final.ttl # File RDF utama
├── semweb.py              # Aplikasi utama Streamlit
├── requirements.txt       # Daftar dependensi
└── README.md              # Dokumen ini

````

---

## ⚙️ Panduan Instalasi

### 1. Prasyarat

Pastikan perangkat Anda sudah terpasang:

- Python 3.7+
- Java 17+ (**penting untuk Apache Jena Fuseki**)
- Git (opsional)

### 2. Clone Repositori

```bash
git clone <URL_REPOSITORI_ANDA>
cd <NAMA_FOLDER_PROYEK>
````

### 3. Instalasi Dependensi Python

```bash
pip install -r requirements.txt
```

---

## 🔧 Konfigurasi Apache Jena Fuseki

1. **Unduh Fuseki** dari [https://jena.apache.org/download/index.cgi](https://jena.apache.org/download/index.cgi)
2. **Ekstrak** file ZIP
3. **Jalankan Server**:

```bash
# Linux / macOS
./fuseki-server

# Windows
fuseki-server.bat
```

4. Akses antarmuka di: [http://localhost:3030](http://localhost:3030)

5. **Buat Dataset**:

* Klik "New Dataset"
* Nama: `kakawin`
* Tipe: `Persistent (TDB2)`
* Klik **Create Dataset**

6. **Upload Data**:

* Pilih dataset `kakawin`
* Masuk ke tab `Upload Data`
* Upload file `naskah_bhakti_final.ttl`

---

## 🚀 Menjalankan Aplikasi

1. Pastikan server Fuseki telah berjalan
2. Jalankan aplikasi:

```bash
streamlit run semweb.py
```

3. Akses aplikasi di: [http://localhost:8501](http://localhost:8501)

---

## 📚 Panduan Penggunaan

### Sidebar

* **Transliterasi & Naskah**
  Menampilkan naskah asli, transliterasi Latin, dan terjemahan. Navigasi antar halaman tersedia.

* **Pencarian**
  Ketik kata kunci, hasil relevan akan ditampilkan lengkap dengan highlight.

* **Tentang Naskah**
  Informasi sejarah dan konteks Kakawin Ramayana.

---

## 🧠 Model Data RDF

Contoh representasi RDF (Turtle):

```turtle
@prefix jawa: <http://example.org/jawa#> .

jawa:kalimat_1 a jawa:Kalimat ;
    jawa:latin "Hana sira ratu dibya rĕngön," ;
    jawa:terjemahan "Ada seorang raja yang agung, dengarkanlah," ;
    jawa:halaman "1"^^xsd:integer ;
    jawa:bagianDari jawa:cerita_1 .
```

---

## 📌 Arsitektur Aplikasi

1. **Data disimpan** dalam file `.ttl` dan diunggah ke dataset `kakawin` di Fuseki.
2. **Antarmuka pengguna** dibuat dengan Streamlit.
3. **Kueri SPARQL** dikirim ke endpoint Fuseki (`http://localhost:3030/kakawin/query`).
4. **Hasil kueri** ditampilkan secara dinamis (JSON → Streamlit).

---

## 🧑‍💻 Tim Pengembang

* **Ecki Fawwaz** (140810220063)
* **Rais Abiyyu Putra** (140810220069)
* **Novem Romadhofi Kika** (140810220083)

---

