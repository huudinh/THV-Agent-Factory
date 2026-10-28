# R1 — PHÂN LOẠI & KỊCH BẢN HỘI THOẠI

**Trả lời câu hỏi:** *Khách inbox tháng này là ai, đang vướng gì, và nhắn lại thế nào.*

**Cần có:** một file hội thoại đã xuất ra (`.md`, `.txt`, `.docx` hoặc `.xlsx` đều được).
**Nhận lại:** 2 file Excel.

| File | Góc nhìn |
|---|---|
| `output/THV_<DV>_PhanLoai_KichBan.xlsx` | **QUY TRÌNH** — mỗi hội thoại đi trọn 4 bước trên một dòng, có sẵn tin nhắn gửi được ngay |
| `output/THV_KichBan_<DV>.xlsx` | **PHÂN LOẠI + BANK KỊCH BẢN** — chi tiết từng hội thoại + bộ kịch bản theo nhóm A/B/C/Z |

> **Trước khi chạy:** thay `{{FILE}}` và `{{DỊCH VỤ}}` ở đầu prompt. Dịch vụ ví dụ: *Nội soi dạ dày · Nội soi đại tràng · Combo tầm soát · Khám tiêu hóa*.

> 🚩 **Báo cáo này có một việc quan trọng hơn mọi con số trong nó: không để sót ca cờ đỏ.** Sheet đầu tiên của cả hai file là khối cờ đỏ. Kỳ nào không có ca nào thì vẫn giữ sheet, ghi rõ *"không phát hiện ca có dấu hiệu cờ đỏ"*.

> **📎 Có code mẫu sẵn.** Không cần viết `openpyxl` từ đầu — [`tools/xuat_bao_cao.py`](../tools/xuat_bao_cao.py) đã dựng đúng cấu trúc sheet, định dạng và sheet chú giải của báo cáo này:
> ```
> python phan_loai.py --src <file hội thoại> --out rows.json
> python xuat_bao_cao.py --bao-cao R1 --rows rows.json --ky "<kỳ>" --out ../output
> ```
> Ô nào script không tính được thì để `⚠` cho người hoặc trợ lý điền. Style dùng chung ở [`tools/excel_style.py`](../tools/excel_style.py) — sửa quy ước màu ở đó thì đổi cả hệ.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Đọc file hội thoại `{{FILE}}` và sinh ra ĐÚNG 2 file Excel trong thư mục `output/`.
Dịch vụ đang phân tích: {{DỊCH VỤ}}.

Viết script Python dùng openpyxl để tạo file. Không trả bảng trong chat — ghi ra file thật.
Nếu môi trường không chạy được code: nói rõ, rồi trả bảng markdown dán được vào Excel.

# ĐẦU VÀO — cấu trúc file hội thoại
Mỗi hội thoại là một khối:

  ## <STT>. <Tên KH> — <DD/MM HH:MM>
  - Phụ trách: <tên NV> · Có SĐT: <Có|Không> · Số tin: <n>
  - **<DD/MM HH:MM> KH:** <nội dung khách>
  - **<DD/MM HH:MM> NV (<tên NV>):** <nội dung nhân viên>

Quy ước: `[Ảnh]` `[Tệp]` `[Thẻ: …]` là đính kèm hoặc tin tự động, KHÔNG phải chữ khách gõ.
Trường `Có SĐT` lấy nguyên từ dữ liệu, không tự suy luận lại.
File có cấu trúc khác → tự nhận dạng, báo cấu trúc đọc được, rồi tiếp tục. Không bắt tôi sửa file.

# BƯỚC 1 — CHẤM MỘT LẦN, HAI FILE DÙNG CHUNG
Chấm từng hội thoại đúng một lần, lưu kết quả, rồi cả hai file đọc từ kết quả đó.
Hai file BẮT BUỘC khớp nhau tuyệt đối về: cờ đỏ · L-code · độ nóng · nhóm giá trị ·
nhóm vấn đề · giai đoạn. Hai file cho ra con số khác nhau cho cùng một hội thoại là SAI.

## 1a. 🚩 SÀNG CỜ ĐỎ TRƯỚC KHI CHẤM BẤT CỨ THỨ GÌ
Đọc lời KHÁCH, tìm sáu dấu hiệu sau. Có thì gắn mã, không thì để trống:
CĐ-1 nôn ra máu · đi ngoài phân đen · phân như bã cà phê · máu lẫn trong phân
CĐ-2 sụt cân nhanh không rõ lý do (kèm triệu chứng tiêu hóa)
CĐ-3 khó nuốt tăng dần · nuốt đau · nuốt nghẹn
CĐ-4 thiếu máu không rõ nguyên nhân (da xanh, xét nghiệm thiếu máu)
CĐ-5 đau bụng dữ dội liên tục · sờ thấy khối ở bụng · vàng da
CĐ-6 tiền sử gia đình ung thư dạ dày / đại tràng trực hệ (bố, mẹ, anh chị em ruột)

