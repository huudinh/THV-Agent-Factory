# P8 — CHUẨN CHẤM ĐIỂM · PHÂN LOẠI · SLA · KPI
Module brand-specific. **Đây là thước đo của toàn bộ hệ báo cáo.** Khi module khác mâu thuẫn với P8 về cách chấm, **P8 thắng**. Cập nhật: 2026-10-28.

---

## §1. ⭐ NĂM TÍN HIỆU → HOT / WARM / COLD

Mỗi tín hiệu **1 điểm**, chấm trên toàn hội thoại:

| # | Tín hiệu | Tính là CÓ khi |
|---|---|---|
| **①** | **Nêu triệu chứng / chỉ định cụ thể** | *"đau thượng vị 2 tháng"*, *"đi ngoài ra máu"*, *"bác sĩ bảo cần soi đại tràng"*, *"cần soi lại sau cắt polyp"* — **không** tính *"khám tiêu hóa"*, *"tư vấn giúp em"* |
| **②** | **Mốc thời gian ≤ 14 ngày** | Nói rõ hôm nay / mai / tuần này / Chủ nhật này · hoặc đã đặt lịch · hoặc đang trên đường đến |
| **③** | **Hỏi lịch, bác sĩ, giá, hoặc cách chuẩn bị theo đúng tình trạng của mình** | *"ca của em thì soi loại nào"*, *"bác sĩ Giang có lịch Chủ nhật không"*, *"em huyết áp cao thì mê được không"* — **không** tính câu hỏi giá chung chung ở tin đầu |
| **④** | **Gửi kết quả / mô tả rõ** | Có ảnh kết quả nội soi · xét nghiệm · đơn thuốc · phiếu hẹn, **hoặc** mô tả đủ: triệu chứng · bao lâu · đã khám/uống thuốc gì |
| **⑤** | **Để lại SĐT/Zalo thật và đồng ý nhận tư vấn** | Ưu tiên có nêu khung giờ tiện nghe máy |

| Mức | Điểm | Nghĩa |
|---|---|---|
| **HOT** | **4–5** | Sẵn sàng đặt lịch khám |
| **WARM** | **2–3** | Quan tâm rõ, còn vướng rào cản hoặc đang so sánh |
| **COLD** | **0–1** | Hỏi tham khảo |

### ⭐ Bốn luật ghi đè — đặc thù ngành tiêu hóa

1. **Đã đặt lịch, hoặc đang đến phòng khám → HOT** bất kể điểm.
2. 🚩 **CÓ CỜ ĐỎ (`TH-01` / `CĐ-1`…`CĐ-6`) → HOT** bất kể điểm, **và gắn cờ ưu tiên y tế**. Gọi ngay bất kể khung giờ, chuyển bác sĩ trong ngày. **Đây là luật an toàn, không phải luật bán hàng** — nó tồn tại để không bỏ sót người bệnh, không phải để xếp hạng lead ([[P4-dich-vu]] §3).
3. **Đã có kết quả nội soi / CT / xét nghiệm từ nơi khác, hoặc đã được bác sĩ nơi khác chỉ định soi (`TH-11`) → HOT** bất kể điểm. Khách đã qua giai đoạn "có cần soi hay không", **chỉ còn chọn nơi làm** — đây là lead nóng nhất của ngành, mà thang 5 tín hiệu thường chấm thấp oan vì tin nhắn của họ rất ngắn.
4. **Đang trong vòng theo dõi / đến hẹn soi lại (`TH-02`) → tối thiểu WARM.** Nhóm này viết tin ngắn, không có triệu chứng cấp, nhưng **gần như chắc chắn soi** — họ chỉ đang chọn đặt lịch ở đâu.

> **So với ngành nha:** ở đó ba luật ghi đè đều nhằm **không chấm thấp oan lead nóng**. Ở đây luật ② có mục đích khác hẳn: **không để sót ca cần ưu tiên y tế**. Hai mục đích đó phải đọc riêng — một ca cờ đỏ được chấm HOT **không** có nghĩa là ca đó dễ chốt, mà có nghĩa là **phải gọi trước mọi ca khác**.

