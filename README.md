# 🩺 THV AGENT FACTORY — Trợ lý đọc số liệu Fanpage & nội dung web, trả về báo cáo

> Version 1.0 · **Bạn đưa file hội thoại, danh sách post hoặc danh sách URL. Nó trả về báo cáo.**
>
> **Không cần biết lập trình. Không cần tạo AI-Agent. Không cài gì lên máy.**

Dành cho **Phòng khám Đa khoa Tiêu Hóa Việt** — `tieuhoaviet.com.vn` · 139 Đại La, Tương Mai, Hà Nội.

---

## 📘 Hướng dẫn sử dụng

> ### → **[Mở trang hướng dẫn](https://claude.ai/artifact/H9LDZsYucRSeGvqnX2ubkg)**
>
> **Trang tự đủ để cài — không tải repo cũng được.** Phần cài đặt nhúng sẵn **toàn bộ bộ não** (bản đầy đủ 19.068 ký tự và bản ngắn 7.610 cho ChatGPT), mỗi cái một nút Copy; cộng **hai file gộp dự phòng** (tri thức 98 KB · khuôn báo cáo 159 KB) thay cho 18 file rời khi máy không tải được file.
>
> Mở đầu là **khối cờ đỏ đọc trước khi cài**, rồi **phần giới thiệu riêng cho từng nhóm người dùng** — nhóm đó hỏi trợ lý việc gì, và trợ lý **không** làm gì cho họ. Sau đó là **22 prompt** bấm copy là dán được:
>
> | Nhóm | Có gì ở đó |
> |---|---|
> | **① Trực page** | Gợi câu nhắn tiếp · tra mã trạng thái · phân biệt `L6.4` với `L6.8` · chạm lại tệp nguội |
> | **② Ads** | Phân tầng post · chống bẫy `%HOT` lẫn cờ đỏ · kiểm giả thuyết post hù bệnh |
> | **③ Trưởng nhóm** | Chấm 10 tiêu chí · kế hoạch đào tạo 4 tuần · bắt lỗi trượt câu hỏi ngầm |
> | **④ Quản lý phòng khám** | Phễu ba con số cuối · vì sao khách đến mà không soi được · tệp đến hẹn soi lại |
> | **⑤ Nội dung & SEO** | Kho câu hỏi thật · câu **không được** trả lời trên web · lịch 8 tuần |
>
> Kèm **năm ô cần điền theo đúng thứ tự trên form** (có 5 biến thể ô Mô tả cho từng bộ phận) · **cài trên 3 nền tảng** · **bảng kiểm 4 câu** bắt ba lỗi cài đặt hay gặp · **10 câu chạy thử** · **bảng tra sự cố** · mục **ba thứ chỉ ngành tiêu hóa mới có**.

**Người mới bắt đầu từ trang đó, không phải từ đây.** Repo này là phần file để cài vào Project/GPT/Gem — trang hướng dẫn nói *khi nào dùng cái gì*.

**Tải file:** nút **Code** → **Download ZIP**, hoặc mở từng file → **Raw** → lưu lại. Mỗi tháng lấy bản [`P7`](knowledge/P7-chien-dich-thang.md) mới tại đây.

> Trang đang ở chế độ **ai có link cũng xem được** — phát link cho cả nhóm là dùng được ngay.

Kiến trúc kế thừa [`Paris-Agent-Factory`](../Paris-Agent-Factory/) v1.0 (bản thân nó kế thừa `Kangnam-Agent-Factory` v2.3). Cùng công thức **lõi brand-neutral + module thương hiệu**, nên đổi brand = đổi module `P`, không sửa lõi. Nhưng bản tiêu hóa **không dùng được khuôn nha khoa nguyên xi** — ba lý do ở mục ⭐ bên dưới.

---

## Dùng trong 3 bước

```
① Xuất file hội thoại từ Fanpage / CRM     →  doc/02-chuan-bi-du-lieu.md
② Dán vào trợ lý, nói một câu              →  doc/03-cau-lenh-mau.md
③ Xác nhận con số khi nó dừng lại           →  nhận báo cáo
```

