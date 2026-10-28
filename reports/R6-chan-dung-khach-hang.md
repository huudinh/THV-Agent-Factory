# R6 — CHÂN DUNG KHÁCH HÀNG TỪ DANH SÁCH KHÁCH

**Trả lời câu hỏi:** *Người đang đến Tiêu Hóa Việt là những ai, mỗi nhóm bao nhiêu người, họ vướng gì và đang dùng dịch vụ nào — để viết nội dung và chia ngân sách cho đúng người.*

**Cần có:** một **bảng danh sách khách** (`.xlsx` · `.csv` · dán thẳng cũng được) có các cột:

| Cột | Bắt buộc | Dùng để làm gì |
|---|---|---|
| Năm sinh **hoặc** tuổi | ✅ | Chia nhóm tuổi — trục quan trọng nhất của ngành này |
| Giới tính | nên có | Khác biệt rõ ở một số nhóm bệnh |
| Khu vực / địa chỉ (quận, tỉnh) | nên có | THV chỉ có 1 cơ sở → đo được bán kính thật của khách |
| Tình trạng (trạng thái hồ sơ) | nên có | Đã khám / đã soi / hẹn lại / huỷ hẹn |
| Vấn đề / triệu chứng / chẩn đoán | ✅ | Gán nhóm `TH-01…TH-12` |
| Dịch vụ đã sử dụng | ✅ | Gán nhóm giá trị `G1/G2/G3` |
| Lần soi thứ mấy / có hẹn soi lại | nên có | Đo được **vòng tái soi** — tệp đáng tiền nhất |

**Nhận lại:** 1 file Excel `output/THV_ChanDung_<kỳ>.xlsx`, **6 sheet**.

| Sheet | Góc nhìn |
|---|---|
| 1 · Chân dung | Mỗi nhóm khách một dòng: họ là ai, bao nhiêu người, nói gì với họ |
| 2 · Bảng chéo | Tuổi × nhóm vấn đề · nhóm vấn đề × nhóm giá trị · khu vực × nhóm giá trị |
| 3 · Khoảng trống | Nhóm đông trong hồ sơ mà vắng trong inbox — và ngược lại |
| 4 · ⭐ Vòng tái soi | Bao nhiêu người đến lần 2+, bao nhiêu người đang có hẹn chưa quay lại |
| 5 · Dữ liệu đã gán mã | Từng dòng khách kèm mã đã gán, để kiểm lại |
| 6 · Chú giải | Bộ mã đầy đủ |

> ⚠️ **R6 ĐỌC DANH SÁCH KHÁCH, KHÔNG ĐỌC HỘI THOẠI.** Bảng này không có nội dung tin nhắn → ⛔ **không chấm độ nóng**, ⛔ **không chấm 5 tín hiệu**, ⛔ **không viết kịch bản nhắn lại**. Ai cần những thứ đó thì chạy R1.
>
> 🔒 **Đây là dữ liệu sức khỏe của người bệnh thật** — nặng hơn mọi loại dữ liệu khác trong tập đoàn. Sheet 5 dùng **STT hoặc mã khách**, ⛔ không in tên. Chạy trên máy nội bộ. Kiểm file trước khi gửi ra ngoài.

---

## PROMPT — copy từ đây

````
# NHIỆM VỤ
Dựng chân dung khách hàng từ bảng danh sách khách {{FILE}}, kỳ {{KỲ}}.
Sinh ra ĐÚNG 1 file Excel: `output/THV_ChanDung_{{KỲ}}.xlsx` — 6 sheet.

Viết script Python dùng openpyxl, ghi file thật. Không chạy được code → nói rõ rồi
trả bảng markdown dán được vào Excel.

⛔ ĐÂY KHÔNG PHẢI FILE HỘI THOẠI. Không chấm độ nóng, không chấm 5 tín hiệu,
không viết kịch bản nhắn lại. Nếu tôi cần những thứ đó, tôi sẽ đưa file hội thoại.

