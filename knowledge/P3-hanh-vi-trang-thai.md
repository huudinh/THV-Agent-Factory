# P3 — HÀNH VI KHÁCH & BẢN ĐỒ GIAI ĐOẠN
Module brand-specific. Nối **giai đoạn hành trình** với **trạng thái vận hành L1–L6** ([[P6-van-hanh]]) và với **báo cáo nào đọc được gì**. Cập nhật: 2026-10-28.

---

## 1. BỐN GIAI ĐOẠN — ký hiệu S dùng trong báo cáo

Trong các file Excel, cột **Giai đoạn** chỉ dùng 4 mã: **S1 · S2 · S3 · CS**.

| Mã | Giai đoạn | Nhiệt | Dấu hiệu nhận ra trong hội thoại | Mục tiêu hội thoại |
|---|---|---|---|---|
| **S1** | **NHẬN BIẾT** | Cold | Hỏi chung "có nội soi không", "bao nhiêu tiền", "ở đâu" ngay câu đầu. Chưa kể triệu chứng của mình | Trả lời đúng câu hỏi, gieo tin, **không chốt vội** |
| **S2** | **TÌM HIỂU** | Warm | Kể triệu chứng · gửi kết quả xét nghiệm / đơn thuốc / kết quả soi cũ · hỏi quy trình, hỏi mê hay không mê, hỏi ai soi | Giáo dục, nêu bằng chứng, hướng tới xin số |
| **S3** | **CÂN NHẮC & NỖI SỢ ★** | Warm→Hot | Hỏi đau/nôn/mê · hỏi dây soi có sạch không · so sánh bệnh viện công · hỏi người nhà · chần chừ giá, thời gian · **hoặc lùi lịch không kèm câu hỏi nào** | **Gỡ đúng rào cản** (SỢ · NGỜ · NGẠI · NÉ) rồi mới CTA |
| **CS** | **SAU NỘI SOI & THEO DÕI** | Existing / LTV | Đã soi rồi, hỏi kết quả, hỏi thuốc, hỏi chế độ ăn · **đến hẹn soi lại** · hỏi cho người nhà | Hướng dẫn, **nhắc đúng mốc tái soi**, mời người nhà cùng tầm soát |

> **S3 là điểm quyết định của ngành tiêu hóa, và nó rơi nhiều hơn ngành nha.** Lý do: ở nha khoa, khách tới S3 là người **muốn** làm; ở tiêu hóa, khách tới S3 vẫn có thể **không muốn biết kết quả** ([[P2-khach-hang]] §2, rào cản **NÉ**). Mọi báo cáo phải tách riêng S3 và nói rõ S3 vướng rào cản nào trong **bốn** nhóm.

---

## 2. BẢN ĐỒ: GIAI ĐOẠN ↔ L-CODE ↔ BÁO CÁO ĐỌC ĐƯỢC GÌ

| Giai đoạn | L-code thường gặp | Báo cáo chính | Đọc ra điều gì |
|---|---|---|---|
| **S1** NHẬN BIẾT | `L1.1` | [[R2-phan-tang-quang-cao]] | Post nào chỉ kéo người hỏi giá |
| **S2** TÌM HIỂU | `L2.1` · `L2.3` · `L2.4` | [[R1-phan-loai-hoi-thoai]] | Khâu xin số mạnh/yếu ở đâu |
| **S3** CÂN NHẮC | `L6.1` → `L6.9` | [[R1-phan-loai-hoi-thoai]] · [[R4-bao-cao-dieu-hanh]] | Rào cản nào chặn nhiều nhất, theo nhóm bệnh nào |
| **Chuyển giao** | `L4.1` → `L5.x` | [[R3-chat-luong-tu-van]] | Xin được số rồi có gọi được không |
| **CS** | — | [[R4-bao-cao-dieu-hanh]] | Tệp tái soi đến hẹn · tệp đã khám chưa soi · người nhà cùng tầm soát |
| **Mọi giai đoạn** | — | [[W1-kho-cau-hoi-noi-dung]] | Câu hỏi thật của khách → đề bài nội dung cho website |

---

## 3. ⭐ ĐẶC THÙ PHỄU TIÊU HÓA — HAI MỐC RÒ VÀ MỘT VÒNG QUAY LẠI

Phễu nha khoa: *inbox → có SĐT → kết nối → đặt lịch khám → đến khám → chốt phác đồ → điều trị*.

**Phễu tiêu hóa có hai mốc rò riêng, và có thêm một vòng tái soi:**

```
inbox → có SĐT → kết nối (gọi được) → đặt lịch
      → ĐẾN KHÁM  ............................. mốc rò 1
      → CHUẨN BỊ ĐẠT (nhịn ăn đủ giờ / ruột sạch / đủ điều kiện tiền mê)
      → THỰC HIỆN ĐƯỢC NỘI SOI  ............... mốc rò 2
      → kết quả (+ sinh thiết / giải phẫu bệnh nếu có)
      → điều trị · HẸN SOI LẠI THEO CHU KỲ  ← vòng LTV, quay lại đầu
```