**Chưa cài?** Bắt đầu từ [`doc/01-cai-dat.md`](doc/01-cai-dat.md) — mất 15 phút, làm một lần.

**Không biết bắt đầu từ đâu?** Dán file vào rồi gõ: *"Đây là file hội thoại tháng 10. Xem giúp mình dùng được những gì."*

**Câu nên hỏi trước mọi báo cáo nào:** *"Trong file này có ca nào có dấu hiệu cần khám sớm không? Có ca nào bị nhân viên trấn an sai không?"*

---

## Chín báo cáo — hai nhóm

### Nhóm R — đọc dữ liệu Fanpage

| Mã | Báo cáo | Trả lời câu hỏi | Cần có |
|---|---|---|---|
| **[R1](reports/R1-phan-loai-hoi-thoai.md)** | Phân loại & kịch bản hội thoại | Khách là ai, đang vướng gì, **nhắn lại thế nào** | File hội thoại |
| **[R2](reports/R2-phan-tang-quang-cao.md)** | Phân tầng post quảng cáo + biểu đồ nhiệt | Post nào kéo khách **cần soi thật**, post nào chỉ kéo người hỏi giá | Danh sách post **+** hội thoại cùng kỳ |
| **[R3](reports/R3-chat-luong-tu-van.md)** | Chất lượng tư vấn & đào tạo | Nhân viên hổng khâu nào, **có bỏ sót cờ đỏ không**, tuần tới dạy gì | Hội thoại có dấu thời gian |
| **[R4](reports/R4-bao-cao-dieu-hanh.md)** | Báo cáo điều hành theo dịch vụ | **Phễu rò ở đâu**, nhóm nào đang mất tiền | Hội thoại (+ số đến khám, số soi được nếu có) |
| **[R5](reports/R5-so-sanh-hai-ky.md)** | So sánh hai kỳ | Có tốt lên không, **nhờ cái gì** | Dữ liệu 2 kỳ đã chạy R1 |
| **[R6](reports/R6-chan-dung-khach-hang.md)** | Chân dung khách hàng | Người đang đến THV **là ai** | **Bảng danh sách khách** |

### Nhóm W — nội dung website

| Mã | Báo cáo | Trả lời câu hỏi | Cần có |
|---|---|---|---|
| **[W1](reports/W1-kho-cau-hoi-noi-dung.md)** | Kho câu hỏi thật → đề bài nội dung | Khách hỏi gì nhiều nhất mà **web chưa trả lời** | File hội thoại (+ danh sách URL) |
| **[W2](reports/W2-ra-soat-noi-dung.md)** | Rà soát nội dung đang có | Bài nào **thiếu khối cờ đỏ**, thiếu byline, sai luật y tế | Danh sách URL + nội dung bài |
| **[W3](reports/W3-ban-do-cum-noi-dung.md)** | Bản đồ cụm & lịch xuất bản | Viết cụm nào trước, cho nhóm khách nào | Kết quả W1 (+ W2) |

**Chạy theo thứ tự R1 → R2 → R3 → R4.** R4 dùng lại kết quả ba cái trước.
**R6 chạy độc lập** (đọc bảng danh sách khách, không phải hội thoại).
**W1 → W3 chạy sau R1**, dùng cùng file hội thoại.

> **Nhóm W không viết bài.** Nó lấy đề bài và bằng chứng từ dữ liệu inbox thật, rồi chuyển sang các skill SEO đã có (`seo-brief-engine` → `seo-article-writer` → `seo-qa-fixer` → `geo-scorecard`). Xem [`P9`](knowledge/P9-noi-dung-web.md) §5.

---

## Năm việc trợ lý KHÔNG làm

Đây là **giới hạn cố ý**, không phải thiếu sót.

