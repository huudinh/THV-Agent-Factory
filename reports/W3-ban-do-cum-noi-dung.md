# W3 — BẢN ĐỒ CỤM NỘI DUNG & LỊCH XUẤT BẢN

**Trả lời câu hỏi:** *Viết cụm nào trước, mỗi tuần làm gì, và sửa bài cũ hay viết bài mới thì đáng hơn.*

**Cần có:** kết quả **W1** (kho câu hỏi). Có thêm **W2** (rà soát bài cũ) và **R2** (dữ liệu quảng cáo) thì ra được bản đầy đủ.
**Nhận lại:** 1 file Excel — `output/THV_BanDoNoiDung_<KỲ>.xlsx`, **5 sheet**. Kèm **lịch 8 tuần** in ra trong chat.

> **Đây là báo cáo quyết định thứ tự, không phải báo cáo sản xuất nội dung.** Nó không viết bài, không ra brief — việc đó thuộc `seo-brief-engine` và `seo-article-writer`. Việc của W3: **xếp hàng đợi**, và nói rõ mỗi việc trong hàng đợi đáng bao nhiêu so với việc khác.

---

## Nguyên tắc xếp ưu tiên — bốn yếu tố, không phải một

Phần lớn lịch nội dung được xếp theo **volume tìm kiếm**. Với một phòng khám có một cơ sở ở Hà Nội thì đó là cách xếp sai, vì phần lớn volume đến từ người không bao giờ đến 139 Đại La.

| Yếu tố | Lấy từ đâu | Vì sao tính |
|---|---|---|
| ① **Nhu cầu thật** | W1 — số hội thoại hỏi câu đó | Người đã chọn THV mà còn vướng → gỡ được là gỡ cho người thật |
| ② **Khoảng trống** | W1 cột "web đã có?" + W2 | Cụm đã có 12 bài thì bài thứ 13 đáng ít hơn bài đầu tiên của cụm trống |
| ③ **Nhóm giá trị** | `G1/G2/G3` theo [[P4-dich-vu]] §4 | Một bài kéo khách combo tầm soát (G1) đáng hơn bài kéo khách khám đầy hơi (G3) |
| ④ **Rủi ro đang mở** | W2 mức 🔴 / 🟠 | **Sửa một bài mức 🔴 luôn đáng hơn viết bài mới**, bất kể ba yếu tố trên |

> **Luật cứng:** mọi việc mức 🔴 ở W2 chiếm chỗ **trước** mọi bài mới trong lịch. Một bài đang hướng người đọc tự xử lý triệu chứng cờ đỏ gây hại nhiều hơn mười bài chưa viết.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Dựng bản đồ cụm nội dung và lịch xuất bản 8 tuần cho tieuhoaviet.com.vn.
Đầu vào: kết quả W1 {{FILE W1}} (+ W2 {{FILE W2}} + R2 {{FILE R2}} nếu có).
Sinh ra ĐÚNG 1 file: `output/THV_BanDoNoiDung_{{KỲ}}.xlsx` — 5 sheet.
Kèm in ra trong chat LỊCH 8 TUẦN dạng bảng.

Viết script Python dùng openpyxl, ghi file thật. Không chạy được code → nói rõ rồi
trả bảng markdown dán được vào Excel.

⛔ KHÔNG viết bài, KHÔNG viết brief chi tiết. Việc này là XẾP THỨ TỰ.
   Brief thuộc skill `seo-brief-engine`, viết bài thuộc `seo-article-writer`.

