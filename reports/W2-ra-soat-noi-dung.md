# W2 — RÀ SOÁT NỘI DUNG WEB ĐANG CÓ

**Trả lời câu hỏi:** *Bài nào trên website đang có rủi ro pháp lý hoặc rủi ro an toàn, bài nào thiếu khối cờ đỏ, bài nào thiếu byline — và sửa theo thứ tự nào.*

**Cần có:** danh sách URL (xuất từ sitemap hoặc WordPress). Có thêm **nội dung bài** (dán vào, hoặc cho phép đọc trang) thì rà được đầy đủ.
**Nhận lại:** 1 file Excel — `output/THV_RaSoatNoiDung_<NGÀY>.xlsx`, **6 sheet**.

> **Báo cáo này khác với chấm SEO.** Chấm điểm SEO và chấm khả năng được AI trích dẫn đã có skill riêng: **`seo-qa-fixer`** (chấm bài trước khi đăng) và **`geo-scorecard`** (chấm từ URL). W2 làm phần hai skill đó không làm: **rà theo luật y tế và luật thương hiệu của THV** ([[P9-noi-dung-web]] §3) — byline bác sĩ trong danh sách duyệt, khối cờ đỏ, không nêu liều thuốc, không so sánh cơ sở khác, giá khớp `P7`.
>
> **Cách dùng cùng nhau:** W2 lọc ra danh sách bài cần sửa và nói sửa gì theo luật y tế → đưa từng bài cho `seo-qa-fixer` hoặc `geo-scorecard` để chấm phần nội dung và trích dẫn.

---

## Ba mức rủi ro — quyết định thứ tự sửa

| Mức | Nghĩa | Hạn xử lý |
|---|---|---|
| 🔴 **CHẶN** | Vi phạm pháp lý hoặc rủi ro an toàn người bệnh: nêu liều thuốc/phác đồ · hướng tự xử lý cho triệu chứng cờ đỏ · câu mang nghĩa loại trừ bệnh · so sánh hạ thấp cơ sở khác · từ cấm · ảnh người bệnh chưa có đồng ý | **Sửa hoặc ẩn bài ngay**, không chờ lịch |
| 🟠 **SỬA GẤP** | Thiếu khối cờ đỏ ở bài về triệu chứng · không có byline · giá lệch `P7` · nêu tên bác sĩ ngoài danh sách duyệt | Trong tuần |
| 🟡 **SỬA THƯỜNG** | Thiếu ngày cập nhật · thiếu câu miễn trừ · câu trả lời không nằm ở đoạn mở · thiếu CTA · thiếu nội liên kết | Theo lịch nội dung |

> **Vì sao "thiếu khối cờ đỏ" là 🟠 chứ không phải 🟡:** một bài về *"đau thượng vị"* hay *"đi ngoài ra máu"* mà không có mục *"khi nào cần đi khám ngay"* thì đang để người đọc có dấu hiệu nguy hiểm tự kết luận rằng mình chỉ bị nhẹ. Đó là thiếu sót về an toàn, không phải thiếu sót về cấu trúc bài.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Rà soát nội dung website tieuhoaviet.com.vn theo luật y tế và luật thương hiệu THV.
Đầu vào: danh sách URL {{FILE URL}} (+ nội dung bài nếu có: {{NỘI DUNG}}).
Sinh ra ĐÚNG 1 file: `output/THV_RaSoatNoiDung_{{NGÀY}}.xlsx` — 6 sheet.

Viết script Python dùng openpyxl, ghi file thật. Không chạy được code → nói rõ rồi
trả bảng markdown dán được vào Excel.

⛔ KHÔNG chấm điểm SEO, KHÔNG chấm khả năng AI trích dẫn — việc đó thuộc skill
`seo-qa-fixer` và `geo-scorecard`. Việc của báo cáo này: rà theo 12 tiêu chí dưới đây.

# PHẠM VI
Chỉ rà được bài nào ĐỌC ĐƯỢC NỘI DUNG. Bài chỉ có URL mà không có nội dung →
ghi `⚠ chưa rà được`, đếm riêng, KHÔNG suy đoán từ tiêu đề.
Nêu rõ ở sheet 1: rà được bao nhiêu / tổng bao nhiêu URL.

# 12 TIÊU CHÍ RÀ SOÁT

## Nhóm 🔴 CHẶN — vi phạm pháp lý hoặc an toàn
① **Nêu thuốc, liều, hoặc phác đồ** — kể cả phác đồ diệt HP, kể cả thuốc không kê đơn.
   Được giải thích NGUYÊN LÝ điều trị; không được chỉ thuốc và liều.
