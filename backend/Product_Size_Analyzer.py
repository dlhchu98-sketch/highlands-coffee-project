"""BẢNG 5: PHÂN TÍCH TỶ TRỌNG KÍCH CỠ SẢN PHẨM"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


class ProductSizeAnalyzer:
    def __init__(self, data_path='output/cleaned_data.csv'):
        self.data_path = data_path
        self.df = None
        self.df_size = None

        print("=" * 60)
        print("BẢNG 5: TỶ TRỌNG KÍCH CỠ SẢN PHẨM")
        print(f"Đọc từ file: {data_path}")
        print("=" * 60)

        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            print(f"Đã tải {len(self.df)} dòng dữ liệu")
            self._prepare_size_data()

        except Exception as e:
            print(f"Lỗi đọc file: {e}")
            print("Sử dụng dữ liệu mẫu thay thế")
            self._use_sample_data()

    def _prepare_size_data(self):
        print("\nĐang tìm kiếm cột sản phẩm và kích cỡ...")

        product_keywords = ['product', 'san_pham', 'product_name', 'item']
        product_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in product_keywords):
                product_col = col
                print(f"Tìm thấy cột sản phẩm: {product_col}")
                break

        size_keywords = ['size', 'kich_co', 'kích_cỡ', 'loại']
        size_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in size_keywords):
                size_col = col
                print(f"Tìm thấy cột kích cỡ: {size_col}")
                break

        qty_keywords = ['quantity', 'qty', 'so_luong', 'số lượng', 'amount']
        qty_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in qty_keywords):
                qty_col = col
                print(f"Tìm thấy cột số lượng: {qty_col}")
                break

        if not product_col or not size_col or not qty_col:
            print("Không tìm thấy đủ cột cần thiết")
            self._use_sample_data()
            return

        print(f"\nTổng hợp số lượng theo {product_col} và {size_col}...")

        # Tổng hợp số lượng theo sản phẩm và kích cỡ
        size_data = self.df.groupby([product_col, size_col])[qty_col].sum().reset_index()

        # Pivot table: sản phẩm × kích cỡ
        pivot_table = size_data.pivot_table(index=product_col, columns=size_col,
                                            values=qty_col, aggfunc='sum', fill_value=0)

        # Reset index và chuẩn hóa tên cột
        self.df_size = pivot_table.reset_index()
        self.df_size.columns.name = None

        # Chuẩn hóa tên cột kích cỡ
        size_columns = [col for col in self.df_size.columns if col != product_col]

        # Tạo cột tổng
        self.df_size['Total'] = self.df_size[size_columns].sum(axis=1)

        # Tính tỷ trọng phần trăm
        for size_col in size_columns:
            if size_col != 'Total':
                self.df_size[f'{size_col}_%'] = (self.df_size[size_col] / self.df_size['Total'] * 100).round(1)

        # Sắp xếp theo tổng số lượng
        self.df_size = self.df_size.sort_values('Total', ascending=False)

        # Giới hạn số lượng sản phẩm hiển thị
        if len(self.df_size) > 10:
            print(f"Có {len(self.df_size)} sản phẩm, chỉ hiển thị top 10")
            self.df_size = self.df_size.head(10)

        print(f"Đã tổng hợp dữ liệu kích cỡ cho {len(self.df_size)} sản phẩm")

    def _use_sample_data(self):
        print("Sử dụng dữ liệu mẫu")
        self.df_size = pd.DataFrame({
            'Product': ['Americano', 'Cappuccino', 'Mocha', 'Latte', 'Iced Black Coffee',
                        'Green Tea Freeze', 'Chocolate Freeze', 'Cookies & Cream',
                        'Classic Phin Freeze', 'Caramel Phin Freeze'],
            'L': [70, 107, 78, 82, 75, 88, 92, 76, 68, 85],
            'M': [82, 78, 85, 79, 88, 76, 81, 89, 72, 84],
            'S': [71, 96, 50, 88, 73, 99, 89, 77, 60, 47]
        })

        self.df_size['Total'] = self.df_size[['L', 'M', 'S']].sum(axis=1)

        for size in ['L', 'M', 'S']:
            self.df_size[f'{size}_%'] = (self.df_size[size] / self.df_size['Total'] * 100).round(1)

    def display_table(self):
        if self.df_size is None or self.df_size.empty:
            print("Không có dữ liệu để hiển thị")
            return

        print(f"\nBẢNG TỶ TRỌNG KÍCH CỠ SẢN PHẨM (Từ file: {os.path.basename(self.data_path)})")
        print("-" * 100)

        # Lấy các cột kích cỡ (loại bỏ cột Product, Total và các cột %)
        size_cols = [col for col in self.df_size.columns
                     if col != 'Product' and col != 'Total' and not col.endswith('_%')]

        # Header
        header = f"{'Sản phẩm':<25}"
        for size in size_cols:
            header += f" {size:<8}"
        header += f" {'Tổng':<10}"

        for size in size_cols:
            header += f" {size}%:<8"

        print(header)
        print("-" * 100)

        # Dữ liệu
        for _, row in self.df_size.iterrows():
            line = f"{row['Product']:<25}"
            for size in size_cols:
                line += f" {row[size]:<8}"
            line += f" {row['Total']:<10}"

            for size in size_cols:
                pct_col = f"{size}_%"
                if pct_col in row:
                    line += f" {row[pct_col]:<7.1f}%"
                else:
                    line += f" {'N/A':<8}"

            print(line)

        print("-" * 100)

        # Tính tổng
        total_L = self.df_size['L'].sum() if 'L' in self.df_size.columns else 0
        total_M = self.df_size['M'].sum() if 'M' in self.df_size.columns else 0
        total_S = self.df_size['S'].sum() if 'S' in self.df_size.columns else 0
        grand_total = total_L + total_M + total_S

        total_L_pct = (total_L / grand_total * 100).round(1) if grand_total > 0 else 0
        total_M_pct = (total_M / grand_total * 100).round(1) if grand_total > 0 else 0
        total_S_pct = (total_S / grand_total * 100).round(1) if grand_total > 0 else 0

        print(f"{'TOTAL':<25} {total_L:<8} {total_M:<8} {total_S:<8} "
              f"{grand_total:<10} {total_L_pct:<7.1f}% {total_M_pct:<7.1f}% {total_S_pct:<7.1f}%")
        print("-" * 100)

        print(f"\nPHÂN TÍCH TỔNG QUAN KÍCH CỠ:")
        print(f"   Tổng số lượng: {grand_total} sản phẩm")
        print(f"   Phân bố: L ({total_L_pct}%), M ({total_M_pct}%), S ({total_S_pct}%)")

        if 'L' in size_cols and 'M' in size_cols and 'S' in size_cols:
            max_size = 'L' if total_L_pct > total_M_pct and total_L_pct > total_S_pct else \
                'M' if total_M_pct > total_S_pct else 'S'
            print(f"   Size phổ biến nhất: {max_size}")

    def visualize_stacked_bar(self, save_path='visualizations/product_size_stacked.png'):
        if self.df_size is None or self.df_size.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        # Lấy các cột kích cỡ
        size_cols = [col for col in self.df_size.columns
                     if col != 'Product' and col != 'Total' and not col.endswith('_%')]

        if not size_cols:
            print("Không tìm thấy cột kích cỡ")
            return

        df_sorted = self.df_size.sort_values('Total', ascending=True)

        plt.figure(figsize=(14, 8))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

        # 1. Stacked bar chart số lượng tuyệt đối
        bottom = np.zeros(len(df_sorted))
        colors = plt.cm.Set3(range(len(size_cols)))

        for i, size in enumerate(size_cols):
            bars = ax1.bar(range(len(df_sorted)), df_sorted[size],
                           bottom=bottom, color=colors[i],
                           label=f'Size {size}', alpha=0.8)
            bottom += df_sorted[size].values

        ax1.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Số lượng', fontsize=12, fontweight='bold')
        ax1.set_title('PHÂN BỐ KÍCH CỠ THEO SẢN PHẨM', fontsize=14, fontweight='bold', pad=20)
        ax1.set_xticks(range(len(df_sorted)))
        ax1.set_xticklabels(df_sorted['Product'], rotation=45, ha='right', fontsize=10)
        ax1.legend(title='Kích cỡ')

        for i, total in enumerate(df_sorted['Total']):
            ax1.text(i, total + 2, f'{total}',
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

        # 2. Stacked bar chart phần trăm
        ax2 = self._create_percentage_chart(ax2, df_sorted, size_cols)

        plt.tight_layout()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Đã lưu biểu đồ tại: {save_path}")
        plt.show()

    def _create_percentage_chart(self, ax, df_sorted, size_cols):
        bottom = np.zeros(len(df_sorted))
        colors = plt.cm.Set2(range(len(size_cols)))

        for i, size in enumerate(size_cols):
            pct_col = f'{size}_%'
            if pct_col in df_sorted.columns:
                percentages = df_sorted[pct_col].values
                bars = ax.bar(range(len(df_sorted)), percentages,
                              bottom=bottom, color=colors[i],
                              label=f'Size {size}', alpha=0.8)
                bottom += percentages

        ax.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tỷ trọng (%)', fontsize=12, fontweight='bold')
        ax.set_title('TỶ TRỌNG KÍCH CỠ THEO SẢN PHẨM', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(range(len(df_sorted)))
        ax.set_xticklabels(df_sorted['Product'], rotation=45, ha='right', fontsize=10)
        ax.set_ylim(0, 100)
        ax.legend(title='Kích cỡ')

        for i in range(len(df_sorted)):
            cumulative = 0
            for size in size_cols:
                pct_col = f'{size}_%'
                if pct_col in df_sorted.columns:
                    pct = df_sorted.iloc[i][pct_col]
                    if pct > 5:
                        ax.text(i, cumulative + pct / 2, f'{pct:.1f}%',
                                ha='center', va='center', fontsize=8, fontweight='bold',
                                color='white' if pct > 15 else 'black')
                    cumulative += pct

        return ax

    def visualize_grouped_bar(self, save_path='visualizations/product_size_grouped.png'):
        if self.df_size is None or self.df_size.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        size_cols = [col for col in self.df_size.columns
                     if col != 'Product' and col != 'Total' and not col.endswith('_%')]

        if not size_cols:
            print("Không tìm thấy cột kích cỡ")
            return

        df_sorted = self.df_size.sort_values('Total', ascending=False)

        plt.figure(figsize=(16, 10))

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))

        # 1. Grouped bar chart số lượng
        x = np.arange(len(df_sorted))
        width = 0.25

        for i, size in enumerate(size_cols):
            offset = width * (i - (len(size_cols) - 1) / 2)
            bars = ax1.bar(x + offset, df_sorted[size], width,
                           label=f'Size {size}',
                           color=plt.cm.tab10(i), alpha=0.8)

            for bar, value in zip(bars, df_sorted[size]):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2., height + 1,
                         f'{int(value)}', ha='center', va='bottom', fontsize=8)

        ax1.set_xlabel('Sản phẩm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Số lượng', fontsize=12, fontweight='bold')
        ax1.set_title('SO SÁNH KÍCH CỠ THEO SẢN PHẨM', fontsize=14, fontweight='bold', pad=20)
        ax1.set_xticks(x)
        ax1.set_xticklabels(df_sorted['Product'], rotation=45, ha='right', fontsize=10)
        ax1.legend()

        # 2. Heatmap phần trăm
        ax2 = self._create_heatmap_chart(ax2, df_sorted, size_cols)

        plt.tight_layout()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Đã lưu biểu đồ tại: {save_path}")
        plt.show()

    def _create_heatmap_chart(self, ax, df_sorted, size_cols):
        heatmap_data = []
        for size in size_cols:
            pct_col = f'{size}_%'
            if pct_col in df_sorted.columns:
                heatmap_data.append(df_sorted[pct_col].values)

        if not heatmap_data:
            return ax

        heatmap_data = np.array(heatmap_data).T

        im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')

        ax.set_xticks(range(len(size_cols)))
        ax.set_xticklabels(size_cols, fontsize=12, fontweight='bold')
        ax.set_yticks(range(len(df_sorted)))
        ax.set_yticklabels(df_sorted['Product'], fontsize=10)

        for i in range(len(df_sorted)):
            for j in range(len(size_cols)):
                if j < heatmap_data.shape[1]:
                    value = heatmap_data[i, j]
                    color = 'white' if value > 50 else 'black'
                    ax.text(j, i, f'{value:.1f}%',
                            ha='center', va='center',
                            color=color, fontsize=9, fontweight='bold')

        ax.set_xlabel('Kích cỡ', fontsize=12, fontweight='bold')
        ax.set_title('HEATMAP TỶ TRỌNG KÍCH CỠ (%)', fontsize=14, fontweight='bold', pad=20)

        plt.colorbar(im, ax=ax, label='Tỷ trọng (%)')

        return ax

    def run_analysis(self):
        print("\n" + "=" * 60)
        print("PHÂN TÍCH BẢNG 5: TỶ TRỌNG KÍCH CỠ SẢN PHẨM")
        print("=" * 60)

        self.display_table()
        self.visualize_stacked_bar()
        self.visualize_grouped_bar()


if __name__ == "__main__":
    analyzer5 = ProductSizeAnalyzer(data_path='output/cleaned_data.csv')
    analyzer5.run_analysis()