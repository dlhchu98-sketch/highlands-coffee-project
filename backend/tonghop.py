"""TỔNG HỢP - PHÂN TÍCH 5 BẢNG DỮ LIỆU"""

import os
import time


def main():
    print("=" * 70)
    print("DASHBOARD PHÂN TÍCH DỮ LIỆU BÁN HÀNG")
    print("Tất cả dữ liệu được đọc từ file: output/cleaned_data.csv")
    print("=" * 70)

    # Tạo thư mục lưu trữ
    directories = ['visualizations', 'reports', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Đã tạo thư mục: {directory}/")

    print("\n" + "=" * 70)
    print("BẮT ĐẦU PHÂN TÍCH...")
    print("=" * 70)

    # Kiểm tra file dữ liệu
    data_file = 'output/cleaned_data.csv'
    if not os.path.exists(data_file):
        print(f"LỖI: Không tìm thấy file dữ liệu: {data_file}")
        print("Vui lòng chạy data_preprocess.py trước để tạo file cleaned_data.csv")
        return

    print(f"Đã tìm thấy file dữ liệu: {data_file}")
    print(f"Kích thước: {os.path.getsize(data_file) / 1024:.1f} KB")

    # Menu chọn bảng để phân tích
    print("\nCHỌN BẢNG ĐỂ PHÂN TÍCH:")
    print("-" * 50)
    print("1. Bảng 1 - Tỷ trọng số lượng sản phẩm")
    print("2. Bảng 2 - Doanh thu theo kênh")
    print("3. Bảng 3 - Xu hướng doanh thu theo thời gian")
    print("4. Bảng 4 - Top nhân viên xuất sắc")
    print("5. Bảng 5 - Tỷ trọng kích cỡ sản phẩm")
    print("6. Phân tích TẤT CẢ bảng")
    print("0. Thoát")
    print("-" * 50)

    choice = input("Nhập lựa chọn (0-6): ").strip()

    if choice == '0':
        print("Kết thúc chương trình!")
        return

    elif choice == '1':
        print("\n" + "=" * 60)
        print("BẮT ĐẦU PHÂN TÍCH BẢNG 1...")
        print("=" * 60)
        from Product_Quantity_Analyzer import ProductQuantityAnalyzer
        analyzer = ProductQuantityAnalyzer(data_path=data_file)
        analyzer.run_analysis()

    elif choice == '2':
        print("\n" + "=" * 60)
        print("BẮT ĐẦU PHÂN TÍCH BẢNG 2...")
        print("=" * 60)
        from Channel_Revenue_Analyzer import ChannelRevenueAnalyzer
        analyzer = ChannelRevenueAnalyzer(data_path=data_file)
        analyzer.run_analysis()

    elif choice == '3':
        print("\n" + "=" * 60)
        print("BẮT ĐẦU PHÂN TÍCH BẢNG 3...")
        print("=" * 60)
        from Revenue_Trend_Analyzer import RevenueTrendAnalyzer
        analyzer = RevenueTrendAnalyzer(data_path=data_file)
        analyzer.run_analysis()

    elif choice == '4':
        print("\n" + "=" * 60)
        print("BẮT ĐẦU PHÂN TÍCH BẢNG 4...")
        print("=" * 60)
        from Top_Staff_Analyzer import TopStaffAnalyzer
        analyzer = TopStaffAnalyzer(data_path=data_file, show_top=10)
        analyzer.run_analysis()

    elif choice == '5':
        print("\n" + "=" * 60)
        print("BẮT ĐẦU PHÂN TÍCH BẢNG 5...")
        print("=" * 60)
        from Product_Size_Analyzer import ProductSizeAnalyzer
        analyzer = ProductSizeAnalyzer(data_path=data_file)
        analyzer.run_analysis()

    elif choice == '6':
        print("\n" + "=" * 60)
        print("BẮT ĐẦU PHÂN TÍCH TẤT CẢ 5 BẢNG...")
        print("=" * 60)

        analyzers = [
            ('Bảng 1', 'product_quantity', 'ProductQuantityAnalyzer', {'data_path': data_file}),
            ('Bảng 2', 'channel_revenue', 'ChannelRevenueAnalyzer', {'data_path': data_file}),
            ('Bảng 3', 'revenue_trend', 'RevenueTrendAnalyzer', {'data_path': data_file}),
            ('Bảng 4', 'top_staff', 'TopStaffAnalyzer', {'data_path': data_file, 'show_top': 10}),
            ('Bảng 5', 'product_size', 'ProductSizeAnalyzer', {'data_path': data_file})
        ]

        for name, module_name, class_name, kwargs in analyzers:
            print(f"\nĐang phân tích {name}...")
            print("-" * 50)

            try:
                module = __import__(module_name)
                analyzer_class = getattr(module, class_name)
                analyzer = analyzer_class(**kwargs)

                if name == 'Bảng 4':
                    analyzer.run_analysis()
                else:
                    analyzer.run_analysis()

                print(f"Hoàn thành phân tích {name}")
                time.sleep(1)

            except Exception as e:
                print(f"Lỗi khi phân tích {name}: {e}")
                continue

        print("\n" + "=" * 60)
        print("ĐÃ HOÀN THÀNH PHÂN TÍCH TẤT CẢ 5 BẢNG!")
        print("=" * 60)
        print("\nCÁC BIỂU ĐỒ ĐÃ ĐƯỢC LƯU TRONG THƯ MỤC 'visualizations/'")

    else:
        print("Lựa chọn không hợp lệ!")

    print("\n" + "=" * 70)
    print("CHƯƠNG TRÌNH KẾT THÚC")
    print("=" * 70)


if __name__ == "__main__":
    main()