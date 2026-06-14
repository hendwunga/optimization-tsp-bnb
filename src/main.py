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
        Mode Eksperimen Transparansi Penuh + Auto-Logging Komprehensif Multi-Seed.
        Menulis CSV global dan membuat TXT detail per 'n' kota mencakup seluruh seed.
        """
        # 1. Setup Folder Output
        output_folder = os.path.join(base_dir, "..", "hasil_penelitian")
        log_folder = os.path.join(output_folder, "laporan_detail")

        for folder in [output_folder, log_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        csv_path = os.path.join(output_folder, "data_tsp_final.csv")

        # Inisialisasi Header CSV
        with open(csv_path, 'w') as f:
            f.write("n,waktu_eksekusi_avg,optimal_cost_avg,nodes_explored_avg\n")

        current_n = start_n

        print(f"🚀 MEMULAI PENGUJIAN (MODE AKURASI PENUH MULTI-SEED)")
        print(f"Seeds: {seeds}")
        print(f"Output CSV : {csv_path}")
        print(f"Output TXT : {log_folder}/research_report_n[X].txt\n")

        try:
            while True:
                # Struktur data untuk menyimpan log mentah per seed untuk file TXT
                seed_log_data = {}

                n_seed_times = []
                n_seed_costs = []
                n_seed_nodes = []

                # Jalur simpan file log teks n saat ini
                txt_path = os.path.join(log_folder, f"research_report_n{current_n}.txt")

                print(f"Menghitung n={current_n}...", end=" ", flush=True)

                for s_val in seeds:
                    # Generate data matriks dan koordinat untuk masing-masing seed
                    matrix, coords = self.solver.generate_matrix(current_n, s_val)

                    seed_times = []
                    last_cost = 0
                    nodes_count = 0

                    for i in range(self.iterations_per_seed):
                        start_time = time.perf_counter()
                        _, cost, n_count, _ = self.solver.solve_tsp(matrix)
                        end_time = time.perf_counter()

                        seed_times.append(end_time - start_time)
                        last_cost = cost
                        nodes_count = n_count

                    # Hitung rata-rata internal per seed untuk waktu komputasi
                    avg_time_this_seed = sum(seed_times) / self.iterations_per_seed

                    # Simpan metrik performa eksternal loop seed
                    n_seed_times.append(avg_time_this_seed)
                    n_seed_costs.append(last_cost)

                    # 1. Mengumpulkan data simpul dari masing-masing seed ke dalam list
                    n_seed_nodes.append(nodes_count)

                    # Simpan salinan data lengkap seed ini untuk keperluan pencetakan log berkas TXT
                    seed_log_data[s_val] = {
                        'coords': coords,
                        'matrix': matrix,
                        'time': avg_time_this_seed,
                        'cost': last_cost,
                        'nodes': nodes_count
                    }

                # 2. Setelah keluar dari loop seed, baru dihitung rata-rata globalnya
                avg_time_global = sum(n_seed_times) / len(seeds)
                avg_cost_global = sum(n_seed_costs) / len(seeds)
                avg_nodes_global = sum(n_seed_nodes) / len(seeds)

                # 3. PROSES PENULISAN ELEGAN LOG SELURUH SEED KE FILE TXT
                with open(txt_path, 'w') as f_txt:
                    original_stdout = sys.stdout
                    sys.stdout = f_txt

                    print(f"===================================================================")
                    print(f"===               TSP DATA REPORT: {current_n:<2} CITIES               ===")
                    print(f"===================================================================\n")
                    print(f"Jumlah Seed Pengujian : {len(seeds)} {seeds}")
                    print(f"Iterasi per Seed      : {self.iterations_per_seed} kali")

                    # Loop 1: Cetak Titik Koordinat Seluruh Seed
                    print("\n[A] DATA TITIK KOORDINAT KOTA (X, Y) PER SEED:")
                    for s_val in seeds:
                        print(f"\n---> KOORDINAT SEED {s_val}:")
                        for idx, (x, y) in enumerate(seed_log_data[s_val]['coords']):
                            print(f"    Kota {chr(65 + idx)}: ({x:.4f}, {y:.4f})")

                    # Loop 2: Cetak Matriks Ketetanggaan Seluruh Seed
                    print("\n[B] MATRIKS KETETANGGAAN (DISTANCE MATRIX) PER SEED:")
                    for s_val in seeds:
                        print(f"\n---> MATRIKS KETETANGGAAN SEED {s_val}:")
                        header = "       " + "".join([f"{chr(65 + i):<12}" for i in range(current_n)])
                        print(header)
                        print("-" * len(header))
                        current_matrix = seed_log_data[s_val]['matrix']
                        for i in range(current_n):
                            row_str = f"{chr(65 + i):<4} | "
                            for j in range(current_n):
                                val = current_matrix[i][j]
                                if val == float('inf') or val > 1e9:
                                    row_str += f"{'inf':<12}"
                                else:
                                    row_str += f"{val:<12.4f}"
                            print(row_str)

                    # Loop 3: Cetak Performa Individu Tiap Seed
                    print("\n[C] METRIK PERFORMA INDIVIDU TIAP SEED:")
                    print(f"-------------------------------------------------------------------")
                    print(f"{'Seed':<10} | {'Waktu Komputasi':<18} | {'Jarak Optimal':<15} | {'Simpul'}")
                    print(f"-------------------------------------------------------------------")
                    for s_val in seeds:
                        data = seed_log_data[s_val]
                        print(f"{s_val:<10} | {data['time']:<14.6f} detik | {data['cost']:<15.2f} | {data['nodes']}")
                    print(f"-------------------------------------------------------------------")

                    # Cetak Rangkuman Rata-Rata Final Global
                    print("\n[D] RATA-RATA METRIK PERFORMA AKHIR GLOBAL (BAB IV DATA):")
                    print(f"    - Waktu Komputasi Rata-rata (Avg) : {avg_time_global:.6f} detik")
                    print(f"    - Jarak Optimal Rata-rata (Avg)   : {avg_cost_global:.2f}")
                    print(f"    - Simpul Dieksplorasi Rata-rata   : {avg_nodes_global:.1f}")

                    sys.stdout = original_stdout

                # 4. SIMPAN KE CSV GLOBAL
                with open(csv_path, 'a') as f_csv:
                    f_csv.write(f"{current_n},{avg_time_global:.6f},{avg_cost_global:.2f},{avg_nodes_global:.1f}\n")

                print(f"Selesai! -> TXT & CSV Terupdate.")

                # Paksa pembersihan objek dari memori lokal loop demi kestabilan RAM
                del n_seed_times, n_seed_costs, n_seed_nodes, seed_log_data
                current_n += 1

        except KeyboardInterrupt:
            print("\n\n⚠️ Pengujian dihentikan oleh pengguna.")
        except MemoryError:
            print(f"\n\n❌ Memori RAM tidak cukup untuk n={current_n}. Batas struktur data pohon tercapai.")
        finally:
            print(f"\n✅ Pengujian Selesai. Seluruh arsip tersimpan aman di folder: {output_folder}")


if __name__ == "__main__":
    research = TSPResearch()
    research.run_stress_test(start_n=3, seeds=[42, 10, 99])