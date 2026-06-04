# Ứng Dụng Mã Hóa - Playfair & RSA

## Thông Tin Đồ Án
- **Tên đồ án:** Ứng dụng Mã Hóa (Playfair Cipher & RSA Encryption)
- **Môn học:** NT101.Q21 - An Toàn Mạng Máy Tính
- **Lớp:** NT101.Q21
- **Năm học:** Học kỳ II - 2025 - 2026

## Thành Viên Nhóm
- Thành viên 1: Võ Minh Đức
- Thành viên 2: Ngô Văn Dũng
- Thành viên 3: Trần Minh Dứcd

## Mô Tả Đồ Án
Ứng dụng này thực hiện các thuật toán mã hóa phổ biến trong lĩnh vực bảo mật thông tin:

### Tính Năng Chính
1. **Mã Hóa Playfair (Playfair Cipher)**
   - Thuật toán mã hóa cổ điển dựa trên ma trận 5x5
   - Mã hóa và giải mã text
   - Xử lý khóa tùy chỉnh

2. **Mã Hóa RSA (RSA Encryption)**
   - Thuật toán mã hóa công khai (Public Key Cryptography)
   - Tạo khóa công khai và khóa bí mật
   - Mã hóa và giải mã thông điệp
   - Chữ ký số

## Cấu Trúc Dự Án
```
DoAnATMMT/
├── README.md                 # Tệp hướng dẫn
├── AppDoAn/
│   ├── crypto_app.py        # Ứng dụng chính
│   ├── crypto_app.spec      # Cấu hình PyInstaller
│   └── build/               # Thư mục build
```

## Hướng Dẫn Sử Dụng

### Yêu Cầu
- Python 3.7 trở lên
- Các thư viện: `tkinter` (GUI)

### Cài Đặt
```bash
cd AppDoAn
python crypto_app.py
```

### Chức Năng Chính
1. **Chọn thuật toán mã hóa:** Playfair hoặc RSA
2. **Nhập văn bản:** Nhập thông điệp cần mã hóa
3. **Nhập khóa:** Nhập khóa mã hóa phù hợp
4. **Mã hóa/Giải mã:** Thực hiện các thao tác mã hóa
5. **Xem kết quả:** Hiển thị kết quả đã mã hóa

## Ghi Chú
- Ứng dụng sử dụng giao diện GUI để dễ sử dụng
- Hỗ trợ cả tiếng Việt và tiếng Anh
- Đảm bảo tính bảo mật cơ bản cho học tập

## Giáo Viên Hướng Dẫn
- Giáo viên: Tô Nguyễn Nhật Quang

---
**Lần cập nhật cuối:** 2026-06-04