| Không làm | Vì sao |
|---|---|
| **Chẩn đoán, loại trừ bệnh, đọc kết quả nội soi / xét nghiệm / giải phẫu bệnh** | Ngoài phạm vi chuyên môn. Kết luận chỉ có sau nội soi, với tổn thương thì sau giải phẫu bệnh |
| **Tư vấn thuốc, liều, phác đồ** — kể cả phác đồ diệt HP | Kê đơn là việc của bác sĩ |
| **Tạo AI-Agent, viết system prompt** | Người dùng không cần việc đó. Nó chỉ đọc số liệu ra báo cáo |
| **Chat với khách, tự gửi tin** | Mọi nội dung nó viết là **bản gợi ý để người duyệt rồi dán lại** |
| **Thao tác trên CRM, website, phần mềm** | Nó chỉ đọc file bạn đưa |

---

## ⭐ Ba thứ khiến bản tiêu hóa khác bản nha khoa

Không phải đổi tên thương hiệu là xong. Ba điểm dưới đây là lý do bản THV không dùng được khuôn Paris nguyên xi.

### ① 🚩 Cột CỜ ĐỎ — cột an toàn, không phải cột bán hàng

Hệ nha khoa có hai trục (`L-code`, độ nóng) cộng một trục giá trị. Hệ tiêu hóa **bắt buộc có thêm một cột cờ**: `CĐ-1`…`CĐ-6`.

| Mã | Dấu hiệu |
|---|---|
| **CĐ-1** | Nôn ra máu · đi ngoài **phân đen** · phân như bã cà phê |
| **CĐ-2** | Sụt cân nhanh không rõ lý do |
| **CĐ-3** | Khó nuốt tăng dần · nuốt đau |
| **CĐ-4** | Thiếu máu không rõ nguyên nhân |
| **CĐ-5** | Đau bụng dữ dội liên tục · khối ở bụng · vàng da |
| **CĐ-6** | Tiền sử gia đình ung thư dạ dày – đại tràng trực hệ |

> **Ở nha khoa, phân loại sai một lead là mất tiền. Ở đây, bỏ sót một ca cờ đỏ là rủi ro cho người bệnh** — và đó là rủi ro không có con số nào bù lại được.
>
> Vì vậy: ca có cờ đỏ → **HOT bất kể điểm**, gọi ngay bất kể khung giờ, chuyển bác sĩ trong ngày. ⛔ Không để lẫn trong hàng đợi nuôi dưỡng, ⛔ không gửi nội dung ưu đãi, ⛔ **không trấn an**.
>
> **Mốc 100% nhận diện cờ đỏ là mốc duy nhất trong cả repo không thương lượng.** Mọi mốc KPI khác đều ghi `⚠ chờ THV chốt`, vì chúng là chuyện kinh doanh.

**Phân biệt bắt buộc, và đây là chỗ dễ sai nhất:** đi ngoài **máu đỏ tươi** kèm rát → `TH-06` (trĩ/hậu môn), **không phải** cờ đỏ. **Phân đen** → `CĐ-1`, **là** cờ đỏ.

Cột cờ đỏ cũng tạo ra một bẫy đọc số riêng: luật ghi đè đẩy **mọi** ca cờ đỏ lên HOT, nên `% HOT` của một post có lẫn cờ đỏ **không nói gì về chất lượng quảng cáo**. Mọi bảng so sánh post phải dùng cột **`% HOT (trừ cờ đỏ)`**.

### ② Rào cản thứ tư: NÉ

Hệ nha khoa có **ba** rào cản: `SỢ` · `NGỜ` · `NGẠI`. Ngành tiêu hóa **bắt buộc có thêm `NÉ`**, vì đây là ngành mà **kết quả có thể là tin xấu**.

| Rào cản | Khách sợ cái gì | Mã |
|---|---|---|
| **SỢ** | Cái ống soi · thuốc tiền mê | `L6.5` · **`L6.7`** |
| **NGỜ** | Chất lượng người soi · **vệ sinh dây soi** | `L6.2` · **`L6.9`** |
| **NGẠI** | Thời gian, tiền, đường xa | `L6.3` · `L6.4` · `L2.5` |
| **NÉ** ⭐ | **Chính cái kết quả** — biết nên soi nhưng trì hoãn vì sợ phát hiện ra bệnh | **`L6.8`** |

