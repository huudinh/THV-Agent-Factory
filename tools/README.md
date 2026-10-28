# tools/ — đối chiếu con số & xuất file Excel

> **Người dùng không làm IT thì bỏ qua thư mục này.** Trợ lý tự đọc, tự đếm và tự xuất Excel, không cần script nào.
>
> Thư mục này dành cho ba việc: ① 🚩 **quét cờ đỏ một lượt cho cả file** — phần này script làm tốt hơn người, vì nó không bỏ sót dòng nào · ② **đếm lại con số bằng máy** để đối chiếu với kết quả trợ lý · ③ **xuất file Excel theo đúng khuôn R1–R5** mà không phải viết `openpyxl` từ đầu.
>
> (R6 đọc bảng khách, nhóm `W1–W3` đọc URL — không phải hội thoại. Hai nhóm đó trợ lý tự viết script, dùng lại `excel_style.py`.)

## Sáu file trong này

| File | Việc |
|---|---|
| [`phan_loai.py`](phan_loai.py) | Đọc file hội thoại → **quét cờ đỏ** → phân loại → `rows.json` + bảng đếm in ra màn hình |
| [`xuat_bao_cao.py`](xuat_bao_cao.py) | Đọc `rows.json` → **xuất file Excel theo đúng khuôn R1–R5** |
| [`excel_style.py`](excel_style.py) | Style dùng chung: bảng màu · font Arial · freeze · wrap · bảng nhiệt · sheet chú giải. **Sửa quy ước màu ở đây thì đổi cả hệ** |
| [`tu-dien-tieu-hoa.json`](tu-dien-tieu-hoa.json) | Từ điển từ khoá — người làm nội dung sửa được, không cần biết code |
| [`huong-dan.html`](huong-dan.html) | **Bản nguồn của [trang hướng dẫn](https://claude.ai/artifact/H9LDZsYucRSeGvqnX2ubkg)** cho người dùng cuối. Sửa phần chữ ở đây, rồi publish **đè lên cùng URL** |
| [`cap-nhat-trang-huong-dan.py`](cap-nhat-trang-huong-dan.py) | Bơm lại bộ não + tri thức gộp + khuôn báo cáo gộp vào `huong-dan.html` |

## ⚠ Sửa repo xong thì bơm lại trang hướng dẫn

Trang hướng dẫn **nhúng sẵn** bộ não, 9 module tri thức và 9 khuôn báo cáo để người dùng bấm Copy mà không cần tải repo. Sửa repo mà quên bơm lại thì trang dạy người dùng **bản cũ**.

```bash
python tools/cap-nhat-trang-huong-dan.py tools/huong-dan.html
```

Script chỉ thay phần bên trong bốn thẻ `<pre>` (`#src-full` · `#src-short` · `#src-gop-k` · `#src-gop-r`) cộng mấy nhãn cỡ file đi kèm — phần chữ còn lại của trang sửa tay. Nó cũng **báo động nếu bản ngắn vượt giới hạn 8.000 ký tự** của ChatGPT.

Bơm xong thì publish lại bằng công cụ Artifact, **đè lên cùng URL cũ** — đừng tạo URL mới, vì link cũ đã phát cho người dùng.

## Chạy hai bước

```bash
cd tools

# Bước 1 — quét cờ đỏ + phân loại
python phan_loai.py --src ../doc/mau-du-lieu/MAU_Hoi-thoai.md --out rows.json

# Bước 2 — xuất Excel
python xuat_bao_cao.py --bao-cao tat-ca --rows rows.json --ky "01-31/10/2026" \
       --dich-vu "Nội soi dạ dày" --posts ../doc/mau-du-lieu/MAU_Danh-sach-post.md \
       --out ../output
```

Chỉ cần một báo cáo thì đổi `tat-ca` thành `R1` · `R2` · `R3` · `R4`. Riêng R5 cần hai kỳ:

```bash
python xuat_bao_cao.py --bao-cao R5 --rows ky10.json --rows-truoc ky09.json \
       --ky "T10/2026" --ky-truoc "T09/2026" --out ../output
```

Cần **Python 3.8+** và `openpyxl` (`pip install openpyxl`) cho bước 2. Bước 1 không cần thư viện ngoài.

### Tham số của `xuat_bao_cao.py`

| Tham số | Nghĩa |
|---|---|
| `--bao-cao` | `R1` · `R2` · `R3` · `R4` · `R5` · `tat-ca` (R1–R4, không gồm R5 vì R5 cần hai kỳ) |
| `--rows` | File `rows.json` từ bước 1 |
| `--ky` · `--dich-vu` | Ghi vào tiêu đề và tên file |
| `--posts` | File markdown danh sách post — **chỉ R2 cần**. Không có thì R2 chạy chế độ dự đoán |
| `--mau-loc` | Nếu mẫu **đã bị lọc** thì ghi rõ cách lọc, ví dụ `"100 HT chọn từ 520, ưu tiên HT dài"`. Script in cảnh báo đúng chỗ thay vì để người đọc tưởng mẫu là toàn bộ |
| `--ket-noi` · `--dat-lich` · `--den-kham` | Số phiếu cho R4. Không có thì phễu nửa sau ghi `⚠ chưa đo được` |
| `--rows-truoc` · `--ky-truoc` | Kỳ trước, **chỉ R5 cần** |
| `--out` | Thư mục ghi file. Mặc định `output/` |

---

## 🚩 Phần script làm tốt hơn người: quét cờ đỏ

Bước 1 in **khối cờ đỏ lên đầu, trước mọi con số khác**, gồm: số hiệu hội thoại · mã `CĐ-x` · có SĐT hay chưa · **và cảnh báo nếu nhân viên đã dùng câu trấn an trong ca đó**.

```
==================================================================
  CO DO  —  doc truoc moi con so khac
==================================================================
Ca co dau hieu co do   3 / 12
    HT#3   Trần Thị Hồng      CĐ-6     SDT:Có    L4.1
    HT#4   Phạm Văn Đức       CĐ-1     SDT:Không L2.1  <== NV TRAN AN SAI
    HT#11  Lý Thị Oanh        CĐ-2     SDT:Có    L4.1

  Trong do BI TRAN AN SAI: 1
      HT#4   Phạm Linh : không sao đâu, chắc không sao, theo dõi thêm đã
```

**Ba điều phải hiểu về khối này:**

1. **Từ điển nhận RỘNG — thà gắn thừa còn hơn bỏ sót.** Danh sách in ra là danh sách **cần người đọc lại**, không phải kết luận y khoa.
2. **Có xử lý phủ định.** `"không sụt cân"` không bị tính là dấu hiệu sụt cân. Nhưng chỉ bắt được phủ định nằm **ngay trước** từ khoá — câu vòng vo thì vẫn cần người đọc.
3. **Máu đỏ tươi không phải cờ đỏ.** Từ điển xếp *"đi ngoài ra máu"* vào `TH-06`; *"phân đen"* vào `CĐ-1`. Đây là luật phân biệt ở `P4` §2, và nó là chỗ dễ sai nhất.

---

## ⚠ Ô ghi `⚠` là cố ý, không phải lỗi

Script tính được con số, **không đọc hiểu được nội dung**. Mọi ô cần đọc hiểu đều để sẵn `⚠` kèm chữ mô tả cần điền gì, và **nền vàng** để nhìn thấy ngay.

| Script làm được | Phải người / trợ lý điền |
|---|---|
| 🚩 Quét 6 mã cờ đỏ cho cả file + phát hiện câu trấn an sai | Nhân viên **có nhận ra** cờ đỏ hay không (có hỏi thêm, có mời khám sớm) |
| Mọi con số đếm được: tổng HT, %, phân bố, phễu nửa đầu | Ba kết luận mở đầu mỗi báo cáo |
| Chấm 5 tín hiệu + 4 luật ghi đè → HOT/WARM/COLD | Bảng chấm 10 tiêu chí của R3 (chỉ ⑨ từ cấm và ③ trấn an là đã điền) |
| Cột **độ nóng trừ cờ đỏ** để so sánh post | Nhận định cho từng bảng nhiệt, từng post |
| Phát hiện từ cấm trong lời nhân viên | Lỗi "trượt câu hỏi ngầm" — cần đọc hai tin liền nhau |
| Phát hiện ca có rào cản mà NV **không đưa bằng chứng nào** của THV | Bằng chứng đó có **đúng rào cản** hay không |
| Gợi `L6.x` theo từ khoá | **Phân biệt `L6.4` với `L6.8`** — hai nhóm nói cùng một câu |
| Phễu nửa đầu (inbox → có SĐT) | Phễu nửa sau: đặt lịch · đến khám · **soi được** · lý do hoãn tại chỗ |

### Chỗ script yếu nhất: `L6.8` né kết quả

`L6.4` (bận) và `L6.8` (né kết quả) nói **cùng một câu**: *"để em sắp xếp đã"*. Từ khoá không phân biệt được. Script bắt được vài tín hiệu bề mặt (*"qua Tết"*, *"soi ra bệnh thì sao"*) nhưng sẽ bỏ sót, và nó in cảnh báo đúng chỗ đó.

Phân biệt bằng cách đọc: **sau khi lùi, khách có hỏi tiếp về lịch không.** Có → `L6.4`. Không, và trước đó đã hỏi rất kỹ về bệnh → `L6.8`. Xem `P6` §2.

Xếp sai nhóm này là gửi sai nội dung: ưu đãi giảm giá cho người đang sợ kết quả **đẩy họ xa thêm**.

---

## Một điểm script khác với khuôn báo cáo

Khuôn `R1`, `R2`, `R4` yêu cầu **khối cờ đỏ là một sheet riêng, đứng đầu file**. Script hiện đặt khối đó **ở đầu sheet thứ nhất** (Tổng quan / Một trang cho lãnh đạo) thay vì tách sheet riêng — trừ `R3`, nơi nó là sheet riêng đúng như khuôn.

Về nội dung thì không thiếu gì, nhưng nếu bạn cần đúng cấu trúc sheet như khuôn thì nói với trợ lý: *"Tách khối cờ đỏ thành sheet riêng đặt trước sheet Tổng quan."*

---

## Sửa từ điển — không cần biết code

Mở [`tu-dien-tieu-hoa.json`](tu-dien-tieu-hoa.json), thêm/bớt từ khoá trong danh sách. Không sửa cấu trúc, không sửa tên khoá.

| Khối trong file | Sửa khi nào |
|---|---|
| `co_do` | Bổ sung cách khách thường gõ về dấu hiệu cờ đỏ. **Thêm thì được, bớt thì cân nhắc rất kỹ** |
| `van_de` | Thêm từ khoá cho `TH-xx`. **Thứ tự trong danh sách là thứ tự ưu tiên** — khớp nhóm đầu tiên thì lấy |
| `rao_can` | Thêm cách khách nói về từng rào cản |
| `tu_cam` · `tran_an_sai` | Bổ sung câu vi phạm mới phát hiện trong hội thoại thật |
| `bang_chung_thv` | Cập nhật khi THV có bằng chứng mới (bác sĩ mới, thiết bị mới) |
| `khu_vuc_gan` | Danh sách địa danh tính là "gần 139 Đại La" |
| `gia_tri` | Map `TH-xx` → `G1/G2/G3` và từ khoá dịch vụ |

Sửa xong chạy lại bước 1 là xong — không phải sửa code.

---

## Dùng để làm gì

**Đối chiếu ở hai điểm dừng.** Trợ lý báo "tách được 120 hội thoại, 48 HOT" — chạy script, nếu nó ra 120/44 thì hỏi lại trợ lý 4 ca chênh là ca nào. Lệch thì **tin bản đọc tay**, vì script chỉ khớp từ khoá.

**Quét cờ đỏ trước khi làm bất cứ việc gì.** Đây là lý do chính để chạy script, kể cả khi bạn không cần file Excel. Mất 2 giây, và nó không bỏ sót dòng nào.

**Có khung Excel sẵn.** Trợ lý đọc `xuat_bao_cao.py` rồi dùng lại các hàm — mỗi lần chạy ra cùng một định dạng, không phải dựng lại từ đầu.
