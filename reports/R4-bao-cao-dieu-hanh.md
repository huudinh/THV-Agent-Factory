# R4 — BÁO CÁO ĐIỀU HÀNH THEO DỊCH VỤ

**Trả lời câu hỏi:** *Phễu đang rò ở khâu nào, nhóm nào đang mất tiền, và tháng tới dồn lực vào đâu.*

**Cần có:** file hội thoại trong kỳ. Có thêm số đặt lịch / đến khám / đã thực hiện nội soi thì đọc được cả phễu.
**Nhận lại:** 1 file Excel — `output/THV_BaoCaoDieuHanh_<KỲ>.xlsx`, **11 sheet**. Kèm **bản tóm tắt 1 trang** để trình bày.

> **📎 Có code mẫu sẵn.** [`tools/xuat_bao_cao.py`](../tools/xuat_bao_cao.py):
> ```
> python xuat_bao_cao.py --bao-cao R4 --rows rows.json --so-lieu <file số liệu> --ky "<kỳ>" --out ../output
> ```

---

## ⚠ Phễu tiêu hóa có BA con số ở cuối — không được lẫn

```
inbox → có SĐT → kết nối (gọi được) → đặt lịch
      → ĐẾN KHÁM                      ← mốc rò 1
      → THỰC HIỆN ĐƯỢC NỘI SOI        ← mốc rò 2, riêng của ngành nội soi
      → kết quả (± sinh thiết / giải phẫu bệnh)
      → điều trị · HẸN SOI LẠI THEO CHU KỲ   ← vòng LTV
```

**Mốc rò 1 — "đặt lịch" không phải "đến khám".** Dữ liệu không có số đến khám → ghi `⚠ chưa đo được show-up`, **tuyệt đối không lấy "đặt lịch" thay thế**.

**Mốc rò 2 — "đến khám" không phải "soi được".** ⭐ Đây là mốc **chỉ ngành nội soi mới có**, và là chỗ mất tiền nhiều nhất: khách đã tốn toàn bộ chi phí quảng cáo, tốn một buổi của mình và của phòng khám, mà doanh thu bằng không. Lý do thường là:

| Lý do hoãn tại chỗ | Lỗi thuộc khâu nào |
|---|---|
| Ăn sáng rồi / nhịn chưa đủ giờ | **Hướng dẫn chuẩn bị** |
| Ruột chưa sạch | **Hướng dẫn chuẩn bị** |
| Không đủ điều kiện tiền mê (bệnh nền, chưa xét nghiệm sàng lọc) | **Sàng lọc trước khi hẹn** |
| Không có người đưa về sau mê | **Dặn trước** |
| Đến rồi vẫn không dám soi | Rào cản **SỢ / NÉ** chưa được gỡ |

> **Phần lớn những lý do trên là lỗi dặn dò, sửa được bằng một tin nhắn mẫu.** Nhưng không ai sửa nếu không có con số. Vì vậy sheet 4 của báo cáo này là **bảng lý do hoãn tại chỗ** — và nó đáng tiền hơn mọi bảng tỷ lệ khác trong file.

**Quyết định tiền thật xảy ra sau khi bác sĩ khám, không xảy ra trong inbox.** Vì vậy báo cáo đo trách nhiệm của trực page **tới mốc đến khám**, tách riêng mốc "thực hiện được nội soi" như chỉ số **chung** của trực page + CSKH + phòng khám, và tách mốc "chỉ định điều trị" như chỉ số của phòng khám.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Dựng báo cáo điều hành cho kỳ {{KỲ}} từ file hội thoại {{FILE}}
(+ file số liệu đặt lịch / đến khám / đã soi nếu có: {{FILE SỐ LIỆU}}).
Sinh ra ĐÚNG 1 file: `output/THV_BaoCaoDieuHanh_{{KỲ}}.xlsx` — 11 sheet.
Kèm in ra trong chat một BẢN TÓM TẮT 1 TRANG.

