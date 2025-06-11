// assets/script.js - Versi Disederhanakan (Juni 2025)

document.addEventListener('DOMContentLoaded', function() {

    // --- SELEKTOR ELEMEN ---
    const lightbox = document.getElementById('imageLightbox');
    const lightboxImg = document.getElementById('lightboxImage');
    const manuscriptImage = document.getElementById('manuscriptImage');
    const closeLightboxBtn = document.querySelector('.lightbox-close');

    // --- FUNGSI LIGHTBOX ---
    function openLightbox(src) {
        if (lightbox && lightboxImg) {
            lightbox.style.display = 'block';
            lightboxImg.src = src;
        }
    }

    function closeLightbox() {
        if (lightbox) {
            lightbox.style.display = 'none';
        }
    }
    
    // --- EVENT LISTENERS ---

    // 1. Event listener untuk gambar naskah -> membuka lightbox
    if (manuscriptImage) {
        manuscriptImage.addEventListener('click', function() {
            openLightbox(this.src);
        });
    }

    // 2. Event listener untuk tombol close pada lightbox
    if (closeLightboxBtn) {
        closeLightboxBtn.addEventListener('click', closeLightbox);
    }
    
});