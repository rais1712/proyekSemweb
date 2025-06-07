from pdf2image import convert_from_path
import os

# Path ke file PDF Anda
pdf_path = "jpg2pdf.pdf"

# Folder untuk menyimpan gambar
output_folder = "images"

# Membuat folder jika belum ada
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Konversi PDF ke gambar
print(f"Mengonversi {pdf_path} ke gambar...")
# GANTI ALAMAT DI BAWAH INI DENGAN ALAMAT POPPLER ANDA!
poppler_folder_path = r"C:\Users\poppler-24.08.0\Library\bin" 

pages = convert_from_path(pdf_path, 300, poppler_path=poppler_folder_path) # Tambahkan poppler_path di sini
# Simpan setiap halaman sebagai file PNG
for i, page in enumerate(pages):
    image_path = os.path.join(output_folder, f"page_{i + 1}.png")
    page.save(image_path, "PNG")
    print(f"Menyimpan {image_path}")

print("Konversi selesai!")