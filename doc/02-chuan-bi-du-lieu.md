# 02 · CHUẨN BỊ DỮ LIỆU — lấy số liệu đầu vào ở đâu

Trợ lý chỉ đọc file bạn đưa. File đúng thì báo cáo đúng; file đã bị lọc thì **mọi con số đều lệch theo cùng một hướng** và không ai phát hiện ra.

---

# 1. Báo cáo nào cần dữ liệu gì

| Báo cáo | Cần có | Không có thì |
|---|---|---|
| **R1** phân loại & kịch bản | File hội thoại | Không chạy được |
| **R2** phân tầng post | Danh sách post **+** hội thoại cùng kỳ | Chỉ ra bản dự đoán, ghi rõ là giả thuyết |
| **R3** chất lượng tư vấn | Hội thoại **có dấu thời gian từng tin** + **tên người phụ trách** | Thiếu dấu thời gian → mất tiêu chí ①; thiếu tên NV → không ra được sheet theo người |
| **R4** điều hành | Hội thoại + **số đặt lịch / đến khám / soi được** | Thiếu ba số cuối → phễu dừng ở "có SĐT", ghi `⚠ chưa đo được` |
| **R5** so hai kỳ | Dữ liệu 2 kỳ **cùng cách lấy mẫu** | Khác cách lấy mẫu → **không so được**, báo cáo tự dừng |
| **R6** chân dung khách | **Bảng danh sách khách** (nguồn khác hẳn) | Không chạy được |
| **W1** kho câu hỏi | File hội thoại (+ danh sách URL) | Thiếu URL → mất cột "web đã có bài chưa" |
| **W2** rà soát web | Danh sách URL **+ nội dung bài** | Chỉ có URL → chỉ rà được tiêu đề, phần lớn là `⚠ chưa rà được` |
| **W3** bản đồ cụm | Kết quả W1 (+ W2) | Thiếu W2 → mất phần sửa bài cũ, là phần đáng làm trước nhất |

---

# 2. ⚠ LUẬT QUAN TRỌNG NHẤT: XUẤT TOÀN BỘ, KHÔNG LỌC

Khi xuất hội thoại, **đừng lọc**. Cụ thể là đừng làm ba việc sau:

| Đừng làm | Vì sao |
|---|---|
| Lọc "chỉ hội thoại dài" | Hội thoại dài = khách tương tác nhiều = **đã thiên về phía nóng**. Mọi post sẽ trông tốt hơn thực tế, và **tốt không đều nhau** → so sánh post thành vô nghĩa |
| Lọc "chỉ hội thoại có số điện thoại" | Bỏ mất toàn bộ nhóm chưa cho số — mà đó chính là nhóm cần đọc để biết khâu xin số hổng ở đâu |
| Bỏ hội thoại một dòng | Nghe như rác, nhưng đó là nhóm `TH-12` và `L1.1`, và tỷ lệ của nó là một chỉ số thật |

**Nếu buộc phải lọc** (ví dụ hệ CRM chỉ cho xuất 500 dòng): nói rõ với trợ lý đã lọc theo tiêu chí gì. Nó sẽ gắn cảnh báo lên sheet đầu và **không dùng số đó để khuyến nghị ngân sách**.

> 🚩 **Riêng ngành này có thêm một lý do không được lọc:** hội thoại bị lọc ra có thể chứa **ca cờ đỏ**. Một khách gõ đúng một dòng *"em đi ngoài phân đen 3 hôm nay"* rồi không nhắn nữa là hội thoại ngắn nhất file — và là ca quan trọng nhất file.

---

# 3. Xuất hội thoại — ba cách

## Cách A · Từ CRM — tốt nhất
Xuất theo khoảng thời gian, lấy đủ các cột:
`Tên khách` · `Thời gian từng tin` · `Nội dung tin` · `Ai gửi (KH/NV)` · `Tên nhân viên phụ trách` · `Có SĐT hay không` · `Thẻ nguồn / chiến dịch`
Thiếu **thẻ nguồn** → không chạy được R2 chế độ đo thật.
Thiếu **thời gian từng tin** → mất tiêu chí ① của R3.

## Cách B · Từ Meta Business Suite
Hộp thư → chọn khoảng thời gian → xuất. Bản này thường **không có tên nhân viên** và **không có thẻ chiến dịch** → chạy được R1 và W1, khó chạy R2/R3.

## Cách C · Dán trực tiếp vào chat
Với lô nhỏ (dưới 30 hội thoại) thì copy từ CRM dán thẳng vào chat cũng được. Trợ lý tự nhận dạng cấu trúc, không cần chỉnh.

---

# 4. Định dạng chuẩn — nếu muốn chỉnh file cho chuẩn

Không bắt buộc. Trợ lý đọc được file lệch chuẩn. Nhưng nếu chỉnh được về dạng này thì script trong [`tools/`](../tools/) đọc được luôn:

```
## 1. Nguyễn Thị A — 03/10 09:12
- Phụ trách: Trần Thu · Có SĐT: Có · Số tin: 10
- **03/10 09:12 KH:** [Thẻ: Inbox từ quảng cáo QC_SoiDaDay_TienMe – Nội soi dạ dày không đau]
- **03/10 09:12 KH:** em bị đau thượng vị 3 tháng nay
- **03/10 09:13 NV (Trần Thu):** Dạ chào chị, em là Thu...
```

Xem bản đầy đủ ở [`mau-du-lieu/MAU_Hoi-thoai.md`](mau-du-lieu/MAU_Hoi-thoai.md).

---

# 5. Danh sách post quảng cáo — cho R2

