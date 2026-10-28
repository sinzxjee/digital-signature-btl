# Ứng dụng chữ ký số – Bài tập lớn

Ứng dụng Python minh họa sinh khóa, ký tệp và xác minh chữ ký số bằng:

- RSA-PSS, khóa 3072 bit, MGF1 và SHA-256.
- ECDSA, đường cong P-256 và SHA-256.

> Chương trình phục vụ học tập. Ứng dụng không tích hợp CA, dấu thời gian hoặc thiết bị bảo vệ khóa nên không tạo chữ ký số có giá trị pháp lý.
## Clone và chạy nhanh

### 1. Clone repository

Trên trang GitHub, chọn **Code → HTTPS** và sao chép URL của repository. Sau đó mở Terminal:

    git clone https://github.com/sinzxjee/digital-signature-btl.git
    cd digital-signature-btl

Thay URL mẫu bằng URL repository thật của nhóm. Nếu repository ở chế độ Private, tài khoản GitHub của người clone phải được thêm vào danh sách Collaborators.

### 2. Tạo và kích hoạt môi trường ảo

Với Windows PowerShell:

    python -m venv .venv
    .venv\Scripts\Activate.ps1

Nếu PowerShell chặn kích hoạt, sử dụng Command Prompt:

    .venv\Scripts\activate.bat

Với macOS hoặc Linux:

    python3 -m venv .venv
    source .venv/bin/activate

### 3. Cài thư viện và chạy

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python app.py

### 4. Chạy kiểm thử

    python -m unittest -v

Repository không chứa khóa bí mật hoặc khóa mẫu. Sau khi clone, người dùng mở chương trình và tự sinh cặp khóa mới để kiểm thử.

## Chức năng

- Sinh cặp khóa công khai và bí mật.
- Mã hóa khóa bí mật bằng mật khẩu.
- Ký mọi loại tệp và lưu chữ ký rời dạng .sig.json.
- Xác minh chữ ký và phát hiện tệp bị chỉnh sửa.
- Giao diện đồ họa Tkinter.
- Kiểm thử tự động cho RSA-PSS và ECDSA.

## Cấu trúc

    digital_signature_btl/
    ├── app.py
    ├── signature_core.py
    ├── test_signature.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Cài đặt trên VS Code

Khuyến nghị Python 3.11 hoặc 3.12. Mở Terminal trong thư mục dự án:

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

Nếu PowerShell chặn kích hoạt, dùng Command Prompt:

    .venv\Scripts\activate.bat

## Chạy chương trình

    python app.py

## Cách sử dụng

### 1. Sinh khóa

1. Chọn RSA-PSS hoặc ECDSA.
2. Chọn thư mục lưu, nên đặt là keys.
3. Nhập mật khẩu bảo vệ khóa bí mật.
4. Nhấn Sinh cặp khóa.

### 2. Ký tệp

1. Chọn tệp cần ký.
2. Chọn khóa bí mật.
3. Chọn nơi lưu tệp .sig.json.
4. Nhập mật khẩu và nhấn Ký tệp.

### 3. Xác minh

1. Chọn tệp gốc.
2. Chọn khóa công khai tương ứng.
3. Chọn tệp .sig.json.
4. Nhấn Xác minh.

Kết quả đúng:

    Chữ ký hợp lệ; tệp còn nguyên vẹn.

Nếu nội dung bị sửa:

    Tệp đã thay đổi: SHA-256 không khớp.

## Kiểm thử tự động

    python -m unittest -v

Kết quả mong đợi:

    test_ecdsa ... ok
    test_rsa ... ok
    Ran 2 tests
    OK

## Ví dụ

Tạo tệp hop_dong.txt:

    HỢP ĐỒNG THANH TOÁN
    Bên A thanh toán cho Bên B số tiền: 10.000.000 VNĐ.
    Thời hạn thanh toán: 30/10/2026.

Sinh khóa, ký và xác minh. Sau đó đổi số tiền thành 90.000.000 VNĐ và xác minh lại bằng chữ ký cũ. Chương trình phải phát hiện tệp đã thay đổi.

## Lưu ý về khóa

- Không tải khóa bí mật lên GitHub.
- Có thể xóa khóa thử nghiệm và sinh khóa mới bất cứ lúc nào.
- Khi sinh khóa mới, chữ ký cũ chỉ xác minh được bằng khóa công khai cũ.
- Thư mục keys và các tệp PEM đã được .gitignore loại trừ.

## Thành viên

| Thành viên | Công việc |
|---|---|
| Bùi Duy Hưng | Cập nhật theo phân công |
| Nguyễn Tuấn Anh | Cập nhật theo phân công |
| Nguyễn Minh Cường | Cập nhật theo phân công |
| Đỗ Yến Nhi | Cập nhật theo phân công |