# BƯỚC 1 — DỰNG BẢN ĐỒ 8 CỤM
Tám cụm nội dung của THV (theo P9 §4), mỗi cụm một dòng:
① Trải nghiệm thủ thuật       (soi có đau không · mê có hại không · dây soi có sạch không)
② Chuẩn bị trước soi          (nhịn ăn bao lâu · uống thuốc làm sạch ruột · người đưa về)
③ Giá & điều kiện             (bao nhiêu tiền · bảo hiểm · cắt polyp thêm bao nhiêu)
④ Triệu chứng → có cần soi    (đau thượng vị · trào ngược · đi ngoài ra máu · táo bón)
⑤ Tầm soát & chu kỳ           (bao nhiêu tuổi nên soi · bao lâu soi lại · gia đình có người ung thư)
⑥ HP                          (lây thế nào · diệt không khỏi · cả nhà có cần test)
⑦ Đọc hiểu kết quả            (thuật ngữ trong phiếu kết quả · có cần soi lại không)
⑧ Địa điểm & bác sĩ           (khám tiêu hóa ở đâu · ai soi · có làm Chủ nhật không)

Với mỗi cụm, tính:
- Số hội thoại hỏi (từ W1)
- Số bài web đang có (từ W1 hoặc W2)
- Tỷ số nhu cầu / nguồn cung = số hội thoại ÷ số bài  → cụm nào đang mỏng nhất
- Nhóm giá trị dịch vụ mà cụm dẫn tới (G1/G2/G3)
- Giai đoạn phễu cụm phục vụ (S1/S2/S3/CS)
- Số bài mức 🔴 và 🟠 trong cụm (từ W2)
- 4 rào cản mà cụm gỡ được

# BƯỚC 2 — XẾP ƯU TIÊN
Điểm ưu tiên của mỗi việc tính từ bốn yếu tố, GHI RÕ CÔNG THỨC ĐÃ DÙNG ở đầu sheet:
nhu cầu thật (số hội thoại) × khoảng trống (chưa có bài = cao nhất) ×
nhóm giá trị (G1 > G2 > G3) — và mọi việc 🔴 ở W2 được đẩy lên đầu hàng đợi
BẤT KỂ điểm.

⛔ KHÔNG dùng volume tìm kiếm làm yếu tố chính. Nếu có số volume thì ghi vào một cột
   riêng để tham khảo, và nói rõ: volume cho biết cả nước tìm gì, số hội thoại cho biết
   người sẽ đến 139 Đại La vướng gì. Hai thứ khác nhau.

Nhóm việc thành bốn loại, vì chúng tốn công khác nhau:
- SỬA GẤP     — bài đã có, mức 🔴 hoặc 🟠 (nhanh nhất, đáng nhất)
- CẬP NHẬT    — bài đã có nhưng lệch ý câu hỏi, hoặc giá cũ (vừa)
- VIẾT MỚI    — chưa có bài (tốn nhất)
- GỘP/XOÁ     — nhiều bài trùng ý nhau trong cùng cụm → gộp về một bài trụ

# BƯỚC 3 — CẤU TRÚC FILE EXCEL, 5 sheet

1. **Bản đồ 8 cụm** — một dòng mỗi cụm, cột:
   Cụm | Số hội thoại hỏi | Số bài đang có | Nhu cầu/cung | Nhóm giá trị | Giai đoạn phễu |
   Rào cản gỡ được | 🔴 | 🟠 | Trạng thái cụm | Việc chính của cụm
   → Trạng thái cụm, chọn một trong bốn:
     MỎNG — nhiều người hỏi, ít bài  ← ưu tiên cao nhất
     ĐỦ — nhu cầu và nguồn cung tương đương
     DÀY — nhiều bài, ít người hỏi  ← cân nhắc gộp, đừng viết thêm
     CÓ RỦI RO — có bài mức 🔴/🟠  ← xử lý trước mọi thứ
   → Sắp xếp: CÓ RỦI RO trước, rồi MỎNG, rồi ĐỦ, rồi DÀY.

2. **Hàng đợi việc** ⭐ — một dòng mỗi việc, cột:
   Hạng | Loại việc (SỬA GẤP/CẬP NHẬT/VIẾT MỚI/GỘP) | Cụm | Tiêu đề bài |
   Câu hỏi gốc (lời khách) | Số hội thoại hỏi | Nhóm giá trị | Điểm ưu tiên |
   Công sức (nhẹ/vừa/nặng) | Người làm | Tuần | Cách đo kết quả
   → Cột "Cách đo kết quả" phải cụ thể và đo được trong 1–2 tháng: ví dụ
     "số hội thoại hỏi câu này giảm" (đo lại bằng W1 kỳ sau) · "trực page có link để
     gửi, đếm số lần gửi" · "bài vào top 10 từ khoá chính".
     ⛔ Không dùng thước đo không đo được như "tăng độ tin cậy".
   → Việc 🔴 luôn ở hạng 1–n, không trộn vào giữa.

