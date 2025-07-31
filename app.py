import streamlit as st
import pandas as pd

# Fixed unit prices (USD/hour)
UNIT_PRICES = {
    'Labor': 10,
    'Office': 15,
    'CNC': 25,
    'Robot': 30,
    'Autoclave': 35,
}

st.title("💰 Cost Comparison Tool")

st.markdown("## 📥 Input Estimated Cost")
with st.form("estimate_form"):
    est_labor = st.number_input("Labor Hours (Estimated)", min_value=0.0, step=1.0)
    est_office = st.number_input("Office Hours (Estimated)", min_value=0.0, step=1.0)
    est_cnc = st.number_input("CNC Hours (Estimated)", min_value=0.0, step=1.0)
    est_robot = st.number_input("Robot Hours (Estimated)", min_value=0.0, step=1.0)
    est_autoclave = st.number_input("Autoclave Hours (Estimated)", min_value=0.0, step=1.0)
    est_material = st.number_input("Material Cost (Estimated, USD)", min_value=0.0, step=10.0)
    margin_percent = st.number_input("Margin (%)", min_value=0.0, step=0.5)

    submitted_est = st.form_submit_button("Submit Estimated Cost")

st.markdown("---")
st.markdown("## 📥 Input Actual Cost")
with st.form("actual_form"):
    act_labor = st.number_input("Labor Hours (Actual)", min_value=0.0, step=1.0)
    act_office = st.number_input("Office Hours (Actual)", min_value=0.0, step=1.0)
    act_cnc = st.number_input("CNC Hours (Actual)", min_value=0.0, step=1.0)
    act_robot = st.number_input("Robot Hours (Actual)", min_value=0.0, step=1.0)
    act_autoclave = st.number_input("Autoclave Hours (Actual)", min_value=0.0, step=1.0)
    act_material = st.number_input("Material Cost (Actual, USD)", min_value=0.0, step=10.0)

    submitted_act = st.form_submit_button("Submit Actual Cost")

if submitted_est and submitted_act:
    # Calculate estimated cost
    est_costs = {
        'Labor': est_labor * UNIT_PRICES['Labor'],
        'Office': est_office * UNIT_PRICES['Office'],
        'CNC': est_cnc * UNIT_PRICES['CNC'],
        'Robot': est_robot * UNIT_PRICES['Robot'],
        'Autoclave': est_autoclave * UNIT_PRICES['Autoclave'],
        'Material': est_material,
    }
    total_estimate = sum(est_costs.values())
    selling_price = total_estimate * (1 + margin_percent / 100)

    # Calculate actual cost
    act_costs = {
        'Labor': act_labor * UNIT_PRICES['Labor'],
        'Office': act_office * UNIT_PRICES['Office'],
        'CNC': act_cnc * UNIT_PRICES['CNC'],
        'Robot': act_robot * UNIT_PRICES['Robot'],
        'Autoclave': act_autoclave * UNIT_PRICES['Autoclave'],
        'Material': act_material,
    }
    total_actual = sum(act_costs.values())

    # Create DataFrame for output
    data = []
    for key in est_costs:
        data.append({
            'Category': key,
            'Estimated Cost': est_costs[key],
            'Actual Cost': act_costs[key],
            'Difference': act_costs[key] - est_costs[key],
        })
    df = pd.DataFrame(data)
    df.loc[len(df)] = {
        'Category': 'TOTAL',
        'Estimated Cost': total_estimate,
        'Actual Cost': total_actual,
        'Difference': total_actual - total_estimate,
    }

    # Display results
    st.markdown("## 📊 Cost Comparison")
    st.dataframe(df.style.format({
        'Estimated Cost': '${:,.2f}',
        'Actual Cost': '${:,.2f}',
        'Difference': '${:,.2f}',
    }))

    st.markdown(f"**💰 Selling Price (with {margin_percent:.1f}% margin):** ${selling_price:,.2f}")
    st.markdown(f"**📉 Profit / Loss:** ${selling_price - total_actual:,.2f}")
