# template/ — file Excel mẫu để đối chiếu định dạng

> **Hai file trong này sinh từ 12 hội thoại MÔ PHỎNG** ở [`doc/mau-du-lieu/MAU_Hoi-thoai.md`](../doc/mau-du-lieu/MAU_Hoi-thoai.md).
> **Không phải người bệnh thật của Tiêu Hóa Việt.** Mở ra xem được ngay, không cần chạy gì.

| File | Khuôn | Số sheet | Xem được gì |
|---|---|---|---|
| `THV_MAU_R1_PhanLoai-KichBan.xlsx` | [`R1`](../reports/R1-phan-loai-hoi-thoai.md) file 1 | 6 | Góc nhìn **quy trình**: mỗi hội thoại một dòng đi trọn 4 bước · khung B1–B5 · nhịp chăm sóc |
| `THV_MAU_R1_BankKichBan.xlsx` | [`R1`](../reports/R1-phan-loai-hoi-thoai.md) file 2 | 6 | Góc nhìn **phân loại**: bitmask tín hiệu, L-code, nhóm giá trị · bank kịch bản theo nhóm · chăm sóc độ nóng × giá trị |
| `THV_MAU_R2_PhanTang-QuangCao.xlsx` | [`R2`](../reports/R2-phan-tang-quang-cao.md) | 14 | Phân tầng post · Post × Nhóm giá trị · **4 bảng nhiệt** · dữ liệu thô |
| `THV_MAU_R3_ChatLuongTuVan.xlsx` | [`R3`](../reports/R3-chat-luong-tu-van.md) | 8 | Bảng chấm 10 tiêu chí · tiêu chí nào hổng · kế hoạch đào tạo · rủi ro pháp lý |
| `THV_MAU_R4_BaoCaoDieuHanh.xlsx` | [`R4`](../reports/R4-bao-cao-dieu-hanh.md) | 11 | Một trang cho lãnh đạo · **hoãn tại chỗ** · phễu ba con số cuối · tệp giá trị dài hạn |
| `Kangnam_KichBan_CatMi.xlsx` | — | 5 | **File của thương hiệu khác trong tập đoàn** (kịch bản cắt mí, Kangnam). Giữ để đối chiếu định dạng giữa các bản. Bản gốc ở `Paris-Agent-Factory/template/` |

> **Sheet đầu tiên của cả 5 file THV là `Cờ đỏ`** — kể cả khi kỳ đó không có ca nào. Mở file ra mà sheet đầu không phải `Cờ đỏ` thì file đó chạy sai khuôn.

## Dùng để làm gì

**Đối chiếu định dạng.** Trợ lý sinh file Excel theo khuôn `reports/R1–R6`; hai file này cho thấy khuôn đó ra trông như thế nào — màu quy ước, sheet chú giải, chỗ nào để `⚠` chờ người điền.

**Thấy trước chỗ script không tự làm được.** Mọi ô nền vàng có dấu `⚠` là chỗ cần người hoặc trợ lý đọc hiểu rồi điền: ba kết luận mở đầu, nhận định từng bảng, bảng chấm 10 tiêu chí của `R3`.

## Sinh lại

```bash
cd tools
python phan_loai.py --src ../doc/mau-du-lieu/MAU_Hoi-thoai.md --out rows.json
python xuat_bao_cao.py --bao-cao R1 --rows rows.json --ky "T10-2026-MAU" --dich-vu "MAU" --out ../output
```

⚠️ **Đừng chép file báo cáo chạy từ dữ liệu thật vào đây.** Thư mục này được `.gitignore` cho phép commit `.xlsx` (ngoại lệ duy nhất ngoài `doc/mau-du-lieu/`), nên file thật bỏ vào đây sẽ bị đẩy lên GitHub — mà repo đang để **public**. File chạy thật để nguyên trong `output/`, thư mục đó đã bị chặn commit.
