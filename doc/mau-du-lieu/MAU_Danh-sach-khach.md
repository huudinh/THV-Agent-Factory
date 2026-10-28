# MẪU — BẢNG DANH SÁCH KHÁCH (đầu vào riêng của R6)

> **Dữ liệu mô phỏng.** Mọi dòng dưới đây do bịa ra để minh hoạ định dạng. **Không phải người bệnh thật của Tiêu Hóa Việt.**

> 🔒 Bảng danh sách khách thật là **dữ liệu sức khỏe**: nó gắn chẩn đoán với tên tuổi địa chỉ. Chạy trên máy nội bộ. R6 cố tình **không in tên khách** ở sheet dữ liệu và **không in chẩn đoán chi tiết** — chỉ in mã nhóm.

---

## Cột cần có

| Cột | Bắt buộc | Dùng để |
|---|---|---|
| `Mã khách` hoặc `STT` | ✅ | Thay cho tên ở file đầu ra |
| `Năm sinh` **hoặc** `Tuổi` | ✅ | Chia nhóm tuổi — trục quan trọng nhất |
| `Giới tính` | nên có | Khác biệt rõ ở một số nhóm bệnh |
| `Khu vực` (quận / tỉnh) | nên có | Đo bán kính thật của khách quanh 139 Đại La |
| `Tình trạng` | nên có | Đã khám / đã soi / hẹn lại / huỷ hẹn |
| `Vấn đề` (triệu chứng hoặc chẩn đoán) | ✅ | Gán nhóm `TH-01…TH-12` |
| `Dịch vụ đã sử dụng` | ✅ | Gán nhóm giá trị `G1/G2/G3` |
| `Lần soi thứ mấy` | nên có | Đo vòng tái soi |
| `Ngày hẹn soi lại` | nên có | ⭐ Sheet tệp giá trị dài hạn lớn nhất |

---

## Bảng mẫu

| Mã KH | Năm sinh | Giới | Khu vực | Tình trạng | Vấn đề | Dịch vụ đã sử dụng | Lần soi | Ngày hẹn soi lại |
|---|---|---|---|---|---|---|---|---|
| KH001 | 1978 | Nữ | Hoàng Mai, HN | Đã soi | Viêm hang vị, HP dương | Nội soi dạ dày + test HP | 1 | 12/2026 |
| KH002 | 1965 | Nam | Hưng Yên | Đã soi | Polyp đại tràng, đã cắt | Nội soi đại tràng tiền mê + cắt polyp | 1 | 06/2028 |
| KH003 | 1990 | Nữ | Thanh Xuân, HN | Đã khám | Trào ngược | Khám chuyên khoa | 0 | |
| KH004 | 1958 | Nam | Thanh Hóa | Đã soi | Loét dạ dày | Combo dạ dày + đại tràng tiền mê | 1 | 10/2027 |
| KH005 | 1982 | Nữ | Hai Bà Trưng, HN | Đã soi | Hội chứng ruột kích thích | Nội soi đại tràng | 2 | |
| KH006 | 1971 | Nam | Bắc Ninh | Huỷ hẹn | Đau thượng vị | — | 0 | |
| KH007 | 1995 | Nữ | Đống Đa, HN | Đã khám | Trĩ độ 1 | Nội soi trực tràng | 1 | |
| KH008 | 1960 | Nam | Hoàng Mai, HN | Đã soi | Barrett thực quản | Nội soi dạ dày tiền mê + sinh thiết | 3 | 04/2027 |
| KH009 | 1987 | Nữ | Hà Đông, HN | Đã soi | Không phát hiện bất thường | Combo dạ dày + đại tràng | 1 | 01/2029 |
| KH010 | 1953 | Nam | Hà Nam | Đã khám | Men gan cao, gan nhiễm mỡ | Khám + siêu âm | 0 | |

---

## Bốn điều hay làm hỏng bảng khách

### ① Gộp ô, nhiều dòng tiêu đề, hàng tổng ở giữa bảng
Trợ lý đọc lệch. Để bảng **phẳng**: một dòng tiêu đề, không gộp ô, không hàng tổng chen vào giữa.

### ② Cột "Tình trạng" mỗi hệ ghi một kiểu
Có hệ ghi trạng thái **hồ sơ** (mới / đang xử lý / đã xong), có hệ ghi trạng thái **lịch hẹn** (đã hẹn / đã đến / huỷ), có hệ ghi trạng thái **điều trị**. Trợ lý sẽ nói rõ ở DỪNG 1 là nó hiểu theo loại nào — **sửa ở đó**, rẻ hơn sửa sau khi đã dựng xong 6 sheet.

### ③ Lẫn chẩn đoán với triệu chứng
Trong bảng mẫu trên, cột `Vấn đề` là **chẩn đoán sau khi soi** — không phải điều khách kể lúc inbox. Hai thứ này khác nhau:

| | R1 đếm gì | R6 đếm gì |
|---|---|---|
| Nguồn | Hội thoại Fanpage | Hồ sơ phòng khám |
| Cột vấn đề là | **Khách nói gì** | **Bác sĩ kết luận gì** |

Hai con số không khớp nhau là **bình thường**, và chính khoảng lệch đó nói lên nội dung nào đang kéo sai người. Nhưng phải biết mình đang đọc cái nào — nói trước cho trợ lý.

### ④ Thiếu cột "Ngày hẹn soi lại"
Mất sheet **Vòng tái soi** — tệp giá trị dài hạn lớn nhất của THV, vì nhóm này không cần tạo nhu cầu: mốc hẹn đã nằm trong phiếu kết quả của chính khách.

Nếu mốc hẹn nằm trong ghi chú tự do thay vì một cột riêng, nói trước để trợ lý biết tìm ở đâu. Nếu hồ sơ chưa ghi mốc này ở đâu cả → đó là **đề nghị dữ liệu quan trọng nhất** mà R6 sẽ nêu ra.

---

## ⚠ Giới hạn của R6 với bảng này

- ⛔ **Không chấm độ nóng, không chấm 5 tín hiệu, không viết kịch bản nhắn lại** từ bảng khách. Bảng này không có nội dung tin nhắn. Ai cần những thứ đó thì chạy R1.
- ⛔ **Không tự tính "đã quá hạn soi lại"** cho từng người. Chu kỳ tái soi là **chỉ định y khoa của bác sĩ cho từng ca**; R6 chỉ đếm theo mốc đã ghi trong hồ sơ.
- ⛔ **Ô bảng chéo dưới 5 người thì không in số chính xác** — ô quá nhỏ có thể nhận ra người cụ thể.
- Rào cản và câu hỏi ngầm ở sheet Chân dung là **suy luận từ nhóm** theo `P2`, không phải đo từ bảng này. R6 ghi rõ điều đó ngay dưới tiêu đề sheet.
