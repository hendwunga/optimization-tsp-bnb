# import numpy as np
# import heapq
# from utils import reduce_matrix, calculate_cost
# from node import Node
# import time
# import os
# import sys
# from scipy.spatial.distance import cdist
# import math
#
# # Fungsi utama untuk menyelesaikan TSP dengan Branch and Bound
# def solve_tsp(adj_matrix):
#     nodes_explored = 0                     # Menghitung jumlah simpul yang diproses (Metrik Kinerja)
#     n = len(adj_matrix)                    # Mendapatkan jumlah total kota
#     adj_matrix = np.array(adj_matrix, dtype=float)
#
#     # Simpan salinan matriks asli (diperlukan untuk menghitung jarak kembali ke kota 0 di akhir)
#     original_matrix = adj_matrix.copy()
#
#     # --- INISIALISASI SIMPUL AKAR (ROOT) ---
#     root_matrix = adj_matrix.copy()
#     # Lakukan reduksi awal untuk mendapatkan Lower Bound pertama
#     initial_matrix, initial_reduction = reduce_matrix(root_matrix)
#
#     # Buat objek Node pertama (Kota awal: 0, level: 0)
#     root = Node(initial_matrix, initial_reduction, [0], 0, 0)
#
#     # Masukkan root ke dalam Priority Queue
#     pq = []
#     heapq.heappush(pq, root)
#
#     best_solution = float('inf')           # Inisialisasi solusi terbaik sementara sebagai tak terhingga
#     best_path = []                         # Inisialisasi rute terbaik sementara
#
#     # --- PROSES PENCARIAN (TRAVERSAL) ---
#     while pq:
#         # Ambil simpul dengan biaya (LB) terendah dari antrean (Strategi LCS)
#         current_node = heapq.heappop(pq)
#         nodes_explored += 1                # Catat bahwa satu simpul telah dievaluasi
#
#         # MEKANISME PRUNING: Jika biaya simpul ini sudah >= solusi terbaik, abaikan (pangkas)
#         if current_node.cost >= best_solution:
#             continue
#
#         # CEK APAKAH RUTE SUDAH LENGKAP (Sudah mengunjungi n-1 kota tujuan)
#         if current_node.level == n - 1:
#             last_city = current_node.current_city
#             # Hitung jarak dari kota terakhir kembali ke kota awal (Kota 0)
#             return_dist = original_matrix[last_city, 0]
#             final_cost = current_node.cost + return_dist
#
#             # Jika rute lengkap ini lebih murah dari rute terbaik sebelumnya, update!
#             if final_cost < best_solution:
#                 best_solution = final_cost
#                 best_path = current_node.path + [0]
#             continue
#
#         # MEKANISME BRANCHING: Coba kunjungi setiap kota yang belum ada di dalam path
#         for next_city in range(n):
#             if next_city not in current_node.path:
#                 # Hitung biaya estimasi (LB) untuk anak simpul baru
#                 child_cost, child_matrix = calculate_cost(
#                     current_node.matrix,
#                     current_node.current_city,
#                     next_city,
#                     current_node.cost
#                 )
#
#                 # PRUNING AWAL: Hanya masukkan ke PQ jika estimasi biayanya lebih kecil dari best_solution
#                 if child_cost < best_solution:
#                     child_node = Node(
#                         child_matrix,
#                         child_cost,
#                         current_node.path + [next_city],
#                         current_node.level + 1,
#                         next_city
#                     )
#                     heapq.heappush(pq, child_node)
#
#     return best_path, best_solution, nodes_explored
#
# # Fungsi untuk membuat data simulasi (Kota & Jarak)
# def generate_matrix(n, seed=42):
#     np.random.seed(seed)                   # Mengunci random agar hasil konsisten (penting untuk penelitian)
#     # Membuat koordinat X dan Y acak di bidang 100x100
#     coords = np.random.randint(1, 101, size=(n, 2))
#
#     # Hitung jarak Euclidean antar koordinat tersebut (Hasilnya Matriks n x n)
#     matrix = cdist(coords, coords, metric='euclidean')
#     # Set diagonal (jarak ke diri sendiri) menjadi infinity agar tidak dipilih
#     np.fill_diagonal(matrix, float('inf'))
#     return matrix
#
#
# if __name__ == "__main__":
#     # 1. Daftar jumlah kota yang ingin diuji
#     variasi_n = [5, 10, 15, 20]
#     seed_value = 42
#
#     # 2. Buat folder utama hasil eksperimen
#     parent_folder = "hasil_eksperimen"
#     if not os.path.exists(parent_folder):
#         os.makedirs(parent_folder)
#
#     print(f"Memulai eksperimen untuk n = {variasi_n}...")
#     print(f"Hasil akan disimpan di folder: {parent_folder}")
#
#     for n_kota in variasi_n:
#         # Buat sub-folder untuk masing-masing jumlah kota
#         folder_n = os.path.join(parent_folder, f"{n_kota}_kota")
#         if not os.path.exists(folder_n):
#             os.makedirs(folder_n)
#
#         # Nama file log untuk masing-masing n
#         file_log = os.path.join(folder_n, f"report_n{n_kota}.txt")
#
#         # Mengalihkan Output Print ke File
#         with open(file_log, 'w') as f:
#             # Simpan referensi terminal asli
#             original_stdout = sys.stdout
#             sys.stdout = f  # Mulai menulis ke file
#
#             # --- MULAI PROSES SEPERTI BIASA ---
#             print(f"=== EKSPERIMEN TSP: {n_kota} KOTA (SEED: {seed_value}) ===")
#
#             np.random.seed(seed_value)
#             coords = np.random.randint(1, 101, size=(n_kota, 2))
#             print("\n1. KOORDINAT KOTA (X, Y):")
#             for i, (x, y) in enumerate(coords):
#                 print(f"   Kota {i}: ({x}, {y})")
#
#             matrix = generate_matrix(n_kota, seed=seed_value)
#
#             print("\n2. MATRIKS JARAK ANTAR KOTA (Euclidean):")
#             header = "      " + "".join([f"K{i:<7}" for i in range(n_kota)])
#             print(header)
#             print("-" * len(header))
#             for i in range(n_kota):
#                 row_str = f"K{i:<4} | "
#                 for j in range(n_kota):
#                     val = matrix[i][j]
#                     row_str += f"{val:<7.2f} " if val != float('inf') else f"{'inf':<7} "
#                 print(row_str)
#
#             print("\n3. PROSES PENCARIAN RUTE TERPENDEK...")
#             start_time = time.perf_counter()
#             path, cost, nodes_count = solve_tsp(matrix)
#             end_time = time.perf_counter()
#             duration = end_time - start_time
#
#             print("\n4. HASIL AKHIR:")
#             print(f"   Rute Terpendek : {path}")
#             print(f"   Total Jarak    : {cost:.2f}")
#             print(f"   Simpul Dieksplorasi : {nodes_count}")
#             print(f"   Waktu Proses   : {duration:.6f} detik")
#
#             # Kembalikan output ke terminal setelah selesai satu iterasi
#             sys.stdout = original_stdout
#
#         print(f" Selesai: {n_kota} kota. Data tersimpan di {file_log}")
#
#     print("\nSeluruh eksperimen selesai.")


