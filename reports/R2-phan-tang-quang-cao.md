# R2 — PHÂN TẦNG POST QUẢNG CÁO + BIỂU ĐỒ NHIỆT

**Trả lời câu hỏi:** *Post nào kéo về khách cần soi thật, post nào chỉ kéo người hỏi giá — và post nào kéo về khách combo tầm soát, post nào kéo về khách khám đầy hơi.*

**Cần có:** danh sách post đang chạy **+** file hội thoại cùng kỳ.
**Nhận lại:** 1 file Excel — `output/THV_PhanTang_QuangCao_<KỲ>.xlsx`, **14 sheet**.

> **📎 Có code mẫu sẵn.** Không cần viết `openpyxl` từ đầu — [`tools/xuat_bao_cao.py`](../tools/xuat_bao_cao.py) đã dựng đúng cấu trúc sheet, định dạng và sheet chú giải của báo cáo này:
> ```
> python phan_loai.py --src <file hội thoại> --out rows.json
> python xuat_bao_cao.py --bao-cao R2 --rows rows.json --posts <file post> --ky "<kỳ>" --out ../output
> ```

---

## Hai chế độ — chọn đúng chế độ trước khi chạy

| Chế độ | Khi nào | Độ tin cậy |
|---|---|---|
| **A · ĐO THẬT** | Có cả danh sách post **và** file hội thoại cùng kỳ | Cao — đếm kết quả thật |
| **B · DỰ ĐOÁN** | Chỉ có post, chưa có hội thoại (post mới, hoặc kỳ cũ không còn log) | Thấp — chỉ là giả thuyết |

**Luôn ưu tiên chế độ A.** Hội thoại xuất từ CRM/Fanpage thường có thẻ nguồn ở tin đầu:

```
[Thẻ: Inbox từ quảng cáo QC_NoiSoiDaDay_TienMe – Nội soi dạ dày không đau…]
```

Thẻ này là **khoá nối** giữa post và hội thoại. Có nó thì không cần đoán.

---

## ⚠ Đọc trước khi tin kết quả

**Mẫu phải là toàn bộ, không được lọc.** File hội thoại chỉ gồm "hội thoại dài" hoặc "hội thoại có số" thì đã **thiên về phía nóng** — dùng để so sánh post sẽ **thổi phồng chất lượng của mọi post, và thổi không đều nhau**.

**Mẫu nhỏ không kết luận được.** Dưới 10 hội thoại thì con số % không nói lên gì → `⚠ chưa đủ mẫu`, **không xếp hạng**.

**Bẫy riêng của ngành tiêu hóa — có hai cái, cả hai đều làm quyết sai ngân sách:**

> **① Bẫy giá trị.** Một post kéo 40 hội thoại hỏi "khám đầy hơi bao nhiêu" và một post kéo 8 hội thoại hỏi combo tầm soát trông rất khác nhau trên bảng `% HOT`, nhưng giá trị thật thì ngược lại — chênh gần **chín lần** về giá dịch vụ. **Bắt buộc đọc bảng phân tầng cùng với sheet 6 (Post × Nhóm giá trị).**
>
> **② Bẫy cờ đỏ.** Luật ghi đè ② đẩy **mọi ca cờ đỏ lên HOT**. Post nào tình cờ kéo nhiều ca cờ đỏ sẽ có `% HOT` rất cao — nhưng đó **không phải chất lượng quảng cáo**, đó là **gánh nặng y tế**. Và nhóm đó thường **không chốt nhanh**, vì họ đang lo chứ không đang mua.
> → **Bắt buộc có cột `% HOT (trừ cờ đỏ)`** ở sheet 4, và **tách `TH-01` ra** khỏi mọi bảng so sánh post. Xếp hạng post bằng `% HOT` có lẫn cờ đỏ là xếp hạng một con số không nói về quảng cáo.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Phân tầng các post quảng cáo theo chất lượng VÀ giá trị khách mà chúng kéo về.
Sinh ra ĐÚNG 1 file: `output/THV_PhanTang_QuangCao_{{KỲ}}.xlsx` — 14 sheet.

Viết script Python dùng openpyxl. Ghi ra file thật, không trả bảng trong chat.
Môi trường không chạy được code → nói rõ, rồi trả bảng markdown dán được vào Excel.

