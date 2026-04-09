import os
import sys
import time
import numpy as np

# Pengaturan Path agar folder visualisasi terbaca
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from visualisasi.visualizer import TSPVisualizer
from solver import TSPSolver
from visualisasi.performance_analyzer import PerformanceAnalyzer


class TSPResearch:
    def __init__(self):
        self.solver = TSPSolver()
        self.visualizer = TSPVisualizer()
        # Jumlah pengulangan untuk setiap n untuk mendapatkan rata-rata waktu yang stabil
        self.iterations_per_n = 5

    def run_experiment(self, variasi_n, seed_value=42):
        parent_folder = os.path.join(base_dir, "..", "reports")
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)

        all_n = []
        all_times_avg = []

        print(f"🔬 MEMULAI EKSPERIMEN PENELITIAN (Seed: {seed_value})")
        print(f"Setiap pengujian 'n' akan diulang {self.iterations_per_n}x untuk akurasi data.")

        for n_kota in variasi_n:
            folder_n = os.path.join(parent_folder, f"{n_kota}_kota")
            if not os.path.exists(folder_n):
                os.makedirs(folder_n)

            file_log = os.path.join(folder_n, f"research_report_n{n_kota}.txt")

            # --- TAHAP 1: Persiapan Data ---
            matrix, coords = self.solver.generate_matrix(n_kota, seed_value)
            iter_times = []

            # --- TAHAP 2: Pengukuran Waktu Berulang (Metode Rata-rata) ---
            # Kita hanya menyimpan detail (pohon/graf) pada iterasi pertama saja
            # Namun waktu dihitung dari beberapa kali jalan untuk stabilitas data
            for i in range(self.iterations_per_n):
                start_time = time.perf_counter()
                path, cost, nodes_count, tree_history = self.solver.solve_tsp(matrix)
                end_time = time.perf_counter()
                iter_times.append(end_time - start_time)

            avg_duration = sum(iter_times) / self.iterations_per_n
            all_n.append(n_kota)
            all_times_avg.append(avg_duration)

            # --- TAHAP 3: Logging Hasil ---
            with open(file_log, 'w') as f:
                original_stdout = sys.stdout
                sys.stdout = f

                print(f"=== LAPORAN PENELITIAN TSP: {n_kota} KOTA ===")
                print(f"Metode: Branch and Bound (Matrix Reduction)")
                print(f"Seed  : {seed_value}")

                # --- 1. DATA INPUT: KOORDINAT ---
                print("\n1. KOORDINAT KOTA (X, Y):")
                for i, (x, y) in enumerate(coords):
                    print(f"   Kota {chr(65 + i)}: ({x:.2f}, {y:.2f})")

                # --- 2. DATA INPUT: MATRIKS JARAK ---
                print("\n2. MATRIKS JARAK ANTAR KOTA (Euclidean):")
                header = "      " + "".join([f"{chr(65 + i):<10}" for i in range(n_kota)])
                print(header)
                print("-" * len(header))
                for i in range(n_kota):
                    row_label = chr(65 + i)
                    row_str = f"{row_label:<4} | "
                    for j in range(n_kota):
                        val = matrix[i][j]
                        if val == float('inf'):
                            row_str += f"{'inf':<10}"
                        else:
                            row_str += f"{val:<10.2f}"
                    print(row_str)

                # --- 3. STATISTIK PERFORMA ---
                print(f"\n3. STATISTIK WAKTU KOMPUTASI ({self.iterations_per_n} iterasi):")
                print(f"   - Waktu Tercepat (Min) : {min(iter_times):.6f} s")
                print(f"   - Waktu Terlama (Max)  : {max(iter_times):.6f} s")
                print(f"   - Rata-rata (Average)  : {avg_duration:.6f} s")

                # --- 4. HASIL OPTIMASI AKHIR ---
                print(f"\n4. HASIL OPTIMASI RUTE:")
                print(f"   - Total Jarak (Cost)   : {cost:.2f}")
                print(f"   - Rute Terpendek       : {' -> '.join([chr(65 + c) for c in path])}")
                print(f"   - Simpul Dieksplorasi  : {nodes_count}")

                # Visualisasi (Tetap hanya sekali)
                self.visualizer.visualize_graph(n_kota, coords, matrix, folder_n)
                if n_kota <= 5:
                    best_path_nodes = [1]
                    for step in range(1, len(path)):
                        target_label = f"={chr(65 + path[step])}"
                        for p_id, c_id, edge_lab, _, _, _ in tree_history:
                            if target_label in edge_lab:
                                best_path_nodes.append(c_id)
                    self.visualizer.visualize_tree(tree_history, folder_n, n_kota, cost, best_path_nodes)

                sys.stdout = original_stdout

            print(f" ✅ [n={n_kota}] Rerata Waktu: {avg_duration:.6f} s")

        # --- TAHAP 4: Analisis Akhir ---
        analyzer = PerformanceAnalyzer(parent_folder)
        analyzer.generate_performance_chart(all_n, all_times_avg)
        print("\n📊 Seluruh data penelitian telah dikompilasi ke folder /reports.")


# if __name__ == "__main__":
#     research = TSPResearch()
#     research.run_experiment(variasi_n=[ 5, 10, 15, 20, 22, 25, 28, 30])

if __name__ == "__main__":
    research = TSPResearch()

    # Membuat list variasi n dari 3 sampai 20
    # range(3, 21) akan menghasilkan [3, 4, 5, ..., 20]
    variasi_n_penelitian = list(range(3, 30))

    # Menjalankan eksperimen
    research.run_experiment(variasi_n=variasi_n_penelitian)