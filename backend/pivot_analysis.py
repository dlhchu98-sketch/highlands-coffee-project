"""Tạo và cập nhật các bảng pivot từ dữ liệu đã làm sạch"""
import os

print("THU MUC HIEN TAI:", os.getcwd())
print("\nKIEM TRA CAC FILE TRONG THU MUC HIEN TAI:")
for file in os.listdir('.'):
    if os.path.isfile(file):
        print(f"  - {file}")

print("\nKIEM TRA THU MUC 'output':")
if os.path.exists('output'):
    for file in os.listdir('output'):
        print(f"  - {file}")
else:
    print("  Thu muc 'output' khong ton tai")
import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class PivotAnalyzer:
    """Lớp phân tích và tạo bảng pivot từ dữ liệu"""

    def __init__(self, data_path='output/cleaned_data.csv'):
        """Khởi tạo analyzer với đường dẫn đến dữ liệu đã làm sạch"""
        self.data_path = data_path
        self.df = None
        self.pivot_tables = {}
        print("=" * 50)
        print("CÔNG CỤ PHÂN TÍCH PIVOT")
        print("=" * 50)

    def load_cleaned_data(self):
        """Tải dữ liệu đã làm sạch"""
        print("\nĐANG TẢI DỮ LIỆU ĐÃ LÀM SẠCH...")

        if not os.path.exists(self.data_path):
            print(f"Không tìm thấy file: {self.data_path}")
            print("   Vui lòng chạy data_preprocess.py trước để tạo dữ liệu đã làm sạch")
            return False

        try:
            self.df = pd.read_csv(self.data_path, encoding='utf-8-sig')
            print(f" Đã tải dữ liệu: {len(self.df)} dòng, {len(self.df.columns)} cột")

            # Hiển thị thông tin cơ bản
            print("\n THÔNG TIN CÁC CỘT:")
            for i, col in enumerate(self.df.columns, 1):
                dtype = self.df[col].dtype
                unique_count = self.df[col].nunique()
                print(f"   {i:2} {col:20} | {str(dtype):10} | {unique_count:5} giá trị duy nhất")

            return True

        except Exception as e:
            print(f" Lỗi khi tải dữ liệu: {e}")
            return False

    def explore_data_structure(self):
        """Khám phá cấu trúc dữ liệu để đề xuất pivot"""
        print("\nPHÂN TÍCH CẤU TRÚC DỮ LIỆU...")

        if self.df is None:
            print(" Chưa có dữ liệu")
            return

        # Phân loại các cột
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        date_cols = [col for col in self.df.columns if 'date' in col.lower() or 'time' in col.lower()]
        category_cols = self.df.select_dtypes(include=['object']).columns.tolist()

        print(f" Phát hiện {len(numeric_cols)} cột số:")
        for col in numeric_cols[:10]:
            print(f"  {col} (min={self.df[col].min():,.0f}, max={self.df[col].max():,.0f})")

        print(f"\n Phát hiện {len(date_cols)} cột ngày tháng:")
        for col in date_cols:
            print(f"  {col}")

        print(f"\nPhát hiện {len(category_cols)} cột phân loại:")
        for col in category_cols[:10]:
            unique_vals = self.df[col].nunique()
            sample_vals = self.df[col].dropna().unique()[:3]
            print(f"  {col} ({unique_vals} giá trị) ví dụ: {sample_vals}")

        # Đề xuất pivot
        print("\n ĐỀ XUẤT PIVOT TABLE:")

        if 'revenue' in numeric_cols:
            print("1. Doanh thu theo thời gian và danh mục")
        if len(date_cols) > 0 and len(category_cols) > 0:
            print("2. Phân tích xu hướng theo thời gian")
        if len(category_cols) >= 2:
            print("3. So sánh giữa các danh mục")

    def create_sales_pivot(self, date_col=None, category_col=None, value_col='revenue'):
        """Tạo pivot table cho phân tích doanh thu"""
        print(f"\nTẠO PIVOT TABLE: DOANH THU")

        if self.df is None:
            print(" Chưa có dữ liệu")
            return None

        # Tự động phát hiện cột nếu không chỉ định
        if date_col is None:
            date_cols = [col for col in self.df.columns if 'date' in col.lower()]
            date_col = date_cols[0] if date_cols else None

        if category_col is None:
            # Tìm cột phân loại phù hợp
            category_options = ['category', 'type', 'product', 'region', 'channel', 'staff']
            for opt in category_options:
                for col in self.df.columns:
                    if opt in col.lower():
                        category_col = col
                        break
                if category_col:
                    break

        if value_col not in self.df.columns:
            # Tìm cột giá trị thay thế
            value_options = ['revenue', 'amount', 'quantity', 'sales', 'value']
            for opt in value_options:
                for col in self.df.columns:
                    if opt in col.lower() and self.df[col].dtype in [np.number]:
                        value_col = col
                        break
                if value_col in self.df.columns:
                    break

        print(f"  Cột thời gian: {date_col}")
        print(f"  Cột danh mục: {category_col}")
        print(f"  Cột giá trị: {value_col}")

        if date_col and category_col and value_col in self.df.columns:
            try:
                # Tạo pivot table
                pivot_df = pd.pivot_table(
                    self.df,
                    values=value_col,
                    index=date_col,
                    columns=category_col,
                    aggfunc='sum',
                    fill_value=0,
                    margins=True,
                    margins_name='Tổng'
                )

                # Lưu pivot table
                pivot_name = f"pivot_{value_col}_by_{date_col}_and_{category_col}"
                self.pivot_tables[pivot_name] = pivot_df

                print(f"Đã tạo pivot table: {pivot_name}")
                print(f" Kích thước: {pivot_df.shape[0]} dòng × {pivot_df.shape[1]} cột")

                # Hiển thị tổng quan
                print("\nTỔNG QUAN PIVOT TABLE:")
                print(pivot_df.head())

                return pivot_df

            except Exception as e:
                print(f" Lỗi khi tạo pivot: {e}")
                return None
        else:
            print("Không đủ dữ liệu để tạo pivot table")
            return None

    def create_time_series_pivot(self, date_col=None, freq='M'):
        """Tạo pivot table theo chuỗi thời gian"""
        print(f"\n[4] TẠO PIVOT TABLE: CHUỖI THỜI GIAN (tần suất: {freq})")

        if self.df is None:
            print(" Chưa có dữ liệu")
            return None

        # Tìm cột ngày tháng
        if date_col is None:
            date_cols = [col for col in self.df.columns if 'date' in col.lower()]
            date_col = date_cols[0] if date_cols else None

        if date_col is None or date_col not in self.df.columns:
            print(" Không tìm thấy cột ngày tháng")
            return None

        # Chuyển đổi sang datetime nếu chưa
        if not pd.api.types.is_datetime64_any_dtype(self.df[date_col]):
            self.df[date_col] = pd.to_datetime(self.df[date_col], errors='coerce')

        # Tìm cột số để phân tích
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            print("Không tìm thấy cột số để phân tích")
            return None

        # Tạo cột thời gian tổng hợp
        freq_map = {'D': 'Ngày', 'W': 'Tuần', 'M': 'Tháng', 'Q': 'Quý', 'Y': 'Năm'}
        freq_name = freq_map.get(freq, freq)

        self.df['time_period'] = self.df[date_col].dt.to_period(freq)

        # Tạo pivot table cho từng cột số
        pivot_results = {}

        for value_col in numeric_cols[:5]:  # Giới hạn 5 cột đầu tiên
            try:
                pivot_df = pd.pivot_table(
                    self.df,
                    values=value_col,
                    index='time_period',
                    aggfunc=['sum', 'mean', 'count'],
                    fill_value=0
                )

                # Làm phẳng multi-index columns
                pivot_df.columns = [f'{agg}_{value_col}' for agg in pivot_df.columns.get_level_values(0)]

                pivot_name = f"timeseries_{value_col}_{freq}"
                pivot_results[pivot_name] = pivot_df

                print(f"{value_col}: {len(pivot_df)} {freq_name.lower()}")

            except Exception as e:
                print(f" {value_col}: Lỗi - {e}")

        if pivot_results:
            self.pivot_tables.update(pivot_results)
            # Kết hợp tất cả pivot tables
            combined_pivot = pd.concat(list(pivot_results.values()), axis=1)
            return combined_pivot
        else:
            return None

    def create_category_comparison_pivot(self, category_cols=None, value_col='revenue'):
        """Tạo pivot table so sánh giữa các danh mụ"""
        print("\n[5] TẠO PIVOT TABLE: SO SÁNH DANH MỤC")

        if self.df is None:
            print(" Chưa có dữ liệu")
            return None

        # Tìm cột danh mục nếu không chỉ định
        if category_cols is None:
            category_cols = []
            category_keywords = ['category', 'type', 'product', 'region', 'channel', 'status', 'group']

            for keyword in category_keywords:
                for col in self.df.select_dtypes(include=['object']).columns:
                    if keyword in col.lower() and self.df[col].nunique() <= 20:  # Giới hạn số lượng danh mục
                        category_cols.append(col)

                if len(category_cols) >= 3:  # Lấy tối đa 3 cột
                    break

        if len(category_cols) < 2:
            print(" Cần ít nhất 2 cột danh mục để so sánh")
            return None

        # Tìm cột giá trị
        if value_col not in self.df.columns:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            value_col = numeric_cols[0] if len(numeric_cols) > 0 else None

        if value_col is None:
            print(" Không tìm thấy cột số để so sánh")
            return None

        print(f"  Cột danh mục: {category_cols}")
        print(f"  Cột giá trị: {value_col}")

        try:
            # Tạo pivot table multi-level
            pivot_df = pd.pivot_table(
                self.df,
                values=value_col,
                index=category_cols,
                aggfunc=['sum', 'count', 'mean', 'std'],
                fill_value=0,
                margins=True,
                margins_name='Tổng'
            )

            # Làm phẳng multi-index
            pivot_df = pivot_df.round(2)

            pivot_name = f"comparison_{value_col}_by_{'_and_'.join(category_cols[:2])}"
            self.pivot_tables[pivot_name] = pivot_df

            print(f"Đã tạo pivot table so sánh")
            print(f" Kích thước: {pivot_df.shape[0]} dòng × {pivot_df.shape[1]} cột")

            # Hiển thị top 10 dòng
            print("\n TOP 10 DANH MỤC:")
            top_categories = pivot_df.nlargest(10, ('sum', value_col))
            print(top_categories)

            return pivot_df

        except Exception as e:
            print(f" Lỗi khi tạo pivot: {e}")
            return None

    def create_custom_pivot(self, values=None, index=None, columns=None, aggfunc='sum'):
        """tạo pivot table tùy chỉn"""
        print("\n[6] TẠO PIVOT TABLE TÙY CHỈNH")

        if self.df is None:
            print(" Chưa có dữ liệu")
            return None

        # Hiển thị các cột có sẵn
        print("\CÁC CỘT CÓ SẴN:")
        for i, col in enumerate(self.df.columns, 1):
            dtype = self.df[col].dtype
            print(f"   {i:2}{col:25} [{dtype}]")

        # Nếu không có tham số, hỏi người dùng
        if values is None:
            print("\n Nhập tên cột giá trị (values): ", end="")
            values = input().strip()

        if index is None:
            print(" Nhập tên cột index (ấn Enter để bỏ qua): ", end="")
            index_input = input().strip()
            index = index_input if index_input else None

        if columns is None:
            print(" Nhập tên cột columns (ấn Enter để bỏ qua): ", end="")
            columns_input = input().strip()
            columns = columns_input if columns_input else None

        try:
            # Tạo pivot table
            pivot_df = pd.pivot_table(
                self.df,
                values=values,
                index=index,
                columns=columns,
                aggfunc=aggfunc,
                fill_value=0,
                margins=True,
                margins_name='Tổng'
            )

            # Tạo tên cho pivot
            pivot_name = f"custom_pivot_{values}"
            if index:
                pivot_name += f"_by_{index}"
            if columns:
                pivot_name += f"_and_{columns}"

            self.pivot_tables[pivot_name] = pivot_df

            print(f"\n Đã tạo pivot table: {pivot_name}")
            print(f" Kích thước: {pivot_df.shape}")

            # Hiển thị kết quả
            print("\n KẾT QUẢ PIVOT TABLE:")
            print(pivot_df.head(10))

            return pivot_df

        except Exception as e:
            print(f" Lỗi khi tạo pivot: {e}")
            return None

    def save_pivot_tables(self, output_folder='output/pivot_tables'):
        """Lưu tất cả pivot tables ra file Excel"""
        print("\n[7] LƯU PIVOT TABLES...")

        if not self.pivot_tables:
            print(" Chưa có pivot table nào để lưu")
            return False

        try:
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(output_folder, exist_ok=True)

            # Tạo timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            excel_file = os.path.join(output_folder, f"pivot_analysis_{timestamp}.xlsx")

            # Tạo Excel writer
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                for pivot_name, pivot_df in self.pivot_tables.items():
                    # Giới hạn tên sheet (Excel giới hạn 31 ký tự)
                    sheet_name = pivot_name[:31]

                    # Ghi vào sheet
                    pivot_df.to_excel(writer, sheet_name=sheet_name)

                    # Định dạng cột width
                    worksheet = writer.sheets[sheet_name]
                    for column in pivot_df:
                        column_width = max(pivot_df[column].astype(str).map(len).max(), len(str(column)))
                        col_idx = pivot_df.columns.get_loc(column)
                        worksheet.column_dimensions[chr(65 + col_idx)].width = min(column_width + 2, 50)

            print(f" Đã lưu {len(self.pivot_tables)} pivot tables vào: {excel_file}")

            # Lưu riêng từng file CSV
            csv_folder = os.path.join(output_folder, 'csv_files')
            os.makedirs(csv_folder, exist_ok=True)

            for pivot_name, pivot_df in self.pivot_tables.items():
                csv_file = os.path.join(csv_folder, f"{pivot_name}.csv")
                pivot_df.to_csv(csv_file, encoding='utf-8-sig')
                print(f"  {pivot_name}.csv")

            return True

        except Exception as e:
            print(f" Lỗi khi lưu pivot tables: {e}")
            return False

    def generate_pivot_report(self):
        """Tạo báo cáo tổng hợp về các pivot tables"""
        print("\n" + "=" * 50)
        print("BÁO CÁO PHÂN TÍCH PIVOT")
        print("=" * 50)

        if not self.pivot_tables:
            print(" Chưa có pivot table nào được tạo")
            return

        print(f"\n TỔNG SỐ PIVOT TABLES: {len(self.pivot_tables)}")
        print("-" * 50)

        for i, (pivot_name, pivot_df) in enumerate(self.pivot_tables.items(), 1):
            print(f"\n{i}. {pivot_name}")
            print(f"   Kích thước: {pivot_df.shape[0]} dòng × {pivot_df.shape[1]} cột")

            # Thông tin thống kê
            if isinstance(pivot_df, pd.DataFrame):
                numeric_cols = pivot_df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    total_sum = pivot_df[numeric_cols].sum().sum()
                    print(f"   Tổng giá trị: {total_sum:,.0f}")

            # Hiển thị top 5 dòng
            print(f"   Top 5 dòng:")
            print(pivot_df.head().to_string())

    def run_full_analysis(self):
        """Chạy toàn bộ phân tích pivot tự động"""
        print("\n" + "=" * 50)
        print("BẮT ĐẦU PHÂN TÍCH PIVOT TỰ ĐỘNG")
        print("=" * 50)

        # 1. Tải dữ liệu
        if not self.load_cleaned_data():
            return

        # 2. Phân tích cấu trúc
        self.explore_data_structure()

        # 3. Tạo các pivot tables cơ bản
        print("\n" + "=" * 50)
        print("TẠO PIVOT TABLES TỰ ĐỘNG")
        print("=" * 50)

        # Pivot doanh thu
        sales_pivot = self.create_sales_pivot()

        # Pivot chuỗi thời gian
        time_pivot = self.create_time_series_pivot(freq='M')

        # Pivot so sánh danh mục
        category_pivot = self.create_category_comparison_pivot()

        # 4. Lưu kết quả
        self.save_pivot_tables()

        # 5. Tạo báo cáo
        self.generate_pivot_report()

        print("\n" + "=" * 50)
        print("HOÀN THÀNH PHÂN TÍCH PIVOT!")
        print("=" * 50)


if __name__ == "__main__":
    print("=== DEBUG THONG TIN ===")
    print(f"Thu muc hien tai: {os.getcwd()}")
    print(f"Noi dung thu muc hien tai: {os.listdir('.')}")

    print("\n=== BAT DAU PHAN TICH ===")

    # Tạo analyzer - tự động tìm file
    analyzer = PivotAnalyzer()

    # Chạy phân tích
    analyzer.run_full_analysis()