3. **Lịch 8 tuần** — cột:
   Tuần | Việc | Loại | Cụm | Người làm | Đầu ra | Phụ thuộc gì
   → Nguyên tắc chia: tuần 1–2 dành cho SỬA GẤP (🔴 và 🟠) · từ tuần 3 mới VIẾT MỚI ·
     mỗi tuần không quá 3 việc nặng · mỗi cụm làm trọn vẹn rồi mới sang cụm khác
     (viết rải rác mỗi cụm một bài thì không cụm nào đủ để liên kết nội bộ).
   → Cột "Phụ thuộc gì" ghi rõ việc nào chờ dữ liệu từ THV: ví dụ bài về chuẩn bị
     trước soi phải chờ `{hướng_dẫn_chuẩn_bị}` bản chính thức (P4 §7 — hiện ⚠ chờ cấp);
     bài về giá phải chờ P7 xác nhận.
     ⛔ Không xếp vào lịch việc đang chờ dữ liệu mà chưa ai đi xin — xếp thì phải ghi
     tên người đi xin và hạn.

4. **Cụm đáng làm trọn gói** — cột:
   Cụm | Bài trụ | Các bài nhánh | Liên kết nội bộ nên có | Trang đích CTA |
   Vì sao làm trọn gói cụm này
   → Chỉ chọn 2–3 cụm cho một kỳ 8 tuần. Làm trọn một cụm (một bài trụ + 3–5 bài nhánh
     liên kết với nhau) đáng hơn rải 8 bài lẻ ở 8 cụm.
   → Bài trụ là bài trả lời câu hỏi rộng nhất của cụm; bài nhánh trả lời các câu hẹp.
     Mọi bài nhánh liên kết về bài trụ, bài trụ liên kết ra các nhánh.

5. **Chú giải & giới hạn** — 8 cụm · 4 loại việc · công thức điểm ưu tiên · 4 mức
   trạng thái cụm · danh sách bác sĩ được duyệt cho byline · nhắc lại ba luật bắt buộc
   của nội dung web (byline · ngày cập nhật · 🚩 khối cờ đỏ) · các slot ⚠ đang chờ
   THV cấp mà chặn việc viết bài.
   → Kèm một đoạn: brief chi tiết lấy từ `seo-brief-engine`, viết bài bằng
     `seo-article-writer`, chấm trước khi đăng bằng `seo-qa-fixer`, chấm URL đã đăng
     bằng `geo-scorecard`. W3 không làm bốn việc đó.

# LỊCH 8 TUẦN — in ra trong chat
Bảng gọn: Tuần | 1–3 việc | Người làm | Đầu ra.
Dưới bảng, ba dòng:
- Việc 🔴 phải xong trong tuần nào, và còn bao nhiêu việc 🔴
- Hai cụm được làm trọn gói trong kỳ này, và vì sao chọn hai cụm đó
- Dữ liệu đang chờ THV cấp mà chặn việc gì — kèm tên người đi xin và hạn

# QUY TẮC
- Việc mức 🔴 từ W2 luôn đứng trước mọi bài mới. Không thương lượng.
- ⛔ Không dùng volume tìm kiếm làm yếu tố xếp hạng chính.
- Cụm dưới 3 hội thoại hỏi trong kỳ → ⚠ chưa đủ mẫu, không xếp ưu tiên dựa trên
  nhu cầu; chỉ xếp nếu có lý do khác (ví dụ cụm đó chặn rủi ro pháp lý).