Ca có cờ đỏ: nhóm vấn đề = TH-01, độ nóng = HOT (ghi đè), nhóm khách = Z, kịch bản = X5.
PHÂN BIỆT BẮT BUỘC: máu ĐỎ TƯƠI khi đi ngoài (kèm rát, kèm trĩ) → TH-06, KHÔNG phải cờ đỏ.
Phân ĐEN, máu lẫn phân, phân như bã cà phê → CĐ-1, LÀ cờ đỏ.
Không chắc → gắn cờ và ghi "⚠ cần bác sĩ xác nhận". Thà gắn thừa còn hơn bỏ sót.

⛔ TUYỆT ĐỐI KHÔNG: viết ra khả năng khách mắc bệnh gì · viết "có thể là ung thư" ·
   viết câu trấn an. Nội dung gợi ý cho ca cờ đỏ chỉ được mời khám sớm và ghi
   "đã chuyển bác sĩ". Không nêu giá trong tin nhắn cho ca cờ đỏ.

## 1b. Chấm 5 tín hiệu (mỗi tín hiệu 1 điểm)
① Nêu triệu chứng / chỉ định CỤ THỂ ("đau thượng vị 2 tháng", "đi ngoài ra máu",
   "bác sĩ bảo cần soi đại tràng", "cần soi lại sau cắt polyp")
   — không tính "khám tiêu hóa", "tư vấn giúp em"
② Mốc thời gian dự kiến ≤ 14 ngày, hoặc đã đặt lịch, hoặc đang đến phòng khám
③ Hỏi lịch, bác sĩ, giá, hoặc CÁCH CHUẨN BỊ theo đúng tình trạng của mình
   ("ca của em soi loại nào", "em huyết áp cao thì mê được không")
   — không tính câu hỏi giá chung chung ở tin đầu
④ Gửi kết quả nội soi / xét nghiệm / đơn thuốc / phiếu hẹn, hoặc mô tả rõ:
   triệu chứng · bao lâu · đã khám hay uống thuốc gì
⑤ Để lại SĐT/Zalo thật và đồng ý nhận tư vấn (ưu tiên có nêu khung giờ)

→ HOT 4–5 · WARM 2–3 · COLD 0–1.
Ghi bitmask 5 chữ số, ví dụ `[10110]` = có ①③④, thiếu ②⑤.

## 1c. BỐN LUẬT GHI ĐÈ — đặc thù ngành tiêu hóa, bắt buộc áp
① Đã đặt lịch hoặc đang đến phòng khám → HOT bất kể điểm.
② 🚩 CÓ CỜ ĐỎ → HOT bất kể điểm. Đây là LUẬT AN TOÀN, không phải luật bán hàng:
   nó tồn tại để ca này được gọi trước mọi ca khác, không phải để nói ca này dễ chốt.
③ ĐÃ CÓ KẾT QUẢ nội soi/CT/xét nghiệm từ nơi khác, hoặc đã được bác sĩ nơi khác
   CHỈ ĐỊNH SOI (TH-11) → HOT bất kể điểm. Khách đã qua giai đoạn "có cần soi hay
   không", chỉ còn chọn nơi làm. Đây là lead nóng nhất của ngành, mà thang 5 tín hiệu
   thường chấm thấp oan vì tin nhắn của họ rất ngắn.
④ ĐANG TRONG VÒNG THEO DÕI / ĐẾN HẸN SOI LẠI (TH-02) → tối thiểu WARM.
   Nhóm này viết tin ngắn, không có triệu chứng cấp, nhưng gần như chắc chắn soi.

Ghi rõ khi áp ghi đè: `[01011] → HOT (ghi đè ③: đã có kết quả nơi khác)`.

# BỘ MÃ BẮT BUỘC — không tự chế mã mới

## Giai đoạn hành trình
S1 · NHẬN BIẾT — hỏi chung, hỏi giá/địa chỉ/giờ làm ngay từ đầu, chưa kể triệu chứng (Cold)
S2 · TÌM HIỂU — kể triệu chứng, gửi kết quả cũ, hỏi quy trình, hỏi mê, hỏi ai soi (Warm)
S3 · CÂN NHẮC & NỖI SỢ — sợ nôn/đau, ngại mê, ngờ dây soi, so sánh bệnh viện công,
     hỏi người nhà, chần chừ giá hoặc thời gian, HOẶC lùi lịch mà không hỏi thêm gì
     (Warm→Hot) ★ điểm quyết định
CS · Sau nội soi / đang theo dõi / đến hẹn soi lại / hỏi cho người nhà