# ĐẦU VÀO
- Danh sách post đang quảng cáo: {{FILE POST}}
- File hội thoại cùng kỳ (nếu có): {{FILE HỘI THOẠI}}
- Dịch vụ: {{DỊCH VỤ}}   — ví dụ: Nội soi dạ dày, Nội soi đại tràng, Combo tầm soát, Tổng quát
- Kỳ: {{KỲ}}             — ví dụ: 01-31/10/2026

Chế độ chạy:
- Có file hội thoại  → CHẾ ĐỘ A (đo thật). Bắt buộc dùng chế độ này.
- Không có           → CHẾ ĐỘ B (dự đoán). Ghi rõ trên MỌI sheet rằng đây là giả thuyết.

# CHẾ ĐỘ A — ĐO THẬT

## A1. Nối post với hội thoại
Đọc thẻ nguồn ở tin đầu của mỗi hội thoại. Chuẩn hoá tên post: gom các biến thể
(cùng nội dung, khác tên chiến dịch / khác đối tượng / khác ngày lên) về một mã post,
và ghi rõ đã gom những biến thể nào.
Hội thoại không có thẻ → xếp "(không rõ nguồn)". Đếm riêng, KHÔNG chia đều cho các post.

## A2. 🚩 SÀNG CỜ ĐỎ TRƯỚC — rồi mới chấm
Với mỗi hội thoại, tìm 6 dấu hiệu cờ đỏ (CĐ-1…CĐ-6, xem khuôn R1 bước 1a).
Ca có cờ đỏ: nhóm vấn đề = TH-01, độ nóng = HOT (ghi đè ②), và ĐÁNH DẤU RIÊNG để
loại ra khỏi mọi phép so sánh post.

## A3. Chấm từng hội thoại (5 tín hiệu — giống R1)
① triệu chứng/chỉ định cụ thể · ② mốc ≤14 ngày · ③ hỏi lịch/bác sĩ/giá/chuẩn bị theo
tình trạng của mình · ④ gửi kết quả cũ hoặc mô tả rõ · ⑤ để lại SĐT + đồng ý.
HOT 4–5 · WARM 2–3 · COLD 0–1. Ghi bitmask.
Bốn luật ghi đè: đã đặt lịch → HOT · 🚩 cờ đỏ → HOT · đã có kết quả nơi khác /
đã được chỉ định soi (TH-11) → HOT · đến hẹn soi lại (TH-02) → tối thiểu WARM.

## A4. Gán nhóm vấn đề và nhóm giá trị cho từng hội thoại
12 nhóm TH-01…TH-12 (xét ưu tiên từ trên xuống, TH-01 luôn thắng).
Nhóm giá trị G1 (combo · can thiệp · gói tầm soát) / G2 (soi dạ dày HOẶC đại tràng
đơn lẻ) / G3 (khám · trực tràng · sigma · siêu âm · test HP).

## A5. Tính cho từng post
Số HT · tỷ lệ có SĐT · HOT/WARM/COLD · % HOT · % HOT (trừ cờ đỏ) · điểm tín hiệu TB ·
phân bố G1/G2/G3 · % G1 · số ca cờ đỏ · nhóm vấn đề chủ đạo · rào cản nổi bật ·
tầng chủ đạo · đủ mẫu hay chưa (≥10 HT).

# CHẾ ĐỘ B — DỰ ĐOÁN TỪ NỘI DUNG
Đọc nội dung post, đoán góc tiếp cận và tầng khách mà nó sẽ kéo về.
Ghi rõ trên MỌI sheet: đây là DỰ ĐOÁN, phải đối chiếu lại khi có hội thoại thật.
Không được in cột % nào trông như số đo thật.

# CẤU TRÚC FILE EXCEL — 14 sheet, đúng thứ tự

1. **🚩 Cờ đỏ theo post** — ĐẶT TRƯỚC MỌI SHEET KHÁC. Cột:
   Mã post | Số ca cờ đỏ | Mã CĐ gặp phải | % trên tổng HT của post | NV có nhận ra |
   NV có trấn an sai | Việc phải làm
   → Sheet này KHÔNG dùng để xếp hạng post. Nó dùng để biết: post nào đang kéo về
     người đang lo bệnh, và ở đó trực page có đủ năng lực xử lý hay không.
   → Nhận định bắt buộc ghi ở cuối sheet: post nào kéo nhiều ca cờ đỏ thì CẦN TRANG BỊ
     TRƯỚC kịch bản X5 cho người trực post đó, không phải cần tăng hay giảm tiền.
   → Không có ca nào: vẫn giữ sheet, ghi rõ đã sàng theo 6 mã CĐ.

