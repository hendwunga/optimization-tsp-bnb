import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# --- 1. DATA ASLI ---
n_kota = np.array([5, 10, 15, 20])
waktu = np.array([0.002815, 0.567258, 6.195577, 138.707353])

# --- 2. SISTEM FOLDER ---
output_folder = "hasil_grafik_final"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# --- 3. SETTING VISUAL PREMIUM ---
sns.set_theme(style="white")
plt.figure(figsize=(11, 7))

# Palet Warna (Deep Navy & Coral)
color_main = '#0f172a'  # Navy gelap
color_accent = '#f43f5e'  # Coral/Rose untuk titik
color_fill = '#3b82f6'  # Biru untuk area

# --- 4. PLOTTING ---
# Efek Gradient Area
x_smooth = np.linspace(n_kota.min(), n_kota.max(), 100)
y_smooth = np.interp(x_smooth, n_kota, waktu)
plt.fill_between(x_smooth, y_smooth, color=color_fill, alpha=0.1)

# Garis Utama
plt.plot(n_kota, waktu, color=color_main, linewidth=2.5, zorder=2)
# Titik Data
plt.scatter(n_kota, waktu, color=color_accent, s=120, edgecolors='white', linewidths=2, zorder=3)

# --- 5. ANOTASI DENGAN SATUAN (DETIK) ---
for i, val in enumerate(waktu):
    # Menggunakan "detik" untuk Indonesia, atau "s" untuk Internasional
    # Di sini saya gunakan "detik" agar dosen langsung paham
    label_text = f"{val} detik"

    plt.annotate(label_text, (n_kota[i], waktu[i]),
                 xytext=(0, 15), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9,
                 fontweight='bold', color='#1e293b',
                 bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#e2e8f0', alpha=0.9))

# --- 6. PENGATURAN SUMBU (INTERVAL 20 DETIK) ---
ax = plt.gca()

# Mengatur interval Y per 20 detik (0, 20, 40, ... 160)
# Ini membuat grafik terlihat sangat terukur dan rapi
plt.yticks(np.arange(0, 180, 20))
plt.xticks(n_kota)

plt.xlabel('Jumlah Kota (n)', fontsize=12, fontweight='bold', labelpad=10)
plt.ylabel('Waktu Eksekusi (detik)', fontsize=12, fontweight='bold', labelpad=10)

# Grid Horizontal Halus
ax.yaxis.grid(True, linestyle='--', color='#f1f5f9', zorder=1)
ax.xaxis.grid(False)

# Memperluas Limit agar teks tidak terpotong
plt.xlim(n_kota.min() - 2, n_kota.max() + 2)
plt.ylim(-5, 170)

# Hapus frame yang tidak perlu
sns.despine(left=True)

# --- 7. PENYIMPANAN ---
file_path = os.path.join(output_folder, 'grafik_tsp_indonesia_style.png')
plt.savefig(file_path, dpi=300, bbox_inches='tight')

print(f"Grafik profesional berhasil disimpan di: {file_path}")
plt.show()

# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
#
# # DATA
# n_kota = [5, 10, 15, 20]
# waktu = [0.002815, 0.567258, 6.195577, 138.707353]
#
# # FOLDER OUTPUT
# output_folder = "hasil_grafik"
# os.makedirs(output_folder, exist_ok=True)
#
# # STYLE MODERN (lebih clean & elegan)
# sns.set_theme(style="ticks", context="talk")
#
# plt.figure(figsize=(12, 7))
#
# # WARNA GRADIENT MODERN
# line_color = "#1f77b4"
# point_color = "#ff6b6b"
#
# # PLOT UTAMA
# plt.plot(
#     n_kota, waktu,
#     marker='o',
#     markersize=10,
#     linewidth=3,
#     color=line_color,
#     markerfacecolor=point_color,
#     markeredgewidth=2,
#     markeredgecolor='white'
# )
#
# # AREA FILL HALUS
# plt.fill_between(n_kota, waktu, color=line_color, alpha=0.1)
#
# # ANOTASI (lebih rapi & tidak terlalu dekat)
# for x, y in zip(n_kota, waktu):
#     plt.annotate(
#         f"{y:.6f}",
#         (x, y),
#         textcoords="offset points",
#         xytext=(0, 10),
#         ha='center',
#         fontsize=10,
#         fontweight='semibold'
#     )
#
# # GRID HALUS
# plt.grid(True, linestyle='--', alpha=0.3)
#
# # LABEL PROFESIONAL
# # plt.title(
# #     "Analisis Waktu Eksekusi Algoritma Branch and Bound (TSP)",
# #     fontsize=16,
# #     fontweight='bold',
# #     pad=20
# # )
#
# plt.xlabel("Jumlah Kota (n)", fontsize=13)
# plt.ylabel("Waktu Eksekusi (detik)", fontsize=13)
#
# # SCALE LOG (INI KUNCI BIAR KELIHATAN PRO 🔥)
# plt.yscale('log')
#
# # AXIS CONTROL
# plt.xticks(n_kota)
# plt.xlim(4, 21)
#
# # REMOVE BORDER ATAS & KANAN
# sns.despine()
#
# # SIMPAN
# file_path = os.path.join(output_folder, "grafik_tsp_profesional.png")
# plt.savefig(file_path, dpi=300, bbox_inches='tight')
#
# print("Grafik berhasil dibuat di:", os.path.abspath(file_path))
#
# plt.show()


# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# import numpy as np
# import seaborn as sns
# import os
#
# # --- 1. DATA ASLI (Presisi Penuh) ---
# n_kota = np.array([5, 10, 15, 20])
# waktu = np.array([0.002815, 0.567258, 6.195577, 138.707353])
#
# # --- 2. SISTEM FOLDER ---
# output_folder = "hasil_grafik_premium"
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)
#
# # --- 3. SETTING VISUAL MODERN ---
# sns.set_theme(style="white")
# plt.figure(figsize=(12, 7))  # Sedikit diperlebar untuk mengakomodasi teks panjang
#
# # Warna Premium
# color_main = '#1e3a8a'
# color_point = '#e74c3c'
# color_fill_start = '#60a5fa'
# color_text = '#334155'
#
# # --- 4. PLOTTING: GARIS & GRADIENT ---
# x_smooth = np.linspace(n_kota.min(), n_kota.max(), 100)
# y_smooth = np.interp(x_smooth, n_kota, waktu)
#
# for i in range(1, 11):
#     alpha_val = (11 - i) / 100 * 0.3
#     plt.fill_between(x_smooth, y_smooth, alpha=alpha_val, color=color_fill_start)
#
# plt.plot(n_kota, waktu, linewidth=3, color=color_main, zorder=3)
# plt.scatter(n_kota, waktu, s=130, color=color_point, edgecolors='white', linewidths=2, zorder=5)
#
# # --- 5. ANOTASI DATA (PRESISI PENUH TANPA PEMBULATAN) ---
# for i, val in enumerate(waktu):
#     # Menggunakan f-string tanpa format .2f agar semua angka muncul
#     label_text = f'{val}'
#
#     # Atur posisi vertikal agar tidak menabrak titik
#     # Khusus untuk n=20, kita taruh sedikit lebih tinggi agar tidak terpotong garis frame
#     offset = 12 if i < 3 else 15
#
#     plt.annotate(label_text, (n_kota[i], waktu[i]),
#                  xytext=(0, offset), textcoords='offset points',
#                  ha='center', va='bottom', fontsize=9,
#                  fontweight='bold', color=color_text,
#                  bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.7))
#
# # --- 6. PENGATURAN SUMBU & LABEL ---
# plt.xlabel('Jumlah Kota (n)', fontsize=12, fontweight='bold', color=color_text, labelpad=12)
# plt.ylabel('Waktu Eksekusi (detik)', fontsize=12, fontweight='bold', color=color_text, labelpad=12)
#
# plt.xticks(n_kota, fontsize=10, fontweight='bold')
# plt.yticks(fontsize=10)
#
# # Grid Horizontal Saja
# ax = plt.gca()
# ax.yaxis.grid(True, linestyle='--', color='#e2e8f0', alpha=0.7)
# ax.xaxis.grid(False)
#
# # Memperluas limit agar teks panjang di n=20 tidak terpotong (sangat penting!)
# plt.xlim(n_kota.min() - 2, n_kota.max() + 2)
# plt.ylim(waktu.min() - 10, waktu.max() + 35)
#
# sns.despine(left=True)  # Hapus garis kiri agar lebih "open" dan modern
#
# # --- 7. PENYIMPANAN ---
# file_name = 'grafik_tsp_presisi_penuh.png'
# file_path = os.path.join(output_folder, file_name)
# plt.savefig(file_path, dpi=300, bbox_inches='tight')
#
# print(f"Grafik presisi penuh berhasil disimpan di: {file_path}")
# plt.show()


# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# import os
#
# # --- 1. DATA ---
# n_kota = np.array([5, 10, 15, 20])
# waktu = np.array([0.002815, 0.567258, 6.195577, 138.707353])
#
# # --- 2. SETTING VISUAL (Eropean Research Style) ---
# plt.style.use('seaborn-v0_8-paper') # Menggunakan style paper ilmiah
# plt.figure(figsize=(10, 6))
#
# # Warna: Deep Blue dan Graphite (Warna khas jurnal teknik)
# main_color = '#0f172a'
# accent_color = '#ef4444'
#
# # --- 3. PLOTTING ---
# # Garis lebih tipis tapi tegas, titik tanpa border yang mencolok
# plt.plot(n_kota, waktu, color=main_color, linewidth=2, label='Computational Time', zorder=2)
# plt.scatter(n_kota, waktu, color=accent_color, s=80, edgecolors=main_color, zorder=3)
#
# # Fill area yang sangat halus (subtle)
# plt.fill_between(n_kota, waktu, color=main_color, alpha=0.05)
#
# # --- 4. ANOTASI PRESISI ---
# for i, val in enumerate(waktu):
#     plt.annotate(f'{val} s', (n_kota[i], waktu[i]),
#                  xytext=(0, 12), textcoords='offset points',
#                  ha='center', fontsize=9, fontweight='600',
#                  color=main_color)
#
# # --- 5. PENGATURAN SUMBU PROFESIONAL (Kuncinya di sini) ---
# ax = plt.gca()
#
# # Mengatur interval Sumbu Y per 20 detik (0, 20, 40, ... 160)
# # Ini memberikan detail yang cukup tanpa membuat grafik penuh sesak
# plt.yticks(np.arange(0, 180, 20))
# plt.xticks(n_kota)
#
# plt.xlabel('Number of Cities (n)', fontsize=11, fontweight='bold')
# plt.ylabel('Execution Time (seconds)', fontsize=11, fontweight='bold')
#
# # Grid hanya horizontal, sangat tipis (light gray)
# ax.yaxis.grid(True, linestyle='--', which='major', color='#e2e8f0', alpha=0.6)
# ax.xaxis.grid(False)
#
# # Hapus frame atas dan kanan (Modern Clean Look)
# sns.despine()
#
# # --- 6. PENYIMPANAN ---
# plt.savefig("grafik_tsp_international_style.png", dpi=300, bbox_inches='tight')
# plt.show()