## L-code (trạng thái vận hành, chuẩn P6)
L1.1 lần đầu nhắn chưa tư vấn · L2.1 đang tư vấn hợp tác · L2.3 chưa phản hồi lại
L2.4 hẹn nhắn lại sau · L2.5 NGOÀI HÀ NỘI / quá xa 139 Đại La · L4.1 có SĐT + nhu cầu rõ
L5.3 gọi không bắt máy · L5.4 từ chối nghe điện thoại · L5.5 hẹn gọi lại · L5.6 chỉ Zalo
L6.1 chưa rõ rào cản · L6.2 so sánh nơi khác (bệnh viện công hoặc cơ sở tư)
L6.3 chưa tài chính / hỏi bảo hiểm · L6.4 chưa sắp xếp được thời gian / sợ nghỉ làm
L6.5 SỢ NỘI SOI (nôn, sặc, đau, sợ uống thuốc làm sạch ruột)
L6.6 hỏi ý kiến người thân
L6.7 NGẠI TIỀN MÊ (sợ thuốc mê ảnh hưởng tim/trí nhớ, "không tỉnh lại", có bệnh nền)
L6.8 NÉ KẾT QUẢ (biết nên soi nhưng trì hoãn vì sợ phát hiện ra bệnh)
L6.9 NGỜ VỆ SINH DÂY SOI (sợ lây nhiễm từ người soi trước)
     → L6.7 · L6.8 · L6.9 là ba mã riêng của ngành tiêu hóa, KHÔNG gộp vào nhau
       và KHÔNG gộp vào L6.5.

THV CHỈ CÓ 1 CƠ SỞ: 139 Đại La, Tương Mai, Hà Nội. Khách NGOÀI Hà Nội → L2.5.
Khách TRONG Hà Nội mà bảo xa/bận → L6.4, vẫn còn cửa.

## PHÂN BIỆT L6.4 vs L6.8 — chỗ dễ sai nhất của báo cáo này
Cả hai đều nói "để em sắp xếp đã". Khác ở chỗ:
- L6.4 (NGẠI thời gian): sau khi lùi, VẪN HỎI TIẾP về lịch, về mất bao lâu, về việc
  nghỉ làm, về Chủ nhật có làm không.
- L6.8 (NÉ kết quả): lùi mà KHÔNG HỎI THÊM GÌ, và trước đó đã hỏi rất kỹ về triệu
  chứng hoặc về ung thư. Hẹn một mốc xa và mơ hồ ("qua Tết", "ổn định rồi em đi").
  Thường đã từng hẹn rồi hoãn ít nhất một lần. Hay hỏi "soi ra bệnh thì sao".
Không chắc → ghi L6.1 kèm ghi chú, ĐỪNG ĐOÁN. Xếp sai nhóm này là gửi sai nội dung:
gửi ưu đãi giảm giá cho người đang sợ kết quả là đẩy họ xa thêm.

## 12 nhóm vấn đề tiêu hóa — xét ưu tiên từ trên xuống, TH-01 LUÔN THẮNG
TH-01 🚩 CỜ ĐỎ — dấu hiệu cần khám ngay (xem bước 1a)
TH-02 theo dõi sau can thiệp · đến hẹn soi lại (đã cắt polyp, Barrett, loạn sản, bác sĩ hẹn)
TH-03 tầm soát ung thư · không triệu chứng (ngoài 40 tuổi, khám định kỳ, phòng xa)
TH-04 dạ dày – thực quản (đau thượng vị, trào ngược, ợ nóng, viêm loét, đầy bụng sau ăn)
TH-05 đại tràng – trực tràng (táo bón, tiêu chảy kéo dài, đi ngoài nhiều lần, đau quặn)
TH-06 chảy máu thấp · trĩ – hậu môn (máu ĐỎ TƯƠI, trĩ, rát, nứt kẽ)
TH-07 polyp · khối u đã biết (đã phát hiện polyp, cần cắt)
TH-08 gan – mật – tụy (men gan cao, gan nhiễm mỡ, sỏi mật, viêm gan B/C, vàng da)
TH-09 rối loạn tiêu hóa chung (khó tiêu, đầy hơi, chướng bụng, buồn nôn)
TH-10 nhiễm HP · kết quả xét nghiệm HP (HP dương, diệt HP không khỏi, cả nhà có HP)
TH-11 mang kết quả nơi khác đến (đã soi ở đâu, có kết quả, bác sĩ kia bảo)
TH-12 chưa rõ / hỏi chung

Khách vừa trào ngược vừa sụt cân nhanh → TH-01, ghi chú "kèm trào ngược".
Khách đã có kết quả nơi khác → LUÔN là TH-11, kể cả đã nêu triệu chứng gì,
  vì cách tư vấn khác hoàn toàn (⛔ không đọc kết quả qua inbox, mời bác sĩ đọc).
