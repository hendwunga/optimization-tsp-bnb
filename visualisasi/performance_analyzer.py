# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# import pandas as pd  # Tambahkan import pandas
#
#
# class PerformanceAnalyzer:
#     def __init__(self, output_folder):
#         self.output_folder = output_folder
#         if not os.path.exists(self.output_folder):
#             os.makedirs(self.output_folder)
#
#     def export_to_csv(self, n_kota, waktu_eksekusi, total_costs):
#         """Menyimpan data eksperimen ke file CSV"""
#         df = pd.DataFrame({
#             'Number of Cities (n)': n_kota,
#             'Execution Time (seconds)': waktu_eksekusi,
#             'Optimal Cost (distance)': total_costs
#         })
#
#         file_path = os.path.join(self.output_folder, 'tsp_research_data.csv')
#         df.to_csv(file_path, index=False)
#         print(f"Excel-ready data saved at: {os.path.abspath(file_path)}")
#
#     def generate_performance_chart(self, n_kota, waktu_eksekusi):
#         sns.set_theme(style="whitegrid")
#         plt.figure(figsize=(10, 6))
#
#         # Plot Garis Utama
#         plt.plot(n_kota, waktu_eksekusi, marker='o', markersize=8, linewidth=2.5,
#                  color='#2c3e50', markerfacecolor='#e74c3c', markeredgecolor='white',
#                  label='Execution Time')
#
#         # Area transparan di bawah garis
#         plt.fill_between(n_kota, waktu_eksekusi, color='#3498db', alpha=0.1)
#
#
#         plt.xlabel('Number of Cities (n)', fontsize=11, fontweight='bold')
#         plt.ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
#
#         plt.xticks(n_kota)
#         plt.xlim(min(n_kota) - 0.5, max(n_kota) + 0.5)
#         sns.despine()
#
#         plt.savefig(os.path.join(self.output_folder, 'performance_chart.png'), dpi=300, bbox_inches='tight')
#         plt.close()
#
#     def generate_cost_chart(self, n_kota, total_costs):
#         sns.set_theme(style="whitegrid")
#         plt.figure(figsize=(10, 6))
#
#         # Plot Garis Utama
#         plt.plot(n_kota, total_costs, marker='s', markersize=8, linewidth=2.5,
#                  color='#27ae60', markerfacecolor='#f1c40f', markeredgecolor='white',
#                  label='Optimal Cost')
#
#         plt.fill_between(n_kota, total_costs, color='#2ecc71', alpha=0.1)
#
#
#         plt.xlabel('Number of Cities (n)', fontsize=11, fontweight='bold')
#         plt.ylabel('Optimal Cost ', fontsize=11, fontweight='bold')
#
#         plt.xticks(n_kota)
#         plt.xlim(min(n_kota) - 0.5, max(n_kota) + 0.5)
#         sns.despine()
#
#         plt.savefig(os.path.join(self.output_folder, 'cost_chart.png'), dpi=300, bbox_inches='tight')
#         plt.close()


import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Load Data
file_path = "../hasil_penelitian/data_tsp_final.csv"

if not os.path.exists(file_path):
    print(f"❌ File {file_path} tidak ditemukan!")
else:
    df = pd.read_csv(file_path)
    df = df[df['n'] >= 3]

    # Konfigurasi Estetika Profesional
    plt.rcParams.update({
        "font.family": "serif",  # Kesan formal jurnal ilmiah
        "font.size": 11,
        "axes.edgecolor": "#333333",  # Warna border abu-abu gelap
        "grid.color": "#e6e6e6",  # Grid halus
    })

    # Palet Warna Peneliti
    color_perf = "#2c3e50"  # Midnight Blue (Serius & Berwibawa)
    color_cost = "#c0392b"  # Deep Red (Tegas untuk metrik biaya)

    # --- GRAFIK 1: PERFORMANCE CHART (TIME) ---
    plt.figure(figsize=(9, 5))
    plt.plot(df['n'], df['waktu_eksekusi_avg'],
             marker='o', markersize=6, color=color_perf,
             linewidth=1.5, markerfacecolor='white', markeredgewidth=1.5)

    plt.xlabel('Number of Cities (n)', fontweight='bold')
    plt.ylabel('Execution Time (seconds)', fontweight='bold')
    plt.xticks(df['n'])

    # Menghilangkan border atas dan kanan agar terlihat modern
    ax1 = plt.gca()
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('performance_chart.png', dpi=600, bbox_inches='tight')  # DPI tinggi untuk cetak
    print("✅ Performance Chart (Professional) disimpan.")

    # --- GRAFIK 2: COST CHART ---
    plt.figure(figsize=(9, 5))
    plt.plot(df['n'], df['optimal_cost_avg'],
             marker='s', markersize=6, color=color_cost,
             linewidth=1.5, markerfacecolor='white', markeredgewidth=1.5)

    plt.xlabel('Number of Cities (n)', fontweight='bold')
    plt.ylabel('Optimal Cost ', fontweight='bold')
    plt.xticks(df['n'])

    ax2 = plt.gca()
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('cost_chart.png', dpi=600, bbox_inches='tight')
    print("✅ Cost Chart (Professional) disimpan.")