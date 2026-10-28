# CHANGELOG

---

## v1.0 — 2026-10-28 · Bản khởi tạo

Dựng từ kiến trúc [`Paris-Agent-Factory`](../../Paris-Agent-Factory/) v1.0 cho **Phòng khám Đa khoa Tiêu Hóa Việt**.

### Kế thừa nguyên vẹn từ Paris
- Công thức **lõi brand-neutral + module thương hiệu `P`**: đổi brand = thay module `P`, không sửa lõi.
- 4 chế độ (kiểm dữ liệu · ra báo cáo · tra nhanh · giải thích số).
- Quy trình 5 bước, **2 điểm dừng**, luật một lần chấm.
- Thang 5 tín hiệu → HOT/WARM/COLD, bitmask, luật `% HOT*` chống lặp vòng.
- Rubric 10 tiêu chí, luật 0 điểm khi vi phạm tiêu chí an toàn/pháp lý.
- Ngưỡng mẫu 10 hội thoại · cổng chặn so hai kỳ · ngưỡng nhiễu theo cỡ mẫu.
- Bộ công cụ `tools/` (3 file Python) — đã port sang taxonomy tiêu hóa.

### Thêm mới cho ngành tiêu hóa
| Thành phần | Nội dung |
|---|---|
| 🚩 **Cột cờ đỏ `CĐ-1…CĐ-6`** | Cột an toàn, chồng lên mọi mã L. Luật ghi đè → HOT. Mốc nhận diện 100%, không thương lượng |
| **Rào cản thứ tư `NÉ`** | `L6.8` né kết quả — nhóm biết nên soi nhưng sợ phát hiện ra bệnh. Nhịp riêng `D+7/D+21/D+45`, nuôi 180 ngày |
| **Hai mã L mới** | `L6.7` ngại tiền mê · `L6.9` ngờ vệ sinh dây soi |
| **12 nhóm `TH-01…TH-12`** | Thay 11 nhóm vấn đề răng. `TH-01` = cờ đỏ, luôn thắng mọi nhóm |
| **Nhóm giá trị `G1/G2/G3`** | Đổi ký hiệu từ `V1/V2/V3` của Paris để không lẫn với `TH-xx` |
| **Mốc rò 2 của phễu** | "Đến khám" ≠ "thực hiện được nội soi". Bảng lý do hoãn tại chỗ ở R4 |
| **Vòng tái soi** | Cơ chế LTV mới: mốc quay lại nằm sẵn trong phiếu kết quả của khách |
| **Luật ghi đè thứ 4** | `TH-02` đến hẹn soi lại → tối thiểu WARM |
| **Hai mốc chăm sóc mới** | `T+48h` gửi hướng dẫn chuẩn bị · `T–1 ngày` nhắc lại |
| **Phiếu bàn giao 14 trường** | Thêm cờ đỏ · bệnh nền & thuốc đang dùng · kết quả nơi khác |
| **Khung B2 thu 5 thông tin** | Thêm sàng cờ đỏ và bệnh nền |
| **Tiêu chí ③ và ⑥ của rubric** | Sàng cờ đỏ · dặn chuẩn bị |
| **Học phần `M0`** | Sàng cờ đỏ & giới hạn chuyên môn. Luôn ở tuần 1 nếu có ca bị xử lý sai |
| **`P9` + nhóm `W1–W3`** | Module nội dung website: kho câu hỏi thật → đề bài · rà soát bài cũ theo luật y tế · bản đồ cụm & lịch 8 tuần |
| **Cột `% HOT (trừ cờ đỏ)`** | Chống bẫy: luật ghi đè đẩy mọi ca cờ đỏ lên HOT nên `% HOT` không nói về quảng cáo |
| **Trang hướng dẫn** | [Artifact HTML](https://claude.ai/artifact/H9LDZsYucRSeGvqnX2ubkg) tự đủ để cài: nhúng sẵn bộ não + 2 file gộp + **22 prompt** bấm copy, mở đầu bằng khối cờ đỏ |

### Bỏ so với Paris
- Mã `L6.7` nghĩa cũ (ngờ vật liệu) và toàn bộ luật chữ "chính hãng" theo hãng vật liệu — không áp dụng.
- Luật `L2.5` theo "7 tỉnh/thành có cơ sở" → THV **chỉ có một cơ sở** ở Hà Nội.
- Nhóm khách `N1–N6` của nha khoa → thay bằng 6 nhóm của ngành tiêu hóa.
- Cross-sell theo dịch vụ nha khoa → thay bằng vòng tái soi theo chỉ định bác sĩ.
- Nội dung nha khoa trong trang hướng dẫn — bản THV viết lại trang từ đầu, giữ nguyên cơ chế bơm nội dung bằng `cap-nhat-trang-huong-dan.py`.

---

## 🔶 Việc còn treo — cần THV cấp dữ liệu

Xếp theo mức chặn công việc, nặng nhất lên đầu.

### 🔴 Chặn việc dùng thật

| # | Việc | Chặn gì | Ở đâu |
|---|---|---|---|
| 1 | **Quy trình nội bộ khi gặp ca cờ đỏ**: chuyển cho ai, kênh nào, trong bao lâu | Hệ nhận diện được ca cờ đỏ nhưng **chưa có chỗ để chuyển**. Đây là slot trống quan trọng nhất của cả repo | `P8` §9 |
| 2 | **Bản hướng dẫn chuẩn bị trước nội soi** chính thức (giờ nhịn ăn, thuốc làm sạch đại tràng, dặn người đưa về) | Trực page không được tự nêu số giờ. Và đây là khâu chặn **mốc rò nặng nhất** của phễu | `P4` §7 · `P7` §5 |
| 3 | **Tiêu chí sàng lọc trước tiền mê**: bệnh nền nào cần hội chẩn, xét nghiệm nào bắt buộc | Nguyên nhân chính của việc khách đến rồi phải về | `P4` §7 |
| 4 | **Bảng giá nội bộ** xác nhận lại — hiện đang dùng giá từ web công khai ngày 28/10/2026 | Mọi con số giá đều phải gắn `⚠` | `P7` §0 · §1 |

### 🟠 Chặn một phần báo cáo

| # | Việc | Chặn gì | Ở đâu |
|---|---|---|---|
| 5 | **Bảng lý do hoãn tại chỗ** — nhờ lễ tân ghi một dòng mỗi ca đến khám mà không soi được | Sheet đáng tiền nhất của `R4` | `R4` sheet 4 |
| 6 | **Cột "ngày hẹn soi lại"** trong hồ sơ, ở dạng đọc được bằng máy | Sheet Vòng tái soi của `R6` — tệp giá trị dài hạn lớn nhất | `R6` sheet 4 |
| 7 | **Ba câu hỏi về giá**: có bảo hiểm không · tổng tiền nếu cắt polyp · phí bác sĩ gây mê đã gồm chưa | Ba câu khách hỏi nhiều nhất mà trực page chưa trả lời được | `P7` §1 |
| 8 | **Mốc KPI**: tỷ lệ xin số · show-up · **soi được / đến khám** · tệp tái soi được nhắc | Báo cáo chỉ nêu số thật + `⚠ chưa có mốc so sánh` | `P8` §7 |
| 9 | **Mô tả quy trình xử lý dây soi** | Không trả lời được rào cản `L6.9` bằng bằng chứng | `P5` §4 |

### 🟡 Hoàn thiện dần

| # | Việc | Ở đâu |
|---|---|---|
| 10 | Thông tin **BS.CKI Nguyễn Thị Thảo**: chuyên khoa, kinh nghiệm, nơi công tác trước | `P1` §4 |
| 11 | Xác minh **mốc thời gian** của ba số công bố (10.000+ ca nội soi · 15.000+ người bệnh · 4.9/5) | `P1` §5 |
| 12 | **Danh mục can thiệp nội soi** đầy đủ và điều kiện thực hiện tại phòng khám | `P4` §1 · §7 |
| 13 | **Danh mục xét nghiệm · siêu âm** và giá | `P4` §7 |
| 14 | Phòng khám có nhận **nội soi cho trẻ em** không | `P4` §7 |
| 15 | **Phân tầng nhân sự CSKH** để định tuyến `HOT·G1` và ca cờ đỏ | `P8` §9 |
| 16 | **Danh sách URL website** (sitemap) để chạy `W1` cột "web đã có bài chưa" và `W2` | `W1` · `W2` |

---

## 🔷 Việc còn treo — thuộc repo, không cần THV

| # | Việc | Ghi chú |
|---|---|---|
| A | ~~Trang hướng dẫn cho người dùng cuối~~ | ✅ **Xong 28/10/2026** — [https://claude.ai/artifact/H9LDZsYucRSeGvqnX2ubkg](https://claude.ai/artifact/H9LDZsYucRSeGvqnX2ubkg). Nguồn ở `tools/huong-dan.html`, bơm lại bằng `tools/cap-nhat-trang-huong-dan.py`. Đã mở Share "ai có link cũng xem". **v1.1 (28/10): dựng lại style + layout** theo hệ Be Vietnam Pro, thanh header tối, step số tròn, file-card có badge, prompt-card có header + footer, bảng header tối |
| B | **Tách khối cờ đỏ thành sheet riêng** trong `xuat_bao_cao.py` cho R1/R2/R4 | Hiện khối đó nằm ở **đầu sheet thứ nhất** thay vì sheet riêng. R3 đã đúng khuôn. Nội dung không thiếu, chỉ khác cấu trúc sheet — xem `tools/README.md` |
| C | **Script cho `R6` và nhóm `W`** | Hiện trợ lý tự viết, dùng lại `excel_style.py`. Chạy nhiều lần thì nên có script |
| D | **Bộ `template/` file Excel mẫu** | Chưa có. Paris có 2 file mẫu để đối chiếu định dạng — bản THV sẽ lấy từ lần chạy thật đầu tiên |
| E | **Cải thiện nhận diện `L6.8`** trong `tu-dien-tieu-hoa.json` | Từ khoá chỉ bắt được tín hiệu bề mặt. Sau vài kỳ dữ liệu thật thì bổ sung được cách khách thật hay nói |
| F | **Kiểm lại nhận xét ở `P9` §1** về cụm nội dung nào đang mỏng | Hiện dựa trên **một lần quan sát bề mặt website**, chưa phải số đo. `W2` phải đo lại bằng danh sách URL thật |

---

## Lịch sử trang hướng dẫn

| Bản | Ngày | Thay đổi |
|---|---|---|
| v1.0 | 28/10/2026 | Dựng trang: khối cờ đỏ, 5 nhóm người dùng, 4 khối copy, 22 prompt |
| v1.1 | 28/10/2026 | Dựng lại style + layout theo hệ Be Vietnam Pro: thanh header tối, step số tròn, file-card có badge, prompt-card có header + footer, bảng header tối. Prompt tăng lên 30 |
| v1.2 | 28/10/2026 | Đồng bộ tone: khối cờ đỏ dùng chung nền tối với header, đỏ rút về vai trò tín hiệu |
| v1.3 | 28/10/2026 | Sửa tương phản chữ trong khối tối (`ol.numbered>li` đè mất màu chữ sáng) · lưới 6 ô cờ đỏ chia hết 1/2/3 cột · vạch vàng chuyển về thanh header |
| v1.4 | 28/10/2026 | Điểm nhấn trong khối tối đổi từ đỏ sang vàng |
| v1.5 | 28/10/2026 | Thêm link repo GitHub vào nav, hero, mục cài đặt và footer |

---

## Ghi chú về cách dựng bản này

**Phần viết mới hoàn toàn:** `SYSTEM-PROMPT` (cả hai bản) · `knowledge/P1–P9` · `reports/R1–R6` · `reports/W1–W3` · `doc/01–05` · `doc/mau-du-lieu/*` · `tools/tu-dien-tieu-hoa.json` · `tools/phan_loai.py` · `tools/huong-dan.html` · `README.md`.

**Phần port từ Paris rồi sửa:** `tools/excel_style.py` (bảng màu, bảng chú giải, tên cột) · `tools/xuat_bao_cao.py` (~1.950 dòng: đổi toàn bộ taxonomy, viết lại các khối văn bản, thêm khối cờ đỏ và cột `% HOT trừ cờ đỏ`) · `tools/cap-nhat-trang-huong-dan.py` (gộp cả `R*` và `W*` vào một file, thêm báo động khi bản ngắn vượt giới hạn ChatGPT).

**Đã chạy thử:** `phan_loai.py` và `xuat_bao_cao.py --bao-cao tat-ca` trên 12 hội thoại mô phỏng → sinh ra 5 file Excel, khối cờ đỏ bắt đúng 3 ca và phát hiện đúng 1 ca bị trấn an sai. Không còn tham chiếu nào tới ngành nha trong `tools/`. `cap-nhat-trang-huong-dan.py` bơm 4 khối vào trang hướng dẫn: bộ não **19.068** ký tự · bản ngắn **7.610** (dư 390 so với giới hạn 8.000 của ChatGPT) · tri thức 9 module 98 KB · khuôn báo cáo 9 khuôn 159 KB → trang 284 KB.

**Nguồn dữ liệu thương hiệu:** `tieuhoaviet.com.vn` (trang chủ · `/ve-chung-toi/` · `/doi-ngu-bac-si/` · `/dich-vu/` · `/benh-tieu-hoa/` · trang bảng giá), lấy ngày **2026-10-28**. Mọi con số và tên riêng lấy từ nguồn công khai này đều được gắn `⚠` trong module tương ứng.
