# R5 — SO SÁNH HAI KỲ

**Trả lời câu hỏi:** *Tháng này có tốt lên không, tốt lên nhờ cái gì, và cái gì đang xấu đi.*

**Cần có:** dữ liệu của **hai kỳ đã chạy R1** (và R2/R3 nếu muốn so sâu hơn).
**Nhận lại:** 1 file Excel — `output/THV_SoSanh_<KỲ1>_vs_<KỲ2>.xlsx`, **8 sheet**.

> **📎 Có code mẫu sẵn.** [`tools/xuat_bao_cao.py`](../tools/xuat_bao_cao.py):
> ```
> python xuat_bao_cao.py --bao-cao R5 --rows rows_ky2.json --rows-truoc rows_ky1.json --ky "T10/2026" --ky-truoc "T09/2026" --out ../output
> ```

---

## 🛑 Cổng chặn: hai kỳ có so được với nhau không

**Đây là bước đầu tiên, và nó có quyền dừng cả báo cáo.** So hai kỳ lấy mẫu khác nhau thì mọi con số chênh lệch đều vô nghĩa — và tệ hơn là nó sẽ được dùng để ra quyết định.

| # | Câu hỏi | Khác nhau thì sao |
|---|---|---|
| ① | Hai kỳ có cùng **cách lấy mẫu** không? (toàn bộ hội thoại, hay đã lọc theo độ dài / theo có số) | **DỪNG.** Không so được. Chỉ được so trong nội bộ từng kỳ |
| ② | Hai kỳ có cùng **phạm vi dịch vụ** không? | Chỉ so phần dịch vụ trùng nhau, nói rõ đã loại gì |
| ③ | Hai kỳ có cùng **cách chấm** không? (cùng bộ 5 tín hiệu, cùng **4 luật ghi đè**, cùng cách sàng cờ đỏ) | Chấm lại kỳ cũ theo chuẩn mới, hoặc dừng |
| ④ | Hai kỳ có **độ dài tương đương** không? (10 ngày vs 31 ngày thì không) | Quy về chỉ số tỷ lệ, không so số tuyệt đối |

**Khác ở ①** → báo cáo chỉ được trả về một trang: *vì sao không so được, và cần làm gì để kỳ sau so được*. Không chạy tiếp.

> **Câu ③ đặc biệt quan trọng với THV ở kỳ đầu tiên áp dụng hệ này.** Nếu kỳ 1 chưa có cột cờ đỏ, thì mọi con số `% HOT` của kỳ 1 **không so được** với kỳ 2 — vì luật ghi đè ② đẩy ca cờ đỏ lên HOT, nên kỳ 2 sẽ "nóng hơn" một cách giả tạo. Cách xử lý đúng: so bằng cột **`% HOT (trừ cờ đỏ)`** cho cả hai kỳ, và ghi rõ đã làm vậy.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
So sánh hai kỳ và chỉ ra điều gì tốt lên, điều gì xấu đi, nhờ cái gì.
Sinh ra ĐÚNG 1 file: `output/THV_SoSanh_{{KỲ1}}_vs_{{KỲ2}}.xlsx` — 8 sheet.

Đầu vào:
- Dữ liệu kỳ 1: {{DỮ LIỆU KỲ 1}}   — kỳ: {{KỲ1}}
- Dữ liệu kỳ 2: {{DỮ LIỆU KỲ 2}}   — kỳ: {{KỲ2}}

Viết script Python dùng openpyxl, ghi file thật. Không chạy được code → nói rõ rồi
trả bảng markdown dán được vào Excel.

# BƯỚC 0 — CỔNG CHẶN, LÀM TRƯỚC MỌI THỨ
Trả lời 4 câu, in ra ngay trong chat:
① Hai kỳ có cùng CÁCH LẤY MẪU không? (toàn bộ hội thoại, hay đã lọc theo độ dài /
   theo có số điện thoại)
② Hai kỳ có cùng PHẠM VI DỊCH VỤ không?
③ Hai kỳ có cùng CÁCH CHẤM không? — cùng bộ 5 tín hiệu, cùng 4 LUẬT GHI ĐÈ của ngành
   tiêu hóa (đã đặt lịch → HOT · 🚩 cờ đỏ → HOT · đã có kết quả nơi khác / đã được chỉ
   định soi → HOT · đến hẹn soi lại → tối thiểu WARM), và cùng cách sàng cờ đỏ
