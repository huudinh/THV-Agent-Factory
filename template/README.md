# template/ — file Excel mẫu để đối chiếu định dạng

> **Hai file trong này sinh từ 12 hội thoại MÔ PHỎNG** ở [`doc/mau-du-lieu/MAU_Hoi-thoai.md`](../doc/mau-du-lieu/MAU_Hoi-thoai.md).
> **Không phải người bệnh thật của Tiêu Hóa Việt.** Mở ra xem được ngay, không cần chạy gì.

| File | Khuôn | Xem được gì |
|---|---|---|
| `THV_MAU_R1_PhanLoai-KichBan.xlsx` | [`R1`](../reports/R1-phan-loai-hoi-thoai.md) file 1 | Góc nhìn **quy trình**: mỗi hội thoại một dòng đi trọn 4 bước, có cột nội dung gợi ý gửi ngay · khung B1–B5 · nhịp chăm sóc |
| `THV_MAU_R1_BankKichBan.xlsx` | [`R1`](../reports/R1-phan-loai-hoi-thoai.md) file 2 | Góc nhìn **phân loại**: từng hội thoại kèm bitmask tín hiệu, L-code, nhóm giá trị · bank kịch bản theo nhóm · bảng chăm sóc độ nóng × giá trị |

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
