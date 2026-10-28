# 04 · OUTPUT MẪU — báo cáo đúng trông như thế nào

Dùng để **đối chiếu**: nếu trợ lý trả về khác hẳn những mẫu dưới đây thì nó đang chạy sai, xem [`05-xu-ly-su-co.md`](05-xu-ly-su-co.md).

Mọi con số trong tài liệu này là **ví dụ mô phỏng**, không phải số thật của THV.

---

# 1. MODE KIỂM DỮ LIỆU

Bạn dán file mà chưa ra lệnh gì → nó phải trả về đại ý thế này:

```
🚩 TRƯỚC KHI NÓI SỐ: file này có 3 ca mang dấu hiệu cần bác sĩ đánh giá sớm
   HT#4  — đi ngoài phân đen (CĐ-1). Chưa có SĐT.
          ⚠ Nhân viên đã trả lời "chắc không sao đâu" và "uống thuốc xem sao".
          Đây là ca cần gọi lại hôm nay, không phải việc để trong báo cáo.
   HT#3  — bố mất vì ung thư dạ dày (CĐ-6). Đã có SĐT, đã hẹn cuối tuần.
   HT#11 — sụt cân + thay đổi khuôn phân (CĐ-2). Đã có SĐT, nhân viên xử lý đúng.

ĐỌC ĐƯỢC GÌ
  12 hội thoại, từ 03/10 đến 12/10
  5 có số điện thoại (41,7%) · 7 không
  11 có thẻ nguồn quảng cáo · 1 không rõ nguồn
  Tất cả đều có dấu thời gian từng tin và tên người phụ trách

LÀM ĐƯỢC
  R1 phân loại & kịch bản          — đủ dữ liệu
  R3 chất lượng tư vấn             — đủ (có dấu thời gian + tên NV)
  W1 kho câu hỏi → đề bài nội dung — đủ
  R2 phân tầng post                — chạy được, nhưng chỉ 11 hội thoại có
                                      thẻ nguồn nên mọi post đều dưới 10 ca
                                      → ⚠ chưa đủ mẫu, không xếp hạng được

CHƯA LÀM ĐƯỢC
  R4 điều hành   — thiếu số đặt lịch / đến khám / soi được
  R5 so hai kỳ   — chỉ có một kỳ
  R6 chân dung   — cần bảng danh sách khách, không phải file hội thoại

⚠ CẢNH BÁO: 12 hội thoại là mẫu nhỏ. Mình chưa biết đây là toàn bộ kỳ hay
   đã lọc — anh/chị xác nhận giúp em.

Anh/chị muốn chạy cái nào trước ạ?
```

**Dấu hiệu sai:** nó nhảy luôn vào làm báo cáo mà không hỏi · nó không nêu ca cờ đỏ · nó nói "đủ dữ liệu cho mọi báo cáo".

---

# 2. MODE RA BÁO CÁO — hai điểm dừng

## 2.1 DỪNG 1 — xác nhận con số đếm được

```
BƯỚC 1 — ĐỌC & ĐẾM. Em dừng ở đây chờ anh/chị xác nhận.

Tách được        12 hội thoại   (tiêu đề file ghi 12 — khớp)
Có SĐT           5 (41,7%)
Khoảng thời gian 03/10 – 12/10
Thiếu dấu thời gian  0
Không rõ nguồn post  1
🚩 Ca có dấu hiệu cờ đỏ  3  → HT#3, HT#4, HT#11

MẪU NÀY LÀ TOÀN BỘ HAY ĐÃ LỌC? Em cần anh/chị trả lời câu này trước khi
chấm, vì nếu đã lọc theo độ dài thì mọi tỷ lệ sẽ thiên về phía nóng.

Con số trên có khớp với anh/chị không ạ?
```

## 2.2 DỪNG 2 — xác nhận phân bố sau khi chấm

