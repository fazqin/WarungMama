# 🍳 Warung Mama - Smart Kitchen System
```
 █████   ███   █████   █████████   ███████████   █████  █████ ██████   █████   █████████ 
░░███   ░███  ░░███   ███░░░░░███ ░░███░░░░░███ ░░███  ░░███ ░░██████ ░░███   ███░░░░░███
 ░███   ░███   ░███  ░███    ░███  ░███    ░███  ░███   ░███  ░███░███ ░███  ███     ░░░ 
 ░███   ░███   ░███  ░███████████  ░██████████   ░███   ░███  ░███░░███░███ ░███         
 ░░███  █████  ███   ░███░░░░░███  ░███░░░░░███  ░███   ░███  ░███ ░░██████ ░███    █████
  ░░░█████░█████░    ░███    ░███  ░███    ░███  ░███   ░███  ░███  ░░█████ ░░███  ░░███ 
    ░░███ ░░███      █████   █████ █████   █████ ░░████████   █████  ░░█████ ░░█████████ 
     ░░░   ░░░      ░░░░░   ░░░░░ ░░░░░   ░░░░░   ░░░░░░░░   ░░░░░    ░░░░░   ░░░░░░░░░  
             ██████   ██████   █████████   ██████   ██████   █████████                               
            ░░██████ ██████   ███░░░░░███ ░░██████ ██████   ███░░░░░███                              
             ░███░█████░███  ░███    ░███  ░███░█████░███  ░███    ░███                              
             ░███░░███ ░███  ░███████████  ░███░░███ ░███  ░███████████                              
             ░███ ░░░  ░███  ░███░░░░░███  ░███ ░░░  ░███  ░███░░░░░███                              
             ░███      ░███  ░███    ░███  ░███      ░███  ░███    ░███                              
             █████     █████ █████   █████ █████     █████ █████   █████                             
            ░░░░░     ░░░░░ ░░░░░   ░░░░░ ░░░░░     ░░░░░ ░░░░░   ░░░░░                                    
```
## Project UAS Algoritma & Pemrograman
Sistem Manajemen Kasir dan Dapur Terintegrasi berbasis Python, JSON, dan Manajemen Antrean Prioritas.
## 📌 Deskripsi Project
Warung Mama Smart Kitchen adalah solusi digital untuk mentransformasi operasional warung makan tradisional menjadi sistem dapur pintar. Project ini dikembangkan untuk menyelesaikan masalah nyata di lapangan seperti kesalahan pesanan, ketidaktahuan stok bahan baku, dan antrean yang tidak teratur.
### Sistem ini terdiri dari dua modul utama:
- Modul Kasir (cashier.py): Untuk input pesanan, manajemen stok bahan baku, dan pencetakan invoice.
- Modul Dapur (kitchen_kds.py): Kitchen Display System untuk koki memantau urutan masak dan melihat standar resep.
# 🚀 Fitur Utama
### 1. Inventory Bottleneck Logic
Sistem tidak hanya melihat stok "porsi" yang statis, tetapi menghitung ketersediaan menu secara dinamis berdasarkan sisa bahan baku di gudang (bahan_baku.json) menggunakan logika resep (recipes.json). Jika satu bahan habis (misal: Telur), maka semua menu yang membutuhkan telur akan otomatis dianggap HABIS.
### 2. Priority Queue with Surcharge
Mendukung layanan VIP. Pesanan dengan level prioritas 3 (VIP) akan otomatis menempati urutan teratas pada antrean dapur. Sebagai kompensasi, sistem secara otomatis menambahkan Biaya Layanan 10% pada total transaksi.
### 3. Lead Time Accumulation
Menghitung estimasi waktu tunggu secara jujur bagi pelanggan. Waktu tunggu dihitung dari:
Total Waktu Masak Antrean Saat Ini + Waktu Masak Pesanan Baru.
### 4. Kitchen Display System (KDS)
Terminal khusus dapur yang menampilkan urutan masak berdasarkan algoritma multi-level sorting (Prioritas > Waktu Masuk) dan fitur pemanggil resep digital untuk menjaga konsistensi rasa.
### 5. Data Persistence
Menggunakan file JSON sebagai database lightweight untuk menyimpan stok dan resep, serta file CSV untuk mencatat riwayat penjualan harian secara permanen.
# 🛠 Struktur Data & Algoritma
- Dictionary (Hash Map): Digunakan untuk akses cepat O(1) pada data menu, resep, dan stok bahan baku.
- List: Digunakan untuk mengelola antrean (Queue) dan keranjang belanja.
- Object-Oriented Programming (OOP): Class Pesanan untuk enkapsulasi data pelanggan dan class Dapur sebagai manajer logika.
- Priority Insertion Sort: Algoritma untuk menyisipkan pesanan baru ke posisi yang tepat dalam antrean berdasarkan tingkat urgensi.
# 📦 Instalasi & Cara Penggunaan
### Persiapan File
Pastikan folder project memiliki struktur berikut:
/warung-mama
├── cashier.py          # Jalankan ini untuk bagian Kasir
├── kitchen_kds.py      # Jalankan ini untuk bagian Dapur
├── recipes.json        # Database resep masakan
├── bahan_baku.json     # Database stok gudang
├── stok_harian.json    # (Auto-generated) Sisa porsi menu
└── riwayat_penjualan.csv # (Auto-generated) Log transaksi
## Cara Menjalankan
### 1. Buka Terminal 1 (Kasir):
```python main.py```
- Input nama pelanggan.
- Tambah menu ke keranjang (Sistem akan memvalidasi stok bahan baku).
- Pilih level prioritas (VIP akan dikenakan biaya tambahan).
- Checkout untuk mengirim pesanan ke dapur.
### 2. Buka Terminal 2 (Dapur):
```python kitchen_kds.py```
- Lihat daftar antrean yang otomatis terurut.
- Pilih opsi "Lihat Resep" untuk memastikan takaran bumbu benar.
- Pilih "Selesaikan Pesanan" jika masakan sudah siap saji.
