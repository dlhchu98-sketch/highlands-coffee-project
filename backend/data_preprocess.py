"""
CÔNG CỤ LÀM SẠCH DỮ LIỆU CSV
Tác giả: [Tên của bạn]
Mục tiêu: Tiền xử lý dữ liệu để sẵn sàng cho phân tích và visualization
"""

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    Lớp xử lý và làm sạch dữ liệu từ file CSV
    """

    def __init__(self, data_folder='data'):
        """
        Khởi tạo preprocessor với thư mục chứa dữ liệu

        Args:
            data_folder (str): Đường dẫn đến thư mục chứa file CSV
        """
        self.data_folder = data_folder
        self.df = None
        self.original_shape = None
        print("=" * 50)
        print("CÔNG CỤ LÀM SẠCH DỮ LIỆU")
        print("=" * 50)

    # ==================== PHẦN 1: ĐỌC VÀ KHÁM PHÁ DỮ LIỆU ====================

    def find_csv_file(self):
        """
        Tìm file CSV trong thư mục data

        Returns:
            str: Đường dẫn đến file CSV hoặc None nếu không tìm thấy
        """
        print("\n[1] TÌM FILE CSV TRONG THƯ MỤC...")

        # Tìm tất cả file CSV
        csv_files = []
        for file in os.listdir(self.data_folder):
            if file.lower().endswith('.csv'):
                csv_files.append(os.path.join(self.data_folder, file))

        if not csv_files:
            print(f"KHONG TIM THAY FILE CSV trong thu muc '{self.data_folder}/'")
            print("   Vui long dat file CSV vao thu muc data/")
            return None

        print(f"TIM THAY {len(csv_files)} file CSV:")
        for i, file in enumerate(csv_files, 1):
            print(f"   {i}. {os.path.basename(file)}")

        # Chọn file đầu tiên (có thể mở rộng để cho người dùng chọn)
        selected_file = csv_files[0]
        print(f"\nDang su dung file: {os.path.basename(selected_file)}")

        return selected_file

    def load_data(self, file_path=None, encoding='utf-8'):
        """
        Đọc dữ liệu từ file CSV bằng pandas

        Args:
            file_path (str): Đường dẫn đến file CSV
            encoding (str): Encoding của file

        Returns:
            bool: True nếu load thành công, False nếu thất bại
        """
        print("\n[2] DOC DU LIEU TU FILE CSV...")

        if file_path is None:
            file_path = self.find_csv_file()
            if file_path is None:
                return False

        try:
            print(f"   Dang doc: {os.path.basename(file_path)}")

            # Thử các encoding phổ biến nếu có lỗi
            encodings_to_try = [encoding, 'latin1', 'cp1258', 'utf-16']

            for enc in encodings_to_try:
                try:
                    self.df = pd.read_csv(file_path, encoding=enc)
                    print(f"   DOC THANH CONG voi encoding: {enc}")
                    break
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"   LOI voi encoding {enc}: {e}")

            if self.df is None:
                print("   KHONG THE DOC FILE voi cac encoding da thu")
                return False

            self.original_shape = self.df.shape
            print(f"   DA LOAD {self.original_shape[0]} dong, {self.original_shape[1]} cot")
            print(f"   Pham vi du lieu tu dong {self.df.index[0] + 1} den {self.df.index[-1] + 1}")

            return True

        except Exception as e:
            print(f"   LOI khi doc file CSV: {e}")
            return False

    def explore_data(self):
        """
        Khám phá dữ liệu ban đầu (số dòng, số cột, kiểu dữ liệu)
        """
        print("\n[3] KHAM PHA DU LIEU BAN DAU...")

        if self.df is None:
            print("   CHUA CO DU LIEU de kham pha")
            return

        # Thông tin cơ bản
        print(f"   So dong: {self.df.shape[0]}")
        print(f"   So cot: {self.df.shape[1]}")
        print(f"   Dung luong bo nho: {self.df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")

        # Kiểu dữ liệu của các cột
        print("\n   KIEU DU LIEU CAC COT:")
        dtype_summary = self.df.dtypes.value_counts()
        for dtype, count in dtype_summary.items():
            print(f"     {dtype}: {count} cot")

        # Xem 5 dòng đầu
        print("\n   5 DONG DAU TIEN:")
        print(self.df.head())

        # Thống kê cơ bản
        print("\n   THONG KE CO BAN:")
        print(self.df.describe(include='all').T.head(10))

    # ==================== PHẦN 2: CHUẨN HOÁ DỮ LIỆU ====================

    def standardize_column_names(self):
        """
        Chuẩn hoá tên cột (loại bỏ khoảng trắng, thống nhất chữ hoa/thường, dễ đọc)
        """
        print("\n[4] CHUAN HOA TEN COT...")

        if self.df is None:
            print("   CHUA CO DU LIEU")
            return

        original_names = self.df.columns.tolist()
        new_names = []

        for col in original_names:
            # Chuyển về chữ thường
            new_col = str(col).strip().lower()

            # Thay thế khoảng trắng và ký tự đặc biệt bằng gạch dưới
            new_col = re.sub(r'\s+', '_', new_col)
            new_col = re.sub(r'[^\w_]', '', new_col)

            # Xóa nhiều gạch dưới liên tiếp
            new_col = re.sub(r'_+', '_', new_col)

            # Xóa gạch dưới ở đầu và cuối
            new_col = new_col.strip('_')

            # Đảm bảo tên cột không rỗng
            if not new_col:
                new_col = f'column_{len(new_names)}'

            new_names.append(new_col)

        # Kiểm tra xem có trùng tên không
        if len(set(new_names)) != len(new_names):
            print("   CO TEN COT TRUNG NHAU SAU KHI CHUAN HOA")
            # Thêm số thứ tự cho các tên trùng
            seen = {}
            for i, name in enumerate(new_names):
                if name in seen:
                    seen[name] += 1
                    new_names[i] = f"{name}_{seen[name]}"
                else:
                    seen[name] = 1

        # Áp dụng tên mới
        self.df.columns = new_names

        print(f"   DA CHUAN HOA {len(original_names)} ten cot")
        print("\n   THAY DOI TEN COT:")
        for old, new in zip(original_names[:10], new_names[:10]):
            print(f"     '{old}' -> '{new}'")

        if len(original_names) > 10:
            print(f"     ... va {len(original_names) - 10} cot khac")

    def convert_date_columns(self):
        """
        Chuyển đổi và xử lý cột ngày tháng (parse về datetime, tách năm/tháng nếu cần)
        """
        print("\n[5] XU LY COT NGAY THANG...")

        if self.df is None:
            print("   CHUA CO DU LIEU")
            return

        date_columns = []
        date_patterns = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d',
                         '%d-%m-%Y', '%m-%d-%Y', '%Y.%m.%d', '%d.%m.%Y']

        # Tìm các cột có thể là ngày tháng
        for col in self.df.columns:
            # Kiểm tra cột object/string
            if self.df[col].dtype == 'object':
                sample = self.df[col].dropna().head(100)
                if len(sample) > 0:
                    # Thử parse ngày tháng
                    for pattern in date_patterns:
                        try:
                            pd.to_datetime(sample, format=pattern, errors='raise')
                            date_columns.append(col)
                            break
                        except:
                            continue

        if not date_columns:
            print("   KHONG TIM THAY COT NGAY THANG")
            return

        print(f"   TIM THAY {len(date_columns)} cot ngay thang:")

        for col in date_columns:
            print(f"\n   XU LY COT: '{col}'")

            try:
                # Chuyển về datetime
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')

                # Tạo các cột mới từ ngày tháng
                self.df[f'{col}_year'] = self.df[col].dt.year
                self.df[f'{col}_month'] = self.df[col].dt.month
                self.df[f'{col}_day'] = self.df[col].dt.day
                self.df[f'{col}_quarter'] = self.df[col].dt.quarter
                self.df[f'{col}_weekday'] = self.df[col].dt.weekday

                # Kiểm tra số giá trị không hợp lệ
                invalid_count = self.df[col].isna().sum()
                if invalid_count > 0:
                    print(f"     CO {invalid_count} gia tri ngay thang khong hop le (da chuyen thanh NaT)")

                print(f"     DA CHUYEN VA TACH THANH 5 COT MOI")

            except Exception as e:
                print(f"     LOI khi xu ly cot {col}: {e}")

    def convert_numeric_columns(self):
        """
        Chuyển các cột số về đúng kiểu numeric
        """
        print("\n[6] CHUYEN DOI COT SO...")

        if self.df is None:
            print("   CHUA CO DU LIEU")
            return

        converted_count = 0

        for col in self.df.columns:
            # Bỏ qua các cột datetime đã xử lý
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                continue

            # Kiểm tra nếu cột object có thể chuyển thành số
            if self.df[col].dtype == 'object':
                try:
                    # Thử chuyển đổi
                    original_non_null = self.df[col].notna().sum()
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    new_non_null = self.df[col].notna().sum()

                    if original_non_null > 0 and new_non_null > 0:
                        loss_percentage = (original_non_null - new_non_null) / original_non_null * 100
                        if loss_percentage < 10:  # Mất dưới 10% dữ liệu
                            converted_count += 1
                            print(f"   '{col}': DA CHUYEN THANH numeric")
                        else:
                            print(f"   '{col}': MAT {loss_percentage:.1f}% du lieu khi chuyen doi")
                    elif new_non_null > 0:
                        converted_count += 1
                        print(f"   '{col}': DA CHUYEN THANH numeric")

                except Exception as e:
                    continue

        # Kiểm tra các cột numeric hiện tại
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        print(f"\n   TONG CONG: {len(numeric_cols)} cot so")
        print(f"   DA CHUYEN DOI: {converted_count} cot tu object sang numeric")

    # ==================== PHẦN 3: XỬ LÝ DỮ LIỆU THIẾU VÀ KHÔNG HỢP LỆ ====================

    def handle_missing_values(self, strategy='auto'):
        """
        Phát hiện và xử lý dữ liệu thiếu (fill hoặc loại bỏ hợp lý)

        Args:
            strategy (str): 'auto', 'fill', 'drop', hoặc 'report'
        """
        print("\n[7] XU LY DU LIEU THIEU...")

        if self.df is None:
            print("   CHUA CO DU LIEU")
            return

        # Phát hiện dữ liệu thiếu
        missing_stats = self.df.isnull().sum()
        total_missing = missing_stats.sum()
        total_cells = self.df.shape[0] * self.df.shape[1]

        print(
            f"   Tong so gia tri thieu: {total_missing:,} / {total_cells:,} ({total_missing / total_cells * 100:.2f}%)")

        if total_missing == 0:
            print("   KHONG CO DU LIEU THIEU")
            return

        # Hiển thị các cột có dữ liệu thiếu
        missing_cols = missing_stats[missing_stats > 0]
        print(f"\n   CAC COT CO DU LIEU THIEU:")
        for col, count in missing_cols.head(15).items():
            percentage = count / self.df.shape[0] * 100
            print(f"     '{col}': {count:,} gia tri ({percentage:.1f}%)")

        if len(missing_cols) > 15:
            print(f"     ... va {len(missing_cols) - 15} cot khac")

        # Xử lý theo chiến lược
        if strategy == 'auto':
            print(f"\n   XU LY TU DONG...")
            for col in missing_cols.index:
                percentage = missing_cols[col] / self.df.shape[0] * 100

                if percentage > 30:  # Xóa cột nếu thiếu quá nhiều
                    print(f"     '{col}': XOA COT (thieu {percentage:.1f}%)")
                    self.df.drop(columns=[col], inplace=True)
                elif self.df[col].dtype in ['float64', 'int64']:  # Cột số
                    if self.df[col].dtype == 'int64':
                        fill_value = int(self.df[col].median()) if not self.df[col].isnull().all() else 0
                    else:
                        fill_value = self.df[col].median()
                    self.df[col].fillna(fill_value, inplace=True)
                    print(f"     '{col}': DIEN BANG {fill_value}")
                else:  # Cột không phải số
                    fill_value = self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'Unknown'
                    self.df[col].fillna(fill_value, inplace=True)
                    print(f"     '{col}': DIEN BANG '{fill_value}'")

        elif strategy == 'fill':
            # Người dùng tự chọn cách điền
            pass

        elif strategy == 'drop':
            # Xóa dòng có dữ liệu thiếu
            before = len(self.df)
            self.df.dropna(inplace=True)
            after = len(self.df)
            print(f"\n     DA XOA {before - after} dong co du lieu thieu")
            print(f"     CON LAI {after} dong ({after / before * 100:.1f}%)")

        # Kiểm tra lại sau khi xử lý
        remaining_missing = self.df.isnull().sum().sum()
        print(f"\n   SAU XU LY: CON {remaining_missing} gia tri thieu")

    def remove_invalid_data(self):
        """
        Loại bỏ dữ liệu sai hoặc không hợp lệ (giá trị âm, số lượng ≤ 0, dòng trùng lặp)
        """
        print("\n[8] LOAI BO DU LIEU KHONG HOP LE...")

        if self.df is None:
            print("   CHUA CO DU LIEU")
            return

        initial_rows = len(self.df)
        removed_counts = {}

        # 1. Loại bỏ dòng trùng lặp
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.df = self.df.drop_duplicates()
            removed_counts['Dong trung'] = duplicates
            print(f"   DA XOA {duplicates} dong trung lap")

        # 2. Loại bỏ giá trị âm trong cột số lượng/giá
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            # Kiểm tra tên cột có chứa từ khóa chỉ số lượng
            if any(keyword in col.lower() for keyword in ['quantity', 'qty', 'amount', 'sl', 'soluong']):
                negative_count = (self.df[col] < 0).sum()
                if negative_count > 0:
                    self.df = self.df[self.df[col] >= 0]
                    removed_counts[f'Gia tri am trong {col}'] = negative_count
                    print(f"   '{col}': XOA {negative_count} gia tri am")

            # Kiểm tra giá
            elif any(keyword in col.lower() for keyword in ['price', 'gia', 'cost', 'don_gia']):
                zero_or_negative = (self.df[col] <= 0).sum()
                if zero_or_negative > 0:
                    self.df = self.df[self.df[col] > 0]
                    removed_counts[f'Gia ≤ 0 trong {col}'] = zero_or_negative
                    print(f"   '{col}': XOA {zero_or_negative} gia tri ≤ 0")

        # 3. Kiểm tra dữ liệu không hợp lệ khác
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # Kiểm tra giá trị rỗng hoặc chỉ có khoảng trắng
                empty_count = self.df[col].astype(str).str.strip().eq('').sum()
                if empty_count > 0:
                    self.df = self.df[~self.df[col].astype(str).str.strip().eq('')]
                    removed_counts[f'Gia tri rong trong {col}'] = empty_count
                    print(f"   '{col}': XOA {empty_count} gia tri rong")

        # Tổng kết
        final_rows = len(self.df)
        total_removed = initial_rows - final_rows

        if total_removed > 0:
            print(f"\n   TONG KET:")
            print(f"     Dong ban dau: {initial_rows}")
            print(f"     Dong da xoa: {total_removed}")
            print(f"     Dong con lai: {final_rows}")

            for reason, count in removed_counts.items():
                print(f"     - {reason}: {count}")
        else:
            print("   KHONG CO DU LIEU KHONG HOP LE")

    # ==================== PHẦN 4: TẠO CỘT MỚI ====================

    def create_basic_columns(self):
        """
        Tạo các cột cơ bản phục vụ phân tích
        """
        print("\n[9] TAO COT MOI PHUC VU PHAN TICH...")

        if self.df is None:
            print("   CHUA CO DU LIEU")
            return

        created_columns = []

        # Tìm cột số lượng và giá
        quantity_cols = [col for col in self.df.columns
                         if any(keyword in col.lower() for keyword in ['quantity', 'qty', 'sl', 'soluong'])]
        price_cols = [col for col in self.df.columns
                      if any(keyword in col.lower() for keyword in ['price', 'gia', 'unit_price', 'don_gia'])]

        # Tạo cột doanh thu nếu có cả số lượng và giá
        if quantity_cols and price_cols:
            quantity_col = quantity_cols[0]
            price_col = price_cols[0]

            if (self.df[quantity_col].dtype in [np.number, 'int64', 'float64']) and \
                    (self.df[price_col].dtype in [np.number, 'int64', 'float64']):
                self.df['revenue'] = self.df[quantity_col] * self.df[price_col]
                created_columns.append('revenue')
                print(f"   DA TAO COT 'revenue' = {quantity_col} × {price_col}")

        # Tạo cột tổng hợp cho phân tích
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        # Tìm cột có thể là lợi nhuận
        for col in numeric_cols:
            if 'profit' in col.lower() or 'loi_nhuan' in col.lower():
                if 'revenue' in self.df.columns and 'revenue' in created_columns:
                    self.df['profit_margin'] = self.df[col] / self.df['revenue'] * 100
                    created_columns.append('profit_margin')
                    print(f"   DA TAO COT 'profit_margin' (%)")
                break

        # Tạo cột phân loại nếu có cột giá trị
        if 'revenue' in self.df.columns:
            # Phân loại doanh thu
            revenue_median = self.df['revenue'].median()
            self.df['revenue_category'] = np.where(
                self.df['revenue'] > revenue_median, 'High', 'Low'
            )
            created_columns.append('revenue_category')
            print(f"   DA TAO COT 'revenue_category' (nguong: {revenue_median:,.0f})")

        # Tạo cột thời gian tổng hợp nếu có ngày tháng
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            date_col = date_cols[0]
            self.df['month_year'] = self.df[date_col].dt.to_period('M').astype(str)
            created_columns.append('month_year')
            print(f"   DA TAO COT 'month_year' tu {date_col}")

        if created_columns:
            print(f"\n   DA TAO {len(created_columns)} COT MOI:")
            for col in created_columns:
                print(f"     - {col}")
        else:
            print("   KHONG TAO DUOC COT MOI NAO")

    # ==================== PHẦN 5: LƯU VÀ BÁO CÁO ====================

    def save_cleaned_data(self, output_path='output/cleaned_data.csv'):
        """
        Lưu dữ liệu sau làm sạch ra file CSV để dùng cho Pivot / Power BI / phân tích tiếp theo

        Args:
            output_path (str): Đường dẫn file output

        Returns:
            bool: True nếu lưu thành công
        """
        print("\n[10] LUU DU LIEU DA LAM SACH...")

        if self.df is None or self.df.empty:
            print("   KHONG CO DU LIEU DE LUU!")
            return False

        try:
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Lưu file CSV
            self.df.to_csv(output_path, index=False, encoding='utf-8-sig')

            print(f"   DA LUU DU LIEU VAO: {output_path}")
            print(f"   KICH THUOC: {len(self.df)} dong × {len(self.df.columns)} cot")
            print(f"   DUNG LUONG FILE: {os.path.getsize(output_path) / 1024:.1f} KB")

            # Hiển thị thông tin về quá trình làm sạch
            if self.original_shape:
                print(f"\n   SO SANH TRUOC - SAU:")
                print(f"     Dong: {self.original_shape[0]} -> {len(self.df)}")
                print(f"     Cot: {self.original_shape[1]} -> {len(self.df.columns)}")
                print(f"     Giam: {self.original_shape[0] - len(self.df)} dong")

            return True

        except Exception as e:
            print(f"   LOI KHI LUU FILE: {e}")
            return False

    def generate_summary_report(self):
        """
        Tạo báo cáo tổng kết quá trình làm sạch
        """
        print("\n" + "=" * 50)
        print("BAO CAO TONG KET LAM SACH DU LIEU")
        print("=" * 50)

        if self.df is None:
            print("KHONG CO DU LIEU")
            return

        print(f"\nTHONG TIN DU LIEU:")
        print(f"   • So dong: {len(self.df):,}")
        print(f"   • So cot: {len(self.df.columns)}")
        print(f"   • Kieu du lieu:")

        dtype_counts = self.df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"     - {dtype}: {count} cot")

        print(f"\nDU LIEU SO:")
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"   • Co {len(numeric_cols)} cot so")
            for col in numeric_cols[:5]:
                print(f"     - {col}: min={self.df[col].min():,.2f}, max={self.df[col].max():,.2f}")
            if len(numeric_cols) > 5:
                print(f"     ... va {len(numeric_cols) - 5} cot khac")

        print(f"\nDU LIEU NGAY THANG:")
        date_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            for col in date_cols:
                date_range = self.df[col].dropna()
                if len(date_range) > 0:
                    print(f"   • {col}: {date_range.min().date()} den {date_range.max().date()}")

        print(f"\nDU LIEU DA SAN SANG CHO:")
        print(" Phan tich Pivot Table")
        print(" Visualization voi Power BI/Tableau")
        print(" Phan tich thong ke")
        print(" Machine Learning")

    #  PHẦN 6: CHẠY TỰ ĐỘNG

    def run_full_pipeline(self, output_path='output/cleaned_data.csv'):
        """Chạy toàn bộ pipeline làm sạch dữ liệu tự động"""
        print("\n" + "=" * 50)
        print("BAT DAU QUY TRINH LAM SACH DU LIEU")
        print("=" * 50)

        steps = [
            ("DOC DU LIEU", self.load_data),
            ("KHAM PHA DU LIEU", self.explore_data),
            ("CHUAN HOA TEN COT", self.standardize_column_names),
            ("XU LY NGAY THANG", self.convert_date_columns),
            ("CHUYEN DOI COT SO", self.convert_numeric_columns),
            ("XU LY DU LIEU THIEU", lambda: self.handle_missing_values('auto')),
            ("LOAI BO DU LIEU KHONG HOP LE", self.remove_invalid_data),
            ("TAO COT MOI", self.create_basic_columns),
            ("LUU DU LIEU", lambda: self.save_cleaned_data(output_path)),
            ("TAO BAO CAO", self.generate_summary_report)
        ]

        for step_name, step_function in steps:
            print(f"\nBUOC: {step_name}")
            print("-" * 30)
            try:
                step_function()
            except Exception as e:
                print(f"LOI: {e}")
                print("TIEP TUC VOI BUOC TIEP THEO...")

        print("\n" + "=" * 50)
        print("HOAN THANH QUY TRINH LAM SACH!")
        print("=" * 50)


#  PHẦN 7: CHẠY CHƯƠNG TRÌNH


if __name__ == "__main__":
    preprocessor = DataPreprocessor(data_folder='data')
    preprocessor.run_full_pipeline(output_path='output/cleaned_data.csv')