```
BƯỚC 3 — PHÂN BỐ SAU KHI CHẤM. Em dừng lần hai.

ĐỘ NÓNG          HOT 7 (58,3%) · WARM 3 · COLD 2
  trong đó 7 ca là do LUẬT GHI ĐÈ, không phải do đủ điểm:
    🚩 cờ đỏ                  3
    đã đặt lịch               1
    đã có kết quả nơi khác    1
    đến hẹn soi lại           1
  (1 ca vừa đủ điểm vừa có ghi đè)

ĐỘ NÓNG TRỪ CỜ ĐỎ  HOT 4 (33,3%) · WARM 5 · COLD 3
  → Đây là cột dùng để so sánh post. Cột trên KHÔNG dùng được cho việc đó.

NHÓM GIÁ TRỊ     G1 5 · G2 5 · G3 1 · chưa rõ 1

NHÓM VẤN ĐỀ      TH-01 cờ đỏ 3 · TH-02 soi lại 2 · TH-04 dạ dày 2
                 TH-05 đại tràng 2 · TH-09 rối loạn 1 · TH-12 chưa rõ 1
  ⚠ Mọi nhóm đều dưới 10 hội thoại → không xếp hạng nhóm nào

RÀO CẢN (đếm theo lượt, tổng > 12 là đúng)
  SỢ 6  (L6.7 ngại tiền mê 3 · L6.5 sợ nội soi 3)
  NGỜ 2 (L6.2 so sánh 1 · L6.9 dây soi 1)
  NÉ 1  (L6.8 né kết quả 1 — HT#7)
  NGẠI 1

⚠ L6.8 em chỉ bắt được 1 ca chắc chắn. Nhóm này nói cùng một câu với nhóm
  bận, nên có thể còn ca nữa mà em xếp vào L6.4. Anh/chị đọc lại HT#12 giúp em.

Phân bố này có hợp lý không ạ? Em viết kịch bản sau khi anh/chị xác nhận.
```

**Dấu hiệu sai:** không có dòng "trừ cờ đỏ" · không nói rõ bao nhiêu ca do ghi đè · xếp hạng nhóm dưới 10 ca · tổng rào cản bằng đúng tổng hội thoại (nghĩa là nó đếm sai cách).

---

# 3. BA DÒNG MỞ ĐẦU BÁO CÁO

Sau khối cờ đỏ, ba dòng đầu phải là ba điều cần biết nhất, mỗi dòng một con số:

```
🚩 Kỳ này có 3 ca mang dấu hiệu cần khám sớm; 1 ca bị trấn an sai (HT#4) —
   đã lập danh sách gọi lại.

① 7/12 hội thoại là HOT, nhưng 3 trong số đó là HOT do cờ đỏ, không phải
   do sẵn sàng đặt lịch. Trừ cờ đỏ thì HOT thật là 4/12 (33%).
② Rào cản nặng nhất là SỢ THỦ THUẬT: 6/12 hội thoại, chia đều giữa sợ nội
   soi (3) và ngại tiền mê (3) — mà chỉ 2 ca được nhân viên nhắc tới việc có
   bác sĩ gây mê theo dõi riêng.
③ 5/12 hội thoại thuộc nhóm giá trị lớn (combo tầm soát, can thiệp), nhưng
   chỉ 2 trong số đó có số điện thoại. Khâu xin số đang hổng ở đúng nhóm
   đáng tiền nhất.
```

**Dấu hiệu sai:** mở đầu bằng phương pháp (*"Em đã đọc 12 hội thoại và phân loại theo…"*) · ba dòng không có con số · ba dòng nói ba điều không dẫn tới hành động nào.

---

# 4. BA VIỆC TUẦN TỚI

```
BA VIỆC TUẦN TỚI

1. 🚩 Gọi lại HT#4 (ca phân đen bị trấn an sai) — trong hôm nay.
   Ai: trưởng nhóm trực page. Đo: đã liên hệ được hay chưa.

2. Trang bị câu trả lời cho hai câu "soi có đau không" và "mê có hại không"
   cho cả nhóm trực page — 6/12 hội thoại vướng đúng hai câu này, chỉ 2 ca
   được trả lời có bằng chứng.
   Ai: trưởng nhóm. Đo: tỷ lệ ca có rào cản SỢ mà nhân viên nêu được bằng
   chứng, mục tiêu ≥70% kỳ sau.

3. Xin lễ tân ghi lý do hoãn tại chỗ, một dòng mỗi ca.
   Ai: quản lý phòng khám. Đo: có bảng đó để chạy R4 kỳ sau.
```