Khách đến hẹn soi lại → LUÔN là TH-02, không xếp theo bệnh cũ.

## Nhóm giá trị — CỘT RIÊNG, không gộp vào độ nóng
G1 giá trị lớn: combo nội soi dạ dày + đại tràng (± tiền mê) · can thiệp nội soi
   (cắt polyp, cầm máu) · gói tầm soát do chuyên gia thực hiện · soi kèm sinh thiết
G2 giá trị trung: nội soi dạ dày HOẶC đại tràng đơn lẻ (thường hoặc tiền mê) · soi + test HP
G3 giá trị nhỏ / cửa vào: khám chuyên khoa · nội soi trực tràng · sigma · siêu âm · test HP

LƯU Ý KHI VIẾT KHUYẾN NGHỊ: một lead WARM của combo tầm soát (WARM·G1) đáng đầu tư
hơn một lead HOT của khám đầy hơi (HOT·G3). Không xếp hạng lead chỉ bằng độ nóng.
Nhóm TH-03 (tầm soát) và TH-02 (tái soi) thường là G1 mà hay bị chấm WARM/COLD —
đừng để bảng xếp hạng đẩy họ xuống cuối.

## 4 rào cản
SỢ → L6.5, L6.7 · NGỜ → L6.2, L6.9 · NGẠI → L6.3, L6.4, L2.5 · NÉ → L6.8
Một hội thoại có thể mang nhiều rào cản. Đếm theo lượt, và ghi rõ cách đếm ở đầu bảng.

## Nhóm đối tượng theo insight
NHÓM Z — 🚩 CA CỜ ĐỎ (đứng ngoài A/B/C, xử lý trước mọi nhóm)
NHÓM A — chưa để lại SĐT (mục tiêu: xin số)
  A1 hỏi giá ngay chưa kể triệu chứng · A2 triệu chứng dai dẳng đã tự uống thuốc
  A3 tầm soát chủ động / chưa có triệu chứng · A4 sợ nội soi hoặc ngại tiền mê
  A5 ở xa Hà Nội · A6 mang kết quả nơi khác đến · A7 né kết quả (L6.8)
NHÓM B — đã để lại SĐT (mục tiêu: kết nối → đến khám → soi được)
  B1 vừa cho số · B2 chưa kết nối được · B3 chỉ nhắn Zalo
  B4 đã gọi còn rào cản · B5 đã đặt lịch — CẦN DẶN CHUẨN BỊ
NHÓM C — sau nội soi (LTV)
  C1 vừa soi xong / đang theo dõi · C2 đến hẹn soi lại · C3 giới thiệu người nhà
Loại — không phải khách hàng (B2B chào bán, tuyển dụng)

## Mã kịch bản
S1.1 hỏi giá ngay · S1.2 hỏi địa chỉ / giờ làm / Chủ nhật có làm không
S1.3 chào mở chưa rõ nhu cầu
S2.1 đã kể triệu chứng → ghi nhận + nói phạm vi bác sĩ cần đánh giá + mời khám + xin số
S2.2 hỏi quy trình / soi loại nào / mất bao lâu / có phải nằm lại không
S2.3 hỏi mê hay không mê → nói thật cảm giác, nêu bác sĩ gây mê theo dõi riêng
S2.4 hỏi ai thực hiện → nêu bác sĩ trong danh sách duyệt + mức giá tương ứng
S2.5 tầm soát chủ động → nói bằng tuổi và nguy cơ, không hù bệnh
S3.1 sợ nội soi (nôn, đau) · S3.2 ngại tiền mê / có bệnh nền
S3.3 ngờ vệ sinh dây soi · S3.4 so sánh bệnh viện công hoặc nơi khác
S3.5 chưa tài chính / hỏi bảo hiểm · S3.6 chưa sắp xếp thời gian (nhắc mở CẢ CHỦ NHẬT)
S3.7 NÉ KẾT QUẢ — nói về lợi ích biết sớm, hẹn mốc cụ thể, KHÔNG gửi ưu đãi
S3.8 hỏi người thân / người nhà đặt hộ · S3.9 ở xa Hà Nội (gộp mọi việc vào 1 buổi)
S3.10 muốn đặt lịch → chốt buổi khám + DẶN CHUẨN BỊ
S4.1 mang kết quả nơi khác đến → mời bác sĩ đọc trực tiếp, không bình luận nơi cũ
S4.2 đến hẹn soi lại → nhắc theo mốc trong phiếu kết quả
X1 xin SĐT đúng cách · X2 gọi nhỡ · X3 chỉ Zalo · X4 nuôi dưỡng COLD/im lặng
X5 🚩 CA CỜ ĐỎ — mời khám trong ngày, không nêu giá, ghi rõ đã chuyển bác sĩ
X6 DẶN CHUẨN BỊ trước buổi hẹn (nhịn ăn, mang kết quả cũ, người đưa về nếu mê)
CS sau nội soi: hướng dẫn chung + nhắc mốc tái soi + mời người nhà cùng tầm soát