Viết script Python dùng openpyxl. Ghi ra file thật.
Môi trường không chạy được code → nói rõ, rồi trả bảng markdown dán được vào Excel.

# BA TRỤC + MỘT CỜ BẮT BUỘC TÁCH RIÊNG
Mọi bảng phễu phải tách theo nhóm giá trị G1/G2/G3 — gộp lại thì nhóm G3 (đông,
dễ chốt, giá nhỏ) sẽ che mất việc G1 đang rò. G1 là chỗ tiền thật.
Cột 🚩 cờ đỏ đứng riêng: nó KHÔNG phải chỉ số kinh doanh, nó là chỉ số an toàn.
Báo cáo điều hành phải có cả hai loại, và không trộn chúng vào một bảng.

# CẤU TRÚC FILE EXCEL — 11 sheet

1. **🚩 An toàn người bệnh** — SHEET SỐ 1. Cột:
   Chỉ số | Giá trị kỳ này | Mốc | Việc phải làm
   Tối thiểu các chỉ số:
   - Số ca có dấu hiệu cờ đỏ trong kỳ
   - Số ca được nhận diện / tổng ca có dấu hiệu → MỐC LÀ 100%, không thương lượng
   - Số ca bị trấn an sai (nếu >0: liệt kê số hiệu hội thoại ngay tại đây)
   - Số ca cờ đỏ cuối kỳ VẪN CHƯA đặt được lịch khám → đây là danh sách phải gọi lại,
     không phải con số để đọc
   - Số ca cờ đỏ được gọi trong SLA ≤5'
   → Chạy R3 rồi thì dùng lại kết quả, không chấm lại.
   → Không có ca nào: vẫn giữ sheet, ghi rõ đã sàng theo 6 mã CĐ-1…CĐ-6.

2. **Một trang cho lãnh đạo**
   Dòng đầu: 🚩 tình hình an toàn (lấy một dòng từ sheet 1).
   Rồi: BA KẾT LUẬN, mỗi dòng một con số, viết bằng lời thường.
   Rồi: bảng phễu toàn kỳ · bảng phễu tách G1/G2/G3 · 3 nhóm đang rò nặng nhất ·
   **số ca hoãn tại chỗ và lý do đứng đầu** · 3 việc tháng tới kèm người phụ trách.
   Rồi: **khối cảnh báo phương pháp** — mẫu là toàn bộ hay đã lọc · chỉ số nào chưa
   đo được · con số nào KHÔNG dùng để quyết ngân sách.
   Sheet này phải đọc hết trong 2 phút. Không có bảng nào quá 10 dòng.

3. **Chú giải ký hiệu** — ⚠ · 🚩 6 mã CĐ · HOT/WARM/COLD và 5 tín hiệu ·
   4 luật ghi đè · G1/G2/G3 · TH-01…TH-12 · L-code (có L6.7 · L6.8 · L6.9) ·
   SỢ/NGỜ/NGẠI/NÉ · S1–S3·CS · nhịp T và D · quy ước màu.
   Đọc sheet này trước khi đọc số.

4. **⭐ Hoãn tại chỗ — vì sao khách đến mà không soi được** — SHEET ĐÁNG TIỀN NHẤT. Cột:
   Lý do hoãn | Số ca | % trên số ca đến khám | Lỗi thuộc khâu nào |
   Sửa bằng cách gì | Ai phụ trách | Cách đo lại sau 1 tháng
   Sáu lý do tối thiểu: nhịn ăn chưa đủ giờ · ruột chưa sạch · không đủ điều kiện
   tiền mê · không có người đưa về · đến rồi không dám soi · lý do khác.
   → Dữ liệu không có số này → ghi `⚠ chưa đo được`, và nêu RÕ cần xin gì từ ai:
     "cần bảng ghi nhận của lễ tân: mỗi ca đến khám mà không soi được, ghi một dòng
     lý do". Đây là đề nghị dữ liệu quan trọng nhất của cả báo cáo.
   → Có số rồi thì phần lớn các dòng sẽ trỏ về khâu "hướng dẫn chuẩn bị" — tức là
     sửa được bằng tin nhắn mẫu + một mốc nhắc trước buổi hẹn, không cần thêm người,
     không cần thêm ngân sách. Nói rõ điều đó ở cuối sheet.