② **Hướng tự xử lý tại nhà cho triệu chứng cờ đỏ** — bài kiểu "đi ngoài phân đen nên
   ăn gì", "cầm máu tại nhà". Đây là mức nặng nhất.
③ **Câu mang nghĩa loại trừ bệnh** — "không phải ung thư", "chỉ là viêm thông thường",
   "không cần soi". Tìm cả biến thể mềm: "phần lớn là lành tính nên không cần lo".
④ **So sánh hạ thấp cơ sở khác** — "tốt hơn bệnh viện X", "rẻ nhất Hà Nội", hoặc bất
   kỳ câu nói xấu tuyến công.
⑤ **Từ cấm** — `khỏi 100%` · `cam kết 100%` · `không đau` · `an toàn tuyệt đối` ·
   `không biến chứng` · `sạch HP 100%` · `tốt nhất` · `số 1` · `duy nhất` · `rẻ nhất` ·
   `phát hiện 100%` · `cam kết kết quả`.
   ⚠ Chú ý riêng: chữ "không đau" rất hay xuất hiện trong bài về nội soi tiền mê, vì nó
   là cách gọi quen của thị trường ("nội soi không đau"). Đánh dấu MỌI chỗ, rồi phân biệt:
   dùng như TÊN DỊCH VỤ trong ngoặc kép hoặc dẫn lại cách gọi phổ thông thì ghi
   🟠 cần sửa cách diễn đạt; dùng như MỘT KHẲNG ĐỊNH về cảm giác thì ghi 🔴.
⑥ **Ảnh người bệnh / ảnh kết quả nội soi / phiếu kết quả** — có mà không có dấu hiệu
   đã xin đồng ý → 🔴, kèm câu hỏi: đã có văn bản đồng ý chưa.

## Nhóm 🟠 SỬA GẤP — thiếu yêu cầu bắt buộc của THV
⑦ 🚩 **Khối "khi nào cần đi khám ngay"** — BẮT BUỘC có ở mọi bài nói về triệu chứng
   tiêu hóa. Khối đó phải nêu đúng CĐ-1…CĐ-6 (P4 §3): xuất huyết (nôn ra máu, phân đen) ·
   sụt cân nhanh không rõ lý do · khó nuốt tăng dần · thiếu máu không rõ nguyên nhân ·
   đau bụng dữ dội liên tục / khối ở bụng / vàng da · tiền sử gia đình ung thư tiêu hóa.
   Có khối nhưng thiếu dấu hiệu → ghi rõ thiếu mã nào.
⑧ **Byline bác sĩ** — phải có người chịu trách nhiệm chuyên môn, và phải nằm trong
   danh sách đã duyệt (P1 §4). Tên ngoài danh sách → 🟠 kèm ⚠ cần THV xác minh.
⑨ **Giá trong bài** — đối chiếu với P7 bản hiện hành. Lệch, hoặc nêu giá mà không nói
   ba điều kiện (ai thực hiện · có tiền mê không · phụ phí chỉ khi có chỉ định) → 🟠.
   Bài giá cũ không còn đúng là lỗi hay gặp nhất và cũng dễ sửa nhất.

## Nhóm 🟡 SỬA THƯỜNG — chất lượng & chuyển đổi
⑩ **Ngày xuất bản + ngày cập nhật** có hiển thị không.
⑪ **Câu miễn trừ** — nội dung tham khảo, không thay thế chẩn đoán của bác sĩ.
⑫ **Trả lời ở đoạn mở + CTA + nội liên kết** — câu hỏi trong tiêu đề có được trả lời
   ngay đoạn đầu không · có CTA về trang dịch vụ/đặt lịch không · có liên kết tới bài
   cùng cụm không.

# CẤU TRÚC FILE EXCEL — 6 sheet

1. **🔴 Danh sách phải xử lý ngay** — SHEET SỐ 1. Cột:
   URL | Tiêu đề | Vi phạm (mã tiêu chí) | Trích nguyên văn đoạn vi phạm |
   Vì sao là mức CHẶN | Việc phải làm | Ai phụ trách
   → Chỉ chứa mức 🔴. Sắp theo mức nặng: ② → ① → ③ → ⑥ → ④ → ⑤.
   → Không có bài nào: vẫn giữ sheet, ghi rõ đã rà bao nhiêu bài theo 6 tiêu chí nhóm 🔴.

