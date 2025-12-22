"""BẢNG 3: PHÂN TÍCH XU HƯỚNG DOANH THU THEO THỜI GIAN"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


class RevenueTrendAnalyzer:
    def __init__(self, data_path='output/cleaned_data.csv'):
        self.data_path = data_path
        self.df = None
        self.df_trend = None
        self.total_revenue = 0

        print("=" * 60)
        print("BẢNG 3: XU HƯỚNG DOANH THU THEO THỜI GIAN")
        print(f"Đọc từ file: {data_path}")
        print("=" * 60)

        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            print(f"Đã tải {len(self.df)} dòng dữ liệu")
            self._prepare_trend_data()

        except Exception as e:
            print(f"Lỗi đọc file: {e}")
            print("Sử dụng dữ liệu mẫu thay thế")
            self._use_sample_data()

    def _prepare_trend_data(self):
        print("\nĐang tìm kiếm cột ngày tháng và doanh thu...")

        date_keywords = ['date', 'ngay', 'thoi_gian', 'time', 'datetime']
        date_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in date_keywords):
                date_col = col
                print(f"Tìm thấy cột ngày tháng: {date_col}")
                break

        revenue_keywords = ['revenue', 'doanh_thu', 'doanh thu', 'total', 'amount']
        revenue_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in revenue_keywords):
                revenue_col = col
                print(f"Tìm thấy cột doanh thu: {revenue_col}")
                break

        if not revenue_col:
            self._create_revenue_column()
            if hasattr(self, 'revenue_col'):
                revenue_col = self.revenue_col

        if not date_col or not revenue_col:
            print("Không tìm thấy cột ngày tháng hoặc doanh thu")
            self._use_sample_data()
            return

        try:
            self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce')

            self.df['Year'] = self.df[date_col].dt.year
            self.df['Month'] = self.df[date_col].dt.month
            self.df['Quarter'] = self.df[date_col].dt.quarter

            print("\nTổng hợp doanh thu theo thời gian...")

            # Tổng hợp theo năm
            yearly_revenue = self.df.groupby('Year')[revenue_col].sum().reset_index()
            yearly_revenue = yearly_revenue.sort_values('Year')

            self.df_trend = yearly_revenue
            self.df_trend.columns = ['Year', 'Revenue']

            # Chuyển năm sang string
            self.df_trend['Year'] = self.df_trend['Year'].astype(str)

            self.total_revenue = self.df_trend['Revenue'].sum()
            self.df_trend['Percentage'] = (self.df_trend['Revenue'] / self.total_revenue * 100).round(2)
            self.df_trend['Revenue_Mil'] = (self.df_trend['Revenue'] / 1000000).round(2)

            # Tính thay đổi
            self.df_trend['Change'] = self.df_trend['Revenue'].pct_change() * 100
            self.df_trend['YoY_Change'] = self.df_trend['Revenue'].diff()
            self.df_trend['YoY_Change_Mil'] = (self.df_trend['YoY_Change'] / 1000000).round(2)

            print(f"Đã tổng hợp doanh thu từ {len(self.df_trend)} năm")

        except Exception as e:
            print(f"Lỗi xử lý ngày tháng: {e}")
            self._use_sample_data()

    def _create_revenue_column(self):
        print("Không tìm thấy cột doanh thu, đang tìm số lượng và giá...")

        qty_keywords = ['quantity', 'qty', 'so_luong', 'số lượng', 'amount']
        qty_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in qty_keywords):
                qty_col = col
                break

        price_keywords = ['price', 'gia', 'đơn_giá', 'đơn giá', 'unit_price']
        price_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in price_keywords):
                price_col = col
                break

        if qty_col and price_col:
            print(f"Tìm thấy: Số lượng ({qty_col}), Giá ({price_col})")
            self.df['revenue'] = self.df[qty_col] * self.df[price_col]
            self.revenue_col = 'revenue'
            print(f"Đã tạo cột doanh thu từ {qty_col} × {price_col}")
        else:
            print("Không tìm thấy cột số lượng hoặc giá")
            self.revenue_col = None

    def _use_sample_data(self):
        print("Sử dụng dữ liệu mẫu")
        self.df_trend = pd.DataFrame({
            'Year': ['2021', '2022', '2023', '2024'],
            'Revenue': [40527190, 44343010, 40118860, 451500],
            'Percentage': [32.31, 35.34, 31.97, 0.36],
            'Revenue_Mil': [40.53, 44.34, 40.12, 0.45],
            'Change': [None, 9.42, -9.53, -88.77],
            'YoY_Change': [None, 3815820, -4224150, -39667360],
            'YoY_Change_Mil': [None, 3.82, -4.22, -39.67]
        })
        self.total_revenue = self.df_trend['Revenue'].sum()

    def display_table(self):
        if self.df_trend is None or self.df_trend.empty:
            print("Không có dữ liệu để hiển thị")
            return

        print(f"\nBẢNG XU HƯỚNG DOANH THU (Từ file: {os.path.basename(self.data_path)})")
        print("-" * 90)
        print(
            f"{'Năm':<8} {'Doanh thu (VND)':<20} {'Doanh thu (Triệu)':<18} {'Thay đổi %':<12} {'Thay đổi (Triệu)':<15} {'Tỷ trọng %':<12}")
        print("-" * 90)

        for _, row in self.df_trend.iterrows():
            revenue_pct = (row['Revenue'] / self.total_revenue * 100).round(2)
            change_pct = f"{row['Change']:.1f}%" if not pd.isna(row['Change']) else "N/A"
            change_mil = f"{row['YoY_Change_Mil']:+.1f}" if not pd.isna(row['YoY_Change_Mil']) else "N/A"

            print(f"{row['Year']:<8} {row['Revenue']:<20,} {row['Revenue_Mil']:<18,.2f} "
                  f"{change_pct:<12} {change_mil:<15} {revenue_pct:<12}")

        print("-" * 90)
        total_mil = self.total_revenue / 1000000
        print(f"{'TOTAL':<8} {self.total_revenue:<20,} {total_mil:<18,.2f} "
              f"{'N/A':<12} {'N/A':<15} {'100.00':<12}")
        print("-" * 90)

        print(f"\nPHÂN TÍCH XU HƯỚNG:")

        max_year = self.df_trend.loc[self.df_trend['Revenue'].idxmax()]
        min_year = self.df_trend.loc[self.df_trend['Revenue'].idxmin()]

        print(f"   Năm cao nhất: {max_year['Year']} - {max_year['Revenue_Mil']:,.1f} triệu VND")
        print(f"   Năm thấp nhất: {min_year['Year']} - {min_year['Revenue_Mil']:,.1f} triệu VND")

        growth_rates = self.df_trend['Change'].dropna()
        if len(growth_rates) > 0:
            avg_growth = growth_rates.mean()
            print(f"   Tăng trưởng trung bình: {avg_growth:.1f}%")

    def visualize_line_chart(self, save_path='visualizations/revenue_trend_line.png'):
        if self.df_trend is None or self.df_trend.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        ax1.plot(self.df_trend['Year'], self.df_trend['Revenue_Mil'],
                 marker='o', linewidth=3, markersize=10,
                 color='#2196F3', label='Doanh thu')

        for x, y in zip(self.df_trend['Year'], self.df_trend['Revenue_Mil']):
            ax1.text(x, y + 0.2, f'{y:.1f}',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax1.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax1.set_title('XU HƯỚNG DOANH THU THEO NĂM', fontsize=14, fontweight='bold', pad=20)
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2.fill_between(self.df_trend['Year'], self.df_trend['Revenue_Mil'],
                         alpha=0.4, color='#4CAF50')
        ax2.plot(self.df_trend['Year'], self.df_trend['Revenue_Mil'],
                 marker='s', linewidth=2, color='#2E7D32')

        for x, y in zip(self.df_trend['Year'], self.df_trend['Revenue_Mil']):
            ax2.text(x, y + 0.2, f'{y:.1f}',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax2.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax2.set_title('DOANH THU THEO NĂM (AREA CHART)', fontsize=14, fontweight='bold', pad=20)
        ax2.grid(True, alpha=0.3)

        bars3 = ax3.bar(self.df_trend['Year'], self.df_trend['Revenue_Mil'],
                        color=plt.cm.viridis(range(len(self.df_trend))),
                        alpha=0.7, label='Doanh thu')

        ax3.plot(self.df_trend['Year'], self.df_trend['Revenue_Mil'],
                 color='red', marker='o', linewidth=2,
                 label='Xu hướng')

        ax3.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax3.set_title('DOANH THU VÀ XU HƯỚNG', fontsize=14, fontweight='bold', pad=20)
        ax3.legend()

        for bar, rev_mil in zip(bars3, self.df_trend['Revenue_Mil']):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                     f'{rev_mil:.1f}', ha='center', va='bottom', fontsize=9)

        change_data = self.df_trend['Change'].dropna()
        if len(change_data) > 0:
            bars4 = ax4.bar(self.df_trend['Year'][1:], change_data,
                            color=['green' if x > 0 else 'red' for x in change_data],
                            alpha=0.7)

            ax4.set_xlabel('Năm', fontsize=12, fontweight='bold')
            ax4.set_ylabel('Tăng trưởng (%)', fontsize=12, fontweight='bold')
            ax4.set_title('TỐC ĐỘ TĂNG TRƯỞNG THEO NĂM', fontsize=14, fontweight='bold', pad=20)
            ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)

            for i, change in enumerate(change_data):
                ax4.text(i + 1, change + (0.5 if change > 0 else -1.5),
                         f'{change:+.1f}%',
                         ha='center', va='bottom' if change > 0 else 'top',
                         fontsize=10, fontweight='bold')

        plt.tight_layout()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path.replace('.png', '_dashboard.png'), dpi=300, bbox_inches='tight')
        print(f"Đã lưu dashboard tại: {save_path.replace('.png', '_dashboard.png')}")
        plt.show()

    def run_analysis(self):
        print("\n" + "=" * 60)
        print("PHÂN TÍCH BẢNG 3: XU HƯỚNG DOANH THU THEO THỜI GIAN")
        print("=" * 60)

        self.display_table()
        self.visualize_line_chart()


if __name__ == "__main__":
    analyzer3 = RevenueTrendAnalyzer(data_path='output/cleaned_data.csv')
    analyzer3.run_analysis()