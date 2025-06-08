// assets/script.js - Versi yang Ditingkatkan dan Terintegrasi

/**
 * Menjalankan semua skrip setelah Document Object Model (DOM) selesai dimuat.
 * Ini memastikan semua elemen HTML sudah ada sebelum kita coba memanipulasinya.
 */
document.addEventListener('DOMContentLoaded', function() {

    // --- VARIABEL GLOBAL & SELEKTOR ELEMEN ---
    const lightbox = document.getElementById('imageLightbox');
    const lightboxImg = document.getElementById('lightboxImage');
    const manuscriptImage = document.getElementById('manuscriptImage');
    const closeBtn = document.querySelector('.lightbox-close');

    // Tombol Kontrol Gambar
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const downloadBtn = document.getElementById('downloadBtn');

    // Variabel untuk melacak skala zoom
    let currentScale = 1.0;
    const scaleStep = 0.2; // Seberapa besar perubahan zoom setiap kali diklik

    // --- FUNGSI LIGHTBOX ---

    /**
     * Membuka lightbox dan menampilkan gambar yang diklik.
     * @param {string} src - URL sumber dari gambar yang akan ditampilkan.
     */
    function openLightbox(src) {
        if (lightbox && lightboxImg) {
            lightbox.style.display = 'block';
            lightboxImg.src = src;
        }
    }

    /**
     * Menutup lightbox.
     */
    function closeLightbox() {
        if (lightbox) {
            lightbox.style.display = 'none';
        }
    }

    // --- FUNGSI KONTROL GAMBAR ---

    /**
     * Memperbesar gambar naskah.
     */
    function zoomIn() {
        if (manuscriptImage) {
            currentScale += scaleStep;
            manuscriptImage.style.transform = `scale(${currentScale})`;
        }
    }

    /**
     * Memperkecil gambar naskah.
     */
    function zoomOut() {
        if (manuscriptImage) {
            // Batasi agar tidak terlalu kecil
            currentScale = Math.max(0.6, currentScale - scaleStep);
            manuscriptImage.style.transform = `scale(${currentScale})`;
        }
    }

    /**
     * Mengunduh gambar naskah yang sedang ditampilkan.
     */
    function downloadImage() {
        if (manuscriptImage) {
            const link = document.createElement('a');
            link.href = manuscriptImage.src;
            // Memberi nama file yang unik berdasarkan waktu
            link.download = `kakawin_ramayana_page_${new Date().getTime()}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }


    // --- EVENT LISTENER UTAMA ---
    // Bagian ini "menghidupkan" tombol dan elemen interaktif.

    // 1. Event listener untuk gambar naskah -> membuka lightbox
    if (manuscriptImage) {
        manuscriptImage.onclick = function() {
            openLightbox(this.src);
        };
    }

    // 2. Event listener untuk tombol close pada lightbox
    if (closeBtn) {
        closeBtn.onclick = function() {
            closeLightbox();
        };
    }

    // 3. Event listener untuk menutup lightbox saat mengklik area gelap di sekitarnya
    if (lightbox) {
        lightbox.onclick = function(event) {
            // Pastikan yang diklik adalah latar belakang, bukan gambarnya
            if (event.target === lightbox) {
                closeLightbox();
            }
        };
    }

    // 4. Event listener untuk tombol-tombol kontrol gambar
    if (zoomInBtn) {
        zoomInBtn.onclick = zoomIn;
    }
    if (zoomOutBtn) {
        zoomOutBtn.onclick = zoomOut;
    }
    if (downloadBtn) {
        downloadBtn.onclick = downloadImage;
    }

});