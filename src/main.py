# import os
# import sys
# import time
# import numpy as np
#
# # Pengaturan Path
# base_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
#
# from visualisasi.visualizer import TSPVisualizer
# from solver import TSPSolver
# from visualisasi.performance_analyzer import PerformanceAnalyzer
#
#
# class TSPResearch:
#     def __init__(self):
#         self.solver = TSPSolver()
#         self.visualizer = TSPVisualizer()
#         self.iterations_per_n = 5  # Rata-rata dari 5x running
#
#     def run_stress_test(self, start_n=3, seeds=[42, 10, 25, 60, 99]):
#         # 1. Setup Folder & Analyzer
#         parent_folder = os.path.join(base_dir, "..", "reports")
#         if not os.path.exists(parent_folder):
#             os.makedirs(parent_folder)
#
#         analyzer = PerformanceAnalyzer(parent_folder)
#
#         # 2. Inisialisasi Data
#         all_n = []
#         all_times_avg = []
#         all_costs_avg = []
#         current_n = start_n
#
#         print(f"🚀 STARTING AUTO-STRESS TEST (Seed: {seeds})")
#         print(f"Logging details for each 'n' to individual .txt files.")
#         print("Press Ctrl+C to stop and generate final charts.\n")
#
#         try:
#             while True:  # Berjalan terus tanpa batas n
#                 folder_n = os.path.join(parent_folder, f"{current_n}_kota")
#                 if not os.path.exists(folder_n):
#                     os.makedirs(folder_n)
#
#                 file_log = os.path.join(folder_n, f"research_report_n{current_n}.txt")
#
#                 # Persiapan Data Matriks
#                 matrix, coords = self.solver.generate_matrix(current_n, seed_value)
#                 iter_times = []
#                 last_cost = 0
#                 last_path = []
#                 nodes_count = 0
#
#                 print(f"Testing n={current_n}...", end=" ", flush=True)
#
#                 # Pengukuran Waktu Berulang
#                 for i in range(self.iterations_per_n):
#                     start_time = time.perf_counter()
#                     path, cost, n_count, tree_history = self.solver.solve_tsp(matrix)
#                     end_time = time.perf_counter()
#
#                     iter_times.append(end_time - start_time)
#                     last_cost = cost
#                     last_path = path
#                     nodes_count = n_count
#
#                 # Hitung Rata-rata
#                 avg_duration = sum(iter_times) / self.iterations_per_n
#
#                 # --- LOGGING KE FILE TEXT (DETAIL) ---
#                 with open(file_log, 'w') as f:
#                     original_stdout = sys.stdout
#                     sys.stdout = f
#
#                     print(f"=== TSP RESEARCH REPORT: {current_n} CITIES ===")
#                     print(f"Method : Branch and Bound (Matrix Reduction)")
#                     print(f"Seed   : {seed_value}")
#
#                     # 1. DATA INPUT: KOORDINAT
#                     print("\n1. CITY COORDINATES (X, Y):")
#                     for i, (x, y) in enumerate(coords):
#                         print(f"   City {chr(65 + i)}: ({x:.2f}, {y:.2f})")
#
#                     # 2. DATA INPUT: MATRIKS JARAK
#                     print("\n2. DISTANCE MATRIX (Euclidean):")
#                     header = "      " + "".join([f"{chr(65 + i):<10}" for i in range(current_n)])
#                     print(header)
#                     print("-" * len(header))
#                     for i in range(current_n):
#                         row_label = chr(65 + i)
#                         row_str = f"{row_label:<4} | "
#                         for j in range(current_n):
#                             val = matrix[i][j]
#                             if val == float('inf'):
#                                 row_str += f"{'inf':<10}"
#                             else:
#                                 row_str += f"{val:<10.2f}"
#                         print(row_str)
#
#                     # 3. STATISTIK PERFORMA
#                     print(f"\n3. COMPUTATION STATISTICS ({self.iterations_per_n} iterations):")
#                     print(f"   - Fastest Time (Min) : {min(iter_times):.6f} s")
#                     print(f"   - Slowest Time (Max) : {max(iter_times):.6f} s")
#                     print(f"   - Average Time       : {avg_duration:.6f} s")
#
#                     # 4. HASIL OPTIMASI AKHIR
#                     print(f"\n4. OPTIMIZATION RESULTS:")
#                     print(f"   - Total Cost (Distance) : {last_cost:.2f}")
#                     print(f"   - Shortest Route        : {' -> '.join([chr(65 + c) for c in last_path])}")
#                     print(f"   - Nodes Explored        : {nodes_count}")
#
#                     sys.stdout = original_stdout
#
#                 # Update List Utama untuk CSV & Grafik
#                 all_n.append(current_n)
#                 all_times_avg.append(avg_duration)
#                 all_costs.append(last_cost)
#
#                 # --- AUTO-SAVE DATA KE CSV ---
#                 analyzer.export_to_csv(all_n, all_times_avg, all_costs)
#
#                 print(f"Done! ({avg_duration:.4f}s) | Saved to CSV & TXT.")
#
#                 # Visualisasi Graph
#                 self.visualizer.visualize_graph(current_n, coords, matrix, folder_n)
#
#                 current_n += 1
#
#         except KeyboardInterrupt:
#             print("\n\n⚠️  Experiment stopped by user (Ctrl+C).")
#         except MemoryError:
#             print("\n\n❌ [STOP] Out of RAM! Memory capacity reached.")
#         except Exception as e:
#             print(f"\n\n❌ [ERROR] An unexpected error occurred: {e}")
#
#         finally:
#             if all_n:
#                 print("\n📊 Generating final performance and cost charts...")
#                 analyzer.generate_performance_chart(all_n, all_times_avg)
#                 analyzer.generate_cost_chart(all_n, all_costs)
#                 print(f"✅ Final reports compiled for n = {min(all_n)} up to {max(all_n)}.")
#             else:
#                 print("❌ No data collected.")
#
#
# if __name__ == "__main__":
#     research = TSPResearch()
#     # Mulai dari n=3 agar data dasar lengkap
#     research.run_stress_test(start_n=3, seed_value=42)