# ĐẦU VÀO — NHẬN CỘT, KHÔNG BẮT TÔI SỬA FILE
Tên cột mỗi hệ CRM ghi một kiểu. Tự nhận dạng, báo lại đã hiểu cột nào là cột nào,
rồi tiếp tục. Thiếu cột nào thì nói rõ cột đó làm mất khả năng đọc gì — không dừng.
Cột tối thiểu để chạy được: tuổi (hoặc năm sinh) · vấn đề/triệu chứng · dịch vụ đã dùng.

# BƯỚC 1 — CHUẨN HOÁ. Chuẩn hoá một lần, cả 6 sheet đọc chung kết quả đó.

## Tuổi
Có năm sinh → tính tuổi theo năm của kỳ báo cáo.
Có tuổi sẵn → dùng luôn. Có cả hai mà lệch → ưu tiên năm sinh, đếm số dòng lệch.
Nhóm tuổi dùng CHUẨN NGÀNH TIÊU HÓA, không dùng nhóm 10 năm đều:
  < 18        — trẻ em & vị thành niên (⚠ kiểm phòng khám có nhận nhóm này không)
  18–29       — người trẻ, phần lớn là dạ dày & rối loạn tiêu hóa
  30–39       — nhóm triệu chứng dai dẳng, đi làm, ngại nghỉ
  40–49  ⭐   — NGƯỠNG TẦM SOÁT. Nhóm bắt đầu có chỉ định soi đại tràng tầm soát
  50–59  ⭐   — nhóm tầm soát chính
  60+         — nhóm nhiều bệnh nền, cần sàng lọc trước tiền mê
Ranh giới 40 tuổi là ranh giới có ý nghĩa y khoa, không phải ranh giới làm tròn.
Nói rõ điều đó ở đầu sheet 1.
Thiếu tuổi → nhóm "⚠ không rõ tuổi", đếm riêng, KHÔNG chia đều vào các nhóm khác.

## Giới tính
Chuẩn hoá về Nam / Nữ / ⚠ không rõ. Không suy từ tên.

## Khu vực
THV chỉ có MỘT cơ sở: 139 Đại La, Tương Mai, Hà Nội.
Gom về 3 mức: "Nội thành Hà Nội" · "Ngoại thành & vùng lân cận" (Hưng Yên, Bắc Ninh,
Hà Nam, Vĩnh Phúc, Hải Dương…) · "Tỉnh xa".
→ Đây là số liệu quyết định phạm vi chạy quảng cáo. Khách "tỉnh xa" chiếm tỷ lệ cao
  trong hồ sơ thật nghĩa là có nhu cầu thật từ xa — và nhóm đó cần nội dung khác:
  gộp mọi việc vào một buổi (xem P5 §4).
Thiếu cột → ghi ⚠ không đo được, nêu rõ mất khả năng đọc gì.

## Cột "Tình trạng" — TỰ NHẬN LOẠI, đừng đoán bừa
Đọc các giá trị thật có trong cột, rồi nói rõ đã hiểu theo loại nào:
- Trạng thái hồ sơ (mới / đang xử lý / đã xong)
- Trạng thái lịch hẹn (đã hẹn / đã đến / huỷ / hoãn)
- Trạng thái điều trị (đang theo dõi / đã kết thúc)
Hiểu sai chỗ này thì cả báo cáo lệch → báo ở DỪNG 1 để tôi sửa, rẻ hơn sửa sau.

# BƯỚC 2 — GÁN MÃ. Dùng đúng bộ mã có sẵn, ⛔ KHÔNG tự chế mã mới.

## Vấn đề / triệu chứng / chẩn đoán → TH-01…TH-12
Xét ưu tiên TỪ TRÊN XUỐNG, một dòng một mã chính:
TH-01 🚩 cờ đỏ (xuất huyết tiêu hóa, sụt cân nhanh, khó nuốt tăng dần, thiếu máu,
      khối ở bụng, vàng da, tiền sử gia đình ung thư tiêu hóa trực hệ)
