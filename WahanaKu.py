import datetime

wahana = {
    "Komedi Putar": 50,
    "Rumah Hantu": 50,
    "Bianglala": 50
}

user_data = {}
tiket_terpesan = {"Komedi Putar": {}, "Rumah Hantu": {}, "Bianglala": {}}

def cek_kuota(wahana, minggu):
    return wahana[minggu] < 50

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
        "promo": True
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

    jumlah_tiket = int(input("Masukkan jumlah tiket: "))


    hari_ini = datetime.datetime.now().weekday() 
    if hari_ini != 5: 
        print("Pemesanan hanya berlaku untuk Sabtu. Redirecting...")
        hari_ini = 5

    minggu_ini = f"Minggu_{datetime.datetime.now().isocalendar()[1]}"
    
    if not cek_kuota(tiket_terpesan[wahana_pilihan], minggu_ini):
        minggu_selanjutnya = f"Minggu_{int(minggu_ini.split('_')[1]) + 1}"
        print("Kuota minggu ini penuh, redirect ke minggu selanjutnya.")
        minggu_ini = minggu_selanjutnya
    
    if jumlah_tiket + len(tiket_terpesan[wahana_pilihan].get(minggu_ini, [])) <= 50:
        tiket_terpesan[wahana_pilihan].setdefault(minggu_ini, []).extend([username] * jumlah_tiket)
        print(f"Tiket untuk {wahana_pilihan} berhasil dipesan sebanyak {jumlah_tiket} untuk {minggu_ini}.")
    else:
        print("Jumlah tiket melebihi kuota minggu ini.")


def main():
    print("Selamat datang di Aplikasi Pembelian Tiket Wahana Pasar Malam!")
    while True:
        print("\nMenu Utama:")
        print("1. Login")
        print("2. Daftar (Register)")
        print("3. Masuk sebagai Guest")
        print("4. Beli Tiket")
        print("5. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            username = login()
        elif pilihan == "2":
            username = register()
        elif pilihan == "3":
            nama_guest, umur_guest = input_guest()
            username = None
        elif pilihan == "4":
            if username:
                beli_tiket(username)
            elif nama_guest:
                beli_tiket(username, nama_guest)
            else:
                print("Silakan login atau masuk sebagai guest terlebih dahulu.")
        else:
            print("Pilihan tidak valid.")

main()
