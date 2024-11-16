# Proyek Akhir Analisis Data Menggunakan Python

## Deskripsi Proyek
Proyek ini bertujuan untuk melakukan analisis data dan visualisasi menggunakan Python pada dataset yang relevan. Dalam proyek ini, kami memanfaatkan berbagai pustaka Python seperti Pandas, Matplotlib, Seaborn, Plotly, dan lain-lain untuk membersihkan, menganalisis, serta memvisualisasikan data. Tujuan akhir dari proyek ini adalah untuk mengidentifikasi pola, tren, dan wawasan yang dapat memberikan nilai tambah dalam pengambilan keputusan.

## Struktur Direktori
Berikut adalah struktur direktori proyek ini:

submission
├───dashboard
| ├───E-Commerce Public Dataset.csv
| └───dashboard.py
├───data
| ├───customers_dataset.csv
| ├───order_items_dataset.csv
| └───orders_dataset.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
└───url.txt


- **`dashboard/`**: Folder ini berisi file data dan script untuk dashboard interaktif.
- **`data/`**: Folder berisi dataset yang digunakan dalam analisis.
- **`notebook.ipynb`**: File Jupyter Notebook yang berisi kode dan analisis utama proyek.
- **`requirements.txt`**: Daftar pustaka Python yang diperlukan untuk menjalankan proyek.
- **`url.txt`**: File yang berisi URL atau link yang relevan dengan proyek.

## Pustaka yang Digunakan
Berikut adalah pustaka utama yang digunakan dalam proyek ini:

- `pandas`: Untuk manipulasi dan pembersihan data.
- `numpy`: Untuk operasi numerik.
- `matplotlib`, `seaborn`, `plotly`: Untuk visualisasi data (statistik deskriptif, analisis grafis).
- `scipy`: Untuk analisis statistik lanjutan.
- `geopandas`, `folium`: Untuk analisis geospasial (opsional, jika ada data lokasi).
- `streamlit`: Untuk membuat aplikasi dashboard interaktif.
- `zipfile36`: Untuk ekstraksi file ZIP (jika diperlukan).

## Instalasi
1. Pastikan Anda telah menginstal Python 3.x di sistem Anda.
2. Install pustaka yang diperlukan dengan menjalankan perintah berikut di terminal:

   ```bash
   pip install -r requirements.txt

3. Untuk menjalankan analisis dan visualisasi, buka file notebook.ipynb menggunakan Jupyter Notebook atau Google Colab.
4. Untuk menjalankan aplikasi dashboard, Anda bisa menjalankan file dashboard.py dengan perintah:

streamlit run dashboard/dashboard.py