2. **Tổng quan**
   Kỳ · dịch vụ · chế độ chạy (A hay B) · nguồn dữ liệu · ngày lập.
   Số post · số hội thoại · số nối được · số không rõ nguồn · số ca cờ đỏ.
   Phân bố HOT/WARM/COLD toàn kỳ. Phân bố G1/G2/G3 toàn kỳ.
   **Khối cảnh báo phương pháp**, ghi rõ:
   - mẫu có phải toàn bộ hội thoại trong kỳ không, hay đã bị lọc
   - nếu đã lọc → kết quả bị thiên về phía nóng, KHÔNG dùng để quyết ngân sách
   - số post chưa đủ mẫu
   - **hai bẫy riêng của ngành tiêu hóa:** ① xếp hạng post chỉ bằng %HOT là quyết sai,
     phải đọc kèm sheet 6 (Post × Nhóm giá trị) · ② %HOT có lẫn ca cờ đỏ là con số
     không nói về quảng cáo, phải đọc cột "% HOT (trừ cờ đỏ)"
   3 kết luận chính, mỗi cái một dòng, có số kèm theo.

3. **Chú giải ký hiệu**
   HOT/WARM/COLD và 5 tín hiệu · 4 luật ghi đè · 🚩 6 mã CĐ · G1/G2/G3 · TH-01…TH-12 ·
   tỷ lệ có SĐT · điểm tín hiệu TB · tầng chủ đạo · ⚠ chưa đủ mẫu · góc tiếp cận ·
   4 rào cản (SỢ/NGỜ/NGẠI/NÉ) · quy ước màu.

4. **Phân tầng theo post** — một dòng mỗi post, cột đúng thứ tự:
   Mã post | Tên post (chuẩn hoá) | Biến thể đã gom | Dịch vụ | Thông điệp chính |
   Góc tiếp cận | Số HT | Tỷ lệ có SĐT | HOT | WARM | COLD | % HOT |
   **% HOT (trừ cờ đỏ)** | Điểm TB | G1 | G2 | G3 | % G1 | 🚩 Số ca cờ đỏ |
   Tầng chủ đạo | Nhóm vấn đề chủ đạo | Đủ mẫu? | Rào cản nổi bật
   → Sắp xếp theo **% HOT (trừ cờ đỏ)** giảm dần, không theo % HOT.
   → Đẩy mọi dòng ⚠ chưa đủ mẫu xuống cuối.

5. **Xếp hạng & khuyến nghị** — cột:
   Hạng | Mã post | % HOT (trừ cờ đỏ) | % G1 | Tỷ lệ có SĐT | Khuyến nghị | Lý do |
   Việc cần làm
   Khuyến nghị chọn trong 5 mức:
   - TĂNG NGÂN SÁCH — %HOT (trừ cờ đỏ) và tỷ lệ có SĐT đều trên trung bình kỳ
   - TĂNG NGÂN SÁCH (giá trị cao) — %HOT quanh trung bình NHƯNG %G1 cao rõ rệt.
     Đây là mức riêng của ngành: post kéo ít khách nhưng toàn khách combo tầm soát /
     can thiệp thì đáng tiền hơn post kéo đông khách khám đầy hơi
   - GIỮ NGUYÊN — quanh mức trung bình
   - SỬA THÔNG ĐIỆP — kéo được nhiều hội thoại nhưng tầng thấp, nêu sửa gì cụ thể
   - XEM XÉT TẮT — vừa ít hội thoại vừa tầng thấp vừa toàn G3
   Post ⚠ chưa đủ mẫu → khuyến nghị bắt buộc là "CHỜ THÊM DỮ LIỆU".
   → Cột "Việc cần làm" phải cụ thể: sửa câu nào, thêm bằng chứng gì, đổi CTA thành gì.

6. **Post × Nhóm giá trị** ⭐ — SHEET QUYẾT ĐỊNH NGÂN SÁCH. Cột:
   Mã post | Góc tiếp cận | Số HT | G1 | G2 | G3 | % G1 | % HOT (trừ cờ đỏ) |
   % HOT trong nhóm G1 | Nhận định
   → Trả lời: post nào kéo về khách giá trị lớn. Đây là sheet quyết định ngân sách,
     không phải sheet 4.
   → Khối "Đọc nhanh" bên dưới nêu rõ: post nào nên tăng tiền dù %HOT thấp.
   → Lưu ý bắt buộc ghi vào sheet: nhóm TH-03 (tầm soát, chưa có triệu chứng) là G1
     nhưng hay bị chấm WARM/COLD vì tin nhắn ngắn. Post kéo được nhóm này mà %HOT thấp
     thì ĐỪNG TẮT — đọc cột "% HOT trong nhóm G1" trước khi quyết.

