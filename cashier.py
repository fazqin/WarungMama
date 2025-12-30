import time, json, csv, os, sys

# --- KONFIGURASI DAN MASTER DATA ---
STOK_FILE = 'stok_harian.json'
RIWAYAT_FILE = 'riwayat_penjualan.csv'
BAHAN_BAKU_FILE = 'bahan_baku.json' 
RECIPES_FILE = 'recipes.json'
ANTRIAN_FILE = 'antrian_aktif.json'

# MASTER DATA MENU (ID, Harga, Prioritas, Waktu Masak)
MENU_MASTER = {
    1: {'nama': 'Nasi Goreng', 'harga': 15000, 'waktu_masak_unit': 5, 'prioritas_default': 2},
    2: {'nama': 'Mie Ayam', 'harga': 18000, 'waktu_masak_unit': 7, 'prioritas_default': 2},
    3: {'nama': 'Sate Biawak', 'harga': 35000, 'waktu_masak_unit': 12, 'prioritas_default': 2},
    4: {'nama': 'Ayam Geprek', 'harga': 20000, 'waktu_masak_unit': 6, 'prioritas_default': 2},
    5: {'nama': 'Bakso', 'harga': 16000, 'waktu_masak_unit': 8, 'prioritas_default': 2},
    6: {'nama': 'Gado-Gado', 'harga': 14000, 'waktu_masak_unit': 4, 'prioritas_default': 2},
    7: {'nama': 'Rendang', 'harga': 40000, 'waktu_masak_unit': 15, 'prioritas_default': 2},
    8: {'nama': 'Soto Ayam', 'harga': 19000, 'waktu_masak_unit': 9, 'prioritas_default': 2},
    9: {'nama': 'Es Teh Manis', 'harga': 5000, 'waktu_masak_unit': 2, 'prioritas_default': 2},
    10: {'nama': 'Es Jeruk', 'harga': 8000, 'waktu_masak_unit': 2, 'prioritas_default': 2},
    11: {'nama': 'Air Mineral', 'harga': 5000, 'waktu_masak_unit': 1, 'prioritas_default': 2},
    12: {'nama': 'Kopi Hitam', 'harga': 4000, 'waktu_masak_unit': 3, 'prioritas_default': 2}
}

# ANSI Color Codes
COLORS = {
    3: '\033[91m',    # Merah (VIP)
    2: '\033[93m',    # Kuning (Standar)
    1: '\033[94m',    # Biru (Katering)
    'header': '\033[96m', # Cyan
    'reset': '\033[0m'
}

# --- UTILITY FUNCTIONS ---

def clear_screen():
    """Membersihkan layar console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_stok():
    """Memuat stok harian dari JSON file."""
    if os.path.exists(STOK_FILE):
        try:
            with open(STOK_FILE, 'r') as f:
                print(f"[DATA] Memuat stok dari {STOK_FILE}...")
                return json.load(f)
        except json.JSONDecodeError:
            print("[ALERT] File JSON rusak. Menggunakan stok default.")
            return {MENU_MASTER[id]['nama']: 50 for id in MENU_MASTER}
    else:
        # Inisialisasi stok default
        return {MENU_MASTER[id]['nama']: 50 for id in MENU_MASTER}

def save_stok(stok_data):
    """Menyimpan stok harian ke JSON file."""
    try:
        with open(STOK_FILE, 'w') as f:
            json.dump(stok_data, f, indent=4)
        print(f"[OK] Data Stok Harian berhasil disimpan ke {STOK_FILE}.")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan data stok: {e}")

def load_json(filename):
    """Fungsi umum untuk memuat file JSON."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_json(filename, data):
    """Fungsi umum untuk menyimpan file JSON."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def hitung_stok_dari_bahan():
    """hitung sisa porsi menu berdasarkan bahan baku (Bottleneck Logic)."""
    bahan = load_json(BAHAN_BAKU_FILE)
    resep_master = load_json(RECIPES_FILE)
    stok_porsi = {}

    for menu_id, recipe in resep_master.items():
        m_id = int(menu_id)
        if m_id in MENU_MASTER:
            nama_menu = MENU_MASTER[m_id]['nama']
            
            # Cari bahan yang paling sedikit (pembatas)
            list_kemungkinan = []
            for item_bahan, butuh in recipe.items():
                tersedia = bahan.get(item_bahan, 0)
                list_kemungkinan.append(int(tersedia // butuh))
            
            # Klo resep ada, ambil angka terkecil. klo gk ada resep, anggap 0.
            stok_porsi[nama_menu] = min(list_kemungkinan) if list_kemungkinan else 0
            
    return stok_porsi

def display_banner():
    """Menampilkan banner ASCII Art untuk Warung Mama Smart Kitchen."""
    clear_screen()
    
    # Gunakan warna header (Cyan) untuk banner
    header_color = COLORS['header']
    reset_color = COLORS['reset']
    
    banner = f"""
    {header_color}

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
    ---------------------------------------------------------
    SISTEM KASIR WARUNG MAMA - SMART KITCHEN
