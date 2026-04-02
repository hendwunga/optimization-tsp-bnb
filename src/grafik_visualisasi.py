import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. DATA ASLI (Sesuai Permintaan: Presisi Penuh Tanpa Pengurangan)
n_kota = [5, 10, 15, 20]
waktu = [0.002535, 0.938527, 9.405895, 136.766872]

# 2. SISTEM FOLDER (Otomatis Membuat Folder Jika Belum Ada)
output_folder = "hasil_grafik_skripsi"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Folder '{output_folder}' telah dibuat.")

# 3. SETTING VISUAL MODERN
sns.set_theme(style="whitegrid") # Background bersih dengan grid abu-abu tipis
plt.figure(figsize=(10, 6))

# 4. PLOTTING
# Menggunakan warna Midnight Blue (#2c3e50) untuk garis dan Alizarin Crimson (#e74c3c) untuk titik
plt.plot(n_kota, waktu, marker='o', markersize=10, linewidth=3,
         color='#2c3e50', markerfacecolor='#e74c3c', markeredgecolor='white',
         label='Waktu Eksekusi (Original Data)')

# Efek area di bawah grafik untuk kesan modern (Gradient-like effect)
plt.fill_between(n_kota, waktu, color='#3498db', alpha=0.15)

# 5. ANOTASI DATA ASLI
# Menampilkan angka presisi penuh di atas setiap titik
for i, val in enumerate(waktu):
    plt.text(n_kota[i], waktu[i] + 4, f'{val}',
             ha='center', va='bottom', fontsize=9, fontweight='bold', color='#34495e')

# 6. PENGATURAN SUMBU & LABEL
plt.title('Grafik Analisis Waktu Komputasi Branch and Bound TSP',
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Jumlah Kota (n)', fontsize=12, fontweight='bold')
plt.ylabel('Waktu Eksekusi (detik)', fontsize=12, fontweight='bold')

plt.xticks(n_kota) # Memastikan sumbu X hanya muncul angka 5, 10, 15, 20
plt.xlim(4, 21)
plt.ylim(-5, 160) # Memberi ruang agar teks di titik 136 tidak terpotong

# Menghilangkan garis tepi atas dan kanan agar lebih minimalis
sns.despine()

# 7. PENYIMPANAN KE FOLDER
file_name = 'grafik_tsp_original.png'
file_path = os.path.join(output_folder, file_name)
plt.savefig(file_path, dpi=300, bbox_inches='tight')

print("-" * 30)
print(f"STATUS: BERHASIL")
print(f"Lokasi Simpan: {os.path.abspath(file_path)}")
print("-" * 30)

# 8. TAMPILKAN
plt.show()