TH-02 theo dõi sau can thiệp · đến hẹn soi lại
TH-03 tầm soát · không triệu chứng
TH-04 dạ dày – thực quản      TH-05 đại tràng – trực tràng
TH-06 chảy máu thấp · trĩ – hậu môn    TH-07 polyp · khối u đã biết
TH-08 gan – mật – tụy          TH-09 rối loạn tiêu hóa chung
TH-10 nhiễm HP                 TH-11 mang kết quả nơi khác đến
TH-12 chưa rõ / không ghi

⚠ LƯU Ý QUAN TRỌNG VỚI DỮ LIỆU HỒ SƠ: cột "vấn đề" trong bảng khách thường là
CHẨN ĐOÁN SAU KHI SOI, không phải triệu chứng lúc khách inbox. Hai thứ này khác nhau,
và đừng trình bày chúng như một. Ghi rõ ở đầu sheet 1 cột này là loại nào.
⛔ Không viết lại chẩn đoán chi tiết của từng người vào bất kỳ sheet nào. Chỉ dùng
   mã nhóm. Đây là dữ liệu sức khỏe.

## Dịch vụ đã sử dụng → nhóm giá trị
G1: combo dạ dày + đại tràng · can thiệp (cắt polyp, cầm máu) · gói tầm soát chuyên gia
G2: nội soi dạ dày HOẶC đại tràng đơn lẻ · soi + test HP
G3: khám chuyên khoa · nội soi trực tràng · sigma · siêu âm · xét nghiệm · test HP đơn lẻ
Dịch vụ không rõ → ⚠ không xác định, đếm riêng.

## Nhóm khách N1–N6 (dùng tuổi + vấn đề + tình trạng, theo thứ tự này)
N1 triệu chứng dai dẳng — TH-04/05/09, tuổi 18–49
N2 có cờ đỏ 🚩 — TH-01, mọi tuổi
N3 tầm soát chủ động — TH-03, hoặc TH-04/05 ở tuổi 40+ không triệu chứng rõ
N4 mang kết quả nơi khác đến — TH-11
N5 theo dõi sau can thiệp — TH-02 hoặc TH-07, hoặc lần soi thứ 2+
N6 người nhà đặt hộ / người cao tuổi — 60+, hoặc có dấu hiệu người khác đặt hộ
Một dòng chỉ thuộc MỘT nhóm. Trùng nhiều nhóm → lấy nhóm có số thứ tự nhỏ hơn
(N2 thắng mọi nhóm).

# DỪNG 1 — BÁO ĐỦ RỒI CHỜ TÔI XÁC NHẬN
In ra: tổng số dòng · số dòng dùng được · đã hiểu cột nào là cột nào ·
cột "Tình trạng" được hiểu theo loại nào · cột "Vấn đề" là triệu chứng hay chẩn đoán ·
phân bố nhóm tuổi · phân bố TH-xx · phân bố G1/G2/G3 · số dòng ⚠ thiếu dữ liệu ·
số dòng là lần soi thứ 2+ (nếu đo được).
Chờ tôi xác nhận trước khi dựng sheet.

# BƯỚC 3 — SHEET 1 · CHÂN DUNG
Một dòng mỗi nhóm khách N1–N6, cột:
Nhóm | Số người | % | Tuổi tập trung | Giới chiếm đa số | Nhóm vấn đề chủ đạo |
Nhóm giá trị chủ đạo | Khu vực chủ đạo | Nỗi lo thật | Rào cản dự đoán |
Câu hỏi ngầm | Giọng nên dùng | Nội dung nên viết cho nhóm này
⚠ Ghi rõ ngay dưới tiêu đề sheet: **rào cản và câu hỏi ngầm là SUY LUẬN TỪ NHÓM**
  (theo P2), không phải đo từ dữ liệu này — bảng khách không có nội dung tin nhắn.
