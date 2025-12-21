"""BẢNG 4: PHÂN TÍCH TOP NHÂN VIÊN XUẤT SẮC"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
class TopStaffAnalyzer:
    def __init__(self):
        # Dữ liệu từ Bảng 4 (mở rộng từ dữ liệu mẫu)
        self.data = {
            'Staff_ID': ['NV1', 'NV5', 'NV50', 'NV12', 'NV8',
                         'NV25', 'NV33', 'NV7', 'NV19', 'NV41',
                         'NV15', 'NV22', 'NV30', 'NV6', 'NV48'],
            'Revenue': [4005910, 1988520, 3439990, 1785640, 2256780,
                        1897540, 1567820, 2345670, 1987650, 1678900,
                        1456700, 1324500, 1543200, 1678900, 1432100],
            'Name': ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D', 'Hoàng Văn E',
                     'Vũ Thị F', 'Đặng Văn G', 'Bùi Thị H', 'Đỗ Văn I', 'Ngô Thị K',
                     'Lý Văn L', 'Trịnh Thị M', 'Lưu Văn N', 'Chu Thị O', 'Mai Văn P'],
            'Department': ['Sales', 'Marketing', 'Sales', 'HR', 'Sales',
                           'Marketing', 'Sales', 'Sales', 'Marketing', 'HR',
                           'Sales', 'Marketing', 'Sales', 'HR', 'Sales']
        }
        self.df = pd.DataFrame(self.data)
        self.total_revenue = self.df['Revenue'].sum()
        self.top_n = 10  # Số nhân viên top để hiển thị

        # Tính tỷ trọng và xếp hạng
        self.df['Percentage'] = (self.df['Revenue'] / self.total_revenue * 100).round(3)
        self.df['Rank'] = self.df['Revenue'].rank(ascending=False).astype(int)
        self.df = self.df.sort_values('Revenue', ascending=False)

        # Chuyển đổi sang triệu đồng
        self.df['Revenue_Mil'] = (self.df['Revenue'] / 1000000).round(3)

        print("=" * 60)
        print("BẢNG 4: TOP NHÂN VIÊN XUẤT SẮC")
        print("=" * 60)

    def display_table(self, show_top=10):
        """Hiển thị bảng dữ liệu"""
        print(f"\nTOP {show_top} NHÂN VIÊN XUẤT SẮC:")
        print("-" * 100)
        print(
            f"{'Hạng':<6} {'Mã NV':<8} {'Tên nhân viên':<20} {'Phòng ban':<12} {'Doanh thu (VND)':<20} {'Doanh thu (Triệu)':<15} {'Tỷ trọng %':<12}")
        print("-" * 100)

        df_top = self.df.head(show_top)
        for _, row in df_top.iterrows():
            print(f"{row['Rank']:<6} {row['Staff_ID']:<8} {row['Name']:<20} {row['Department']:<12} "
                  f"{row['Revenue']:<20,} {row['Revenue_Mil']:<15,.3f} {row['Percentage']:<12}")

        print("-" * 100)

        # Tính tổng doanh thu top N
        top_revenue = df_top['Revenue'].sum()
        top_percentage = (top_revenue / self.total_revenue * 100).round(2)
        total_mil = self.total_revenue / 1000000

        print(
            f"{'TOTAL (Top ' + str(show_top) + ')':<46} {top_revenue:<20,} {top_revenue / 1000000:<15,.3f} {top_percentage:<12}")
        print(f"{'GRAND TOTAL (Tất cả NV)':<46} {self.total_revenue:<20,} {total_mil:<15,.3f} {'100.00':<12}")
        print("-" * 100)

        # Phân tích top nhân viên
        print(f"\n PHÂN TÍCH TOP {show_top} NHÂN VIÊN:")
        print(f"   • Top {show_top} chiếm {top_percentage}% tổng doanh thu")
        print(f"   • Doanh thu trung bình top {show_top}: {df_top['Revenue_Mil'].mean():.3f} triệu/nhân viên")
        print(
            f"   • Chênh lệch cao nhất - thấp nhất: {df_top['Revenue_Mil'].max() - df_top['Revenue_Mil'].min():.3f} triệu")

        # Phân tích theo phòng ban
        dept_analysis = df_top.groupby('Department')['Revenue'].sum().sort_values(ascending=False)
        print(f"\n PHÂN TÍCH THEO PHÒNG BAN (Top {show_top}):")
        for dept, rev in dept_analysis.items():
            dept_pct = (rev / top_revenue * 100).round(1)
            print(f"   • {dept}: {rev / 1000000:.3f} triệu ({dept_pct}%)")

    def visualize_horizontal_bar(self, show_top=10, save_path='visualizations/top_staff_horizontal.png'):
        """Vẽ biểu đồ ngang top nhân viên"""
        df_top = self.df.head(show_top).sort_values('Revenue', ascending=True)

        plt.figure(figsize=(14, 10))

        # Tạo subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

        # 1. Horizontal bar chart với thông tin đầy đủ
        bars1 = ax1.barh(range(len(df_top)), df_top['Revenue_Mil'],
                         color=plt.cm.viridis(np.linspace(0, 1, len(df_top))))

        ax1.set_yticks(range(len(df_top)))
        ax1.set_yticklabels([f"{row['Name']}\n({row['Staff_ID']} - {row['Department']})"
                             for _, row in df_top.iterrows()], fontsize=10)
        ax1.set_xlabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax1.set_title(f'TOP {show_top} NHÂN VIÊN XUẤT SẮC\n(Horizontal Bar Chart)',
                      fontsize=14, fontweight='bold', pad=20)
        ax1.invert_yaxis()

        # Thêm giá trị trên mỗi bar
        for i, (bar, rev_mil, pct) in enumerate(zip(bars1, df_top['Revenue_Mil'], df_top['Percentage'])):
            width = bar.get_width()
            ax1.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                     f'{rev_mil:.3f} triệu\n({pct:.3f}%)',
                     va='center', fontsize=9, fontweight='bold')

        # 2. Bar chart theo phòng ban (Stacked)
        ax2 = self._create_department_chart(ax2, df_top)

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Đã lưu biểu đồ ngang tại: {save_path}")
        plt.show()

    def _create_department_chart(self, ax, df_top):
        """Tạo biểu đồ theo phòng ban"""
        # Phân tích theo phòng ban
        dept_data = df_top.groupby('Department').agg({
            'Revenue_Mil': 'sum',
            'Staff_ID': 'count'
        }).reset_index()
        dept_data = dept_data.sort_values('Revenue_Mil', ascending=True)

        # Bar chart tổng doanh thu theo phòng
        bars = ax.barh(range(len(dept_data)), dept_data['Revenue_Mil'],
                       color=plt.cm.Set2(range(len(dept_data))))

        ax.set_yticks(range(len(dept_data)))
        ax.set_yticklabels([f"{row['Department']}\n({row['Staff_ID']} nhân viên)"
                            for _, row in dept_data.iterrows()], fontsize=10)
        ax.set_xlabel('Tổng doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax.set_title('DOANH THU THEO PHÒNG BAN\n(Top nhân viên)',
                     fontsize=14, fontweight='bold', pad=20)
        ax.invert_yaxis()

        # Thêm giá trị
        for i, (bar, rev_mil) in enumerate(zip(bars, dept_data['Revenue_Mil'])):
            width = bar.get_width()
            dept_pct = (rev_mil / dept_data['Revenue_Mil'].sum() * 100).round(1)
            ax.text(width + 0.05, bar.get_y() + bar.get_height() / 2,
                    f'{rev_mil:.3f} triệu\n({dept_pct}%)',
                    va='center', fontsize=9, fontweight='bold')

        return ax

    def visualize_lollipop_chart(self, show_top=10, save_path='visualizations/top_staff_lollipop.png'):
        """Vẽ biểu đồ lollipop cho top nhân viên"""
        df_top = self.df.head(show_top).sort_values('Revenue', ascending=True)

        plt.figure(figsize=(12, 8))

        # Tạo lollipop chart
        fig, ax = plt.subplots(figsize=(14, 8))

        # Vẽ đường thẳng (stem)
        for i, rev_mil in enumerate(df_top['Revenue_Mil']):
            ax.plot([0, rev_mil], [i, i], color='gray', alpha=0.5, linewidth=1)

        # Vẽ điểm tròn (circle)
        scatter = ax.scatter(df_top['Revenue_Mil'], range(len(df_top)),
                             s=300, c=df_top['Revenue_Mil'],
                             cmap='viridis', alpha=0.7, edgecolors='black')

        ax.set_yticks(range(len(df_top)))
        ax.set_yticklabels([f"{row['Name']} ({row['Staff_ID']})"
                            for _, row in df_top.iterrows()], fontsize=10)
        ax.set_xlabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax.set_title(f'TOP {show_top} NHÂN VIÊN - LOLLIPOP CHART',
                     fontsize=14, fontweight='bold', pad=20)
        ax.invert_yaxis()

        # Thêm giá trị
        for i, (rev_mil, pct, rank) in enumerate(zip(df_top['Revenue_Mil'],
                                                     df_top['Percentage'],
                                                     df_top['Rank'])):
            ax.text(rev_mil + 0.1, i,
                    f'Hạng {rank}: {rev_mil:.3f} triệu\n({pct:.3f}%)',
                    va='center', fontsize=9, fontweight='bold')

        # Thêm colorbar
        plt.colorbar(scatter, ax=ax, label='Doanh thu (Triệu VND)')

        # Thêm thông tin tổng
        total_top_rev = df_top['Revenue_Mil'].sum()
        total_top_pct = (df_top['Revenue'].sum() / self.total_revenue * 100).round(2)

        info_text = (f"Top {show_top} nhân viên\n"
                     f"Doanh thu: {total_top_rev:.3f} triệu VND\n"
                     f"Chiếm: {total_top_pct}% tổng doanh thu")

        ax.text(0.95, 0.02, info_text,
                transform=ax.transAxes,
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8),
                verticalalignment='bottom', horizontalalignment='right')

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ lollipop tại: {save_path}")
        plt.show()

    def visualize_radar_chart(self, show_top=5, save_path='visualizations/top_staff_radar.png'):
        """Vẽ biểu đồ radar cho top 5 nhân viên"""
        df_top = self.df.head(show_top)

        # Chuẩn hóa dữ liệu cho radar chart (0-100)
        max_revenue = df_top['Revenue_Mil'].max()
        df_top['Normalized'] = (df_top['Revenue_Mil'] / max_revenue * 100).round(1)

        # Số lượng metrics (chỉ doanh thu)
        categories = ['Doanh thu']
        N = len(categories)

        # Góc cho radar chart
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Đóng vòng tròn

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

        # Vẽ cho từng nhân viên
        colors = plt.cm.tab10(range(show_top))
        for i, (_, row) in enumerate(df_top.iterrows()):
            values = [row['Normalized']]
            values += values[:1]  # Đóng vòng tròn

            ax.plot(angles, values, linewidth=2, linestyle='solid',
                    label=f"{row['Name']} ({row['Revenue_Mil']:.3f}M)", color=colors[i])
            ax.fill(angles, values, alpha=0.1, color=colors[i])

        # Thiết lập các label
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
        ax.set_ylim(0, 110)

        # Thêm các vòng tròn đồng tâm
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=9)

        ax.set_title(f'TOP {show_top} NHÂN VIÊN - RADAR CHART\n(So sánh tương đối)',
                     fontsize=14, fontweight='bold', pad=30)

        # Thêm legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=9)

        # Thêm thông tin
        info_text = f"Chuẩn hóa theo NV xuất sắc nhất:\n{df_top.iloc[0]['Name']}\n({df_top.iloc[0]['Revenue_Mil']:.3f} triệu VND = 100%)"
        ax.text(0.5, -0.1, info_text, transform=ax.transAxes,
                ha='center', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Đã lưu biểu đồ radar tại: {save_path}")
        plt.show()

    def run_analysis(self, show_top=10):
        """Chạy toàn bộ phân tích Bảng 4"""
        print("\n" + "=" * 60)
        print(f"PHÂN TÍCH BẢNG 4: TOP {show_top} NHÂN VIÊN XUẤT SẮC")
        print("=" * 60)

        self.display_table(show_top)
        self.visualize_horizontal_bar(show_top)
        self.visualize_lollipop_chart(show_top)
        if show_top >= 5:
            self.visualize_radar_chart(show_top=5)


# Chạy phân tích Bảng 4
if __name__ == "__main__":
    analyzer4 = TopStaffAnalyzer()
    analyzer4.run_analysis(show_top=10)