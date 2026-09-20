# Student Tracker - Quản lý học sinh và xếp loại
Sản phẩm Python của ứng viên Nguyễn Lê Minh cho thử thách ứng viên TEKY. Chương trình hỗ trợ giáo viên quản lý học sinh, điểm số và xếp loại bằng giao diện Tkinter hoặc menu dòng lệnh.

## Tính năng đã hoàn thành
- [x] Nhập một hoặc nhiều học sinh.
- [x] Lưu tên, tuổi và điểm Toán - Văn - Anh.
- [x] Tính điểm trung bình và xếp loại học lực tự động.
- [x] Hiển thị danh sách tổng hợp theo ID.
- [x] Tìm kiếm gần đúng theo tên, không phân biệt chữ hoa/chữ thường.
- [x] Menu thao tác bằng vòng lặp.
- [x] Thêm, xem, sửa và xóa dữ liệu.
- [x] Giao diện Tkinter.
- [x] Lưu dữ liệu bằng SQLite.
- [x] Tổ chức code theo OOP.
- [ ] Tích hợp API, threading và đóng gói bằng PyInstaller.

## Yêu cầu hệ thống
- Python 3.10 trở lên.
- Tkinter để chạy giao diện đồ họa.
- Không cần cài package Python bên thứ ba.

Trên Ubuntu/Debian, cài Tkinter nếu hệ thống chưa có:
```bash
sudo apt install python3-tk
```

## Chạy dự án
Giao diện Tkinter:
```bash
python3 student_tracker_gui.py
```

Giao diện dòng lệnh:
```bash
python3 student_tracker.py
```

Hai giao diện dùng chung file `students.db`. Mọi thay đổi được lưu tự động và
vẫn còn sau khi đóng chương trình.

## Cấu trúc dự án
```text
teky-python/
├── README.md
├── student_tracker.py
├── student_tracker_gui.py
├── students.db
└── .gitignore
```

- `student_tracker.py`: model `Student`, repository SQLite và giao diện dòng lệnh.
- `student_tracker_gui.py`: giao diện Tkinter dùng chung logic và dữ liệu.
- `students.db`: cơ sở dữ liệu SQLite chứa 40 học sinh mẫu.
- `.gitignore`: loại bỏ cache và bytecode Python khỏi Git.