④ Hai kỳ có ĐỘ DÀI tương đương không?

- Khác ở ① → DỪNG. Chỉ trả về một trang: vì sao không so được, cần làm gì để kỳ sau
  so được. KHÔNG chạy tiếp, KHÔNG đưa ra con số chênh lệch nào.
- Khác ở ② → chỉ so phần dịch vụ trùng nhau, ghi rõ đã loại những gì.
- Khác ở ③ → chấm lại kỳ cũ theo chuẩn hiện hành, ghi rõ đã chấm lại. Không chấm lại
  được thì dừng.
  TRƯỜNG HỢP RIÊNG: kỳ cũ chưa sàng cờ đỏ → KHÔNG so cột %HOT thường. So bằng cột
  "% HOT (trừ cờ đỏ)" cho cả hai kỳ, hoặc sàng lại cờ đỏ cho kỳ cũ rồi mới so.
- Khác ở ④ → chỉ so chỉ số TỶ LỆ, không so số tuyệt đối. Ghi rõ trên mọi sheet.

DỪNG LẠI cho tôi xác nhận kết quả cổng chặn trước khi tiếp tục.

# NGUYÊN TẮC SO SÁNH
- **So ở mức GÓC TIẾP CẬN, không so từng post.** Post hay bị nhân bản và đổi tên giữa
  các kỳ nên không khớp 1-1 được.
- **Chênh lệch dưới mức dao động tự nhiên thì KHÔNG gọi là thay đổi.** Quy tắc:
  nhóm dưới 30 hội thoại thì chênh lệch dưới 10 điểm % là nhiễu, không kết luận.
  Nhóm 30–100 thì dưới 5 điểm %. Trên 100 thì dưới 3 điểm %.
  Ghi rõ ngưỡng đã dùng ở đầu bảng.
- **Nhóm dưới 10 hội thoại ở MỘT trong hai kỳ → không so.** Ghi ⚠ chưa đủ mẫu.
- **Không gán nguyên nhân khi chưa có bằng chứng.** Chỉ được nói "tăng cùng lúc với
  việc X" nếu X có trong dữ liệu. Không suy ra "nhờ đào tạo nên tăng" khi không đo
  được điều đó.
- **Mọi so sánh %HOT dùng cột đã trừ cờ đỏ.** Số ca cờ đỏ dao động theo mùa và theo
  nội dung quảng cáo, nên nó làm %HOT nhảy mà không liên quan gì tới chất lượng vận hành.

# CẤU TRÚC FILE EXCEL — 8 sheet

1. **🚩 So sánh chỉ số an toàn** — SHEET SỐ 1. Cột:
   Chỉ số | Kỳ 1 | Kỳ 2 | Chênh | Nhận định
   Tối thiểu: số ca cờ đỏ · tỷ lệ nhận diện cờ đỏ · số ca bị trấn an sai ·
   số ca cờ đỏ chưa đặt được lịch.
   → Đây là sheet KHÔNG áp ngưỡng nhiễu. Một ca bị trấn an sai ở kỳ 2 trong khi kỳ 1
     không có ca nào là một thay đổi thật, bất kể cỡ mẫu.
   → Tỷ lệ nhận diện giảm → đưa thẳng lên sheet 2 và nêu ngay trong chat.

2. **Tổng quan & cổng chặn**
   Kết quả 4 câu cổng chặn, ghi rõ ràng.
   Ngưỡng nhiễu đã dùng cho từng cỡ mẫu.
   Bảng so sánh tổng: số inbox · % có SĐT · % HOT (trừ cờ đỏ) · % G1 · điểm chấm TB ·
   % đến khám · **% soi được / đến khám**.
   3 KẾT LUẬN, mỗi dòng: chỉ số nào đổi · đổi bao nhiêu · có vượt ngưỡng nhiễu không ·
   bằng chứng về nguyên nhân (hoặc "chưa xác định được nguyên nhân").
   **Khối cảnh báo:** điều gì không so được và vì sao.

