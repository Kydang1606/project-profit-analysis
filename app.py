# app.py
import streamlit as st
from utils import calculate_costs
from constants import HOURLY_RATES

st.set_page_config(page_title="Cost Estimation App", layout="wide")
st.title("📊 Cost Estimation & Comparison Tool")

st.subheader("1. Input Time and Material Cost")

col1, col2 = st.columns(2)

with col1:
    worker_hours = st.number_input("👷‍♂️ Worker Hours", min_value=0.0, format="%.2f")
    office_hours = st.number_input("🧑‍💼 Office Hours", min_value=0.0, format="%.2f")
    cnc_hours = st.number_input("🛠 CNC Hours", min_value=0.0, format="%.2f")
    robot_hours = st.number_input("🤖 Robot Hours", min_value=0.0, format="%.2f")
    autoclave_hours = st.number_input("🔥 Autoclave Hours", min_value=0.0, format="%.2f")

with col2:
    material_cost = st.number_input("🧱 Material Cost (USD)", min_value=0.0, format="%.2f")
    actual_cost = st.number_input("💰 Actual Incurred Cost (USD)", min_value=0.0, format="%.2f")
    profit_margin = st.slider("📈 Profit Margin (%)", min_value=0, max_value=100, value=20)

# Show fixed rates
with st.expander("🔧 Hourly Rates (Fixed)"):
    st.write(HOURLY_RATES)

# Calculate
if st.button("🧮 Calculate & Compare"):
    input_data = {
        "Worker Hours": worker_hours,
        "Office Hours": office_hours,
        "CNC Hours": cnc_hours,
        "Robot Hours": robot_hours,
        "Autoclave Hours": autoclave_hours,
        "Material Cost": material_cost,
    }

    result = calculate_costs(input_data, profit_margin)

    st.subheader("2. 📋 Cost Breakdown")
    st.write({
        "Worker Cost (USD)": result["Cost (Worker)"],
        "Office Cost (USD)": result["Cost (Office)"],
        "Machine Cost (USD)": result["Cost (Machines)"],
        "Material Cost (USD)": result["Cost (Material)"],
        "Total Estimated Cost": result["Total Cost"],
        "Estimated Base Price": result["Base Price"],
        "Selling Price (USD)": result["Selling Price"],
    })

    st.subheader("3. 📈 Comparison Table")

    comparison_data = {
        "Metric": [
            "Estimated Base Price",
            "Selling Price (with Profit)",
            "Actual Incurred Cost"
        ],
        "Value (USD)": [
            result["Base Price"],
            result["Selling Price"],
            actual_cost
        ]
    }

    st.table(comparison_data)