Nhiều mã dùng kèm thì nối bằng ` · ` — ví dụ `S3.2 · X1`.

# FILE 1 — output/THV_<DV>_PhanLoai_KichBan.xlsx
Góc nhìn: QUY TRÌNH. Mỗi hội thoại đi trọn 4 bước trên một dòng. 6 sheet, đúng thứ tự:

1. **🚩 Cờ đỏ** — ĐẶT TRƯỚC MỌI SHEET KHÁC. Cột:
   STT | Mã cờ (CĐ-x) | Trích dẫn lời khách (che SĐT) | Nhóm vấn đề | Có SĐT |
   Nhân viên phụ trách | NV có nhận ra không (Có/Không) | NV có trấn an sai không (Có/Không) |
   Việc phải làm ngay
   → Dòng nào cột "NV có trấn an sai" = Có thì tô đỏ đậm, và ghi lên đầu sheet.
   → Không có ca nào: vẫn giữ sheet, ghi "Kỳ này không phát hiện ca có dấu hiệu cờ đỏ"
     và nêu rõ đã sàng theo 6 mã CĐ-1…CĐ-6.
2. **Tổng quan** — tiêu đề, nguồn dữ liệu, ngày lập; sơ đồ 4 bước
   ① ĐỐI TƯỢNG → ② NHÓM → ③ KỊCH BẢN → ④ NỘI DUNG;
   bảng 5 tín hiệu + 4 luật ghi đè; bảng HOT/WARM/COLD; bảng giai đoạn S1–S3·CS;
   bảng nhóm giá trị G1/G2/G3; kết quả phân loại (đếm thật);
   6 nguyên tắc bắt buộc khi dùng nội dung.
3. **Chú giải ký hiệu** — giải nghĩa mọi ký hiệu dùng trong file:
   ⚠ · 🚩 và 6 mã CĐ · giai đoạn S · nhóm chăm sóc · L-code (có L6.7 · L6.8 · L6.9) ·
   mã nhóm vấn đề TH-xx · nhóm giá trị G1/G2/G3 · mã kịch bản · `[ … ]` chỗ cần điền ·
   `{ … }` biến lấy từ P7 · `·` phân tách mã · `→` bước kế tiếp · nhịp T/D · quy ước màu.
4. **Khung 5 bước B1-B5** — khung tư vấn chuẩn, cột: Bước | Làm gì | Câu mẫu | Lưu ý.
   Bước B2 phải ghi rõ 5 THÔNG TIN BẮT BUỘC: triệu chứng + bao lâu · 🚩 có dấu hiệu
   cờ đỏ không · đã khám/soi ở đâu chưa, có kết quả không · BỆNH NỀN & THUỐC ĐANG DÙNG ·
   thời gian dự kiến.
   Bước B5 phải ghi rõ 4 thứ: tên người sẽ gọi · số sẽ gọi · giờ gọi · DẶN CHUẨN BỊ.
5. **Quy trình <N> HT** — một dòng mỗi hội thoại, cột đúng thứ tự:
   STT | Tên khách | 🚩 Cờ đỏ | Nhóm vấn đề (TH-xx) | Triệu chứng / Nhu cầu | Giai đoạn |
   Nhóm KH (insight) | Nhóm giá trị | Nhóm chăm sóc | Kịch bản (mã) | Tên kịch bản |
   Nội dung gợi ý gửi ngay | Rào cản / ghi chú
   → Cột "Nội dung gợi ý gửi ngay" phải là TIN NHẮN gửi được ngay, đã cá nhân hoá theo
     tình trạng của chính khách đó (triệu chứng gì, bao lâu, điều khách vừa lo),
     không phải mô tả việc cần làm.
6. **Nhịp chăm sóc** — cột: Nhóm | Khi nào dùng | Nhịp chạm | Kịch bản gợi ý | Điều kiện dừng.
   Tối thiểu các nhóm: 🚩 cờ đỏ · HOT·G1 · HOT·G2–G3 · HOT gọi nhỡ · WARM·G1 (nuôi dài) ·
   WARM·G2–G3 · COLD · L6.8 né kết quả (nhịp RIÊNG) · ở xa Hà Nội · đã đặt lịch (dặn
   chuẩn bị) · đến hẹn soi lại.
   Ghi rõ ba nhịp khác nhau: chuỗi T+0→T+7 sau khi xin số (có mốc T+48h gửi hướng dẫn
   chuẩn bị và T–1 ngày nhắc lại) · D+3/D+7/D+15 cho L6.x · D+7/D+21/D+45 cho L6.8.
   Ghi rõ: L6.x·G1 nuôi tới 90 ngày, L6.8 nuôi tới 180 ngày bằng nội dung giáo dục,
   các nhóm khác 30 ngày.
   Chốt bằng dòng trần nhắn: tối đa 6 lần / 7 ngày, khách từ chối thì dừng.

