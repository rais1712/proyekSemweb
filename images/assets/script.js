// assets/script.js

// Pastikan skrip ini dijalankan setelah DOM sepenuhnya dimuat
document.addEventListener('DOMContentLoaded', function() {
    
    // Ambil elemen-elemen yang diperlukan
    const lightbox = document.getElementById('imageLightbox');
    const lightboxImg = document.getElementById('lightboxImage');
    const manuscriptImage = document.getElementById('manuscriptImage');
    const closeBtn = document.querySelector('.lightbox-close');

    // Cek apakah semua elemen ada sebelum menambahkan event listener
    if (manuscriptImage && lightbox && lightboxImg && closeBtn) {
        
        // Ketika gambar naskah diklik
        manuscriptImage.onclick = function() {
            lightbox.style.display = 'block';
            lightboxImg.src = this.src;
        }

        // Ketika tombol close diklik
        closeBtn.onclick = function() {
            lightbox.style.display = 'none';
        }

        // Ketika area di luar gambar pada lightbox diklik
        lightbox.onclick = function(event) {
            // Pastikan klik bukan pada gambar itu sendiri
            if (event.target === lightbox) {
                lightbox.style.display = "none";
            }
        }
    }
});