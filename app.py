import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Phân Tích Lợi Nhuận Dự Án", layout="wide")
st.title("📊 Ứng Dụng Phân Tích Lợi Nhuận Dự Án")

# === TỶ GIÁ VÀ ĐƠN GIÁ THEO GIỜ ===
st.markdown("### 💲 Cài đặt đơn giá và tỷ giá")
col1, col2, col3, col4 = st.columns(4)
rate_worker = col1.number_input("💼 Đơn giá giờ công công nhân (VND)", value=50000.0, step=1000.0, format="%.2f")
rate_office = col2.number_input("🧑‍💻 Đơn giá giờ công văn phòng (VND)", value=60000.0, step=1000.0, format="%.2f")
rate_machine = col3.number_input("🤖 Đơn giá giờ máy móc (Robot/CNC/Autoclave) (VND)", value=150000.0, step=1000.0, format="%.2f")
exchange_rate = col4.number_input("💱 Tỷ giá VND/USD", value=24000.0, step=100.0, format="%.2f")

# === NHẬP DỮ LIỆU DỰ TOÁN ===
st.markdown("### 📋 Nhập dữ liệu dự toán (Input 1)")
input1 = st.data_editor(
    pd.DataFrame({
        "Hạng mục": ["Giờ công công nhân", "Giờ công văn phòng", "Robot", "CNC1", "CNC2", "Autoclave", "Vật liệu"],
        "Số giờ / Giá trị": [0.0]*7
    }),
    num_rows="fixed",
    key="input1"
)

# === NHẬP DỮ LIỆU THỰC TẾ ===
st.markdown("### 📋 Nhập dữ liệu thực tế (Input 2)")
input2 = st.data_editor(
    pd.DataFrame({
        "Hạng mục": ["Giờ công công nhân", "Giờ công văn phòng", "Robot", "CNC1", "CNC2", "Autoclave", "Vật liệu"],
        "Số giờ / Giá trị": [0.0]*7
    }),
    num_rows="fixed",
    key="input2"
)

# === CHI PHÍ PHÁT SINH ===
st.markdown("### ⚙️ Chi phí bảo hành / hao mòn (Input 3 - tùy chọn)")
input3 = st.data_editor(
    pd.DataFrame({
        "Loại chi phí": ["Bảo hành", "Hao mòn"],
        "Giá trị (VND)": [0.0, 0.0]
    }),
    num_rows="fixed",
    key="input3"
)

# === BIÊN LỢI NHUẬN ===
st.markdown("### 💹 Nhập biên độ lợi nhuận kế hoạch (Input 4)")
margin = st.slider("Biên độ lợi nhuận kế hoạch (%)", min_value=0.0, max_value=100.0, value=20.0) / 100

st.divider()
st.header("📉 So sánh chi phí dự toán và thực tế")

# === HÀM TÍNH TOÁN CHI PHÍ THEO GIÁ GIỜ ===
def calculate_cost(df, rate_worker, rate_office, rate_machine):
    df = df.copy()
    df["Giá trị (VND)"] = 0.0
    for i, row in df.iterrows():
        category = row["Hạng mục"]
        hours = row["Số giờ / Giá trị"]
        if "công nhân" in category:
            df.at[i, "Giá trị (VND)"] = hours * rate_worker
        elif "văn phòng" in category:
            df.at[i, "Giá trị (VND)"] = hours * rate_office
        elif category in ["Robot", "CNC1", "CNC2", "Autoclave"]:
            df.at[i, "Giá trị (VND)"] = hours * rate_machine
        elif category == "Vật liệu":
            df.at[i, "Giá trị (VND)"] = hours  # Vật liệu đã là giá trị
    df["Giá trị (USD)"] = df["Giá trị (VND)"] / exchange_rate
    return df.set_index("Hạng mục")

# === TÍNH TOÁN ===
plan_df = calculate_cost(input1, rate_worker, rate_office, rate_machine)
actual_df = calculate_cost(input2, rate_worker, rate_office, rate_machine)

# === BẢNG SO SÁNH ===
comparison = pd.DataFrame({
    "Dự toán (VND)": plan_df["Giá trị (VND)"],
    "Thực tế (VND)": actual_df["Giá trị (VND)"],
    "Chênh lệch (VND)": actual_df["Giá trị (VND)"] - plan_df["Giá trị (VND)"],
    "Dự toán (USD)": plan_df["Giá trị (USD)"],
    "Thực tế (USD)": actual_df["Giá trị (USD)"],
})

st.dataframe(comparison, use_container_width=True)

# === BIỂU ĐỒ ===
fig = px.bar(
    comparison.reset_index(),
    x="Hạng mục",
    y=["Dự toán (VND)", "Thực tế (VND)"],
    barmode="group",
    title="So sánh chi phí từng hạng mục (VND)",
    color_discrete_sequence=["#1f77b4", "#ff7f0e"]
)
st.plotly_chart(fig, use_container_width=True)

# === TỔNG HỢP LỢI NHUẬN ===
plan_total = plan_df["Giá trị (VND)"].sum()
actual_total = actual_df["Giá trị (VND)"].sum() + input3["Giá trị (VND)"].sum()
expected_profit = plan_total * margin
actual_profit = plan_total - actual_total
profit_diff = actual_profit - expected_profit

st.subheader("📌 Tóm tắt lợi nhuận")

col1, col2, col3 = st.columns(3)
col1.metric("Chi phí dự toán (VND)", f"{plan_total:,.0f}")
col2.metric("Chi phí thực tế (VND)", f"{actual_total:,.0f}")
col3.metric("Chi phí phát sinh", f"{input3['Giá trị (VND)'].sum():,.0f}")

col4, col5, col6 = st.columns(3)
col4.metric("Biên độ kế hoạch", f"{margin*100:.1f}%")
col5.metric("Lợi nhuận thực tế (VND)", f"{actual_profit:,.0f}")
col6.metric("Lệch so với kế hoạch", f"{profit_diff:,.0f}", delta_color="inverse")

col7, col8 = st.columns(2)
col7.metric("Chi phí thực tế (USD)", f"{actual_total / exchange_rate:,.2f}")
col8.metric("Lợi nhuận thực tế (USD)", f"{actual_profit / exchange_rate:,.2f}")