---------------------------------------------------------
    VERSION 1.0 | DEVELOPED FOR UAS ALGORITMA
========================================================={reset_color}
    """
    print(banner)

# --- FUNGSI INVOICE (OUTPUT KE FILE TXT) ---

def generate_invoice_file(pesanan, keranjang, total_harga, no_antrian, estimasi_tunggu, biaya_vip=0):
    """Membuat simulasi invoice dan menyimpannya ke file teks (.txt)"""
    invoice_filename = f"INVOICE_{pesanan.nama.replace(' ', '_')}_{int(time.time())}.txt"
    
    # Membuat konten item list
    item_list_content = ""
    for item in keranjang:
        item_total = item['harga'] * item['qty']
        item_list_content += f"{item['nama']:<25} {item['qty']:<5} Rp{item['harga']:,.0f} | Total: Rp{item_total:,.0f}\n"

    # Tambahkan baris biaya VIP jika ada
    info_vip = ""
    if biaya_vip > 0:
        info_vip = f"Biaya Prioritas (VIP 10%): Rp{biaya_vip:,.0f}\n"

    invoice_content = f"""
========================================
       INVOICE WARUNG MAMA (RESMI)
========================================
Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')}
Antrian: {no_antrian} | Pelanggan: {pesanan.nama}
----------------------------------------
{'MENU':<25} {'QTY':<5} {'TOTAL'}
{item_list_content.strip()}
----------------------------------------
{info_vip}TOTAL AKHIR:             Rp{total_harga:,.0f}
----------------------------------------
Prioritas: Level {pesanan.prioritas_level} ({'VIP' if pesanan.prioritas_level == 3 else 'Normal'})
Estimasi Selesai: {estimasi_tunggu} detik
========================================
"""
    
    try:
        with open(invoice_filename, 'w') as f:
            f.write(invoice_content)
        
        clear_screen()
        print("="*50)
        print("INVOICE BERHASIL DICETAK (SIMULASI)")
        print(f"File disimpan sebagai: {invoice_filename}")
        print("="*50)
        print(invoice_content) 
        time.sleep(1) 
        input("\nTekan ENTER untuk kembali ke Menu Kasir...")
        
    except Exception as e:
        print(f"\n[ERROR] Gagal menyimpan file invoice: {e}")
        time.sleep(2)

# --- CLASS PESANAN (DATA MODEL) ---

class Pesanan:
    """Class merepresentasikan pesanan pelanggan (dibuat per transaksi, bukan per item)."""

    def __init__(self, nama, menu_id, jumlah, prioritas_level=None):
        data = MENU_MASTER.get(menu_id)
        if not data:
             raise ValueError(f"Menu ID {menu_id} tidak ditemukan di MENU_MASTER.")

        self.nama = nama
        self.menu = data['nama']
        self.harga = data['harga']
        self.jumlah = int(jumlah)
        self.prioritas_level = int(prioritas_level) if prioritas_level is not None else data['prioritas_default']
        self.waktu_masuk = time.time()
        # Perhatian: Di sini waktu estimasi akan di-override di finalisasi_dan_submit
        self.waktu_estimasi_masak = self._hitung_estimasi(data['waktu_masak_unit']) 

    def _hitung_estimasi(self, unit_time):
        """Menghitung estimasi waktu masak."""
        return unit_time * self.jumlah

    def __str__(self):
        """String representation dengan warna ANSI untuk KDS."""
        color = COLORS.get(self.prioritas_level, COLORS['reset'])
        status_text = {3: "VIP", 2: "STD", 1: "LOW"}.get(self.prioritas_level, "UNK")
        
        return (f"{color}[{status_text} Lvl {self.prioritas_level}]{COLORS['reset']} "
                f"| {self.nama} | {self.menu} x{self.jumlah} "
                f"| Est: {self.waktu_estimasi_masak}s")

# --- CLASS DAPUR (QUEUE & LOGIC) ---

class DapurWarungMama:
    """Class mengelola antrian dapur, stok, dan proses masak."""

    def __init__(self):
        self.antrian = []
        self.stok_harian = hitung_stok_dari_bahan()
    
    def kurangi_bahan_baku(self, keranjang):
        """Mengurangi stok mentah di bahan_baku.json berdasarkan resep."""
        bahan = load_json(BAHAN_BAKU_FILE)
        resep_master = load_json(RECIPES_FILE)
        for item in keranjang:
            m_id_str = str(item['menu_id'])
            qty = item['qty']
            
            if m_id_str in resep_master:
                resep = resep_master[m_id_str]
                for nama_bahan, butuh in resep.items():
                    bahan[nama_bahan] -= (butuh * qty)

        # Simpan kembali ke file bahan baku
        save_json(BAHAN_BAKU_FILE, bahan)
        # Update tampilan stok porsi di sistem
        self.stok_harian = hitung_stok_dari_bahan()
        # Opsional: simpan stok porsi ke stok_harian.json jika perlu
        save_json(STOK_FILE, self.stok_harian)

    def hitung_total_waktu_di_antrian(self):
        """Menghitung total waktu masak dari semua pesanan yang masih mengantri."""
        return sum(p.waktu_estimasi_masak for p in self.antrian)

    def tambah_pesanan(self, pesanan):
        """Menambahkan pesanan dengan Priority Insertion. Stok diasumsikan sudah divalidasi."""
        
        # Stok sudah dikurangi di finalisasi_dan_submit, ini hanya insertion
        
        # ALGORITMA PRIORITY INSERTION 
        posisi_sisip = len(self.antrian)
        
        for i, existing in enumerate(self.antrian):
            if pesanan.prioritas_level > existing.prioritas_level:
                posisi_sisip = i
                break
            elif pesanan.prioritas_level == existing.prioritas_level:
                if pesanan.waktu_masuk < existing.waktu_masuk:
                    posisi_sisip = i 
                    break
                else:
                    posisi_sisip = i + 1
            elif pesanan.prioritas_level < existing.prioritas_level:
                posisi_sisip = i
                break

        self.antrian.insert(posisi_sisip, pesanan)
        
        print(f"\n[OK] Pesanan {pesanan.nama} ({pesanan.menu}) berhasil masuk.")
        return True, posisi_sisip + 1

    def lihat_antrian(self):
        """Menampilkan antrian dapur (KDS) dan simulasi proses masak secara otomatis."""
        clear_screen()
        print(f"{COLORS['header']}="*60)
        print(" DAPUR WARUNG MAMA - KITCHEN DISPLAY SYSTEM (KDS) ")
        print("="*60 + COLORS['reset'])
        
        if not self.antrian:
            print("\n (Antrian Kosong - Koki Santai) ")
        else:
            self.antrian.sort(key=lambda p: (p.prioritas_level, p.waktu_masuk), reverse=True)
            
            # Tampilkan 5 pesanan teratas di KDS
            print(f"{'No.':<4} {'Prioritas':<15} {'Nama/Meja':<15} {'Pesanan':<15} {'Est. Masak':<10}")
            print("-" * 60)
            
            for i, p in enumerate(self.antrian[:5]): 
                status_text = {3: "VIP", 2: "STD", 1: "LOW"}.get(p.prioritas_level, "UNK")
                est_text = f"{p.waktu_estimasi_masak}s"
                print(f"{i+1:<4} {COLORS.get(p.prioritas_level)}{status_text:<15}{COLORS['reset']} {p.nama:<15} {p.menu} x{p.jumlah:<10} {est_text:<10}")
            
            # Otomatis Masak Pesanan Pertama (Simulasi Koki selalu siap)
            if self.antrian:
                print(f"\n{COLORS['header']}>>> OTOMATIS MEMASAK PESANAN NO. 1...{COLORS['reset']}")
                self.proses_masak(simulasi=True)

        print("\n" + "="*60)
        input("\nTekan ENTER untuk me-refresh/kembali ke Menu Utama...")

    def proses_masak(self, simulasi=False):
        """Memproses pesanan paling depan (Dequeue) dan mencatat riwayat."""
        if not self.antrian:
            return

        pesanan = self.antrian.pop(0)
        waktu_mulai = time.time()
        
        if simulasi:
            print(f"    [MASAK] Pesanan {pesanan.nama} ({pesanan.menu}) sedang diproses (Tunggu {pesanan.waktu_estimasi_masak}s)")
        
        # Simulasi proses masak
        if not simulasi:
             time.sleep(pesanan.waktu_estimasi_masak) 
        
        waktu_selesai = time.time()
        waktu_tunggu_total = waktu_selesai - pesanan.waktu_masuk
        
        if not simulasi:
             print(f"\n>>> SELESAI ({time.strftime('%H:%M:%S', time.localtime(waktu_selesai))})! Pesanan {pesanan.nama} siap diantar.")
        else:
             print(f"    [SELESAI] Pesanan {pesanan.nama} berhasil diselesaikan otomatis.")

        self._catat_riwayat(pesanan, waktu_selesai, waktu_tunggu_total)

    def _catat_riwayat(self, pesanan, waktu_selesai, waktu_tunggu):
        """Mencatat riwayat penjualan ke CSV file."""
        row = [
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pesanan.waktu_masuk)),
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(waktu_selesai)),
            pesanan.nama,
            pesanan.menu,
            pesanan.jumlah,
            pesanan.prioritas_level,
            round(waktu_tunggu, 2)
        ]
        file_exists = os.path.exists(RIWAYAT_FILE)
        
        with open(RIWAYAT_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Waktu Masuk', 'Waktu Selesai', 'Nama Pelanggan', 'Menu', 'Jumlah', 'Prioritas Level', 'Waktu Tunggu Total'])
            writer.writerow(row)
    
    def lihat_stok(self):
        """Menampilkan stok harian terkini."""
        clear_screen()
        print(f"{COLORS['header']}="*35)
        print("STOK HARIAN TERKINI")
        print("="*35 + COLORS['reset'])
        for menu, qty in self.stok_harian.items():
            print(f"- {menu}: {qty} porsi")
        print("="*35)
        input("\nTekan ENTER untuk kembali...")
    def update_antrian_ke_dapur(self):
        """Menyinkronkan antrean aktif ke file JSON agar bisa dibaca oleh kitchen_kds.py"""
        data_untuk_dapur = []
        for p in self.antrian:
            data_untuk_dapur.append({
                'menu_id': 1, # Placeholder, atau sesuaikan jika perlu detail per item
                'nama_pelanggan': p.nama,
                'nama_menu': p.menu,
                'prioritas': p.prioritas_level,
                'waktu_masak': p.waktu_estimasi_masak,
                'waktu_masuk': p.waktu_masuk
            })
        save_json(ANTRIAN_FILE, data_untuk_dapur)

    # UBAH fungsi tambah_pesanan milikmu menjadi seperti ini:
    def tambah_pesanan(self, pesanan):
        posisi_sisip = len(self.antrian)
        for i, existing in enumerate(self.antrian):
            if pesanan.prioritas_level > existing.prioritas_level:
                posisi_sisip = i
                break
        self.antrian.insert(posisi_sisip, pesanan)
        
        # --- TAMBAHKAN BARIS INI ---
        self.update_antrian_ke_dapur() 
        # ---------------------------
        
        print(f"\n[OK] Pesanan {pesanan.nama} berhasil masuk.")
        return True, posisi_sisip + 1

    # UBAH fungsi proses_masak milikmu menjadi seperti ini:
    def proses_masak(self, simulasi=False):
        if not self.antrian: return
        pesanan = self.antrian.pop(0)
        
        # --- TAMBAHKAN BARIS INI ---
        self.update_antrian_ke_dapur() 
        # ---------------------------
        
        # (Sisa kode proses_masak tetap sama)
        self._catat_riwayat(pesanan, time.time(), 0)
        print(f"    [SELESAI] Pesanan {pesanan.nama} berhasil diselesaikan.")


# --- FUNGSI FLOW KASIR INTERAKTIF (SHOPPING CART) ---

def tampilkan_menu_kasir(stok_harian):
    print(f"{COLORS['header']}="*85)
    # Tambahkan header STOK TERSEDIA
    print(f"{'ID':<4} {'NAMA MENU':<25} {'HARGA':<12} {'EST. MASAK':<15} {'STOK TERSEDIA'}")
    print("="*85 + COLORS['reset'])
    
    for id, data in sorted(MENU_MASTER.items()):
        menu_name = data['nama']
        stok = stok_harian.get(menu_name, 0)
        
        # Logika warna: Merah jika stok 0
        color = '\033[91m' if stok == 0 else COLORS['reset']
        stok_display = f"{stok} porsi" if stok > 0 else "HABIS"
        
        print(f"{id:<4} {menu_name:<25} Rp{data['harga']:<11,.0f} {data['waktu_masak_unit']:<15} {color}{stok_display}{COLORS['reset']}")
    print("-" * 85)


def tambahkan_item_ke_keranjang(dapur, keranjang):
    """Menambahkan satu item baru ke keranjang."""
    clear_screen()
    print("--- TAMBAH ITEM KE KERANJANG ---")
    tampilkan_menu_kasir(dapur.stok_harian) # Tampilkan menu saat input
    
    try:
        menu_id = int(input("Input ID Menu: "))
        if menu_id not in MENU_MASTER:
            print("ID Menu tidak valid!")
            time.sleep(1)
            return

        qty = int(input("Jumlah: "))
        if qty <= 0:
            print("Jumlah harus lebih dari 0.")
            time.sleep(1)
            return

        
        data = MENU_MASTER[menu_id]

# Tambahkan pengecekan stok ini:
        if dapur.stok_harian.get(data['nama'], 0) < qty:
            print(f"\n[GAGAL] Stok tidak cukup! Sisa stok {data['nama']}: {dapur.stok_harian.get(data['nama'])}")
            time.sleep(2)
            return # Batalkan penambahan ke keranjang    
        data = MENU_MASTER[menu_id]
        
        # Tambahkan item ke keranjang
        keranjang.append({
            'menu_id': menu_id,
            'nama': data['nama'],
            'qty': qty,
            'harga': data['harga']
        })
        print(f"{qty}x {data['nama']} berhasil ditambahkan ke keranjang.")
        time.sleep(1)
        
    except ValueError:
        print("Input ID atau Jumlah harus berupa angka.")
        time.sleep(1)


def finalisasi_dan_submit(dapur, nama_pelanggan, keranjang, estimasi_tunggu):
    """Memvalidasi stok, mengurangi, dan submit keranjang ke Dapur."""
    
    # 1. Validasi Stok Total
    stok_dibutuhkan = {}
    for item in keranjang:
        menu_name = item['nama']
        stok_dibutuhkan[menu_name] = stok_dibutuhkan.get(menu_name, 0) + item['qty']
        
    for menu, qty_needed in stok_dibutuhkan.items():
        if dapur.stok_harian.get(menu, 0) < qty_needed:
            print(f"\n[GAGAL SUBMIT] Stok {menu} ({dapur.stok_harian.get(menu, 0)}) tidak mencukupi {qty_needed} porsi!")
            input("Tekan ENTER untuk kembali dan koreksi keranjang...")
            return

    # 2. Hitung Harga Dasar
    total_harga_dasar = sum(item['harga'] * item['qty'] for item in keranjang)

    # 3. Input Prioritas
    prioritas_tertinggi = max(MENU_MASTER[item['menu_id']]['prioritas_default'] for item in keranjang)
    print(f"\nPrioritas default: Level {prioritas_tertinggi}.")
    prioritas_input = input("Level Prioritas (1-2=Normal, 3=VIP + 1,5% Biaya): ")
    
    prioritas_final = int(prioritas_input) if prioritas_input in ['1','2','3'] else prioritas_tertinggi

    # 4. HITUNG BIAYA TAMBAHAN VIP
    biaya_vip = 0
    if prioritas_final == 3:
        biaya_vip = total_harga_dasar * 0.015  # Surcharge 2%
        print(f"{COLORS[3]}[SISTEM] Pesanan VIP terdeteksi. Tambahan Biaya: Rp{biaya_vip:,.0f}{COLORS['reset']}")

    total_harga_akhir = total_harga_dasar + biaya_vip
            
    # 5. Kurangi Bahan Baku
    dapur.kurangi_bahan_baku(keranjang)
    
    # 6. Buat Objek Pesanan
    total_estimasi = sum(MENU_MASTER[item['menu_id']]['waktu_masak_unit'] * item['qty'] for item in keranjang)
    
    pesanan_utama = Pesanan(nama=nama_pelanggan, menu_id=1, jumlah=1, prioritas_level=prioritas_final)
    pesanan_utama.waktu_estimasi_masak = total_estimasi
    pesanan_utama.harga = total_harga_akhir # Simpan harga yang sudah termasuk biaya VIP

    # 7. Submit & Cetak Invoice (Kirim biaya_vip agar muncul di invoice)
    result = dapur.tambah_pesanan(pesanan_utama)
    if result:
        is_success, no_antrian = result
        generate_invoice_file(pesanan_utama, keranjang, total_harga_akhir, no_antrian, estimasi_tunggu, biaya_vip)

def input_keranjang_interaktif(dapur, nama_pelanggan):
    """Mengelola keranjang belanja interaktif hingga disubmit."""
    
    keranjang = []
    
    while True:
        clear_screen()
        print(f"--- 🛒 KERANJANG BELANJA untuk {nama_pelanggan} ---")
        print("----------------------------------------")
        
        total_harga_keranjang = 0
        
        # Tampilkan Keranjang Saat Ini
        if not keranjang:
            print("[Keranjang Kosong]")
        else:
            print(f"{'No.':<4} {'Menu':<25} {'Qty':<5} {'Total Harga'}")
            print("-" * 50)
            for i, item in enumerate(keranjang, 1):
                item_total = item['harga'] * item['qty']
                total_harga_keranjang += item_total
                print(f"{i:<4} {item['nama']:<25} {item['qty']:<5} Rp{item_total:,.0f}")
            print("-" * 50)
            print(f"TOTAL AKHIR: {'':<30} Rp{total_harga_keranjang:,.0f}")
        
        print("\n--- Aksi Cepat ---")
        print("A. Tambah Menu Baru")
        print("B. Hapus/Koreksi Item (Berdasarkan No.)")
        print("C. Submit Pesanan ke Dapur (Selesai)")
        print("X. Batalkan Transaksi (Kembali ke Menu Utama)")
        
        aksi = input("\nPilih Aksi (A/B/C/X): ").upper()
        
        if aksi == 'A':
            tambahkan_item_ke_keranjang(dapur, keranjang)
        elif aksi == 'B':
            if not keranjang:
                print("Keranjang kosong. Tidak ada yang bisa dihapus.")
                time.sleep(1)
                continue
                
            try:
                item_no = int(input("Nomor item yang akan dihapus/dikoreksi: ")) - 1
                if 0 <= item_no < len(keranjang):
                    keranjang.pop(item_no)
                    print("Item berhasil dihapus dari keranjang.")
                else:
                    print("Nomor item tidak valid.")
                time.sleep(1)
            except ValueError:
                print("Input harus berupa angka.")
                time.sleep(1)
        elif aksi == 'C':
            if not keranjang:
                continue
    
            # 1. Hitung waktu pesanan yang sudah ada di dapur
            waktu_tunggu_antrian_lama = dapur.hitung_total_waktu_di_antrian()
            
            # 2. Hitung waktu masak pesanan yang baru ini
            total_estimasi_baru = sum(MENU_MASTER[item['menu_id']]['waktu_masak_unit'] * item['qty'] for item in keranjang)
            
            # 3. Total waktu tunggu pelanggan = Antrian Lama + Pesanan Baru
            estimasi_selesai_total = waktu_tunggu_antrian_lama + total_estimasi_baru
            # --------------------------

            # (Lanjutkan proses submit seperti biasa, lalu kirim estimasi_selesai_total ke invoice)
            finalisasi_dan_submit(dapur, nama_pelanggan, keranjang, estimasi_selesai_total)
            break
        elif aksi == 'X':
            print("Transaksi dibatalkan.")
            time.sleep(1)
            break
        else:
            print("Aksi tidak valid.")
            time.sleep(1)


# --- MAIN PROGRAM ---

def main():
    dapur = DapurWarungMama()
    display_banner()
    dapur.stok_harian = hitung_stok_dari_bahan() 
    
    while True:
        clear_screen()
        display_banner()
        print(f"{COLORS['header']}="*50)
        print(" SISTEM KASIR WARUNG MAMA - MENU UTAMA")
        print("="*50 + COLORS['reset'])
        
        print("1. Tambah Pesanan Baru (Flow Keranjang)")
        print("2. Koki: Lihat Antrian (KDS) & Proses Otomatis")
        print("3. Lihat Stok Harian Terkini")
        print("-" * 50)
        print("4. KELUAR & SIMPAN DATA")
        print("="*50)
        
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == '1':
            try:
                clear_screen()
                nama = input("Nama Pelanggan / No. Meja: ")
                if not nama:
                    print("Nama pelanggan tidak boleh kosong.")
                    time.sleep(1)
                    continue
                
                input_keranjang_interaktif(dapur, nama)
                
            except Exception as e:
                 print(f"\nTerjadi error: {e}")
                 time.sleep(2)


        elif pilihan == '2':
            dapur.lihat_antrian()

        elif pilihan == '3':
            dapur.lihat_stok()

        elif pilihan == '4':
            save_stok(dapur.stok_harian)
            print("Sistem dimatikan. Sampai jumpa!")
            sys.exit(0)
            
        else:
            print("Pilihan tidak valid.")
            time.sleep(1)

if __name__ == "__main__":
    main()