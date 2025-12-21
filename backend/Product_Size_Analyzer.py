"""BẢNG 5: PHÂN TÍCH TỶ TRỌNG KÍCH CỠ SẢN PHẨM"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
class ProductSizeAnalyzer:
    def __init__(self):
        # Dữ liệu từ Bảng 5
        self.data = {
            'Product': ['Americano', 'Cappuccino', 'Mocha', 'Latte', 'Iced Black Coffee',
                        'Green Tea Freeze', 'Chocolate Freeze', 'Cookies & Cream',
                        'Classic Phin Freeze', 'Caramel Phin Freeze'],
            'L': [70, 107, 78, 82, 75, 88, 92, 76, 68, 85],
            'M': [82, 78, 85, 79, 88, 76, 81, 89, 72, 84],
            'S': [71, 96, 50, 88, 73, 99, 89, 77, 60, 47]
        }
        self.df = pd.DataFrame(self.data)

        # Tính tổng cho từng sản phẩm
        self.df['Total'] = self.df[['L', 'M', 'S']].sum(axis=1)

        # Tính tỷ trọng phần trăm
        for size in ['L', 'M', 'S']:
            self.df[f'{size}_%'] = (self.df[size] / self.df['Total'] * 100).round(1)

        # Tính tổng cho từng size
        self.total_L = self.df['L'].sum()
        self.total_M = self.df['M'].sum()
        self.total_S = self.df['S'].sum()
        self.grand_total = self.total_L + self.total_M + self.total_S

        print("=" * 60)
        print("BẢNG 5: TỶ TRỌNG KÍCH CỠ SẢN PHẨM")
        print("=" * 60)

    def display_table(self):
        """Hiển thị bảng dữ liệu"""
        print("\nBẢNG TỶ TRỌNG KÍCH CỠ SẢN PHẨM:")
        print("-" * 100)
        print(f"{'Sản phẩm':<25} {'L':<8} {'M':<8} {'S':<8} {'Tổng':<10} {'L%':<8} {'M%':<8} {'S%':<8}")
        print("-" * 100)

        for _, row in self.df.iterrows():
            print(f"{row['Product']:<25} {row['L']:<8} {row['M']:<8} {row['S']:<8} "
                  f"{row['Total']:<10} {row['L_%']:<8} {row['M_%']:<8} {row['S_%']:<8}")

        print("-" * 100)

        # Tính tỷ trọng tổng
        total_L_pct = (self.total_L / self.grand_total * 100).round(1)
        total_M_pct = (self.total_M / self.grand_total * 100).round(1)
        total_S_pct = (self.total_S / self.grand_total * 100).round(1)

        print(f"{'TOTAL':<25} {self.total_L:<8} {self.total_M:<8} {self.total_S:<8} "
              f"{self.grand_total:<10} {total_L_pct:<8} {total_M_pct:<8} {total_S_pct:<8}")
        print("-" * 100)

        # Phân tích tổng quan
        print(f"\n PHÂN TÍCH TỔNG QUAN KÍCH CỠ:")
        print(f"   • Tổng số lượng: {self.grand_total} sản phẩm")
        print(
            f"   • Size phổ biến nhất: {'L' if self.total_L > self.total_M and self.total_L > self.total_S else 'M' if self.total_M > self.total_S else 'S'}")
        print(f"   • Phân bố: L ({total_L_pct}%), M ({total_M_pct}%), S ({total_S_pct}%)")

        # Tìm sản phẩm có tỷ lệ size đặc biệt
        print(f"\nSẢN PHẨM ĐẶC BIỆT:")

        # Sản phẩm có tỷ lệ L cao nhất
        max_L_product = self.df.loc[self.df['L_%'].idxmax()]
        print(f"   • Tỷ lệ L cao nhất: {max_L_product['Product']} ({max_L_product['L_%']}%)")

        # Sản phẩm có tỷ lệ S cao nhất
        max_S_product = self.df.loc[self.df['S_%'].idxmax()]
        print(f"   • Tỷ lệ S cao nhất: {max_S_product['Product']} ({max_S_product['S_%']}%)")

        # Sản phẩm có phân bố cân bằng nhất
        self.df['Balance_Score'] = self.df[['L_%', 'M_%', 'S_%']].std(axis=1)
        most_balanced = self.df.loc[self.df['Balance_Score'].idxmin()]
        print(f"   • Phân bố cân bằng nhất: {most_balanced['Product']} "
              f"(L:{most_balanced['L_%']}%, M:{most_balanced['M_%']}%, S:{most_balanced['S_%']}%)")

    def visualize_stacked_bar(self, save_path='visualizations/product_size_stacked.png'):
        """Vẽ biểu đồ stacked bar tỷ trọng kích cỡ"""
        # Sắp xếp dữ liệu theo tổng số lượng
        df_sorted = self.df.sort_values('Total', ascending=True)

        plt.figure(figsize=(14, 8))

        # Tạo subplot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

        # 1. Stacked bar chart số lượng tuyệt đối
        bottom = np.zeros(len(df_sorted))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # L, M, S

        for i, size in enumerate(['L', 'M', 'S']):
            bars = ax1.bar(range(len(df_sorted)), df_sorted[size],
                           bottom=bottom, color=colors[i],
                           label=f'Size {size}', alpha=0.8)
            bottom += df_sorted[size].values

        ax1.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Số lượng', fontsize=12, fontweight='bold')
        ax1.set_title('PHÂN BỐ KÍCH CỠ THEO SẢN PHẨM\n(Stacked Bar Chart - Số lượng)',
                      fontsize=14, fontweight='bold', pad=20)
        ax1.set_xticks(range(len(df_sorted)))
        ax1.set_xticklabels(df_sorted['Product'], rotation=45, ha='right', fontsize=10)
        ax1.legend(title='Kích cỡ')

        # Thêm tổng số lượng trên mỗi stack
        for i, total in enumerate(df_sorted['Total']):
            ax1.text(i, total + 2, f'{total}',
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

        # 2. Stacked bar chart phần trăm
        ax2 = self._create_percentage_chart(ax2, df_sorted, colors)

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ stacked tại: {save_path}")
        plt.show()

    def _create_percentage_chart(self, ax, df_sorted, colors):
        """Tạo biểu đồ phần trăm"""
        # Tính phần trăm tích lũy
        bottom = np.zeros(len(df_sorted))

        for i, size in enumerate(['L', 'M', 'S']):
            percentages = df_sorted[f'{size}_%'].values
            bars = ax.bar(range(len(df_sorted)), percentages,
                          bottom=bottom, color=colors[i],
                          label=f'Size {size}', alpha=0.8)
            bottom += percentages

        ax.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tỷ trọng (%)', fontsize=12, fontweight='bold')
        ax.set_title('TỶ TRỌNG KÍCH CỠ THEO SẢN PHẨM\n(Stacked Bar Chart - Phần trăm)',
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(range(len(df_sorted)))
        ax.set_xticklabels(df_sorted['Product'], rotation=45, ha='right', fontsize=10)
        ax.set_ylim(0, 100)
        ax.legend(title='Kích cỡ')

        # Thêm tỷ lệ % cho từng segment
        for i in range(len(df_sorted)):
            cumulative = 0
            for size in ['L', 'M', 'S']:
                pct = df_sorted.iloc[i][f'{size}_%']
                if pct > 5:  # Chỉ hiển thị nếu > 5%
                    ax.text(i, cumulative + pct / 2, f'{pct}%',
                            ha='center', va='center', fontsize=8, fontweight='bold',
                            color='white' if pct > 15 else 'black')
                cumulative += pct

        return ax

    def visualize_grouped_bar(self, save_path='visualizations/product_size_grouped.png'):
        """Vẽ biểu đồ grouped bar"""
        df_sorted = self.df.sort_values('Total', ascending=False)

        plt.figure(figsize=(16, 10))

        # Tạo subplot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))

        # 1. Grouped bar chart số lượng
        x = np.arange(len(df_sorted))
        width = 0.25

        bars_L = ax1.bar(x - width, df_sorted['L'], width, label='Size L', color='#FF6B6B', alpha=0.8)
        bars_M = ax1.bar(x, df_sorted['M'], width, label='Size M', color='#4ECDC4', alpha=0.8)
        bars_S = ax1.bar(x + width, df_sorted['S'], width, label='Size S', color='#45B7D1', alpha=0.8)

        ax1.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Số lượng', fontsize=12, fontweight='bold')
        ax1.set_title('SO SÁNH KÍCH CỠ THEO SẢN PHẨM\n(Grouped Bar Chart)',
                      fontsize=14, fontweight='bold', pad=20)
        ax1.set_xticks(x)
        ax1.set_xticklabels(df_sorted['Product'], rotation=45, ha='right', fontsize=10)
        ax1.legend()

        # Thêm giá trị trên bar
        for bars in [bars_L, bars_M, bars_S]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height + 1,
                         f'{int(height)}', ha='center', va='bottom', fontsize=8)

        # 2. Heatmap phần trăm
        ax2 = self._create_heatmap_chart(ax2, df_sorted)

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ grouped tại: {save_path}")
        plt.show()

    def _create_heatmap_chart(self, ax, df_sorted):
        """Tạo biểu đồ heatmap"""
        # Chuẩn bị dữ liệu cho heatmap
        heatmap_data = df_sorted[['L_%', 'M_%', 'S_%']].values
        products = df_sorted['Product'].values
        sizes = ['L', 'M', 'S']

        # Tạo heatmap
        im = ax.imshow(heatmap_data.T, cmap='YlOrRd', aspect='auto')

        # Thiết lập ticks và labels
        ax.set_xticks(range(len(products)))
        ax.set_xticklabels(products, rotation=45, ha='right', fontsize=10)
        ax.set_yticks(range(len(sizes)))
        ax.set_yticklabels(sizes, fontsize=12, fontweight='bold')

        # Thêm giá trị vào ô
        for i in range(len(products)):
            for j in range(len(sizes)):
                value = heatmap_data[i, j]
                color = 'white' if value > 50 else 'black'
                ax.text(i, j, f'{value}%',
                        ha='center', va='center',
                        color=color, fontsize=9, fontweight='bold')

        ax.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax.set_title('HEATMAP TỶ TRỌNG KÍCH CỠ (%)\n(Màu càng đậm = tỷ trọng càng cao)',
                     fontsize=14, fontweight='bold', pad=20)

        # Thêm colorbar
        plt.colorbar(im, ax=ax, label='Tỷ trọng (%)')

        return ax

    def visualize_pie_donut_combo(self, save_path='visualizations/product_size_pie_donut.png'):
        """Vẽ biểu đồ pie và donut kết hợp"""
        # Tổng hợp dữ liệu theo size
        size_totals = {
            'L': self.total_L,
            'M': self.total_M,
            'S': self.total_S
        }

        # Tính phần trăm
        total = sum(size_totals.values())
        size_percentages = {k: (v / total * 100).round(1) for k, v in size_totals.items()}

        plt.figure(figsize=(15, 12))

        # Tạo subplot 2x2
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 14))

        # 1. Pie chart tổng thể
        wedges1, texts1, autotexts1 = ax1.pie(
            size_totals.values(),
            labels=size_totals.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
            explode=[0.05, 0, 0],
            shadow=True
        )

        for autotext in autotexts1:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax1.set_title('PHÂN BỐ KÍCH CỠ TỔNG THỂ', fontsize=14, fontweight='bold', pad=20)

        # 2. Donut chart tổng thể
        wedges2, texts2, autotexts2 = ax2.pie(
            size_totals.values(),
            labels=size_totals.keys(),
            autopct=lambda pct: f'{pct:.1f}%\n({pct * total / 100:.0f} sp)',
            startangle=90,
            colors=['#FF8A8A', '#7FE0D6', '#6BCAE2']
        )

        # Tạo donut
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax2.add_patch(centre_circle)

        # Thêm thông tin ở giữa
        ax2.text(0, 0, f'Tổng:\n{total} sản phẩm',
                 ha='center', va='center', fontsize=12, fontweight='bold')

        ax2.set_title('DONUT CHART KÍCH CỠ', fontsize=14, fontweight='bold', pad=20)

        # 3. Waffle chart cho 3 sản phẩm đầu
        ax3 = self._create_waffle_chart(ax3)

        # 4. 100% stacked bar
        ax4 = self._create_100pct_stacked_bar(ax4)

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ pie-donut tại: {save_path}")
        plt.show()

    def _create_waffle_chart(self, ax):
        """Tạo waffle chart cho 3 sản phẩm đầu"""
        # Lấy 3 sản phẩm đầu
        top_products = self.df.head(3)

        # Tạo waffle chart đơn giản
        ax.axis('off')
        ax.set_title('WAFFLE CHART - TOP 3 SẢN PHẨM\n(Mỗi ô = 5 sản phẩm)',
                     fontsize=12, fontweight='bold', pad=20)

        # Thông tin text
        info_text = ""
        for _, row in top_products.iterrows():
            info_text += (f"{row['Product']}:\n"
                          f"  L: {row['L']} ({row['L_%']}%)\n"
                          f"  M: {row['M']} ({row['M_%']}%)\n"
                          f"  S: {row['S']} ({row['S_%']}%)\n"
                          f"  Tổng: {row['Total']}\n\n")

        ax.text(0.5, 0.5, info_text,
                transform=ax.transAxes,
                ha='center', va='center',
                fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))

        return ax

    def _create_100pct_stacked_bar(self, ax):
        """Tạo 100% stacked bar"""
        # Lấy dữ liệu cho 5 sản phẩm đầu
        top_products = self.df.head(5)

        bottom = np.zeros(len(top_products))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

        for i, size in enumerate(['L', 'M', 'S']):
            percentages = top_products[f'{size}_%'].values
            ax.bar(range(len(top_products)), percentages,
                   bottom=bottom, color=colors[i], label=f'Size {size}')
            bottom += percentages

        ax.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tỷ trọng (%)', fontsize=12, fontweight='bold')
        ax.set_title('100% STACKED BAR - TOP 5 SẢN PHẨM',
                     fontsize=12, fontweight='bold', pad=20)
        ax.set_xticks(range(len(top_products)))
        ax.set_xticklabels(top_products['Product'], rotation=45, ha='right', fontsize=10)
        ax.set_ylim(0, 100)
        ax.legend()

        return ax

    def run_analysis(self):
        """Chạy toàn bộ phân tích Bảng 5"""
        print("\n" + "=" * 60)
        print("PHÂN TÍCH BẢNG 5: TỶ TRỌNG KÍCH CỠ SẢN PHẨM")
        print("=" * 60)

        self.display_table()
        self.visualize_stacked_bar()
        self.visualize_grouped_bar()
        self.visualize_pie_donut_combo()


# Chạy phân tích Bảng 5
if __name__ == "__main__":
    analyzer5 = ProductSizeAnalyzer()
    analyzer5.run_analysis()