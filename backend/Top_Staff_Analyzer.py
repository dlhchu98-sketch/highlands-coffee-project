"""BẢNG 4: PHÂN TÍCH TOP NHÂN VIÊN XUẤT SẮC"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


class TopStaffAnalyzer:
    def __init__(self, data_path='output/cleaned_data.csv', show_top=10):
        self.data_path = data_path
        self.df = None
        self.df_staff = None
        self.total_revenue = 0
        self.show_top = show_top

        print("=" * 60)
        print(f"BẢNG 4: TOP {show_top} NHÂN VIÊN XUẤT SẮC")
        print(f"Đọc từ file: {data_path}")
        print("=" * 60)

        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            print(f"Đã tải {len(self.df)} dòng dữ liệu")
            self._prepare_staff_data()

        except Exception as e:
            print(f"Lỗi đọc file: {e}")
            print("Sử dụng dữ liệu mẫu thay thế")
            self._use_sample_data()

    def _prepare_staff_data(self):
        print("\nĐang tìm kiếm cột nhân viên và doanh thu...")

        staff_keywords = ['staff', 'nhan_vien', 'employee', 'sales_person', 'nv']
        staff_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in staff_keywords):
                staff_col = col
                print(f"Tìm thấy cột nhân viên: {staff_col}")
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

        if not staff_col or not revenue_col:
            print("Không tìm thấy cột nhân viên hoặc doanh thu")
            self._use_sample_data()
            return

        print(f"\nTổng hợp doanh thu theo {staff_col}...")
        staff_revenue = self.df.groupby(staff_col)[revenue_col].sum().reset_index()
        staff_revenue = staff_revenue.sort_values(revenue_col, ascending=False)

        # Lấy top nhân viên
        if len(staff_revenue) > self.show_top:
            top_staff = staff_revenue.head(self.show_top)
            other_revenue = staff_revenue.iloc[self.show_top:][revenue_col].sum()

            other_row = pd.DataFrame({
                staff_col: ['Khác'],
                revenue_col: [other_revenue]
            })
            self.df_staff = pd.concat([top_staff, other_row], ignore_index=True)
        else:
            self.df_staff = staff_revenue

        self.df_staff.columns = ['Staff_ID', 'Revenue']
        self.total_revenue = self.df_staff['Revenue'].sum()

        # Tính tỷ trọng và xếp hạng
        self.df_staff['Percentage'] = (self.df_staff['Revenue'] / self.total_revenue * 100).round(3)
        self.df_staff['Rank'] = range(1, len(self.df_staff) + 1)
        self.df_staff['Revenue_Mil'] = (self.df_staff['Revenue'] / 1000000).round(3)

        print(f"Đã tổng hợp {len(self.df_staff)} nhân viên")

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
        self.df_staff = pd.DataFrame({
            'Staff_ID': ['NV1', 'NV5', 'NV50', 'NV12', 'NV8', 'NV25', 'NV33', 'NV7', 'NV19', 'NV41'],
            'Revenue': [4005910, 1988520, 3439990, 1785640, 2256780, 1897540, 1567820, 2345670, 1987650, 1678900],
            'Percentage': [3.19, 1.59, 2.74, 1.42, 1.80, 1.51, 1.25, 1.87, 1.58, 1.34],
            'Revenue_Mil': [4.01, 1.99, 3.44, 1.79, 2.26, 1.90, 1.57, 2.35, 1.99, 1.68]
        })
        self.total_revenue = self.df_staff['Revenue'].sum()
        self.df_staff['Rank'] = range(1, len(self.df_staff) + 1)

    def display_table(self):
        if self.df_staff is None or self.df_staff.empty:
            print("Không có dữ liệu để hiển thị")
            return

        print(f"\nTOP {len(self.df_staff)} NHÂN VIÊN XUẤT SẮC (Từ file: {os.path.basename(self.data_path)})")
        print("-" * 90)
        print(f"{'Hạng':<6} {'Mã NV':<10} {'Doanh thu (VND)':<20} {'Doanh thu (Triệu)':<15} {'Tỷ trọng %':<12}")
        print("-" * 90)

        for _, row in self.df_staff.iterrows():
            print(
                f"{row['Rank']:<6} {row['Staff_ID']:<10} {row['Revenue']:<20,} {row['Revenue_Mil']:<15,.3f} {row['Percentage']:<12}")

        print("-" * 90)
        total_mil = self.total_revenue / 1000000
        print(f"{'TOTAL':<16} {self.total_revenue:<20,} {total_mil:<15,.3f} {'100.00':<12}")
        print("-" * 90)

        top_revenue = self.df_staff.iloc[0]['Revenue']
        top_percentage = self.df_staff.iloc[0]['Percentage']

        print(f"\nPHÂN TÍCH TOP NHÂN VIÊN:")
        print(f"   Nhân viên xuất sắc nhất: {self.df_staff.iloc[0]['Staff_ID']}")
        print(f"   Doanh thu: {top_revenue:,.0f} VND ({top_percentage:.2f}% tổng doanh thu)")

        if len(self.df_staff) > 1:
            avg_top = self.df_staff['Revenue_Mil'].mean()
            print(f"   Doanh thu trung bình top {len(self.df_staff)}: {avg_top:.3f} triệu/nhân viên")

    def visualize_horizontal_bar(self, save_path='visualizations/top_staff_horizontal.png'):
        if self.df_staff is None or self.df_staff.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        df_top = self.df_staff.sort_values('Revenue', ascending=True)

        plt.figure(figsize=(14, 10))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

        bars1 = ax1.barh(range(len(df_top)), df_top['Revenue_Mil'],
                         color=plt.cm.viridis(np.linspace(0, 1, len(df_top))))

        ax1.set_yticks(range(len(df_top)))
        ax1.set_yticklabels([f"{row['Staff_ID']} (Hạng {row['Rank']})"
                             for _, row in df_top.iterrows()], fontsize=10)
        ax1.set_xlabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax1.set_title(f'TOP {len(df_top)} NHÂN VIÊN XUẤT SẮC', fontsize=14, fontweight='bold', pad=20)
        ax1.invert_yaxis()

        for i, (bar, rev_mil, pct) in enumerate(zip(bars1, df_top['Revenue_Mil'], df_top['Percentage'])):
            width = bar.get_width()
            ax1.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                     f'{rev_mil:.3f} triệu\n({pct:.3f}%)',
                     va='center', fontsize=9, fontweight='bold')

        # Lollipop chart
        for i, rev_mil in enumerate(df_top['Revenue_Mil']):
            ax2.plot([0, rev_mil], [i, i], color='gray', alpha=0.5, linewidth=1)

        scatter = ax2.scatter(df_top['Revenue_Mil'], range(len(df_top)),
                              s=300, c=df_top['Revenue_Mil'],
                              cmap='viridis', alpha=0.7, edgecolors='black')

        ax2.set_yticks(range(len(df_top)))
        ax2.set_yticklabels([f"{row['Staff_ID']}"
                             for _, row in df_top.iterrows()], fontsize=10)
        ax2.set_xlabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax2.set_title(f'TOP NHÂN VIÊN - LOLLIPOP CHART',
                      fontsize=14, fontweight='bold', pad=20)
        ax2.invert_yaxis()

        for i, (rev_mil, pct, rank) in enumerate(zip(df_top['Revenue_Mil'],
                                                     df_top['Percentage'],
                                                     df_top['Rank'])):
            ax2.text(rev_mil + 0.1, i,
                     f'Hạng {rank}: {rev_mil:.3f} triệu\n({pct:.3f}%)',
                     va='center', fontsize=9, fontweight='bold')

        plt.colorbar(scatter, ax=ax2, label='Doanh thu (Triệu VND)')

        info_text = (f"Top {len(df_top)} nhân viên\n"
                     f"Doanh thu: {df_top['Revenue_Mil'].sum():.3f} triệu VND\n"
                     f"Chiếm: {(df_top['Revenue'].sum() / self.total_revenue * 100).round(2)}% tổng")

        ax2.text(0.95, 0.02, info_text,
                 transform=ax2.transAxes,
                 fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
                 verticalalignment='bottom', horizontalalignment='right')

        plt.tight_layout()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Đã lưu biểu đồ tại: {save_path}")
        plt.show()

    def run_analysis(self):
        print("\n" + "=" * 60)
        print(f"PHÂN TÍCH BẢNG 4: TOP {self.show_top} NHÂN VIÊN XUẤT SẮC")
        print("=" * 60)

        self.display_table()
        self.visualize_horizontal_bar()


if __name__ == "__main__":
    analyzer4 = TopStaffAnalyzer(data_path='output/cleaned_data.csv', show_top=10)
    analyzer4.run_analysis()