import numpy as np
import heapq
from utils import reduce_matrix, calculate_cost
from node import Node
import time
import os
import sys
from scipy.spatial.distance import cdist
import math
import matplotlib.pyplot as plt
import networkx as nx
from graphviz import Digraph


def solve_tsp(adj_matrix):
    nodes_explored = 0
    n = len(adj_matrix)
    adj_matrix = np.array(adj_matrix, dtype=float)
    original_matrix = adj_matrix.copy()

    # List untuk menyimpan riwayat pohon: (parent_id, child_id, label, cost, is_sol, is_pruned)
    tree_data = []
    node_counter = 1  # ID untuk root adalah 1

    root_matrix, initial_reduction = reduce_matrix(adj_matrix.copy())
    # Kita modifikasi sedikit agar Node menyimpan ID-nya sendiri
    root = Node(root_matrix, initial_reduction, [0], 0, 0)
    root.id = node_counter

    pq = []
    heapq.heappush(pq, root)
    # Rekam root (parent None)
    tree_data.append((None, root.id, "Start: A", root.cost, False, False))

    best_solution = float('inf')
    best_path = []
    final_node_id = None

    while pq:
        current_node = heapq.heappop(pq)
        nodes_explored += 1

        if current_node.cost >= best_solution:
            # Rekam simpul yang dipangkas (Pruning)
            # tree_data.append((current_node.parent_id, current_node.id, ... , is_pruned=True))
            continue

        if current_node.level == n - 1:
            last_city = current_node.current_city
            return_dist = original_matrix[last_city, 0]
            final_cost = current_node.cost + return_dist

            if final_cost < best_solution:
                best_solution = final_cost
                best_path = current_node.path + [0]
                final_node_id = current_node.id
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

                child_node = Node(child_matrix, child_cost, current_node.path + [next_city], current_node.level + 1,
                                  next_city)
                child_node.id = node_counter
                child_node.parent_id = current_node.id

                heapq.heappush(pq, child_node)

                # Rekam setiap cabang yang dibuat
                edge_label = f"X{child_node.level}={chr(65 + next_city)}"
                tree_data.append((current_node.id, child_node.id, edge_label, round(child_cost, 2), False, False))

    # Tandai rute solusi di tree_data untuk warna hijau/merah
    # (Opsional: Anda bisa melooping tree_data untuk mengubah is_sol menjadi True pada node yang ada di best_path)

    return best_path, best_solution, nodes_explored, tree_data

