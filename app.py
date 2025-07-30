import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Project Profit Analysis (USD)", layout="wide")
st.title("💰 Project Profit Analysis (USD only)")

# === UNIT RATES (USD/hour or USD/unit) ===
st.markdown("### 💲 Input Hourly Rates (USD)")
col1, col2, col3 = st.columns(3)
rate_worker = col1.number_input("👷 Worker hourly rate (USD)", value=2.0, step=0.1, format="%.2f")
rate_office = col2.number_input("🧑‍💻 Office hourly rate (USD)", value=3.0, step=0.1, format="%.2f")
rate_machine = col3.number_input("🤖 Machine hourly rate (USD)", value=6.0, step=0.5, format="%.2f")

# === INPUT: PLANNED ===
st.markdown("### 📋 Planned Input")
input1 = st.data_editor(
    pd.DataFrame({
        "Category": ["Worker Hours", "Office Hours", "Robot", "CNC1", "CNC2", "Autoclave", "Material"],
        "Hours / Cost": [0.0]*7
    }),
    num_rows="fixed",
    key="input1"
)

# === INPUT: ACTUAL ===
st.markdown("### 📋 Actual Input")
input2 = st.data_editor(
    pd.DataFrame({
        "Category": ["Worker Hours", "Office Hours", "Robot", "CNC1", "CNC2", "Autoclave", "Material"],
        "Hours / Cost": [0.0]*7
    }),
    num_rows="fixed",
    key="input2"
)

# === EXTRA COSTS (WARRANTY, WEAR, etc.) ===
st.markdown("### ⚙️ Extra Costs (USD)")
input3 = st.data_editor(
    pd.DataFrame({
        "Type": ["Warranty", "Wear & Tear"],
        "Amount (USD)": [0.0, 0.0]
    }),
    num_rows="fixed",
    key="input3"
)

# === MARGIN INPUT ===
st.markdown("### 💹 Planned Profit Margin")
margin = st.slider("Planned profit margin (%)", min_value=0.0, max_value=100.0, value=20.0) / 100

st.divider()
st.header("📉 Comparison Report (USD)")

# === COST CALCULATION ===
def calculate_cost(df, rate_worker, rate_office, rate_machine):
    df = df.copy()
    df["Cost (USD)"] = 0.0
    for i, row in df.iterrows():
        cat = row["Category"]
        val = row["Hours / Cost"]
        if "Worker" in cat:
            df.at[i, "Cost (USD)"] = val * rate_worker
        elif "Office" in cat:
            df.at[i, "Cost (USD)"] = val * rate_office
        elif cat in ["Robot", "CNC1", "CNC2", "Autoclave"]:
            df.at[i, "Cost (USD)"] = val * rate_machine
        elif cat == "Material":
            df.at[i, "Cost (USD)"] = val
    return df.set_index("Category")

plan_df = calculate_cost(input1, rate_worker, rate_office, rate_machine)
actual_df = calculate_cost(input2, rate_worker, rate_office, rate_machine)

# === COMPARISON TABLE ===
comparison = pd.DataFrame({
    "Planned (USD)": plan_df["Cost (USD)"],
    "Actual (USD)": actual_df["Cost (USD)"],
    "Difference (USD)": actual_df["Cost (USD)"] - plan_df["Cost (USD)"]
})

st.dataframe(comparison, use_container_width=True)

# === CHART ===
fig = px.bar(
    comparison.reset_index(),
    x="Category",
    y=["Planned (USD)", "Actual (USD)"],
    barmode="group",
    title="Cost Comparison by Category (USD)",
    color_discrete_sequence=["#1f77b4", "#ff7f0e"]
)
st.plotly_chart(fig, use_container_width=True)

# === PROFIT ANALYSIS ===
plan_total = plan_df["Cost (USD)"].sum()
actual_total = actual_df["Cost (USD)"].sum() + input3["Amount (USD)"].sum()
expected_profit = plan_total * margin
actual_profit = plan_total - actual_total
profit_diff = actual_profit - expected_profit

st.subheader("📌 Profit Summary (USD)")

col1, col2, col3 = st.columns(3)
col1.metric("Planned Cost", f"${plan_total:,.2f}")
col2.metric("Actual Cost", f"${actual_total:,.2f}")
col3.metric("Extra Costs", f"${input3['Amount (USD)'].sum():,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Planned Margin", f"{margin*100:.1f}%")
col5.metric("Actual Profit", f"${actual_profit:,.2f}")
col6.metric("Profit Delta", f"${profit_diff:,.2f}", delta_color="inverse")
