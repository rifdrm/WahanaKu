import datetime
import calendar

wahana = {
    "Komedi Putar": 50,
    "Rumah Hantu": 50,
    "Bianglala": 50
}

user_data = {}
tiket_terpesan = {"Komedi Putar": {}, "Rumah Hantu": {}, "Bianglala": {}}

def cek_kuota(terpesan, minggu):
    """Cek apakah kuota tiket untuk wahana dan minggu tertentu tersedia."""
    return len(terpesan.get(minggu, [])) < 50

def login():
    username = input("Masukkan username: ")
    if username in user_data:
        print("Login berhasil.")
        return username
    else:
        print("Username tidak ditemukan.")
        return None

def register():
    username = input("Masukkan username baru: ")
    user_data[username] = {
        "tiket": [],
        "promo": True,
        "ulasan": []
    }
    print("Pendaftaran berhasil.")
    return username

def input_guest():
    nama = input("Masukkan nama: ")
    umur = int(input("Masukkan umur: "))
    return nama, umur

def beli_tiket(username, nama_guest=None):
    print("Wahana yang tersedia:")
    for idx, w in enumerate(wahana.keys(), 1):
        print(f"{idx}. {w}")

    pilihan = int(input("Pilih wahana (masukkan nomor): ")) - 1
    wahana_pilihan = list(wahana.keys())[pilihan]
    harga_per_tiket = 25000

    jumlah_tiket = int(input("Masukkan jumlah tiket: "))

    hari_ini = datetime.datetime.now()
    if hari_ini.weekday() != 5: 
        print("Pemesanan hanya berlaku untuk Sabtu. Redirecting...")
        hari_sabtu = hari_ini + datetime.timedelta(days=(5 - hari_ini.weekday()) % 7)
    else:
        hari_sabtu = hari_ini

    nama_hari_sabtu = calendar.day_name[hari_sabtu.weekday()]  
    nama_hari_sabtu = nama_hari_sabtu.capitalize()  
    minggu_ini = f"{nama_hari_sabtu}, Minggu {hari_sabtu.isocalendar()[1]}"

    if not cek_kuota(tiket_terpesan[wahana_pilihan], minggu_ini):
        minggu_selanjutnya = f"{nama_hari_sabtu}, Minggu {int(minggu_ini.split()[-1]) + 1}"
        print("Kuota minggu ini penuh, redirect ke minggu selanjutnya.")
        minggu_ini = minggu_selanjutnya

    total_harga = jumlah_tiket * harga_per_tiket

    if jumlah_tiket + len(tiket_terpesan[wahana_pilihan].get(minggu_ini, [])) <= 50:
        tiket_terpesan[wahana_pilihan].setdefault(minggu_ini, []).extend([username or nama_guest] * jumlah_tiket)
        print(f"Tiket untuk {wahana_pilihan} berhasil dipesan sebanyak {jumlah_tiket} untuk {minggu_ini}.")
        print(f"Total harga yang harus dibayar: Rp {total_harga:,}")
    else:
        print("Jumlah tiket melebihi kuota minggu ini.")

def menu_user(username):
    while True:
        print("\nMenu User:")
        print("1. Beli Tiket")
        print("2. Ulasan Wahana")
        print("3. Cek Promo")
        print("4. Cancel Tiket")
        print("5. Lihat Ulasan")
        print("6. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            beli_tiket(username)
        elif pilihan == "6":
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