Tối thiểu cần: `Mã/tên post` · `Nội dung chính (headline)` · `Dịch vụ` · `Thời gian chạy`.
Có thêm chi phí thì tốt, nhưng không bắt buộc — R2 đo **chất lượng khách kéo về**, không đo chi phí.

**Lấy "tên post đúng như trong thẻ" ở đâu:** mở một hội thoại có thẻ nguồn, copy nguyên văn phần sau chữ *"Inbox từ quảng cáo"*. Đó là khoá nối giữa post và hội thoại.

**Gom bản sao về post gốc:** post hay bị nhân bản với hậu tố `- Bản sao`, `_Group_1`, `_V2`. Gom chúng về một mã post, và **nói rõ đã gom những gì** — nếu không, mỗi bản sao chỉ còn 3–4 hội thoại và không bản nào đủ mẫu để xếp hạng.

Mẫu điền sẵn: [`mau-du-lieu/MAU_Danh-sach-post.md`](mau-du-lieu/MAU_Danh-sach-post.md).

---

# 6. Số liệu phễu — cho R4

Phễu của THV có **ba con số ở cuối**, và chúng khác nhau:

| Số cần | Lấy ở đâu | Nếu thiếu |
|---|---|---|
| Số **đặt lịch** trong kỳ | Sổ lịch hẹn / CRM | Phễu dừng ở "kết nối" |
| Số **đến khám** (show-up) | Lễ tân | `⚠ chưa đo được show-up` |
| Số **thực hiện được nội soi** ⭐ | Phòng nội soi / sổ ca | `⚠ chưa đo được` — mất **mốc rò nặng nhất** |
| **Lý do hoãn tại chỗ** ⭐⭐ | Lễ tân ghi tay | Mất sheet đáng tiền nhất của R4 |

> ### ⭐⭐ Một việc nhỏ đáng làm nhất trong cả tài liệu này
> Nhờ lễ tân ghi **một dòng** cho mỗi ca đến khám mà **không soi được**, chọn một trong sáu lý do:
> *nhịn ăn chưa đủ giờ · ruột chưa sạch · không đủ điều kiện tiền mê · không có người đưa về · đến rồi không dám soi · lý do khác.*
>
> Mất vài giây mỗi ca. Đổi lại, R4 chỉ ra được **chỗ mất tiền nhiều nhất của phòng khám** — và phần lớn các dòng sẽ trỏ về khâu dặn dò, tức là **sửa được bằng một tin nhắn mẫu**, không cần thêm người, không cần thêm ngân sách.

Có thêm số **đến hẹn soi lại** và **số đã được nhắc** thì R4 đo được cả vòng LTV.

---

# 7. Bảng danh sách khách — đầu vào riêng của R6

Nguồn khác hẳn hội thoại: đây là **hồ sơ người đã đến phòng khám**.

Cột cần có: `Năm sinh hoặc tuổi` (bắt buộc) · `Giới tính` · `Khu vực/địa chỉ` · `Tình trạng hồ sơ` · `Vấn đề/triệu chứng/chẩn đoán` (bắt buộc) · `Dịch vụ đã sử dụng` (bắt buộc) · `Lần soi thứ mấy` · `Ngày hẹn soi lại`.

### Bốn điều hay làm hỏng bảng khách
1. **Gộp ô, nhiều dòng tiêu đề, hàng tổng ở giữa bảng** → trợ lý đọc lệch. Để bảng phẳng, một dòng tiêu đề.
2. **Cột "Tình trạng" mỗi hệ ghi một kiểu** (trạng thái hồ sơ / trạng thái lịch hẹn / trạng thái điều trị). Trợ lý sẽ hỏi lại ở DỪNG 1 — trả lời đúng ở đó rẻ hơn sửa sau.
3. **Lẫn chẩn đoán với triệu chứng.** Cột "Vấn đề" trong hồ sơ thường là **chẩn đoán sau khi soi**, không phải điều khách kể lúc inbox. Nói rõ cột đó là loại nào.
4. **Thiếu cột "ngày hẹn soi lại"** → mất sheet Vòng tái soi, là tệp giá trị dài hạn lớn nhất. Nếu hồ sơ có mốc hẹn mà nằm trong ghi chú tự do thì nói trước để trợ lý biết tìm ở đâu.

Mẫu: [`mau-du-lieu/MAU_Danh-sach-khach.md`](mau-du-lieu/MAU_Danh-sach-khach.md).

---

# 8. Danh sách URL — cho W1 và W2

Xuất từ `tieuhoaviet.com.vn/sitemap.xml`, hoặc từ danh sách bài trong WordPress.
Tối thiểu: `URL` · `Tiêu đề`. Có thêm `ngày cập nhật` và `tác giả` thì W2 rà được tiêu chí byline và ngày cập nhật mà không cần mở từng bài.

**Chạy W2 theo lô, đừng chạy cả site một lần.** Thứ tự nên rà: cụm **Giá & điều kiện** → cụm **Triệu chứng → có cần soi** → cụm **điều trị / HP** → còn lại.

---

# 9. Danh sách kiểm trước khi đưa cho trợ lý

- [ ] File hội thoại là **toàn bộ kỳ**, không lọc theo độ dài hay theo có số
- [ ] Có **dấu thời gian** từng tin (cần cho R3)
- [ ] Có **tên người phụ trách** (cần cho R3)
- [ ] Có **thẻ nguồn / chiến dịch** (cần cho R2)
- [ ] Biết rõ **khoảng thời gian** của dữ liệu
- [ ] Nếu chạy R4: đã có số **đặt lịch / đến khám / soi được**, hoặc biết là chưa có
- [ ] Nếu chạy R6: bảng khách phẳng, một dòng tiêu đề, biết cột "Tình trạng" là loại nào
- [ ] File chạy trên **máy nội bộ** — đây là dữ liệu sức khỏe
