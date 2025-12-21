"""BẢNG 1: PHÂN TÍCH TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
class ProductQuantityAnalyzer:
    def __init__(self):
        self.data = {
            'Product': ['Mocha', 'Latte', 'Iced Black Coffee', 'Green Tea Freeze',
                        'Chocolate Freeze', 'Cookies & Cream', 'Classic Phin Freeze',
                        'Caramel Phin Freeze', 'Cappuccino', 'Americano'],
            'Quantity': [213, 249, 236, 263, 262, 242, 200, 216, 296, 223]
        }
        self.df = pd.DataFrame(self.data)
        self.total_quantity = self.df['Quantity'].sum()

        # Tính tỷ trọng
        self.df['Percentage'] = (self.df['Quantity'] / self.total_quantity * 100).round(2)
        self.df['Cumulative_Percentage'] = self.df['Percentage'].cumsum()

        print("=" * 60)
        print("BẢNG 1: TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM")
        print("=" * 60)

    def display_table(self):
        """Hiển thị bảng dữ liệu"""
        df_display = self.df.copy()
        df_display.loc['Total'] = ['Grand Total', self.total_quantity, 100.00, 100.00]

        print("\nBẢNG SỐ LƯỢNG SẢN PHẨM:")
        print("-" * 60)
        print(f"{'Sản phẩm':<25} {'Số lượng':<12} {'Tỷ trọng %':<12} {'Tích lũy %':<12}")
        print("-" * 60)

        for _, row in self.df.iterrows():
            print(
                f"{row['Product']:<25} {row['Quantity']:<12} {row['Percentage']:<12} {row['Cumulative_Percentage']:<12}")

        print("-" * 60)
        print(f"{'GRAND TOTAL':<25} {self.total_quantity:<12} {'100.00':<12} {'100.00':<12}")
        print("-" * 60)

        # Phân tích Pareto
        pareto_products = self.df[self.df['Cumulative_Percentage'] <= 80]
        print(f"\n PHÂN TÍCH PARETO (80/20):")
        print(
            f"   • {len(pareto_products)} sản phẩm đầu chiếm {pareto_products['Percentage'].sum():.1f}% tổng số lượng")
        print(f"   • Sản phẩm quan trọng: {', '.join(pareto_products['Product'].tolist())}")

    def visualize_bar_chart(self, save_path='visualizations/product_quantity_bar.png'):
        """Vẽ biểu đồ cột số lượng sản phẩm"""
        plt.figure(figsize=(14, 8))

        # Sắp xếp dữ liệu
        df_sorted = self.df.sort_values('Quantity', ascending=True)

        # Bar chart
        bars = plt.barh(df_sorted['Product'], df_sorted['Quantity'],
                        color=plt.cm.Set3(range(len(df_sorted))))

        plt.xlabel('Số lượng', fontsize=12, fontweight='bold')
        plt.title('TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM', fontsize=16, fontweight='bold', pad=20)

        # Thêm giá trị trên mỗi bar
        for bar, qty, pct in zip(bars, df_sorted['Quantity'], df_sorted['Percentage']):
            width = bar.get_width()
            plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
                     f'{qty} ({pct}%)',
                     va='center', fontsize=10, fontweight='bold')

        # Thêm tổng số lượng
        plt.text(0.95, 0.02, f'Tổng số lượng: {self.total_quantity}',
                 transform=plt.gca().transAxes,
                 fontsize=12, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f" Đã lưu biểu đồ tại: {save_path}")
        plt.show()

    def visualize_pie_chart(self, save_path='visualizations/product_quantity_pie.png'):
        """Vẽ biểu đồ tròn tỷ trọng"""
        plt.figure(figsize=(12, 10))

        # Tạo subplot 2x2
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # 1. Pie chart đơn giản
        ax1 = axes[0, 0]
        wedges1, texts1, autotexts1 = ax1.pie(
            self.df['Quantity'],
            labels=self.df['Product'],
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3(range(len(self.df))),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        ax1.set_title('BIỂU ĐỒ TRÒN TỶ TRỌNG SẢN PHẨM', fontsize=14, fontweight='bold')

        # 2. Pie chart với explode (3 sản phẩm top)
        ax2 = axes[0, 1]
        explode = [0.1 if i < 3 else 0 for i in range(len(self.df))]
        wedges2, texts2, autotexts2 = ax2.pie(
            self.df['Quantity'],
            labels=self.df['Product'],
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            shadow=True,
            colors=plt.cm.Set2(range(len(self.df)))
        )
        ax2.set_title('BIỂU ĐỒ TRÒN VỚI TOP 3 NỔI BẬT', fontsize=14, fontweight='bold')

        # 3. Bar chart tỷ trọng
        ax3 = axes[1, 0]
        df_sorted = self.df.sort_values('Percentage', ascending=False)
        bars3 = ax3.bar(df_sorted['Product'], df_sorted['Percentage'],
                        color=plt.cm.tab20c(range(len(df_sorted))))
        ax3.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Tỷ trọng (%)', fontsize=12, fontweight='bold')
        ax3.set_title('TỶ TRỌNG PHẦN TRĂM THEO SẢN PHẨM', fontsize=14, fontweight='bold')
        ax3.set_xticklabels(df_sorted['Product'], rotation=45, ha='right')

        # Thêm giá trị trên bar
        for bar, pct in zip(bars3, df_sorted['Percentage']):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                     f'{pct}%', ha='center', va='bottom', fontsize=9)

        # 4. Pareto chart
        ax4 = axes[1, 1]

        # Bar chart số lượng
        bars4 = ax4.bar(range(len(df_sorted)), df_sorted['Quantity'],
                        alpha=0.6, label='Số lượng')
        ax4.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Số lượng', fontsize=12, fontweight='bold', color='blue')
        ax4.set_xticks(range(len(df_sorted)))
        ax4.set_xticklabels(df_sorted['Product'], rotation=45, ha='right')
        ax4.tick_params(axis='y', labelcolor='blue')

        # Line chart tỷ trọng tích lũy
        ax4_twin = ax4.twinx()
        ax4_twin.plot(range(len(df_sorted)), df_sorted['Cumulative_Percentage'],
                      color='red', marker='o', linewidth=2, label='Tích lũy %')
        ax4_twin.set_ylabel('Tích lũy %', fontsize=12, fontweight='bold', color='red')
        ax4_twin.set_ylim(0, 110)
        ax4_twin.tick_params(axis='y', labelcolor='red')

        # Đường 80%
        ax4_twin.axhline(y=80, color='green', linestyle='--', alpha=0.7)
        ax4_twin.text(len(df_sorted) - 0.5, 82, '80%', color='green', fontweight='bold')

        ax4.set_title('BIỂU ĐỒ PARETO SỐ LƯỢNG', fontsize=14, fontweight='bold')

        # Kết hợp legend
        lines1, labels1 = ax4.get_legend_handles_labels()
        lines2, labels2 = ax4_twin.get_legend_handles_labels()
        ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        plt.tight_layout()

        # Lưu biểu đồ
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path.replace('.png', '_dashboard.png'), dpi=300, bbox_inches='tight')
        print(f" Đã lưu dashboard tại: {save_path.replace('.png', '_dashboard.png')}")
        plt.show()

    def run_analysis(self):
        """Chạy toàn bộ phân tích Bảng 1"""
        print("\n" + "=" * 60)
        print("PHÂN TÍCH BẢNG 1: TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM")
        print("=" * 60)

        self.display_table()
        self.visualize_bar_chart()
        self.visualize_pie_chart()


# Chạy phân tích Bảng 1
if __name__ == "__main__":
    analyzer1 = ProductQuantityAnalyzer()
    analyzer1.run_analysis()