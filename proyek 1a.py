import random
import time
 
 
class Produk:
    def __init__(self, id_produk, nama, kategori, harga, stok):
        self.id_produk = id_produk
        self.nama = nama
        self.kategori = kategori
        self.harga = harga
        self.stok = stok
 
    def __str__(self):
        return f"{self.id_produk} | {self.nama} | {self.kategori} | Rp{self.harga:,} | stok: {self.stok}"
 
 
class Inventaris:
    def tambah_produk(self, produk):
        pass
 
    def cari_produk(self, id_produk):
        pass
 
    def hapus_produk(self, id_produk):
        pass
 
    def semua_produk(self):
        pass
 
    def jumlah(self):
        pass
 
    # dua method di bawah hanya dipakai untuk benchmark
    def isi_data(self, daftar):
        pass
 
    def tambah_cepat(self, produk):
        pass
 
 
# 1. Array List
class InventarisArray(Inventaris):
    def __init__(self):
        self.data = []
 
    def tambah_produk(self, produk):
        # cek dulu ID nya sudah ada atau belum -> O(n)
        if self.cari_produk(produk.id_produk) is not None:
            return False
        self.data.append(produk)
        return True
 
    def cari_produk(self, id_produk):
        # linear search -> O(n)
        for p in self.data:
            if p.id_produk == id_produk:
                return p
        return None
 
    def hapus_produk(self, id_produk):
        # cari dulu (O(n)), lalu pop menggeser elemen (O(n))
        for i in range(len(self.data)):
            if self.data[i].id_produk == id_produk:
                self.data.pop(i)
                return True
        return False
 
    def semua_produk(self):
        return list(self.data)
 
    def jumlah(self):
        return len(self.data)
 
    def isi_data(self, daftar):
        self.data.extend(daftar)
 
    def tambah_cepat(self, produk):
        self.data.append(produk)
 
 
# 2. Linked List
class Node:
    def __init__(self, produk):
        self.produk = produk
        self.next = None
 
 
class InventarisLinkedList(Inventaris):
    def __init__(self):
        self.head = None
        self.tail = None
        self.ukuran = 0
 
    def tambah_produk(self, produk):
        # cek ID dulu -> O(n)
        if self.cari_produk(produk.id_produk) is not None:
            return False
        self.tambah_cepat(produk)
        return True
 
    def cari_produk(self, id_produk):
        # jalan dari node pertama sampai ketemu -> O(n)
        sekarang = self.head
        while sekarang is not None:
            if sekarang.produk.id_produk == id_produk:
                return sekarang.produk
            sekarang = sekarang.next
        return None
 
    def hapus_produk(self, id_produk):
        # cari node nya (O(n)), melepas node itu sendiri cuma O(1)
        sebelum = None
        sekarang = self.head
        while sekarang is not None:
            if sekarang.produk.id_produk == id_produk:
                if sebelum is None:
                    self.head = sekarang.next
                else:
                    sebelum.next = sekarang.next
                if sekarang == self.tail:
                    self.tail = sebelum
                self.ukuran -= 1
                return True
            sebelum = sekarang
            sekarang = sekarang.next
        return False
 
    def semua_produk(self):
        hasil = []
        sekarang = self.head
        while sekarang is not None:
            hasil.append(sekarang.produk)
            sekarang = sekarang.next
        return hasil
 
    def jumlah(self):
        return self.ukuran
 
    def isi_data(self, daftar):
        for p in daftar:
            self.tambah_cepat(p)
 
    def tambah_cepat(self, produk):
        # taruh di belakang lewat tail -> O(1)
        baru = Node(produk)
        if self.head is None:
            self.head = baru
        else:
            self.tail.next = baru
        self.tail = baru
        self.ukuran += 1
 
 
# 3. Hash Table (yang dipilih)
class InventarisHashTable(Inventaris):
    def __init__(self):
        self.data = {}   # key = ID produk, value = objek Produk
 
    def tambah_produk(self, produk):
        if produk.id_produk in self.data:
            return False
        self.data[produk.id_produk] = produk   # rata-rata O(1)
        return True
 
    def cari_produk(self, id_produk):
        return self.data.get(id_produk)        # rata-rata O(1)
 
    def hapus_produk(self, id_produk):
        if id_produk in self.data:
            del self.data[id_produk]           # rata-rata O(1)
            return True
        return False
 
    def semua_produk(self):
        return list(self.data.values())
 
    def jumlah(self):
        return len(self.data)
 
    def isi_data(self, daftar):
        for p in daftar:
            self.data[p.id_produk] = p
 
    def tambah_cepat(self, produk):
        self.data[produk.id_produk] = produk
 
 
