import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


class PerformanceAnalyzer:
    def __init__(self, output_folder):
        self.output_folder = output_folder
        # Memastikan folder reports ada
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def generate_performance_chart(self, n_kota, waktu_eksekusi):
        """
        Membuat grafik garis (line chart) untuk membandingkan
        waktu eksekusi dari berbagai jumlah kota (n).
        """
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        # Plot Garis Utama
        plt.plot(n_kota, waktu_eksekusi, marker='o', markersize=10, linewidth=3,
                 color='#2c3e50', markerfacecolor='#e74c3c', markeredgecolor='white',
                 label='Waktu Eksekusi (Original Data)')

        # Efek Area Biru Transparan
        plt.fill_between(n_kota, waktu_eksekusi, color='#3498db', alpha=0.15)

        # Menambahkan Teks Nilai Detik di Atas Titik
        for i, val in enumerate(waktu_eksekusi):
            plt.text(n_kota[i], waktu_eksekusi[i] + 5, f'{val}',
                     ha='center', va='bottom', fontsize=9,
                     fontweight='bold', color='#34495e')

        # Labeling Profesional
        plt.xlabel('Jumlah Kota (n)', fontsize=12, fontweight='bold')
        plt.ylabel('Waktu Eksekusi (detik)', fontsize=12, fontweight='bold')

        # Pengaturan Sumbu agar rapi
        plt.xticks(n_kota)
        plt.xlim(min(n_kota) - 1, max(n_kota) + 1)

        # Memberi ruang di atas agar teks tidak terpotong
        plt.ylim(-5, max(waktu_eksekusi) + 30)

        sns.despine()

        # Simpan Hasil
        file_path = os.path.join(self.output_folder, 'grafik_perbandingan_performa.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()

        print("-" * 30)
        print(f"ANALISIS SELESAI")
        print(f"Grafik perbandingan disimpan di: {os.path.abspath(file_path)}")
        print("-" * 30)