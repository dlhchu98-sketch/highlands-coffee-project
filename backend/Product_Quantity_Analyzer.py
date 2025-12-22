"""BẢNG 1: PHÂN TÍCH TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


class ProductQuantityAnalyzer:
    def __init__(self, data_path='output/cleaned_data.csv'):
        self.data_path = data_path
        self.df = None
        self.df_product = None
        self.total_quantity = 0

        print("=" * 60)
        print("BẢNG 1: TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM")
        print(f"Đọc từ file: {data_path}")
        print("=" * 60)

        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            print(f"Đã tải {len(self.df)} dòng dữ liệu")
            self._prepare_product_data()

        except Exception as e:
            print(f"Lỗi đọc file: {e}")
            print("Sử dụng dữ liệu mẫu thay thế")
            self._use_sample_data()

    def _prepare_product_data(self):
        print("\nĐang tìm kiếm cột sản phẩm và số lượng...")

        # Tìm cột sản phẩm
        product_keywords = ['product', 'san_pham', 'product_name', 'item']
        product_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in product_keywords):
                product_col = col
                print(f"Tìm thấy cột sản phẩm: {product_col}")
                break

        # Tìm cột số lượng
        qty_keywords = ['quantity', 'qty', 'so_luong', 'số lượng', 'amount', 'sl']
        qty_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in qty_keywords):
                qty_col = col
                print(f"Tìm thấy cột số lượng: {qty_col}")
                break

        if not product_col or not qty_col:
            print("Không tìm thấy cột sản phẩm hoặc số lượng")
            self._use_sample_data()
            return

        # Tổng hợp số lượng theo sản phẩm
        print(f"\nTổng hợp số lượng theo {product_col}...")
        product_qty = self.df.groupby(product_col)[qty_col].sum().reset_index()
        product_qty = product_qty.sort_values(qty_col, ascending=False)

        # Lấy top 15 sản phẩm
        if len(product_qty) > 15:
            print(f"Có {len(product_qty)} sản phẩm, chỉ hiển thị top 15")
            top_products = product_qty.head(15)
            other_qty = product_qty.iloc[15:][qty_col].sum()

            other_row = pd.DataFrame({
                product_col: ['Khác'],
                qty_col: [other_qty]
            })
            self.df_product = pd.concat([top_products, other_row], ignore_index=True)
        else:
            self.df_product = product_qty

        self.df_product.columns = ['Product', 'Quantity']
        self.total_quantity = self.df_product['Quantity'].sum()

        # Tính tỷ trọng
        self.df_product['Percentage'] = (self.df_product['Quantity'] / self.total_quantity * 100).round(2)
        self.df_product['Cumulative_Percentage'] = self.df_product['Percentage'].cumsum()

        print(f"Đã tổng hợp {len(self.df_product)} sản phẩm")

    def _use_sample_data(self):
        print("Sử dụng dữ liệu mẫu")
        self.df_product = pd.DataFrame({
            'Product': ['Mocha', 'Latte', 'Iced Black Coffee', 'Green Tea Freeze',
                        'Chocolate Freeze', 'Cookies & Cream', 'Classic Phin Freeze',
                        'Caramel Phin Freeze', 'Cappuccino', 'Americano'],
            'Quantity': [213, 249, 236, 263, 262, 242, 200, 216, 296, 223]
        })
        self.total_quantity = self.df_product['Quantity'].sum()
        self.df_product['Percentage'] = (self.df_product['Quantity'] / self.total_quantity * 100).round(2)
        self.df_product['Cumulative_Percentage'] = self.df_product['Percentage'].cumsum()

    def display_table(self):
        if self.df_product is None or self.df_product.empty:
            print("Không có dữ liệu để hiển thị")
            return

        print(f"\nBẢNG SỐ LƯỢNG SẢN PHẨM (Từ file: {os.path.basename(self.data_path)})")
        print("-" * 80)
        print(f"{'Sản phẩm':<25} {'Số lượng':<12} {'Tỷ trọng %':<12} {'Tích lũy %':<12}")
        print("-" * 80)

        for _, row in self.df_product.iterrows():
            print(
                f"{row['Product']:<25} {row['Quantity']:<12} {row['Percentage']:<12} {row['Cumulative_Percentage']:<12}")

        print("-" * 80)
        print(f"{'TOTAL':<25} {self.total_quantity:<12} {'100.00':<12} {'100.00':<12}")
        print("-" * 80)

        # Phân tích Pareto
        pareto_products = self.df_product[self.df_product['Cumulative_Percentage'] <= 80]
        print(f"\nPHÂN TÍCH PARETO (80/20):")
        print(f"   {len(pareto_products)} sản phẩm đầu chiếm {pareto_products['Percentage'].sum():.1f}% tổng số lượng")

        if len(pareto_products) <= 10:
            print(f"   Sản phẩm quan trọng: {', '.join(pareto_products['Product'].tolist())}")

    def visualize_bar_chart(self, save_path='visualizations/product_quantity_bar.png'):
        if self.df_product is None or self.df_product.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        plt.figure(figsize=(14, 8))

        df_sorted = self.df_product.sort_values('Quantity', ascending=True)

        bars = plt.barh(df_sorted['Product'], df_sorted['Quantity'],
                        color=plt.cm.Set3(range(len(df_sorted))))

        plt.xlabel('Số lượng', fontsize=12, fontweight='bold')
        plt.title('TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM', fontsize=16, fontweight='bold', pad=20)

        for bar, qty, pct in zip(bars, df_sorted['Quantity'], df_sorted['Percentage']):
            width = bar.get_width()
            plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
                     f'{qty} ({pct}%)',
                     va='center', fontsize=10, fontweight='bold')

        info_text = f"Tổng số lượng: {self.total_quantity} sản phẩm\nTừ file: {os.path.basename(self.data_path)}"
        plt.text(0.95, 0.02, info_text,
                 transform=plt.gca().transAxes,
                 fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))

        plt.tight_layout()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Đã lưu biểu đồ tại: {save_path}")
        plt.show()

    def visualize_pie_chart(self, save_path='visualizations/product_quantity_pie.png'):
        if self.df_product is None or self.df_product.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # 1. Pie chart
        ax1 = axes[0, 0]
        wedges1, texts1, autotexts1 = ax1.pie(
            self.df_product['Quantity'],
            labels=self.df_product['Product'],
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3(range(len(self.df_product))),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        ax1.set_title('BIỂU ĐỒ TRÒN TỶ TRỌNG SẢN PHẨM', fontsize=14, fontweight='bold')

        # 2. Bar chart tỷ trọng
        ax2 = axes[0, 1]
        df_sorted = self.df_product.sort_values('Percentage', ascending=False)
        bars2 = ax2.bar(df_sorted['Product'], df_sorted['Percentage'],
                        color=plt.cm.tab20c(range(len(df_sorted))))
        ax2.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Tỷ trọng (%)', fontsize=12, fontweight='bold')
        ax2.set_title('TỶ TRỌNG PHẦN TRĂM THEO SẢN PHẨM', fontsize=14, fontweight='bold')
        ax2.set_xticklabels(df_sorted['Product'], rotation=45, ha='right')

        for bar, pct in zip(bars2, df_sorted['Percentage']):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                     f'{pct}%', ha='center', va='bottom', fontsize=9)

        # 3. Pareto chart
        ax3 = axes[1, 0]
        bars3 = ax3.bar(range(len(df_sorted)), df_sorted['Quantity'],
                        alpha=0.6, label='Số lượng')
        ax3.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Số lượng', fontsize=12, fontweight='bold', color='blue')
        ax3.set_xticks(range(len(df_sorted)))
        ax3.set_xticklabels(df_sorted['Product'], rotation=45, ha='right')

        ax3_twin = ax3.twinx()
        ax3_twin.plot(range(len(df_sorted)), df_sorted['Cumulative_Percentage'],
                      color='red', marker='o', linewidth=2, label='Tích lũy %')
        ax3_twin.set_ylabel('Tích lũy %', fontsize=12, fontweight='bold', color='red')
        ax3_twin.set_ylim(0, 110)

        ax3_twin.axhline(y=80, color='green', linestyle='--', alpha=0.7)
        ax3_twin.text(len(df_sorted) - 0.5, 82, '80%', color='green', fontweight='bold')

        ax3.set_title('BIỂU ĐỒ PARETO SỐ LƯỢNG', fontsize=14, fontweight='bold')

        # 4. Area chart
        ax4 = axes[1, 1]
        ax4.fill_between(range(len(df_sorted)), df_sorted['Cumulative_Percentage'], alpha=0.3)
        ax4.plot(range(len(df_sorted)), df_sorted['Cumulative_Percentage'],
                 color='blue', linewidth=2)
        ax4.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Tích lũy %', fontsize=12, fontweight='bold')
        ax4.set_title('ĐƯỜNG TÍCH LŨY TỶ TRỌNG', fontsize=14, fontweight='bold')
        ax4.set_xticks(range(len(df_sorted)))
        ax4.set_xticklabels(df_sorted['Product'], rotation=45, ha='right')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path.replace('.png', '_dashboard.png'), dpi=300, bbox_inches='tight')
        print(f"Đã lưu dashboard tại: {save_path.replace('.png', '_dashboard.png')}")
        plt.show()

    def run_analysis(self):
        print("\n" + "=" * 60)
        print("PHÂN TÍCH BẢNG 1: TỶ TRỌNG SỐ LƯỢNG SẢN PHẨM")
        print("=" * 60)

        self.display_table()
        self.visualize_bar_chart()
        self.visualize_pie_chart()


if __name__ == "__main__":
    analyzer1 = ProductQuantityAnalyzer(data_path='output/cleaned_data.csv')
    analyzer1.run_analysis()