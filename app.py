# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db_utils import fetch_table
from optimizer import run_inventory_optimization

st.set_page_config(page_title="Inventory Optimization Dashboard", layout="wide")

st.title("📦 Inventory Optimization Web App")
st.markdown("""
This app calculates **Economic Order Quantity (EOQ)**, **Reorder Points**, and **Safety Stock**
for each product based on historical demand data stored in an SQLite database.
""")

# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Optimization Parameters")
ordering_cost = st.sidebar.number_input(
    "Ordering Cost per Order ($)", value=100.0, step=10.0
)
service_level = st.sidebar.slider("Service Level (Z-value)", 0.5, 3.0, 1.65, step=0.05)

st.sidebar.markdown("---")
if st.sidebar.button("Run Optimization"):
    with st.spinner("Running optimization..."):
        results_df = run_inventory_optimization()
        st.session_state["results"] = results_df
        st.success("Optimization completed!")

# --- Data Section ---
st.header("📊 Current Data")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Products")
    st.dataframe(fetch_table("products"))

with col2:
    st.subheader("Demand (Sample)")
    demand_df = fetch_table("demand")
    st.dataframe(demand_df.head(10))

# --- Optimization Results ---
if "results" in st.session_state:
    st.header("🧮 Optimization Results")

    results_df = st.session_state["results"]
    st.dataframe(results_df)

    # --- Charts ---
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            results_df,
            x="product_name",
            y="EOQ",
            title="EOQ by Product",
            color="product_name",
            text_auto=True,
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            results_df,
            x="product_name",
            y="Reorder_Point",
            title="Reorder Points by Product",
            color="product_name",
            text_auto=True,
        )
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Click **Run Optimization** in the sidebar to start the analysis.")
