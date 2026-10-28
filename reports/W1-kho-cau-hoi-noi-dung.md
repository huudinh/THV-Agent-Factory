# W1 — KHO CÂU HỎI THẬT → ĐỀ BÀI NỘI DUNG WEB

**Trả lời câu hỏi:** *Khách hỏi gì nhiều nhất trong inbox, và website đã trả lời chưa — nên viết bài gì tiếp.*

**Cần có:** file hội thoại (cùng loại file dùng cho R1). Có thêm **danh sách URL hiện có** thì đọc được cả cột "web đã có bài chưa".
**Nhận lại:** 1 file Excel — `output/THV_KhoCauHoi_<KỲ>.xlsx`, **6 sheet**.

> **Vì sao có báo cáo này.** Skill SEO làm rất tốt việc *biến một từ khoá thành bài viết*. Việc nó không làm được là **biết nên viết bài gì** — vì nó không có dữ liệu inbox của THV. Công cụ từ khoá cho biết người ta tìm gì trên Google; file hội thoại cho biết **người đã chọn THV thì còn vướng gì**. Hai thứ khác nhau, và cái thứ hai mới là thứ đối thủ không copy được.
>
> **Thứ tự dùng:** `W1` ra đề bài → skill **`seo-brief-engine`** ra brief → skill **`seo-article-writer`** viết → skill **`seo-qa-fixer`** chấm → đăng → `W2` rà soát định kỳ. Xem [[P9-noi-dung-web]] §5.

> ⚠️ **Báo cáo này có một nhiệm vụ mà các báo cáo R không có: chặn những câu hỏi KHÔNG ĐƯỢC trả lời trên web.** Khách hỏi *"HP kháng thuốc thì uống thuốc gì"* rất nhiều — và đó là câu **không được viết bài trả lời trực tiếp** ([[P9-noi-dung-web]] §3). Sheet 5 là nơi chặn.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Đọc file hội thoại {{FILE}} (kỳ {{KỲ}}) và rút ra KHO CÂU HỎI THẬT của khách,
rồi biến thành đề bài nội dung cho website tieuhoaviet.com.vn.
Có danh sách URL hiện có thì dùng thêm: {{FILE URL}}.
Sinh ra ĐÚNG 1 file: `output/THV_KhoCauHoi_{{KỲ}}.xlsx` — 6 sheet.

Viết script Python dùng openpyxl, ghi file thật. Không chạy được code → nói rõ rồi
trả bảng markdown dán được vào Excel.

⛔ ĐÂY KHÔNG PHẢI BÁO CÁO BÁN HÀNG. Không chấm độ nóng, không viết kịch bản nhắn lại,
không xếp hạng nhân viên. Việc duy nhất: lấy câu hỏi thật → ra đề bài nội dung.

# BƯỚC 1 — TRÍCH CÂU HỎI
Quét toàn bộ lời KHÁCH, lấy mọi câu có dạng câu hỏi hoặc mang ý hỏi
(kể cả không có dấu "?": "em muốn biết soi có đau không", "không rõ mê có sao không").
Với mỗi câu, ghi: nguyên văn (che SĐT) · số hiệu hội thoại · giai đoạn hội thoại đang ở.

Bỏ ra ngoài: câu hỏi về lịch cụ thể của chính khách ("mai 9h có chỗ không"),
câu xác nhận ("vậy là 1tr250 đúng không ạ"), câu hỏi không thuộc chuyên môn
(hỏi đường, hỏi gửi xe) — gom vào một dòng "câu hỏi vận hành", đếm số lượng, không
đưa vào kho đề bài.

# BƯỚC 2 — CHUẨN HOÁ & GOM
Gom các câu hỏi cùng ý về MỘT câu chuẩn hoá, viết bằng đúng lời khách hay dùng
(không viết lại thành ngôn ngữ y khoa):
  "soi có đau không" ← "soi có buồn nôn không", "em sợ nôn lắm", "đưa ống vào có rát không"
  "mê có hại không" ← "gây mê có ảnh hưởng trí nhớ không", "em tim đập nhanh mê được không"
Mỗi câu chuẩn hoá: đếm số LẦN XUẤT HIỆN và số HỘI THOẠI riêng biệt chứa nó.
→ Hai con số này khác nhau: một người hỏi lại ba lần không bằng ba người cùng hỏi.
  Xếp hạng theo SỐ HỘI THOẠI, không theo số lần.

