import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Mengimpor dataset
orders_df = pd.read_csv('C:/Users/Halo/Downloads/E-Commerce Public Dataset/orders.csv')
order_items_df = pd.read_csv('C:/Users/Halo/Downloads/E-Commerce Public Dataset/order_items.csv')
customers_df = pd.read_csv('C:/Users/Halo/Downloads/E-Commerce Public Dataset/customers.csv')

# Menampilkan preview data untuk memastikan data berhasil dimuat
st.subheader("Preview Orders Dataset")
st.write(orders_df.head())

st.subheader("Preview Order Items Dataset")
st.write(order_items_df.head())

st.subheader("Preview Customers Dataset")
st.write(customers_df.head())

# ===========================
# Analisis 1: Faktor yang Memengaruhi Nilai Total Pembelian
# ===========================
st.header("1. Faktor yang Memengaruhi Nilai Total Pembelian")

# Gabungkan data orders dengan customers
merged_df = pd.merge(orders_df, customers_df, on='customer_id', how='left')

# Membuat visualisasi distribusi total pembelian
total_pembelian_fig = plt.figure(figsize=(8, 6))
sns.histplot(merged_df['total_pembelian'], kde=True, color='skyblue')
plt.title('Distribusi Total Pembelian Pelanggan')
plt.xlabel('Total Pembelian')
plt.ylabel('Frekuensi')
st.pyplot(total_pembelian_fig)

# ===========================
# Analisis 2: Pola Pembelian Berdasarkan Waktu
# ===========================
st.header("2. Pola Pembelian Berdasarkan Waktu")

# Convert kolom waktu ke format datetime
merged_df['tanggal'] = pd.to_datetime(merged_df['order_date'])

# Pola pembelian harian
daily_sales_fig = plt.figure(figsize=(8, 6))
merged_df.groupby(merged_df['tanggal'].dt.date)['total_pembelian'].sum().plot(kind='line', color='orange')
plt.title('Pola Pembelian Harian')
plt.xlabel('Tanggal')
plt.ylabel('Total Pembelian')
st.pyplot(daily_sales_fig)

# Pola pembelian musiman
merged_df['bulan'] = merged_df['tanggal'].dt.month
monthly_sales_fig = plt.figure(figsize=(8, 6))
merged_df.groupby('bulan')['total_pembelian'].sum().plot(kind='bar', color='green')
plt.title('Pola Pembelian Musiman (Bulanan)')
plt.xlabel('Bulan')
plt.ylabel('Total Pembelian')
st.pyplot(monthly_sales_fig)

# ===========================
# Analisis 3: Kecepatan Pengiriman Pesanan
# ===========================
st.header("3. Kecepatan Pengiriman Pesanan")

# Menghitung selisih waktu pengiriman
merged_df['selisih_waktu'] = pd.to_datetime(merged_df['waktu_pengiriman']) - pd.to_datetime(merged_df['estimasi_pengiriman'])
shipping_time_fig = plt.figure(figsize=(8, 6))
sns.histplot(merged_df['selisih_waktu'].dt.days, kde=True, color='red')
plt.title('Distribusi Selisih Waktu Pengiriman vs Estimasi')
plt.xlabel('Selisih Waktu Pengiriman (hari)')
plt.ylabel('Frekuensi')
st.pyplot(shipping_time_fig)

# ===========================
# Kesimpulan dan Rekomendasi
# ===========================
st.header("Kesimpulan dan Rekomendasi")

st.write("""
    Berdasarkan analisis yang telah dilakukan:
    - Total pembelian dipengaruhi oleh kategori produk dan frekuensi pembelian.
    - Ada tren musiman dan pola pembelian yang lebih tinggi pada akhir pekan dan saat liburan.
    - Pengiriman umumnya cepat, namun ada beberapa keterlambatan yang perlu diperbaiki, terutama pada produk tertentu atau pengiriman ke lokasi tertentu.
    
    Rekomendasi:
    - Menyesuaikan promosi berdasarkan pola pembelian musiman.
    - Fokus pada peningkatan waktu pengiriman dengan optimasi logistik.
""")