7. **Góc tiếp cận → tầng** — quy luật rút ra được, cột:
   Góc tiếp cận | Post đại diện | Số HT gộp | % HOT gộp (trừ cờ đỏ) | % G1 gộp |
   Tầng thường kéo về | Nhóm vấn đề thường kéo về | Rào cản thường đẻ ra | Vì sao |
   Dùng khi nào
   Tám góc tiếp cận cần phân biệt:
   - Giá & điều kiện (nêu con số giá, "bảng giá công khai")
   - Soi không đau / tiền mê ("ngủ một giấc", "không còn sợ nôn")
   - Triệu chứng cụ thể ("đau thượng vị", "đi ngoài ra máu", "táo bón kéo dài")
   - Tầm soát & phòng xa ("ngoài 40 nên soi", "gia đình có người ung thư")
   - Chuyên môn bác sĩ — chuyên gia Bạch Mai
   - Công nghệ máy & AI (Fujifilm VP-7000, BLI/LCI)
   - Banner thông báo / lịch làm việc (mở cả Chủ nhật)
   - Gói cho người nhà – doanh nghiệp
   → Chỉ kết luận khi tổng hội thoại của góc đó ≥10. Chưa đủ thì ghi ⚠.

8. **Rào cản theo post** — post nào đẻ ra rào cản gì, cột:
   Mã post | Rào cản | Nhóm (SỢ/NGỜ/NGẠI/NÉ) | Số ca | % trên tổng HT của post |
   Hàm ý cho thông điệp | Kịch bản cần chuẩn bị (mã S3.x / X.x)
   → Dùng để biết post nào cần sửa thông điệp từ gốc, post nào chỉ cần trang bị trước
     kịch bản xử lý cho trực page.
   → BA QUY LUẬT CẦN KIỂM TRONG DỮ LIỆU, nếu thấy thì nói thẳng:
     ① Post nhấn mạnh GIÁ RẺ thường đẻ ra rào cản NGỜ (L6.2 · L6.9) — khách nghĩ
        "rẻ thế thì máy gì, dây soi có sạch không".
     ② Post nhấn mạnh TIỀN MÊ / "không đau" thường đẻ ra L6.7 (ngại thuốc mê) —
        chính câu quảng cáo gọi nỗi sợ đó lên.
     ③ Post HÙ BỆNH (nhấn nguy cơ ung thư) thường đẻ ra L6.8 (NÉ KẾT QUẢ) và kéo về
        hội thoại hỏi dồn rồi im lặng. Đây là quy luật quan trọng nhất của ngành này:
        post càng đáng sợ thì inbox càng nhiều mà đặt lịch càng ít. Nếu dữ liệu cho
        thấy điều đó, đưa lên sheet 2.

9. **① Nhiệt · Nhóm vấn đề × Độ nóng** — biểu đồ nhiệt. Hàng = 12 nhóm TH,
   cột = HOT/WARM/COLD. Cột phụ bên phải: Tổng HT · **% HOT** · **% HOT\*** · % cho số.
   > ⚠ **Bắt buộc có cột `% HOT*`.** Tín hiệu ① của thang chấm chính là "nêu triệu chứng/
   > chỉ định cụ thể". Bảng này lại chia nhóm THEO VẤN ĐỀ, nên mọi nhóm có vấn đề cụ thể
   > đã được cộng sẵn 1 điểm — cột `% HOT` bị **lặp vòng** và không so sánh được.
   > `% HOT*` chấm lại chỉ bằng 4 tín hiệu còn lại (②③④⑤), đạt ≥3/4 tính HOT*.
   > **VÀ: tách dòng TH-01 ra khỏi mọi so sánh** — luật ghi đè đẩy nhóm đó lên 100% HOT,
   > con số đó chỉ phản ánh chính luật ghi đè, không phản ánh khách.
   > Ghi ngay dưới bảng: cột nào dùng được, cột nào không, và số thật là bao nhiêu.
   > Nếu bỏ tín hiệu ① mà chênh lệch biến mất → NÓI THẲNG LÀ KHÔNG CÓ BẰNG CHỨNG.

