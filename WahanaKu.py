import datetime
import calendar
import getpass

wahana = {
    "Kora-Kora": 50,
    "Rumah Hantu": 50,
    "Bianglala": 50
}

user_data = {}
tiket_terpesan = {"Kora-Kora": {}, "Rumah Hantu": {}, "Bianglala": {}}
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
# ===========================================================================

# === Fungsi login dan register ===
def login():
    """Login dengan username dan password yang benar.

    Mengembalikan username jika login berhasil, atau None jika gagal.
    
    :returns: username jika login berhasil, atau None jika gagal
    """

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
    """Mendaftarkan pengguna baru.

    Membuat akun pengguna dengan username dan password yang unik.
    Jika username sudah terdaftar, maka akan mengembalikan None.
    Jika berhasil, maka akan menyimpan data pengguna ke file dan
    mengembalikan username yang berhasil didaftarkan."""
    
    username = input("Masukkan username baru: ")
    while not username.isalnum():
        print("Username tidak boleh mengandung spasi atau kosong.")
        username = input("Masukkan username baru: ")
    if username in user_data:
        print("Username sudah terdaftar.")
        return None
    password = getpass.getpass("Masukkan password baru: ")
    while password is '':
        print("Password harus diisi.")
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
# ===========================================================================

# === Fungsi pembelian tiket ===
def beli_tiket(username=None):
    """
    Memproses pembelian tiket untuk pengguna atau guest.

    Params:
    username (str, optional): Nama pengguna yang terdaftar. Jika None, dianggap sebagai guest.
    
    Proses:
    - Memeriksa status VIP pengguna. Pengguna VIP dapat memesan tiket kapan saja, sementara non-VIP hanya dapat memesan pada hari Sabtu.
    - Menampilkan daftar wahana yang tersedia.
    - Memungkinkan pengguna untuk memilih wahana dan jumlah tiket yang ingin dibeli.
    - Menghitung total harga tiket, dengan diskon 25% jika pengguna telah membeli lebih dari 50 tiket.
    - Memeriksa ketersediaan kuota tiket untuk wahana dan minggu yang dipilih.
    - Menyimpan transaksi jika kuota tersedia dan mengurangi saldo pengguna jika saldo mencukupi, atau memberi tahu pengguna jika saldo tidak mencukupi.
    - Menyimpan data pengguna dan histori transaksi ke file.
    """
    
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
    print("Harga 1 tiket wahana adalah Rp25000.")

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
        print("Pilih Metode Pembayaran")
        print("1. Transfer")
        print(f"2. Potong Saldo (Saldo Anda sekarang: Rp {user_data[username]['saldo']:,})")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            print(f"Total harga yang harus dibayar (Guest): Rp {total_harga:,}")
            print("Silakan transfer ke rekening kami:")
            print("A/n Wahana Pasar Malam (9876543210)")
            input("Tekan Enter jika sudah melakukan transfer...")
        elif pilihan == "2":
            print(f"Sisa saldo Anda: Rp {user_data[username]['saldo']:,}")
            if user_data[username]["saldo"] >= total_harga:
                user_data[username]["saldo"] -= total_harga
                user_data[username]["total_tiket"] += jumlah_tiket
                save_users()
                print(f"Total harga yang dibayar: Rp {total_harga:,.0f}")
            else:
                print("Saldo Anda tidak mencukupi. Silakan top-up terlebih dahulu.")
    else:
        print(f"Total harga yang harus dibayar (Guest): Rp {total_harga:,}")
# ===========================================================================

# === Fungsi Lihat Ulasan Pengguna ===
def lihat_ulasan():
    """Menampilkan ulasan pengguna dan memungkinkan penambahan ulasan baru."""
    print("\n=== Ulasan Pengguna ===")
    try:
        with open("reviews.txt", "r") as file:
            reviews = file.readlines()
            if reviews:
                for review in reviews:
                    print(review.strip())
            else:
                print("Belum ada ulasan.")
    except FileNotFoundError:
        print("Belum ada ulasan.")

    print("\nMenu:")
    print("1. Tambahkan Ulasan")
    print("2. Kembali ke Menu Utama")

    pilihan = input("Pilih menu: ")
    if pilihan == "1":
        tambah_ulasan()
    elif pilihan == "2":
        return  # Kembali ke menu utama

def tambah_ulasan():
    """Menambahkan ulasan baru ke file reviews.txt."""
    ulasan = input("Masukkan ulasan Anda: ")
    with open("reviews.txt", "a") as file:
        file.write(f"{ulasan}\n")
    print("Ulasan berhasil ditambahkan.")
    lihat_ulasan()
# ===========================================================================

# === Fungsi lain (top-up, upgrade VIP, dll.) ===

