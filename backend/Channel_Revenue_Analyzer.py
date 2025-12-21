"""BẢNG 2: PHÂN TÍCH TỶ TRỌNG DOANH THU THEO KÊNH BÁN HÀNG"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
class ChannelRevenueAnalyzer:
    def __init__(self):
        # Dữ liệu từ Bảng 2
        self.data = {
            'Channel': ['Online', 'Offline'],
            'Revenue': [57218560, 68222000]
        }
        self.df = pd.DataFrame(self.data)
        self.total_revenue = self.df['Revenue'].sum()

        # Tính tỷ trọng
        self.df['Percentage'] = (self.df['Revenue'] / self.total_revenue * 100).round(2)

        # Chuyển đổi sang triệu đồng cho dễ đọc
        self.df['Revenue_Mil'] = (self.df['Revenue'] / 1000000).round(2)

        print("=" * 60)
        print("BẢNG 2: TỶ TRỌNG DOANH THU THEO KÊNH")
        print("=" * 60)

    def display_table(self):
        """Hiển thị bảng dữ liệu"""
        print("\nBẢNG DOANH THU THEO KÊNH:")
        print("-" * 70)
        print(f"{'Kênh bán hàng':<15} {'Doanh thu (VND)':<20} {'Doanh thu (Triệu)':<18} {'Tỷ trọng %':<12}")
        print("-" * 70)

        for _, row in self.df.iterrows():
            print(f"{row['Channel']:<15} {row['Revenue']:<20,} {row['Revenue_Mil']:<18,.2f} {row['Percentage']:<12}")

        print("-" * 70)
        total_mil = self.total_revenue / 1000000
        print(f"{'TOTAL':<15} {self.total_revenue:<20,} {total_mil:<18,.2f} {'100.00':<12}")
        print("-" * 70)

        # So sánh kênh
        online_rev = self.df[self.df['Channel'] == 'Online']['Revenue'].values[0]
        offline_rev = self.df[self.df['Channel'] == 'Offline']['Revenue'].values[0]
        diff = offline_rev - online_rev
        diff_percent = (diff / online_rev * 100)

        print(f"\n SO SÁNH KÊNH BÁN HÀNG:")
        print(f"   • Offline cao hơn Online: {diff:,.0f} VND ({diff_percent:.1f}%)")
        print(f"   • Tỷ lệ Offline/Online: {(offline_rev / online_rev):.2f}:1")

        if offline_rev > online_rev:
            print(f"   → Kênh Offline chiếm ưu thế")
        else:
            print(f"   → Kênh Online chiếm ưu thế")

    def visualize_pie_chart(self, save_path='visualizations/channel_revenue_pie.png'):
        """Vẽ biểu đồ tròn tỷ trọng doanh thu theo kênh"""
        plt.figure(figsize=(10, 8))

        # Tạo 2 subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # 1. Pie chart cơ bản
        wedges1, texts1, autotexts1 = ax1.pie(
            self.df['Revenue'],
            labels=self.df['Channel'],
            autopct=lambda pct: f'{pct:.1f}%\n({pct * self.total_revenue / 100:,.0f} VND)',
            startangle=90,
            colors=['#4CAF50', '#2196F3'],  # Xanh lá cho Online, xanh dương cho Offline
            explode=[0.05, 0],  # Làm nổi Online
            shadow=True,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        ax1.set_title('TỶ TRỌNG DOANH THU THEO KÊNH\n(Pie Chart)',
                      fontsize=14, fontweight='bold', pad=20)

        # Làm đậm text
        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        for text in texts1:
            text.set_fontsize(12)
            text.set_fontweight('bold')

        # 2. Donut chart
        ax2.pie(
            self.df['Revenue'],
            labels=self.df['Channel'],
            autopct='%1.1f%%',
            startangle=90,
            colors=['#66BB6A', '#42A5F5'],
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )

        # Vẽ vòng tròn ở giữa để tạo donut
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax2.add_patch(centre_circle)

        # Thêm tổng doanh thu ở giữa
        ax2.text(0, 0, f'Tổng doanh thu:\n{self.total_revenue / 1000000:,.1f} triệu\n({self.total_revenue:,.0f} VND)',
                 ha='center', va='center', fontsize=11, fontweight='bold')

        ax2.set_title('DOANH THU THEO KÊNH\n(Donut Chart)',
                      fontsize=14, fontweight='bold', pad=20)

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ tại: {save_path}")
        plt.show()

    def visualize_bar_chart(self, save_path='visualizations/channel_revenue_bar.png'):
        """Vẽ biểu đồ cột doanh thu theo kênh"""
        plt.figure(figsize=(12, 7))

        # Tạo subplot 2x1
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # 1. Bar chart đơn giản
        bars1 = ax1.bar(self.df['Channel'], self.df['Revenue_Mil'],
                        color=['#4CAF50', '#2196F5'], alpha=0.8)
        ax1.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax1.set_title('DOANH THU THEO KÊNH BÁN HÀNG',
                      fontsize=14, fontweight='bold', pad=20)

        # Thêm giá trị trên bar
        for bar, rev_mil, pct in zip(bars1, self.df['Revenue_Mil'], self.df['Percentage']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                     f'{rev_mil:,.1f} triệu\n({pct}%)',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        # 2. Bar chart với tỷ trọng
        ax2.bar(self.df['Channel'], self.df['Percentage'],
                color=['#81C784', '#64B5F6'], alpha=0.8)
        ax2.set_ylabel('Tỷ trọng (%)', fontsize=12, fontweight='bold')
        ax2.set_title('TỶ TRỌNG DOANH THU THEO KÊNH',
                      fontsize=14, fontweight='bold', pad=20)
        ax2.set_ylim(0, 60)

        # Thêm giá trị phần trăm
        for i, pct in enumerate(self.df['Percentage']):
            ax2.text(i, pct + 1, f'{pct}%',
                     ha='center', va='bottom', fontsize=11, fontweight='bold')

        # Thêm thông tin tổng
        ax2.text(0.5, -0.15,
                 f'Tổng doanh thu: {self.total_revenue:,.0f} VND = {self.total_revenue / 1000000:,.1f} triệu',
                 transform=ax2.transAxes, ha='center', fontsize=11,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ tại: {save_path}")
        plt.show()

    def run_analysis(self):
        """Chạy toàn bộ phân tích Bảng 2"""
        print("\n" + "=" * 60)
        print("PHÂN TÍCH BẢNG 2: TỶ TRỌNG DOANH THU THEO KÊNH")
        print("=" * 60)

        self.display_table()
        self.visualize_pie_chart()
        self.visualize_bar_chart()


# Chạy phân tích Bảng 2
if __name__ == "__main__":
    analyzer2 = ChannelRevenueAnalyzer()
    analyzer2.run_analysis()