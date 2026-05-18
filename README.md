# 🚀 Optimization of Traveling Salesman Problem (TSP) using Branch and Bound Algorithm

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NumPy-Scientific-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Sanata_Dharma-Informatics-blue?style=for-the-badge" alt="USD">
  <img src="https://img.shields.io/badge/Status-Research_Project-success?style=for-the-badge" alt="Status">
</p>

## 📌 Abstract

Proyek ini menyajikan implementasi algoritma **Branch and Bound (BnB)** dengan teknik **Matrix Reduction** untuk menyelesaikan *Traveling Salesman Problem (TSP)* secara optimal. Fokus utama riset ini adalah mengukur batas performa komputasi (*Stress Testing*) melalui eksplorasi jumlah kota secara dinamis hingga batas kapasitas memori sistem tercapai.

---

## 🏛️ Research Background

TSP diklasifikasikan sebagai masalah **NP-Hard**, dengan kompleksitas faktorial $O(n!)$. Penelitian ini menerapkan sinergi teknik utama:

* **Cost Matrix Reduction**: Menentukan *Lower Bound* pada setiap simpul melalui reduksi baris dan kolom.
* **State Space Search**: Eksplorasi rute hierarkis menggunakan struktur data pohon.
* **Best-First Search**: Menggunakan *Priority Queue* (Min-Heap) untuk memprioritaskan simpul dengan estimasi biaya terendah.

---

## 🏗️ Project Architecture

Sistem dirancang modular untuk memisahkan logika algoritma, visualisasi, dan manajemen data:

```text
proyek_tsp/
├── src/                    # Core Logic
│   ├── main.py             # Entry Point (Stress Test Mode)
│   ├── solver.py           # BnB Algorithm Engine
│   ├── node.py             # State Space Data Structure
│   └── utils.py            # Matrix Reduction & Cost Operations
├── visualisasi/            # Analytics Module
│   ├── visualizer.py       # Graph & Tree Rendering (Graphviz)
│   └── performance_analyzer.py # CSV Export & Charting (Seaborn)
├── reports/                # Research Artifacts (Auto-Generated)
│   ├── [n]_kota/           # Detailed Logs (.txt) & Plots (.png)
│   ├── tsp_research_data.csv # Compiled Raw Data
│   └── performance_chart.png # Execution Time Trend
└── requirements.txt        # Dependency Management
```

---

## 🧪 Experimental Methodology

### 📈 Dynamic Stress Testing
Berbeda dengan pengujian statis, sistem ini menggunakan mode **Auto-Increment**:
1.  Program memulai pengujian dari $n=3$.
2.  Setiap $n$ diselesaikan dengan protokol **5x Iteration Averaging** untuk validitas waktu.
3.  Hasil setiap $n$ langsung dicatat ke dalam laporan `.txt` dan `.csv` secara *real-time*.
4.  Eksperimen berlanjut secara otomatis hingga sistem mencapai limitasi perangkat keras (RAM/CPU).

### 📐 Euclidean Metric
Matriks biaya dibangun berdasarkan jarak garis lurus 2D:
$$d(i, j) = \sqrt{(x_j - x_i)^2 + (y_j - y_i)^2}$$

---

## ⚙️ Installation & Setup

### 1. Prasyarat Sistem (Graphviz)
Untuk merender *State Space Tree*, pastikan Graphviz terinstal:
```bash
sudo apt install graphviz  # Linux
brew install graphviz      # macOS
```

### 2. Eksekusi
```bash
# Clone & Install
git clone https://github.com/hendwunga/optimization-tsp-bnb.git
cd optimization-tsp-bnb
pip install -r requirements.txt

# Start Stress Test
python3 src/main.py
```

---

## 📊 Results & Visualization

Program menghasilkan tiga output utama untuk analisis Bab IV Skripsi:
1.  **Laporan Detail (.txt)**: Berisi koordinat kota, matriks jarak awal, dan statistik eksplorasi simpul.
2.  **Performance Chart**: Grafik garis minimalis yang menunjukkan tren kenaikan waktu eksekusi terhadap jumlah kota.
3.  **Optimal Cost Trend**: Grafik yang menunjukkan stabilitas pencarian solusi optimal.



---

## 👤 Author
**Hendrikus Yohanes Wunga**
Informatics Student - Universitas Sanata Dharma, Yogyakarta
*Aspiring Backend Developer | Java Specialist*

---
> “Good algorithms are not just fast — they are scalable.”
