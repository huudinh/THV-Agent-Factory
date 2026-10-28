# 05 · XỬ LÝ SỰ CỐ

Tra theo triệu chứng. Mỗi mục có **câu gõ lại** để sửa ngay trong chat.

---

# 1. 🚩 Lỗi an toàn — xử lý trước mọi lỗi khác

| Triệu chứng | Nghĩa là | Gõ lại |
|---|---|---|
| **Không nêu ca cờ đỏ** khi file rõ ràng có | Nó đang chạy như một hệ bán hàng thường | *"Quét lại toàn bộ file theo 6 mã CĐ-1…CĐ-6 ở P4 §3. Liệt kê từng ca kèm số hiệu hội thoại và trích dẫn lời khách."* |
| **Nêu cờ đỏ ở cuối báo cáo** | Sai thứ tự, người đọc sẽ không tới đó | *"Đưa khối cờ đỏ lên đầu, trước cả ba dòng kết luận. Đây là yêu cầu của P8 §11."* |
| **Trấn an khách**: *"chắc không sao đâu"* | Vi phạm nặng nhất của hệ | *"Xoá câu đó. P5 §1 lỗi 1: không được trấn an ca có cờ đỏ. Viết lại bản chỉ mời khám sớm, không nêu giá, không nói khả năng mắc bệnh gì."* |
| **Kết luận bệnh** hoặc **loại trừ ung thư** | Ngoài phạm vi, sai pháp lý | *"Bỏ phần kết luận bệnh. Em chỉ được nói cần bác sĩ đánh giá sớm."* |
| **Đọc kết quả nội soi / xét nghiệm** | Ngoài phạm vi | *"Không đọc kết quả. Viết lại theo hướng mời bác sĩ đọc trực tiếp."* |
| **Tư vấn thuốc / liều / phác đồ** | Ngoài phạm vi | *"Bỏ phần thuốc. P5 §1 lỗi 4."* |
| **Hứa chắc tiền mê được** | Chưa sàng lọc bệnh nền | *"Sửa thành: bác sĩ phải khám sàng lọc trước mới quyết định được."* |

> Nếu trợ lý mắc **bất kỳ lỗi nào ở mục 1** trong lúc chạy thử, **đừng dùng với dữ liệu thật** cho tới khi sửa xong. Kiểm lại hai việc: ô chỉ dẫn đã dán **toàn bộ** phần giữa hai vạch chưa, và `P4` + `P5` + `P8` đã upload chưa.

---

# 2. Trợ lý trả lời sai kiểu

| Triệu chứng | Gõ lại |
|---|---|
| Trả lời bằng toàn mã, không giải nghĩa | *"Nói lại bằng tiếng Việt thường, mã nào dùng lần đầu thì giải nghĩa ngay."* |
| Hỏi câu kỹ thuật (encoding, schema, định dạng cột) | *"Đừng hỏi em về kỹ thuật file. Em cần gì thì nói việc cần làm."* |
| Mở đầu báo cáo bằng phương pháp | *"Bỏ phần mô tả phương pháp. Ba dòng đầu phải là ba điều quan trọng nhất, mỗi dòng một con số."* |
| Đòi tạo AI-Agent / viết system prompt | *"Việc đó ngoài phạm vi theo §1. Em chỉ đọc số liệu ra báo cáo."* |
| Tự nhận đã gửi tin cho khách | *"Em chỉ viết bản gợi ý. Người duyệt rồi dán lại."* |

---

# 3. Trợ lý chấm sai

| Triệu chứng | Nghĩa là | Gõ lại |
|---|---|---|
| **HOT quá nhiều** (trên 50%) | Có thể đúng — nếu phần lớn là do luật ghi đè | *"Tách giúp mình: bao nhiêu ca HOT do đủ điểm, bao nhiêu do ghi đè, ghi đè nào."* |
| **Mọi ca cờ đỏ đều HOT nên %HOT vô nghĩa** | Đúng cơ chế, sai cách đọc | *"Thêm cột % HOT trừ cờ đỏ và dùng cột đó để so sánh post."* |
| **Xếp ca "để qua Tết" vào L6.4** | Nhầm NÉ thành NGẠI | *"Đọc lại P6 §2 phần phân biệt L6.4 với L6.8. Ca này sau khi lùi có hỏi tiếp về lịch không?"* |
| **Xếp máu đỏ tươi vào cờ đỏ** | Nhận quá rộng | *"Máu đỏ tươi kèm rát hậu môn là TH-06, không phải cờ đỏ. Phân đen mới là CĐ-1. Xem P4 §2."* |
| **Bỏ qua nhóm tầm soát** vì họ COLD | Đúng điểm, sai hướng | *"Nhóm TH-03 là G1. Xem lại ma trận ở P4 §4: WARM·G1 đáng hơn HOT·G3."* |
| **Hai bảng cho hai con số khác nhau** về cùng một hội thoại | Chấm hai lần | *"Chấm lại một lần duy nhất rồi cho mọi bảng đọc từ kết quả đó. Đối chiếu lại và báo chỗ lệch."* |
| **Bitmask không có** | Không ai kiểm lại được điểm | *"Thêm cột bitmask 5 chữ số cho từng hội thoại."* |