# FILE 2 — output/THV_KichBan_<DV>.xlsx
Góc nhìn: PHÂN LOẠI + BANK KỊCH BẢN theo nhóm đối tượng. 6 sheet, đúng thứ tự:

1. **🚩 Cờ đỏ** — giống sheet 1 của file 1, cùng con số.
2. **Tổng quan** — kết quả phân loại (tổng HT · có/không SĐT kèm % · HOT/WARM/COLD ·
   phân bố G1/G2/G3 · số ca cờ đỏ · đã đặt lịch · đã soi);
   bảng nhóm đối tượng Z/A/B/C kèm insight từng nhóm;
   bảng phân bố 12 nhóm vấn đề tiêu hóa;
   **mục "Lỗi quan sát trong data — phải tránh"**: trích số hiệu hội thoại thật làm
   dẫn chứng cho từng lỗi trong 9 lỗi cấm (trấn an ca cờ đỏ · chẩn đoán/loại trừ bệnh ·
   đọc kết quả qua inbox · tư vấn thuốc · nói "không đau" · hứa chắc tiền mê được ·
   lờ câu hỏi giá · báo giá thiếu điều kiện · mời khám mà không dặn chuẩn bị / xin số
   rồi để yên);
   mục biến số từ P7, mọi số gắn ⚠.
3. **Chú giải ký hiệu** — theo cột của file này: cột SĐT · 🚩 Cờ đỏ · Nhóm vấn đề ·
   Ghi chú (bitmask) · Nhóm ĐT · L-code · Độ nóng · Nhóm giá trị · nhịp chăm sóc · ⚠ ·
   lưu ý cốt lõi BA TRỤC + MỘT CỜ không gộp.
4. **Phân loại <N> HT** — một dòng mỗi hội thoại, cột đúng thứ tự:
   STT | Tên KH | Ngày | Phụ trách | Số tin | SĐT | 🚩 Cờ đỏ | Nhóm vấn đề | Nhóm ĐT |
   L-code | Độ nóng | Nhóm giá trị | Rào cản | Ghi chú (tín hiệu ①②③④⑤)
   → Cột Ghi chú: bitmask `[01011]` + dấu hiệu quan sát (gửi kết quả cũ, kể triệu chứng
     bao lâu, hỏi giá, ở xa, sợ nôn, ngại mê, hỏi dây soi, so sánh viện công, hỏi người
     nhà, bận, lùi không hỏi thêm gì).
   → Áp luật ghi đè thì ghi rõ: `[01011] → HOT (ghi đè ③: đã có kết quả nơi khác)`.
5. **Kịch bản <DV>** — bank kịch bản theo nhóm đối tượng, cột:
   Nhóm | Mã | Giai đoạn | Insight khách hàng (nỗi lo thật) | Rào cản | L-code |
   Nhóm giá trị | Khi nào dùng | Nội dung 1 | Nội dung 2 | Nội dung 3 | Lưu ý an toàn
   → Mỗi mã Z, A1–A7, B1–B5, C1–C3 một dòng.
   → Dòng Z (cờ đỏ): cột nội dung CHỈ được mời khám sớm + ghi đã chuyển bác sĩ.
     ⛔ Không nêu giá, ⛔ không trấn an, ⛔ không nêu khả năng mắc bệnh gì.
6. **Chăm sóc theo độ nóng × giá trị** — cột:
   Độ nóng | Nhóm giá trị | Số lead | Nghĩa | Tín hiệu nhận biết | SLA kết nối |
   Nhịp chăm sóc | Hành động | Mục tiêu
   → Tối thiểu 9 dòng (3 độ nóng × 3 nhóm giá trị) + 1 dòng riêng cho 🚩 cờ đỏ.
   → Cột "Số lead" phải khớp con số đếm được ở bước 1.
   → SLA: cờ đỏ ≤5' gọi trước mọi ca · HOT·G1 ≤10' · HOT·G2–G3 ≤15' · WARM ≤30'.
     Phòng khám mở 7h–17h CẢ CHỦ NHẬT → SLA áp cho cả 7 ngày.

