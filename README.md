# Age Gender Recognition Project

Dự án nhận diện tuổi và giới tính sử dụng Deep Learning và OpenCV.

## Tính năng
- 🎥 Nhận diện real-time từ webcam
- 📹 Phân tích từ file video  
- 🖼️ Phân tích từ hình ảnh
- 🎯 Hiển thị tuổi và giới tính với độ chính xác cao

## Yêu cầu hệ thống
- Python 3.8 - 3.11
- Windows (khuyến nghị)
- Webcam (tùy chọn)

## Cài đặt

### 1. Clone hoặc tải dự án
```bash
# Giải nén file và di chuyển vào thư mục
cd Age_Gender_Recongnition
```

### 2. Cài đặt thư viện
```bash
# Cách 1: Sử dụng requirements.txt
py -m pip install -r requirements.txt

# Cách 2: Cài đặt thủ công
py -m pip install --upgrade pip setuptools wheel
py -m pip install opencv-python numpy Pillow
```

### 3. Chạy chương trình
```bash
py main.py
```

## Sử dụng
1. Chọn một trong 3 tùy chọn:
   - **Webcam**: Nhận diện real-time
   - **Video**: Chọn file video để phân tích
   - **Image**: Chọn hình ảnh để phân tích

2. **Lưu ý**: Khi sử dụng Webcam/Video, nhấn `ESC` để dừng

## Phím tắt
- `W`: Mở webcam
- `V`: Chọn video
- `I`: Chọn hình ảnh
- `ESC`: Dừng webcam/video

## Khắc phục lỗi

### Python không tìm thấy
```bash
# Sử dụng py thay vì python
py --version
```

### Lỗi thư viện
```bash
# Cài đặt lại thư viện
py -m pip uninstall opencv-python numpy Pillow
py -m pip install opencv-python numpy Pillow --no-cache-dir
```

## Cấu trúc file
- `main.py`: File chính
- `*.prototxt`, `*.caffemodel`: Mô hình AI
- `hinhanh_videos/`: Assets giao diện
- `requirements.txt`: Danh sách thư viện

## Công nghệ sử dụng
- **OpenCV**: Computer Vision
- **Deep Learning**: Nhận diện khuôn mặt, tuổi, giới tính  
- **Tkinter**: Giao diện người dùng
- **NumPy**: Xử lý dữ liệu
- **PIL**: Xử lý hình ảnh

---
Phát triển bởi: [Syntax Ngo]
