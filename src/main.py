import numpy as np
import heapq
from utils import reduce_matrix, calculate_cost
from node import Node
import time
import os
import sys
from scipy.spatial.distance import cdist

# Fungsi utama untuk menyelesaikan TSP dengan Branch and Bound
def solve_tsp(adj_matrix):
    nodes_explored = 0                     # Menghitung jumlah simpul yang diproses (Metrik Kinerja)
    n = len(adj_matrix)                    # Mendapatkan jumlah total kota
    adj_matrix = np.array(adj_matrix, dtype=float)

    # Simpan salinan matriks asli (diperlukan untuk menghitung jarak kembali ke kota 0 di akhir)
    original_matrix = adj_matrix.copy()

    # --- INISIALISASI SIMPUL AKAR (ROOT) ---
    root_matrix = adj_matrix.copy()
    # Lakukan reduksi awal untuk mendapatkan Lower Bound pertama
    initial_matrix, initial_reduction = reduce_matrix(root_matrix)

    # Buat objek Node pertama (Kota awal: 0, level: 0)
    root = Node(initial_matrix, initial_reduction, [0], 0, 0)

    # Masukkan root ke dalam Priority Queue
    pq = []
    heapq.heappush(pq, root)

    best_solution = float('inf')           # Inisialisasi solusi terbaik sementara sebagai tak terhingga
    best_path = []                         # Inisialisasi rute terbaik sementara

    # --- PROSES PENCARIAN (TRAVERSAL) ---
    while pq:
        # Ambil simpul dengan biaya (LB) terendah dari antrean (Strategi LCS)
        current_node = heapq.heappop(pq)
        nodes_explored += 1                # Catat bahwa satu simpul telah dievaluasi

        # MEKANISME PRUNING: Jika biaya simpul ini sudah >= solusi terbaik, abaikan (pangkas)
        if current_node.cost >= best_solution:
            continue

        # CEK APAKAH RUTE SUDAH LENGKAP (Sudah mengunjungi n-1 kota tujuan)
        if current_node.level == n - 1:
            last_city = current_node.current_city
            # Hitung jarak dari kota terakhir kembali ke kota awal (Kota 0)
            return_dist = original_matrix[last_city, 0]
            final_cost = current_node.cost + return_dist

            # Jika rute lengkap ini lebih murah dari rute terbaik sebelumnya, update!
            if final_cost < best_solution:
                best_solution = final_cost
                best_path = current_node.path + [0]
            continue

        # MEKANISME BRANCHING: Coba kunjungi setiap kota yang belum ada di dalam path
        for next_city in range(n):
            if next_city not in current_node.path:
                # Hitung biaya estimasi (LB) untuk anak simpul baru
                child_cost, child_matrix = calculate_cost(
                    current_node.matrix,
                    current_node.current_city,
                    next_city,
                    current_node.cost
                )

                # PRUNING AWAL: Hanya masukkan ke PQ jika estimasi biayanya lebih kecil dari best_solution
                if child_cost < best_solution:
                    child_node = Node(
                        child_matrix,
                        child_cost,
                        current_node.path + [next_city],
                        current_node.level + 1,
                        next_city
                    )
                    heapq.heappush(pq, child_node)

    return best_path, best_solution, nodes_explored

# Fungsi untuk membuat data simulasi (Kota & Jarak)
def generate_matrix(n, seed=42):
    np.random.seed(seed)                   # Mengunci random agar hasil konsisten (penting untuk penelitian)
    # Membuat koordinat X dan Y acak di bidang 100x100
    coords = np.random.randint(1, 101, size=(n, 2))

    # Hitung jarak Euclidean antar koordinat tersebut (Hasilnya Matriks n x n)
    matrix = cdist(coords, coords, metric='euclidean')
    # Set diagonal (jarak ke diri sendiri) menjadi infinity agar tidak dipilih
    np.fill_diagonal(matrix, float('inf'))
    return matrix


if __name__ == "__main__":
    # 1. Daftar jumlah kota yang ingin diuji
    variasi_n = [5, 10, 15, 20]
    seed_value = 42

    # 2. Buat folder utama hasil eksperimen
    parent_folder = "hasil_eksperimen_skripsi"
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    print(f"Memulai eksperimen untuk n = {variasi_n}...")
    print(f"Hasil akan disimpan di folder: {parent_folder}")

    for n_kota in variasi_n:
        # Buat sub-folder untuk masing-masing jumlah kota
        folder_n = os.path.join(parent_folder, f"{n_kota}_kota")
        if not os.path.exists(folder_n):
            os.makedirs(folder_n)

        # Nama file log untuk masing-masing n
        file_log = os.path.join(folder_n, f"report_n{n_kota}.txt")

        # Mengalihkan Output Print ke File
        with open(file_log, 'w') as f:
            # Simpan referensi terminal asli
            original_stdout = sys.stdout
            sys.stdout = f  # Mulai menulis ke file

            # --- MULAI PROSES SEPERTI BIASA ---
            print(f"=== EKSPERIMEN TSP: {n_kota} KOTA (SEED: {seed_value}) ===")

            np.random.seed(seed_value)
            coords = np.random.randint(1, 101, size=(n_kota, 2))
            print("\n1. KOORDINAT KOTA (X, Y):")
            for i, (x, y) in enumerate(coords):
                print(f"   Kota {i}: ({x}, {y})")

            matrix = generate_matrix(n_kota, seed=seed_value)

            print("\n2. MATRIKS JARAK ANTAR KOTA (Euclidean):")
            header = "      " + "".join([f"K{i:<7}" for i in range(n_kota)])
            print(header)
            print("-" * len(header))
            for i in range(n_kota):
                row_str = f"K{i:<4} | "
                for j in range(n_kota):
                    val = matrix[i][j]
                    row_str += f"{val:<7.2f} " if val != float('inf') else f"{'inf':<7} "
                print(row_str)

            print("\n3. PROSES PENCARIAN RUTE TERPENDEK...")
            start_time = time.perf_counter()
            path, cost, nodes_count = solve_tsp(matrix)
            end_time = time.perf_counter()
            duration = end_time - start_time

            print("\n4. HASIL AKHIR:")
            print(f"   Rute Terpendek : {path}")
            print(f"   Total Jarak    : {cost:.2f}")
            print(f"   Simpul Dieksplorasi : {nodes_count}")
            print(f"   Waktu Proses   : {duration:.6f} detik")

            # Kembalikan output ke terminal setelah selesai satu iterasi
            sys.stdout = original_stdout

        print(f" Selesai: {n_kota} kota. Data tersimpan di {file_log}")

    print("\nSeluruh eksperimen selesai.")