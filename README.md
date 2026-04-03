

# 🚀 Optimization of Traveling Salesman Problem (TSP) using Branch and Bound Algorithm

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NumPy-Scientific-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Sanata_Dharma-Informatics-blue?style=for-the-badge" alt="USD">
  <img src="https://img.shields.io/badge/Status-Research_Project-success?style=for-the-badge" alt="Status">
</p>

-----

## 📌 Abstract

Proyek ini menyajikan implementasi tingkat lanjut dari algoritma **Branch and Bound (BnB)** dengan teknik **Matrix Reduction** untuk menyelesaikan *Traveling Salesman Problem (TSP)* secara optimal.

Tujuan utama dari riset ini adalah mereduksi kompleksitas komputasi dari pendekatan *brute-force* melalui estimasi **Lower Bound** yang ketat dan **State Space Pruning**, dengan tetap menjamin tercapainya solusi global optimal.

-----

## 🏛️ Research Background

Traveling Salesman Problem (TSP) diklasifikasikan sebagai masalah **NP-Hard**, dengan kompleksitas komputasi faktorial:

$$O(n!)$$

Solusi *brute-force* menjadi tidak layak seiring bertambahnya jumlah kota. Oleh karena itu, penelitian ini menerapkan sinergi teknik utama:

  * **Euclidean Distance Metric**: Perhitungan jarak antar kota berbasis koordinat Cartesius $(x, y)$ untuk akurasi spasial.
  * **Cost Matrix Reduction**: Untuk menentukan *Lower Bound* pada setiap simpul melalui reduksi baris dan kolom.
  * **State Space Search**: Menggunakan struktur data pohon untuk eksplorasi rute secara hierarkis.
  * **Best-First Search**: Optimasi antrean prioritas (Priority Queue) untuk mempercepat penemuan solusi.

-----

## 🎯 Research Objectives

  * **Efficiency**: Merestriksi ruang pencarian menggunakan teknik *pruning* pada cabang non-potensial.
  * **Scalability Analysis**: Menganalisis pertumbuhan waktu eksekusi terhadap penambahan jumlah input ($n$).
  * **Computational Validation**: Mengevaluasi stabilitas algoritma pada lingkungan terkontrol.
  * **Process Visualization**: Merepresentasikan proses pengambilan keputusan algoritma secara grafis.

-----

## 🏗️ Project Architecture

Sistem dirancang dengan pola modular untuk memisahkan logika algoritma dari alat analisis:

```text
proyek_tsp/
├── src/                    # Core Logic
│   ├── main.py             # Research Entry Point
│   ├── solver.py           # BnB Algorithm Engine
│   ├── node.py             # State Space Data Structure
│   └── utils.py            # Euclidean & Matrix Operations
├── visualisasi/            # Analytics Module
│   ├── visualizer.py       # Graph & Tree Rendering
│   └── performance.py      # Statistical Charting
├── reports/                # Research Artifacts
│   └── [n]_kota/           # Automated Logs & PNG Results
├── requirements.txt        # Dependency Management
└── README.md               # Research Documentation
```

-----

## 🧪 Experimental Methodology

### 📐 Euclidean Distance Calculation

Matriks biaya dibangun berdasarkan jarak garis lurus antar dua titik di ruang 2D menggunakan rumus:
$$d(i, j) = \sqrt{(x_j - x_i)^2 + (y_j - y_i)^2}$$
Metode ini menjamin konsistensi jarak dalam simulasi koordinat kota yang bersifat simetris.

### ⏱️ Precision Time Measurement

Untuk menjamin validitas data dalam **Bab IV Skripsi**, pengukuran dilakukan dengan:

  * **Function**: `time.perf_counter()` (Resolusi tinggi).
  * **Protocol**: **5x Iteration Averaging**.
  * **Goal**: Mengeliminasi *system noise* dan fluktuasi beban CPU pada OS Linux.

### 🌳 State Space Analysis

Visualisasi pohon keputusan dihasilkan otomatis untuk $n \le 5$. Analisis fokus pada:

  * Mekanisme *Branching* (pembentukan anak simpul).
  * Keputusan *Pruning* (pemangkasan cabang berdasarkan *cost*).

-----

## ⚙️ Installation & Setup

### 1\. Prasyarat Sistem

Pastikan **Graphviz** terinstal di sistem Anda untuk rendering pohon:

```bash
sudo apt install graphviz  # Untuk Linux (Ubuntu/Debian)
```

### 2\. Setup Lingkungan

```bash
git clone https://github.com/username/proyek_tsp.git
cd proyek_tsp
pip install -r requirements.txt
```

### 3\. Eksekusi Riset

Jalankan skrip utama untuk memulai seluruh variasi eksperimen:

```bash
python3 src/main.py
```

-----

## 📊 Results & Visualization

Eksperimen dilakukan pada variasi jumlah kota: **$n = [5, 10, 15, 20]$**.

Proyek ini secara otomatis menghasilkan:

1.  **City Connectivity Graph**: Visualisasi spasial koordinat kota berdasarkan metrik Euclidean.
2.  **State Space Tree**: Logika pemangkasan pada setiap level *node*.
3.  **Execution Performance Chart**: Kurva pertumbuhan waktu komputasi (Average Time).

-----

## 📚 References

  * **Little, J. D. et al. (1963)** - *An Algorithm for the Traveling Salesman Problem*. Operations Research.
  * **Cormen, T. H.** - *Introduction to Algorithms*. MIT Press.
  * **Universitas Sanata Dharma** - *Modul Kuliah Strategi Algoritma*.

-----

## 👤 Author & Researcher

**Hendrikus Yohanes Wunga**
Informatics Student
**Universitas Sanata Dharma, Yogyakarta**
*Specialization: Backend Development & Computer Networking*

-----

## 📜 Academic License

Proyek ini dikembangkan secara eksklusif untuk **kepentingan akademik dan penelitian**. Penggunaan ulang kode harus mencantumkan atribusi kepada penulis asli.

-----

> “Good algorithms are not just fast — they are scalable.”