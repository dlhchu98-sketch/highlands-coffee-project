"""BẢNG 2: PHÂN TÍCH TỶ TRỌNG DOANH THU THEO KÊNH BÁN HÀNG"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
class ChannelRevenueAnalyzer:
    def __init__(self, data_path='output/cleaned_data.csv'):
        """
        Khởi tạo analyzer với đường dẫn đến file dữ liệu đã làm sạch
        """
        self.data_path = data_path
        self.df = None
        self.df_channel = None  # DataFrame cho Bảng 2
        self.total_revenue = 0

        print("=" * 60)
        print("BẢNG 2: TỶ TRỌNG DOANH THU THEO KÊNH")
        print(f"Đọc từ file: {data_path}")
        print("=" * 60)

        # Tải dữ liệu từ file
        self.load_data()

    def load_data(self):
        """Tải dữ liệu từ file CSV"""
        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            print(f" Đã tải {len(self.df)} dòng dữ liệu")

            # Tìm cột kênh bán hàng và doanh thu
            self._identify_columns()
            # Tạo dữ liệu cho Bảng 2
            self._prepare_channel_data()

        except Exception as e:
            print(f" Lỗi đọc file: {e}")
            print("️ Sử dụng dữ liệu mẫu thay thế")
            self._use_sample_data()

    def _identify_columns(self):
        """Xác định các cột cần thiết"""
        print("\nĐang tìm kiếm các cột trong dữ liệu...")

        # Tìm cột channel (kênh bán hàng)
        channel_keywords = ['channel', 'kênh', 'loại', 'type', 'sales_channel']
        self.channel_col = None

        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in channel_keywords):
                self.channel_col = col
                print(f" Tìm thấy cột kênh: {self.channel_col}")
                break

        # Tìm cột doanh thu
        revenue_keywords = ['revenue', 'doanh_thu', 'doanh thu', 'total', 'amount']
        self.revenue_col = None

        for col in self.df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in revenue_keywords):
                self.revenue_col = col
                print(f" Tìm thấy cột doanh thu: {self.revenue_col}")
                break

        # Nếu không tìm thấy doanh thu, thử tạo từ quantity * price
        if not self.revenue_col:
            self._create_revenue_column()

    def _create_revenue_column(self):
        """Tạo cột doanh thu từ số lượng và giá"""
        print(" Không tìm thấy cột doanh thu, đang tìm số lượng và giá...")

        # Tìm cột số lượng
        qty_keywords = ['quantity', 'qty', 'so_luong', 'số lượng', 'amount']
        qty_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in qty_keywords):
                qty_col = col
                break

        # Tìm cột giá
        price_keywords = ['price', 'gia', 'đơn_giá', 'đơn giá', 'unit_price']
        price_col = None
        for col in self.df.columns:
            if any(keyword in col.lower() for keyword in price_keywords):
                price_col = col
                break

        if qty_col and price_col:
            print(f" Tìm thấy: Số lượng ({qty_col}), Giá ({price_col})")
            self.df['revenue'] = self.df[qty_col] * self.df[price_col]
            self.revenue_col = 'revenue'
            print(f" Đã tạo cột doanh thu từ {qty_col} × {price_col}")
        else:
            print(" Không tìm thấy cột số lượng hoặc giá")
            self.revenue_col = None

    def _prepare_channel_data(self):
        """Chuẩn bị dữ liệu cho Bảng 2"""
        if not self.channel_col or not self.revenue_col:
            print(" Thiếu dữ liệu cần thiết cho phân tích kênh")
            self._use_sample_data()
            return

        print(f"\nĐang tổng hợp doanh thu theo kênh...")
        print(f"   Cột kênh: {self.channel_col}")
        print(f"   Cột doanh thu: {self.revenue_col}")

        # Tổng hợp doanh thu theo kênh
        channel_revenue = self.df.groupby(self.channel_col)[self.revenue_col].sum().reset_index()

        # Sắp xếp theo doanh thu giảm dần
        channel_revenue = channel_revenue.sort_values(self.revenue_col, ascending=False)

        # Lấy top kênh (nếu có nhiều kênh)
        if len(channel_revenue) > 10:
            print(f" Có {len(channel_revenue)} kênh, chỉ hiển thị top 10")
            top_channels = channel_revenue.head(10)
            other_revenue = channel_revenue.iloc[10:][self.revenue_col].sum()

            # Thêm hàng "Khác"
            other_row = pd.DataFrame({
                self.channel_col: ['Khác'],
                self.revenue_col: [other_revenue]
            })

            self.df_channel = pd.concat([top_channels, other_row], ignore_index=True)
        else:
            self.df_channel = channel_revenue

        # Đổi tên cột cho dễ hiểu
        self.df_channel.columns = ['Channel', 'Revenue']

        # Tính tổng doanh thu
        self.total_revenue = self.df_channel['Revenue'].sum()

        # Tính tỷ trọng
        self.df_channel['Percentage'] = (self.df_channel['Revenue'] / self.total_revenue * 100).round(2)

        # Chuyển đổi sang triệu đồng cho dễ đọc
        self.df_channel['Revenue_Mil'] = (self.df_channel['Revenue'] / 1000000).round(2)

        print(f" Đã tổng hợp doanh thu từ {len(self.df_channel)} kênh")

    def _use_sample_data(self):
        """Sử dụng dữ liệu mẫu nếu không đọc được từ file"""
        print("️ Sử dụng dữ liệu mẫu cho Bảng 2")

        self.df_channel = pd.DataFrame({
            'Channel': ['Online', 'Offline'],
            'Revenue': [57218560, 68222000],
            'Percentage': [45.62, 54.38],
            'Revenue_Mil': [57.22, 68.22]
        })

        self.total_revenue = self.df_channel['Revenue'].sum()
        print(" Đã sử dụng dữ liệu mẫu")

    def display_table(self):
        """Hiển thị bảng dữ liệu"""
        if self.df_channel is None or self.df_channel.empty:
            print(" Không có dữ liệu để hiển thị")
            return

        print(f"\nBẢNG DOANH THU THEO KÊNH (Từ file: {os.path.basename(self.data_path)})")
        print("-" * 70)
        print(f"{'Kênh bán hàng':<15} {'Doanh thu (VND)':<20} {'Doanh thu (Triệu)':<18} {'Tỷ trọng %':<12}")
        print("-" * 70)

        for _, row in self.df_channel.iterrows():
            print(f"{row['Channel']:<15} {row['Revenue']:<20,} {row['Revenue_Mil']:<18,.2f} {row['Percentage']:<12}")

        print("-" * 70)
        total_mil = self.total_revenue / 1000000
        print(f"{'TOTAL':<15} {self.total_revenue:<20,} {total_mil:<18,.2f} {'100.00':<12}")
        print("-" * 70)

        # So sánh kênh
        if len(self.df_channel) >= 2:
            # Tìm kênh cao nhất và thấp nhất
            max_channel = self.df_channel.loc[self.df_channel['Revenue'].idxmax()]
            min_channel = self.df_channel.loc[self.df_channel['Revenue'].idxmin()]

            print(f"\n PHÂN TÍCH KÊNH BÁN HÀNG:")
            print(
                f"   • Kênh cao nhất: {max_channel['Channel']} - {max_channel['Revenue_Mil']:,.2f} triệu ({max_channel['Percentage']}%)")
            print(
                f"   • Kênh thấp nhất: {min_channel['Channel']} - {min_channel['Revenue_Mil']:,.2f} triệu ({min_channel['Percentage']}%)")

            if len(self.df_channel) == 2:
                # So sánh Online vs Offline
                online_rev = self.df_channel[self.df_channel['Channel'] == 'Online']
                offline_rev = self.df_channel[self.df_channel['Channel'] == 'Offline']

                if not online_rev.empty and not offline_rev.empty:
                    online_val = online_rev.iloc[0]['Revenue']
                    offline_val = offline_rev.iloc[0]['Revenue']

                    if online_val > offline_val:
                        diff = online_val - offline_val
                        diff_percent = (diff / offline_val * 100).round(1)
                        print(f"   • Online cao hơn Offline: {diff:,.0f} VND ({diff_percent}%)")
                    else:
                        diff = offline_val - online_val
                        diff_percent = (diff / online_val * 100).round(1)
                        print(f"   • Offline cao hơn Online: {diff:,.0f} VND ({diff_percent}%)")

        # Phân tích Pareto nếu có nhiều kênh
        if len(self.df_channel) > 2:
            print(f"\n PHÂN TÍCH PARETO:")
            # Tính tỷ trọng tích lũy
            self.df_channel['Cumulative_Percentage'] = self.df_channel['Percentage'].cumsum()

            # Tìm kênh chiếm 80% doanh thu
            pareto_channels = self.df_channel[self.df_channel['Cumulative_Percentage'] <= 80]
            print(f"   • {len(pareto_channels)}/{len(self.df_channel)} kênh chiếm 80% doanh thu")
            print(f"   • Các kênh quan trọng: {', '.join(pareto_channels['Channel'].tolist())}")

    def visualize_pie_chart(self, save_path='visualizations/channel_revenue_pie.png'):
        """Vẽ biểu đồ tròn tỷ trọng doanh thu theo kênh"""
        if self.df_channel is None or self.df_channel.empty:
            print(" Không có dữ liệu để vẽ biểu đồ")
            return

        plt.figure(figsize=(10, 8))

        # Tạo 2 subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # 1. Pie chart cơ bản
        wedges1, texts1, autotexts1 = ax1.pie(
            self.df_channel['Revenue'],
            labels=self.df_channel['Channel'],
            autopct=lambda pct: f'{pct:.1f}%\n({pct * self.total_revenue / 100:,.0f} VND)',
            startangle=90,
            colors=plt.cm.Set2(range(len(self.df_channel))),
            explode=[0.05 if i == 0 else 0 for i in range(len(self.df_channel))],  # Làm nổi kênh đầu tiên
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
            text.set_fontsize(11)
            text.set_fontweight('bold')

        # 2. Donut chart
        wedges2, texts2, autotexts2 = ax2.pie(
            self.df_channel['Revenue'],
            labels=self.df_channel['Channel'],
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3(range(len(self.df_channel))),
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
        if self.df_channel is None or self.df_channel.empty:
            print(" Không có dữ liệu để vẽ biểu đồ")
            return

        plt.figure(figsize=(12, 7))

        # Tạo subplot 2x1
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # 1. Bar chart đơn giản
        bars1 = ax1.bar(self.df_channel['Channel'], self.df_channel['Revenue_Mil'],
                        color=plt.cm.viridis(range(len(self.df_channel))), alpha=0.8)

        ax1.set_ylabel('Doanh thu (Triệu VND)', fontsize=12, fontweight='bold')
        ax1.set_title('DOANH THU THEO KÊNH BÁN HÀNG',
                      fontsize=14, fontweight='bold', pad=20)

        # Thêm giá trị trên bar
        for bar, rev_mil, pct in zip(bars1, self.df_channel['Revenue_Mil'], self.df_channel['Percentage']):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                     f'{rev_mil:,.1f} triệu\n({pct}%)',
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        # 2. Horizontal bar chart
        ax2.barh(self.df_channel['Channel'], self.df_channel['Percentage'],
                 color=plt.cm.Set3(range(len(self.df_channel))), alpha=0.8)

        ax2.set_xlabel('Tỷ trọng (%)', fontsize=12, fontweight='bold')
        ax2.set_title('TỶ TRỌNG DOANH THU THEO KÊNH',
                      fontsize=14, fontweight='bold', pad=20)
        ax2.set_xlim(0, max(self.df_channel['Percentage']) * 1.2)

        # Thêm giá trị phần trăm
        for i, (channel, pct) in enumerate(zip(self.df_channel['Channel'], self.df_channel['Percentage'])):
            ax2.text(pct + 1, i, f'{pct}%',
                     va='center', fontsize=11, fontweight='bold')

        # Thêm thông tin tổng
        info_text = (f"Dữ liệu từ: {os.path.basename(self.data_path)}\n"
                     f"Tổng doanh thu: {self.total_revenue:,.0f} VND\n"
                     f"Tương đương: {self.total_revenue / 1000000:,.1f} triệu VND")

        ax2.text(0.5, -0.2, info_text,
                 transform=ax2.transAxes,
                 ha='center', fontsize=11,
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


# Chạy phân tích Bảng 2 với dữ liệu từ file
if __name__ == "__main__":
    analyzer2 = ChannelRevenueAnalyzer(data_path='output/cleaned_data.csv')
    analyzer2.run_analysis()