5. **Phễu theo nhóm vấn đề** — cột:
   Nhóm vấn đề (TH-xx) | Nhóm giá trị | Inbox | Có SĐT | % có SĐT | Kết nối được |
   % kết nối | Đặt lịch | % đặt lịch | Đến khám | % show-up | **Soi được** |
   **% soi được / đến khám** | Khâu rò nặng nhất | Chênh so mốc KPI
   → Mốc KPI để so: kết nối/số ≥78% · đặt lịch/kết nối ≥50%. Các mốc khác chưa có →
     ghi `⚠ chưa có mốc so sánh`, KHÔNG tự đặt mốc rồi kết luận đạt/không đạt.
   → Cột "Khâu rò nặng nhất" = khâu có % thấp nhất so với mốc, hoặc thấp nhất so với
     trung bình các nhóm khác khi chưa có mốc.
   → Nhóm dưới 10 hội thoại: ghi ⚠ chưa đủ mẫu, KHÔNG kết luận khâu rò.
   → TH-01 (cờ đỏ) tách riêng một dòng cuối bảng, KHÔNG gộp vào trung bình —
     nhóm này được ưu tiên xử lý nên mọi tỷ lệ của nó không so được với nhóm khác.

6. **Chân dung khách theo nhóm vấn đề & rào cản** — cột:
   Nhóm vấn đề | Số HT | Nhóm khách chủ đạo (N1–N6) | Đặc điểm quan sát được |
   Rào cản số 1 | Rào cản số 2 | % mang rào cản NÉ | Mong muốn chính nêu ra |
   Hàm ý cho nội dung
   Sáu nhóm khách: N1 triệu chứng dai dẳng · N2 có cờ đỏ · N3 tầm soát chủ động ·
   N4 mang kết quả nơi khác đến · N5 theo dõi sau can thiệp · N6 người nhà đặt hộ
   → Một hội thoại có thể mang nhiều rào cản. Ghi rõ cách đếm ở đầu bảng.
   → Cột "% mang rào cản NÉ" (L6.8) là chỉ số đáng theo nhất của ngành này: nhóm NÉ
     không lùi vì tiền hay vì bận, nên mọi nỗ lực giảm giá và mọi lần nhắc lịch đều
     trượt. Tỷ lệ NÉ cao thì việc cần làm là ĐỔI NỘI DUNG, không phải tăng tần suất nhắc.

7. **Rào cản toàn kỳ** — cột:
   Rào cản | Nhóm (SỢ/NGỜ/NGẠI/NÉ) | L-code | Số ca | % trên tổng HT |
   Nhóm vấn đề vướng nhiều nhất | NV xử lý được bao nhiêu ca | Bằng chứng nên dùng |
   Việc cần làm
   → Cột "NV xử lý được bao nhiêu ca": đếm số ca mà sau khi khách nêu rào cản, nhân
     viên có đưa ra bằng chứng/kịch bản phù hợp. Đây là chỗ nối sang R3.
   → Ba dòng bắt buộc có, kể cả khi số nhỏ: L6.7 (ngại tiền mê) · L6.8 (né kết quả) ·
     L6.9 (ngờ vệ sinh dây soi). Ba rào cản này là đặc thù ngành, và THV có bằng chứng
     để gỡ cả ba — khoảng cách giữa "mình có bằng chứng" và "mình có nói ra" là phát
     hiện đáng giá nhất của sheet này.

