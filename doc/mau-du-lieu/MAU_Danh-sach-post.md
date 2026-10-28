# MẪU — DANH SÁCH POST QUẢNG CÁO (đầu vào của R2)

> **Dữ liệu mô phỏng.** Tên post và nội dung do bịa ra để minh hoạ định dạng, không phải chiến dịch thật của Tiêu Hóa Việt.

---

## Cần tối thiểu bốn cột

`Mã post` · `Tên post đúng như trong thẻ` · `Thông điệp chính` · `Thời gian chạy`

Có thêm `Góc tiếp cận` và `Dịch vụ` thì trợ lý khỏi phải suy. Chi phí quảng cáo **không bắt buộc** — R2 đo chất lượng khách kéo về, không đo chi phí.

---

## Bảng mẫu

| Mã post | Tên post đúng như trong thẻ | Thông điệp chính | Góc tiếp cận | Dịch vụ | Thời gian chạy | Biến thể đã gom |
|---|---|---|---|---|---|---|
| P01 | QC_SoiDaDay_TienMe | Nội soi dạ dày không đau, hệ Fujifilm tích hợp AI | Soi không đau / tiền mê | Nội soi dạ dày | 01–31/10 | `- Bản sao`, `_V2` |
| P02 | QC_SoiDaiTrang_TienMe | Nội soi đại tràng không đau | Soi không đau / tiền mê | Nội soi đại tràng | 01–31/10 | — |
| P03 | QC_BangGia_Banner | Bảng giá nội soi công khai, không phát sinh | Giá & điều kiện | Tổng quát | 05–31/10 | `_Group_1` |
| P04 | QC_TamSoat_Combo | Tầm soát dạ dày và đại tràng trong một lần, ngoài 40 nên kiểm tra | Tầm soát & phòng xa | Combo | 01–31/10 | — |
| P05 | QC_TamSoat_UngThu | Ung thư tiêu hóa phát hiện sớm điều trị được | Tầm soát & phòng xa | Combo | 10–31/10 | — |
| P06 | QC_BacSi_BachMai | Chuyên gia tiêu hóa từ Bệnh viện Bạch Mai | Chuyên môn bác sĩ | Tổng quát | 01–31/10 | — |
| P07 | QC_TrieuChung_DaDay | Đau bụng kéo dài, khi nào cần nội soi | Triệu chứng cụ thể | Nội soi dạ dày | 03–31/10 | — |
| P08 | QC_TrieuChung_DaiTrang | Táo bón kéo dài, khi nào cần soi đại tràng | Triệu chứng cụ thể | Nội soi đại tràng | 03–31/10 | — |
| P09 | QC_ChuNhat_Banner | Phòng khám làm cả Chủ nhật, 7h–17h | Banner thông báo | Tổng quát | 01–31/10 | — |
| P10 | QC_MayAI_Fujifilm | Hệ nội soi Fujifilm VP-7000 tích hợp AI, chế độ BLI/LCI | Công nghệ máy & AI | Tổng quát | 15–31/10 | — |

---

## Ba điều hay làm hỏng bảng post

### ① Không gom bản sao
Post bị nhân bản với hậu tố `- Bản sao`, `_Group_1`, `_V2`, `_Copy`. Để rời thì mỗi bản chỉ còn 3–4 hội thoại, **không bản nào đủ 10 ca để xếp hạng** — và báo cáo trả về toàn `⚠ chưa đủ mẫu`.

→ Gom về một mã, ghi rõ ở cột *Biến thể đã gom*.

### ② Tên post trong bảng khác tên trong thẻ hội thoại
Thẻ là **khoá nối** giữa post và hội thoại. Lệch một chữ là không nối được.

→ Mở một hội thoại có thẻ, copy **nguyên văn** phần sau chữ *"Inbox từ quảng cáo"*, dán vào cột *Tên post đúng như trong thẻ*.

### ③ Để trống cột Góc tiếp cận
Không sao — trợ lý tự suy từ thông điệp. Nhưng nếu bạn điền thì bảng *Góc tiếp cận → tầng* chính xác hơn, và đó là bảng dùng để chọn góc khi viết content mới.

**Tám góc tiếp cận của THV:** Giá & điều kiện · Soi không đau/tiền mê · Triệu chứng cụ thể · Tầm soát & phòng xa · Chuyên môn bác sĩ – chuyên gia Bạch Mai · Công nghệ máy & AI · Banner thông báo/lịch làm việc · Gói cho người nhà – doanh nghiệp.

---

## ⚠ Hai post trong bảng mẫu cố tình đặt cạnh nhau để đối chiếu

`P04 QC_TamSoat_Combo` và `P05 QC_TamSoat_UngThu` cùng nhắm nhóm tầm soát, nhưng khác hẳn về cách nói: một cái nói *"ngoài 40 nên kiểm tra"*, một cái nói *"ung thư phát hiện sớm điều trị được"*.

Khi chạy R2, **so riêng hai post này**. Giả thuyết cần kiểm trong dữ liệu thật: post nghiêng về hù bệnh thường kéo nhiều inbox hơn nhưng đẻ ra nhiều `L6.8` (né kết quả) hơn, và tỷ lệ đặt lịch thấp hơn. Nếu dữ liệu cho thấy vậy thì đó là phát hiện đáng đưa lên đầu báo cáo — xem [`reports/R2`](../../reports/R2-phan-tang-quang-cao.md) sheet 8.
