#%%
import pandas as pd
import os

def preprocess_data(input_path='data.csv',
                    output_path='output/data_1.csv'):

    # 1. Đọc dữ liệu gốc
    df = pd.read_csv(input_path, sep=';', encoding='utf-8')
    print(f"Đã tải {len(df)} bản ghi")

    # 2. Chuẩn hóa tên cột
    df.columns = df.columns.str.strip()
    df.rename(columns={
        'Oder_chanel': 'Order_Channel',
        'Product Name': 'Product_Name',
        'Actual Selling Price': 'Actual_Selling_Price'
    }, inplace=True)

    # 3. Chuẩn hóa cột ngày
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # 4. Chuẩn hóa dữ liệu số
    for col in ['Quantity', 'Actual_Selling_Price', 'Revenue']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 5. Chuẩn hóa chuỗi
    df['Product_Name'] = df['Product_Name'].str.strip()
    df['Order_Channel'] = df['Order_Channel'].str.title().str.strip()

    # 6. Tính Revenue nếu thiếu
    df['Revenue'] = df['Revenue'].fillna(
        df['Quantity'] * df['Actual_Selling_Price']
    )

    # 7. Loại bỏ dòng thiếu dữ liệu quan trọng
    df.dropna(subset=['Product_Name', 'Quantity', 'Revenue'], inplace=True)

    # 8. Lưu file CSV chuẩn Excel
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(
        output_path,
        sep=';',
        index=False,
        encoding='utf-8-sig'
    )

    # 9. Thống kê nhanh
    print("Số bản ghi:", len(df))
    print("Số sản phẩm:", df['Product_Name'].nunique())
    print("Tổng doanh thu:", f"{df['Revenue'].sum():,.0f}")

    return df


if __name__ == "__main__":
    preprocess_data()
#%%