# BƯỚC 3 — GÁN MÃ CHO TỪNG CÂU HỎI
- Nhóm vấn đề `TH-01…TH-12` (theo P4)
- Rào cản tương ứng: SỢ (L6.5·L6.7) · NGỜ (L6.2·L6.9) · NGẠI (L6.3·L6.4·L2.5) ·
  NÉ (L6.8) · hoặc "không mang rào cản" (câu hỏi thông tin thuần)
- Giai đoạn phễu câu hỏi đó thuộc về: S1 (chưa kể tình trạng) · S2 (đang tìm hiểu) ·
  S3 (đang vướng rào cản) · CS (sau nội soi)
- Nhóm giá trị dịch vụ mà câu hỏi dẫn tới: G1 / G2 / G3 / không rõ
- Cụm nội dung (theo P9 §4): Trải nghiệm thủ thuật · Chuẩn bị trước soi ·
  Giá & điều kiện · Triệu chứng → có cần soi · Tầm soát & chu kỳ · HP ·
  Đọc hiểu kết quả · Địa điểm & bác sĩ

# BƯỚC 4 — ĐỐI CHIẾU VỚI WEB
Có danh sách URL → với mỗi câu hỏi, đánh một trong bốn mức:
  ĐÃ CÓ BÀI ĐÚNG Ý       — có bài trả lời đúng câu hỏi đó
  CÓ BÀI NHƯNG LỆCH Ý    — có bài cùng chủ đề nhưng không trả lời đúng câu này
  CHƯA CÓ                — không có bài nào
  ⚠ KHÔNG KIỂM ĐƯỢC      — không có danh sách URL
Không có danh sách URL → cả cột này là ⚠, và nêu rõ: cần danh sách URL (xuất từ
sitemap hoặc từ WordPress) để đo được khoảng trống. KHÔNG tự suy đoán web có gì.

# DỪNG 1 — BÁO RỒI CHỜ TÔI XÁC NHẬN
In ra: tổng số câu hỏi trích được · số câu sau khi gom · 15 câu hỏi nhiều hội thoại
nhất kèm số đếm · phân bố theo cụm nội dung · phân bố theo rào cản ·
số câu thuộc nhóm KHÔNG ĐƯỢC TRẢ LỜI TRÊN WEB (bước 5).
Chờ tôi xác nhận trước khi viết đề bài.

# BƯỚC 5 — 🛑 CHẶN: CÂU HỎI KHÔNG ĐƯỢC TRẢ LỜI TRỰC TIẾP TRÊN WEB
Bốn loại câu hỏi dưới đây xuất hiện NHIỀU trong inbox nhưng KHÔNG được viết bài
trả lời trực tiếp (theo P9 §3). Tách riêng sang sheet 5:

| Loại câu hỏi | Ví dụ | Viết được gì thay thế |
|---|---|---|
| Hỏi thuốc, liều, phác đồ | "HP kháng thuốc uống thuốc gì", "thuốc dạ dày uống bao lâu" | Bài giải thích NGUYÊN LÝ điều trị và vì sao phải theo chỉ định bác sĩ — ⛔ không nêu tên thuốc, liều, phác đồ |
| Nhờ đọc kết quả | "kết quả ghi viêm hang vị HP+ là nặng không" | Bài giải thích các THUẬT NGỮ thường gặp trong phiếu kết quả, kèm câu: kết luận cho từng người phải do bác sĩ đọc trực tiếp |
| Hỏi để loại trừ ung thư | "em bị thế này có phải ung thư không" | Bài về DẤU HIỆU CẦN ĐI KHÁM NGAY (khối cờ đỏ CĐ-1…CĐ-6) — ⛔ không viết câu nào mang nghĩa loại trừ |
| Hỏi tự xử lý tại nhà cho triệu chứng cờ đỏ | "đi ngoài phân đen uống gì cho hết" | ⛔ KHÔNG viết bài hướng tự xử lý. Viết bài về việc đây là dấu hiệu cần khám sớm |

→ Với mỗi câu bị chặn, sheet 5 phải ghi: câu hỏi · số hội thoại hỏi · VÌ SAO chặn ·
  bài thay thế nên viết gì. Số lượng câu bị chặn cao là tín hiệu tốt cho nội dung —
  nó cho biết nên viết bài hướng khám ở đúng chỗ nào.

# BƯỚC 6 — CẤU TRÚC FILE EXCEL, 6 sheet

1. **Tổng quan**
   Kỳ · nguồn dữ liệu · số hội thoại đọc được · ngày lập.
   Tổng câu hỏi trích được / sau khi gom. Số câu bị chặn (sheet 5).
   Bảng: 10 câu hỏi nhiều hội thoại nhất, kèm mức đối chiếu web.
   Bảng: phân bố câu hỏi theo 8 cụm nội dung, kèm cột "web đã có bao nhiêu bài".
   3 KẾT LUẬN, mỗi dòng một con số — dạng: "cụm X có N hội thoại hỏi, web có M bài".
   **Khối cảnh báo:** mẫu là toàn bộ hay đã lọc · có danh sách URL để đối chiếu không ·
   con số nào không dùng để quyết nội dung.

