class Node:
    # Fungsi __init__ adalah konstruktor untuk membuat objek "simpul" baru
    def __init__(self, matrix, cost, path, level, current_city):
        # Menyimpan kondisi matriks jarak yang sudah dikurangi (direduksi) untuk simpul ini
        # Matriks ini berbeda-beda untuk setiap rute yang sedang dicoba
        self.matrix = matrix

        # Menyimpan nilai Batas Bawah (Lower Bound).
        # Ini adalah estimasi total jarak terpendek yang mungkin dicapai dari jalur ini
        self.cost = cost

        # Menyimpan daftar urutan kota yang sudah dikunjungi (misal: [0, 2, 4])
        # Gunanya agar kita tahu riwayat perjalanan rute ini
        self.path = path

        # Menunjukkan tingkat kedalaman simpul dalam pohon (dimulai dari 0)
        # Jika level == n-1, artinya semua kota sudah dikunjungi
        self.level = level

        # Menyimpan indeks kota di mana agen berada sekarang (titik terakhir di dalam path)
        self.current_city = current_city

    # Fungsi khusus agar modul 'heapq' (Priority Queue) bisa membandingkan dua Node
    # '__lt__' berarti 'Less Than' (Kurang Dari)
    def __lt__(self, other):
        # Membandingkan cost (LB) simpul ini dengan simpul lain (other)
        # Jika True, maka simpul ini akan diletakkan di depan antrean untuk diproses duluan
        # Inilah yang menjalankan strategi "Least Cost Search" (LCS)
        return self.cost < other.cost