### Cách ghi lại
Ghi kết quả dạng **bitmask 5 chữ số**: `[10110]` = có ①③④, thiếu ②⑤.
Mọi file Excel phải có cột bitmask này. **Không có bitmask thì không ai kiểm lại được điểm.**
Áp luật ghi đè thì ghi rõ: `[01011] → HOT (ghi đè ③: đã có kết quả nơi khác)`.

---

## §2. CHẤM LẠI KHÔNG KỂ TÍN HIỆU ① — cột `% HOT*`

> ⚠️ **Luật chống lặp vòng. Đây là lỗi phân tích đã xảy ra thật và phải chống bằng quy tắc, không bằng sự cẩn thận.**

Tín hiệu ① là *"nêu triệu chứng/chỉ định cụ thể"*. Khi một bảng **chia nhóm theo nhóm vấn đề tiêu hóa** (biểu đồ nhiệt), thì mọi nhóm có vấn đề cụ thể **đã được cộng sẵn 1 điểm** — trong khi nhóm `TH-12 chưa rõ` thì không. So sánh `% HOT` giữa các nhóm đó là so sánh một thứ đã được định nghĩa sẵn: **kết luận giả**.

**Bắt buộc:** mọi bảng chia nhóm theo nhóm vấn đề phải có thêm cột **`% HOT*`** — chấm lại chỉ bằng 4 tín hiệu ②③④⑤, đạt **≥3/4** tính là HOT\*.

Ghi ngay dưới bảng: cột nào dùng được, cột nào không, và số thật là bao nhiêu. **Nếu bỏ tín hiệu ① mà chênh lệch biến mất thì nói thẳng là "không có bằng chứng"**, không được giữ kết luận cũ.

→ Luật này áp cho **mọi** trường hợp chia nhóm theo một thuộc tính vốn là tín hiệu chấm điểm, không chỉ riêng tín hiệu ①.

> **Một bẫy lặp vòng thứ hai, riêng của hệ này:** luật ghi đè ② đẩy mọi ca cờ đỏ lên HOT. Vì vậy **bảng `% HOT` theo nhóm vấn đề luôn cho `TH-01` = 100% HOT** — con số đó vô nghĩa, nó chỉ phản ánh chính luật ghi đè. Khi so sánh nhóm vấn đề hoặc so sánh post, **phải loại `TH-01` ra hoặc tách riêng**, và ghi rõ đã làm vậy.

---

## §3. BA TRỤC + MỘT CỜ & MA TRẬN ƯU TIÊN

Ba trục: **L-code** ([[P6-van-hanh]] §2) · **Độ nóng** (§1 trên) · **Nhóm giá trị G1/G2/G3** ([[P4-dich-vu]] §4). Cộng cột 🚩 **Cờ đỏ**. Bốn cột riêng, không gộp.

Ma trận ưu tiên HOT/WARM/COLD × G1/G2/G3: xem [[P4-dich-vu]] §4. **Ca cờ đỏ đứng ngoài ma trận — gọi ngay.**

**Điều phải nhớ khi viết khuyến nghị:** HOT·G3 chốt nhanh nhưng giá trị nhỏ; WARM·G1 chậm nhưng đáng đầu tư hơn. Báo cáo nào xếp hạng lead chỉ bằng độ nóng là báo cáo sai hướng cho ngành này.

---

## §4. SLA GỌI SAU KHI CÓ SỐ

| Khung giờ nhận số | 🚩 **Cờ đỏ** | HOT · G1 | HOT · G2–G3 | WARM | COLD |
|---|---|---|---|---|---|
| **7h–17h (cả Chủ nhật)** | ≤ **5'**, gọi trước mọi ca | ≤ **10'** | ≤ 15' | ≤ 30' | Nhắn Zalo ≤2h, gọi trong ngày |
| **17h–21h** | ≤ **15'** hoặc nhắn ngay + gọi đầu giờ sáng | ≤ 20' | ≤ 30' | ≤ 60' hoặc đúng giờ hẹn | Hàng đợi sáng hôm sau |
| **21h–7h** | **Nhắn ngay** ghi nhận + mời khám sớm, gọi 7h–8h | 7h–9h | 8h–10h | 9h–11h | 10h–12h |

**Giới hạn tải:** khoảng **8 số HOT/giờ/người**. Vượt thì chuyển người cùng bậc đang rảnh.