> Khách `L6.8` **dùng đúng lý do của nhóm bận và nhóm thiếu tiền để từ chối**, nên nếu gộp họ vào `NGẠI` thì:
> - Nhịp chăm sai: gửi ưu đãi giảm giá cho người đang sợ kết quả là **đẩy họ xa thêm**.
> - Mất luôn khả năng đo: đây là nhóm **đông nhất trong tệp nguội** của ngành, và là nhóm **gọi lại được** nếu nói đúng điều họ cần nghe.
>
> **Dấu hiệu nhận ra sau lớp lý do:** đã hỏi rất kỹ về bệnh rồi mới lùi · lùi **không kèm câu hỏi mới nào** · hẹn một mốc xa và mơ hồ ("qua Tết") · hỏi *"soi ra bệnh thì sao"* trước khi hỏi giá.
>
> Nhóm này nuôi tới **180 ngày** bằng nội dung giáo dục, nhịp `D+7 / D+21 / D+45`.

### ③ Phễu có HAI mốc rò và MỘT vòng tái soi

```
inbox → có SĐT → kết nối → đặt lịch
      → ĐẾN KHÁM                      ← mốc rò 1
      → THỰC HIỆN ĐƯỢC NỘI SOI        ← mốc rò 2, chỉ ngành nội soi mới có
      → kết quả → điều trị · HẸN SOI LẠI THEO CHU KỲ   ← vòng LTV
```

**Mốc rò 2 là chỗ mất tiền nhiều nhất của phòng khám:** khách đã đến tận nơi, đã tốn **toàn bộ** chi phí quảng cáo và một buổi của hai bên — mà doanh thu bằng không. Lý do thường là: nhịn ăn chưa đủ giờ · ruột chưa sạch · không đủ điều kiện tiền mê · không có người đưa về · đến rồi vẫn không dám soi.

> **Phần lớn những lý do đó là lỗi dặn dò, sửa được bằng một tin nhắn mẫu.** Nhưng không ai sửa nếu không có con số — nên [`R4`](reports/R4-bao-cao-dieu-hanh.md) có một sheet riêng là **bảng lý do hoãn tại chỗ**, và `P8` §5 thêm hai mốc chăm sóc `T+48h` (gửi hướng dẫn chuẩn bị) và `T–1 ngày` (nhắc lại).

**Vòng tái soi là cơ chế LTV mà ngành nha không có.** Ở nha khoa, LTV phải tạo ra bằng cross-sell. Ở đây, **mốc quay lại đã nằm sẵn trong phiếu kết quả của chính khách** — bác sĩ đã hẹn, khách đã biết. Tệp này không cần thuyết phục, chỉ cần nhắc đúng lúc, mà nó không xuất hiện trong bất kỳ báo cáo lead mới nào.

⚠️ Giới hạn: chu kỳ tái soi là **chỉ định y khoa cho từng ca**. Báo cáo chỉ được nói *"theo mốc bác sĩ đã hẹn trong phiếu kết quả"*, **không tự điền số năm**.

---

## Bốn luật ghi đè khi chấm độ nóng

Thang 5 tín hiệu chấm thấp oan cho bốn nhóm quan trọng nhất của ngành:

| Luật | Vì sao |
|---|---|
| Đã **đặt lịch** / đang đến → **HOT** | Hiển nhiên |
| 🚩 **Có cờ đỏ** → **HOT**, và gắn cờ ưu tiên y tế | **Luật an toàn.** Nó tồn tại để ca này được gọi trước mọi ca khác, không phải để nói ca này dễ chốt |
| **Đã có kết quả nơi khác**, hoặc đã được chỉ định soi (`TH-11`) → **HOT** | Khách đã qua giai đoạn *"có cần soi hay không"*, **chỉ còn chọn nơi làm**. Lead nóng nhất của ngành, mà tin nhắn của họ rất ngắn nên bị chấm thấp oan |
| **Đến hẹn soi lại** (`TH-02`) → tối thiểu **WARM** | Nhóm này viết tin ngắn, không có triệu chứng cấp, nhưng gần như chắc chắn soi |