# import os
# import sys
# import time
# import numpy as np
#
# # Pengaturan Path
# base_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))
#
# from visualisasi.visualizer import TSPVisualizer
# from solver import TSPSolver
# from visualisasi.performance_analyzer import PerformanceAnalyzer
#
#
# class TSPResearch:
#     def __init__(self):
#         self.solver = TSPSolver()
#         self.visualizer = TSPVisualizer()
#         self.iterations_per_seed = 5  # Mengurangi noise OS per seed
#
#     def run_stress_test(self, start_n=3, seeds=[42, 10, 25, 60, 99]):
#         """
#         Melakukan stress test dengan merata-ratakan hasil dari beberapa seed.
#         """
#         # 1. Setup Folder & Analyzer
#         parent_folder = os.path.join(base_dir, "..", "reports")
#         if not os.path.exists(parent_folder):
#             os.makedirs(parent_folder)
#
#         analyzer = PerformanceAnalyzer(parent_folder)
#
#         # 2. Inisialisasi Data Global
#         all_n = []
#         all_times_avg = []
#         all_costs_avg = []
#         current_n = start_n
#
#         print(f"🚀 STARTING MULTI-SEED STRESS TEST")
#         print(f"Seeds used       : {seeds}")
#         print(f"Iter per seed    : {self.iterations_per_seed}")
#         print("Press Ctrl+C to stop and generate final charts.\n")
#
#         try:
#             while True:  # Berjalan terus hingga dihentikan user atau RAM habis
#                 folder_n = os.path.join(parent_folder, f"{current_n}_kota")
#                 if not os.path.exists(folder_n):
#                     os.makedirs(folder_n)
#
#                 file_log = os.path.join(folder_n, f"research_report_n{current_n}.txt")
#
#                 # List untuk menampung hasil dari berbagai seed pada n yang sama
#                 n_seed_times = []
#                 n_seed_costs = []
#                 n_seed_nodes = []
#
#                 print(f"Testing n={current_n}...", end=" ", flush=True)
#
#                 # --- LOOP UNTUK SETIAP SEED ---
#                 for s_val in seeds:
#                     # Generate matriks berdasarkan seed saat ini
#                     matrix, coords = self.solver.generate_matrix(current_n, s_val)
#
#                     iter_times = []
#                     last_cost = 0
#                     nodes_count = 0
#
#                     # Pengukuran waktu berulang (untuk stabilitas noise OS)
#                     for i in range(self.iterations_per_seed):
#                         start_time = time.perf_counter()
#                         path, cost, n_count, _ = self.solver.solve_tsp(matrix)
#                         end_time = time.perf_counter()
#
#                         iter_times.append(end_time - start_time)
#                         last_cost = cost
#                         nodes_count = n_count
#
#                     # Simpan rata-rata performa untuk SEED ini
#                     n_seed_times.append(sum(iter_times) / self.iterations_per_seed)
#                     n_seed_costs.append(last_cost)
#                     n_seed_nodes.append(nodes_count)
#
#                 # --- HITUNG RATA-RATA DARI SEMUA SEED ---
#                 final_avg_time = sum(n_seed_times) / len(seeds)
#                 final_avg_cost = sum(n_seed_costs) / len(seeds)
#                 final_avg_nodes = sum(n_seed_nodes) / len(seeds)
#
#                 # --- LOGGING KE FILE TEXT (DETAIL RATA-RATA) ---
#                 with open(file_log, 'w') as f:
#                     original_stdout = sys.stdout
#                     sys.stdout = f
#
#                     print(f"=== TSP MULTI-SEED RESEARCH REPORT: {current_n} CITIES ===")
#                     print(f"Method          : Branch and Bound (Matrix Reduction)")
#                     print(f"Seeds Tested    : {seeds}")
#                     print(f"Iter per Seed   : {self.iterations_per_seed}")
#
#                     print(f"\n1. SUMMARY STATISTICS (Average across {len(seeds)} seeds):")
#                     print(f"   - Average Time      : {final_avg_time:.6f} s")
#                     print(f"   - Average Cost      : {final_avg_cost:.2f}")
#                     print(f"   - Average Nodes     : {final_avg_nodes:.1f}")
#
#                     print(f"\n2. BREAKDOWN PER SEED:")
#                     print(f"{'Seed':<10} | {'Time (s)':<12} | {'Cost':<10} | {'Nodes':<10}")
#                     print("-" * 50)
#                     for idx, s_val in enumerate(seeds):
#                         print(
#                             f"{s_val:<10} | {n_seed_times[idx]:<12.6f} | {n_seed_costs[idx]:<10.2f} | {n_seed_nodes[idx]:<10}")
#
#                     sys.stdout = original_stdout
#
#                 # Update List Utama untuk Grafik
#                 all_n.append(current_n)
#                 all_times_avg.append(final_avg_time)
#                 all_costs_avg.append(final_avg_cost)
#
#                 # --- AUTO-SAVE DATA KE CSV ---
#                 analyzer.export_to_csv(all_n, all_times_avg, all_costs_avg)
#
#                 print(f"Done! ({final_avg_time:.4f}s avg) | Saved to CSV & TXT.")
#
#                 # Visualisasi (Hanya untuk seed pertama agar folder tidak penuh gambar)
#                 # Anda bisa mengganti ini jika ingin memvisualisasikan semua seed
#                 first_matrix, first_coords = self.solver.generate_matrix(current_n, seeds[0])
#                 self.visualizer.visualize_graph(current_n, first_coords, first_matrix, folder_n)
#
#                 current_n += 1
#
#         except KeyboardInterrupt:
#             print("\n\n⚠️  Experiment stopped by user (Ctrl+C).")
#         except MemoryError:
#             print("\n\n❌ [STOP] Out of RAM! Memory capacity reached.")
#         except Exception as e:
#             print(f"\n\n❌ [ERROR] An unexpected error occurred: {e}")
#
#         finally:
#             if all_n:
#                 print("\n📊 Generating final multi-seed performance and cost charts...")
#                 analyzer.generate_performance_chart(all_n, all_times_avg)
#                 analyzer.generate_cost_chart(all_n, all_costs_avg)
#                 print(f"✅ Final reports compiled for n = {min(all_n)} up to {max(all_n)}.")
#             else:
#                 print("❌ No data collected.")
#
#
# if __name__ == "__main__":
#     research = TSPResearch()
#     # Menjalankan pengujian dengan 5 seed berbeda untuk hasil yang objektif
#     # Anda bisa menambah atau mengubah angka di list seeds ini
#     research.run_stress_test(start_n=3, seeds=[42, 10, 25, 60, 99])