> **Ngoại lệ quan trọng nhất của ngành tiêu hóa — ca có cờ đỏ** 🚩: gọi ngay bất kể độ nóng, bất kể nhóm giá trị, bất kể khung giờ; **và chuyển bác sĩ / người phụ trách chuyên môn trong ngày**. ⛔ Không đưa ca cờ đỏ vào nhịp nuôi dưỡng, ⛔ không gửi nội dung ưu đãi.
>
> **Phòng khám mở cả Chủ nhật** → SLA áp cho **cả 7 ngày**. Hội thoại đến Chủ nhật mà không có ai trả lời là lỗi vận hành, không phải "ngoài giờ". Báo cáo đếm riêng hội thoại Chủ nhật và thời gian phản hồi của ngày đó.

---

## §5. CHUỖI CHĂM SÓC SAU KHI XIN SỐ — T+0 → T+7

| Mốc | Việc |
|---|---|
| **T+0 ≤ 2'** | Nhắn xác nhận: **tên người sẽ gọi · số sẽ gọi · giờ gọi** (bước B5) |
| **T+30'** | Chưa nghe máy → hỏi lại khung giờ tiện nghe máy để báo bác sĩ sắp xếp |
| **T+2h** | Gửi nội dung giá trị theo đúng rào cản (ai soi · hệ máy · tiền mê có bác sĩ gây mê riêng · quy trình dây soi), hỏi lại khung giờ |
| **T+24h** | Gọi lần 2. Trực page **nhắn nhắc 15 phút trước** |
| **T+48h · ĐÃ CÓ LỊCH** | ⭐ **Gửi hướng dẫn chuẩn bị** `{hướng_dẫn_chuẩn_bị}` + hỏi **bệnh nền, thuốc đang dùng, có người đưa về không** |
| **T–1 ngày (trước buổi hẹn)** | ⭐ **Nhắc chuẩn bị lần hai**: giờ nhịn ăn, mang kết quả cũ, mang theo người đi cùng nếu tiền mê |
| **T+72h (chưa có lịch)** | Mời khám (nhấn **bác sĩ xem rồi mới quyết định có soi**), kèm chương trình nếu có |
| **T+7 ngày** | **Lần chạm cuối.** Không phản hồi thì chuyển nhóm nuôi dưỡng dài hạn |

**Trần: tối đa 6 lần nhắn / 7 ngày. Khách từ chối thì dừng ngay.**

> ⭐ **Hai mốc `T+48h` và `T–1 ngày` là phần riêng của ngành nội soi, và là phần rẻ nhất để sửa trong cả hệ.** Chúng tồn tại để chống **mốc rò 2** ([[P3-hanh-vi-trang-thai]] §3): khách đến tận nơi mà không soi được vì chưa nhịn ăn, ruột chưa sạch, không đủ điều kiện mê, hoặc không có người đưa về. Một tin nhắn mẫu đúng lúc cứu được cả một buổi của hai bên.
>
> **Ba nhịp khác nhau, đừng lẫn:** chuỗi **T** dùng **ngay sau khi xin được số** · nhịp **D+3 / D+7 / D+15** dùng khi **đã tư vấn mà chưa đặt lịch** (`L6.x`) · nhịp **D+7 / D+21 / D+45** dùng riêng cho **`L6.8` né kết quả**, nội dung giáo dục không ưu đãi. Với **`L6.x · G1`** thì nuôi tới **90 ngày**; với **`L6.8`** tới **180 ngày**.

---

## §6. ⭐ BẢNG CHẤM HỘI THOẠI — 10 TIÊU CHÍ · CHUẨN ĐẠT ≥ 8/10