Nhóm dưới 10 người → ghi ⚠ chưa đủ mẫu, không viết khuyến nghị nội dung.

# BƯỚC 4 — SHEET 2 · BẢNG CHÉO
Ba bảng chéo, mỗi bảng kèm một dòng "đọc bảng này thế nào":
① Nhóm tuổi × nhóm vấn đề TH-xx
② Nhóm vấn đề × nhóm giá trị G
③ Khu vực × nhóm giá trị G
→ Ô dưới 5 người để trống hoặc ghi "<5", không in số chính xác. Đây là dữ liệu sức
  khỏe: ô quá nhỏ thì có thể nhận ra người cụ thể.

# BƯỚC 5 — SHEET 3 · KHOẢNG TRỐNG (phần đáng tiền nhất của báo cáo)
Chỉ dựng được khi có cả R6 (bảng khách) và R1 (hội thoại) cùng kỳ. Cột:
Nhóm | % trong hồ sơ khách (R6) | % trong inbox (R1) | Chênh | Đọc ra điều gì |
Việc cần làm
Hai hướng chênh, hai ý nghĩa ngược nhau:
- Đông trong hồ sơ, VẮNG trong inbox → nhóm này đến bằng đường khác (giới thiệu,
  tìm Google, đi qua thấy biển). QUẢNG CÁO CHƯA CHẠM TỚI HỌ → cơ hội rõ nhất.
- Đông trong inbox, VẮNG trong hồ sơ → quảng cáo kéo đúng người nhưng MẤT Ở GIỮA
  PHỄU. Đọc kèm R4 để biết mất ở khâu nào.
Chưa có R1 cùng kỳ → ghi `⚠ chưa dựng được`, nêu rõ cần gì.

# BƯỚC 6 — SHEET 4 · ⭐ VÒNG TÁI SOI
Cột: Chỉ số | Số người | % | Nhận định | Việc cần làm
Tối thiểu:
- Số người đến lần đầu / số người đến lần 2+
- Số người thuộc TH-02 (đang trong vòng theo dõi)
- Số người ĐANG CÓ HẸN SOI LẠI mà chưa quay lại → đây là danh sách cần nhắc,
  không phải con số để đọc
- Số người từng cắt polyp (TH-07) → nhóm có chỉ định theo dõi dài hạn
- Tỷ lệ quay lại theo nhóm tuổi
⚠ Chu kỳ tái soi là CHỈ ĐỊNH Y KHOA CỦA BÁC SĨ cho từng ca. ⛔ Không tự nêu số năm,
  ⛔ không tự tính "đã quá hạn soi lại". Chỉ được đếm theo mốc đã ghi trong hồ sơ.
  Không có cột mốc hẹn → ghi `⚠ chưa đo được`, và nêu rõ: cần cột "ngày hẹn soi lại"
  trong hồ sơ để đo được tệp này.
→ Đây là tệp giá trị dài hạn lớn nhất của THV. Khác với mọi ngành khác trong tập đoàn,
  nhóm này không cần tạo nhu cầu — mốc quay lại đã nằm trong phiếu kết quả của họ.

# BƯỚC 7 — GHI FILE + TỰ KIỂM
Sheet 5 ghi lại từng dòng khách kèm mã đã gán: STT/mã khách | Nhóm tuổi | Giới |
Khu vực | TH-xx | Nhóm giá trị | Nhóm N | Lần soi | Ghi chú ⚠
  ⛔ KHÔNG in tên khách. ⛔ KHÔNG in chẩn đoán chi tiết, chỉ in mã nhóm.
Sheet 6 chú giải đầy đủ bộ mã: nhóm tuổi (và vì sao mốc 40) · TH-01…TH-12 ·
  G1/G2/G3 · N1–N6 · ⚠ · 🚩.