10. **② Nhiệt · Góc tiếp cận × Nhóm vấn đề** — mỗi góc quảng cáo kéo về nhóm vấn đề nào.
    Dùng để chọn góc khi viết content mới. Nối trực tiếp sang khuôn W3.

11. **③ Nhiệt · Nhóm vấn đề × Rào cản** — mỗi nhóm vấn đề thường vướng gì.
    Một hội thoại có thể mang nhiều rào cản — ghi rõ cách đếm ở đầu bảng.

12. **④ Nhiệt · Post × Độ nóng** — như sheet 4 nhưng dạng nhiệt, có cột *Đủ mẫu?*
    và cột *đã trừ cờ đỏ chưa*.

13. **Mẫu hội thoại thực tế** — mỗi nhóm vấn đề tối đa 3 ca, cột:
    Nhóm vấn đề | HT# | 🚩 | Độ nóng | Nhóm giá trị | Có SĐT | Post | Trích lời khách
    → **Che số điện thoại** trong phần trích. ⛔ Không trích nội dung kết quả xét nghiệm
      hay chi tiết bệnh án. Chỉ trích đủ để thấy vì sao phân loại như vậy.
    → Đây là phần giúp người đọc kiểm tra máy phân loại có đúng không — bảng số mà
      không có ví dụ thì không ai tin được.

14. **Dữ liệu thô** — để kiểm chứng lại, cột:
    STT HT | Tên KH | Ngày | Thẻ nguồn gốc (nguyên văn) | Mã post sau chuẩn hoá |
    Có SĐT | Bitmask tín hiệu | Ghi đè? | 🚩 Cờ đỏ | Độ nóng | Nhóm vấn đề |
    Nhóm giá trị | L-code
    → Bắt buộc có sheet này. Không có thì không ai kiểm được con số ở sheet 4.
    → Cột "Ghi đè?" ghi rõ luật nào đã áp (đã đặt lịch / cờ đỏ / đã có kết quả nơi khác /
      đến hẹn soi lại).

# KHI CHẠY NHIỀU KỲ
Từ 2 kỳ trở lên thì thêm sheet cuối: **So sánh kỳ** — xem khuôn R5.
→ Chỉ so sánh ở mức GÓC TIẾP CẬN, không so từng post, vì post thường đổi tên và
  nhân bản giữa các kỳ nên không khớp 1-1.
→ Nêu rõ hai kỳ có cùng cách lấy mẫu không. Khác cách lấy mẫu thì không so sánh được.

# QUY TẮC
- Mọi con số phải đếm được từ dữ liệu. Không ước lượng, không làm tròn đẹp.
- Post dưới 10 hội thoại → ⚠ chưa đủ mẫu, không xếp hạng, không khuyến nghị.
- **Không xếp hạng post chỉ bằng %HOT.** Luôn đọc kèm %G1 (sheet 6) và luôn dùng cột
  đã trừ cờ đỏ.
- Hội thoại không rõ nguồn → đếm riêng, không chia đều cho các post.
- Nội dung post vi phạm từ cấm (`không đau` · `khỏi 100%` · `an toàn tuyệt đối` ·
  `phát hiện 100%` · `rẻ nhất`), hoặc **hứa kết quả chẩn đoán**, hoặc **nói "không cần
  soi"**, hoặc **hù bệnh bằng hình ảnh tổn thương** → ghi vào cột riêng
  "⚠ rủi ro pháp lý", báo lên sheet Tổng quan. Nội dung quảng cáo dịch vụ khám chữa
  bệnh chịu Luật Quảng cáo và Nghị định 38/2021 — đây là rủi ro thật, không phải
  chuyện câu chữ.
- Post dùng **ảnh nội soi của người bệnh** → ghi vào cột rủi ro, kèm câu hỏi: đã có
  văn bản đồng ý chưa.

# QUY TẮC VẼ BIỂU ĐỒ NHIỆT
- Dùng tô nền theo mức, không dùng chart object — để file mở được ở mọi phiên bản Excel.
- Thang màu: đậm nhất ở giá trị cao nhất của chính bảng đó, không dùng thang tuyệt đối.
- Ô có giá trị 0 để trắng, không tô.
- Mỗi bảng nhiệt kèm một dòng "đọc bảng này thế nào" bằng lời thường.
- Hàng/cột chưa đủ 10 HT → đánh dấu ⚠ ngay trong ô tiêu đề hàng.