8. **Chất lượng tư vấn — bản rút gọn** — cột:
   Chỉ số | Giá trị kỳ này | Mốc | Chênh | Hậu quả thấy được trong dữ liệu
   Tối thiểu các chỉ số: 🚩 tỷ lệ nhận diện cờ đỏ · điểm chấm TB · % đạt ≥8/10 ·
   % có bước B5 đầy đủ · % thu đủ 5 thông tin · **% có dặn chuẩn bị** ·
   % đưa bằng chứng đúng rào cản · số ca vi phạm ngôn từ.
   → Chạy R3 rồi thì DÙNG LẠI kết quả, không chấm lại.
   → Chưa chạy R3 thì chấm rút gọn 4 tiêu chí: ③⑤⑥⑩, và ghi rõ là bản rút gọn.
     Chọn bốn tiêu chí này vì chúng tương ứng bốn chỗ mất nhiều nhất: bỏ sót cờ đỏ ·
     không có bằng chứng · không dặn chuẩn bị · không nêu bước tiếp theo.

9. **Hiệu quả quảng cáo — bản rút gọn** — cột:
   Mã post | Góc tiếp cận | Số HT | % có SĐT | % HOT (trừ cờ đỏ) | % G1 |
   Khuyến nghị | Đủ mẫu?
   → Chạy R2 rồi thì DÙNG LẠI kết quả. Chưa chạy thì ghi `⚠ chưa có dữ liệu post`,
     KHÔNG suy đoán.
   → Luôn có cột %G1 và luôn dùng cột %HOT đã trừ cờ đỏ.

10. **⭐ Tệp giá trị dài hạn** — sheet riêng của ngành tiêu hóa. Cột:
    Nhóm tệp | Số HT / số người | Mô tả | Vì sao đáng giữ | Nhịp chạm đề xuất | Ai phụ trách
    Tối thiểu các nhóm:
    - **ĐẾN HẸN SOI LẠI (TH-02)** ⭐ — tệp đáng tiền nhất của ngành. Khác với mọi
      ngành khác trong tập đoàn, nhóm này KHÔNG cần tạo nhu cầu: mốc hẹn đã nằm
      trong phiếu kết quả của chính khách. Họ gần như chắc chắn soi lại — vấn đề chỉ
      là soi ở đâu. Mà họ không xuất hiện trong báo cáo lead mới, nên thường không
      ai nhắc.
      ⚠ Nhắc theo MỐC BÁC SĨ ĐÃ HẸN trong phiếu kết quả. ⛔ Không tự nêu số năm chu kỳ.
    - **Đã đến khám mà chưa soi được (hoãn tại chỗ)** — khách đã bỏ công đến tận nơi.
      Tệp nóng nhất mà hay bị bỏ nhất. Lấy từ sheet 4.
    - **WARM/COLD · G1** — chưa sẵn sàng nhưng là ca combo tầm soát / can thiệp.
      Nuôi tới 90 ngày, không hạ tệp ở 30 ngày như nhóm khác.
    - **L6.8 né kết quả** — nuôi tới 180 ngày bằng nội dung giáo dục, nhịp
      D+7/D+21/D+45. ⛔ Không gửi ưu đãi giảm giá cho nhóm này.
    - **TH-11 mang kết quả nơi khác đến** — đã qua giai đoạn "có cần soi hay không",
      chỉ còn chọn nơi làm. Giá trị cao, chu kỳ ngắn.
    - **TH-03 tầm soát chủ động chưa đặt lịch** — nhóm G1 hay bị chấm COLD vì tin
      nhắn ngắn và không có triệu chứng cấp.
    - **Có dấu hiệu người nhà** — hội thoại nhắc "cho bố em", "cả nhà", "vợ em cũng
      bị". Đếm riêng. Có yếu tố gia đình trong tiền sử ung thư tiêu hóa thì đây vừa
      là tệp LTV vừa là nhóm nguy cơ cao (CĐ-6).
    → Mỗi nhóm phải có con số đếm được. Nhóm không đếm được từ dữ liệu → ghi
      `⚠ chưa đo được`, nêu cần thêm dữ liệu gì.

