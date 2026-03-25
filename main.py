import numpy as np
import heapq
from utils import reduce_matrix, calculate_cost
from node import Node
import time
from scipy.spatial.distance import cdist

#
# def solve_tsp(adj_matrix):
#     n = len(adj_matrix)
#     adj_matrix = np.array(adj_matrix, dtype=float)
#
#     # Inisialisasi Root
#     root_matrix = adj_matrix.copy()
#     initial_matrix, initial_reduction = reduce_matrix(root_matrix)
#
#     root = Node(initial_matrix, initial_reduction, [0], 0, 0)
#
#     # Priority Queue (LCS Strategy)
#     pq = []
#     heapq.heappush(pq, root)
#
#     best_solution = float('inf')
#     best_path = []
#
#     while pq:
#         # Ambil simpul dengan LB terkecil
#         current_node = heapq.heappop(pq)
#
#         # Pruning
#         if current_node.cost >= best_solution:
#             continue
#
#         # Jika sudah sampai level terakhir (semua kota dikunjungi)
#         if current_node.level == n - 1:
#             # Ambil biaya dari kota saat ini kembali ke kota 0
#             last_to_start_cost = current_node.matrix[current_node.current_city, 0]
#             final_cost = current_node.cost + last_to_start_cost
#             if final_cost < best_solution:
#                 best_solution = final_cost
#                 best_path = current_node.path + [0]
#             continue
#
#         # Branching
#         for next_city in range(n):
#             if next_city not in current_node.path:
#                 # Hitung LB untuk simpul anak
#                 child_cost, child_matrix = calculate_cost(
#                     current_node.matrix,
#                     current_node.current_city,
#                     next_city,
#                     current_node.cost
#                 )
#
#                 child_node = Node(
#                     child_matrix,
#                     child_cost,
#                     current_node.path + [next_city],
#                     current_node.level + 1,
#                     next_city
#                 )
#
#                 # Push ke PQ jika berpotensi lebih baik (Pruning awal)
#                 if child_node.cost < best_solution:
#                     heapq.heappush(pq, child_node)
#
#     return best_path, best_solution

def solve_tsp(adj_matrix):
    nodes_explored = 0
    n = len(adj_matrix)
    adj_matrix = np.array(adj_matrix, dtype=float)

    # Simpan salinan matriks asli untuk menghitung biaya rute terakhir nanti
    original_matrix = adj_matrix.copy()

    # Inisialisasi Root
    root_matrix = adj_matrix.copy()
    initial_matrix, initial_reduction = reduce_matrix(root_matrix)

    # Node(matrix, cost, path, level, current_city)
    root = Node(initial_matrix, initial_reduction, [0], 0, 0)

    pq = []
    heapq.heappush(pq, root)

    best_solution = float('inf')
    best_path = []

    while pq:
        current_node = heapq.heappop(pq)
        nodes_explored += 1 # Setiap pop, hitung sebagai simpul yang dieksplorasi

        if current_node.cost >= best_solution:
            continue

        # Jika sudah mengunjungi SEMUA kota (n-1 kota tujuan + kota asal)
        if current_node.level == n - 1:
            # Ambil jarak asli dari kota terakhir ke kota 0
            last_city = current_node.current_city
            return_dist = original_matrix[last_city, 0]

            # Total cost adalah cost akumulasi + jarak kembali ke 0
            final_cost = current_node.cost + return_dist

            if final_cost < best_solution:
                best_solution = final_cost
                best_path = current_node.path + [0]
            continue

        for next_city in range(n):
            if next_city not in current_node.path:
                child_cost, child_matrix = calculate_cost(
                    current_node.matrix,
                    current_node.current_city,
                    next_city,
                    current_node.cost
                )

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

def generate_matrix(n, seed=42):
    np.random.seed(seed)
    # Membuat koordinat X dan Y (1-100)
    coords = np.random.randint(1, 101, size=(n, 2))

    # Menggunakan cdist yang sudah diimport di atas
    matrix = cdist(coords, coords, metric='euclidean')
    np.fill_diagonal(matrix, float('inf'))
    return matrix




if __name__ == "__main__":
    # Ganti jumlah kota di sini
    n_kota = 5
    seed_value = 42

    print(f"=== EKSPERIMEN TSP: {n_kota} KOTA (SEED: {seed_value}) ===")

    # 1. Generate Koordinat secara eksplisit untuk ditampilkan
    np.random.seed(seed_value)
    coords = np.random.randint(1, 101, size=(n_kota, 2))

    print("\n1. KOORDINAT KOTA (X, Y):")
    for i, (x, y) in enumerate(coords):
        print(f"   Kota {i}: ({x}, {y})")

    # 2. Generate Matriks Jarak
    matrix = generate_matrix(n_kota, seed=seed_value)

    print("\n2. MATRIKS JARAK ANTAR KOTA (Euclidean):")
    # Header kolom
    header = "      " + "".join([f"K{i:<7}" for i in range(n_kota)])
    print(header)
    print("-" * len(header))

    for i in range(n_kota):
        row_str = f"K{i:<4} | "
        for j in range(n_kota):
            val = matrix[i][j]
            if val == float('inf'):
                row_str += f"{'inf':<7} "
            else:
                row_str += f"{val:<7.2f} "
        print(row_str)

    print("\n3. PROSES PENCARIAN RUTE TERPENDEK...")

    # 3. Jalankan Algoritma
    start_time = time.perf_counter()
    # UBAH BARIS DI BAWAH INI (Tambahkan nodes_count)
    path, cost, nodes_count = solve_tsp(matrix)
    end_time = time.perf_counter()

    duration = end_time - start_time

    print("\n4. HASIL AKHIR:")
    print(f"   Rute Terpendek : {path}")
    print(f"   Total Jarak    : {cost:.2f}")
    print(f"   Simpul Dieksplorasi : {nodes_count}")
    print(f"   Waktu Proses   : {duration:.6f} detik")