---

# 4. Trợ lý kết luận sai hướng

| Triệu chứng | Gõ lại |
|---|---|
| Xếp hạng nhóm chỉ có 4–6 hội thoại | *"Nhóm dưới 10 hội thoại thì ghi ⚠ chưa đủ mẫu và bỏ xếp hạng."* |
| Kết luận từ bảng chia nhóm mà không có cột `% HOT*` | *"Thêm cột % HOT* chấm lại không kể tín hiệu ①. Nếu chênh lệch biến mất thì nói thẳng là không có bằng chứng."* |
| Tự đặt mốc KPI rồi nói "chưa đạt" | *"P8 §7 chưa có mốc cho chỉ số này. Nêu số thật và ghi ⚠ chưa có mốc so sánh."* |
| Lấy "đặt lịch" thay cho "đến khám" | *"Ba con số khác nhau: đặt lịch, đến khám, soi được. Thiếu số nào thì ghi ⚠ chưa đo được."* |
| Gán nguyên nhân mà không có bằng chứng | *"Bỏ phần nguyên nhân. Chỉ được nói 'tăng cùng lúc với việc X' nếu X có trong dữ liệu."* |
| Khuyên tắt post kéo ít khách nhưng toàn G1 | *"Đọc kèm bảng Post × Nhóm giá trị trước khi khuyến nghị tắt."* |
| Khuyên giảm giá cho nhóm né kết quả | *"Nhóm L6.8 không lùi vì tiền. Đổi sang nội dung giáo dục, nhịp D+7/D+21/D+45."* |

---

# 5. Lỗi dữ liệu đầu vào

| Triệu chứng | Nguyên nhân | Làm gì |
|---|---|---|
| Tách được ít hội thoại hơn thực tế | File lệch định dạng, hoặc tiêu đề hội thoại không theo mẫu | Hỏi: *"Em đọc được cấu trúc file thế nào? Báo lại rồi tiếp tục."* Không cần sửa file |
| Mọi hội thoại đều "không rõ nguồn" | File thiếu thẻ chiến dịch | Chỉ chạy được R1/R3/W1. Muốn chạy R2 thì xuất lại từ CRM có cột thẻ |
| Mất tiêu chí ① ở R3 | File không có dấu thời gian từng tin | Chấp nhận, chuẩn đạt đổi sang ≥7/9. Hoặc xuất lại có dấu thời gian |
| Tỷ lệ HOT cao bất thường, mọi post đều tốt | **Mẫu đã bị lọc** theo độ dài hoặc theo có SĐT | Nói rõ với trợ lý. Nó sẽ gắn cảnh báo và không dùng số để quyết ngân sách |
| R6 hiểu sai cột "Tình trạng" | Mỗi hệ CRM ghi một kiểu | Sửa ngay ở DỪNG 1. Rẻ hơn sửa sau khi đã dựng xong 6 sheet |
| R6 trộn chẩn đoán với triệu chứng | Cột "Vấn đề" trong hồ sơ là chẩn đoán sau soi | Nói trước: *"Cột này là chẩn đoán sau soi, không phải điều khách kể lúc inbox."* |

---

# 6. Vấn đề kỹ thuật nhẹ

| Triệu chứng | Làm gì |
|---|---|
| Không xuất được file Excel | Bật Code Interpreter (ChatGPT) · hoặc yêu cầu: *"Trả bảng markdown dán được vào Excel, ghi rõ tên từng sheet."* |
| File Excel thiếu sheet so với khuôn | *"Đọc lại khuôn reports/R{n} và dựng đủ sheet theo đúng thứ tự."* |
| Không đọc được file `.xlsx` | Lưu lại thành `.csv`, hoặc copy dán trực tiếp vào chat |
| Trả lời bị cắt giữa | *"Tiếp tục từ chỗ bị cắt."* Hoặc chạy từng sheet một |
| Dùng số giá của tháng trước | *"Lấy số từ P7 bản hiện hành. Mình vừa upload bản mới, xoá bản cũ khỏi Knowledge chưa?"* |

---

# 7. Khi không biết lỗi ở đâu — làm lại 4 bước

1. **Kiểm ô chỉ dẫn**: đã dán **toàn bộ** phần giữa `▼▼▼` và `▲▲▲` chưa? Dán thiếu là lỗi hay gặp nhất.
2. **Kiểm Knowledge**: có đủ `P4`, `P6`, `P8` chưa? Ba file này giữ bộ mã, cờ đỏ và cách chấm — thiếu một file là trợ lý tự nghĩ ra cách chấm riêng.
3. **Kiểm bản P7**: còn bản tháng cũ trong Knowledge không? Hai bản cùng lúc thì nó trộn số.
4. **Chạy lại 10 câu thử** ở [`01-cai-dat.md`](01-cai-dat.md) mục 3. Câu nào sai thì biết hổng ở đâu.

Vẫn sai → mở chat mới. Chat dài có thể đã trôi mất phần đầu của cuộc trao đổi.