def generate_matrix(n, seed=42):
    np.random.seed(seed)
    coords = np.random.randint(1, 101, size=(n, 2))
    matrix = cdist(coords, coords, metric='euclidean')
    np.fill_diagonal(matrix, float('inf'))
    return matrix

def visualize_graph(n, coords, matrix, folder_path):
    plt.figure(figsize=(10, 8))
    G = nx.Graph()

    # 1. Tambahkan Node dengan label alfabet (A, B, C...)
    for i in range(n):
        label = chr(65 + i) # 65 adalah ASCII untuk 'A'
        G.add_node(label, pos=(coords[i][0], coords[i][1]))

    pos = nx.get_node_attributes(G, 'pos')

    # 2. Tambahkan Edge
    for i in range(n):
        for j in range(i + 1, n):
            u = chr(65 + i)
            v = chr(65 + j)
            G.add_edge(u, v)

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray', style='dashed')

    plt.grid(True, linestyle='--', alpha=0.6)
    plot_file = os.path.join(folder_path, f"graph_connectivity_n{n}.png")
    plt.savefig(plot_file)
    plt.close()


# def visualize_tree(node_data, folder_path, n):
#     """
#     Menghasilkan visualisasi State Space Tree mirip gambar referensi.
#     node_data: list berisi tuple (parent_id, child_id, label_edge, cost, is_solution, is_pruned)
#     """
#     dot = Digraph(comment='TSP State Space Tree')
#     dot.attr(rankdir='TB', size='10,10')
#
#     for p_id, c_id, edge_lab, cost, is_sol, is_pruned in node_data:
#         # Atur label node (ID dan Nilai Cost)
#         node_label = f"{c_id}\n({cost})"
#
#         # Logika Warna dan Bentuk
#         if is_sol:
#             dot.node(str(c_id), node_label, color='green', penwidth='2')
#         elif is_pruned:
#             dot.node(str(c_id), node_label, color='red', shape='doublecircle')
#         else:
#             dot.node(str(c_id), node_label)
#
#         # Gambar garis (Edge)
#         if p_id is not None:
#             color = 'red' if is_sol else 'black'
#             dot.edge(str(p_id), str(c_id), label=edge_lab, color=color)
#
#     # Simpan file
#     output_path = os.path.join(folder_path, f'tree_n{n}')
#     dot.render(output_path, format='png', cleanup=True)
#     print(f"   [Visualisasi] Tree disimpan di: {output_path}.png")


