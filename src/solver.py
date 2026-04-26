import numpy as np
import heapq
from utils import reduce_matrix, calculate_cost
from node import Node
from scipy.spatial.distance import cdist

class TSPSolver:
    # Fungsi untuk membuat data simulasi berupa matriks jarak dan koordinat
    def generate_matrix(self, n, seed=5):
        np.random.seed(seed)  # Mengunci angka acak agar hasil eksperimen konsisten
        coords = np.random.randint(1, 101, size=(n, 2))  # Membuat n titik koordinat X,Y acak (1-100)
        matrix = cdist(coords, coords, metric='euclidean')  # Menghitung jarak lurus (Euclidean) antar semua titik
        np.fill_diagonal(matrix, float('inf'))  # Mengisi diagonal matriks dengan INF agar tidak ke kota sendiri
        return matrix, coords

    def solve_tsp(self, adj_matrix):
        nodes_explored = 0  # Variabel untuk menghitung jumlah simpul yang dieksplorasi (performa)
        n = len(adj_matrix)  # Mengambil jumlah total kota (ukuran matriks)
        adj_matrix = np.array(adj_matrix, dtype=float)  # Memastikan matriks bertipe data float
        original_matrix = adj_matrix.copy()  # Menyimpan matriks asli sebagai referensi jarak nyata

        tree_data = []  # List untuk menyimpan riwayat hubungan simpul (untuk visualisasi pohon)
        node_counter = 1  # Penghitung untuk memberikan ID unik pada setiap simpul baru

        # --- TAHAP PERSIAPAN AKAR (ROOT) ---
        root_matrix, initial_reduction = reduce_matrix(adj_matrix.copy())  # Reduksi awal untuk Lower Bound akar
        root = Node(root_matrix, initial_reduction, [0], 0, 0)  # Membuat objek Node pertama (Kota A/0)
        root.id = node_counter  # Memberikan ID 1 pada simpul akar

        pq = []  # Inisialisasi Priority Queue (Antrean Prioritas)
        heapq.heappush(pq, root)  # Memasukkan simpul akar ke dalam antrean
        tree_data.append((None, root.id, "Start: A", root.cost, False, False))  # Log data akar untuk visualisasi

        best_solution = float('inf')  # Batas atas (Upper Bound) awal diset tak terhingga
        best_path = []  # Variabel untuk menyimpan urutan rute terpendek yang ditemukan

        while pq:
            current_node = heapq.heappop(pq)  # Mengambil simpul dengan cost (Lower Bound) terendah
            nodes_explored += 1  # Menambah hitungan simpul yang diperiksa

            # PRUNING: Jika estimasi biaya simpul ini >= solusi terbaik saat ini, abaikan
            if current_node.cost >= best_solution:
                continue

            # Jika sudah sampai pada level terakhir (semua kota sudah dikunjungi sekali)
            if current_node.level == n - 1:
                last_city = current_node.current_city  # Ambil kota terakhir di rute
                return_dist = original_matrix[last_city, 0]  # Jarak dari kota terakhir kembali ke kota awal (0)
                final_cost = current_node.cost + return_dist  # Hitung total biaya rute lengkap (tour)

                # Jika rute lengkap ini lebih pendek dari yang pernah ada, simpan sebagai yang terbaik
                if final_cost < best_solution:
                    best_solution = final_cost
                    best_path = current_node.path + [0]  # Simpan urutan rute (tambah 0 di akhir)
                continue

            # --- TAHAP PEMBANGKITAN ANAK (BRANCHING) ---
            for next_city in range(n):
                # Jika kota belum ada di dalam jalur yang sedang ditempuh
                if next_city not in current_node.path:
                    node_counter += 1  # Increment ID simpul baru
                    # Hitung biaya reduksi dan matriks baru jika kita pergi ke next_city
                    child_cost, child_matrix = calculate_cost(
                        current_node.matrix,
                        current_node.current_city,
                        next_city,
                        current_node.cost
                    )

                    # Membuat objek Node baru (simpul anak)
                    child_node = Node(child_matrix, child_cost, current_node.path + [next_city], current_node.level + 1, next_city)
                    child_node.id = node_counter  # Berikan ID unik
                    child_node.parent_id = current_node.id  # Catat siapa induknya
                    heapq.heappush(pq, child_node)  # Masukkan simpul anak ke antrean prioritas

                    # Format label rute untuk visualisasi (misal: X1=B)
                    edge_label = f"X{child_node.level}={chr(65 + next_city)}"
                    # Simpan data simpul ke riwayat pohon
                    tree_data.append((current_node.id, child_node.id, edge_label, round(child_cost, 2), False, False))

        # Mengembalikan rute terbaik, total biaya, statistik simpul, dan data pohon visual
        return best_path, best_solution, nodes_explored, tree_data