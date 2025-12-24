import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from streamlit_option_menu import option_menu
from PIL import Image

#LOGO VÀ TIÊU ĐỀ
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    logo_url = "highland.png"
    st.image(logo_url, width=190)

st.markdown("<h1 style='text-align: center;'>HIGHLANDS COFFEE</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("MENU")
    st.write("Tổng Quan")
    st.write("CRUD & Cleaning")
    st.write("Visualizations")
    st.write("Forecasting")
    st.write("Power BI Dashboard")
    default_index = 0,

selected = option_menu(
    menu_title=None,
    options=["HOME", "Nhập & quản lý dữ liệu", "Phân tích kết quả kinh doanh","Trực quan hóa dữ liệu","Dự báo doanh thu tương lai","Power BI Dashboard"],
    menu_icon=["cast","activity", "bar-chart", "graph-up", "clipboard-data"],
    default_index=0,
    orientation="horizontal",
)
#HOME
if selected == "HOME":
    st.markdown("<h1 style='text-align: center; color: #3E2723;'>PHÂN TÍCH KẾT QUẢ KINH DOANH HIGHLANDS COFFEE</h1>", unsafe_allow_html=True)

    # Hàng 1:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image("HLC_New_logo_5.1_Products__CAPPUCINO.jpg", caption="CAPPUCCINO")
    with col2:
        st.image("HLC_New_logo_5.1_Products__LATTE_1.jpg", caption="LATTE")
    with col3:
        st.image("HLC_New_logo_5.1_Products__AMERICANO_NONG.jpg", caption="AMERICANO")
    with col4:
        st.image("HLC_New_logo_5.1_Products__MOCHA.jpg", caption="MOCHA")
    with col5:
        st.image("HLC_New_logo_5.1_Products__PHIN_DEN_DA.jpg", caption="ICED BLACK COFFEE")


    # Hàng 2:
    col6, col7, col8, col9, col10 = st.columns(5)
    with col6:
        st.image("HLC_New_logo_5.1_Products__FREEZE_TRA_XANH.jpg", caption="GREEN TEA FREEZE")
    with col7:
        st.image("HLC_New_logo_5.1_Products__CLASSIC_FREEZE_PHINDI.jpg", caption="CLASSIC PHIN FREEZE")
    with col8:
        st.image("HLC_New_logo_5.1_Products__FREEZE_CHOCO.jpg", caption="CHOCOLATE FREEZE")
    with col9:
        st.image("HLC_New_logo_5.1_Products__COOKIES_FREEZE.jpg", caption="COOKIES AND CREAM")
    with col10:
        st.image("HLC_New_logo_5.1_Products__CARAMEL_FREEZE_PHINDI.jpg", caption="CARAMEL PHIN FREEZE")



# --- PHẦN 1: NHẬP DỮ LIỆU ---
elif selected == "Nhập & quản lý dữ liệu":
    st.header("📦 Nhập dữ liệu và Làm sạch")
    try:
        df_raw = pd.read_csv("data_1.csv")
        st.subheader("Dữ liệu gốc (Chưa xử lý)")
        st.dataframe(df_raw, use_container_width=True)

        if st.button("Tiến hành làm sạch và chuẩn hóa dữ liệu"):
            # Kiểm tra file
            if os.path.exists("output/cleaned_data.csv"):
                df_cleaned = pd.read_csv("output/cleaned_data.csv")
                st.success("Đã làm sạch dữ liệu thành công!")
                st.subheader("Dữ liệu sau khi chuẩn hóa")
                st.dataframe(df_cleaned, use_container_width=True)
                st.write(f"Tổng số bản ghi: {len(df_cleaned)}")
            else:
                st.error("Lỗi: Không tìm thấy file cleaned_data.csv")
    except FileNotFoundError:
        st.error("Vui lòng kiểm tra file data_1.csv trong thư mục dự án.")

# --- PHẦN 2: PHÂN TÍCH ---
elif selected == "Phân tích kết quả kinh doanh":
    st.header("📊 Thống kê và Phân tích kết quả")
    try:
        path_pivot = "output/pivot_tables.xlsx"
        st.subheader("Phân tích Sản phẩm theo Kênh")
        df_kênh = pd.read_excel(path_pivot, sheet_name=0)
        st.dataframe(df_kênh, use_container_width=True)

        st.subheader("Hiệu suất Nhân viên")
        df_nv = pd.read_excel(path_pivot, sheet_name='staff_performance')
        st.dataframe(df_nv, use_container_width=True)
        st.bar_chart(df_nv.set_index('Staff_id')['Revenue'])

    except Exception as e:
        st.warning(f"Lỗi: {e}. Vui lòng chạy file pivot_analysis.py trước.")

# --- PHẦN 3: TRỰC QUAN HÓA
elif selected == "Trực quan hóa dữ liệu":
    st.header("📊 Hệ thống Trực quan hóa (Biểu đồ đã trích xuất)")

    # Tạo các Tab để xem từng biểu đồ
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12 = st.tabs([
        "🛒 Channel Analysis",
        "Channel by Product",
        "Channel trend",
        "Daily Revenue",
        "Monthly Trend",
        "Product Size Distribution",
        "Quarterly Comparison",
        "Staff by channel",
        "Staff trend",
        "Top Products Quantity",
        "Top Products Revenue",
        "Top Staff Performance",
    ])

    with t1:
        st.subheader("Phân phối doanh thu theo kênh")
        chart_path = "output/charts/"
        st.image(f"{chart_path}channel_analysis.png", use_container_width=True)
        st.info("So sánh tổng quan tỷ trọng doanh thu giữa các kênh Online và Offline.")

    with t2:
        st.subheader("Phân phối kênh cho top 5 sản phẩm")
        st.image(f"{chart_path}channel_by_product.png", use_container_width=True)

    with t3:
        st.subheader("Xu hướng doanh thu")
        st.image(f"{chart_path}channel_trend.png", use_container_width=True)

    with t4:
        st.subheader("Biến động Doanh thu hàng ngày")
        st.image(f"{chart_path}daily_revenue.png", use_container_width=True)

    with t5:
        st.subheader("Doanh thu theo Tháng")
        st.image(f"{chart_path}monthly_trend.png", use_container_width=True)

    with t6:
        st.subheader("Phân bổ Kích cỡ Sản phẩm (S, M, L)")
        st.image(f"{chart_path}product_size_distribution.png", use_container_width=True)

    with t7:
        st.subheader("So sánh Hiệu suất theo Quý")
        st.image(f"{chart_path}quarterly_comparison.png", use_container_width=True)

    with t8:
        st.subheader("Phân bổ Nhân viên theo Kênh bán")
        st.image(f"{chart_path}staff_by_channel.png", use_container_width=True)

    with t9:
        st.subheader("Xu hướng làm việc của Đội ngũ Nhân viên")
        st.image(f"{chart_path}staff_trend.png", use_container_width=True)

    with t10:
        st.subheader("Top Sản phẩm bán chạy nhất (Số lượng)")
        st.image(f"{chart_path}top_products_quantity.png", use_container_width=True)

    with t11:
        st.subheader("Top Sản phẩm mang lại Doanh thu cao nhất")
        st.image(f"{chart_path}top_products_revenue.png", use_container_width=True)

    with t12:
        st.subheader("Bảng Hiệu suất Nhân viên (Top 10)")
        st.image(f"{chart_path}top_staff_performance.png", use_container_width=True)
        st.success("Cá nhân dẫn đầu đang đóng góp đáng kể vào doanh thu tổng của cửa hàng.")

# --- PHẦN 4: DỰ BÁO DOANH THU
elif selected == "Dự báo doanh thu tương lai":
    st.header("🔮 Dự báo Doanh thu tương lai")

    try:
        path_pivot = "output/pivot_tables.xlsx"
        # 1. Đọc dữ liệu
        df_monthly = pd.read_excel(path_pivot, sheet_name='monthly_trend')

        # 2. HIỂN THỊ BẢNG
        st.subheader("Dữ liệu xu hướng hàng tháng")
        st.dataframe(df_monthly, use_container_width=True)

        # 3. Kiểm tra và xử lý dữ liệu để dự báo
        if 'Year_Month' in df_monthly.columns and 'Revenue' in df_monthly.columns:
            y = df_monthly['Revenue'].values
            X = np.arange(len(y))

            # Thuật toán Hồi quy
            a, b = np.polyfit(X, y, 1)

            # Thanh slider tương tác
            num_periods = st.slider("Dự báo thêm bao nhiêu tháng:", 1, 12, 3)

            future_X = np.arange(len(y), len(y) + num_periods)
            future_y = a * future_X + b

            # 4. HIỂN THỊ CHỈ SỐ
            c1, c2 = st.columns(2)
            with c1:
                st.metric(f"Dự báo tháng thứ +{num_periods}", f"{future_y[-1]:,.0f} VNĐ")
            with c2:
                st.metric("Tốc độ tăng trưởng", f"{a:,.0f} VNĐ/tháng")

            # 5. VẼ BIỂU ĐỒ
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df_monthly['Year_Month'], y, color='#8A2432', marker='o', label='Thực tế')

            full_X = np.append(X, future_X)
            ax.plot(full_X, a * full_X + b, color='gray', linestyle='--', label='Xu hướng')
            ax.scatter(future_X, future_y, color='gold', s=100, label='Dự báo')

            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("Không tìm thấy cột 'Year_Month' hoặc 'Revenue' để tính toán dự báo.")

    except Exception as e:
        st.error(f"Lỗi: {e}")

# --- PHẦN 5: POWER BI DASHBOARD

elif selected == "Power BI Dashboard":
    st.header("📊 Hệ thống báo cáo Power BI")

    pbi_url = "https://app.powerbi.com/reportEmbed?reportId=5447e2ef-f67e-4dba-b056-f1975b969541&autoAuth=true&ctid=fc0bdaaf-292e-45cc-b51f-872867f9c981"

    st.link_button("🚀 TRUY CẬP POWER BI DASHBOARD", pbi_url, type="primary", use_container_width=True)