---

## Cấu trúc repo

```
SYSTEM-PROMPT.md          ← bộ não, dán vào ô chỉ dẫn (19.068 ký tự)
SYSTEM-PROMPT-NGAN.md     ← bản 7.610 ký tự, CHỈ cho ChatGPT
knowledge/P1–P9           ← module thương hiệu, upload lên Knowledge
reports/R1–R6 · W1–W3     ← khuôn báo cáo, upload lên Knowledge
doc/                      ← tài liệu cho người đọc, KHÔNG upload
tools/                    ← quét cờ đỏ + đối chiếu con số + XUẤT EXCEL + trang hướng dẫn
```

### Module tri thức — upload cả 9 file

| File | Nội dung | Trạng thái |
|---|---|---|
| [P1-thuong-hieu](knowledge/P1-thuong-hieu.md) | Định vị · **4 trụ bằng chứng** · 3 tuyên bố có rủi ro pháp lý · bác sĩ được nêu tên · **chỉ 1 cơ sở, mở cả Chủ nhật** | ⚠ BS.CKI Nguyễn Thị Thảo chưa có thông tin |
| [P2-khach-hang](knowledge/P2-khach-hang.md) | **4 rào cản SỢ · NGỜ · NGẠI · NÉ** · 6 nhóm khách · bảng câu hỏi ngầm | ✅ |
| [P3-hanh-vi-trang-thai](knowledge/P3-hanh-vi-trang-thai.md) | Giai đoạn S1–S3·CS · **phễu 2 mốc rò + vòng tái soi** · CTA và cái bẫy của nó | ✅ |
| [P4-dich-vu](knowledge/P4-dich-vu.md) | **12 nhóm `TH-01…TH-12`** · 🚩 **cột cờ đỏ `CĐ-1…CĐ-6`** · **nhóm giá trị G1/G2/G3** | ⚠ danh mục can thiệp & phụ phí chờ cấp |
| [P5-kich-ban](knowledge/P5-kich-ban.md) | **9 lỗi cấm** · 8 quy tắc vàng · **khung B1–B5 (5 thông tin)** · 9 lý do từ chối · từ cấm | ⚠ hướng dẫn chuẩn bị chờ cấp |
| [P6-van-hanh](knowledge/P6-van-hanh.md) | **Xương sống** — L1–L6 (có **`L6.7` · `L6.8` · `L6.9`**) · 3 trục + 1 cờ · phiếu **14 trường** | ✅ |
| [P7-chien-dich-thang](knowledge/P7-chien-dich-thang.md) | **HOT-SWAP, thay mỗi tháng** — bảng giá & mọi con số | ⚠ **giá lấy từ web công khai, chưa phải bảng giá nội bộ** |
| [P8-chuan-cham-ban-giao](knowledge/P8-chuan-cham-ban-giao.md) | **Thước đo** — 5 tín hiệu · **4 luật ghi đè** · luật `% HOT*` · SLA · rubric 10 tiêu chí · KPI · 5 rủi ro đọc số | ⚠ phần lớn mốc KPI chờ THV chốt |
| [P9-noi-dung-web](knowledge/P9-noi-dung-web.md) | Cấu trúc web · giọng web · **luật pháp lý nội dung y tế** · 8 cụm nội dung | ⚠ quan sát web một lần, W2 phải đo lại |

> **Quy ước:** mã `P1–P9`, `R1–R6`, `W1–W3`, `TH-01…TH-12`, `CĐ-1…CĐ-6`, `G1/G2/G3`, `L6.7/L6.8/L6.9` là **từ vựng vận hành**, được tham chiếu khắp các file — **không đổi tên**.