3. **Chú giải ký hiệu** — như các báo cáo khác, THÊM ba mục riêng của R5:
   *ngưỡng nhiễu* (chênh dưới mức dao động tự nhiên thì không gọi là thay đổi) ·
   *tương quan ≠ nhân quả* · *vì sao %HOT phải trừ cờ đỏ khi so hai kỳ*.

4. **So theo chỉ số phễu** — cột:
   Chỉ số | Kỳ 1 | Kỳ 2 | Chênh (điểm %) | Vượt ngưỡng nhiễu? | Nhận định |
   Bằng chứng về nguyên nhân
   Tối thiểu: % có SĐT · % kết nối · % đặt lịch · % đến khám · **% soi được** ·
   % HOT (trừ cờ đỏ) · % WARM · % COLD · % G1 · % G2 · % G3 · điểm chấm TB ·
   % đạt ≥8/10 · **% có dặn chuẩn bị**.
   → Cột "Vượt ngưỡng nhiễu?" ghi CÓ / KHÔNG. Ghi KHÔNG thì cột Nhận định phải là
     "chưa kết luận được", không được viết nhận định có hướng.
   → Hai dòng đáng theo nhất của ngành này: **% soi được / đến khám** và
     **% có dặn chuẩn bị**. Nếu cả hai cùng tăng, đó là bằng chứng gần nhất cho việc
     sửa khâu hướng dẫn chuẩn bị có tác dụng — vẫn phải ghi rõ là tương quan.

5. **So theo nhóm giá trị G1/G2/G3** ⭐ — cột:
   Nhóm giá trị | Chỉ số | Kỳ 1 | Kỳ 2 | Chênh | Vượt ngưỡng? | Nhận định
   → Đây là sheet dễ bị lừa nhất. Một kỳ có thể TĂNG tổng số lead mà lại GIẢM lead G1 —
     tổng trông đẹp hơn trong khi doanh thu kỳ vọng giảm. Chỉ nhìn số tổng là không thấy.
   → Nếu thấy hiện tượng đó, đưa thẳng lên sheet 2.

6. **So theo góc tiếp cận** — cột:
   Góc tiếp cận | Số HT kỳ 1 | Số HT kỳ 2 | % HOT kỳ 1 | % HOT kỳ 2 | Chênh %HOT |
   % G1 kỳ 1 | % G1 kỳ 2 | Chênh %G1 | Vượt ngưỡng? | Nhận định | Dùng tiếp hay đổi
   Tám góc: Giá & điều kiện · Soi không đau/tiền mê · Triệu chứng cụ thể ·
   Tầm soát & phòng xa · Chuyên môn bác sĩ – chuyên gia Bạch Mai · Công nghệ máy & AI ·
   Banner thông báo/lịch làm việc · Gói cho người nhà – doanh nghiệp.
   → Góc nào chỉ xuất hiện ở một kỳ: ghi rõ, không so.
   → Kiểm riêng góc "Tầm soát & phòng xa": nếu kỳ nào góc này tăng mạnh mà tỷ lệ
     L6.8 (né kết quả) cũng tăng, đó là dấu hiệu nội dung đã nghiêng sang hù bệnh.
     Có thì nói rõ, kèm số.

7. **So theo rào cản** — cột:
   Rào cản | Nhóm (SỢ/NGỜ/NGẠI/NÉ) | % kỳ 1 | % kỳ 2 | Chênh | Vượt ngưỡng? |
   NV xử lý được bao nhiêu (kỳ 1 → kỳ 2) | Nhận định
   → Ba dòng bắt buộc có: L6.7 (ngại tiền mê) · L6.8 (né kết quả) · L6.9 (ngờ vệ sinh
     dây soi).
   → Chỉ số đáng theo nhất: **tỷ lệ ca mang rào cản mà nhân viên CÓ đưa đúng bằng
     chứng** — với L6.7 là bác sĩ gây mê theo dõi riêng + sàng lọc trước mê, với L6.9
     là quy trình xử lý dây soi, với L6.2 là chuyên gia Bạch Mai + hệ máy.
     Chỉ số này tăng mà % đặt lịch cũng tăng → bằng chứng gần nhất cho việc đào tạo
     có tác dụng. Vẫn phải ghi rõ đây là tương quan, không phải nhân quả.

