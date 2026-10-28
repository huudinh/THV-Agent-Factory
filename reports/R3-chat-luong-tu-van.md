# R3 — CHẤT LƯỢNG TƯ VẤN & KẾ HOẠCH ĐÀO TẠO

**Trả lời câu hỏi:** *Nhân viên trực page đang hổng khâu nào, **có bỏ sót ca cờ đỏ không**, mất khách ở bước nào, và tuần tới phải dạy gì cho ai.*

**Cần có:** file hội thoại **có dấu thời gian từng tin** và **tên người phụ trách**.
**Nhận lại:** 1 file Excel — `output/THV_ChatLuongTuVan_<KỲ>.xlsx`, **8 sheet**.

> 🔒 **Báo cáo này có tên người thật.** Dùng cho **đào tạo và định tuyến**, không đưa vào nội dung gửi khách, không chia sẻ ra ngoài nhóm quản lý. Phần xếp hạng cá nhân để sheet riêng, có thể ẩn khi trình bày chung.

> 🚩 **Hai sheet đọc trước mọi sheet khác: sheet 1 (Bỏ sót cờ đỏ) và sheet 8 (Rủi ro pháp lý).** Một ca nôn ra máu bị trả lời *"chị uống thuốc dạ dày xem sao"* là chuyện nặng hơn mọi điểm trung bình trong báo cáo này.

> **📎 Có code mẫu sẵn.** [`tools/xuat_bao_cao.py`](../tools/xuat_bao_cao.py) đã dựng đúng cấu trúc sheet và định dạng:
> ```
> python xuat_bao_cao.py --bao-cao R3 --rows rows.json --ky "<kỳ>" --out ../output
> ```

---

## Thiếu dấu thời gian thì sao

- Tiêu chí ① (phản hồi ≤2 phút) → ghi `⚠ không đo được`, **không cho 0 điểm**.
- Chuẩn đạt đổi từ ≥8/10 thành **≥7/9**, và ghi rõ đã đổi.
- Nói rõ trên sheet Tổng quan rằng điểm của kỳ này không so được với kỳ có đủ dấu thời gian.

Thiếu phần ghi chú nội bộ → tiêu chí ⑧ (phiếu 14 trường) cũng `⚠ không đo được`.
Dữ liệu dừng trước khi khách có lịch → tiêu chí ⑥ (dặn chuẩn bị) `⚠ không đo được`.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Chấm chất lượng tư vấn của trực page từ file hội thoại `{{FILE}}`, kỳ {{KỲ}}.
Sinh ra ĐÚNG 1 file: `output/THV_ChatLuongTuVan_{{KỲ}}.xlsx` — 8 sheet.

Viết script Python dùng openpyxl. Ghi ra file thật.
Môi trường không chạy được code → nói rõ, rồi trả bảng markdown dán được vào Excel.

# VIỆC QUAN TRỌNG NHẤT — LÀM TRƯỚC KHI CHẤM ĐIỂM
🚩 Quét toàn bộ hội thoại tìm 6 dấu hiệu CỜ ĐỎ (CĐ-1…CĐ-6):
CĐ-1 nôn ra máu · phân đen · phân như bã cà phê · máu lẫn phân
CĐ-2 sụt cân nhanh không rõ lý do · CĐ-3 khó nuốt tăng dần / nuốt đau
CĐ-4 thiếu máu không rõ nguyên nhân · CĐ-5 đau bụng dữ dội liên tục / khối ở bụng / vàng da
CĐ-6 tiền sử gia đình ung thư dạ dày – đại tràng trực hệ

Với mỗi ca có cờ đỏ, trả lời ba câu bằng bằng chứng trích dẫn:
① Nhân viên CÓ NHẬN RA không? (có hỏi thêm, có mời khám sớm, có nói sẽ chuyển bác sĩ)
② Nhân viên CÓ TRẤN AN SAI không? ("không sao đâu", "chắc chỉ viêm thôi",
   "chị uống thuốc xem sao", "không phải ung thư đâu")
③ Ca đó kết thúc ở trạng thái nào? (đã đặt lịch / còn ở L6.x / im lặng)

