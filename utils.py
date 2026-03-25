import numpy as np


def reduce_matrix(matrix):
    n = len(matrix)
    row_reduction = 0
    col_reduction = 0

    # Reduksi Baris
    for i in range(n):
        row = matrix[i, :]
        min_val = np.min(row[row != np.inf]) if np.any(row != np.inf) else 0
        if min_val != 0 and min_val != np.inf:
            row_reduction += min_val
            matrix[i, :] -= min_val

    # Reduksi Kolom
    for j in range(n):
        col = matrix[:, j]
        min_val = np.min(col[col != np.inf]) if np.any(col != np.inf) else 0
        if min_val != 0 and min_val != np.inf:
            col_reduction += min_val
            matrix[:, j] -= min_val

    return matrix, row_reduction + col_reduction


def calculate_cost(parent_matrix, i, j, parent_cost):
    n = len(parent_matrix)
    matrix = parent_matrix.copy()

    # Aturan modifikasi matriks anak:
    # 1. Biaya dari i ke j diambil
    edge_cost = matrix[i, j]

    # 2. Set baris i dan kolom j menjadi infinity
    matrix[i, :] = np.inf
    matrix[:, j] = np.inf

    # 3. Set A[j, 0] menjadi infinity (mencegah siklus prematur ke root)
    matrix[j, 0] = np.inf

    # 4. Reduksi matriks baru
    reduced_matrix, reduction_cost = reduce_matrix(matrix)

    # Rumus: Cost(S) = Cost(R) + A[i,j] + r
    total_cost = parent_cost + edge_cost + reduction_cost

    return total_cost, reduced_matrix