import os
import sys
import time

# Pengaturan Path agar bisa memanggil solver
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(base_dir, '..')))

from solver import TSPSolver


class TSPResearch:
    def __init__(self):
        self.solver = TSPSolver()
        # Menggunakan 3 iterasi per seed untuk stabilitas
        self.iterations_per_seed = 3

    def run_stress_test(self, start_n=3, seeds=[42, 10, 99]):
        """
        Mode Ultra-Hemat Memori:
        Langsung menulis hasil ke CSV setiap kali satu 'n' selesai.
        """
        # 1. Setup Folder & File
        output_folder = os.path.join(base_dir, "..", "hasil_penelitian")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        csv_path = os.path.join(output_folder, "data_tsp_final.csv")

        # 2. Inisialisasi Header CSV (Overwrites existing file)
        with open(csv_path, 'w') as f:
            f.write("n,waktu_eksekusi_avg,optimal_cost_avg,nodes_explored_avg\n")

        current_n = start_n

        print(f"🚀 MEMULAI PENGUJIAN (MODE HEMAT MEMORI)")
        print(f"Seeds: {seeds} | Output: {csv_path}")
        print("Tekan Ctrl+C untuk berhenti kapan saja.\n")

        try:
            while True:
                n_seed_times = []
                n_seed_costs = []
                n_seed_nodes = []

                print(f"Menghitung n={current_n}...", end=" ", flush=True)

                for s_val in seeds:
                    # Generate matriks kota
                    matrix, _ = self.solver.generate_matrix(current_n, s_val)

                    seed_times = []
                    last_cost = 0
                    nodes_count = 0

                    for i in range(self.iterations_per_seed):
                        start_time = time.perf_counter()
                        # Jalankan solver (pure logic)
                        _, cost, n_count, _ = self.solver.solve_tsp(matrix)
                        end_time = time.perf_counter()

                        seed_times.append(end_time - start_time)
                        last_cost = cost
                        nodes_count = n_count

                    # Rata-rata untuk seed ini
                    n_seed_times.append(sum(seed_times) / self.iterations_per_seed)
                    n_seed_costs.append(last_cost)
                    n_seed_nodes.append(nodes_count)

                # Rata-rata final untuk n ini (dari semua seed)
                avg_time = sum(n_seed_times) / len(seeds)
                avg_cost = sum(n_seed_costs) / len(seeds)
                avg_nodes = sum(n_seed_nodes) / len(seeds)

                # 3. LANGSUNG SIMPAN KE CSV (Append Mode)
                # Data aman di disk meskipun program crash setelah ini
                with open(csv_path, 'a') as f:
                    f.write(f"{current_n},{avg_time:.6f},{avg_cost:.2f},{avg_nodes:.1f}\n")

                print(f"Selesai! ({avg_time:.4f}s)")

                # Memaksa garbage collection sederhana jika perlu
                del n_seed_times, n_seed_costs, n_seed_nodes

                current_n += 1

        except KeyboardInterrupt:
            print("\n\n⚠️ Pengujian dihentikan oleh pengguna.")
        except MemoryError:
            print(f"\n\n❌ Memori RAM tidak cukup untuk n={current_n}. Eksak TSP mencapai batas.")
        finally:
            print(f"\n✅ File CSV final tersimpan di: {csv_path}")


if __name__ == "__main__":
    research = TSPResearch()
    # Menggunakan 3 seed untuk efisiensi tinggi
    research.run_stress_test(start_n=3, seeds=[42, 10, 99])