Ca có cờ đỏ mà bị trấn an sai → hội thoại 0/10, đưa lên sheet 1 VÀ sheet 8.
Ca có cờ đỏ mà nhân viên không nhận ra (không hỏi thêm, trả lời như ca thường)
→ tiêu chí ③ = 0, và ghi vào sheet 1 với mức rủi ro "bỏ sót".

# BẢNG CHẤM 10 TIÊU CHÍ — CHUẨN ĐẠT ≥ 8/10
① Phản hồi ≤ 2 phút (chênh lệch dấu thời gian tin khách → tin NV đầu tiên)
② Gọi đúng tên dịch vụ / triệu chứng theo post khách bấm vào
   — không hỏi chung "anh/chị cần tư vấn gì"
③ 🚩 SÀNG CỜ ĐỎ — có hỏi hoặc có nhận ra dấu hiệu cờ đỏ; ca có cờ đỏ được mời khám
   sớm và ghi nhận chuyển bác sĩ
④ Thu đủ 5 THÔNG TIN: triệu chứng + bao lâu · có cờ đỏ không · đã khám/soi ở đâu chưa
   và có kết quả không · BỆNH NỀN & THUỐC ĐANG DÙNG · thời gian dự kiến
⑤ Tạo tin cậy bằng BẰNG CHỨNG đúng rào cản khách mang (chuyên gia Bạch Mai · hệ
   Fujifilm VP-7000 + AI · giấy phép · bác sĩ gây mê theo dõi riêng · bảng giá công khai)
   — không chỉ dùng tính từ ("uy tín", "yên tâm nhé")