- Mỗi việc phải có người làm và cách đo kết quả. Việc không có cả hai thì bỏ khỏi lịch.
- Việc đang chờ dữ liệu từ THV: ghi rõ chờ gì, ai đi xin, hạn khi nào. ⛔ Không xếp
  vào lịch như thể đã có dữ liệu.
- Mỗi tuần không quá 3 việc nặng. Lịch dày quá thì không ai làm, và tuần 3 trở đi
  lịch chết.
- ⛔ Không tự đặt mục tiêu traffic hay thứ hạng rồi kết luận đạt/không đạt. Chưa có
  mốc do THV chốt → ghi ⚠ chưa có mốc so sánh.

# CÁCH LÀM
1. Đọc W1 (+ W2, R2 nếu có). Báo: có đủ ba đầu vào không · thiếu cái nào thì mất
   khả năng đọc gì.
   DỪNG LẠI cho tôi xác nhận.
2. Dựng bản đồ 8 cụm, in bảng trạng thái cụm.
   DỪNG LẠI cho tôi xác nhận cụm nào MỎNG, cụm nào CÓ RỦI RO.
3. Xếp hàng đợi việc + lịch 8 tuần.
4. Ghi file + in lịch trong chat.
5. Tự kiểm và báo: mọi việc 🔴 có đứng trước bài mới không · có việc nào thiếu người
   làm hoặc thiếu cách đo không · có tuần nào quá 3 việc nặng không · có việc nào
   đang chờ dữ liệu mà không ghi tên người đi xin không.
````

## Đến đây

---

## Lưu ý khi dùng

**Chạy W3 sau W1, và nếu được thì sau cả W2.** Chỉ có W1 thì vẫn ra được bản đồ cụm và hàng đợi bài mới, nhưng mất toàn bộ phần **sửa bài cũ** — mà đó thường là phần đáng làm trước nhất, vì nó nhanh hơn và gỡ rủi ro đang mở.

**Yếu tố ④ (rủi ro đang mở) thắng ba yếu tố còn lại, và đó là điểm khác biệt lớn nhất so với một lịch nội dung thông thường.** Lịch nội dung bình thường xếp theo cơ hội. Ở một ngành khám chữa bệnh, **một bài sai đang chạy gây hại nhiều hơn mười bài đúng chưa viết** — vì bài sai vẫn đang được đọc hàng ngày.

**Làm trọn một cụm đáng hơn rải mỗi cụm một bài.** Một cụm có bài trụ và các bài nhánh liên kết với nhau thì: người đọc đi được từ câu hỏi hẹp tới câu trả lời rộng, trực page có một link duy nhất để gửi, và cụm đó có cơ hội được AI trích dẫn như một nguồn. Tám bài lẻ ở tám cụm thì không đạt được điều nào trong ba điều đó.

**Hai cụm nên làm trọn gói trước, theo quan sát ban đầu ở [[P9-noi-dung-web]] §1:** cụm ① **Trải nghiệm thủ thuật** và cụm ② **Chuẩn bị trước soi**. Lý do: cả hai đều mỏng trên web so với lượng câu hỏi thật trong inbox, cả hai đều gỡ đúng rào cản chặn nhiều nhất (**SỢ**), và cụm ② còn chặn thẳng **mốc rò 2** của phễu — khách đến tận nơi mà không soi được ([[P3-hanh-vi-trang-thai]] §3).

⚠️ Nhưng nhận xét đó dựa trên **một lần quan sát bề mặt website ngày 2026-10-28**, không phải trên số đo. W3 phải đo lại bằng W1 + W2 rồi mới chốt, và nếu dữ liệu nói khác thì theo dữ liệu.

**Cụm ② có một chỗ chặn thật: chưa có bản hướng dẫn chuẩn bị chính thức của THV** ([[P4-dich-vu]] §7). Không có nó thì không ai được viết số giờ nhịn ăn hay cách uống thuốc làm sạch đại tràng — kể cả khi tìm thấy con số đó ở nguồn khác. Việc đầu tiên của cụm này không phải viết bài, mà là **đi xin bản hướng dẫn đó**. Lịch phải ghi tên người đi xin.
