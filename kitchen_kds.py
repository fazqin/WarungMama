import json
import os
import time

# --- KONFIGURASI FILE ---
ANTRIAN_FILE = 'antrian_aktif.json' # File hasil kiriman kasir
RECIPES_FILE = 'recipes.json'
STOK_FILE = 'stok_harian.json' # Untuk referensi nama menu

COLORS = {
    3: '\033[91m',    # Merah (VIP)
    2: '\033[93m',    # Kuning (Standar)
    1: '\033[94m',    # Biru (Low/Katering)
    'header': '\033[96m', # Cyan
    'reset': '\033[0m'
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def display_recipe(menu_id):
    """Menyelesaikan Masalah #5: Inkonsistensi Rasa/Takaran Bumbu"""
    resep = load_json(RECIPES_FILE)
    m_id_str = str(menu_id)
    
    # Cari nama menu untuk tampilan (bisa ditambah metadata menu di sini)
    MENU_MASTER = {
        "1": "Nasi Goreng", "2": "Mie Ayam", "3": "Sate Babi", 
        "4": "Ayam Geprek", "5": "Bakso", "6": "Gado-Gado",
        "7": "Rendang", "8": "Soto Ayam", "9": "Es Teh Manis",
        "10": "Es Jeruk", "11": "Air Mineral", "12": "Kopi Hitam"
    }

    print(f"\n{COLORS['header']}--- STANDAR RESEP: {MENU_MASTER.get(m_id_str, 'Menu Tak Dikenal')} ---{COLORS['reset']}")
    if m_id_str in resep:
        print(f"{'BAHAN':<20} | {'TAKARAN (PER PORSI)'}")
        print("-" * 40)
        for bahan, takaran in resep[m_id_str].items():
            print(f"{bahan:<20} | {takaran} unit/gram")
        print("-" * 40)
    else:
        print("⚠️ Data resep tidak ditemukan!")

def kds_main():
    while True:
        clear_screen()
        print(f"{COLORS['header']}🍳 KITCHEN DISPLAY SYSTEM (KDS) - WARUNG MAMA 🧑‍🍳")
        print(f"Sistem Urutan Masak & Standarisasi Resep{COLORS['reset']}")
        print("=" * 60)

        # Muat Antrean Aktif dari file yang dikirim Kasir
        antrian = load_json(ANTRIAN_FILE) # Format: list of dicts

        if not antrian:
            print("\n   [ ANTRIAN KOSONG - KOKI BISA ISTIRAHAT ]")
            print("\n1. Refresh Antrean")
            print("2. Keluar")
        else:
            # Menyelesaikan Masalah #3: Manajemen Waktu & Alur Kerja
            # Sortir otomatis berdasarkan Prioritas (3 tertinggi) lalu Waktu Masuk
            antrian.sort(key=lambda x: (x['prioritas'], x['waktu_masuk']), reverse=True)

            print(f"{'URUTAN':<7} {'LEVEL':<10} {'PELANGGAN':<15} {'MENU':<15} {'ESTIMASI'}")
            print("-" * 60)

            for i, p in enumerate(antrian):
                prio_color = COLORS.get(p['prioritas'], COLORS['reset'])
                prio_text = {3: "VIP", 2: "STD", 1: "LOW"}.get(p['prioritas'], "UNK")
                
                print(f"{i+1:<7} {prio_color}{prio_text:<10}{COLORS['reset']} {p['nama_pelanggan']:<15} {p['nama_menu']:<15} {p['waktu_masak']}s")

            print("\n" + "=" * 60)
            print("AKSI DAPUR:")
            print("1. Lihat Resep (Cek Takaran Bumbu)")
            print("2. Selesaikan Pesanan Teratas (Selesai Masak)")
            print("3. Refresh Antrean")
            print("4. Keluar")

        pilihan = input("\nPilih Aksi (1-4): ")

        if pilihan == '1':
            if not antrian: continue
            try:
                idx = int(input("Lihat resep urutan No berapa? ")) - 1
                if 0 <= idx < len(antrian):
                    display_recipe(antrian[idx]['menu_id'])
                    input("\nTekan ENTER untuk kembali ke daftar antrean...")
            except: pass
        
        elif pilihan == '2':
            if not antrian: continue
            # Ambil pesanan teratas (FIFO + Priority)
            pesanan_selesai = antrian.pop(0)
            save_json(ANTRIAN_FILE, antrian)
            print(f"\n✅ Pesanan {pesanan_selesai['nama_menu']} untuk {pesanan_selesai['nama_pelanggan']} TELAH SELESAI!")
            time.sleep(1.5)

        elif pilihan == '3':
            continue
        
        elif pilihan == '4':
            break

if __name__ == "__main__":
    kds_main()