⑥ DẶN CHUẨN BỊ khi mời khám hoặc khi đã có lịch (để soi được luôn nếu bác sĩ chỉ định)
⑦ Xin số có lý do có lợi cho khách ("để bác sĩ xem trước và sắp lịch đúng buổi
   anh/chị tiện"). ❌ "để gửi ưu đãi"
⑧ Phiếu bàn giao đủ 14 trường (có 🚩 cờ đỏ · bệnh nền · kết quả nơi khác)
⑨ Không vi phạm an toàn & pháp lý — xem danh sách lỗi cấm bên dưới
⑩ Nêu rõ bước tiếp theo: ai gọi · số nào · lúc mấy giờ

Mỗi tiêu chí ghi 1 (đạt) · 0 (không đạt) · ⚠ (không đo được).
VI PHẠM TIÊU CHÍ ⑨ → TOÀN HỘI THOẠI 0 ĐIỂM, bất kể 9 tiêu chí kia.
Không đo được thì ghi ⚠ và đổi chuẩn đạt tương ứng, KHÔNG cho 0 điểm oan.

# CHÍN LỖI CẤM — ĐẾM RIÊNG, CÓ TRÍCH DẪN
1. 🚩 Trấn an một ca có cờ đỏ ("không sao đâu", "chắc chỉ viêm thôi")
2. Chẩn đoán hoặc loại trừ bệnh qua tin nhắn ("đây là trào ngược", "không phải ung thư đâu")
3. Đọc kết quả nội soi / xét nghiệm / giải phẫu bệnh của khách qua inbox
4. Tư vấn thuốc, liều, phác đồ — kể cả phác đồ diệt HP
5. Nói "nội soi không đau"
6. Hứa chắc tiền mê được khi chưa biết bệnh nền
7. Lờ câu hỏi giá (khách hỏi giá, NV chỉ đáp "để lại số em tư vấn")
8. Báo giá mà không nói rõ ba điều kiện: ai thực hiện · có tiền mê không ·
   phụ phí (sinh thiết, cắt polyp) chỉ phát sinh khi có chỉ định
9. Mời khám mà không dặn chuẩn bị · hoặc xin số rồi để yên (không nhắn xác nhận
   ai gọi, số nào, mấy giờ)

Lỗi 7 và lỗi 8 là HAI LỖI KHÁC NHAU, đừng gộp: lờ câu hỏi giá là né, báo giá thiếu
điều kiện là nói chưa đủ. Cả hai đều sai, cách sửa ngược nhau.
Lỗi 1 và lỗi 2 cũng khác nhau: trấn an là làm khách hoãn khám, chẩn đoán là nói sai
phạm vi. Lỗi 1 nặng hơn.

# LỖI "TRƯỢT CÂU HỎI NGẦM" — chấm riêng, đây là lỗi hay gặp nhất
| Khách gõ | Thật sự đang hỏi | Trả lời trượt là |
|---|---|---|
| "Nội soi bao nhiêu tiền?" | Có bị cộng thêm khoản gì không | Chỉ bắn con số, không nói 3 điều kiện |
| "Soi có đau không?" | Tôi chịu được không, các anh có nói thật không | Nói "không đau" |
| "Có cần gây mê không?" | Mê có hại không | Chỉ nói "mê thì không biết gì", không nói có bác sĩ gây mê theo dõi |
| "Ai soi cho em?" | Người soi có đủ giỏi để không bỏ sót không | Nói tên mà không nói kinh nghiệm, hoặc không nói mức giá tương ứng |
| "Dây soi dùng chung à?" | Tôi có bị lây bệnh không | Đáp "sạch mà chị" — không nêu quy trình xử lý dây soi |
| "Em bị thế này có sao không?" | Có phải ung thư không | Trấn an, hoặc loại trừ bệnh → đây là lỗi cấm 1 và 2 |
| "Soi ra bệnh thì sao?" | Tôi sợ kết quả, không sợ ống soi | Đáp về cảm giác soi, hoặc gửi ưu đãi |
| "Để qua Tết em đi" | Tôi chưa đủ can đảm / chưa đủ lý do đi ngay | Buông luôn, hoặc gửi ưu đãi giảm giá |
| "Phải nghỉ làm cả ngày không?" | Tính được thời gian thì tôi đi | Chỉ đáp "khoảng 30 phút", không nhắc MỞ CẢ CHỦ NHẬT |
→ Đếm số hội thoại có lỗi này, kèm trích dẫn. Lỗi này KHÔNG trừ vào 10 tiêu chí
  (để tránh trừ hai lần), mà báo thành chỉ số riêng: "tỷ lệ trượt câu hỏi ngầm".
→ Hai dòng cuối bảng là đặc thù của ngành này: nhận sai L6.8 (né kết quả) thành
  L6.4 (bận) thì mọi nội dung sau đó đều trượt. Đếm riêng số ca nhận sai này.

# CẤU TRÚC FILE EXCEL — 8 sheet

1. **🚩 Cờ đỏ — nhận ra hay bỏ sót** — SHEET SỐ 1, đọc trước mọi sheet khác. Cột:
   STT HT | Ngày | Phụ trách | Mã CĐ | Trích nguyên văn lời khách (che SĐT) |
   NV có nhận ra? | NV có trấn an sai? | Trích nguyên văn lời NV | Ca kết thúc ở đâu |
   Mức rủi ro | Việc cần làm ngay
   → Mức rủi ro: "ĐÃ TRẤN AN SAI" (nặng nhất) · "BỎ SÓT" (không nhận ra) ·
     "NHẬN RA, XỬ LÝ ĐÚNG".
   → Dòng "ĐÃ TRẤN AN SAI" tô đỏ đậm. Ghi tổng số ngay dưới tiêu đề sheet.
   → Chốt sheet bằng một dòng: tỷ lệ nhận diện cờ đỏ của kỳ này = <số ca nhận ra> /
     <tổng ca có dấu hiệu>. MỐC LÀ 100% — đây là mốc duy nhất của hệ này không
     thương lượng. Dưới 100% thì ghi rõ cần xử lý trước khi hết kỳ, không chờ báo cáo sau.
   → Không có ca nào: vẫn giữ sheet, ghi "Đã sàng <N> hội thoại theo 6 mã CĐ-1…CĐ-6,
     không phát hiện ca có dấu hiệu cờ đỏ".

2. **Tổng quan**
   Kỳ · dịch vụ · nguồn dữ liệu · số hội thoại chấm được · ngày lập.
   🚩 Tỷ lệ nhận diện cờ đỏ (lấy từ sheet 1) — ĐẶT Ở DÒNG ĐẦU TIÊN.
   Điểm trung bình toàn kỳ · % hội thoại đạt ≥8/10 · số hội thoại bị 0 điểm (vi phạm ⑨).
   Tỷ lệ trượt câu hỏi ngầm. Số ca nhận sai L6.8 thành L6.4.
   Bảng: tiêu chí nào đạt cao nhất / thấp nhất, kèm %.
   **Khối cảnh báo:** tiêu chí nào không đo được và vì sao · chuẩn đạt đã đổi thành gì ·
   mẫu là toàn bộ hay đã lọc · điểm kỳ này có so được với kỳ trước không.
   3 kết luận chính, mỗi dòng một con số.

3. **Chú giải** — 10 tiêu chí · chuẩn đạt · luật 0 điểm · 🚩 6 mã CĐ · 9 lỗi cấm ·
   lỗi trượt câu hỏi ngầm · 4 rào cản · quy ước màu · ⚠.

4. **Chấm từng hội thoại** — một dòng mỗi hội thoại, cột:
   STT | Tên KH | Ngày | Phụ trách | 🚩 Cờ đỏ | Nhóm vấn đề | Nhóm giá trị | Độ nóng |
   ① | ② | ③ | ④ | ⑤ | ⑥ | ⑦ | ⑧ | ⑨ | ⑩ | Tổng điểm | Đạt? |
   Lỗi cấm mắc phải | Trượt câu hỏi ngầm? | Trích dẫn bằng chứng | Ghi chú
   → Cột "Trích dẫn bằng chứng" BẮT BUỘC có với mọi tiêu chí bị 0 và mọi lỗi cấm.
     Bảng điểm không có trích dẫn thì nhân viên không phục và trưởng nhóm không
     đào tạo được.
   → Che số điện thoại. ⛔ Không trích nội dung kết quả xét nghiệm hay chi tiết bệnh án
     ngoài mức cần thiết để thấy vì sao bị trừ điểm.

5. **Tiêu chí nào đang hổng** — cột:
   Tiêu chí | Số HT đạt | Số HT không đạt | Số HT không đo được | % đạt |
   Khâu phễu bị ảnh hưởng | Hậu quả thấy được trong dữ liệu | Học phần cần dạy
   → Sắp xếp theo % đạt tăng dần: tiêu chí hổng nhất lên đầu.
   → Cột "Hậu quả thấy được trong dữ liệu" phải dẫn số thật, ví dụ:
     "22 hội thoại thiếu tiêu chí ⑥ (dặn chuẩn bị) → trong đó 7 ca đã đến khám mà
     phải hẹn lại buổi khác".
   → Tiêu chí ③ (sàng cờ đỏ) và ⑥ (dặn chuẩn bị) là hai tiêu chí riêng của ngành này.
     Nếu cả hai đều hổng, nói rõ: một cái là rủi ro người bệnh, một cái là rò doanh thu
     ở mốc đắt nhất.

6. **Theo người phụ trách** 🔒 — cột:
   Tên NV | Số HT | Điểm TB | % đạt ≥8/10 | Số HT bị 0 điểm | 🚩 Số ca cờ đỏ gặp phải |
   🚩 Số ca bỏ sót hoặc trấn an sai | Tỷ lệ xin được số | Tiêu chí mạnh nhất |
   Tiêu chí yếu nhất | Nhóm (A/B/C/D) | Học phần cần học
   Phân nhóm:
   - **A · Hạt nhân** — điểm TB cao, mạnh đều, không bỏ sót cờ đỏ → làm mentor
   - **B · Yếu khâu chốt** — xin số tốt nhưng thiếu ⑥ ⑩ (không dặn chuẩn bị, không
     nêu bước tiếp theo)
   - **C · Yếu khâu bằng chứng** — thiếu ⑤, hay dùng tính từ thay bằng chứng
   - **D · Yếu khâu an toàn** ⚠ — có ca bỏ sót cờ đỏ, hoặc có vi phạm ⑨.
     **Nhóm này ưu tiên đào tạo trước mọi nhóm khác, bất kể điểm trung bình cao hay thấp.**
   → NV dưới 10 hội thoại trong kỳ: ghi ⚠ chưa đủ mẫu, KHÔNG xếp nhóm, KHÔNG kết luận.
     NGOẠI LỆ: nếu NV đó có ca bỏ sót cờ đỏ thì vẫn ghi vào nhóm D — một ca là đủ,
     đây không phải chỉ số thống kê.
   → Sheet này là dữ liệu nhân sự nội bộ. Ghi chú rõ ở đầu sheet.

7. **Kế hoạch đào tạo 4 tuần** — cột:
   Học phần | Nội dung | Vì sao cần (dẫn số từ sheet 5) | Người học | Mentor đề xuất |
   Tuần | Cách đo kết quả
   Sáu học phần tiêu chuẩn:
   - **M0 🚩 Sàng cờ đỏ & giới hạn chuyên môn** — 6 dấu hiệu CĐ · câu hỏi sàng bằng
     lời thường · xử lý ca cờ đỏ (mời khám sớm, chuyển bác sĩ, không trấn an,
     không nêu giá) · bốn điều tuyệt đối không làm: chẩn đoán, loại trừ bệnh,
     đọc kết quả, tư vấn thuốc.
     **M0 LUÔN NẰM Ở TUẦN 1 nếu sheet 1 có bất kỳ ca bỏ sót hoặc trấn an sai nào.**
   - **M1 Mở hội thoại** — phản hồi 2' · chào theo đúng dịch vụ · 5 câu khám phá
   - **M2 Bằng chứng ngành tiêu hóa** — chuyên gia Bạch Mai · hệ máy + AI · xử lý câu
     "soi có đau không" (không nói "không đau") · xử lý câu "mê có hại không" ·
     xử lý câu "dây soi có sạch không"
   - **M3 Xin số & xác thực** — xin có lý do · kiểm Zalo · hỏi khung giờ · nhắn xác nhận
   - **M4 Chốt lịch + DẶN CHUẨN BỊ** — xử lý 9 lý do từ chối · CTA đến khám (bác sĩ
     quyết định có soi) · nhắc mở cả Chủ nhật · dặn chuẩn bị để soi được luôn ·
     nhận diện L6.8 né kết quả và KHÔNG gửi ưu đãi cho nhóm đó
   - **M5 Phân loại & bàn giao** — HOT/WARM/COLD · nhóm giá trị G · 🚩 cờ đỏ ·
     phiếu 14 trường
   → Chỉ đưa vào kế hoạch học phần nào mà dữ liệu cho thấy đang hổng. Không rải đều.
     NGOẠI LỆ: M0 đưa vào bất kể, nếu có ca cờ đỏ bị xử lý sai.
   → Cột "Cách đo kết quả" phải nêu con số cụ thể sẽ đo lại sau 4 tuần.

8. **Rủi ro pháp lý & an toàn** ⚠ — cột:
   STT HT | Ngày | Phụ trách | Loại vi phạm | Trích nguyên văn | Mức rủi ro | Việc cần làm
   Loại vi phạm: 🚩 trấn an ca cờ đỏ · chẩn đoán / loại trừ bệnh · đọc kết quả ·
   tư vấn thuốc hoặc phác đồ · từ cấm · hứa chắc tiền mê · chốt giá cứng ·
   nêu tên bác sĩ ngoài danh sách duyệt · hứa có cơ sở gần khách.
   → Sắp xếp theo mức rủi ro giảm dần. "Trấn an ca cờ đỏ" luôn ở trên cùng.
   → Sheet này đi lên trước mọi sheet khác khi trình bày, cùng sheet 1.
   → Nếu kỳ này không có vi phạm nào: vẫn giữ sheet, ghi "Không phát hiện vi phạm
     trong <N> hội thoại đã chấm".

# QUY TẮC
- Mỗi tiêu chí bị 0 và mỗi lỗi cấm BẮT BUỘC có trích dẫn nguyên văn.
- Không đo được thì ghi ⚠, không cho 0 điểm. Và ghi rõ chuẩn đạt đã đổi thành gì.
- NV dưới 10 hội thoại: không xếp nhóm, không kết luận — trừ trường hợp có ca cờ đỏ
  bị xử lý sai.
- Che số điện thoại, không đưa thông tin định danh hay dữ liệu sức khỏe của khách
  vào file.
- Không suy ra thái độ hay động cơ của nhân viên. Chỉ ghi hành vi quan sát được
  trong hội thoại.
- Kế hoạch đào tạo phải dẫn số từ sheet 5. Học phần không có số chứng minh đang hổng
  thì không đưa vào — trừ M0.
- ⛔ Không dùng báo cáo này để phạt. Nó chỉ ra HỌC PHẦN NÀO CẦN DẠY, không xếp loại
  nhân sự.

# CÁCH LÀM
1. Tách hội thoại. Báo: số hội thoại · số có dấu thời gian · số có tên phụ trách ·
   số có phần ghi chú nội bộ · 🚩 SỐ CA CÓ DẤU HIỆU CỜ ĐỎ và số hiệu từng ca ·
   tiêu chí nào đo được, tiêu chí nào không.
   DỪNG LẠI cho tôi xác nhận.
2. Dựng sheet 1 (cờ đỏ) TRƯỚC, báo ngay nếu có ca bị trấn an sai — đừng chờ hết báo cáo.
3. Chấm 10 tiêu chí, lưu một bảng kết quả duy nhất.
4. In bảng tóm tắt: tỷ lệ nhận diện cờ đỏ · điểm TB · % đạt · số ca 0 điểm ·
   3 tiêu chí hổng nhất.
   DỪNG LẠI cho tôi xác nhận.
5. Ghi file Excel.
6. Tự kiểm và báo: mọi tiêu chí bị 0 có trích dẫn chưa · mọi ca cờ đỏ ở sheet 1 có
   mặt ở sheet 4 không · có NV nào <10 HT mà vẫn bị xếp nhóm không (trừ nhóm D) ·
   sheet 8 có bỏ sót vi phạm nào mà sheet 4 đã ghi không · kế hoạch đào tạo có học
   phần nào không dẫn được số không.
````

## Đến đây

---

## Lưu ý khi dùng

**Sheet 1 và sheet 8 đọc trước, không đọc sau.** Và sheet 1 **không chờ hết báo cáo** — prompt yêu cầu báo ngay ở bước 2 nếu có ca bị trấn an sai. Lý do đơn giản: nếu một khách nôn ra máu được trả lời *"chị uống thuốc dạ dày xem sao"* cách đây mười ngày, thì việc cần làm là **gọi lại khách đó hôm nay**, không phải đọc con số ở cuối tháng.

**Mốc 100% nhận diện cờ đỏ là mốc duy nhất trong cả repo không thương lượng.** Mọi mốc KPI khác đều ghi `⚠ chờ THV chốt`, vì chúng là chuyện kinh doanh. Mốc này khác: nó không phụ thuộc vào năng lực đội ngũ hay điều kiện thị trường.

**Nhóm D được ưu tiên đào tạo trước, bất kể điểm trung bình.** Một nhân viên có thể đạt 9/10 ở chín hội thoại và bỏ sót một ca cờ đỏ ở hội thoại thứ mười — điểm trung bình vẫn đẹp, nhưng đó là người cần học M0 trước tiên. Bảng điểm trung bình không bắt được việc này, nên sheet 6 có hai cột riêng cho cờ đỏ.

**Sheet 6 là dữ liệu nhân sự.** Khi trình bày cho nhóm, ẩn sheet này hoặc chỉ nói theo nhóm A/B/C/D, không đọc tên kèm điểm trước cả nhóm.

**Tiêu chí ⑥ (dặn chuẩn bị) là tiêu chí rẻ nhất để cải thiện trong cả bảng.** Nó không cần kỹ năng tư vấn, chỉ cần một tin nhắn mẫu đúng và một thói quen gửi nó. Mà nó lại chặn đúng chỗ mất tiền nhiều nhất của ngành: khách đến tận phòng khám rồi phải về vì chưa nhịn ăn. Nếu sheet 5 cho thấy tiêu chí này hổng, đó là việc nên làm trong tuần, không phải trong quý.