def visualize_tree(node_data, folder_path, n, best_cost_final):
    from graphviz import Digraph

    dot = Digraph(comment='TSP State Space Tree')
    dot.attr(rankdir='TB', size='70,70')

    # Konfigurasi Node Standar
    dot.attr('node', shape='ellipse', style='filled', fontname='Arial')

    # --- BAGIAN LEGENDA (Dibuat sebagai Subgraph) ---
    with dot.subgraph(name='cluster_legend') as l:
        l.attr(label='Keterangan / Legenda', fontsize='14', fontcolor='blue', style='dashed')
        l.node('l1', 'Simpul Standar\n(Sedang Dieksplorasi)', fillcolor='#e1f5fe', color='#01579b')
        l.node('l2', 'Simpul Solusi\n(Rute Terpendek)', fillcolor='#98fb98', color='#2e8b57', penwidth='2')
        l.node('l3', 'Simpul Pruning\n(LB > Solusi Terbaik)', fillcolor='#ffcccb', color='#ff0000')
        l.node('l4', 'ID: Nomor Urut Simpul\nLB: Lower Bound (Estimasi Biaya)', shape='plaintext', style='')
        # l1 -> l2 -> l3 -> l4 [style=invis] # Untuk mengurutkan jika diperlukan

    # --- RENDER DATA POHON ---
    for p_id, c_id, edge_lab, cost, is_sol, is_pruned in node_data:
        node_label = f"ID: {c_id}\nLB: {cost:.2f}"

        if is_sol:
            dot.node(str(c_id), node_label, fillcolor='#98fb98', color='#2e8b57', penwidth='2')
        elif cost > best_cost_final:
            dot.node(str(c_id), node_label, fillcolor='#ffcccb', color='#ff0000')
        else:
            dot.node(str(c_id), node_label, fillcolor='#e1f5fe', color='#01579b')

        if p_id is not None:
            # Jalur merah tebal untuk rute solusi akhir
            e_color = '#2e8b57' if is_sol else '#555555'
            e_width = '2.5' if is_sol else '1.0'
            dot.edge(str(p_id), str(c_id), label=edge_lab, color=e_color, penwidth=e_width)

    output_path = os.path.join(folder_path, f'tree_n{n}_final')
    dot.render(output_path, format='png', cleanup=True)
    print(f"   [Visualisasi] Pohon dengan legenda berhasil dibuat di: {output_path}.png")

if __name__ == "__main__":
    variasi_n = [5]
    seed_value = 42

    parent_folder = "hasil_eksperimen"
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    print(f"Memulai eksperimen untuk n = {variasi_n}...")

    for n_kota in variasi_n:
        folder_n = os.path.join(parent_folder, f"{n_kota}_kota")
        if not os.path.exists(folder_n):
            os.makedirs(folder_n)

        file_log = os.path.join(folder_n, f"report_n{n_kota}.txt")

        with open(file_log, 'w') as f:
            original_stdout = sys.stdout
            sys.stdout = f

            print(f"=== EKSPERIMEN TSP: {n_kota} KOTA (SEED: {seed_value}) ===")

            np.random.seed(seed_value)
            coords = np.random.randint(1, 501, size=(n_kota, 2))

            # --- Tampilan Koordinat (Alfabet) ---
            print("\n1. KOORDINAT KOTA (X, Y):")
            for i, (x, y) in enumerate(coords):
                print(f"   Kota {chr(65 + i)}: ({x}, {y})")

            matrix = generate_matrix(n_kota, seed=seed_value)
            visualize_graph(n_kota, coords, matrix, folder_n)

            # --- Tampilan Header Matriks (Alfabet) ---
            print("\n2. MATRIKS JARAK ANTAR KOTA (Euclidean):")
            header = "      " + "".join([f"{chr(65 + i):<7}" for i in range(n_kota)])
            print(header)
            print("-" * len(header))
            for i in range(n_kota):
                row_label = chr(65 + i)
                row_str = f"{row_label:<4} | "
                for j in range(n_kota):
                    val = matrix[i][j]
                    row_str += f"{val:<7.2f} " if val != float('inf') else f"{'inf':<7} "
                print(row_str)

            print("\n3. PROSES PENCARIAN RUTE TERPENDEK...")
            start_time = time.perf_counter()
            # Sekarang solve_tsp mengembalikan tree_data juga
            path, cost, nodes_count, tree_history = solve_tsp(matrix)
            end_time = time.perf_counter()
            duration = end_time - start_time

            # Panggil visualisasi pohon
            if n_kota <= 6:  # Batasi hanya untuk n kecil agar gambar tidak terlalu besar
                # visualize_tree(tree_history, folder_n, n_kota)
                visualize_tree(tree_history, folder_n, n_kota, cost)
            # --- Tampilan Rute (Alfabet) ---
            readable_path = [chr(65 + city) for city in path]

            print("\n4. HASIL AKHIR:")
            print(f"   Rute Terpendek : {' -> '.join(readable_path)}")
            print(f"   Total Jarak    : {cost:.2f}")
            print(f"   Simpul Dieksplorasi : {nodes_count}")
            print(f"   Waktu Proses   : {duration:.6f} detik")

            sys.stdout = original_stdout

        print(f" Selesai: {n_kota} kota. Data tersimpan di {file_log}")

    print("\nSeluruh eksperimen selesai.")