# TRÌNH BÀY
- Font Arial. Freeze dòng tiêu đề + cột đầu. Wrap text ở cột nội dung.
- Màu: ĐỎ ĐẬM cho dòng/ô liên quan cờ đỏ · đỏ nhạt HOT · cam WARM · xanh dương nhạt
  COLD · vàng cho mọi ô ⚠ · viền đậm cho dòng post thuộc nhóm "TĂNG NGÂN SÁCH".

# CÁCH LÀM — theo thứ tự
1. Đọc danh sách post + hội thoại. Báo: số post, số HT, số nối được, số không rõ nguồn,
   🚩 số ca cờ đỏ, mẫu là toàn bộ hay đã lọc.
   DỪNG LẠI cho tôi xác nhận.
2. Sàng cờ đỏ → chấm 5 tín hiệu + 4 luật ghi đè → gán nhóm vấn đề + nhóm giá trị.
   Lưu một bảng kết quả duy nhất.
3. In bảng đếm theo post: số HT · % HOT · % HOT (trừ cờ đỏ) · % G1 · đủ mẫu hay chưa.
   DỪNG LẠI cho tôi xác nhận trước khi xếp hạng và viết khuyến nghị.
4. Dựng 14 sheet.
5. Ghi file.
6. Tự kiểm và báo: tổng HT ở sheet 4 có bằng tổng ở sheet 14 không · có post nào được
   xếp hạng khi chưa đủ mẫu không · cột % HOT* có mặt ở mọi bảng chia nhóm theo vấn đề
   không · dòng TH-01 đã được tách khỏi so sánh chưa · có post nào bị xếp hạng bằng
   %HOT chưa trừ cờ đỏ không.
````

## Đến đây

---

## Bảng kiểm sheet — đối chiếu trước khi giao file

File ra phải có **đúng 14 sheet, đúng thứ tự, đúng tên**. Thiếu hoặc sai tên là chạy sai.

```
[ ]  1. Cờ đỏ                      [ ]  8. Rào cản theo post
[ ]  2. Tổng quan                  [ ]  9. ① Nhiệt Vấn đề × Nóng
[ ]  3. Chú giải ký hiệu           [ ] 10. ② Nhiệt Góc × Vấn đề
[ ]  4. Phân tầng theo post        [ ] 11. ③ Nhiệt Vấn đề × Rào cản
[ ]  5. Xếp hạng & khuyến nghị     [ ] 12. ④ Nhiệt Post × Nóng
[ ]  6. Post × Nhóm giá trị        [ ] 13. Mẫu hội thoại thực tế
[ ]  7. Góc tiếp cận → tầng        [ ] 14. Dữ liệu thô
```

📐 File mẫu đủ 14 sheet: [`template/THV_MAU_R2_PhanTang-QuangCao.xlsx`](../template/THV_MAU_R2_PhanTang-QuangCao.xlsx)

---

## Chuẩn bị dữ liệu đầu vào

**Danh sách post** cần tối thiểu: tên/mã post · nội dung chính (headline) · dịch vụ · thời gian chạy. Có thêm chi phí và lượt tin nhắn thì tốt, nhưng không bắt buộc — báo cáo này đo **chất lượng khách kéo về**, không đo chi phí quảng cáo.

**File hội thoại** phải là **toàn bộ hội thoại trong kỳ**, không lọc theo độ dài hay theo "có số điện thoại". Mẫu đã lọc thì mọi so sánh post đều vô nghĩa.

---

## Vì sao bản tiêu hóa có 14 sheet thay vì 13

Thêm **sheet 1 (Cờ đỏ theo post)** — và nó không nằm ở cuối.

Lý do: ở ngành nha, post kéo về khách "sợ đau" là chuyện marketing. Ở đây, post kéo về người **đi ngoài phân đen ba ngày** là chuyện khác hẳn. Hai việc phải tách:

- **Quyết ngân sách** → đọc sheet 4, 5, 6 với cột đã **trừ cờ đỏ**.
- **Quyết năng lực trực page** → đọc sheet 1. Post nào kéo nhiều ca cờ đỏ thì người trực post đó cần được trang bị kịch bản `X5` trước, không phải cần đổi ngân sách.

Gộp hai việc lại thì hoặc là tắt mất một post đang tiếp cận đúng người cần khám, hoặc là tăng tiền cho một post mà trực page chưa đủ năng lực xử lý. Cả hai đều sai, và cái sai thứ hai thì không ai phát hiện bằng bảng `% HOT`.
