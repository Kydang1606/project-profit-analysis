import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🔍 Phân Tích Lợi Nhuận Dự Án", layout="wide")

st.title("📊 Ứng Dụng Phân Tích Lợi Nhuận Dự Án")

st.markdown("### 📝 Nhập dữ liệu dự toán (Input 1)")
input1_data = st.data_editor(
    pd.DataFrame({
        "Hạng mục": ["Giờ công công nhân", "Giờ công văn phòng", "Robot", "CNC1", "CNC2", "Autoclave", "Vật liệu"],
        "Giá trị": [0]*7
    }),
    num_rows="fixed",
    key="input1"
)

st.markdown("### 📝 Nhập dữ liệu thực tế (Input 2)")
input2_data = st.data_editor(
    pd.DataFrame({
        "Hạng mục": ["Giờ công công nhân", "Giờ công văn phòng", "Robot", "CNC1", "CNC2", "Autoclave", "Vật liệu"],
        "Giá trị": [0]*7
    }),
    num_rows="fixed",
    key="input2"
)

st.markdown("### 📝 Nhập chi phí bảo hành / hao mòn (Input 3 - tuỳ chọn)")
input3_data = st.data_editor(
    pd.DataFrame({
        "Loại chi phí": ["Bảo hành", "Hao mòn"],
        "Giá trị": [0, 0]
    }),
    num_rows="fixed",
    key="input3"
)

st.markdown("### 💹 Nhập biên độ lợi nhuận kế hoạch (Input 4)")
margin = st.slider("Biên độ lợi nhuận kế hoạch (%)", min_value=0.0, max_value=100.0, value=20.0) / 100

# === So sánh dữ liệu ===
st.divider()
st.header("📉 So sánh chi phí dự toán và thực tế")

def summarize(df):
    return df.set_index("Hạng mục")["Giá trị"]

cost_plan = summarize(input1_data)
cost_actual = summarize(input2_data)
comparison = pd.DataFrame({
    "Dự toán": cost_plan,
    "Thực tế": cost_actual,
    "Chênh lệch": cost_actual - cost_plan
})

st.dataframe(comparison, use_container_width=True)

# === Biểu đồ ===
fig = px.bar(
    comparison.reset_index(),
    x="Hạng mục",
    y=["Dự toán", "Thực tế"],
    barmode="group",
    title="So sánh chi phí từng hạng mục",
    color_discrete_sequence=["#1f77b4", "#ff7f0e"]
)
st.plotly_chart(fig, use_container_width=True)

# === Tổng hợp chi phí và lợi nhuận ===
total_plan = cost_plan.sum()
total_actual = cost_actual.sum() + input3_data["Giá trị"].sum()
expected_profit = total_plan * margin
actual_profit = total_plan - total_actual
profit_diff = actual_profit - expected_profit

st.subheader("📌 Tóm tắt lợi nhuận")

col1, col2, col3 = st.columns(3)
col1.metric("Tổng chi phí kế hoạch", f"{total_plan:,.0f}")
col2.metric("Tổng chi phí thực tế", f"{total_actual:,.0f}")
col3.metric("Chi phí phát sinh (Bảo hành / hao mòn)", f"{input3_data['Giá trị'].sum():,.0f}")

col4, col5, col6 = st.columns(3)
col4.metric("Biên lợi nhuận kế hoạch", f"{margin*100:.1f}%")
col5.metric("Lợi nhuận thực tế", f"{actual_profit:,.0f}")
col6.metric("Lệch so với kế hoạch", f"{profit_diff:,.0f}", delta_color="inverse")