# QUY TẮC VIẾT NỘI DUNG KỊCH BẢN
- Nội dung là TIN NHẮN gửi khách, viết sẵn để trực page dán — không phải hướng dẫn.
- Mỗi tin một giá trị mới, 2–4 dòng, một câu hỏi chính.
- Trả lời câu khách hỏi TRƯỚC, rồi mới hỏi câu mới.
- Không lờ câu hỏi giá: bảng giá của THV là CÔNG KHAI, nêu khung được. Nhưng phải kèm
  BA ĐIỀU KIỆN: ai thực hiện · có tiền mê hay không · phụ phí (sinh thiết, cắt polyp)
  chỉ phát sinh khi có chỉ định.
- CTA là ĐẾN KHÁM với bác sĩ tiêu hóa, nói rõ BÁC SĨ XEM XONG MỚI QUYẾT ĐỊNH CÓ SOI
  và soi loại nào. Dễ nhận hơn mời soi — dùng nó, đừng nhảy thẳng vào "đặt combo".
- MỜI KHÁM LÀ PHẢI DẶN CHUẨN BỊ, để khách soi được luôn trong buổi đó nếu bác sĩ chỉ
  định. Thiếu câu này là nguyên nhân số một của việc khách đến tận nơi mà không soi được.
  ⚠ Dùng bản hướng dẫn chuẩn bị chính thức của THV `{hướng_dẫn_chuẩn_bị}` — KHÔNG tự
  nêu số giờ nhịn ăn hay cách uống thuốc làm sạch đại tràng.
- Đề nghị = chọn giữa 2 phương án, không hỏi có/không. Nhắc MỞ CẢ CHỦ NHẬT khi khách
  vướng thời gian — đây là lợi thế thật và là đòn bẩy gỡ L6.4.