2. **Kho câu hỏi** — một dòng mỗi câu hỏi chuẩn hoá, cột:
   Hạng | Câu hỏi (lời khách) | Số hội thoại | Số lần | Cụm nội dung | Nhóm vấn đề |
   Rào cản | Giai đoạn | Nhóm giá trị | Web đã có? | URL liên quan | Mức ưu tiên |
   Trích dẫn thật (1–2 câu, che SĐT)
   → Sắp xếp theo số hội thoại giảm dần.
   → Mức ưu tiên tính bằng ba yếu tố, ghi rõ công thức ở đầu sheet:
     số hội thoại hỏi × (web CHƯA CÓ hoặc LỆCH Ý) × nhóm giá trị G.
     Câu hỏi ít người hỏi nhưng dẫn tới G1 vẫn có thể ưu tiên cao hơn câu nhiều người
     hỏi mà dẫn tới G3 — nói rõ điều đó.
   → Câu dưới 3 hội thoại: ghi ⚠ chưa đủ mẫu, không xếp ưu tiên.

3. **Đề bài nội dung** ⭐ — sheet mang sang cho người viết. Một dòng mỗi bài, cột:
   Mã đề bài | Tiêu đề đề xuất | Câu hỏi gốc (lời khách) | Ý định tìm kiếm |
   **Câu trả lời ngắn phải nằm ở đoạn mở** | Các mục cần có | Bằng chứng THV nên dùng |
   🚩 Khối cờ đỏ cần có? | Byline bác sĩ đề xuất | Trang đích CTA | Nội liên kết tới |
   ⛔ Không được viết gì | Nhóm khách (N1–N6) | Nhóm giá trị | Mức ưu tiên
   → Cột "Câu trả lời ngắn phải nằm ở đoạn mở": viết sẵn 1–2 câu trả lời thẳng câu hỏi.
     Đây là phần quan trọng nhất của sheet — bài nào bắt người đọc kéo xuống mới thấy
     câu trả lời thì vừa mất người đọc vừa mất khả năng được AI trích dẫn.
   → Cột "🚩 Khối cờ đỏ cần có?": GHI CÓ với mọi bài nói về triệu chứng tiêu hóa.
     Khối đó liệt kê đúng CĐ-1…CĐ-6 theo P4 §3. Đây là yêu cầu an toàn, không phải SEO.
   → Cột "Bằng chứng THV nên dùng": chọn trong 4 trụ (chuyên gia Bạch Mai · hệ Fujifilm
     VP-7000 + AI · giấy phép 4654/HNO-GPHĐ · bác sĩ gây mê theo dõi riêng + bảng giá
     công khai). Không rải cả bốn vào một bài.
   → Cột "⛔ Không được viết gì": nêu cụ thể cho từng bài. Ví dụ bài "soi có đau không"
     → ⛔ không được dùng chữ "không đau"; bài giá → ⛔ không chốt số cuối, phải nêu
     ba điều kiện.
   → Byline: chỉ dùng bác sĩ trong danh sách đã duyệt (P1 §4). Không chắc → ⚠ cần THV
     phân công.

4. **Câu hỏi × cụm nội dung** — bảng chéo. Hàng = 8 cụm, cột = 4 rào cản + "không
   mang rào cản". Cột phụ: tổng hội thoại · số bài web đang có · khoảng trống.
   → Kèm một dòng "đọc bảng này thế nào".
   → Ô có nhiều hội thoại mà web ít bài = khoảng trống. Đây là bảng dùng để quyết
     viết cụm nào trước, và nó nối thẳng sang W3.

5. **🛑 Câu hỏi KHÔNG trả lời trực tiếp** — cột:
   Câu hỏi | Số hội thoại | Loại chặn | Vì sao chặn (dẫn P9 §3) | Bài thay thế nên viết |
   Trang đích
   → Không có câu nào bị chặn: vẫn giữ sheet, ghi rõ đã kiểm theo 4 loại.
   → Lưu ý ghi vào sheet: câu hỏi bị chặn trên WEB thì cũng bị chặn trong INBOX
     (P5 §1). Số lượng câu loại này cao là tín hiệu cần đào tạo trực page, không chỉ
     là tín hiệu nội dung — nói rõ và nối sang R3 học phần M0.