11. **Dữ liệu thô & cách tính** — cột:
    Chỉ số | Công thức | Tử số | Mẫu số | Nguồn dữ liệu | Hạn chế khi đọc
    → Bắt buộc có. Lãnh đạo hỏi "số này ở đâu ra" thì mở sheet này, không phải hỏi lại
      người làm báo cáo.
    → Ba dòng bắt buộc ghi rõ công thức riêng: % show-up (đến khám / đặt lịch) ·
      % soi được (soi được / đến khám) · % hoãn tại chỗ (hoãn / đến khám).
      Ba con số này hay bị tính lẫn nhau.

# BẢN TÓM TẮT 1 TRANG — in ra trong chat
Cấu trúc:
- 🚩 **Một câu về an toàn**: kỳ này có bao nhiêu ca cờ đỏ, nhận diện được bao nhiêu,
  còn ca nào chưa đặt được lịch
- **3 câu kết luận**, mỗi câu một con số, viết cho người không đọc bảng
- **Phễu toàn kỳ** 1 bảng nhỏ — có cả ba con số cuối: đặt lịch · đến khám · soi được
- **Phễu tách G1/G2/G3** 1 bảng nhỏ — kèm một câu nhận định về chênh lệch
- **Khâu rò nặng nhất** và nó làm mất bao nhiêu lead trong kỳ
- **Hoãn tại chỗ**: bao nhiêu ca, lý do đứng đầu, sửa bằng gì
- **3 việc tháng tới**, mỗi việc có người phụ trách và cách đo kết quả
- **Điều chưa đo được** — liệt kê, và nói rõ cần xin dữ liệu gì từ ai

# QUY TẮC
- Mọi con số phải đếm được. Không ước lượng, không làm tròn đẹp.
- Nhóm dưới 10 hội thoại: ⚠ chưa đủ mẫu, không kết luận khâu rò.
- Chưa có mốc KPI: nêu số thật + `⚠ chưa có mốc so sánh`. KHÔNG tự đặt mốc rồi kết
  luận đạt/không đạt. NGOẠI LỆ: mốc 100% nhận diện cờ đỏ là mốc của chính hệ này.
- ❌ Không lấy "đặt lịch" thay cho "đến khám". ❌ Không lấy "đến khám" thay cho
  "thực hiện được nội soi". Ba con số, ba cột riêng.
- Mọi bảng phễu tách theo G1/G2/G3. TH-01 tách riêng, không gộp vào trung bình.
- Mỗi con số đi kèm một việc phải làm. Số không gắn hành động thì bỏ khỏi báo cáo.
- Mọi con số giá trích từ hội thoại: ghi rõ "nhân viên đã nói với khách", gắn ⚠.
- Phát hiện hai nhân viên báo hai giá khác nhau cho cùng dịch vụ, hoặc báo giá mà
  không nói rõ ai thực hiện / có tiền mê hay không → ĐƯA LÊN SHEET 2, không ghi chú
  nhỏ ở cuối. Giá của THV thay đổi theo người thực hiện nên lỗi này rất dễ xảy ra.
- Không đưa SĐT, thông tin định danh, hay dữ liệu sức khỏe của khách vào file.
- Phần có tên nhân viên: chỉ để dạng tổng hợp, không xếp hạng cá nhân trong báo cáo
  này (xếp hạng cá nhân thuộc R3).

# CÁCH LÀM
1. Đọc dữ liệu. Báo: số hội thoại · khoảng thời gian · 🚩 số ca cờ đỏ ·
   có số đặt lịch / đến khám / đã soi không · có bảng lý do hoãn tại chỗ không ·
   mẫu là toàn bộ hay đã lọc · đã chạy R1/R2/R3 cho kỳ này chưa.
   DỪNG LẠI cho tôi xác nhận.
2. Dựng phễu. In bảng phễu toàn kỳ (có cả ba con số cuối) + bảng phễu tách G1/G2/G3.
   DỪNG LẠI cho tôi xác nhận con số.