### Code xuất Excel — có sẵn

| File | Việc |
|---|---|
| [tools/phan_loai.py](tools/phan_loai.py) | File hội thoại → **quét cờ đỏ** → phân loại → `rows.json` + bảng đếm |
| [tools/xuat_bao_cao.py](tools/xuat_bao_cao.py) | `rows.json` → **file Excel theo đúng khuôn R1–R5** |
| [tools/excel_style.py](tools/excel_style.py) | Style dùng chung. Sửa ở đây thì đổi cả hệ |
| [tools/tu-dien-tieu-hoa.json](tools/tu-dien-tieu-hoa.json) | Từ điển từ khoá — người làm nội dung sửa được, không cần biết code |
| [tools/huong-dan.html](tools/huong-dan.html) | **Bản nguồn của [trang hướng dẫn](https://claude.ai/artifact/H9LDZsYucRSeGvqnX2ubkg).** Sửa ở đây rồi publish đè lên cùng URL |
| [tools/cap-nhat-trang-huong-dan.py](tools/cap-nhat-trang-huong-dan.py) | Bơm lại bộ não + tri thức + khuôn báo cáo vào `huong-dan.html`. **Chạy sau mỗi lần sửa repo** |

```bash
cd tools
python phan_loai.py --src <file hội thoại> --out rows.json
python xuat_bao_cao.py --bao-cao tat-ca --rows rows.json --ky "T10/2026" --out ../output
```

Chi tiết và giới hạn: [tools/README.md](tools/README.md).

### Tài liệu

| File | Nội dung |
|---|---|
| [doc/01-cai-dat.md](doc/01-cai-dat.md) | Cài lên Claude / Gemini / ChatGPT · **10 câu chạy thử** · bảo trì hàng tháng |
| [doc/02-chuan-bi-du-lieu.md](doc/02-chuan-bi-du-lieu.md) | **Xuất dữ liệu ở đâu** · luật không được lọc mẫu · **việc nhỏ đáng làm nhất** (ghi lý do hoãn tại chỗ) |
| [doc/03-cau-lenh-mau.md](doc/03-cau-lenh-mau.md) | Câu lệnh copy-dán cho 9 báo cáo · bảng hỏi nhanh · 5 việc trợ lý sẽ từ chối |
| [doc/04-output-mau.md](doc/04-output-mau.md) | Output mẫu từng mode · **6 dấu hiệu đúng · 6 dấu hiệu sai** |
| [doc/05-xu-ly-su-co.md](doc/05-xu-ly-su-co.md) | Tra theo triệu chứng · **lỗi an toàn xử lý trước mọi lỗi khác** |
| [doc/mau-du-lieu/](doc/mau-du-lieu/) | **12 hội thoại mô phỏng** có đủ các ca khó · mẫu danh sách post · mẫu bảng khách |
| [doc/CHANGELOG.md](doc/CHANGELOG.md) | Lịch sử · việc còn treo |

---

## 🔴 VIỆC PHẢI LÀM TRƯỚC KHI DÙNG THẬT

### ① Xác nhận bảng giá ở `P7`
Bảng giá hiện tại **lấy từ website công khai ngày 28/10/2026**, không phải bảng giá nội bộ do THV cấp. Dùng được để **đối chiếu xem nhân viên có báo giá lệch không**, nhưng không nên trích vào nội dung gửi khách.

**Ba câu khách hỏi nhiều nhất mà hệ hiện CHƯA trả lời được:**
- Có áp **bảo hiểm y tế / bảo hiểm tư nhân** không?
- Nếu soi phát hiện **polyp và cắt luôn** thì tổng khoảng bao nhiêu?
- Mức **"tiền mê"** đã gồm phí bác sĩ gây mê chưa?

### ② Xin bản **hướng dẫn chuẩn bị trước nội soi** chính thức
Hiện `⚠ chờ cấp` ([`P4`](knowledge/P4-dich-vu.md) §7). Không có nó thì trực page **không được tự nêu số giờ nhịn ăn** hay cách uống thuốc làm sạch đại tràng — kể cả khi tìm thấy con số đó ở nguồn khác. Và đây đúng là khâu chặn **mốc rò nặng nhất** của phễu.

### ③ Chốt quy trình nội bộ khi gặp ca cờ đỏ
**Chuyển cho ai, bằng kênh nào, trong bao lâu.** Đây là slot trống quan trọng nhất của cả repo: hệ đã nhận diện được ca cờ đỏ, nhưng chưa có chỗ để chuyển.

### ④ Bảo trì cuối mỗi tháng
1. Đổi tên bản cũ → `P7-2026-10.md`
2. Tạo `P7-chien-dich-thang.md` mới cho tháng sau
3. Upload lại lên Knowledge, **xoá bản cũ**
4. **Không đụng file nào khác**

---

## Năm rủi ro đọc số — báo cáo tự đi tìm

| Rủi ro | Hậu quả nếu bỏ qua |
|---|---|
| **Mẫu bị lọc** — file chỉ gồm hội thoại dài, hoặc chỉ hội thoại có số | Đã thiên về phía nóng. Thổi phồng mọi post, và **thổi không đều nhau**. 🚩 Và hội thoại bị lọc ra có thể chứa **ca cờ đỏ** — một dòng *"em đi ngoài phân đen"* là hội thoại ngắn nhất file và quan trọng nhất file |
| **Mẫu nhỏ** — dưới 10 hội thoại một nhóm | `⚠ chưa đủ mẫu`. Không xếp hạng, không khuyến nghị |
| **Lặp vòng** — chia nhóm theo đúng thuộc tính đang chấm điểm | Chênh lệch là **giả**. Bắt buộc có cột `% HOT*` chấm lại không kể tín hiệu ①. **Và phải tách `TH-01` ra** — luật ghi đè đẩy nhóm đó lên 100% HOT |
| **Lạm phát HOT** | HOT tràn lan, SLA vỡ. HOT mà tỷ lệ đến khám thấp là **chấm sai**, không phải khách tệ |
| **Lẫn hai mốc cuối phễu** | Phễu có **ba** con số ở cuối: đặt lịch → đến khám → **soi được**. Lẫn mốc là che đi đúng chỗ mất tiền nhiều nhất |

---

## Ranh giới

Human-in-the-loop, mọi nội dung là bản đề xuất · 🚩 **không trấn an ca có cờ đỏ** · không chẩn đoán, không loại trừ bệnh, không đọc kết quả, không tư vấn thuốc hay phác đồ · không cam kết y khoa tuyệt đối (`khỏi 100%` · `không đau` · `an toàn tuyệt đối` · `sạch HP 100%` · `chắc chắn không phải ung thư` · `tốt nhất` · `rẻ nhất` · `phát hiện 100%`) · không hứa chắc tiền mê khi chưa sàng lọc bệnh nền · nêu khung giá công khai thì được nhưng **phải kèm ba điều kiện** (ai thực hiện · có tiền mê không · phụ phí chỉ khi có chỉ định) · mọi con số lấy từ `P7` hiện hành · chỉ nêu bác sĩ trong danh sách đã duyệt · **THV chỉ có một cơ sở ở 139 Đại La, Hà Nội** — không hứa có cơ sở gần khách · không đưa SĐT / kết quả xét nghiệm / ảnh nội soi / hồ sơ bệnh án vào file báo cáo · không nêu tên đối thủ để hạ thấp và **không nói xấu tuyến công** · nội dung website chịu thêm luật ở `P9` §3 (byline bác sĩ · ngày cập nhật · câu miễn trừ · 🚩 khối "khi nào cần đi khám ngay") · báo cáo có tên nhân viên **chỉ dùng cho đào tạo và định tuyến**.

Quyết định cuối luôn thuộc người dùng.
"# THV-Agent-Factory" 
