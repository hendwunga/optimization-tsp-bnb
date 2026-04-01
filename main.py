import numpy as np
import heapq
from utils import reduce_matrix, calculate_cost
from node import Node
import time
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
    n_kota = 10                             # Tentukan jumlah kota untuk eksperimen ini
    seed_value = 42

    print(f"=== EKSPERIMEN TSP: {n_kota} KOTA (SEED: {seed_value}) ===")

    # Tampilkan Koordinat (Untuk validasi perhitungan manual jika diminta penguji)
    np.random.seed(seed_value)
    coords = np.random.randint(1, 101, size=(n_kota, 2))
    print("\n1. KOORDINAT KOTA (X, Y):")
    for i, (x, y) in enumerate(coords):
        print(f"   Kota {i}: ({x}, {y})")

    # Siapkan data matriks jarak
    matrix = generate_matrix(n_kota, seed=seed_value)

    # Cetak matriks jarak (untuk lampiran Bab IV)
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

    # Jalankan algoritma dan ukur waktunya
    start_time = time.perf_counter()       # Mulai hitung waktu
    path, cost, nodes_count = solve_tsp(matrix)
    end_time = time.perf_counter()         # Selesai hitung waktu

    duration = end_time - start_time

    # Tampilkan Hasil Akhir
    print("\n4. HASIL AKHIR:")
    print(f"   Rute Terpendek : {path}")
    print(f"   Total Jarak    : {cost:.2f}")
    print(f"   Simpul Dieksplorasi : {nodes_count}")
    print(f"   Waktu Proses   : {duration:.6f} detik")