### Mốc rò 1 — đặt lịch → đến khám
Giống mọi ngành y: khách hẹn rồi không đến. **Không được lấy "đặt lịch" thay cho "đến khám"**.

### Mốc rò 2 — đến khám → thực hiện được nội soi ⭐
**Đây là mốc rò chỉ ngành nội soi mới có.** Khách đã đến tận phòng khám mà vẫn không soi được, vì:

| Lý do hoãn tại chỗ | Thuộc về khâu nào |
|---|---|
| **Ăn sáng rồi / nhịn chưa đủ giờ** | Lỗi **hướng dẫn chuẩn bị** — của trực page và CSKH |
| **Ruột chưa sạch**, uống thuốc làm sạch không đúng cách | Lỗi **hướng dẫn chuẩn bị** |
| **Không đủ điều kiện tiền mê** (bệnh nền tim mạch/hô hấp, huyết áp cao, mang thai, chưa làm xét nghiệm sàng lọc) | Lỗi **sàng lọc trước khi hẹn** |
| **Không có người đưa về** sau mê | Lỗi **dặn trước** |
| **Đến rồi vẫn không dám soi** | Rào cản **SỢ / NÉ** chưa được gỡ ([[P2-khach-hang]] §2) |

> **Vì sao mốc này quan trọng hơn mọi con số khác trong báo cáo:** một ca hoãn ở đây đã tốn **toàn bộ** chi phí quảng cáo, chi phí nhân sự, và cả buổi của khách — mà doanh thu bằng không, lại kèm một khách thất vọng. Trong khi nguyên nhân thì **phần lớn là lỗi dặn dò, sửa được bằng một tin nhắn mẫu**.
>
> → [[R4-bao-cao-dieu-hanh]] **bắt buộc có cả hai cột** "đến khám" và "thực hiện được nội soi", kèm bảng **lý do hoãn tại chỗ**. Không có số thì ghi `⚠ chưa đo được`, **không suy ra**.

### Vòng tái soi — cơ chế LTV của ngành tiêu hóa

| Khách vừa làm gì | Mốc quay lại tự nhiên |
|---|---|
| **Cắt polyp đại tràng** | Soi lại theo hẹn của bác sĩ — thường tính bằng **năm**, tùy số lượng, kích thước và kết quả giải phẫu bệnh. `⚠ chu kỳ cụ thể do bác sĩ chỉ định, không tự nêu con số` |
| **Điều trị HP** | **Kiểm tra lại sau khi kết thúc phác đồ** theo hẹn của bác sĩ |
| **Viêm loét / Barrett / loạn sản** | Theo dõi định kỳ theo chỉ định |
| **Tầm soát ở người không triệu chứng** | Soi lại theo chu kỳ theo tuổi và nguy cơ |
| **Người bệnh hài lòng** | **Người nhà cùng tầm soát** — đặc biệt khi có yếu tố gia đình |

> ⚠️ **Luật viết nội dung:** chu kỳ tái soi là **chỉ định y khoa của bác sĩ cho từng ca**, không phải một con số marketing. Nội dung gợi ý chỉ được viết *"theo mốc bác sĩ đã hẹn trong phiếu kết quả"*, **không tự điền số năm**.
>
> **Nhưng cơ chế thì dùng được, và nó là tài sản lớn nhất của THV:** khác với nha khoa phải tạo nhu cầu mới, ở đây **danh sách khách đến hẹn đã có sẵn trong hồ sơ**. Tệp này gần như chắc chắn quay lại nếu được nhắc — mà thường không ai nhắc, vì họ không xuất hiện trong báo cáo lead mới. Xem [[R4-bao-cao-dieu-hanh]] sheet *Tệp giá trị dài hạn*.

---

## 4. CTA MẠNH NHẤT CỦA NGÀNH — VÀ CÁI BẪY CỦA NÓ

**CTA của THV là "đến khám với bác sĩ tiêu hóa để xem có cần soi và soi loại nào".**

Nói "đi khám" dễ nhận hơn nói "đi soi" rất nhiều: khám là **nghe bác sĩ nói**, chưa phải chịu thủ thuật, chưa phải trả khoản lớn. Hội thoại nào nhảy thẳng vào *"anh/chị đặt soi combo nhé"* là tư vấn sai nhịp — đặc biệt với nhóm đang **SỢ** hoặc **NÉ**.

**Cái bẫy:** CTA đó đẩy khách tới mốc rò 2. Khách đến khám với tâm thế "chỉ nghe tư vấn" thì **chưa nhịn ăn, chưa chuẩn bị ruột** — và nếu bác sĩ chỉ định soi luôn thì phải hẹn lại buổi khác.

→ **Luật:** mọi nội dung gợi ý mời khám **phải kèm một câu dặn chuẩn bị** để khách có lựa chọn soi luôn trong buổi đó nếu bác sĩ chỉ định. Thiếu câu đó là lỗi đếm được, và nó nằm trong bảng chấm 10 tiêu chí ([[P8-chuan-cham-ban-giao]] §6, tiêu chí ⑥).

---

## 5. LIÊN KẾT MODULE
[[P2-khach-hang]] · [[P4-dich-vu]] · [[P6-van-hanh]] · [[P8-chuan-cham-ban-giao]]