**Dấu hiệu sai:** nhiều hơn 3 việc · việc không có người phụ trách · việc không có cách đo · việc chung chung kiểu "cải thiện chất lượng tư vấn".

---

# 5. MODE TRA NHANH

```
Hỏi: Khách bảo "để qua Tết em đi" thì xếp mã nào?

L6.8 — NÉ KẾT QUẢ.
Nghĩa: khách biết mình nên soi nhưng trì hoãn vì sợ phát hiện ra bệnh.
Rào cản: NÉ (rào cản thứ tư, riêng ngành tiêu hóa — không gộp vào SỢ hay NGẠI).

Phân biệt với L6.4 (bận): nếu sau khi lùi, khách VẪN hỏi tiếp về lịch, về
mất bao lâu, về Chủ nhật có làm không → đó là L6.4. Nếu lùi mà không hỏi
thêm gì, và trước đó đã hỏi rất kỹ về bệnh → L6.8.

Nhịp chăm: D+7 → D+21 → D+45, nuôi tới 180 ngày. Nội dung GIÁO DỤC.
⛔ Không gửi ưu đãi giảm giá — họ không lùi vì tiền, và câu chào giá làm họ
   nghĩ đây là chỗ bán hàng.

Nguồn: P6 §2 · P2 §2 · P8 §5.
```

Dưới 15 dòng. Không mở báo cáo. Có nguồn module.

---

# 6. SÁU DẤU HIỆU BÁO CÁO ĐÚNG

1. 🚩 **Khối cờ đỏ ở đầu**, kể cả khi không có ca nào (ghi rõ "đã sàng N hội thoại").
2. Có **hai điểm dừng**, và nó thật sự đợi bạn trả lời.
3. Mỗi con số **gắn một việc phải làm**.
4. Chỗ chưa đo được thì ghi `⚠ chưa đo được` và **nói rõ cần xin gì từ ai** — không suy ra.
5. Nhóm dưới 10 hội thoại được đánh dấu `⚠ chưa đủ mẫu` và **không bị xếp hạng**.
6. Mọi con số giá đều gắn `⚠` và ghi rõ là khung giá công khai, không phải báo giá.

# 7. SÁU DẤU HIỆU BÁO CÁO SAI

1. Không nêu ca cờ đỏ, hoặc nêu ở cuối báo cáo.
2. Chạy một mạch không dừng.
3. Xếp hạng post bằng `% HOT` chưa trừ cờ đỏ.
4. Tự đặt mốc KPI rồi kết luận "đạt / không đạt".
5. Trả lời bằng toàn mã (`L6.8 · TH-04 · G2`) mà không giải nghĩa.
6. Viết ra khả năng khách mắc bệnh gì, hoặc trấn an *"chắc không sao"*.

---

# 8. Khi trợ lý không chạy được code

Một số nền tảng không bật được code. Lúc đó nó phải **nói rõ**, rồi trả **bảng markdown dán được vào Excel**:

```
Môi trường này không chạy được Python nên em không ghi ra file .xlsx được ạ.
Em trả bảng dưới đây, anh/chị copy dán vào Excel là thành bảng đúng cấu trúc.
Mỗi sheet là một bảng, em ghi rõ tên sheet ở trên mỗi bảng.

=== SHEET 1: 🚩 Cờ đỏ ===
| STT HT | Tên KH | Mã CĐ | NV có trấn an sai? | Việc phải làm ngay |
...
```

**Dấu hiệu sai:** nó im lặng bỏ qua yêu cầu xuất file, hoặc nói "đã tạo file" mà không có file nào.