## Tài liệu tham khảo

- NIST FIPS 186-5.
- RFC 8017, PKCS #1 v2.2.
- William Stallings, Cryptography and Network Security.
- Bruce Schneier, Applied Cryptography.

## Hướng dẫn kiểm thử chi tiết

Trước khi kiểm thử, kích hoạt môi trường ảo và cài thư viện:

    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

### Kiểm thử 1: Chạy bộ kiểm thử tự động

Tại Terminal của VS Code, chạy:

    python -m unittest -v

Kết quả mong đợi:

    test_ecdsa ... ok
    test_rsa ... ok
    Ran 2 tests
    OK

Bộ kiểm thử thực hiện lần lượt việc sinh khóa, ký dữ liệu, xác minh chữ ký hợp lệ, sửa dữ liệu và kiểm tra chương trình phát hiện thay đổi.

### Kiểm thử 2: Ký và xác minh tệp hợp lệ

1. Tạo tệp hop_dong.txt với nội dung:

       HỢP ĐỒNG THANH TOÁN
       Bên A thanh toán cho Bên B số tiền: 10.000.000 VNĐ.
       Thời hạn thanh toán: 30/10/2026.

2. Chạy chương trình:

       python app.py

3. Chọn RSA-PSS 3072.
4. Trong tab Sinh khóa, chọn thư mục keys, nhập mật khẩu 123456 và sinh khóa.
5. Trong tab Ký tệp, chọn:
   - Tệp cần ký: hop_dong.txt
   - Khóa bí mật: keys/rsa_private.pem
   - Tệp chữ ký: hop_dong.sig.json
   - Mật khẩu: 123456
6. Trong tab Xác minh, chọn:
   - Tệp gốc: hop_dong.txt
   - Khóa công khai: keys/rsa_public.pem
   - Tệp chữ ký: hop_dong.sig.json

Kết quả mong đợi:

    Chữ ký hợp lệ; tệp còn nguyên vẹn.

### Kiểm thử 3: Phát hiện tệp bị chỉnh sửa

Sau khi hoàn thành kiểm thử 2, sửa nội dung hop_dong.txt:

    Bên A thanh toán cho Bên B số tiền: 90.000.000 VNĐ.

Giữ nguyên khóa công khai và tệp chữ ký cũ, sau đó xác minh lại.

Kết quả mong đợi:

    Tệp đã thay đổi: SHA-256 không khớp.

Điều này chứng minh chương trình phát hiện được nội dung đã thay đổi sau thời điểm ký.

### Kiểm thử 4: Sử dụng sai khóa công khai

1. Khôi phục hop_dong.txt về đúng nội dung lúc ký.
2. Sinh một cặp khóa RSA khác trong thư mục keys_khac.
3. Chọn keys_khac/rsa_public.pem để xác minh chữ ký cũ.

Kết quả mong đợi:

    Chữ ký sai hoặc khóa không tương ứng.

Điều này minh họa chữ ký chỉ xác minh được bằng khóa công khai thuộc cùng cặp khóa với khóa bí mật đã dùng để ký.

### Kiểm thử 5: Sai mật khẩu khóa bí mật

Trong tab Ký tệp, chọn đúng khóa bí mật nhưng nhập mật khẩu khác mật khẩu đã đặt khi sinh khóa.

Kết quả mong đợi: chương trình hiển thị thông báo lỗi và không tạo chữ ký.

### Kiểm thử 6: Thực hiện với ECDSA

1. Chọn ECDSA P-256.
2. Sinh khóa trong thư mục keys_ecdsa.
3. Ký và xác minh tệp giống kiểm thử 2.
4. Sửa tệp rồi xác minh lại giống kiểm thử 3.

Kết quả mong đợi lần đầu là chữ ký hợp lệ; sau khi sửa tệp, chương trình phát hiện SHA-256 không khớp.

### Bảng tổng hợp kết quả

| Mã | Trường hợp | Kết quả mong đợi |
|---|---|---|
| TC01 | Đúng tệp, chữ ký và khóa RSA | Hợp lệ |
| TC02 | Tệp bị sửa sau khi ký | Không hợp lệ – SHA-256 không khớp |
| TC03 | Dùng khóa công khai RSA khác | Không hợp lệ – khóa không tương ứng |
| TC04 | Nhập sai mật khẩu khóa bí mật | Không tạo được chữ ký |
| TC05 | Đúng tệp, chữ ký và khóa ECDSA | Hợp lệ |
| TC06 | Tệp ECDSA bị sửa sau khi ký | Không hợp lệ – SHA-256 không khớp |

Nhóm có thể chụp màn hình kết quả của TC01, TC02, TC03 và TC05 để đưa vào chương kiểm thử của báo cáo.


