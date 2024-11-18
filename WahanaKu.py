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

# === Fungsi untuk penyimpanan data ===
def load_users():
    """Membaca data pengguna dari file."""
    try:
        with open("users.txt", "r") as file:
            for line in file:
                username, password, saldo, vip, total_tiket = line.strip().split("|")
                user_data[username] = {
                    "password": password,
                    "saldo": int(saldo),
                    "vip": vip == "True",
                    "total_tiket": int(total_tiket),
                }
    except FileNotFoundError:
        pass

def save_users():
    """Menyimpan data pengguna ke file."""
    with open("users.txt", "w") as file:
        for username, data in user_data.items():
            file.write(f"{username}|{data['password']}|{data['saldo']}|{data['vip']}|{data['total_tiket']}\n")

def save_transaction(username, wahana, jumlah_tiket, total_harga):
    """Menyimpan histori transaksi ke file."""
    with open("transactions.txt", "a") as file:
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{waktu}|{username}|{wahana}|{jumlah_tiket}|{total_harga}\n")

# === Fungsi login dan register ===
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
    if username in user_data:
        print("Username sudah terdaftar.")
        return None
    password = getpass.getpass("Masukkan password baru: ")
    user_data[username] = {
        "password": password,
        "saldo": 0,
        "vip": False,
        "total_tiket": 0,
    }
    save_users()
    print("Pendaftaran berhasil.")
    return username

# === Fungsi pembelian tiket ===
def beli_tiket(username=None):
    is_vip = user_data.get(username, {}).get("vip", False) if username else False
    if is_vip:
        print("Anda adalah pengguna VIP! Anda dapat memesan tiket tanpa batas waktu.")
    else:
        hari_ini = datetime.datetime.now()
        if hari_ini.weekday() != 5: 
            print("Pemesanan hanya berlaku untuk Sabtu. Redirecting...")
            hari_sabtu = hari_ini + datetime.timedelta(days=(5 - hari_ini.weekday()) % 7)
        else:
            hari_sabtu = hari_ini
        minggu_ini = f"Minggu {hari_sabtu.isocalendar()[1]}"

    print("Wahana yang tersedia:")
    for idx, w in enumerate(wahana.keys(), 1):
        print(f"{idx}. {w}")

    pilihan = int(input("Pilih wahana (masukkan nomor): ")) - 1
    wahana_pilihan = list(wahana.keys())[pilihan]

    jumlah_tiket = int(input("Masukkan jumlah tiket: "))
    harga_per_tiket = 25000
    total_harga = jumlah_tiket * harga_per_tiket

    if username and user_data[username]["total_tiket"] > 50:
        total_harga *= 0.75
        print("Selamat! Anda mendapatkan diskon 25%.")

    if jumlah_tiket + len(tiket_terpesan[wahana_pilihan].get(minggu_ini, [])) <= 50:
        tiket_terpesan[wahana_pilihan].setdefault(minggu_ini, []).extend([username or "Guest"] * jumlah_tiket)
        print(f"Tiket untuk {wahana_pilihan} berhasil dipesan sebanyak {jumlah_tiket} untuk {minggu_ini}.")
        save_transaction(username or "Guest", wahana_pilihan, jumlah_tiket, total_harga)
    else:
        print(f"Kuota untuk {wahana_pilihan} pada minggu ini penuh.")

    if username:
        if user_data[username]["saldo"] >= total_harga:
            user_data[username]["saldo"] -= total_harga
            user_data[username]["total_tiket"] += jumlah_tiket
            save_users()
            print(f"Total harga yang dibayar: Rp {total_harga:,.0f}")
            print(f"Sisa saldo Anda: Rp {user_data[username]['saldo']:,}")
        else:
            print("Saldo Anda tidak mencukupi. Silakan top-up terlebih dahulu.")
    else:
        print(f"Total harga yang harus dibayar (Guest): Rp {total_harga:,}")

# === Fungsi lain (top-up, upgrade VIP, dll.) ===
def top_up(username):
    nominal = int(input("Masukkan nominal yang ingin di-top-up: "))
    user_data[username]["saldo"] += nominal
    save_users()
    print(f"Top-up berhasil! Saldo Anda sekarang: Rp {user_data[username]['saldo']:,}")

def upgrade_vip(username):
    if user_data[username]["vip"]:
        print("Anda sudah menjadi pengguna VIP.")
    elif user_data[username]["saldo"] >= HARGA_VIP:
        user_data[username]["saldo"] -= HARGA_VIP
        user_data[username]["vip"] = True
        save_users()
        print(f"Upgrade ke VIP berhasil! Saldo Anda sekarang: Rp {user_data[username]['saldo']:,}")
    else:
        print(f"Saldo Anda tidak mencukupi untuk upgrade VIP. Saldo Anda: Rp {user_data[username]['saldo']:,}")
def lihat_histori(username=None):
    """Menampilkan histori pembelian tiket."""
    print("\n=== Histori Pembelian ===")
    try:
        with open("transactions.txt", "r") as file:
            transactions = file.readlines()
            if username:  
                user_transactions = [t for t in transactions if f"|{username}|" in t]
                if user_transactions:
                    for t in user_transactions:
                        print(t.strip())
                else:
                    print("Belum ada histori pembelian untuk akun ini.")
            else:  
                if transactions:
                    for t in transactions:
                        print(t.strip())
                else:
                    print("Belum ada histori pembelian.")
    except FileNotFoundError:
        print("Belum ada histori pembelian.")
    input("Tekan Enter untuk Melanjutkan...")

# === Menu Utama ===
def main():
    load_users()
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
                while True:
                    print("\nMenu User:")
                    print("1. Beli Tiket")
                    print("2. Top-Up Saldo")
                    print("3. Upgrade VIP")
                    print("4. Lihat Histori Pembelian")
                    print("5. Logout")
                    pilihan_user = input("Pilih menu: ")
                    if pilihan_user == "1":
                        beli_tiket(username)
                    elif pilihan_user == "2":
                        top_up(username)
                    elif pilihan_user == "3":
                        upgrade_vip(username)
                    elif pilihan_user == "4":
                        lihat_histori(username)
                    elif pilihan_user == "5":
                        print("Logout berhasil.")
                        break
                    else:
                        print("Pilihan tidak valid.")
        elif pilihan == "2":
            while True:
                print("\nMenu Guest:")
                print("1. Beli Tiket")
                print("2. Lihat Histori Pembelian")
                print("3. Logout")
                pilihan_guest = input("Pilih menu: ")
                if pilihan_guest == "1":
                    beli_tiket()
                elif pilihan_guest == "2":
                    lihat_histori()
                elif pilihan_guest == "3":
                    print("Terima kasih telah menggunakan aplikasi kami!")
                    break
                else:
                    print("Pilihan tidak valid.")
        elif pilihan == "3":
            register()
        elif pilihan == "4":
            print("Terima kasih telah menggunakan aplikasi kami!")
            break
        else:
            print("Pilihan tidak valid.")

main()
