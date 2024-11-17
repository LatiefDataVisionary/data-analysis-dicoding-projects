import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Pengaturan gaya visualisasi
sns.set(style='darkgrid')

# Mengimpor dataset
orders = pd.read_csv(
    os.path.join('orders_dataset.csv'),
    parse_dates=[
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
)
order_items = pd.read_csv(os.path.join('order_items_dataset.csv'))
customers = pd.read_csv(os.path.join('customers_dataset.csv'))

# Filter berdasarkan rentang tanggal
min_date = orders["order_approved_at"].min()
max_date = orders["order_approved_at"].max()

with st.sidebar:
    st.write("### Filter by Date Range")
    start_date, end_date = st.date_input(
        "Select Date Range",
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
    .agg(order_count=("order_id", "count"), revenue=("order_id", "size"))
    .reset_index()
)

# Pengeluaran per pelanggan
customer_spend = (
    order_items.merge(orders, on="order_id")
    .groupby("customer_id")
    .agg(total_spend=("price", "sum"))
    .reset_index()
)

# Analisis produk
product_sales = order_items.groupby("product_id").agg(
    product_count=("order_item_id", "count"),
    total_revenue=("price", "sum")
).reset_index()

# Visualisasi Dashboard
st.title("E-Commerce Dashboard")

# Daily Orders
st.subheader("Daily Orders Overview")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Total Orders:** {daily_orders['order_count'].sum()}")
with col2:
    st.markdown(f"**Total Revenue:** {daily_orders['revenue'].sum()}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=daily_orders, x="order_approved_at", y="order_count", marker="o", ax=ax)
ax.set_title("Daily Orders")
st.pyplot(fig)

# Customer Spending
st.subheader("Customer Spending Analysis")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Total Spending:** {customer_spend['total_spend'].sum()}")
with col2:
    st.markdown(f"**Average Spending:** {customer_spend['total_spend'].mean():.2f}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(customer_spend["total_spend"], bins=20, kde=True, ax=ax)
ax.set_title("Distribution of Customer Spending")
st.pyplot(fig)

# Product Performance
st.subheader("Product Performance")
col1, col2 = st.columns(2)
with col1:
    most_sold = product_sales.nlargest(5, "product_count")
    st.markdown(f"**Most Sold Product ID:** {most_sold.iloc[0]['product_id']}")
with col2:
    least_sold = product_sales.nsmallest(5, "product_count")
    st.markdown(f"**Least Sold Product ID:** {least_sold.iloc[0]['product_id']}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=most_sold, x="product_count", y="product_id", ax=ax)
ax.set_title("Top 5 Most Sold Products")
st.pyplot(fig)

# Customer Geography
st.subheader("Customer Demographics")
state_counts = customers["customer_state"].value_counts()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=state_counts.index, y=state_counts.values, ax=ax)
ax.set_title("Customers by State")
st.pyplot(fig)

st.caption("Dashboard created for analysis of E-Commerce dataset.")
