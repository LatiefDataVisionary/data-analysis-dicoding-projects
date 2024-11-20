import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Pengaturan gaya visualisasi
sns.set(style='darkgrid')

# Memuat dataset
orders = pd.read_csv(
    'orders_dataset.csv',
    parse_dates=[
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
)
order_items = pd.read_csv('order_items_dataset.csv')
customers = pd.read_csv('customers_dataset.csv')

# Filter berdasarkan rentang tanggal
min_date = orders["order_approved_at"].min()
max_date = orders["order_approved_at"].max()

with st.sidebar:
    st.write("### Filter Berdasarkan Rentang Tanggal")
    start_date, end_date = st.date_input(
        "Pilih Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data berdasarkan tanggal
filtered_orders = orders[
    (orders["order_approved_at"] >= pd.to_datetime(start_date)) &
    (orders["order_approved_at"] <= pd.to_datetime(end_date))
]

# Analisis harian
daily_orders = (
    filtered_orders.groupby(filtered_orders["order_approved_at"].dt.date)
    .agg(jumlah_pesanan=("order_id", "count"))
    .reset_index()
)

# Pengeluaran per pelanggan
customer_spend = (
    order_items.merge(orders, on="order_id")
    .groupby("customer_id")
    .agg(total_pengeluaran=("price", "sum"))
    .reset_index()
)

# Analisis produk
product_sales = order_items.groupby("product_id").agg(
    jumlah_produk_terjual=("order_item_id", "count")
).reset_index()

# Visualisasi Dashboard
st.title("Dashboard E-Commerce")

# Tinjauan Harian
st.subheader("Tinjauan Pesanan Harian")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Total Pesanan:** {daily_orders['jumlah_pesanan'].sum()}")
with col2:
    st.markdown(f"**Total Pendapatan:** {daily_orders['jumlah_pesanan'].sum()}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=daily_orders, x="order_approved_at", y="jumlah_pesanan", marker="o", ax=ax)
ax.set_title("Jumlah Pesanan Harian")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Grafik Baru: Jumlah Pembelian per Hari dalam Minggu
st.subheader("Jumlah Pembelian per Hari dalam Minggu")
filtered_orders["day_of_week"] = filtered_orders["order_approved_at"].dt.day_name()
orders_per_day = (
    filtered_orders.groupby("day_of_week")
    .agg(jumlah_pesanan=("order_id", "count"))
    .reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )  # Urutkan hari dalam minggu
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=orders_per_day.index, y=orders_per_day["jumlah_pesanan"], ax=ax)
ax.set_title("Jumlah Pembelian per Hari dalam Minggu")
ax.set_xlabel("Hari dalam Minggu")
ax.set_ylabel("Jumlah Pesanan")
st.pyplot(fig)

# Pengeluaran Pelanggan
st.subheader("Analisis Pengeluaran Pelanggan")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Total Pengeluaran:** {customer_spend['total_pengeluaran'].sum()}")
with col2:
    st.markdown(f"**Rata-rata Pengeluaran:** {customer_spend['total_pengeluaran'].mean():.2f}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(customer_spend["total_pengeluaran"], bins=20, kde=True, ax=ax)
ax.set_title("Distribusi Pengeluaran Pelanggan")
ax.set_xlabel("Total Pengeluaran")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Grafik Baru: Distribusi Kecepatan Pengiriman (Hari)
st.subheader("Distribusi Kecepatan Pengiriman dalam Hari")
orders["delivery_speed"] = (
    orders["order_delivered_customer_date"] - orders["order_approved_at"]
).dt.days

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(orders["delivery_speed"].dropna(), bins=20, kde=True, ax=ax)
ax.set_title("Distribusi Kecepatan Pengiriman")
ax.set_xlabel("Kecepatan Pengiriman (Hari)")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Performa Produk
st.subheader("Performa Produk")
col1, col2 = st.columns(2)
with col1:
    produk_terlaris = product_sales.nlargest(5, "jumlah_produk_terjual")
    st.markdown(f"**ID Produk Terlaris:** {produk_terlaris.iloc[0]['product_id']}")
with col2:
    produk_terendah = product_sales.nsmallest(5, "jumlah_produk_terjual")
    st.markdown(f"**ID Produk Terendah Penjualan:** {produk_terendah.iloc[0]['product_id']}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=produk_terlaris, x="jumlah_produk_terjual", y="product_id", ax=ax)
ax.set_title("5 Produk Terlaris")
ax.set_xlabel("Jumlah Terjual")
ax.set_ylabel("ID Produk")
st.pyplot(fig)

# Demografi Pelanggan Berdasarkan Lokasi
st.subheader("Demografi Pelanggan Berdasarkan Lokasi")
jumlah_per_state = customers["customer_state"].value_counts()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=jumlah_per_state.index, y=jumlah_per_state.values, ax=ax)
ax.set_title("Jumlah Pelanggan Berdasarkan Provinsi")
ax.set_xlabel("Provinsi")
ax.set_ylabel("Jumlah Pelanggan")
st.pyplot(fig)