Tự kiểm và báo: tổng số người ở mọi sheet có bằng nhau không · có nhóm nào <10 người
mà vẫn viết khuyến nghị không · sheet 5 có lọt tên khách hay chẩn đoán chi tiết không ·
bảng chéo có ô nào <5 mà vẫn in số chính xác không.

# KHÔNG ĐƯỢC
- ⛔ Chấm độ nóng, chấm 5 tín hiệu, viết kịch bản nhắn lại từ dữ liệu này.
- ⛔ Suy ra rào cản của từng người cụ thể. Rào cản chỉ được nói ở mức NHÓM, và phải
  ghi rõ là suy luận từ P2.
- ⛔ In tên khách, số điện thoại, địa chỉ chi tiết, hay chẩn đoán chi tiết vào file.
- ⛔ Tự tính "đã quá hạn soi lại" cho từng người.
- ⛔ Tự chế nhóm tuổi khác, hoặc tự chế mã TH / G / N mới.
- ⛔ Kết luận từ nhóm dưới 10 người.

# TRÌNH BÀY EXCEL
- Font Arial. Freeze dòng tiêu đề. Wrap text ở cột nội dung dài.
- Sheet 1 mỗi chân dung một dòng, chiều cao dòng đủ đọc hết cột giọng và câu hỏi ngầm.
- Vàng cho mọi ô ⚠. Đỏ đậm cho dòng nhóm N2 (có cờ đỏ).
- Viền đậm cho dòng nhóm giá trị G1 và cho nhóm tuổi 40+.
````

## Đến đây

---

## Lưu ý khi dùng

**R6 chạy độc lập với R1–R5** vì nó đọc nguồn khác: bảng danh sách khách, không phải hội thoại. Có cả hai thì R1 trả lời *ai đang inbox*, R6 trả lời *ai đang thật sự đến phòng khám* — và sheet 3 (Khoảng trống) là chỗ hai câu trả lời đó gặp nhau. Nhóm đông ở R6 mà vắng ở R1 là **nhóm quảng cáo chưa chạm tới**.

**Mốc 40 tuổi trong bảng nhóm tuổi không phải mốc làm tròn.** Đó là ngưỡng mà chỉ định tầm soát bắt đầu đổi. Chia nhóm tuổi theo bước 10 năm đều (20–29, 30–39, 40–49) thì tình cờ vẫn đúng, nhưng nếu ai sửa thành 35–44 thì bảng mất ý nghĩa y khoa. Vì vậy prompt ghi rõ và cấm tự đổi.

**Cột "Vấn đề" trong bảng khách thường là chẩn đoán sau khi soi, không phải triệu chứng lúc inbox.** Đây là chỗ dễ nhầm nhất khi đọc R6 cạnh R1: R1 đếm *khách nói gì*, R6 đếm *bác sĩ kết luận gì*. Hai con số không khớp nhau là bình thường — và chính khoảng lệch đó nói lên nội dung nào đang kéo sai người. Nhưng phải biết mình đang đọc cái nào.

**Sheet 4 (Vòng tái soi) thường bắt đầu bằng `⚠ chưa đo được`** vì hồ sơ ít khi có cột "ngày hẹn soi lại" ở dạng đọc được bằng máy. Việc của lần chạy đầu là **xin cột đó**. Từ lần sau, đây là sheet trỏ thẳng ra một danh sách người cần gọi — loại danh sách có giá trị cao nhất mà lại rẻ nhất để có.

**Dữ liệu này nhạy cảm hơn mọi báo cáo khác trong repo.** Bảng danh sách khách của một phòng khám tiêu hóa chứa chẩn đoán — tức là thông tin về sức khỏe của người có tên tuổi địa chỉ. Prompt cố tình: không in tên ở sheet dữ liệu, không in chẩn đoán chi tiết, và ô bảng chéo dưới 5 người thì không in số chính xác (ô quá nhỏ có thể nhận ra người cụ thể). Kiểm lại file trước khi gửi cho bất kỳ ai ngoài nhóm quản lý.
