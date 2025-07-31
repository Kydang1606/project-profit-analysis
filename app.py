import streamlit as st
import pandas as pd
import plotly.express as px

# === Constants ===
LABOR_COST_WORKER = 13.41
LABOR_COST_OFFICE = 31.25
MACHINE_COST = {
    'CNC': 18.33,
    'Robot': 19.79,
    'Autoclave': 49.98
}

st.set_page_config(page_title="Cost Estimation Tool", layout="wide")
st.title("📊 Cost Estimation & Comparison Dashboard")

# === Project Info ===
st.markdown("### 📁 Project Information")
project_name = st.text_input("Project Name")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# === Inputs ===
st.markdown("### 1. Input Estimate and Actual Data")

with st.expander("🔧 Estimated Cost Input"):
    est_labor_worker = st.number_input("Estimated Labor Hours - Worker", min_value=0.0, step=0.1, format="%.2f")
    est_labor_office = st.number_input("Estimated Labor Hours - Office", min_value=0.0, step=0.1, format="%.2f")
    est_machine = {}
    for machine in MACHINE_COST:
        est_machine[machine] = st.number_input(f"Estimated Machine Hours - {machine}", min_value=0.0, step=0.1, format="%.2f")
    est_material = st.number_input("Estimated Material Cost (USD)", min_value=0.0, step=1.0, format="%.2f")

with st.expander("📌 Actual Cost Input"):
    act_labor_worker = st.number_input("Actual Labor Hours - Worker", min_value=0.0, step=0.1, format="%.2f")
    act_labor_office = st.number_input("Actual Labor Hours - Office", min_value=0.0, step=0.1, format="%.2f")
    act_machine = {}
    for machine in MACHINE_COST:
        act_machine[machine] = st.number_input(f"Actual Machine Hours - {machine}", min_value=0.0, step=0.1, format="%.2f")
    act_material = st.number_input("Actual Material Cost (USD)", min_value=0.0, step=1.0, format="%.2f")

with st.expander("🛠️ Additional Actual Cost: Warranty & Afterwork"):
    warranty_cost = st.number_input("Warranty Cost (USD)", min_value=0.0, step=1.0, format="%.2f")
    afterwork_cost = st.number_input("Afterwork Cost (USD)", min_value=0.0, step=1.0, format="%.2f")

# === Calculations ===
est_cost = {
    "Labor - Worker": est_labor_worker * LABOR_COST_WORKER,
    "Labor - Office": est_labor_office * LABOR_COST_OFFICE,
    "Material": est_material
}
for machine in MACHINE_COST:
    est_cost[machine] = est_machine[machine] * MACHINE_COST[machine]
est_total = sum(est_cost.values())

act_cost = {
    "Labor - Worker": act_labor_worker * LABOR_COST_WORKER,
    "Labor - Office": act_labor_office * LABOR_COST_OFFICE,
    "Material": act_material
}
for machine in MACHINE_COST:
    act_cost[machine] = act_machine[machine] * MACHINE_COST[machine]
act_total = sum(act_cost.values())
act_total_with_extra = act_total + warranty_cost + afterwork_cost

# === Summary Table ===
st.markdown("### 2. Summary Table")
data = []
for category in est_cost:
    estimated = est_cost[category]
    actual = act_cost.get(category, 0.0)
    diff = actual - estimated
    percent_diff = (diff / estimated * 100) if estimated != 0 else 0
    data.append({
        "Category": category,
        "Estimated (USD)": estimated,
        "Actual (USD)": actual,
        "Difference (USD)": diff,
        "Difference (%)": round(percent_diff, 2)
    })
summary_df = pd.DataFrame(data)
st.dataframe(summary_df, use_container_width=True)

# === Pie Charts ===
col1, col2 = st.columns(2)
with col1:
    fig1 = px.pie(values=list(est_cost.values()), names=list(est_cost.keys()), title="Estimated Cost Composition")
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.pie(values=list(act_cost.values()), names=list(act_cost.keys()), title="Actual Cost Composition")
    st.plotly_chart(fig2, use_container_width=True)

# === Bar Chart ===
chart_df = pd.DataFrame({
    "Category": list(est_cost.keys()),
    "Estimated": list(est_cost.values()),
    "Actual": [act_cost[k] for k in est_cost.keys()]
})
fig3 = px.bar(chart_df, x="Category", y=["Estimated", "Actual"], barmode="group", title="Cost Comparison by Category")
st.plotly_chart(fig3, use_container_width=True)

# === Final Summary ===
st.markdown("### 3. Final Comparison")
final_df = pd.DataFrame({
    "Item": [
        "Estimated Total",
        "Actual Total (No Warranty/Afterwork)",
        "Warranty Cost",
        "Afterwork Cost",
        "Actual Total (All Included)",
        "Gap (USD)",
        "Gap (%)"
    ],
    "Value (USD)": [
        est_total,
        act_total,
        warranty_cost,
        afterwork_cost,
        act_total_with_extra,
        act_total_with_extra - est_total,
        round((act_total_with_extra - est_total) / est_total * 100, 2) if est_total != 0 else 0.0
    ]
})
st.dataframe(final_df, use_container_width=True)

# === Fixed Unit Cost Info ===
st.markdown("### 4. Fixed Unit Costs (USD/hour)")
st.write(f"👷 Labor - Worker: ${LABOR_COST_WORKER:.2f} | 🧑‍💼 Office: ${LABOR_COST_OFFICE:.2f}")
st.write("🛠️ Machine Rates:")
for machine, cost in MACHINE_COST.items():
    st.write(f"- {machine}: ${cost:.2f} per hour")
