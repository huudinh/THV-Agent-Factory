# P6 — TRẠNG THÁI L1–L6 & LUỒNG VẬN HÀNH
Module brand-specific. **Đây là xương sống của cả hệ báo cáo** — mọi file Excel đều có cột L-code lấy từ đây. Cập nhật: 2026-10-28.

---

## 1. LUỒNG VẬN HÀNH ĐẦU–CUỐI

```
KH nhắn Fanpage (FB / Zalo / Web / TikTok)
  → Trực page đọc & trả lời
  → 🚩 SÀNG CỜ ĐỎ ngay ở khâu này          ← bước riêng của ngành tiêu hóa
  → KH cho SĐT → tạo Lead, chuyển CSKH / tổng đài
  → Gọi tư vấn, mời đặt lịch khám + GỬI HƯỚNG DẪN CHUẨN BỊ
  → KH ĐẾN KHÁM với bác sĩ tiêu hóa        ← mốc rò 1
  → Bác sĩ chỉ định → THỰC HIỆN NỘI SOI    ← mốc rò 2 (chuẩn bị không đạt thì hoãn)
  → Kết quả (± sinh thiết / giải phẫu bệnh)
  → Điều trị / HẸN SOI LẠI THEO CHU KỲ     ← vòng LTV
```

**Hệ báo cáo này đứng ở đâu:** đọc **dữ liệu đã xảy ra** (hội thoại đã xuất ra file, danh sách post đã chạy) rồi sinh báo cáo. Nó **không** nối vào CRM, **không** tự trả lời khách, **không** thao tác trên phần mềm nào. Người dùng xuất file → dán cho trợ lý → nhận báo cáo → đọc và ra quyết định.

> 🚩 **Bước sàng cờ đỏ nằm ở trực page, không nằm ở bác sĩ.** Người đầu tiên đọc được câu *"em đi ngoài phân đen"* là trực page. Vì vậy mọi báo cáo của hệ này đều có cột cờ đỏ, và [[R3-chat-luong-tu-van]] chấm riêng khâu này.

---

## 2. TAXONOMY TRẠNG THÁI L1–L6

Bộ mã này là chuẩn chung với hệ CSKH của tập đoàn, **cộng thêm ba mã riêng của ngành tiêu hóa: `L6.7` · `L6.8` · `L6.9`**.

| Level | Mã | Định nghĩa | Nhiệt | Rào cản |
|---|---|---|---|---|
| **L1 Tương tác mới** | **L1.1** | Lần đầu nhắn, chưa được tư vấn gì | Cold | — |
| **L2 Đang tư vấn** | **L2.1** | Có nhu cầu thật, hợp tác cung cấp thông tin, chưa cho số | Warm | — |
| | **L2.3** | Đã tư vấn nhưng chưa phản hồi lại | Warm | — |
| | **L2.4** | Khách chủ động hẹn nhắn lại sau | Warm | — |
| | **L2.5** | **Ngoài Hà Nội / quá xa 139 Đại La** → khách từ chối vì đường xa | Cool | NGẠI |
| **L4 Cơ hội mới** | **L4.1** | **Có SĐT + nhu cầu rõ** → chuyển CSKH/tổng đài | Hot | — |
| **L5 Đang kết nối** | **L5.3** | Gọi không bắt máy | Hot | — |
| | **L5.4** | Từ chối nghe điện thoại, chỉ muốn nhắn | Hot | — |
| | **L5.5** | Hẹn giờ gọi lại cụ thể | Hot | — |
| | **L5.6** | Chỉ trao đổi qua Zalo | Hot | — |
| **L6 Cơ hội ≤30 ngày** | **L6.1** | Có nhu cầu, **chưa xác định được rào cản** | Warm→Hot | ? |
| | **L6.2** | Đang so sánh nơi khác — **bệnh viện công** hoặc cơ sở tư khác | Warm→Hot | **NGỜ** |
| | **L6.3** | Chưa đủ / chưa sẵn ngân sách · hỏi có bảo hiểm không | Warm→Hot | **NGẠI** |
| | **L6.4** | Chưa sắp xếp được thời gian · sợ phải nghỉ làm · không có người đưa về | Warm→Hot | **NGẠI** |
| | **L6.5** | **Sợ nội soi** — sợ buồn nôn, sặc, đau, sợ uống thuốc làm sạch ruột | Warm→Hot | **SỢ** |
| | **L6.6** | Cần hỏi ý kiến người thân | Warm→Hot | NGỜ + NGẠI |
| | **L6.7** ⭐ | **Ngại tiền mê / gây mê** — sợ thuốc mê ảnh hưởng tim, trí nhớ, "không tỉnh lại"; có bệnh nền nên lo | Warm→Hot | **SỢ (nặng)** |
| | **L6.8** ⭐ | **NÉ KẾT QUẢ** — biết nên soi nhưng trì hoãn vì **sợ phát hiện ra bệnh** | Warm→Hot | **NÉ** |
| | **L6.9** ⭐ | **Ngờ vệ sinh dây soi** — sợ lây nhiễm chéo từ người soi trước | Warm→Hot | **NGỜ** |

