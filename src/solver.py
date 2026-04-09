import numpy as np
import heapq
from utils import reduce_matrix, calculate_cost
from node import Node
from scipy.spatial.distance import cdist

class TSPSolver:
    def generate_matrix(self, n, seed=42):
        np.random.seed(seed)
        coords = np.random.randint(1, 101, size=(n, 2))
        matrix = cdist(coords, coords, metric='euclidean')
        np.fill_diagonal(matrix, float('inf'))
        return matrix, coords

    def solve_tsp(self, adj_matrix):
        nodes_explored = 0
        n = len(adj_matrix)
        adj_matrix = np.array(adj_matrix, dtype=float)
        original_matrix = adj_matrix.copy()

        tree_data = []
        node_counter = 1

        root_matrix, initial_reduction = reduce_matrix(adj_matrix.copy())
        root = Node(root_matrix, initial_reduction, [0], 0, 0)
        root.id = node_counter

        pq = []
        heapq.heappush(pq, root)
        tree_data.append((None, root.id, "Start: A", root.cost, False, False))

        best_solution = float('inf')
        best_path = []

        while pq:
            current_node = heapq.heappop(pq)
            nodes_explored += 1

            if current_node.cost >= best_solution:
                continue

            if current_node.level == n - 1:
                last_city = current_node.current_city
                return_dist = original_matrix[last_city, 0]
                final_cost = current_node.cost + return_dist

                if final_cost < best_solution:
                    best_solution = final_cost
                    best_path = current_node.path + [0]
                continue

            for next_city in range(n):
                if next_city not in current_node.path:
                    node_counter += 1
                    child_cost, child_matrix = calculate_cost(
                        current_node.matrix,
                        current_node.current_city,
                        next_city,
                        current_node.cost
                    )

                    child_node = Node(child_matrix, child_cost, current_node.path + [next_city], current_node.level + 1, next_city)
                    child_node.id = node_counter
                    child_node.parent_id = current_node.id
                    heapq.heappush(pq, child_node)

                    edge_label = f"X{child_node.level}={chr(65 + next_city)}"
                    tree_data.append((current_node.id, child_node.id, edge_label, round(child_cost, 2), False, False))

        return best_path, best_solution, nodes_explored, tree_data


# import numpy as np
# import heapq
# from utils import reduce_matrix, calculate_cost
# from node import Node
# from scipy.spatial.distance import cdist # Import ini jangan lupa
#
# class TSPSolver:
#     # --- FUNGSI GENERATE DATA (Wajib Ada untuk main.py) ---
#     def generate_matrix(self, n, seed=42):
#         np.random.seed(seed)
#         # Menghasilkan koordinat acak
#         coords = np.random.randint(1, 101, size=(n, 2))
#         # Menggunakan cdist untuk menghitung matriks jarak Euclidean secara efisien
#         matrix = cdist(coords, coords, metric='euclidean')
#         # Isi diagonal dengan infinity agar tidak mengunjungi diri sendiri
#         np.fill_diagonal(matrix, float('inf'))
#         return matrix, coords
#
#     # --- TRIK 1: Greedy Search (Mendapatkan Upper Bound awal) ---
#     def _get_greedy_bound(self, matrix):
#         n = len(matrix)
#         curr = 0
#         visited = {curr}
#         total_cost = 0
#         for _ in range(n - 1):
#             next_city = -1
#             min_dist = float('inf')
#             for j in range(n):
#                 if j not in visited and matrix[curr, j] < min_dist:
#                     min_dist = matrix[curr, j]
#                     next_city = j
#             if next_city != -1:
#                 total_cost += min_dist
#                 visited.add(next_city)
#                 curr = next_city
#         total_cost += matrix[curr, 0] # Kembali ke kota awal
#         return total_cost
#
#     def solve_tsp(self, adj_matrix):
#         nodes_explored = 0
#         n = len(adj_matrix)
#         # Gunakan float32 untuk menghemat RAM pada n besar
#         adj_matrix = np.array(adj_matrix, dtype=np.float32)
#         original_matrix = adj_matrix.copy()
#
#         # Inisialisasi best_solution dengan rute Greedy agar Pruning maksimal
#         best_solution = self._get_greedy_bound(original_matrix)
#         best_path = []
#
#         # Hitung reduksi awal untuk simpul akar (Root)
#         root_matrix, initial_reduction = reduce_matrix(adj_matrix.copy())
#         root = Node(root_matrix, initial_reduction, [0], 0, 0)
#         root.id = 1
#
#         pq = [root]
#         tree_data = []
#
#         while pq:
#             current_node = heapq.heappop(pq)
#             nodes_explored += 1
#
#             # Pruning: Jika biaya simpul sudah lebih buruk dari solusi terbaik, abaikan
#             if current_node.cost >= best_solution:
#                 continue
#
#             # Jika sudah mencapai semua kota
#             if current_node.level == n - 1:
#                 last_city = current_node.current_city
#                 return_dist = original_matrix[last_city, 0]
#                 final_cost = current_node.cost + return_dist
#
#                 if final_cost < best_solution:
#                     best_solution = final_cost
#                     # Pastikan ini menyimpan urutan kota dari root sampai kembali ke 0
#                     best_path = current_node.path + [0]
#                 continue
#
#             # --- TRIK 2: Heuristic Branching (Urutkan anak yang jaraknya paling dekat) ---
#             children_candidates = []
#             for next_city in range(n):
#                 if next_city not in current_node.path:
#                     priority = original_matrix[current_node.current_city, next_city]
#                     children_candidates.append((priority, next_city))
#
#             # Urutkan berdasarkan jarak terkecil
#             children_candidates.sort()
#
#             for _, next_city in children_candidates:
#                 child_cost, child_matrix = calculate_cost(
#                     current_node.matrix,
#                     current_node.current_city,
#                     next_city,
#                     current_node.cost
#                 )
#
#                 # --- TRIK 3: Pre-Push Pruning ---
#                 if child_cost < best_solution:
#                     child_node = Node(child_matrix, child_cost, current_node.path + [next_city], current_node.level + 1,
#                                       next_city)
#                     child_node.id = nodes_explored + len(pq) + 1
#                     heapq.heappush(pq, child_node)
#
#                     # Simpan data pohon hanya untuk n kecil agar memori tidak bocor
#                     if n <= 10:
#                         edge_label = f"X{child_node.level}={chr(65 + next_city)}"
#                         tree_data.append(
#                             (current_node.id, child_node.id, edge_label, round(child_cost, 2), False, False))
#
#         return best_path, best_solution, nodes_explored, tree_data