import numpy as np


# Fungsi untuk mengurangi nilai matriks agar mendapatkan Batas Bawah (Lower Bound)
def reduce_matrix(matrix):
    n = len(matrix)
    row_reduction = 0  # Menyimpan total nilai pengurang dari semua baris
    col_reduction = 0  # Menyimpan total nilai pengurang dari semua kolom

    # --- Tahap 1: Reduksi Baris ---
    for i in range(n):
        row = matrix[i, :]  # Mengambil satu baris i

        # Mencari nilai minimum di baris tersebut yang bukan 'inf' (tak terhingga)
        # Jika semua sel adalah 'inf', min_val diset 0
        min_val = np.min(row[row != np.inf]) if np.any(row != np.inf) else 0

        # Jika ditemukan nilai minimum yang valid (bukan 0 dan bukan inf)
        if min_val != 0 and min_val != np.inf:
            row_reduction += min_val  # Tambahkan ke total reduksi
            matrix[i, :] -= min_val  # Kurangi semua elemen di baris tersebut dengan min_val

    # --- Tahap 2: Reduksi Kolom ---
    for j in range(n):
        col = matrix[:, j]  # Mengambil satu kolom j

        # Mencari nilai minimum di kolom tersebut (yang sudah dikurangi reduksi baris tadi)
        min_val = np.min(col[col != np.inf]) if np.any(col != np.inf) else 0

        # Jika ditemukan nilai minimum yang valid
        if min_val != 0 and min_val != np.inf:
            col_reduction += min_val  # Tambahkan ke total reduksi
            matrix[:, j] -= min_val  # Kurangi semua elemen di kolom tersebut dengan min_val

    # Mengembalikan matriks yang sudah tereduksi dan total biaya reduksinya (r)
    return matrix, row_reduction + col_reduction


# Fungsi untuk menghitung biaya estimasi (LB) saat berpindah dari kota i ke kota j
def calculate_cost(parent_matrix, i, j, parent_cost):
    n = len(parent_matrix)
    matrix = parent_matrix.copy()  # Membuat salinan matriks induk agar tidak merusak data asli

    # 1. Mengambil biaya asli dari kota i ke kota j sebelum matriks dimodifikasi
    edge_cost = matrix[i, j]

    # 2. Aturan Branch and Bound:
    # Karena kita sudah berangkat dari i, baris i tidak boleh digunakan lagi (set ke inf)
    # Karena kita sudah menuju ke j, kolom j tidak boleh dimasuki oleh kota lain (set ke inf)
    matrix[i, :] = np.inf
    matrix[:, j] = np.inf

    # 3. Mencegah agen kembali ke kota asal (Kota 0) sebelum waktunya
    # Ini memastikan tidak terbentuk siklus kecil (misal: 0 -> 1 -> 0)
    matrix[j, 0] = np.inf

    # 4. Melakukan reduksi pada matriks baru simpul anak untuk mendapatkan biaya reduksi tambahan (r')
    reduced_matrix, reduction_cost = reduce_matrix(matrix)

    # Rumus Utama: Biaya Anak = Biaya Induk + Jarak i-j + Biaya Reduksi Tambahan
    # Ini adalah implementasi rumus: Cost(S) = Cost(R) + A[i,j] + r
    total_cost = parent_cost + edge_cost + reduction_cost

    # Mengembalikan nilai biaya total yang baru dan matriks tereduksinya
    return total_cost, reduced_matrix