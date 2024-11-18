import datetime
import calendar
import getpass

wahana = {
    "Komedi Putar": 50,
    "Rumah Hantu": 50,
    "Bianglala": 50
}

user_data = {}
tiket_terpesan = {"Komedi Putar": {}, "Rumah Hantu": {}, "Bianglala": {}}
HARGA_VIP = 100000  

def cek_kuota(terpesan, minggu):
    """Cek apakah kuota tiket untuk wahana dan minggu tertentu tersedia."""
    return len(terpesan.get(minggu, [])) < 50

def login():
    username = input("Masukkan username: ")
    if username in user_data:
        password = getpass.getpass("Masukkan password: ")
        if user_data[username]["password"] == password:
            print("Login berhasil.")
            return username
        else:
            print("Password salah.")
            return None
    else:
        print("Username tidak ditemukan.")
        return None

def register():
    username = input("Masukkan username baru: ")
    password = getpass.getpass("Masukkan password baru: ")
    user_data[username] = {
        "password": password,
        "tiket": [],
        "promo": True,
        "ulasan": [],
        "total_tiket": 0,  
        "vip": False,       
        "saldo": 0          
    }
    print("Pendaftaran berhasil.")
    return username

def input_guest():
    nama = input("Masukkan nama: ")
    umur = int(input("Masukkan umur: "))
    return nama, umur

def top_up(username):
    print("=== Top-Up Saldo ===")
    bank_account = input("Masukkan nomor rekening Anda: ")
    nominal = int(input("Masukkan nominal yang ingin di-top-up: "))
    user_data[username]["saldo"] += nominal
    print(f"Top-up berhasil! Saldo Anda sekarang: Rp {user_data[username]['saldo']:,}")

def beli_tiket(username, nama_guest=None):
    is_vip = user_data.get(username, {}).get("vip", False)
    if is_vip:
        print("Anda adalah pengguna VIP! Anda dapat memesan tiket tanpa batas waktu.")
    else:
        hari_ini = datetime.datetime.now()
        if hari_ini.weekday() != 5: 
            print("Pemesanan hanya berlaku untuk Sabtu. Redirecting...")
            hari_sabtu = hari_ini + datetime.timedelta(days=(5 - hari_ini.weekday()) % 7)
        else:
            hari_sabtu = hari_ini

        nama_hari_sabtu = calendar.day_name[hari_sabtu.weekday()]  
        nama_hari_sabtu = nama_hari_sabtu.capitalize()  
        minggu_ini = f"{nama_hari_sabtu}, Minggu {hari_sabtu.isocalendar()[1]}"

    # Memilih wahana
    print("Wahana yang tersedia:")
    for idx, w in enumerate(wahana.keys(), 1):
        print(f"{idx}. {w}")

    if is_vip:
        pilihan1 = int(input("Pilih wahana pertama (masukkan nomor): ")) - 1
        wahana_pilihan1 = list(wahana.keys())[pilihan1]
        pilihan2 = int(input("Pilih wahana kedua (masukkan nomor): ")) - 1
        wahana_pilihan2 = list(wahana.keys())[pilihan2]
    else:
        pilihan = int(input("Pilih wahana (masukkan nomor): ")) - 1
        wahana_pilihan1 = list(wahana.keys())[pilihan]

    jumlah_tiket = int(input("Masukkan jumlah tiket: "))
    harga_per_tiket = 25000

    # Hitung total harga
    total_harga = jumlah_tiket * harga_per_tiket
    if user_data.get(username, {}).get("total_tiket", 0) > 50:
        total_harga *= 0.75
        print("Selamat! Anda mendapatkan diskon 25%.")

    # Proses pemesanan tiket
    for wahana_pilihan in ([wahana_pilihan1, wahana_pilihan2] if is_vip else [wahana_pilihan1]):
        if jumlah_tiket + len(tiket_terpesan[wahana_pilihan].get(minggu_ini, [])) <= 50:
            tiket_terpesan[wahana_pilihan].setdefault(minggu_ini, []).extend([username or nama_guest] * jumlah_tiket)
            print(f"Tiket untuk {wahana_pilihan} berhasil dipesan sebanyak {jumlah_tiket} untuk {minggu_ini}.")
        else:
            print(f"Kuota untuk {wahana_pilihan} pada minggu ini penuh.")

    # Potong saldo
    if username:
        if user_data[username]["saldo"] >= total_harga:
            user_data[username]["saldo"] -= total_harga
            print(f"Total harga yang dibayar: Rp {total_harga:,.0f}")
            print(f"Sisa saldo Anda: Rp {user_data[username]['saldo']:,}")
        else:
            print("Saldo Anda tidak mencukupi. Silakan top-up terlebih dahulu.")
    elif not username:
        print(f"Total harga yang harus dibayar (Guest): Rp {total_harga:,}")

    # Update poin royalti
    if username:
        user_data[username]["total_tiket"] += jumlah_tiket

def upgrade_vip(username):
    if user_data[username]["vip"]:
        print("Anda sudah menjadi pengguna VIP.")
    elif user_data[username]["saldo"] >= HARGA_VIP:
        user_data[username]["saldo"] -= HARGA_VIP
        user_data[username]["vip"] = True
        print(f"Upgrade ke VIP berhasil! Saldo Anda sekarang: Rp {user_data[username]['saldo']:,}")
    else:
        print(f"Saldo Anda tidak mencukupi untuk upgrade VIP. Saldo Anda: Rp {user_data[username]['saldo']:,}")

def menu_user(username):
    while True:
        print("\nMenu User:")
        print("1. Beli Tiket")
        print("2. Ulasan Wahana")
        print("3. Cek Promo")
        print("4. Cancel Tiket")
        print("5. Lihat Ulasan")
        print("6. Top-Up Saldo")
        print("7. Upgrade VIP")
        print("8. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            beli_tiket(username)
        elif pilihan == "6":
            top_up(username)
        elif pilihan == "7":
            upgrade_vip(username)
        elif pilihan == "8":
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")

def menu_guest(nama, umur):
    while True:
        print("\nMenu Guest:")
        print("1. Beli Tiket")
        print("2. Lihat Ulasan")
        print("3. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            beli_tiket(None, nama_guest=nama)
        elif pilihan == "2":
            lihat_ulasan()
        elif pilihan == "3":
            print("Terima kasih telah menggunakan aplikasi kami!")
            break
        else:
            print("Pilihan tidak valid.")

def main():
    print("Selamat datang di Aplikasi Pembelian Tiket Wahana Pasar Malam!")
    while True:
        print("\nMenu Utama:")
        print("1. Login")
        print("2. Masuk sebagai Guest")
        print("3. Daftar (Register)")
        print("4. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            username = login()
            if username:
                menu_user(username)
        elif pilihan == "2":
            nama_guest, umur_guest = input_guest()
            menu_guest(nama_guest, umur_guest)
        elif pilihan == "3":
            username = register()
            menu_user(username)
        elif pilihan == "4":
            print("Terima kasih telah menggunakan aplikasi kami!")
            break
        else:
            print("Pilihan tidak valid.")

main()