| # | Tiêu chí | Đạt khi |
|---|---|---|
| **①** | **Phản hồi ≤ 2 phút** | Chênh lệch dấu thời gian tin khách → tin nhân viên đầu tiên ≤ 2' |
| **②** | **Gọi đúng tên dịch vụ / triệu chứng** theo post khách bấm vào | Tin mở nhắc đúng dịch vụ, không hỏi chung "cần tư vấn gì" |
| **③** | 🚩 **SÀNG CỜ ĐỎ** | Có hỏi hoặc có nhận ra dấu hiệu cờ đỏ; **ca có cờ đỏ được mời khám sớm và ghi nhận chuyển bác sĩ**. Bỏ sót cờ đỏ = **không đạt tiêu chí này VÀ trừ nặng ở ⑨** |
| **④** | **Thu đủ 5 thông tin** | Triệu chứng + bao lâu · cờ đỏ · đã khám/soi ở đâu chưa · **bệnh nền & thuốc đang dùng** · thời gian dự kiến ([[P5-kich-ban]] §3) |
| **⑤** | **Tạo tin cậy bằng bằng chứng**, đúng rào cản khách mang | Có ít nhất 1 bằng chứng thật ([[P1-thuong-hieu]] §2), không chỉ tính từ |
| **⑥** | ⭐ **Dặn chuẩn bị khi mời khám / đã có lịch** | Có nhắc việc chuẩn bị để soi được luôn nếu bác sĩ chỉ định. Dữ liệu không tới mốc có lịch → `⚠ không đo được`, không cho 0 oan |
| **⑦** | **Xin số có lý do có lợi cho khách** | Lý do kiểu "để bác sĩ xem trước và sắp lịch đúng buổi anh/chị tiện". ❌ "để gửi ưu đãi" |
| **⑧** | **Phiếu bàn giao đủ 14 trường** ([[P6-van-hanh]] §5) | Dữ liệu không có phần ghi chú → `⚠ không đo được`, không cho 0 oan |
| **⑨** | **Không vi phạm an toàn & pháp lý** | Không từ cấm · **không trấn an ca cờ đỏ** · không chẩn đoán/loại trừ bệnh · không đọc kết quả · không tư vấn thuốc · không hứa chắc tiền mê · không báo giá thiếu điều kiện ([[P5-kich-ban]] §1 · §5) |
| **⑩** | **Nêu rõ bước tiếp theo** | Ai gọi · số nào · lúc mấy giờ (bước B5) |

> **Vi phạm tiêu chí ⑨ thì toàn hội thoại 0 điểm**, bất kể 9 tiêu chí kia. Đây là rủi ro pháp lý và rủi ro an toàn người bệnh, không phải lỗi kỹ năng.
>
> **Trong tiêu chí ⑨, nặng nhất là trấn an một ca có cờ đỏ.** Báo cáo phải **đếm riêng** lỗi này và đưa lên **sheet đầu tiên**, kèm trích dẫn thật — không gộp vào tổng số lỗi.

**Cách báo điểm:** luôn kèm **trích dẫn thật** từ hội thoại làm bằng chứng cho mỗi tiêu chí bị trừ. Bảng điểm không có trích dẫn thì nhân viên không phục và trưởng nhóm không đào tạo được.

---

## §7. KPI — mốc để báo cáo so vào

| Chỉ số | Mục tiêu | Ghi chú |
|---|---|---|
| 🚩 **Ca cờ đỏ được nhận diện / tổng ca có dấu hiệu cờ đỏ** | **100%** | **Mốc duy nhất không thương lượng.** Dưới 100% là phát hiện phải báo ngay, không chờ cuối kỳ |
| 🚩 **Ca cờ đỏ được gọi ≤ 5'** | ≥ **95%** | `⚠ mốc tham chiếu, chờ THV chốt` |
| Tỷ lệ hội thoại **xin được số** | `⚠ chờ THV chốt` | Chỉ số chính của trực page |
| **Kết nối / số đã xin** (gọi được) | ≥ **78%** | Khâu hay hổng nhất |
| **Đặt lịch / kết nối** | ≥ **50%** | |
| **Đến khám / đặt lịch** (show-up) | `⚠ chờ THV chốt` | Mốc rò 1 |
| ⭐ **Thực hiện được nội soi / đến khám** | `⚠ chờ THV chốt` | **Mốc rò 2** — chỉ số riêng của ngành nội soi, xem [[P3-hanh-vi-trang-thai]] §3 |
| ⭐ **Hoãn tại chỗ do chuẩn bị không đạt** | càng thấp càng tốt | Đây là **lỗi dặn dò**, sửa được bằng tin nhắn mẫu. Có số thì mới sửa được |
| **Tệp đến hẹn soi lại được nhắc** | `⚠ chờ THV chốt` | Vòng LTV của ngành |
| Số được **phân loại + có phiếu đủ** | ≥ **95%** | |
| Điểm chấm hội thoại | ≥ **8/10** | |