3. Ghi file Excel + in bản tóm tắt 1 trang.
4. Tự kiểm và báo: tổng hội thoại mọi sheet có bằng nhau không · có nhóm nào <10 HT
   mà vẫn kết luận không · có chỗ nào lấy "đặt lịch" thay "đến khám" hoặc "đến khám"
   thay "soi được" không · TH-01 đã tách khỏi trung bình chưa · mỗi con số ở sheet 2
   có gắn một việc phải làm không.
````

## Đến đây

---

## Bảng kiểm sheet — đối chiếu trước khi giao file

File ra phải có **đúng 11 sheet, đúng thứ tự, đúng tên**.

```
[ ]  1. Cờ đỏ                       [ ]  7. Rào cản toàn kỳ
[ ]  2. Một trang cho lãnh đạo      [ ]  8. Chất lượng tư vấn
[ ]  3. Chú giải ký hiệu            [ ]  9. Hiệu quả quảng cáo
[ ]  4. Hoãn tại chỗ          ⭐    [ ] 10. Tệp giá trị dài hạn
[ ]  5. Phễu theo dịch vụ           [ ] 11. Dữ liệu thô & cách tính
[ ]  6. Chân dung theo vấn đề
```

⭐ Sheet 4 thường toàn `⚠ chưa đo được` ở lần chạy đầu — **vẫn phải có**, vì nó là chỗ
nêu đề nghị dữ liệu quan trọng nhất của báo cáo: nhờ lễ tân ghi một dòng lý do cho mỗi
ca đến khám mà không soi được.

📐 File mẫu đủ 11 sheet: [`template/THV_MAU_R4_BaoCaoDieuHanh.xlsx`](../template/THV_MAU_R4_BaoCaoDieuHanh.xlsx)

---

## Lưu ý khi dùng

**Chạy R4 sau cùng.** Nó dùng lại kết quả của R1 (phân loại), R2 (quảng cáo), R3 (chất lượng tư vấn). Chạy R4 đầu tiên thì sheet 8 và sheet 9 chỉ còn bản rút gọn, giá trị thấp hơn nhiều.

**Sheet 4 (Hoãn tại chỗ) là sheet đáng tiền nhất, và nó thường bắt đầu bằng `⚠ chưa đo được`.** Đó là chuyện bình thường ở lần chạy đầu — vì không ai ghi lại lý do khách đến mà không soi được. Việc của lần chạy đầu là **xin được bảng đó**: một dòng mỗi ca, do lễ tân ghi, mất vài giây. Từ lần chạy thứ hai, đây là sheet mà người đọc quay lại nhiều nhất.

Lý do: mọi khâu khác trong phễu cần tiền hoặc cần người để cải thiện. Khâu này **phần lớn cần một tin nhắn mẫu và một mốc nhắc** trước buổi hẹn.

**Sheet 10 (Tệp giá trị dài hạn) có một nhóm mà ngành nha không có: tệp đến hẹn soi lại.** Ở nha khoa, LTV phải tạo ra bằng cross-sell và gói gia đình. Ở đây, **mốc quay lại đã nằm sẵn trong phiếu kết quả của chính khách** — bác sĩ đã hẹn, khách đã biết. Tệp này không cần thuyết phục, chỉ cần nhắc đúng lúc. Mà nó không xuất hiện trong bất kỳ báo cáo lead mới nào, nên thường không ai nhắc.

⚠️ Giới hạn quan trọng: **chu kỳ tái soi là chỉ định y khoa cho từng ca.** Báo cáo chỉ được nói *"theo mốc bác sĩ đã hẹn trong phiếu kết quả"*, không tự điền số năm. Nhầm chỗ này là vừa sai y khoa vừa làm khách mất tin.

**Cột "% mang rào cản NÉ" ở sheet 6 là chỗ hay bị đọc sai thành chuyện giá.** Khi tỷ lệ NÉ cao, phản xạ thường gặp là giảm giá hoặc tăng tần suất nhắc lịch — cả hai đều trượt, và cái thứ hai còn đẩy khách xa thêm. Việc cần làm là đổi nội dung: nói về việc biết sớm thì xử lý được, và hẹn một mốc cụ thể thay vì để ngỏ.