# Benchmark
def buat_data(n):
    daftar = []
    for i in range(n):
        daftar.append(Produk("P%07d" % i, "Produk " + str(i), "Umum", 10000 + i, 10))
    return daftar
 
 
def ukur(kelas, n, ulang=100):
    # hasilnya rata-rata waktu per operasi dalam mikrodetik
    random.seed(42)
    data = buat_data(n)
    inv = kelas()
    inv.isi_data(data)
    acak = random.sample(range(n), ulang)
 
    # cari
    mulai = time.perf_counter()
    for i in acak:
        inv.cari_produk(data[i].id_produk)
    t_cari = (time.perf_counter() - mulai) / ulang * 1e6
 
    # hapus (setelah dihapus dimasukkan lagi, waktunya tidak dihitung)
    total = 0
    for i in acak:
        mulai = time.perf_counter()
        inv.hapus_produk(data[i].id_produk)
        total += time.perf_counter() - mulai
        inv.tambah_cepat(data[i])
    t_hapus = total / ulang * 1e6
 
    # tambah (produk baru, lalu dihapus lagi, waktu hapus tidak dihitung)
    total = 0
    for k in range(ulang):
        baru = Produk("BARU%05d" % k, "Produk Baru", "Umum", 5000, 1)
        mulai = time.perf_counter()
        inv.tambah_produk(baru)
        total += time.perf_counter() - mulai
        inv.hapus_produk(baru.id_produk)
    t_tambah = total / ulang * 1e6
 
    return t_tambah, t_cari, t_hapus
 
 
def benchmark():
    daftar_struktur = [
        ("Array List", InventarisArray),
        ("Linked List", InventarisLinkedList),
        ("Hash Table", InventarisHashTable),
    ]
    print("\nHasil benchmark (rata-rata waktu per operasi, satuan mikrodetik)")
    for n in [1000, 10000, 100000]:
        print("\nJumlah produk:", n)
        print("%-14s%14s%14s%14s" % ("Struktur", "Tambah", "Cari", "Hapus"))
        for nama, kelas in daftar_struktur:
            t, c, h = ukur(kelas, n)
            print("%-14s%14.2f%14.2f%14.2f" % (nama, t, c, h))
 
 
# ---------- Program utama (CLI) ----------
def input_angka(teks):
    while True:
        try:
            angka = int(input(teks))
            if angka < 0:
                print("Tidak boleh negatif!")
            else:
                return angka
        except ValueError:
            print("Masukkan angka ya!")
 
 
def menu_tambah(inv):
    print("\n-- Tambah Produk --")
    id_produk = input("ID Produk : ").strip()
    if id_produk == "":
        print("ID tidak boleh kosong!")
        return
    nama = input("Nama      : ")
    kategori = input("Kategori  : ")
    harga = input_angka("Harga     : ")
    stok = input_angka("Stok      : ")
    if inv.tambah_produk(Produk(id_produk, nama, kategori, harga, stok)):
        print("Produk berhasil ditambahkan.")
    else:
        print("Gagal, ID produk sudah ada.")
 
 
def menu_cari(inv):
    print("\n-- Cari Produk --")
    produk = inv.cari_produk(input("ID Produk: ").strip())
    if produk is None:
        print("Produk tidak ditemukan.")
    else:
        print("Ditemukan:", produk)
 
 
def menu_hapus(inv):
    print("\n-- Hapus Produk --")
    if inv.hapus_produk(input("ID Produk: ").strip()):
        print("Produk berhasil dihapus.")
    else:
        print("Produk tidak ditemukan.")
 
 
def menu_tampil(inv):
    print("\n-- Daftar Produk (total %d) --" % inv.jumlah())
    for p in inv.semua_produk():
        print(p)
 
 
def main():
    inv = InventarisHashTable()
    # data contoh
    inv.tambah_produk(Produk("P001", "Laptop Asus", "Elektronik", 8500000, 12))
    inv.tambah_produk(Produk("P002", "Mouse Wireless", "Aksesoris", 150000, 80))
    inv.tambah_produk(Produk("P003", "Kemeja Batik", "Fashion", 250000, 40))
 
    while True:
        print("\n===== INVENTARIS PRODUK =====")
        print("1. Tambah produk")
        print("2. Cari produk (by ID)")
        print("3. Hapus produk")
        print("4. Tampilkan semua produk")
        print("5. Benchmark (Array vs Linked List vs Hash Table)")
        print("0. Keluar")
        pilih = input("Pilih menu: ").strip()
 
        if pilih == "1":
            menu_tambah(inv)
        elif pilih == "2":
            menu_cari(inv)
        elif pilih == "3":
            menu_hapus(inv)
        elif pilih == "4":
            menu_tampil(inv)
        elif pilih == "5":
            benchmark()
        elif pilih == "0":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak ada.")
 
 
if __name__ == "__main__":
    main()