# === Fungsi top-up ===
def top_up(username):
    """
    Menambahkan saldo ke akun pengguna.

    Params:
    username (str): Nama pengguna yang akan di-top-up saldonya.

    Proses:
    - Meminta pengguna memasukkan nominal top-up.
    - Menambahkan nominal ke saldo pengguna.
    - Menyimpan data pengguna setelah top-up.
    - Menampilkan pesan keberhasilan dan saldo terkini.
    """
    nominal = int(input("Masukkan nominal yang ingin di-top-up: "))
    user_data[username]["saldo"] += nominal
    save_users()
    print("Silakan transfer ke rekening kami:")
    print("A/n Wahana Pasar Malam (9876543210)")
    input("Tekan Enter jika sudah melakukan transfer...")
    print(f"Top-up berhasil! Saldo Anda sekarang: Rp {user_data[username]['saldo']:,}")

def upgrade_vip(username):
    """
    Upgrade akun pengguna menjadi VIP.

    Params:
    username (str): Nama pengguna yang akan di-upgrade.

    Proses:
    - Memeriksa apakah pengguna sudah VIP atau belum.
    - Jika belum, memeriksa apakah saldo pengguna mencukupi untuk upgrade.
    - Jika mencukupi, mengurangi saldo pengguna dengan harga upgrade VIP.
    - Menambahkan status VIP ke akun pengguna.
    - Menyimpan data pengguna setelah upgrade.
    - Menampilkan pesan keberhasilan dan saldo terkini.
    """
    if user_data[username]["vip"]:
        print("Anda sudah menjadi pengguna VIP.")
    elif user_data[username]["saldo"] >= HARGA_VIP:
        user_data[username]["saldo"] -= HARGA_VIP
        user_data[username]["vip"] = True
        save_users()
        print(f"Upgrade ke VIP berhasil! Saldo Anda sekarang: Rp {user_data[username]['saldo']:,}")
    else:
        print(f"Saldo Anda tidak mencukupi untuk upgrade VIP. Saldo Anda: Rp {user_data[username]['saldo']:,}")

# === Fungsi cancel tiket ===
def cancel_tiket(username):
    """Membatalkan tiket terakhir yang dibeli oleh pengguna."""
    try:
        with open("transactions.txt", "r") as file:
            transactions = file.readlines()
        
        # Mencari transaksi terbaru milik pengguna
        user_transactions = [t for t in transactions if f"|{username}|" in t]
        
        if not user_transactions:
            print("Tidak ada tiket yang dapat dibatalkan.")
            return
        
        # Mengambil transaksi terbaru
        last_transaction = user_transactions[-1]
        waktu, user, wahana, jumlah_tiket, total_harga = last_transaction.strip().split("|")
        jumlah_tiket = int(jumlah_tiket)
        total_harga = int(total_harga)

        # Menghapus transaksi terbaru dari list
        transactions.remove(last_transaction)

        # Menyimpan kembali transaksi yang telah diupdate
        with open("transactions.txt", "w") as file:
            file.writelines(transactions)

        # Memperbarui saldo dan total tiket pengguna
        user_data[username]["saldo"] += total_harga
        user_data[username]["total_tiket"] -= jumlah_tiket
        save_users()

        print(f"Tiket untuk {wahana} sebanyak {jumlah_tiket} berhasil dibatalkan.")
        print(f"Saldo Anda telah dikembalikan: Rp {total_harga:,.0f}.")
        print(f"Sisa saldo Anda: Rp {user_data[username]['saldo']:,}.")
    except FileNotFoundError:
        print("Belum ada histori pembelian.")
        
# === Fungsi lihat histori ===
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

    print("1. Cancel Tiket Terbaru")
    print("2. Kembali ke Menu Utama")

    pilihan = input("Pilih menu: ")
    if pilihan == "1":
        cancel_tiket(username)
    elif pilihan == "2":
        load_users()

# === Fungsi ganti password ===
def ganti_password(username):
    password_lama = getpass.getpass("Masukkan password lama: ")
    if user_data[username]["password"] == password_lama:
        password_baru = getpass.getpass("Masukkan password baru: ")
        user_data[username]["password"] = password_baru
        save_users()
        print("Password berhasil diubah.")
    else:
        print("Password lama salah.")
        ganti_password(username)
# ===========================================================================

# === Menu Utama ===
def main():
        
    """
    Menu utama aplikasi yang menampilkan pilihan menu
    Login, Masuk sebagai Guest, Daftar (Register), dan Keluar.
    Jika memilih Login atau Masuk sebagai Guest, maka akan masuk
    ke menu user atau guest. Jika memilih Daftar, maka akan
    menampilkan form pendaftaran. Jika memilih Keluar, maka
    akan keluar dari aplikasi.
    """
    load_users()
    print("Selamat datang di Aplikasi Pembelian Tiket Wahana Pasar Malam!")
    while True:
        print("\nMenu Utama:")
        print("1. Login")
        print("2. Masuk sebagai Guest")
        print("3. Daftar (Register)")
        print("4. Lihat Ulasan Pengguna")
        print("5. Keluar")

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
                    print("5. Ganti Password")
                    print("6. Logout")
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
                        ganti_password(username)
                    elif pilihan_user == "6":
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
            lihat_ulasan()
        elif pilihan == "5":
            print("Terima kasih telah menggunakan aplikasi kami!")
            break
        else:
            print("Pilihan tidak valid.")

main()
# ===========================================================================