- Xin SĐT kèm lý do có lợi cho khách ("để bác sĩ xem trước và sắp lịch đúng buổi anh/chị
  tiện") + 2 khung giờ cụ thể, tối đa 2 lần/hội thoại. ❌ Không xin số "để gửi ưu đãi".
- Nhóm SỢ (L6.5, L6.7) và NÉ (L6.8): mở đầu bằng GHI NHẬN CẢM GIÁC của khách,
  không mở đầu bằng ưu đãi.
- KHÔNG HÙ BỆNH. Không dùng câu "để lâu thành ung thư đấy". Nói về lợi ích của việc
  biết sớm, không về hình phạt của việc chậm.
- Chưa rõ giới tính → xưng "mình". Khách đặt hộ người nhà → chuyển giọng sang người đặt.
- `[ … ]` = chỗ điền theo tình huống. `{ … }` = biến lấy từ P7, luôn kèm ⚠.

# QUY TẮC AN TOÀN — kiểm trước khi ghi file
- 🚩 ❌ KHÔNG trấn an ca có cờ đỏ. Câu "không sao đâu" trong hội thoại có cờ đỏ là lỗi
  nặng nhất của hệ này — ghi lên sheet 1, kèm trích dẫn.
- ❌ KHÔNG chẩn đoán, không loại trừ bệnh ("không phải ung thư đâu", "chỉ là viêm thôi").
- ❌ KHÔNG đọc kết quả nội soi / xét nghiệm / giải phẫu bệnh của khách.
- ❌ KHÔNG tư vấn thuốc, liều, phác đồ — kể cả phác đồ diệt HP.
- ❌ Từ cấm: `khỏi 100%` · `cam kết 100%` · `không đau` · `an toàn tuyệt đối` ·
  `không biến chứng` · `sạch HP 100%` · `tốt nhất` · `số 1` · `duy nhất` · `rẻ nhất` ·
  `chắc chắn không phải ung thư` · `không cần soi đâu` · `phát hiện 100%`.
- ❌ KHÔNG hứa chắc tiền mê được khi chưa biết bệnh nền — phải khám sàng lọc trước.
- ❌ KHÔNG chốt giá cứng cho ca cụ thể. Nêu khung giá công khai kèm 3 điều kiện thì được.
- ❌ Chỉ nêu bác sĩ trong danh sách đã duyệt (P1 §4). Tên khác → ⚠ cần xác minh.
- ❌ KHÔNG hứa có cơ sở gần khách. THV chỉ có 139 Đại La, Hà Nội.
- ❌ KHÔNG nói xấu tuyến công khi khách so sánh bệnh viện công.
- ❌ KHÔNG bịa ca bệnh, giải thưởng, tỷ lệ phát hiện.
- ⚠ Mọi con số giá / % / ngày / hotline / địa chỉ phải gắn ⚠ và ghi rõ cần xác minh.
- Không đưa SĐT, link, kết quả xét nghiệm, ảnh nội soi, hay thông tin định danh của
  khách vào file đầu ra. Tên khách giữ như file nguồn, không bổ sung gì thêm.

# TRÌNH BÀY EXCEL
- Font Arial toàn bộ. Freeze dòng tiêu đề. Wrap text ở các cột nội dung dài.
- Tiêu đề bảng: nền đậm, chữ trắng, in đậm.
- Độ rộng cột đặt theo nội dung; cột nội dung tin nhắn tối thiểu 60.
- Màu quy ước: ĐỎ ĐẬM cho mọi dòng có cờ đỏ · xanh nhạt bước ①/giai đoạn S1 ·
  cam nhạt bước ② · xanh lá nhạt bước ③ · vàng bước ④ và mọi ô có ⚠ · đỏ nhạt HOT ·
  cam WARM · xanh dương nhạt COLD · viền đậm cho dòng nhóm giá trị G1.

# CÁCH LÀM — theo thứ tự
1. Đọc và tách toàn bộ hội thoại. Báo số lượng tách được, đối chiếu với tiêu đề file.
   Báo luôn: bao nhiêu có SĐT · khoảng thời gian dữ liệu · bao nhiêu thiếu dấu thời
   gian · 🚩 BAO NHIÊU CA CÓ DẤU HIỆU CỜ ĐỎ và số hiệu từng ca · mẫu này là toàn bộ
   hay đã bị lọc.
   DỪNG LẠI cho tôi xác nhận trước khi chấm.
2. Chấm 5 tín hiệu + 4 luật ghi đè cho từng hội thoại, lưu một bảng kết quả duy nhất.
3. In ra bảng đếm: tổng HT · có/không SĐT · HOT/WARM/COLD · phân bố G1/G2/G3 ·
   phân bố 12 nhóm vấn đề · phân bố giai đoạn · phân bố 4 rào cản · số ca cờ đỏ.
   DỪNG LẠI cho tôi xác nhận con số trước khi viết kịch bản.
4. Sinh bank kịch bản cho các mã có xuất hiện trong dữ liệu.
   Mã không có hội thoại nào → ghi "⚠ chưa có ca trong kỳ", không viết lấp.
5. Ghi 2 file Excel.
6. Tự kiểm và báo: mọi ca cờ đỏ đã lên sheet 1 của CẢ HAI file chưa · hai file có khớp
   nhau về cờ đỏ / L-code / độ nóng / nhóm giá trị / nhóm vấn đề của từng hội thoại không ·
   tổng số lead ở sheet "Chăm sóc theo độ nóng × giá trị" có bằng tổng đếm được không ·
   còn sót từ cấm hoặc số chưa gắn ⚠ không · có chỗ nào chẩn đoán hoặc trấn an không.
````

## Đến đây

---

## Lưu ý khi dùng

**Sheet cờ đỏ đọc trước, không đọc sau.** Một ca nôn ra máu bị trả lời *"chị uống thuốc dạ dày xem sao"* là chuyện nặng hơn mọi con số tỷ lệ trong báo cáo. Vì vậy nó là **sheet số 1 của cả hai file**, và nó vẫn tồn tại ở kỳ không có ca nào — để người đọc biết là **đã sàng**, không phải **chưa sàng**.

**Bước 1 và bước 3 cố tình dừng lại.** Chấm 5 tín hiệu là chỗ dễ lệch nhất — xem con số phân bố trước khi AI viết hàng trăm dòng kịch bản sẽ rẻ hơn nhiều so với sửa sau.

**Hai file phải khớp nhau.** Ở thương hiệu khác trong tập đoàn, bản sinh lần đầu từng bị lệch: một file ghi HOT 47 · WARM 50 · COLD 3, file kia ghi HOT 25 · WARM 57 · COLD 18 **trên cùng 100 hội thoại**. Prompt này ép chấm một lần rồi cả hai file đọc chung kết quả, và yêu cầu tự đối chiếu ở bước 6.

**Chỗ dễ sai nhất của bản tiêu hóa là phân biệt `L6.4` với `L6.8`.** Hai nhóm nói cùng một câu — *"để em sắp xếp đã"* — nhưng cần hai nội dung ngược nhau: nhóm bận thì giải quyết bằng lịch và Chủ nhật; nhóm né kết quả thì **càng nhắc càng xa**, phải đổi sang nội dung giáo dục và nhịp thưa. Prompt đưa dấu hiệu phân biệt và cho phép ghi `L6.1` khi không chắc — **đừng đoán**.

**Đổi dịch vụ khác** chỉ cần thay `{{DỊCH VỤ}}`. Bảng 12 nhóm vấn đề dùng chung cho mọi dịch vụ, không cần sửa.

**File nguồn chứa dữ liệu sức khỏe thật** — triệu chứng, kết quả xét nghiệm, có thể cả ảnh kết quả nội soi. Đây là loại dữ liệu nhạy cảm hơn mọi ngành khác trong tập đoàn. Chạy trên máy nội bộ, và kiểm file đầu ra trước khi chia sẻ.