2. **Tổng quan**
   Ngày rà · số URL nhận được · số bài rà được · số bài ⚠ chưa rà được.
   Bảng đếm theo mức: 🔴 / 🟠 / 🟡 / đạt.
   Bảng đếm theo từng tiêu chí ①–⑫: bao nhiêu bài không đạt.
   3 KẾT LUẬN, mỗi dòng một con số.
   **Khối cảnh báo:** bao nhiêu bài chưa rà được và vì sao · tiêu chí nào không kiểm
   được (ví dụ ⑥ ảnh người bệnh thì cần người xem bằng mắt) · P7 dùng để đối chiếu
   giá là bản nào, ngày nào.

3. **Chấm từng bài** — một dòng mỗi URL, cột:
   URL | Tiêu đề | Cụm nội dung (P9 §4) | Nhóm vấn đề TH-xx | ① | ② | ③ | ④ | ⑤ |
   ⑥ | ⑦ | ⑧ | ⑨ | ⑩ | ⑪ | ⑫ | Mức cao nhất | Việc cần làm | Trích dẫn bằng chứng
   → Mỗi tiêu chí: ✔ đạt · ✘ không đạt · ⚠ không kiểm được · "–" không áp dụng.
   → "Không áp dụng" dùng cho ví dụ: bài về bảng giá thì tiêu chí ⑦ (khối cờ đỏ)
     không áp dụng; bài giới thiệu phòng khám thì ⑨ (giá) có áp dụng.
   → Cột "Trích dẫn bằng chứng" BẮT BUỘC có với mọi ✘ ở nhóm 🔴 và 🟠.

4. **🚩 Khối cờ đỏ — bài nào thiếu** — cột:
   URL | Tiêu đề | Nhóm vấn đề | Có khối cờ đỏ? | Thiếu mã CĐ nào |
   Câu đề xuất thêm vào | Vị trí nên đặt
   → Chỉ liệt kê bài có áp dụng tiêu chí ⑦.
   → Cột "Câu đề xuất thêm vào": viết sẵn đoạn văn ngắn liệt kê CĐ-1…CĐ-6 bằng lời
     thường, để người biên tập dán được ngay. Dùng CHUNG MỘT bản cho mọi bài để nội
     dung nhất quán.
   → Vị trí nên đặt: sau phần mô tả triệu chứng, TRƯỚC phần nói về điều trị hoặc chi phí.
     Đặt ở cuối bài thì phần lớn người đọc không tới.

5. **Giá & thông tin động** — cột:
   URL | Con số/thông tin trong bài | Giá trị theo P7 hiện hành | Khớp? |
   Có nêu 3 điều kiện? | Việc cần làm
   Rà cả: giá dịch vụ · giờ làm việc (7h–17h, Thứ 2–Chủ nhật) · địa chỉ (139 Đại La,
   Tương Mai, Hà Nội — MỘT cơ sở) · hotline (0287 306 8668) · số giấy phép
   (4654/HNO-GPHĐ) · tên và chức danh bác sĩ.
   → Đây là sheet dễ sửa nhất và cũng là sheet lệch nhiều nhất, vì mỗi lần đổi giá
     hay đổi giờ làm thì các bài cũ không ai sửa theo.
   → Thông tin không có trong P7 → ghi ⚠ Cần xác minh từ THV, KHÔNG tự sửa theo
     con số tìm thấy ở nơi khác.

6. **Chú giải & cách rà lại** — 12 tiêu chí · 3 mức rủi ro · 6 mã CĐ · 8 cụm nội dung ·
   danh sách bác sĩ được duyệt · danh sách từ cấm · P7 bản nào đang dùng.
   → Kèm một đoạn: muốn chấm tiếp phần SEO và khả năng được AI trích dẫn thì đưa URL
     cho skill `geo-scorecard`, muốn chấm bài trước khi đăng thì dùng `seo-qa-fixer`.
     Hai việc đó không thuộc báo cáo này.

# QUY TẮC
- Bài không đọc được nội dung → ⚠ chưa rà được. ⛔ KHÔNG suy đoán từ tiêu đề hay URL.
- Mọi ✘ ở nhóm 🔴 và 🟠 BẮT BUỘC có trích dẫn nguyên văn.
- ⛔ Không tự sửa bài trong báo cáo này. Báo cáo chỉ ra chỗ sai và viết sẵn câu thay
  thế; việc sửa là của người biên tập.
