import os
import sys
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from visualisasi.visualizer import TSPVisualizer
from solver import TSPSolver
from visualisasi.performance_analyzer import PerformanceAnalyzer


class TSPExperiment:
    def __init__(self):
        self.solver = TSPSolver()
        self.visualizer = TSPVisualizer()

    def run(self, variasi_n, seed_value=42):
        # --- LOGIKA JALUR FOLDER ---
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_folder = os.path.join(base_dir, "..", "reports")

        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)
            print(f"Folder '{parent_folder}' telah berhasil dibuat.")

        # List untuk menampung data kumulatif hasil eksperimen
        all_n = []
        all_times = []

        print(f"Memulai eksperimen untuk n = {variasi_n}...")

        for n_kota in variasi_n:
            folder_n = os.path.join(parent_folder, f"{n_kota}_kota")
            if not os.path.exists(folder_n):
                os.makedirs(folder_n)

            file_log = os.path.join(folder_n, f"report_n{n_kota}.txt")

            # --- 1. GENERATE DATA ---
            matrix, coords = self.solver.generate_matrix(n_kota, seed_value)

            with open(file_log, 'w') as f:
                original_stdout = sys.stdout
                sys.stdout = f

                print(f"=== EKSPERIMEN TSP: {n_kota} KOTA (SEED: {seed_value}) ===")

                # --- KOORDINAT ---
                print("\n1. KOORDINAT KOTA (X, Y):")
                for i, (x, y) in enumerate(coords):
                    print(f"   Kota {chr(65 + i)}: ({x:.2f}, {y:.2f})")

                # --- MATRIKS JARAK ---
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

                # --- 2. SOLVER & VISUALISASI PER KOTA ---
                print("\n3. PROSES PENCARIAN RUTE TERPENDEK...")
                self.visualizer.visualize_graph(n_kota, coords, matrix, folder_n)

                start_time = time.perf_counter()
                path, cost, nodes_count, tree_history = self.solver.solve_tsp(matrix)
                duration = time.perf_counter() - start_time

                # Simpan data untuk grafik performa gabungan
                all_n.append(n_kota)
                all_times.append(duration)

                # Cari ID Best Path Nodes untuk jalur hijau di pohon
                best_path_nodes = [1]
                for step in range(1, len(path)):
                    target_label = f"={chr(65 + path[step])}"
                    for p_id, c_id, edge_lab, _, _, _ in tree_history:
                        if target_label in edge_lab:
                            best_path_nodes.append(c_id)

                if n_kota <= 5:
                    self.visualizer.visualize_tree(tree_history, folder_n, n_kota, cost, best_path_nodes)

                # --- 3. HASIL AKHIR PER KOTA ---
                readable_path = [chr(65 + city) for city in path]
                print(f"\n4. HASIL AKHIR:")
                print(f"   Rute Terpendek      : {' -> '.join(readable_path)}")
                print(f"   Total Jarak (Cost)  : {cost:.2f}")
                print(f"   Simpul Dieksplorasi : {nodes_count}")
                print(f"   Waktu Eksekusi      : {duration:.6f} detik")

                sys.stdout = original_stdout

            print(f" [+] Selesai: {n_kota} kota. Waktu: {duration:.4f} detik.")

        # --- 4. TAHAP AKHIR: ANALISIS PERFORMA KESELURUHAN ---
        print("\nSedang membuat grafik perbandingan performa...")
        analyzer = PerformanceAnalyzer(parent_folder)
        analyzer.generate_performance_chart(all_n, all_times)
        print("Seluruh eksperimen selesai dengan sukses.")


if __name__ == "__main__":
    app = TSPExperiment()
    # Menjalankan dari 5 sampai 20 kota sesuai permintaan
    app.run(variasi_n=[5, 10, 15, 20])