8. **Dữ liệu thô & cách tính** — cột:
   Chỉ số | Công thức | Tử/mẫu kỳ 1 | Tử/mẫu kỳ 2 | Nguồn | Hạn chế khi đọc
   → Bắt buộc có. Không có sheet này thì không ai kiểm được con số chênh lệch.

# QUY TẮC
- Cổng chặn ở bước 0 có quyền dừng cả báo cáo. Không bỏ qua.
- Chênh lệch chưa vượt ngưỡng nhiễu → ghi "chưa kết luận được", KHÔNG viết nhận định
  có hướng ("có dấu hiệu cải thiện" cũng là nhận định có hướng — không được viết).
  NGOẠI LỆ: sheet 1 (an toàn) không áp ngưỡng nhiễu.
- Không gán nguyên nhân khi chưa có bằng chứng trong dữ liệu.
- Không so từng post, chỉ so góc tiếp cận.
- Nhóm dưới 10 HT ở một trong hai kỳ → không so.
- Mọi so sánh %HOT dùng cột đã trừ cờ đỏ.
- Không đưa thông tin định danh hay dữ liệu sức khỏe của khách vào file.

# CÁCH LÀM
1. Chạy cổng chặn bước 0. In kết quả 4 câu.
   DỪNG LẠI cho tôi xác nhận.
2. Dựng sheet 1 (an toàn) trước. Nếu tỷ lệ nhận diện cờ đỏ giảm, nêu ngay trong chat.
3. Tính ngưỡng nhiễu theo cỡ mẫu từng nhóm. In bảng ngưỡng.
4. So các chỉ số. In bảng tóm tắt: chỉ số nào vượt ngưỡng, chỉ số nào không.
   DỪNG LẠI cho tôi xác nhận.
5. Ghi file Excel.
6. Tự kiểm và báo: có chỉ số nào chưa vượt ngưỡng mà vẫn bị viết nhận định có hướng
   không · có nhóm nào <10 HT mà vẫn bị so không · có chỗ nào so %HOT chưa trừ cờ đỏ
   không · có chỗ nào gán nhân quả mà không có bằng chứng không.
````

## Đến đây

---

## Lưu ý khi dùng

**Sheet 4 (So theo nhóm giá trị) là chỗ dễ bị lừa nhất.** Tổng lead tăng mà lead G1 giảm là tình huống rất hay xảy ra khi chuyển ngân sách sang post banner giá rẻ: số inbox tăng vọt, báo cáo trông đẹp, doanh thu kỳ vọng lại giảm. Bảng tổng không bắt được điều đó.

**Hai dòng của sheet 4 đáng theo hơn mọi dòng khác với THV: `% soi được / đến khám` và `% có dặn chuẩn bị`.** Đây là cặp chỉ số có quan hệ gần nhất với một việc cụ thể làm được trong tháng — gửi hướng dẫn chuẩn bị đúng lúc. Nếu cả hai cùng tăng, đó là lần duy nhất trong báo cáo này mà việc làm và kết quả nằm đủ gần nhau để nói được điều gì. Ngay cả vậy thì vẫn là tương quan.

**Sheet 1 không áp ngưỡng nhiễu, và đó là cố ý.** Mọi chỉ số kinh doanh đều cần ngưỡng nhiễu để tránh đọc dao động thành thay đổi. Nhưng một ca cờ đỏ bị trấn an sai không phải một điểm dữ liệu — nó là một người bệnh. Một ca cũng phải báo.

**Kỳ đầu tiên áp dụng hệ này thì cổng chặn câu ③ gần như chắc chắn "khác".** Kỳ cũ không có cột cờ đỏ, không có `L6.8`, không có mốc "soi được". Đó là chuyện bình thường — xử lý bằng cách so phần so được (`% có SĐT`, `% đặt lịch`, `% đến khám`) và ghi rõ phần nào bắt đầu đo từ kỳ này. Đừng chấm lại kỳ cũ bằng tay cho đủ bộ, trừ khi dữ liệu kỳ cũ còn nguyên.