- Giá đối chiếu với P7 bản hiện hành, ghi rõ bản nào ngày nào. P7 trống ở mục nào thì
  ghi ⚠, không đối chiếu bằng số tìm được ở nơi khác.
- Tên bác sĩ ngoài danh sách duyệt → ⚠ cần THV xác minh, KHÔNG tự xoá, KHÔNG tự coi
  là sai.
- Tiêu chí ⑥ (ảnh người bệnh) cần người xem bằng mắt — nếu chỉ có text thì ghi
  ⚠ không kiểm được, và nêu rõ cần ai kiểm.

# CÁCH LÀM
1. Đọc danh sách URL. Báo: tổng URL · bao nhiêu đọc được nội dung · bao nhiêu không.
   DỪNG LẠI cho tôi xác nhận phạm vi rà.
2. Rà nhóm 🔴 TRƯỚC cho toàn bộ bài đọc được. Nếu có bài mức 🔴, BÁO NGAY trong chat,
   đừng chờ hết báo cáo.
3. Rà nhóm 🟠 và 🟡.
4. In bảng đếm theo mức và theo tiêu chí.
   DỪNG LẠI cho tôi xác nhận.
5. Ghi file.
6. Tự kiểm và báo: mọi ✘ nhóm 🔴/🟠 có trích dẫn chưa · sheet 1 có bỏ sót bài nào mà
   sheet 3 đã ghi 🔴 không · có bài nào bị chấm ⑦ "không đạt" mà thực ra không áp dụng
   không · có chỗ nào tự sửa nội dung thay vì chỉ đề xuất không.
````

## Đến đây

---

## Chuẩn bị dữ liệu đầu vào

**Danh sách URL:** xuất từ `tieuhoaviet.com.vn/sitemap.xml`, hoặc từ danh sách bài trong WordPress (Bài viết → chọn tất cả → xuất). Tối thiểu: URL · tiêu đề. Có thêm ngày cập nhật và tác giả thì rà được tiêu chí ⑧ ⑩ mà không cần mở từng bài.

**Nội dung bài:** ba cách, chọn cách nào tiện:
1. Xuất nội dung từ WordPress (plugin xuất CSV).
2. Dán nội dung từng bài — làm được với lô nhỏ 10–20 bài.
3. Cho trợ lý đọc trực tiếp từ URL, nếu môi trường cho phép.

**Chạy theo lô, đừng chạy cả site một lần.** Thứ tự nên rà: cụm **Giá & điều kiện** trước (lệch nhiều nhất, dễ sửa nhất) → cụm **Triệu chứng → có cần soi** (nhiều bài thiếu khối cờ đỏ nhất) → cụm **điều trị / HP** (nhiều bài có nguy cơ nêu thuốc nhất) → còn lại.

---

## Lưu ý khi dùng

**Sheet 1 báo ngay, không chờ hết báo cáo.** Một bài đang hướng người đọc *"đi ngoài phân đen thì ăn gì cho đỡ"* là bài cần ẩn trong hôm nay, không phải trong báo cáo cuối tháng. Prompt yêu cầu báo ở bước 2.

**Chữ "không đau" là chỗ cần tỉnh táo nhất khi rà.** Cả thị trường gọi nội soi tiền mê là *"nội soi không đau"* — kể cả trang bảng giá của chính THV. Rà máy móc sẽ gắn 🔴 cho hàng loạt bài, và kết quả là không ai sửa gì cả vì danh sách quá dài. Vì vậy tiêu chí ⑤ phân biệt hai cách dùng: **tên dịch vụ** (sửa cách diễn đạt, 🟠) và **khẳng định về cảm giác** (🔴). Khi sửa, cách an toàn là viết *"nội soi tiền mê (thường gọi là nội soi không đau)"* rồi nói thật về cảm giác ngay sau đó.

**Sheet 5 (Giá & thông tin động) là sheet nên chạy lại mỗi lần đổi `P7`.** Mọi lần phòng khám đổi giá, đổi giờ làm, hay thay bác sĩ, các bài cũ vẫn giữ số cũ — và khách đọc bài cũ rồi gọi tới với con số không còn đúng. Đây là nguồn gốc của phần lớn các vụ *"trên web ghi khác"*.

**Báo cáo này không sửa bài.** Nó chỉ ra chỗ sai, viết sẵn câu thay thế, và xếp thứ tự. Lý do: sửa nội dung y khoa cần người có trách nhiệm chuyên môn ký tên — và chính byline đó là một trong 12 tiêu chí đang rà.
