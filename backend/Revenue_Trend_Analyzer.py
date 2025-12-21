"""BẢNG 3: PHÂN TÍCH XU HƯỚNG DOANH THU THEO THỜI GIAN"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
class RevenueTrendAnalyzer:
    def __init__(self):
        # Dữ liệu từ Bảng 3
        self.data = {
            'Year': ['2021', '2022', '2023', '2024'],
            'Revenue': [40527190, 44343010, 40118860, 451500]
        }
        self.df = pd.DataFrame(self.data)
        self.total_revenue = self.df['Revenue'].sum()

        # Tính phần trăm thay đổi
        self.df['Change'] = self.df['Revenue'].pct_change() * 100
        self.df['YoY_Change'] = self.df['Revenue'].diff()

        # Chuyển đổi sang triệu đồng
        self.df['Revenue_Mil'] = (self.df['Revenue'] / 1000000).round(2)
        self.df['YoY_Change_Mil'] = (self.df['YoY_Change'] / 1000000).round(2)

        print("=" * 60)
        print("BẢNG 3: XU HƯỚNG DOANH THU THEO THỜI GIAN")
        print("=" * 60)

    def display_table(self):
        """Hiển thị bảng dữ liệu"""
        print("\nBẢNG XU HƯỚNG DOANH THU:")
        print("-" * 85)
        print(
            f"{'Năm':<8} {'Doanh thu (VND)':<20} {'Doanh thu (Triệu)':<18} {'Thay đổi %':<12} {'Thay đổi (Triệu)':<15} {'Tỷ trọng %':<12}")
        print("-" * 85)

        for _, row in self.df.iterrows():
            revenue_pct = (row['Revenue'] / self.total_revenue * 100).round(2)
            change_pct = f"{row['Change']:.1f}%" if not pd.isna(row['Change']) else "N/A"
            change_mil = f"{row['YoY_Change_Mil']:+.1f}" if not pd.isna(row['YoY_Change_Mil']) else "N/A"

            print(f"{row['Year']:<8} {row['Revenue']:<20,} {row['Revenue_Mil']:<18,.2f} "
                  f"{change_pct:<12} {change_mil:<15} {revenue_pct:<12}")

        print("-" * 85)
        total_mil = self.total_revenue / 1000000
        print(f"{'TOTAL':<8} {self.total_revenue:<20,} {total_mil:<18,.2f} "
              f"{'N/A':<12} {'N/A':<15} {'100.00':<12}")
        print("-" * 85)

        # Phân tích xu hướng
        print(f"\nPHÂN TÍCH XU HƯỚNG:")

        # Tìm năm cao nhất, thấp nhất
        max_year = self.df.loc[self.df['Revenue'].idxmax()]
        min_year = self.df.loc[self.df['Revenue'].idxmin()]

        print(f"   • Năm cao nhất: {max_year['Year']} - {max_year['Revenue_Mil']:,.1f} triệu VND")
        print(f"   • Năm thấp nhất: {min_year['Year']} - {min_year['Revenue_Mil']:,.1f} triệu VND")

        # Tính tăng trưởng trung bình
        growth_rates = self.df['Change'].dropna()
        if len(growth_rates) > 0:
            avg_growth = growth_rates.mean()
            print(f"   • Tăng trưởng trung bình: {avg_growth:.1f}%")

            if avg_growth > 0:
                print(f"   → Xu hướng: TĂNG TRƯỞNG TÍCH CỰC")
            else:
                print(f"   → Xu hướng: GIẢM SÚT")

        # So sánh 2023 vs 2022
        rev_2022 = self.df[self.df['Year'] == '2022']['Revenue'].values[0]
        rev_2023 = self.df[self.df['Year'] == '2023']['Revenue'].values[0]
        change_2023 = ((rev_2023 - rev_2022) / rev_2022 * 100).round(1)
        print(f"   • 2023 so với 2022: {change_2023:+.1f}%")

    def visualize_line_chart(self, save_path='visualizations/revenue_trend_line.png'):
        """Vẽ biểu đồ đường xu hướng doanh thu"""
        plt.figure(figsize=(14, 8))

        # Tạo subplot 2x2
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # 1. Line chart cơ bản
        ax1.plot(self.df['Year'], self.df['Revenue_Mil'],
                 marker='o', linewidth=3, markersize=10,
                 color='#2196F3', label='Doanh thu')

        # Thêm điểm dữ liệu
        for x, y in zip(self.df['Year'], self.df['Revenue_Mil']):
            ax1.text(x, y + 0.2, f'{y:.1f}',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax1.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax1.set_title('XU HƯỚNG DOANH THU THEO NĂM\n(Line Chart)',
                      fontsize=14, fontweight='bold', pad=20)
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # 2. Area chart
        ax2.fill_between(self.df['Year'], self.df['Revenue_Mil'],
                         alpha=0.4, color='#4CAF50')
        ax2.plot(self.df['Year'], self.df['Revenue_Mil'],
                 marker='s', linewidth=2, color='#2E7D32')

        # Thêm giá trị
        for x, y in zip(self.df['Year'], self.df['Revenue_Mil']):
            ax2.text(x, y + 0.2, f'{y:.1f}',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax2.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax2.set_title('DOANH THU THEO NĂM\n(Area Chart)',
                      fontsize=14, fontweight='bold', pad=20)
        ax2.grid(True, alpha=0.3)

        # 3. Bar chart với line
        bars3 = ax3.bar(self.df['Year'], self.df['Revenue_Mil'],
                        color=plt.cm.viridis(range(len(self.df))),
                        alpha=0.7, label='Doanh thu')

        # Thêm line trend
        ax3.plot(self.df['Year'], self.df['Revenue_Mil'],
                 color='red', marker='o', linewidth=2,
                 label='Xu hướng')

        ax3.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax3.set_title('DOANH THU VÀ XU HƯỚNG\n(Bar + Line Chart)',
                      fontsize=14, fontweight='bold', pad=20)
        ax3.legend()

        # Thêm giá trị trên bar
        for bar, rev_mil in zip(bars3, self.df['Revenue_Mil']):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                     f'{rev_mil:.1f}', ha='center', va='bottom', fontsize=9)

        # 4. Biểu đồ tăng trưởng
        ax4.bar(self.df['Year'][1:], self.df['Change'].dropna(),
                color=['green' if x > 0 else 'red' for x in self.df['Change'].dropna()],
                alpha=0.7)

        ax4.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Tăng trưởng (%)', fontsize=12, fontweight='bold')
        ax4.set_title('TỐC ĐỘ TĂNG TRƯỞNG THEO NĂM',
                      fontsize=14, fontweight='bold', pad=20)
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)

        # Thêm giá trị tăng trưởng
        for i, change in enumerate(self.df['Change'].dropna()):
            ax4.text(i + 1, change + (0.5 if change > 0 else -1.5),
                     f'{change:+.1f}%',
                     ha='center', va='bottom' if change > 0 else 'top',
                     fontsize=10, fontweight='bold')

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path.replace('.png', '_dashboard.png'), dpi=300, bbox_inches='tight')
        print(f"Đã lưu dashboard tại: {save_path.replace('.png', '_dashboard.png')}")
        plt.show()

    def visualize_waterfall_chart(self, save_path='visualizations/revenue_waterfall.png'):
        """Vẽ biểu đồ waterfall tăng trưởng"""
        plt.figure(figsize=(10, 7))

        # Tính cumulative
        self.df['Cumulative'] = self.df['Revenue_Mil'].cumsum()

        fig, ax = plt.subplots(figsize=(12, 8))

        # Vẽ bar cho từng năm
        for i, (year, rev_mil, cum) in enumerate(zip(self.df['Year'],
                                                     self.df['Revenue_Mil'],
                                                     self.df['Cumulative'])):
            if i == 0:
                bottom = 0
            else:
                bottom = self.df['Cumulative'].iloc[i - 1]

            color = '#4CAF50' if i < len(self.df) - 1 else '#2196F3'  # Màu khác cho năm cuối
            bar = ax.bar(year, rev_mil, bottom=bottom, color=color, alpha=0.8)

            # Thêm giá trị
            ax.text(year, bottom + rev_mil / 2, f'{rev_mil:.1f}\ntriệu',
                    ha='center', va='center', fontsize=9, fontweight='bold', color='white')

        # Thêm line cumulative
        ax.plot(self.df['Year'], self.df['Cumulative'],
                marker='o', color='red', linewidth=2, markersize=8,
                label='Tích lũy')

        # Thêm giá trị cumulative
        for x, y in zip(self.df['Year'], self.df['Cumulative']):
            ax.text(x, y + 2, f'{y:.1f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_xlabel('Năm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax.set_title('BIỂU ĐỒ WATERFALL - TÍCH LŨY DOANH THU THEO NĂM',
                     fontsize=14, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Thêm tổng doanh thu
        total_text = f'Tổng doanh thu 4 năm: {self.total_revenue / 1000000:,.1f} triệu VND\n({self.total_revenue:,.0f} VND)'
        ax.text(0.5, -0.1, total_text,
                transform=ax.transAxes, ha='center', fontsize=11,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.9))

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ waterfall tại: {save_path}")
        plt.show()

    def run_analysis(self):
        """Chạy toàn bộ phân tích Bảng 3"""
        print("\n" + "=" * 60)
        print("PHÂN TÍCH BẢNG 3: XU HƯỚNG DOANH THU THEO THỜI GIAN")
        print("=" * 60)

        self.display_table()
        self.visualize_line_chart()
        self.visualize_waterfall_chart()

# Chạy phân tích Bảng
if __name__ == "__main__":
    analyzer3 = RevenueTrendAnalyzer()
    analyzer3.run_analysis()