> **Chưa có mốc thì báo cáo nêu số thật và ghi `⚠ chưa có mốc so sánh`** — tuyệt đối không tự đặt mốc rồi kết luận "đạt / không đạt". Mốc là việc của THV chốt, không phải việc của trợ lý suy ra.
>
> Các mốc có số ở trên (78% · 50% · 95% · 8/10) là **mốc tham chiếu kế thừa từ hệ CSKH của tập đoàn**, chưa được THV xác nhận cho ngành tiêu hóa. Báo cáo phải ghi rõ điều đó khi so vào. **Riêng mốc 100% nhận diện cờ đỏ là mốc của chính hệ này**, không thương lượng.

---

## §8. NĂM RỦI RO ĐỌC SỐ — báo cáo phải tự kiểm

| Rủi ro | Biểu hiện | Cách chống |
|---|---|---|
| **Mẫu bị lọc** | File hội thoại chỉ gồm "hội thoại dài" hoặc "hội thoại có số" | Hội thoại dài = khách tương tác nhiều = **đã thiên về phía nóng**. Thổi phồng mọi post, và thổi **không đều nhau** → ghi cảnh báo, **không dùng để quyết ngân sách** |
| **Mẫu nhỏ** | Một post / một nhóm có **dưới 10 hội thoại** | Ghi `⚠ chưa đủ mẫu`. **Không xếp hạng, không khuyến nghị** |
| **Lặp vòng** | Chia nhóm theo đúng thuộc tính đang dùng để chấm điểm | Chấm lại không kể tín hiệu đó (§2). **Nhớ tách `TH-01` ra** vì luật ghi đè đẩy nhóm đó lên 100% HOT |
| **Lạm phát HOT** | Chấm rộng tay nên HOT tràn lan, SLA vỡ | Đối chiếu **tỷ lệ đến khám của nhóm HOT**. HOT mà show-up thấp là chấm sai, không phải khách tệ |
| ⭐ **Lẫn hai mốc cuối phễu** | Lấy "đặt lịch" thay cho "đến khám", hoặc lấy "đến khám" thay cho "thực hiện được nội soi" | Ba con số, ba cột riêng. Thiếu cột nào thì ghi `⚠ chưa đo được`, **không suy ra**. Lẫn mốc 2 là che đi đúng chỗ mất tiền nhiều nhất của ngành |

---

## §9. BÁO CÁO NÀO DÙNG PHẦN NÀO CỦA P8

| Báo cáo | Dùng |
|---|---|
| [[R1-phan-loai-hoi-thoai]] | §1 · §2 · §3 · §5 |
| [[R2-phan-tang-quang-cao]] | §1 · §2 · §8 |
| [[R3-chat-luong-tu-van]] | §6 · §4 · §5 |
| [[R4-bao-cao-dieu-hanh]] | §3 · §7 · §8 |
| [[R5-so-sanh-hai-ky]] | §7 · §8 |
| [[R6-chan-dung-khach-hang]] | §3 · §8 |
| [[W1-kho-cau-hoi-noi-dung]] | §2 (chống lặp vòng khi xếp hạng câu hỏi) |

## 🔶 Cần THV xác nhận
- Mốc KPI: tỷ lệ xin số · show-up · **thực hiện được nội soi / đến khám** · tệp tái soi được nhắc: `⚠ chờ cấp`
- **Tiêu chí sàng lọc trước tiền mê** (bệnh nền nào cần hội chẩn, xét nghiệm nào bắt buộc): `⚠ chờ cấp`
- **Bản hướng dẫn chuẩn bị trước nội soi chính thức**: `⚠ chờ cấp`
- Quy trình nội bộ khi trực page gặp ca cờ đỏ: **chuyển cho ai, bằng kênh nào, trong bao lâu**: `⚠ chờ cấp` — đây là slot trống quan trọng nhất của cả repo
- Phân tầng nhân sự CSKH để định tuyến HOT·G1 và ca cờ đỏ: `⚠ chờ cấp`