### ⭐ Vì sao cần ba mã riêng, trong khi hệ nha khoa chỉ thêm một

Rào cản của ngành nha nằm ở **vật liệu** (một thứ). Rào cản của ngành nội soi nằm ở **thủ thuật**, mà thủ thuật có ba mặt hoàn toàn khác nhau, cần ba bằng chứng khác nhau để gỡ:

| Mã | Khách sợ cái gì | Gỡ bằng | Gộp vào mã khác thì mất gì |
|---|---|---|---|
| `L6.5` | **Cái ống** — cảm giác trong lúc soi | Bản tiền mê | Mất nhóm **chuyển đổi được ngay** bằng cách đổi sang bản mê |
| `L6.7` | **Thuốc mê** — ảnh hưởng sức khỏe | Sàng lọc trước mê + bác sĩ gây mê theo dõi riêng | Gộp vào `L6.5` thì gợi ý *"mình soi tiền mê nhé"* — **đúng cái khách đang sợ** |
| `L6.9` | **Dây soi** — lây bệnh | Quy trình rửa – tiệt khuẩn | Mất khả năng đo xem nhân viên có biết trả lời câu này hay không |
| `L6.8` | **Kết quả** — tin xấu | Nói về lợi ích biết sớm, hẹn mốc cụ thể | Gộp vào `L6.3`/`L6.4` thì gửi ưu đãi giảm giá — **đẩy khách xa thêm** |

> **`L6.8` là mã quan trọng nhất trong bốn mã trên.** Nó là nhóm đông nhất của tệp nguội ngành tiêu hóa, và là nhóm **duy nhất mà nội dung đúng có thể gọi lại được** — nhưng chỉ khi nhận ra đúng. Xem dấu hiệu nhận biết ở [[P2-khach-hang]] §2.

**Nhịp theo dõi L6 (đã tư vấn, chưa đặt lịch khám):** **D+3 → D+7 → D+15**.
**Ngoại lệ `L6.8`:** nhịp **D+7 → D+21 → D+45**, nội dung là **giáo dục, không phải ưu đãi**. Người đang né kết quả cần thời gian, không cần bị nhắc nhiều.

### Quy ước phân biệt các mã dễ lẫn
- **`L2.3` vs `L6.x`:** chưa biết rào cản *và* chưa tư vấn sâu → `L2.3`. Đã tư vấn, biết rào cản → `L6.x` tương ứng.
- **`L2.5` vs `L6.4`:** khách **ngoài Hà Nội** → `L2.5`. Khách **trong Hà Nội** mà bảo xa/bận → **`L6.4`**, vẫn còn cửa.
- **`L6.4` vs `L6.8`:** cùng nói "để em sắp xếp". Khác ở chỗ `L6.4` **hỏi tiếp về lịch, về thời gian làm, về việc nghỉ bao lâu**; `L6.8` **lùi mà không hỏi thêm gì**, và trước đó đã hỏi rất kỹ về bệnh. Không chắc → ghi `L6.1` kèm ghi chú, **đừng đoán**.
- **`L4.1`:** phải có **cả hai**: số điện thoại **và** nhu cầu/triệu chứng rõ. Có số mà không rõ gì → vẫn `L2.x`, ghi chú "có số, chưa rõ nhu cầu".
- 🚩 **Ca cờ đỏ không có mã L riêng.** Nó là **cột riêng**, chồng lên mọi mã L. Một ca có thể là `L2.1 · 🚩 CĐ-1` — và cờ đỏ thắng về ưu tiên xử lý.

---

## 3. ⭐ BA TRỤC + MỘT CỜ — KHÔNG ĐƯỢC GỘP

Mọi file Excel do hệ này sinh ra phải có **ba cột riêng cộng một cột cờ**:

| Cột | Là gì | Giá trị | Quyết định điều gì |
|---|---|---|---|
| **L-code** | *Trạng thái vận hành* — khách đang ở đâu trong luồng | `L1.1` … `L6.9` | Dùng kịch bản nào, ai xử lý tiếp |
| **Độ nóng** | *Mức sẵn sàng* — chấm theo 5 tín hiệu ([[P8-chuan-cham-ban-giao]] §1) | HOT / WARM / COLD | SLA gọi, ai nhận |
| **Nhóm giá trị** | *Giá trị kỳ vọng của dịch vụ* ([[P4-dich-vu]] §4) | G1 / G2 / G3 | Mức đầu tư chăm sóc, được phép nuôi bao lâu |
| 🚩 **Cờ đỏ** | *Mức ưu tiên y tế* ([[P4-dich-vu]] §3) | `CĐ-1`…`CĐ-6` hoặc trống | **Có cờ là gọi ngay + chuyển bác sĩ trong ngày**, bất kể ba cột trên |

Một lead mang cả bốn: ví dụ `L6.7 · WARM · G1 · (không cờ)` = *đang ngại tiền mê, chưa sẵn sàng, nhưng là ca combo tầm soát* → **nuôi kỹ bằng bằng chứng sàng lọc trước mê và bác sĩ gây mê riêng, không bỏ**.

> Hệ thẩm mỹ có hai trục, hệ nha khoa có ba. Hệ tiêu hóa có **ba trục + một cờ an toàn**. Cờ đỏ không phải trục thứ tư vì nó **không dùng để xếp hạng giá trị** — nó dùng để **không bỏ sót người bệnh**.

---

## 4. ĐIỀU KIỆN THOÁT — khi nào ngừng nuôi

- **Đã thực hiện nội soi** → chuyển sang luồng kết quả & theo dõi, thoát luồng nuôi của trực page.
- **Từ chối dứt khoát** ("không có nhu cầu") → đóng, dừng nhắn.
- **Hết cửa sổ 24h Messenger** mà chưa phản hồi → ngừng nhắn tự do; có SĐT thì chuyển CSKH, chưa có thì chờ khách quay lại.
- **Quá 30 ngày ở L6 không tiến triển** → hạ về tệp remarketing. **Hai ngoại lệ:**
  - **`L6.x · G1` nuôi tới 90 ngày** — chu kỳ quyết định của combo tầm soát và ca can thiệp dài hơn hẳn.
  - **`L6.8` (né kết quả) nuôi tới 180 ngày** bằng nội dung giáo dục, nhịp thưa. Đây là nhóm quay lại muộn nhưng **quay lại thật** — cắt ở 30 ngày là bỏ đúng tệp dễ gọi lại nhất của ngành.
- 🚩 **Ca cờ đỏ không bao giờ "thoát" bằng cách im lặng.** Khách không phản hồi thì vẫn phải có một lần chạm ghi nhận lại, và ghi vào báo cáo là **chưa tiếp cận được ca có dấu hiệu cần khám sớm**.

---

## 5. PHIẾU BÀN GIAO — 14 TRƯỜNG

Khi lead lên `L4.1`, trực page ghi lại cho CSKH:

`Họ tên` · `SĐT` · `Zalo` · `Triệu chứng & bị bao lâu` · 🚩 `Dấu hiệu cờ đỏ (có/không, mã nào)` · `Đã khám/soi ở đâu chưa, có kết quả không` · `Bệnh nền & thuốc đang dùng` · `Dịch vụ/nhóm vấn đề (TH-xx)` · `Rào cản chính (SỢ/NGỜ/NGẠI/NÉ)` · `Thời gian dự kiến` · `Khung giờ tiện` · `Độ nóng + Nhóm giá trị` · `Link hội thoại` · `Tên trực page`

> Ngành tiêu hóa cần **14 trường**, thêm so với ngành nha ba mục: 🚩 **dấu hiệu cờ đỏ**, **bệnh nền & thuốc đang dùng**, và **có kết quả từ nơi khác không**.
> - Thiếu **cờ đỏ** → ca cần ưu tiên y tế lẫn vào hàng đợi thường.
> - Thiếu **bệnh nền** → CSKH hẹn tiền mê cho người chưa đủ điều kiện, khách đến rồi phải về (**mốc rò 2**).
> - Thiếu **kết quả nơi khác** → bác sĩ phải hỏi lại từ đầu, và khách phải kể lại bệnh của mình lần thứ ba.

**Báo cáo chất lượng tư vấn chấm tiêu chí ⑧ bằng cách đếm xem phiếu đủ 14 trường hay không.** Dữ liệu không có phần ghi chú bàn giao → ghi `⚠ không đo được tiêu chí ⑧`, **không cho điểm 0 oan**.

---

## 6. LIÊN KẾT MODULE
[[P3-hanh-vi-trang-thai]] · [[P4-dich-vu]] · [[P5-kich-ban]] · [[P8-chuan-cham-ban-giao]]