6. **Dữ liệu thô** — cột:
   STT HT | Ngày | Câu hỏi nguyên văn (che SĐT) | Câu chuẩn hoá đã gom về |
   Cụm | Nhóm vấn đề | Rào cản | Giai đoạn
   → Bắt buộc có. Không có sheet này thì không ai kiểm được việc gom câu hỏi có đúng không.

# QUY TẮC
- Câu hỏi chuẩn hoá phải viết bằng LỜI KHÁCH, không dịch sang ngôn ngữ y khoa.
  "soi có đau không" — không phải "lo ngại về cảm giác trong quá trình nội soi".
- Xếp hạng theo SỐ HỘI THOẠI, không theo số lần xuất hiện.
- Câu dưới 3 hội thoại: ⚠ chưa đủ mẫu, không xếp ưu tiên, nhưng vẫn giữ trong kho.
- Không có danh sách URL thì cột "Web đã có?" là ⚠ — ⛔ KHÔNG tự suy đoán web có gì.
- ⛔ Không trích nội dung kết quả xét nghiệm, chẩn đoán, hay thông tin định danh của
  khách vào bất kỳ sheet nào. Trích dẫn chỉ đủ để thấy câu hỏi là gì.
- Mọi đề bài phải đi qua sheet 5 trước: câu bị chặn thì không vào sheet 3.
- Đề bài nào chạm tới giá → ghi rõ phải lấy số từ P7 bản hiện hành, gắn ⚠.

# CÁCH LÀM
1. Trích và gom câu hỏi. Báo con số ở DỪNG 1.
2. Dựng sheet 5 (chặn) TRƯỚC sheet 3 — để không viết đề bài cho câu không được trả lời.
3. Viết đề bài cho các câu còn lại.
4. Ghi file.
5. Tự kiểm và báo: có đề bài nào ở sheet 3 trùng với câu bị chặn ở sheet 5 không ·
   mọi bài nói về triệu chứng có ghi "cần khối cờ đỏ" không · có byline nào ngoài
   danh sách duyệt không · có câu hỏi nào <3 hội thoại mà vẫn được xếp ưu tiên không.
````

## Đến đây

---

## Chuẩn bị dữ liệu đầu vào

**File hội thoại:** dùng lại đúng file đã chạy R1. Không cần xuất thêm.

**Danh sách URL** (nên có, không bắt buộc): xuất từ sitemap `tieuhoaviet.com.vn/sitemap.xml`, hoặc từ danh sách bài trong WordPress. Tối thiểu cần: URL · tiêu đề. Có thêm ngày cập nhật thì W2 dùng được luôn.

Không có danh sách URL thì W1 vẫn chạy — chỉ mất cột "web đã có bài chưa", tức là mất khả năng đo khoảng trống. Vẫn ra được kho câu hỏi và đề bài.

---

## Lưu ý khi dùng

**Giá trị của báo cáo này không nằm ở việc tìm từ khoá.** Công cụ từ khoá làm việc đó tốt hơn. Giá trị nằm ở chỗ: nó cho biết **người đã chọn THV rồi vẫn còn vướng gì** — và đó thường là những câu không ai search trên Google, như *"dây soi có dùng chung không"*. Câu đó không có volume tìm kiếm đáng kể, nhưng nếu nó xuất hiện trong 30 hội thoại của một kỳ thì một bài trả lời nó sẽ gỡ được rào cản cho 30 người tiếp theo, và trực page có chỗ để gửi link.

**Sheet 5 là phần dễ bị bỏ nhất và cũng là phần dễ gây hại nhất nếu bỏ.** Câu *"HP kháng thuốc uống thuốc gì"* là một trong những câu được hỏi nhiều nhất của ngành này, và nó rất "có volume". Viết bài trả lời trực tiếp câu đó là vừa sai phạm vi chuyên môn vừa rủi ro pháp lý — dù bài sẽ lên top. Prompt cố tình dựng sheet 5 **trước** sheet 3 để chặn trước khi đề bài được viết ra.

**Số câu hỏi bị chặn cao là một phát hiện về đào tạo, không chỉ về nội dung.** Nếu khách hỏi thuốc và hỏi đọc kết quả rất nhiều, thì trực page đang phải đối mặt với những câu đó hàng ngày — và câu hỏi đặt ra là họ đang trả lời thế nào. Nối sang R3, học phần M0.

**Đừng dùng kho câu hỏi này làm danh sách bài viết.** Nó là danh sách **đề bài có thứ tự ưu tiên**. Việc chọn viết bài nào trước, viết bao nhiêu bài một tuần, và cụm nào làm trọn gói thì thuộc W3.
