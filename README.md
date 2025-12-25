**Highlands Coffee Business Analysis**

**Mục đích**
Dự án phân tích kết quả kinh doanh của một cửa hàng Highlands Coffee dựa trên dữ liệu bán hàng.
Thông qua quá trình làm sạch – chuẩn hoá – phân tích – trực quan hoá dữ liệu, dự án giúp đánh giá hiệu quả kinh doanh, xu hướng doanh thu và hỗ trợ dự báo kết quả kinh doanh trong thời gian tới.

**Cấu trúc thư mục**
data/
Xử lý dữ liệu gốc, làm sạch và chuẩn hoá dữ liệu
raw/ : Dữ liệu gốc (file Excel/CSV ban đầu)
processed/ : Dữ liệu sau khi làm sạch
data_cleaning.py : Code làm sạch và chuẩn hoá dữ liệu
backend/
Code backend – xử lý logic chính, phân tích, thống kê, dự báo
CRUD dữ liệu
Phân tích kết quả kinh doanh
Dự báo doanh thu
frontend/
Code giao diện  hiển thị dữ liệu và biểu đồ trực quan
powerbi/
File Power BI kết nối với dữ liệu đã làm sạch
Trực quan hoá và dashboard phân tích+  video
docs/
Báo cáo chi tiết, tài liệu mô tả quá trình xử lý dữ liệu và xây dựng ứng dụng
report/
Slide thuyết trình và báo cáo 
README.md
Mô tả chung dự án và phân công công việc

**Phân công công việc**
- Ánh : Code chính 
- Nhi:Làm Sile+ Báo cáo 
- Hân: Phụ trách dữ liệu – chuẩn bị dữ liệu gốc, làm sạch, chuẩn hoá và xuất dữ liệu đầu vào cho hệ thống, báo cáo 
- Hiền: Code giao diện 

**Hướng dẫn nhanh**
Chạy xử lý dữ liệu:
Xem hướng dẫn trong data/data_cleaning.py
Chạy backend:
Xem hướng dẫn trong backend/README_backend.md
Chạy giao diện:
Xem hướng dẫn trong frontend/README_frontend.md
Power BI:
Mở file trong thư mục powerbi/ và kết nối với dữ liệu trong data/processed/
Tài liệu & báo cáo:
Xem trong thư mục docs/ và report/
