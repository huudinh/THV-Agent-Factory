# -*- coding: utf-8 -*-
"""Xuat file Excel theo dung khuon reports/R1-R5.

Day la BAN THAM CHIEU. Hai cach dung:

  1. Nguoi dung chay truc tiep -> ra file Excel co san cau truc, dinh dang,
     sheet chu giai, va phan du lieu nao dem duoc tu rows.json thi da dien.
     O nao script khong tinh duoc thi ghi ⚠ de tro ly / nguoi dien vao.

  2. Tro ly doc file nay roi dung lai cac ham -> moi lan chay ra cung mot
     dinh dang, khong phai tu viet openpyxl lai tu dau.

Cach dung:
    python phan_loai.py --src hoi-thoai.md --out rows.json
    python xuat_bao_cao.py --bao-cao R1 --rows rows.json --ky "01-31/10/2026" \
                           --dich-vu "Nội soi dạ dày" --out ../output
    python xuat_bao_cao.py --bao-cao tat-ca --rows rows.json --ky T10/2026

    # R2 can them danh sach post (file markdown co bang, hoac bo qua)
    python xuat_bao_cao.py --bao-cao R2 --rows rows.json --posts posts.md

    # R4 co the nhan them so lieu phieu
    python xuat_bao_cao.py --bao-cao R4 --rows rows.json \
                           --ket-noi 41 --dat-lich 23 --den-kham 14

    # R5 can hai ky
    python xuat_bao_cao.py --bao-cao R5 --rows ky2.json --rows-truoc ky1.json \
                           --ky "T10/2026" --ky-truoc "T09/2026"

GIOI HAN — doc truoc khi tin file xuat ra:
  - Bang cham 10 tieu chi cua R3 can DOC HIEU, script khong cham duoc.
    R3 xuat ra la KHUNG da dien san STT/ten/NV + phan phat hien tu cam,
    cac o tieu chi de ⚠ cho nguoi hoac tro ly dien.
  - Noi dung tin nhan goi y la KHUNG theo rao can, phai ca nhan hoa lai.
  - So ket noi / dat lich / den kham / SOI DUOC khong co trong hoi thoai
    -> phai truyen vao. Khong lay "dat lich" thay "den kham", khong lay
    "den kham" thay "soi duoc".
  - CO DO: script quet bang tu khoa va nhan RONG. Danh sach co do trong file
    xuat ra la danh sach CAN NGUOI DOC LAI, khong phai ket luan y khoa.
"""
import argparse
import collections
import io
import json
import os
import re
import sys

from excel_style import (B1, B2, B3, B4, CANH_BAO, MAU_GIA_TRI, MO, TOT,
                         cot_phu_vang, doc_nhanh, dong, dong_nong,
                         dong_tieu_de, hoan_thien, khoi_canh_bao, muc, nhiet,
                         sheet, sheet_chu_giai, so_do_buoc, so_moi, tieu_de,
                         trong)

NGUONG_MAU = 10          # duoi nguong nay: ⚠ chua du mau, khong xep hang
CX = "⚠ Cần xác minh từ THV"
CD = "⚠ chưa đo được"

VAN_DE_TEN = {
    "TH-01": "🚩 CỜ ĐỎ — dấu hiệu cần khám ngay",
    "TH-02": "Theo dõi sau can thiệp · đến hẹn soi lại",
    "TH-03": "Tầm soát ung thư · không triệu chứng",
    "TH-04": "Dạ dày – thực quản",
    "TH-05": "Đại tràng – trực tràng",
    "TH-06": "Chảy máu thấp · trĩ – hậu môn",
    "TH-07": "Polyp · khối u đã biết",
    "TH-08": "Gan – mật – tụy",
    "TH-09": "Rối loạn tiêu hóa chung",
    "TH-10": "Nhiễm HP · kết quả xét nghiệm HP",
    "TH-11": "Mang kết quả nơi khác đến",
    "TH-12": "Chưa rõ / hỏi chung",
}
VAN_DE_MA = list(VAN_DE_TEN)

CO_DO_TEN = {
    "CĐ-1": "Xuất huyết tiêu hóa (nôn ra máu · phân đen)",
    "CĐ-2": "Sụt cân nhanh không rõ lý do",
    "CĐ-3": "Khó nuốt tăng dần · nuốt đau",
    "CĐ-4": "Thiếu máu không rõ nguyên nhân",
    "CĐ-5": "Đau dữ dội liên tục · khối ở bụng · vàng da",
    "CĐ-6": "Tiền sử gia đình ung thư dạ dày – đại tràng",
}

RAO_CAN_TEN = {
    "L6.1": ("?", "Chưa rõ rào cản"),
    "L6.2": ("NGỜ", "So sánh nơi khác (bệnh viện công / cơ sở tư)"),
    "L6.3": ("NGẠI", "Chưa tài chính / hỏi bảo hiểm"),
    "L6.4": ("NGẠI", "Chưa có thời gian / sợ nghỉ làm"),
    "L6.5": ("SỢ", "Sợ nội soi (nôn, sặc, đau)"),
    "L6.6": ("NGỜ+NGẠI", "Hỏi ý kiến người thân"),
    "L6.7": ("SỢ", "Ngại tiền mê / gây mê"),
    "L6.8": ("NÉ", "Né kết quả"),
    "L6.9": ("NGỜ", "Ngờ vệ sinh dây soi"),
}

# Khung noi dung theo rao can. DAY LA KHUNG, khong phai tin gui duoc ngay —
# phai thay [ ] theo tinh trang cua chinh khach do.
KHUNG_ND = {
    "CĐ": ("Dạ [tên khách], với dấu hiệu anh/chị kể thì bác sĩ cần xem sớm ạ. "
           "Em chuyển bác sĩ của phòng khám xem trường hợp của anh/chị ngay. "
           "Anh/chị đến được trong hôm nay hay sáng mai ạ? "
           "Phòng khám mở 7h-17h cả Chủ nhật.\n"
           "⛔ KHUNG CHO CA CỜ ĐỎ: không nêu giá · không trấn an · không nói "
           "khả năng mắc bệnh gì. Ghi rõ đã chuyển bác sĩ.", "X5"),
    "L6.7": ("Dạ với [bệnh nền anh/chị vừa kể] thì bác sĩ phải khám sàng lọc "
             "trước mới quyết định được có tiền mê hay không, em chưa dám hứa "
             "trước ạ. Khi làm tiền mê thì có bác sĩ gây mê theo dõi riêng "
             "trong suốt ca soi.\n"
             "Anh/chị tiện [sáng mai] hay [Chủ nhật này] để bác sĩ khám và "
             "đánh giá ạ?", "S3.2"),
    "L6.5": ("Dạ em nói thật với anh/chị: soi thường có cảm giác khó chịu, "
             "không phải không có. Còn bản tiền mê thì anh/chị ngủ trong lúc "
             "soi, có bác sĩ gây mê theo dõi riêng ạ.\n"
             "Anh/chị đến khám trước đã, bác sĩ xem rồi mới quyết định có cần "
             "soi và soi loại nào. Anh/chị tiện [khung giờ 1] hay "
             "[khung giờ 2] ạ?", "S3.1"),
    "L6.9": ("Dạ anh/chị lo đúng chỗ ạ. Dây soi được xử lý theo quy trình rửa - "
             "tiệt khuẩn trước mỗi ca; anh/chị đến có thể xem khu xử lý dây soi.\n"
             "⚠ Mô tả quy trình cụ thể lấy từ THV, không tự viết thêm.\n"
             "Anh/chị tiện [khung giờ 1] hay [khung giờ 2] ạ?", "S3.3"),
    "L6.8": ("Dạ em hiểu ạ. Phần lớn tổn thương phát hiện sớm thì xử lý được, "
             "có những tổn thương nhỏ bác sĩ xử lý ngay trong lúc soi. Biết sớm "
             "là để chủ động, anh/chị ạ.\n"
             "Em giữ giúp anh/chị buổi [Chủ nhật tuần sau] nhé, đổi được nếu "
             "anh/chị có việc.\n"
             "⛔ KHÔNG gửi ưu đãi giảm giá cho nhóm này - họ không lùi vì tiền.",
             "S3.7"),
    "L6.3": ("Dạ bảng giá bên em công khai từng mục ạ: [khung giá theo P7]. "
             "Mức cụ thể phụ thuộc ba thứ - ai thực hiện · có tiền mê hay không · "
             "sinh thiết hay cắt polyp thì chỉ phát sinh khi bác sĩ chỉ định.\n"
             "⚠ Mọi con số lấy từ P7 bản hiện hành. Phần bảo hiểm: ⚠ chờ THV cấp.\n"
             "Anh/chị đến khám trước để biết mình cần làm gì đã nhé, tiện "
             "[khung giờ 1] hay [khung giờ 2] ạ?", "S3.5"),
    "L6.4": ("Dạ phòng khám mở 7h-17h cả Chủ nhật nên anh/chị chọn được buổi "
             "tiện nhất, không phải nghỉ làm ngày thường ạ. Bên em sắp để khám "
             "và soi gọn trong một buổi.\n"
             "Anh/chị tiện [Chủ nhật này] hay [Chủ nhật sau] ạ?", "S3.6"),
    "L6.2": ("Dạ anh/chị so sánh là đúng ạ, và em không so sánh với bệnh viện. "
             "Em nói anh/chị mấy điểm để tự đối chiếu: ai là người trực tiếp soi "
             "và kinh nghiệm bao lâu · hệ máy đời nào, có chế độ nhuộm ảo không · "
             "có bác sĩ gây mê riêng không · bảng giá có công khai không.\n"
             "Ở bên em cố vấn chuyên môn là TS.BS Đỗ Anh Giang, nguyên Phó Giám "
             "đốc Trung tâm Tiêu hóa - Gan mật Bệnh viện Bạch Mai; hệ nội soi là "
             "Fujifilm VP-7000 có AI.\n"
             "Anh/chị tiện [khung giờ 1] hay [khung giờ 2] ạ?", "S3.4"),
    "L6.6": ("Dạ vâng anh/chị. Buổi khám đầu anh/chị đưa [người nhà] đi cùng "
             "được ạ, hai người nghe bác sĩ nói một lượt thì dễ quyết hơn.\n"
             "Anh/chị tiện [Chủ nhật này] hay [Chủ nhật sau] ạ?", "S3.8"),
    "L2.5": ("Dạ phòng khám chỉ có một cơ sở ở 139 Đại La, Tương Mai, Hà Nội ạ. "
             "Với anh/chị ở xa thì bên em sắp để khám, soi và nhận kết quả gọn "
             "trong một buổi; nếu làm tiền mê thì anh/chị cần có người đi cùng.\n"
             "Anh/chị dự kiến lên Hà Nội hôm nào để em giữ lịch ạ?", "S3.9"),
    "L4.1": ("Em cảm ơn anh/chị. Khoảng [10 phút nữa / 16h chiều nay], "
             "[tên người gọi] của Tiêu Hóa Việt sẽ gọi anh/chị từ số [hotline]. "
             "Anh/chị để ý máy giúp em nhé, bận thì nhắn em dời giờ ạ.\n"
             "Em gửi kèm hướng dẫn chuẩn bị {hướng_dẫn_chuẩn_bị} ⚠ để anh/chị "
             "soi được luôn trong buổi khám nếu bác sĩ chỉ định.", "X1 · X6"),
    "L5.3": ("Dạ em gọi anh/chị không được ạ. Anh/chị tiện nghe máy khung giờ "
             "nào để em báo bác sĩ sắp xếp ạ? [sáng 9-11h] hay [chiều 14-17h] ạ?",
             "X2"),
}
KHUNG_MAC_DINH = ("Dạ chào anh/chị, em thấy anh/chị đang quan tâm [dịch vụ theo "
                  "post]. Anh/chị đang có biểu hiện gì và bị bao lâu rồi ạ?\n"
                  "Anh/chị có dấu hiệu nào như nôn ra máu, đi ngoài phân đen, "
                  "sụt cân nhanh hay nuốt nghẹn không ạ?\n"
                  "⚠ Khung mở hội thoại - cần cá nhân hoá theo tình trạng của "
                  "chính khách này.", "S1.3")

NHOM_DT = {  # suy tu l_code + co_sdt, de dien cot "Nhom KH (insight)"
    "Z": "Z 🚩 CA CỜ ĐỎ — xử lý trước mọi nhóm",
    "A1": "A1 hỏi giá ngay chưa kể triệu chứng",
    "A2": "A2 triệu chứng dai dẳng, đã tự uống thuốc",
    "A3": "A3 tầm soát chủ động / chưa có triệu chứng",
    "A4": "A4 sợ nội soi hoặc ngại tiền mê",
    "A5": "A5 ở xa Hà Nội",
    "A6": "A6 mang kết quả nơi khác đến",
    "A7": "A7 né kết quả (L6.8)",
    "B1": "B1 vừa cho số",
    "B2": "B2 chưa kết nối được",
    "B3": "B3 chỉ nhắn Zalo",
    "B4": "B4 đã gọi còn rào cản",
    "B5": "B5 đã đặt lịch — CẦN DẶN CHUẨN BỊ",
    "C1": "C1 vừa soi xong / đang theo dõi",
    "C2": "C2 đến hẹn soi lại",
    "C3": "C3 giới thiệu người nhà",
}


# --------------------------------------------------------------- tien ich

def doc_rows(p):
    rows = json.load(io.open(p, encoding="utf-8"))
    if not rows:
        raise SystemExit("rows.json rỗng.")
    return rows


def pc(tu, mau):
    """Ty le phan tram, dung dau phay thap phan theo quy uoc tieng Viet."""
    if not mau:
        return "0,0%"
    return ("%.1f%%" % (100.0 * tu / mau)).replace(".", ",")


def co_sdt(r):
    return str(r.get("co_sdt", "")).lower().startswith("c")


def ma_rao_can(r):
    return [c["ma"] for c in r.get("rao_can", [])]


def co_do_ma(r):
    return [c["ma"] for c in r.get("co_do", [])]


def nhom_dt(r):
    """Suy nhom doi tuong Z/A/B/C tu du lieu da cham.

    Nhom Z (co do) thang moi nhom khac: ca nay xu ly truoc, va KHONG duoc
    nam trong hang doi nuoi duong.
    """
    if co_do_ma(r):
        return NHOM_DT["Z"]
    if r.get("van_de") == "TH-02":
        return NHOM_DT["C2"]
    if r.get("giai_doan") == "CS":
        return NHOM_DT["C1"]
    if co_sdt(r):
        if r.get("ghi_de") == "đã đặt lịch":
            return NHOM_DT["B5"]
        if r.get("l_code") == "L5.6":
            return NHOM_DT["B3"]
        if r.get("l_code") == "L5.3":
            return NHOM_DT["B2"]
        return NHOM_DT["B4"] if ma_rao_can(r) else NHOM_DT["B1"]
    rc = ma_rao_can(r)
    if r.get("l_code") == "L2.5":
        return NHOM_DT["A5"]
    if r.get("van_de") == "TH-11":
        return NHOM_DT["A6"]
    if "L6.8" in rc:
        return NHOM_DT["A7"]
    if "L6.5" in rc or "L6.7" in rc:
        return NHOM_DT["A4"]
    if r.get("van_de") == "TH-03":
        return NHOM_DT["A3"]
    if r.get("van_de") in ("TH-04", "TH-05", "TH-09"):
        return NHOM_DT["A2"]
    return NHOM_DT["A1"]


def khung_nd(r):
    """Tra ve (noi dung khung, ma kich ban). Khung - phai ca nhan hoa lai.

    Ca co co do dung khung rieng "CĐ": moi khach den kham som, khong neu gia,
    khong tran an. Khung nay thang moi rao can khac.
    """
    if co_do_ma(r):
        return KHUNG_ND["CĐ"]
    for ma in ma_rao_can(r):
        if ma in KHUNG_ND:
            return KHUNG_ND[ma]
    if r.get("l_code") in KHUNG_ND:
        return KHUNG_ND[r["l_code"]]
    return KHUNG_MAC_DINH


def rao_can_chu(r):
    rc = r.get("rao_can", [])
    if not rc:
        return "— chưa xác định rào cản"
    return " · ".join("%s %s" % (c["ma"], c["ten"]) for c in rc)


def dem(rows, key):
    return collections.Counter(r.get(key) for r in rows)


def du_mau(n):
    return "Đủ" if n >= NGUONG_MAU else "⚠ chưa đủ mẫu"


def ghi(wb, out_dir, ten):
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    p = os.path.join(out_dir, ten)
    wb.save(p)
    return p


# -------------------------------------------------------- khoi dung chung

def khoi_canh_bao_chuan(ws, rows, mau_loc=None, extra=None):
    n = len(rows)
    it_mau = [v for v in dem(rows, "van_de").values() if v < NGUONG_MAU]
    d = []
    if mau_loc:
        d.append("MẪU ĐÃ BỊ LỌC: %s. Hội thoại đã lọc thiên về phía nóng, "
                 "thổi phồng mọi post và thổi KHÔNG ĐỀU NHAU → chỉ dùng tham "
                 "khảo, KHÔNG dùng để quyết ngân sách." % mau_loc)
    else:
        d.append("Mẫu: %d hội thoại. ⚠ Người lập báo cáo phải xác nhận đây là "
                 "TOÀN BỘ hội thoại trong kỳ, hay đã lọc (theo độ dài / theo "
                 "có số điện thoại)." % n)
    d.append("%d nhóm vấn đề có dưới %d hội thoại → ⚠ chưa đủ mẫu, "
             "không xếp hạng, không khuyến nghị." % (len(it_mau), NGUONG_MAU))
    cd = [r for r in rows if r.get("co_do")]
    if cd:
        d.append("🚩 %d ca có dấu hiệu CỜ ĐỎ trong kỳ. Luật ghi đè đẩy mọi ca "
                 "này lên HOT, nên %% HOT của bảng chia nhóm KHÔNG nói về chất "
                 "lượng quảng cáo — đọc cột đã trừ cờ đỏ, và tách TH-01 ra khỏi "
                 "mọi so sánh." % len(cd))
        d.append("🚩 Danh sách cờ đỏ do script quét bằng TỪ KHOÁ và nhận RỘNG. "
                 "Đây là danh sách CẦN NGƯỜI ĐỌC LẠI, không phải kết luận y khoa.")
    else:
        d.append("🚩 Không phát hiện ca có dấu hiệu cờ đỏ theo 6 mã CĐ-1…CĐ-6 "
                 "trong %d hội thoại. Vẫn phải giữ khối này trong báo cáo để "
                 "người đọc biết là ĐÃ SÀNG." % n)
    d.append("Mọi con số giá/ưu đãi trong file đều phải đối chiếu P7 bản hiện "
             "hành. Số nào trích từ hội thoại thì là 'nhân viên đã nói với "
             "khách', không phải giá chính thức. Giá của THV thay đổi theo "
             "NGƯỜI THỰC HIỆN và theo có tiền mê hay không.")
    d.append("Phễu có BA con số ở cuối: đặt lịch → đến khám → SOI ĐƯỢC. "
             "Chưa có số thì ghi ⚠ chưa đo được. Không lấy 'đặt lịch' thay cho "
             "'đến khám', không lấy 'đến khám' thay cho 'soi được'.")
    for x in (extra or []):
        d.append(x)
    return khoi_canh_bao(ws, "CẢNH BÁO PHƯƠNG PHÁP — đọc trước khi dùng số", d)


def bang_5_tin_hieu(ws):
    muc(ws, "Năm tín hiệu chấm độ nóng")
    dong_tieu_de(ws, ["#", "Tín hiệu", "Tính là CÓ khi"])
    for a, b, c in [
        ("①", "Nêu triệu chứng / chỉ định cụ thể",
         "\"đau thượng vị 2 tháng\", \"đi ngoài ra máu\", \"bác sĩ bảo cần "
         "soi đại tràng\" — không tính \"khám tiêu hóa\""),
        ("②", "Mốc thời gian ≤ 14 ngày",
         "hôm nay / mai / tuần này / Chủ nhật này · đã đặt lịch · đang đến"),
        ("③", "Hỏi lịch, bác sĩ, giá hoặc cách chuẩn bị theo tình trạng của mình",
         "\"ca của em soi loại nào\", \"em huyết áp cao thì mê được không\" — "
         "không tính câu hỏi giá chung chung ở tin đầu"),
        ("④", "Gửi kết quả cũ / mô tả rõ",
         "có ảnh kết quả, đơn thuốc, phiếu hẹn · hoặc mô tả đủ: triệu chứng · "
         "bao lâu · đã khám hay uống thuốc gì"),
        ("⑤", "Để lại SĐT/Zalo và đồng ý nhận tư vấn",
         "ưu tiên có nêu khung giờ tiện nghe máy"),
    ]:
        dong(ws, [a, b, c])
    trong(ws)
    muc(ws, "Bốn luật ghi đè — đặc thù ngành tiêu hóa, áp bất kể điểm")
    dong_tieu_de(ws, ["#", "Luật", "Vì sao"])
    for a, b, c in [
        ("①", "Đã đặt lịch / đang đến → HOT", "Hiển nhiên"),
        ("②", "🚩 CÓ CỜ ĐỎ → HOT, và gắn cờ ưu tiên y tế",
         "ĐÂY LÀ LUẬT AN TOÀN, không phải luật bán hàng: nó tồn tại để ca này "
         "được gọi trước mọi ca khác và được chuyển bác sĩ trong ngày, không "
         "phải để nói ca này dễ chốt"),
        ("③", "ĐÃ CÓ KẾT QUẢ nơi khác, hoặc đã được chỉ định soi (TH-11) → HOT",
         "Khách đã qua giai đoạn 'có cần soi hay không', chỉ còn chọn nơi làm. "
         "Lead nóng nhất của ngành, mà tin nhắn thường rất ngắn nên bị chấm "
         "thấp oan"),
        ("④", "Đến hẹn soi lại (TH-02) → tối thiểu WARM",
         "Nhóm này viết tin ngắn, không có triệu chứng cấp, nhưng gần như chắc "
         "chắn soi — họ chỉ đang chọn đặt lịch ở đâu"),
    ]:
        dong(ws, [a, b, c])


def bang_co_do(ws, rows):
    """Khoi CO DO — bat buoc dat TRUOC moi bang khac cua moi bao cao."""
    cd = [r for r in rows if r.get("co_do")]
    muc(ws, "🚩 CỜ ĐỎ — đọc trước mọi con số khác")
    if not cd:
        dong(ws, ["Đã sàng %d hội thoại theo 6 mã CĐ-1…CĐ-6. "
                  "Không phát hiện ca có dấu hiệu cờ đỏ trong kỳ."
                  % len(rows)])
        return
    dong_tieu_de(ws, ["STT HT", "Tên KH", "Mã CĐ", "Dấu hiệu", "Có SĐT",
                      "Phụ trách", "NV có trấn an sai?", "L-code",
                      "Việc phải làm ngay"])
    for r in sorted(cd, key=lambda x: (not x.get("tran_an_sai_nv"), x["stt"])):
        tas = r.get("tran_an_sai_nv") or []
        viec = ("GỌI LẠI NGAY + rà soát lại hội thoại với trưởng nhóm"
                if tas else
                ("Gọi trong SLA ≤5' + chuyển bác sĩ trong ngày"
                 if co_sdt(r) else
                 "Chưa có SĐT — nhắn lại mời khám sớm, ghi nhận vào danh sách "
                 "chưa tiếp cận được"))
        dong(ws, [r["stt"], r["ten"],
                  " ".join(c["ma"] for c in r["co_do"]),
                  " · ".join(c["ten"] for c in r["co_do"]),
                  "Có" if co_sdt(r) else "Không",
                  r.get("nv", ""),
                  ("CÓ: " + ", ".join(tas)) if tas else "Không",
                  r.get("l_code", ""), viec],
             nen=None if not tas else "F9D5D5")
    trong(ws)
    nhan_ra = len([r for r in cd if not r.get("tran_an_sai_nv")])
    dong(ws, ["Tỷ lệ xử lý đúng: %d/%d ca. MỐC LÀ 100%% — đây là mốc duy nhất "
              "của hệ này không thương lượng. Dưới 100%% thì xử lý trước khi "
              "hết kỳ, không chờ báo cáo sau." % (nhan_ra, len(cd))])
    dong(ws, ["⚠ Script quét bằng từ khoá và nhận RỘNG: thà gắn thừa còn hơn bỏ "
              "sót. Danh sách này CẦN NGƯỜI ĐỌC LẠI. Lưu ý máu ĐỎ TƯƠI khi đi "
              "ngoài là TH-06, không phải cờ đỏ; PHÂN ĐEN thì là cờ đỏ."])
    trong(ws)


def bang_phan_bo(ws, rows):
    n = len(rows)
    muc(ws, "Kết quả phân loại — đếm thật từ dữ liệu")
    dong_tieu_de(ws, ["Chỉ số", "Số", "Tỷ lệ"])
    sdt = sum(1 for r in rows if co_sdt(r))
    dong(ws, ["Tổng hội thoại", n, "100,0%"], dam=True)
    dong(ws, ["Có SĐT", sdt, pc(sdt, n)])
    dong(ws, ["Không có SĐT", n - sdt, pc(n - sdt, n)])
    trong(ws)

    dong_tieu_de(ws, ["Độ nóng", "Số", "Tỷ lệ", "Ghi chú"])
    dn = dem(rows, "do_nong")
    gd = [r for r in rows if r.get("ghi_de")]
    for k in ("HOT", "WARM", "COLD"):
        gc = ""
        if k == "HOT" and gd:
            gc = "trong đó %d ca do luật ghi đè" % len(gd)
        dong_nong(ws, [k, dn[k], pc(dn[k], n), gc], k)
    for k, v in collections.Counter(r["ghi_de"] for r in gd).items():
        dong(ws, ["   ghi đè: " + k, v, pc(v, n), ""])
    trong(ws)

    dong_tieu_de(ws, ["Nhóm giá trị", "Số", "Tỷ lệ", "Nghĩa"])
    gt = dem(rows, "nhom_gia_tri")
    for k, ng in [("G1", "Combo dạ dày + đại tràng · can thiệp (cắt polyp, "
                         "cầm máu) · gói tầm soát"),
                  ("G2", "Soi dạ dày HOẶC đại tràng đơn lẻ · soi + test HP"),
                  ("G3", "Khám chuyên khoa · trực tràng · sigma · siêu âm · "
                         "test HP"),
                  ("?", "Chưa xác định được — thường là TH-12 hỏi chung")]:
        if gt[k]:
            dong(ws, [k, gt[k], pc(gt[k], n), ng], nen=MAU_GIA_TRI.get(k))
    dong(ws, ["⚠ Lưu ý khi đọc", "", "",
              "Một lead WARM của combo tầm soát (WARM·G1) đáng đầu tư hơn một "
              "lead HOT của khám đầy hơi (HOT·G3) — dải giá chênh gần chín lần. "
              "Không xếp hạng lead chỉ bằng độ nóng."])
    trong(ws)

    dong_tieu_de(ws, ["Nhóm vấn đề", "Tên nhóm", "Số", "Tỷ lệ", "Đủ mẫu?"])
    vd = dem(rows, "van_de")
    for ma in VAN_DE_MA:
        if vd[ma]:
            dong(ws, [ma, VAN_DE_TEN[ma], vd[ma], pc(vd[ma], n), du_mau(vd[ma])],
                 nen=MO if vd[ma] < NGUONG_MAU else None)
    trong(ws)

    dong_tieu_de(ws, ["Giai đoạn", "Số", "Tỷ lệ"])
    g = dem(rows, "giai_doan")
    for k in ("S1", "S2", "S3", "CS"):
        if g[k]:
            dong(ws, [k, g[k], pc(g[k], n)], nen=B1 if k == "S1" else None)
    trong(ws)

    dong_tieu_de(ws, ["Rào cản", "Nhóm", "Số lượt", "% trên tổng HT"])
    c = collections.Counter()
    for r in rows:
        for x in r.get("rao_can", []):
            c[(x["ma"], x["nhom"], x["ten"])] += 1
    for (ma, nh, ten), v in sorted(c.items(), key=lambda x: -x[1]):
        dong(ws, ["%s %s" % (ma, ten), nh, v, pc(v, n)])
    dong(ws, ["⚠ Cách đếm", "", "",
              "Một hội thoại có thể mang nhiều rào cản → tổng lượt LỚN HƠN "
              "tổng hội thoại là đúng, không phải lỗi."])


# ------------------------------------------------------------------- R1

def r1(rows, ky, dich_vu, out_dir, mau_loc=None):
    n = len(rows)
    ra = []

    # ---------- FILE 1: goc nhin QUY TRINH
    wb = so_moi()
    ws = sheet(wb, "Tổng quan")
    tieu_de(ws, "R1 · PHÂN LOẠI & KỊCH BẢN HỘI THOẠI — %s" % dich_vu,
            "Kỳ %s · %d hội thoại · góc nhìn QUY TRÌNH · lập ngày %s"
            % (ky, n, _hom_nay()))
    muc(ws, "Sơ đồ 4 bước")
    so_do_buoc(ws, [
        ("① ĐỐI TƯỢNG", "Khách là ai, đang bị gì", B1),
        ("② NHÓM", "Xếp vào nhóm chăm nào", B2),
        ("③ KỊCH BẢN", "Chọn mã kịch bản", B3),
        ("④ NỘI DUNG", "Soạn tin gửi được ngay", B4),
    ])
    trong(ws)
    bang_co_do(ws, rows)
    khoi_canh_bao_chuan(ws, rows, mau_loc)
    trong(ws)
    bang_5_tin_hieu(ws)
    trong(ws)
    bang_phan_bo(ws, rows)
    trong(ws)
    muc(ws, "Bảy nguyên tắc bắt buộc khi dùng nội dung trong file này")
    for i, t in enumerate([
        "Mọi nội dung là BẢN ĐỀ XUẤT — người duyệt trước khi gửi khách.",
        "Cột nội dung là KHUNG theo rào cản, phải cá nhân hoá theo tình trạng "
        "của chính khách đó (triệu chứng gì, bao lâu, điều khách vừa lo).",
        "🚩 Ca có CỜ ĐỎ: chỉ mời khám sớm + ghi rõ đã chuyển bác sĩ. "
        "⛔ Không nêu giá, ⛔ không trấn an, ⛔ không nói khả năng mắc bệnh gì.",
        "⛔ Không chẩn đoán, không loại trừ bệnh, không đọc kết quả xét nghiệm, "
        "không tư vấn thuốc hay phác đồ — kể cả phác đồ diệt HP.",
        "Không dùng từ cấm: khỏi 100% · không đau · an toàn tuyệt đối · "
        "sạch HP 100% · chắc chắn không phải ung thư · tốt nhất · rẻ nhất.",
        "Nêu khung giá công khai thì được, nhưng phải kèm BA ĐIỀU KIỆN: "
        "ai thực hiện · có tiền mê hay không · phụ phí chỉ khi có chỉ định. "
        "Chốt số cuối cho ca cụ thể thì không.",
        "CTA là ĐẾN KHÁM với bác sĩ tiêu hóa, nói rõ bác sĩ xem xong mới quyết "
        "định có soi và soi loại nào. MỜI KHÁM LÀ PHẢI DẶN CHUẨN BỊ.",
    ], start=1):
        dong(ws, ["%d." % i, t])
    hoan_thien(ws)

    sheet_chu_giai(wb)

    ws = sheet(wb, "Khung 5 bước B1-B5")
    tieu_de(ws, "KHUNG 5 BƯỚC TƯ VẤN B1 → B5",
            "Thước đo cấu trúc hội thoại. Bỏ bước nào thì mất lead ở đúng "
            "khâu đó.")
    dong_tieu_de(ws, ["Bước", "Làm gì", "Câu mẫu", "Lưu ý"])
    for b, lg, cm, lu in [
        ("B1", "MỞ — chào và định danh theo đúng post khách bấm vào",
         "Chào anh/chị, em là [tên], tư vấn viên của Tiêu Hóa Việt. Em thấy "
         "anh/chị đang quan tâm [dịch vụ theo post]. Anh/chị đang bị "
         "[tình trạng] ở vị trí nào và bao lâu rồi ạ?",
         "Gọi ĐÚNG TÊN dịch vụ theo quảng cáo khách vừa bấm — không hỏi chung "
         "\"anh/chị cần tư vấn gì\". Phản hồi trong 2 phút."),
        ("B2", "KHÁM PHÁ — sàng cờ đỏ TRƯỚC, rồi thu đủ 5 THÔNG TIN",
         "Anh/chị có dấu hiệu nào như nôn ra máu, đi ngoài phân đen, sụt cân "
         "nhanh hay nuốt nghẹn không ạ?\n"
         "Trước đây anh/chị đã khám hay soi ở đâu chưa, có kết quả không ạ?\n"
         "Anh/chị có bệnh nền hay đang dùng thuốc gì không ạ?",
         "NĂM thông tin: ① triệu chứng + bao lâu · ② 🚩 CÓ DẤU HIỆU CỜ ĐỎ KHÔNG · "
         "③ đã khám/soi ở đâu chưa, có kết quả không · ④ BỆNH NỀN & THUỐC ĐANG "
         "DÙNG · ⑤ thời gian dự kiến.\n"
         "Ngành tiêu hóa cần 5, nhiều hơn ngành nha hai mục là ② và ④. "
         "Thiếu ② là bỏ sót ca cần ưu tiên y tế; thiếu ④ là hẹn tiền mê cho "
         "người chưa đủ điều kiện → khách đến rồi phải về.\n"
         "🚩 Có cờ đỏ thì DỪNG khai thác, mời khám trong ngày, chuyển bác sĩ."),
        ("B3", "TẠO TIN CẬY — đưa bằng chứng ĐÚNG rào cản khách mang",
         "Với biểu hiện kéo dài như vậy, bác sĩ cần soi mới thấy được bề mặt "
         "niêm mạc. Ở Tiêu Hóa Việt hệ nội soi là Fujifilm VP-7000 có AI, chế "
         "độ BLI/LCI giúp bác sĩ nhìn rõ các tổn thương nhỏ; cố vấn chuyên môn "
         "là TS.BS Đỗ Anh Giang, nguyên Phó Giám đốc Trung tâm Tiêu hóa - Gan "
         "mật Bệnh viện Bạch Mai.",
         "Gỡ ĐÚNG MỘT rào cản (SỢ / NGỜ / NGẠI / NÉ), không rải hết. "
         "Thứ tự bằng chứng: chuyên gia Bạch Mai → hệ Fujifilm + AI → giấy phép "
         "Sở Y tế → bác sĩ gây mê theo dõi riêng → bảng giá công khai.\n"
         "KHÔNG HÙ BỆNH: nói về lợi ích của việc biết sớm, không về hình phạt "
         "của việc chậm. Không hứa kết quả."),
        ("B4", "XIN SỐ — lý do phải CÓ LỢI CHO KHÁCH",
         "Để bác sĩ xem trước thông tin và sắp lịch đúng buổi anh/chị tiện, "
         "anh/chị cho em xin số điện thoại (có Zalo) nhé. "
         "Anh/chị tiện nghe máy khung giờ nào ạ?",
         "❌ Không xin số bằng lý do \"để gửi ưu đãi\". "
         "Luôn hỏi kèm khung giờ. Tối đa 2 lần/hội thoại."),
        ("B5", "XÁC NHẬN — báo trước ai gọi, số nào, lúc mấy giờ",
         "Em cảm ơn. Khoảng [10 phút nữa / 16h chiều nay], [tên người gọi] của "
         "Tiêu Hóa Việt sẽ gọi anh/chị từ số [hotline]. Anh/chị để ý máy giúp "
         "em nhé. Bận thì nhắn em, em dời giờ cho anh/chị.",
         "BỐN thứ bắt buộc: tên người sẽ gọi · số sẽ gọi đến · giờ gọi · "
         "DẶN CHUẨN BỊ. Kèm lối thoát \"bận thì em dời giờ\".\n"
         "B5 của ngành tiêu hóa có một mục hơn ngành nha: dặn chuẩn bị. "
         "Bỏ nó là nguyên nhân số một của việc khách đến tận nơi mà không soi "
         "được.\n⚠ Dùng bản hướng dẫn chuẩn bị chính thức của THV — trực page "
         "KHÔNG tự nêu số giờ nhịn ăn hay cách uống thuốc làm sạch đại tràng."),
    ]:
        dong(ws, [b, lg, cm, lu])
    hoan_thien(ws)

    ws = sheet(wb, "Quy trình %d HT" % n)
    tieu_de(ws, "QUY TRÌNH — %d HỘI THOẠI" % n,
            "Mỗi hội thoại đi trọn 4 bước trên một dòng. Cột \"Nội dung gợi ý\" "
            "là KHUNG theo rào cản — PHẢI cá nhân hoá trước khi gửi.")
    dong_tieu_de(ws, ["STT", "Tên khách", "🚩 Cờ đỏ", "Nhóm vấn đề",
                      "Triệu chứng / Nhu cầu",
                      "Giai đoạn", "Nhóm KH (insight)", "Nhóm giá trị",
                      "Nhóm chăm sóc", "Kịch bản (mã)", "Tên kịch bản",
                      "Nội dung gợi ý gửi ngay", "Rào cản / ghi chú"])
    for r in rows:
        nd, ma_kb = khung_nd(r)
        nong = r.get("do_nong", "")
        cd = " ".join(c["ma"] for c in r.get("co_do", []))
        dong_nong(ws, [
            r["stt"], r.get("ten", ""),
            ("🚩 " + cd) if cd else "",
            "%s %s" % (r.get("van_de", ""), VAN_DE_TEN.get(r.get("van_de"), "")),
            "⚠ điền từ hội thoại — triệu chứng · bao lâu · đã khám/uống thuốc gì",
            r.get("giai_doan", ""), nhom_dt(r), r.get("nhom_gia_tri", ""),
            "%s · %s" % (nong, r.get("nhom_gia_tri", "")),
            ma_kb, _ten_kb(ma_kb), nd, rao_can_chu(r),
        ], nong, cot_nong=9)
    hoan_thien(ws)

    ws = sheet(wb, "Nhịp chăm sóc")
    tieu_de(ws, "NHỊP CHĂM SÓC THEO NHÓM",
            "Hai nhịp khác nhau: chuỗi T dùng NGAY SAU KHI XIN ĐƯỢC SỐ · "
            "nhịp D dùng khi ĐÃ TƯ VẤN mà chưa đặt lịch khám (L6.x).")
    dong_tieu_de(ws, ["Nhóm", "Khi nào dùng", "Nhịp chạm", "Kịch bản gợi ý",
                      "Điều kiện dừng"])
    for a, b, c, d, e in [
        ("🚩 CỜ ĐỎ", "Hội thoại có dấu hiệu CĐ-1…CĐ-6",
         "GỌI NGAY bất kể độ nóng, bất kể khung giờ. SLA ≤5'. "
         "Chuyển bác sĩ trong ngày", "X5",
         "Đã đến khám. ⛔ Không bao giờ 'thoát' bằng cách im lặng — khách không "
         "phản hồi thì vẫn ghi vào danh sách chưa tiếp cận được"),
        ("HOT · G1", "Có SĐT, ca combo tầm soát / can thiệp / gói chuyên gia",
         "T+0 ≤2' → T+30' → T+2h → T+24h → T+48h gửi hướng dẫn chuẩn bị → "
         "T-1 ngày nhắc lại → T+7 ngày. SLA gọi ≤10'",
         "X1 → S3.x theo rào cản → X6 dặn chuẩn bị",
         "Đã thực hiện nội soi → chuyển luồng kết quả & theo dõi"),
        ("HOT · G2–G3", "Có SĐT, dịch vụ giá trị trung/nhỏ",
         "T+0 ≤2' → T+30' → T+24h → T+48h gửi hướng dẫn chuẩn bị. SLA gọi ≤15'",
         "X1 · X6", "Đã soi được, hoặc chốt lịch gọn"),
        ("HOT gọi nhỡ", "Đã có số, gọi không bắt máy (L5.3)",
         "T+30' nhắn hỏi khung giờ → T+24h gọi lần 2 (nhắn nhắc 15' trước)",
         "X2", "Khách phản hồi, hoặc hết trần 6 lần/7 ngày"),
        ("ĐÃ CÓ LỊCH", "Khách đã đặt được buổi khám (B5)",
         "T+48h gửi hướng dẫn chuẩn bị + hỏi bệnh nền, thuốc đang dùng, có "
         "người đưa về không → T-1 ngày nhắc lại giờ nhịn ăn và mang kết quả cũ",
         "X6", "Đã soi được. Đây là nhịp chặn mốc rò nặng nhất của ngành"),
        ("WARM · G1", "Chưa sẵn sàng NHƯNG là ca giá trị lớn (gồm TH-03 tầm soát)",
         "D+3 → D+7 → D+15 → sau đó 2 tuần/lần. NUÔI TỚI 90 NGÀY, "
         "không hạ tệp ở 30 ngày", "S3.x theo rào cản + nội dung giáo dục",
         "Khách từ chối dứt khoát, hoặc quá 90 ngày không tiến triển"),
        ("WARM · G2–G3", "Chưa sẵn sàng, dịch vụ giá trị trung/nhỏ",
         "D+3 → D+7 → D+15", "S3.x theo rào cản",
         "Quá 30 ngày không tiến triển → tệp remarketing"),
        ("COLD", "Hỏi tham khảo, 0–1 tín hiệu",
         "Nuôi bằng nội dung, không chạm dồn dập", "X4",
         "Quá 30 ngày → tệp remarketing"),
        ("L6.8 NÉ KẾT QUẢ", "Biết nên soi nhưng trì hoãn vì sợ phát hiện ra bệnh",
         "D+7 → D+21 → D+45, nội dung GIÁO DỤC, nhịp thưa. NUÔI TỚI 180 NGÀY",
         "S3.7 — ⛔ KHÔNG gửi ưu đãi giảm giá, họ không lùi vì tiền",
         "Khách tự quay lại, hoặc từ chối dứt khoát. Nhóm này quay lại muộn "
         "nhưng quay lại thật — cắt ở 30 ngày là bỏ tệp dễ gọi lại nhất"),
        ("Ở xa Hà Nội (L2.5)", "Ngoài Hà Nội và vùng lân cận",
         "Chốt một buổi gọn: khám + soi + nhận kết quả trong ngày",
         "S3.9", "Khách chốt được buổi, hoặc từ chối vì khoảng cách"),
        ("TH-11 mang kết quả nơi khác", "Đã có kết quả soi/CT/xét nghiệm",
         "Gọi sớm (HOT theo ghi đè ③), mời bác sĩ đọc trực tiếp",
         "S4.1 — ⛔ KHÔNG đọc kết quả qua inbox, ⛔ không bình luận nơi cũ",
         "Đã đến khám để bác sĩ đọc kết quả"),
        ("TH-02 đến hẹn soi lại", "Đã cắt polyp / đang theo dõi / bác sĩ hẹn",
         "Nhắc theo MỐC ĐÃ GHI TRONG PHIẾU KẾT QUẢ của khách",
         "S4.2 — ⚠ không tự nêu số năm chu kỳ, đó là chỉ định của bác sĩ",
         "Đã soi lại. Tệp giá trị dài hạn lớn nhất của THV"),
        ("Người nhà đặt hộ", "Hội thoại nhắc \"cho bố\", \"cho mẹ\", \"cả nhà\"",
         "Nói với người đặt về quy trình và chuẩn bị; nói với người bệnh về "
         "cảm giác", "CS + mời người nhà cùng tầm soát",
         "Nhóm này hay bị chấm COLD oan — giữ trong tệp LTV, không bỏ"),
    ]:
        dong(ws, [a, b, c, d, e])
    trong(ws)
    dong(ws, ["⚠ TRẦN NHẮN", "Tối đa 6 lần nhắn / 7 ngày. "
              "Khách từ chối thì DỪNG NGAY.", "", "", ""], nen=CANH_BAO)
    hoan_thien(ws)

    ra.append(ghi(wb, out_dir,
                  "THV_%s_PhanLoai_KichBan.xlsx" % _slug(dich_vu)))

    # ---------- FILE 2: goc nhin PHAN LOAI + BANK KICH BAN
    wb = so_moi()
    ws = sheet(wb, "Tổng quan")
    tieu_de(ws, "R1 · PHÂN LOẠI CHI TIẾT & BANK KỊCH BẢN — %s" % dich_vu,
            "Kỳ %s · %d hội thoại · lập ngày %s" % (ky, n, _hom_nay()))
    bang_co_do(ws, rows)
    khoi_canh_bao_chuan(ws, rows, mau_loc)
    trong(ws)
    bang_phan_bo(ws, rows)
    trong(ws)
    muc(ws, "Nhóm đối tượng theo insight")
    dong_tieu_de(ws, ["Mã", "Nhóm", "Số HT", "Insight / nỗi lo thật"])
    c_nhom = collections.Counter(nhom_dt(r) for r in rows)
    for ma, ten in NHOM_DT.items():
        ins = {
            "Z": "🚩 Có phải bệnh nặng không — XỬ LÝ TRƯỚC MỌI NHÓM, "
                 "gọi ≤5' và chuyển bác sĩ trong ngày",
            "A1": "Chưa kể triệu chứng, hỏi giá để sàng lọc nhanh",
            "A2": "Uống thuốc mãi không khỏi, có phải bị nặng rồi không",
            "A3": "Chưa có triệu chứng thì có cần soi không · bao lâu soi lại "
                  "một lần — nhóm GIÁ TRỊ CAO NHẤT mà ít bị chấm HOT",
            "A4": "Tôi có chịu được không · thuốc mê có hại không · "
                  "các anh có nói thật không",
            "A5": "Lên Hà Nội một buổi có xong việc không",
            "A6": "Kết quả này nghĩa là gì · có phải soi lại không",
            "A7": "Tôi sợ chính cái kết quả, không sợ ống soi — "
                  "⛔ gửi ưu đãi cho nhóm này là đẩy họ xa thêm",
            "B1": "Vừa cho số, đang chờ được gọi — rơi ở đây là đắt nhất",
            "B2": "Đã cho số mà không gọi được",
            "B3": "Không muốn nghe điện, chỉ nhắn",
            "B4": "Đã nghe tư vấn, còn vướng một rào cản cụ thể",
            "B5": "Đã có lịch — CẦN DẶN CHUẨN BỊ để soi được luôn trong buổi đó",
            "C1": "Lo kết quả, chế độ ăn, dùng thuốc theo đơn",
            "C2": "Đến hẹn soi lại — tệp gần như chắc chắn quay lại nếu "
                  "được nhắc đúng mốc trong phiếu kết quả",
            "C3": "Hài lòng → giới thiệu người nhà cùng tầm soát",
        }[ma]
        dong(ws, [ma, ten, c_nhom.get(ten, 0), ins])
    trong(ws)
    muc(ws, "Lỗi quan sát trong data — phải tránh")
    dong_tieu_de(ws, ["#", "Lỗi", "Số HT phát hiện", "Dẫn chứng (số hiệu HT)"])
    tc = [r for r in rows if r.get("tu_cam_nv")]
    ngo_ko_hang = [r for r in rows
                   if ma_rao_can(r) and not r.get("bang_chung_nv")]
    co_do_tran_an = [r for r in rows if r.get("tran_an_sai_nv")]
    for i, (ten, dsach, cach) in enumerate([
        ("Lờ câu hỏi giá — khách hỏi giá, nhân viên chỉ đáp \"để lại số\"",
         None, "⚠ cần đọc hiểu, script không bắt được — xem R3"),
        ("Bắn giá cứng cho một ca cụ thể", None,
         "⚠ cần đọc hiểu — xem R3"),
        ("Dán mẫu máy móc, trả lời không dính điều khách vừa nói", None,
         "⚠ cần đọc hiểu — xem R3"),
        ("Nói \"không đau\" / dùng từ cấm", tc, None),
        ("Gắn \"chính hãng\" cho vật liệu ngoài 4 hãng đã duyệt", None,
         "⚠ cần đọc hiểu — xem R3 sheet Rủi ro pháp lý"),
        ("Xin số không có lý do, hoặc lý do \"để gửi ưu đãi\"", None,
         "⚠ cần đọc hiểu — xem R3"),
        ("Xin số rồi để yên — không nhắn xác nhận ai gọi, số nào, mấy giờ",
         None, "⚠ cần đọc hiểu — xem R3"),
        ("Hứa thời gian điều trị cứng", None, "⚠ cần đọc hiểu — xem R3"),
        ("BỎ MẤT BẰNG CHỨNG: khách ngờ vật liệu (L6.7) mà không nhắc đối tác hãng",
         ngo_ko_hang, None),
    ], start=1):
        if dsach is not None:
            dong(ws, [i, ten, len(dsach),
                      ", ".join("HT#%d" % r["stt"] for r in dsach) or "—"],
                 nen=CANH_BAO if dsach else None)
        else:
            dong(ws, [i, ten, CD, cach])
    trong(ws)
    dong(ws, ["⚠ BIẾN SỐ TỪ CHƯƠNG TRÌNH THÁNG", CX,
              "P7 chưa điền → mọi ưu đãi/giá/% /trả góp trong nội dung gợi ý "
              "để dạng {biến} kèm ⚠, trực page tự điền theo P7 hiện hành.", ""],
         nen=CANH_BAO)
    hoan_thien(ws)

    sheet_chu_giai(wb)

    ws = sheet(wb, "Phân loại %d HT" % n)
    tieu_de(ws, "PHÂN LOẠI — %d HỘI THOẠI" % n,
            "Ba trục riêng: L-code (trạng thái) · Độ nóng (sẵn sàng) · "
            "Nhóm giá trị (giá trị kỳ vọng). KHÔNG gộp.")
    dong_tieu_de(ws, ["STT", "Tên KH", "Ngày", "Phụ trách", "Số tin", "SĐT",
                      "Nhóm vấn đề", "Nhóm ĐT", "L-code", "Độ nóng",
                      "Nhóm giá trị", "Rào cản",
                      "Ghi chú (tín hiệu ①②③④⑤)"])
    for r in rows:
        bm = "[%s]" % r.get("bitmask", "")
        if r.get("ghi_de"):
            bm += " → %s (ghi đè: %s)" % (r.get("do_nong"), r["ghi_de"])
        dh = []
        cd = " ".join(c["ma"] for c in r.get("co_do", []))
        if cd:
            dh.append("🚩 " + cd)
        if r.get("tran_an_sai_nv"):
            dh.append("NV TRẤN AN SAI: " + ", ".join(r["tran_an_sai_nv"]))
        if r.get("dau_hieu_nguoi_nha"):
            dh.append("dấu hiệu người nhà")
        if r.get("bang_chung_nv"):
            dh.append("NV có đưa bằng chứng: " + ", ".join(r["bang_chung_nv"]))
        if dh:
            bm += " · " + " · ".join(dh)
        dong_nong(ws, [
            r["stt"], r.get("ten", ""), r.get("ngay", ""), r.get("nv", ""),
            r.get("so_tin", ""), "Có" if co_sdt(r) else "Không",
            "%s %s" % (r.get("van_de", ""), VAN_DE_TEN.get(r.get("van_de"), "")),
            nhom_dt(r).split()[0], r.get("l_code", ""), r.get("do_nong", ""),
            r.get("nhom_gia_tri", ""), rao_can_chu(r), bm,
        ], r.get("do_nong", ""), cot_nong=10)
    hoan_thien(ws)

    ws = sheet(wb, "Kịch bản %s" % dich_vu)
    tieu_de(ws, "BANK KỊCH BẢN THEO NHÓM ĐỐI TƯỢNG — %s" % dich_vu,
            "Chỉ sinh cho các mã CÓ xuất hiện trong dữ liệu. Mã không có ca "
            "nào trong kỳ thì ghi ⚠ chưa có ca, KHÔNG viết lấp.")
    dong_tieu_de(ws, ["Nhóm", "Mã", "Giai đoạn", "Insight khách hàng (nỗi lo thật)",
                      "Rào cản", "L-code", "Nhóm giá trị", "Khi nào dùng",
                      "Nội dung 1", "Nội dung 2", "Nội dung 3", "Lưu ý an toàn"])
    for ma, ten in NHOM_DT.items():
        hts = [r for r in rows if nhom_dt(r) == ten]
        if not hts:
            dong(ws, [ten.split()[0], ma, "—", "⚠ chưa có ca trong kỳ này",
                      "—", "—", "—", "—", "⚠ chưa viết — không có ca để căn cứ",
                      "", "", ""], nen=MO)
            continue
        rc = collections.Counter(x["ma"] for r in hts for x in r.get("rao_can", []))
        rc_chinh = rc.most_common(1)[0][0] if rc else ""
        nd, _ = (KHUNG_ND.get(rc_chinh) or KHUNG_MAC_DINH)
        gt = collections.Counter(r.get("nhom_gia_tri") for r in hts)
        dong(ws, [
            ten.split()[0], ma,
            " · ".join(sorted({r.get("giai_doan", "") for r in hts})),
            "⚠ viết lại theo lời khách thật trong %d ca của nhóm này" % len(hts),
            "%s %s" % (rc_chinh, RAO_CAN_TEN.get(rc_chinh, ("", ""))[1])
            if rc_chinh else "— chưa xác định",
            " · ".join(sorted({r.get("l_code", "") for r in hts})),
            " · ".join("%s(%d)" % (k, v) for k, v in gt.most_common() if k),
            "%d ca trong kỳ · %s" % (len(hts), du_mau(len(hts))),
            nd,
            "⚠ chưa viết — nội dung chạm lần 2",
            "⚠ chưa viết — nội dung chạm lần 3",
            "Không từ cấm · \"chính hãng\" chỉ cho 4 hãng duyệt · "
            "không chốt giá ca cụ thể · không hứa thời gian cứng · "
            "không chẩn đoán qua tin nhắn",
        ], nen=MO if len(hts) < NGUONG_MAU else None)
    hoan_thien(ws)

    ws = sheet(wb, "Chăm sóc nóng × giá trị")
    tieu_de(ws, "CHĂM SÓC THEO ĐỘ NÓNG × NHÓM GIÁ TRỊ",
            "Chín ô = 3 độ nóng × 3 nhóm giá trị. Tổng số lead phải bằng %d."
            % n)
    dong_tieu_de(ws, ["Độ nóng", "Nhóm giá trị", "Số lead", "Nghĩa",
                      "Tín hiệu nhận biết", "SLA kết nối", "Nhịp chăm sóc",
                      "Hành động", "Mục tiêu"])
    bang = {
        ("HOT", "G1"): ("Sẵn sàng đặt lịch, ca giá trị lớn",
                        "4–5 tín hiệu, hoặc đã có phim / đã đặt lịch",
                        "≤ 5' giờ hành chính · ≤10' giờ cao điểm",
                        "T+0 → T+7", "ƯU TIÊN TUYỆT ĐỐI — người giỏi nhất nhận",
                        "Đến khám trong 48h"),
        ("HOT", "G2"): ("Sẵn sàng, giá trị trung", "4–5 tín hiệu",
                        "≤ 10'", "T+0 → T+24h", "Gọi theo SLA",
                        "Đến khám trong tuần"),
        ("HOT", "G3"): ("Sẵn sàng, giá trị nhỏ", "4–5 tín hiệu",
                        "≤ 10'", "T+0 → T+24h",
                        "Chốt lịch nhanh gọn — KHÔNG dồn người giỏi nhất",
                        "Đến khám + phát sinh dịch vụ tiếp theo"),
        ("WARM", "G1"): ("Chưa sẵn sàng NHƯNG đáng đầu tư hơn HOT·G3",
                         "2–3 tín hiệu, còn vướng rào cản",
                         "≤ 30'", "D+3 → D+7 → D+15 → NUÔI TỚI 90 NGÀY",
                         "Nuôi kỹ bằng bằng chứng đối tác hãng, không bỏ",
                         "Chuyển lên HOT trong 90 ngày"),
        ("WARM", "G2"): ("Quan tâm rõ, giá trị trung", "2–3 tín hiệu",
                         "≤ 30'", "D+3 → D+7 → D+15", "Nuôi theo nhịp chung",
                         "Chuyển lên HOT trong 30 ngày"),
        ("WARM", "G3"): ("Quan tâm, giá trị nhỏ", "2–3 tín hiệu",
                         "≤ 30'", "D+3 → D+7", "Nhắn Zalo, mời khám định kỳ",
                         "Đến khám"),
        ("COLD", "G1"): ("Hỏi tham khảo, nhưng là ca giá trị lớn",
                         "0–1 tín hiệu", "Nhắn Zalo ≤2h",
                         "Nuôi dài hạn bằng nội dung giáo dục",
                         "KHÔNG BỎ — đây là chỗ mất tiền nhiều nhất nếu bỏ",
                         "Chuyển lên WARM"),
        ("COLD", "G2"): ("Hỏi tham khảo", "0–1 tín hiệu", "Nhắn Zalo ≤2h",
                         "Nhịp chung", "Nuôi bằng nội dung", "Chuyển lên WARM"),
        ("COLD", "G3"): ("Hỏi tham khảo, giá trị nhỏ", "0–1 tín hiệu",
                         "Nhắn Zalo trong ngày", "Chạm thưa",
                         "Tệp remarketing", "Quay lại khi có nhu cầu"),
    }
    tong = 0
    for nong in ("HOT", "WARM", "COLD"):
        for gt in ("G1", "G2", "G3"):
            sl = sum(1 for r in rows if r.get("do_nong") == nong
                     and r.get("nhom_gia_tri") == gt)
            tong += sl
            v = bang[(nong, gt)]
            dong_nong(ws, [nong, gt, sl] + list(v), nong, cot_nong=1)
    khac = n - tong
    if khac:
        dong(ws, ["—", "?", khac, "Chưa xác định được nhóm giá trị",
                  "Thường là TH-12 hỏi chung", "—", "—",
                  "⚠ cần đọc lại để gán nhóm giá trị", "—"], nen=CANH_BAO)
    dong(ws, ["TỔNG", "", n, "Phải bằng tổng hội thoại đếm được ở sheet 1",
              "", "", "", "", ""], dam=True)
    hoan_thien(ws)

    ra.append(ghi(wb, out_dir, "THV_KichBan_%s.xlsx" % _slug(dich_vu)))
    return ra


def _ten_kb(ma):
    t = {
        "S1.3": "Chào mở, chưa rõ nhu cầu",
        "S3.1": "Sợ nội soi — nói thật cảm giác, nêu bản tiền mê",
        "S3.2": "Ngại tiền mê — sàng lọc trước mê, bác sĩ gây mê theo dõi riêng",
        "S3.3": "Ngờ vệ sinh dây soi — quy trình rửa, tiệt khuẩn",
        "S3.4": "So sánh nơi khác — đưa bộ tiêu chí, không nói xấu tuyến công",
        "S3.5": "Chưa tài chính — khung giá công khai + ba điều kiện",
        "S3.6": "Chưa sắp xếp thời gian — nhắc mở cả Chủ nhật",
        "S3.7": "NÉ KẾT QUẢ — nói về lợi ích biết sớm, KHÔNG gửi ưu đãi",
        "S3.8": "Hỏi người nhà — mời đi cùng buổi khám",
        "S3.9": "Ở xa Hà Nội — gộp mọi việc vào một buổi",
        "S4.1": "Mang kết quả nơi khác đến — mời bác sĩ đọc trực tiếp",
        "S4.2": "Đến hẹn soi lại — nhắc theo mốc trong phiếu kết quả",
        "X1": "Xin SĐT đúng cách",
        "X1 · X6": "Xác nhận ai gọi/số nào/mấy giờ + dặn chuẩn bị",
        "X2": "Gọi nhỡ — hỏi lại khung giờ",
        "X4": "Nuôi dưỡng COLD / im lặng",
        "X5": "🚩 CA CỜ ĐỎ — mời khám trong ngày, chuyển bác sĩ, không nêu giá",
        "X6": "Dặn chuẩn bị trước buổi hẹn",
        "CS": "Sau nội soi — hướng dẫn, nhắc mốc tái soi",
    }
    return t.get(ma, "⚠ chưa đặt tên kịch bản")


# ------------------------------------------------------------------- R2

def doc_posts(p):
    """Doc bang markdown danh sach post. Tra ve dict ten_post -> thong tin."""
    if not p or not os.path.exists(p):
        return {}
    out = {}
    for line in io.open(p, encoding="utf-8"):
        if not line.strip().startswith("|"):
            continue
        o = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(o) < 4 or o[0] in ("Mã post", "---") or set(o[0]) <= set("-: "):
            continue
        out[o[1]] = {"ma": o[0], "dich_vu": o[2], "headline": o[3],
                     "goc": o[8] if len(o) > 8 else "",
                     "gom": o[6] if len(o) > 6 else ""}
    return out


def r2(rows, ky, dich_vu, out_dir, posts=None, mau_loc=None):
    n = len(rows)
    ps = doc_posts(posts)
    che_do = "A · ĐO THẬT" if any(r.get("post", "").startswith("QC")
                                  for r in rows) else "B · DỰ ĐOÁN"

    def gom(r):
        p = r.get("post", "") or "(không rõ nguồn)"
        if p in ps and ps[p].get("gom"):
            for ten, inf in ps.items():
                if inf["ma"] == ps[p]["gom"]:
                    return ten
        return p

    theo_post = collections.defaultdict(list)
    for r in rows:
        theo_post[gom(r)].append(r)

    wb = so_moi()
    ws = sheet(wb, "Tổng quan")
    tieu_de(ws, "R2 · PHÂN TẦNG POST QUẢNG CÁO — %s" % dich_vu,
            "Kỳ %s · chế độ %s · %d hội thoại · %d post · lập ngày %s"
            % (ky, che_do, n, len([k for k in theo_post if k.startswith("QC")]),
               _hom_nay()))
    noi = sum(1 for r in rows if r.get("post", "").startswith("QC"))
    muc(ws, "Dữ liệu đọc được")
    dong_tieu_de(ws, ["Chỉ số", "Số"])
    for a, b in [("Tổng hội thoại", n), ("Nối được với post qua thẻ", noi),
                 ("Thẻ không phải quảng cáo", sum(
                     1 for r in rows if "không phải QC" in r.get("post", ""))),
                 ("Không rõ nguồn", sum(
                     1 for r in rows if "không rõ nguồn" in r.get("post", ""))),
                 ("Số post duy nhất sau chuẩn hoá",
                  len([k for k in theo_post if k.startswith("QC")]))]:
        dong(ws, [a, b])
    trong(ws)
    it = [k for k, v in theo_post.items() if len(v) < NGUONG_MAU]
    bang_co_do(ws, rows)
    khoi_canh_bao_chuan(ws, rows, mau_loc, extra=[
        "%d / %d post có dưới %d hội thoại → ⚠ chưa đủ mẫu, khuyến nghị bắt "
        "buộc là CHỜ THÊM DỮ LIỆU." % (len(it), len(theo_post), NGUONG_MAU),
        "BẪY GIÁ TRỊ: xếp hạng post chỉ bằng %HOT là quyết SAI ngân sách. "
        "Một post kéo 40 hội thoại hỏi khám đầy hơi trông thắng mọi post combo "
        "tầm soát trên bảng %HOT, nhưng giá trị thật thì ngược lại — dải giá "
        "chênh gần chín lần. PHẢI đọc kèm sheet \"Post × Nhóm giá trị\".",
        "BẪY CỜ ĐỎ: luật ghi đè ② đẩy MỌI ca cờ đỏ lên HOT. Post nào tình cờ "
        "kéo nhiều ca cờ đỏ sẽ có %HOT rất cao — nhưng đó không phải chất lượng "
        "quảng cáo, đó là gánh nặng y tế, và nhóm đó thường không chốt nhanh. "
        "Xếp hạng post phải dùng cột đã TRỪ CỜ ĐỎ, và tách TH-01 ra khỏi mọi "
        "bảng so sánh.",
    ])
    trong(ws)
    muc(ws, "Ba kết luận chính")
    for i in range(1, 4):
        dong(ws, ["%d." % i, "⚠ chưa viết — cần người/trợ lý đọc bảng rồi kết "
                             "luận, mỗi kết luận kèm một con số"], nen=CANH_BAO)
    hoan_thien(ws, freeze=False)   # sheet tong quan: nhieu khoi, khong freeze

    sheet_chu_giai(wb)

    # sheet 3: phan tang theo post
    ws = sheet(wb, "Phân tầng theo post")
    tieu_de(ws, "PHÂN TẦNG THEO POST",
            "Sắp xếp theo %HOT giảm dần, dòng ⚠ chưa đủ mẫu đẩy xuống cuối. "
            "ĐỌC KÈM sheet Post × Nhóm giá trị trước khi quyết ngân sách.")
    cot = ["Mã post", "Tên post (chuẩn hoá)", "Biến thể đã gom", "Dịch vụ",
           "Thông điệp chính", "Góc tiếp cận", "Số HT", "Tỷ lệ có SĐT",
           "HOT", "WARM", "COLD", "% HOT", "Điểm TB", "G1", "G2", "G3",
           "% G1", "Tầng chủ đạo", "Nhóm vấn đề chủ đạo", "Đủ mẫu?",
           "Rào cản nổi bật"]
    dong_tieu_de(ws, cot)
    bang = []
    for ten, hts in theo_post.items():
        m = len(hts)
        d = dem(hts, "do_nong")
        g = dem(hts, "nhom_gia_tri")
        vd = dem(hts, "van_de").most_common(1)
        rc = collections.Counter(x["ten"] for r in hts
                                 for x in r.get("rao_can", []))
        inf = ps.get(ten, {})
        bang.append((
            100.0 * d["HOT"] / m, m >= NGUONG_MAU,
            [inf.get("ma", "—"), ten,
             ", ".join(k for k, i in ps.items()
                       if i.get("gom") and i["gom"] == inf.get("ma")) or "—",
             inf.get("dich_vu", dich_vu), inf.get("headline", "⚠ chưa có"),
             inf.get("goc", "⚠ chưa điền"), m,
             pc(sum(1 for r in hts if co_sdt(r)), m),
             d["HOT"], d["WARM"], d["COLD"], pc(d["HOT"], m),
             round(sum(r.get("diem", 0) for r in hts) / float(m), 2),
             g["G1"], g["G2"], g["G3"], pc(g["G1"], m),
             d.most_common(1)[0][0] if m else "—",
             "%s %s" % (vd[0][0], VAN_DE_TEN.get(vd[0][0], "")) if vd else "—",
             du_mau(m),
             " · ".join("%s(%d)" % (k, v) for k, v in rc.most_common(3)) or "—"]))
    for _, ok, v in sorted(bang, key=lambda x: (not x[1], -x[0])):
        dong_nong(ws, v, v[17], cot_nong=18) if ok else dong(ws, v, nen=MO)
    hoan_thien(ws)

    # sheet 4: xep hang & khuyen nghi
    ws = sheet(wb, "Xếp hạng & khuyến nghị")
    tieu_de(ws, "XẾP HẠNG & KHUYẾN NGHỊ",
            "Năm mức. Mức \"TĂNG NGÂN SÁCH (giá trị cao)\" là mức RIÊNG của "
            "ngành tiêu hóa: post ít khách nhưng toàn khách V1 thì đáng tiền hơn "
            "post đông khách V3.")
    dong_tieu_de(ws, ["Hạng", "Mã post", "% HOT", "% G1", "Tỷ lệ có SĐT",
                      "Khuyến nghị", "Lý do", "Việc cần làm"])
    du = [(h, v) for h, ok, v in sorted(bang, key=lambda x: -x[0]) if ok]
    tb_hot = sum(h for h, _ in du) / len(du) if du else 0
    tb_v1 = (sum(float(v[16].replace("%", "").replace(",", ".")) for _, v in du)
             / len(du)) if du else 0
    for i, (h, v) in enumerate(du, start=1):
        v1 = float(v[16].replace("%", "").replace(",", "."))
        if h >= tb_hot and v1 >= tb_v1:
            kn, ly = "TĂNG NGÂN SÁCH", "%HOT và %G1 đều trên trung bình kỳ"
        elif v1 >= tb_v1 + 10:
            kn, ly = ("TĂNG NGÂN SÁCH (giá trị cao)",
                      "%HOT quanh trung bình nhưng %G1 cao rõ rệt — post này "
                      "kéo về khách combo tầm soát / can thiệp")
        elif h >= tb_hot * 0.8:
            kn, ly = "GIỮ NGUYÊN", "quanh mức trung bình kỳ"
        elif v[6] >= NGUONG_MAU * 2:
            kn, ly = ("SỬA THÔNG ĐIỆP",
                      "kéo được nhiều hội thoại nhưng tầng thấp")
        else:
            kn, ly = "XEM XÉT TẮT", "vừa ít hội thoại vừa tầng thấp"
        dong(ws, [i, v[0], v[11], v[16], v[7], kn, ly,
                  "⚠ chưa viết — nêu cụ thể sửa câu nào, thêm bằng chứng gì, "
                  "đổi CTA thành gì"],
             nen=TOT if kn.startswith("TĂNG") else None)
    for h, ok, v in sorted(bang, key=lambda x: -x[0]):
        if not ok:
            dong(ws, ["—", v[0], v[11], v[16], v[7], "CHỜ THÊM DỮ LIỆU",
                      "dưới %d hội thoại — con số %% không nói lên gì"
                      % NGUONG_MAU, "Chạy lại khi đủ mẫu"], nen=MO)
    hoan_thien(ws)

    # sheet 5: Post x Nhom gia tri  (sheet rieng cua nganh nha)
    ws = sheet(wb, "Post × Nhóm giá trị")
    tieu_de(ws, "⭐ POST × NHÓM GIÁ TRỊ — sheet quyết định ngân sách",
            "Đây là sheet quyết ngân sách, KHÔNG phải sheet Phân tầng. "
            "Post nào kéo về khách giá trị lớn.")
    dong_tieu_de(ws, ["Mã post", "Góc tiếp cận", "Số HT", "G1", "G2", "G3",
                      "% G1", "% HOT", "% HOT trong nhóm V1", "Nhận định"])
    r0 = None
    for _, ok, v in sorted(bang, key=lambda x: -float(
            x[2][16].replace("%", "").replace(",", "."))):
        hts = theo_post[v[1]]
        v1s = [r for r in hts if r.get("nhom_gia_tri") == "G1"]
        hv1 = pc(sum(1 for r in v1s if r.get("do_nong") == "HOT"),
                 len(v1s)) if v1s else "—"
        r = dong(ws, [v[0], v[5], v[6], v[13], v[14], v[15], v[16], v[11], hv1,
                      "⚠ chưa viết" if ok else "⚠ chưa đủ mẫu, không kết luận"],
                 nen=None if ok else MO)
        r0 = r0 or r
    if r0:
        nhiet(ws, r0, 4, ws.max_row, 6)
        cot_phu_vang(ws, r0, ws.max_row, 3)
        for c in (7, 8, 9):
            cot_phu_vang(ws, r0, ws.max_row, c)
    doc_nhanh(ws, [
        "⚠ chưa viết — nêu post nào nên TĂNG tiền dù %HOT thấp, kèm con số.",
        "⚠ chưa viết — nêu post nào %HOT cao nhưng toàn V3, tức đang mua lead rẻ.",
        "Màu nhiệt chỉ so sánh được trong cùng bảng này, không so với bảng khác.",
    ])
    hoan_thien(ws)

    # sheet 6: Goc tiep can -> tang
    ws = sheet(wb, "Góc tiếp cận → tầng")
    tieu_de(ws, "GÓC TIẾP CẬN → TẦNG",
            "Quy luật rút ra được. Chỉ kết luận khi tổng hội thoại của góc "
            "đó ≥ %d." % NGUONG_MAU)
    dong_tieu_de(ws, ["Góc tiếp cận", "Post đại diện", "Số HT gộp", "% HOT gộp",
                      "% G1 gộp", "Tầng thường kéo về",
                      "Nhóm vấn đề thường kéo về", "Vì sao", "Dùng khi nào"])
    GOC = ["Giá - ưu đãi - trả góp", "Công nghệ giảm đau", "Tình trạng cụ thể",
           "Giáo dục - giải đáp lo lắng", "Chuyên môn - bác sĩ - đối tác hãng",
           "Case thật / before-after", "Banner thông báo",
           "Gói gia đình - trẻ em"]
    theo_goc = collections.defaultdict(list)
    for ten, hts in theo_post.items():
        theo_goc[ps.get(ten, {}).get("goc") or "⚠ chưa điền"].extend(hts)
    for g in GOC + ["⚠ chưa điền"]:
        hts = theo_goc.get(g, [])
        m = len(hts)
        if not m:
            dong(ws, [g, "—", 0, "—", "—", "—", "—",
                      "⚠ không có post nào thuộc góc này trong kỳ", "—"], nen=MO)
            continue
        d, gt = dem(hts, "do_nong"), dem(hts, "nhom_gia_tri")
        vd = dem(hts, "van_de").most_common(1)
        dong(ws, [g, ", ".join(sorted({ps.get(k, {}).get("ma", "—")
                                       for k, v in theo_post.items()
                                       if ps.get(k, {}).get("goc") == g})) or "—",
                  m, pc(d["HOT"], m), pc(gt["G1"], m),
                  d.most_common(1)[0][0],
                  "%s %s" % (vd[0][0], VAN_DE_TEN.get(vd[0][0], "")) if vd else "—",
                  "⚠ chưa viết" if m >= NGUONG_MAU
                  else "⚠ chưa đủ mẫu (%d < %d), không kết luận" % (m, NGUONG_MAU),
                  "⚠ chưa viết"], nen=None if m >= NGUONG_MAU else MO)
    hoan_thien(ws)

    # sheet 7: Rao can theo post
    ws = sheet(wb, "Rào cản theo post")
    tieu_de(ws, "RÀO CẢN THEO POST",
            "Post nào đẻ ra rào cản gì. Dùng để biết post nào cần SỬA THÔNG "
            "ĐIỆP TỪ GỐC, post nào chỉ cần trang bị trước kịch bản cho trực page.")
    dong_tieu_de(ws, ["Mã post", "Rào cản", "Nhóm (SỢ/NGỜ/NGẠI)", "Số ca",
                      "% trên tổng HT của post", "Hàm ý cho thông điệp",
                      "Kịch bản cần chuẩn bị"])
    for ten, hts in sorted(theo_post.items(), key=lambda x: -len(x[1])):
        m = len(hts)
        c = collections.Counter((x["ma"], x["nhom"], x["ten"])
                                for r in hts for x in r.get("rao_can", []))
        if not c:
            dong(ws, [ps.get(ten, {}).get("ma", "—"), "— không ghi nhận rào cản",
                      "—", 0, "—", "—", "—"])
            continue
        for (ma, nh, tenrc), v in c.most_common():
            dong(ws, [ps.get(ten, {}).get("ma", "—"), "%s %s" % (ma, tenrc), nh,
                      v, pc(v, m), "⚠ chưa viết",
                      _ten_kb(KHUNG_ND.get(ma, ("", "—"))[1])])
    trong(ws)
    dong(ws, ["⚠ QUY LUẬT ĐÁNG CHÚ Ý", "Post nói nhiều về giá thường đẻ ra rào "
              "cản NGỜ VẬT LIỆU (L6.7) — khách nghĩ \"rẻ thế thì trụ gì\". "
              "Nếu thấy quy luật này trong dữ liệu, nói thẳng ở sheet Tổng quan.",
              "", "", "", "", ""], nen=CANH_BAO)
    hoan_thien(ws)

    # sheet 8: nhiet Van de rang x Do nong  (co cot % HOT*)
    ws = sheet(wb, "① Nhiệt Vấn đề × Nóng")
    tieu_de(ws, "① BIỂU ĐỒ NHIỆT — VẤN ĐỀ RĂNG × ĐỘ NÓNG",
            "⚠ BẮT BUỘC đọc cột % HOT* chứ không đọc % HOT. Xem ghi chú dưới bảng.")
    dong_tieu_de(ws, ["Nhóm vấn đề", "HOT", "WARM", "COLD", "Tổng HT",
                      "% HOT", "% HOT*", "% cho số"])
    r0 = None
    for ma in VAN_DE_MA:
        hts = [r for r in rows if r.get("van_de") == ma]
        if not hts:
            continue
        m = len(hts)
        d = dem(hts, "do_nong")
        h4 = sum(1 for r in hts if r.get("nong4") == "HOT*")
        r = dong(ws, ["%s %s" % (ma, VAN_DE_TEN[ma]), d["HOT"], d["WARM"],
                      d["COLD"], m, pc(d["HOT"], m), pc(h4, m),
                      pc(sum(1 for r2_ in hts if co_sdt(r2_)), m)],
                 nen=MO if m < NGUONG_MAU else None)
        r0 = r0 or r
    if r0:
        nhiet(ws, r0, 2, ws.max_row, 4)
        for c in (5, 6, 7, 8):
            cot_phu_vang(ws, r0, ws.max_row, c)
    trong(ws)
    r = dong(ws, ["⚠ LUẬT CHỐNG LẶP VÒNG — đọc trước khi kết luận",
                  "Tín hiệu ① của thang chấm chính là \"nêu triệu chứng/chỉ "
                  "định cụ thể\". Bảng này lại chia nhóm THEO VẤN ĐỀ, nên mọi "
                  "nhóm có vấn đề cụ thể đã được cộng sẵn 1 điểm — trong khi "
                  "TH-12 hỏi chung thì không. Vì vậy cột % HOT bị LẶP VÒNG và "
                  "KHÔNG so sánh được giữa các nhóm.\n"
                  "VÀ: dòng TH-01 (cờ đỏ) luôn 100% HOT do luật ghi đè ② — "
                  "phải TÁCH RA khỏi mọi so sánh, con số đó chỉ phản ánh chính "
                  "luật ghi đè.", "", "", "", "", "", ""],
             nen=CANH_BAO)
    dong(ws, ["→ Cột dùng được", "% HOT* — chấm lại chỉ bằng 4 tín hiệu "
              "②③④⑤, đạt ≥3/4 tính HOT*.", "", "", "", "", "", ""])
    dong(ws, ["→ Nếu bỏ tín hiệu ① mà chênh lệch biến mất",
              "PHẢI NÓI THẲNG LÀ KHÔNG CÓ BẰNG CHỨNG. Không được giữ kết luận "
              "cũ.", "", "", "", "", "", ""], nen=CANH_BAO)
    doc_nhanh(ws, ["⚠ chưa viết — 2–4 điều rút ra, mỗi điều kèm con số, và nói "
                   "rõ đã dùng cột % HOT* chứ không dùng % HOT.",
                   "Ô dưới %d ca thì không kết luận được." % NGUONG_MAU])
    hoan_thien(ws)

    # sheet 9: nhiet Goc x Van de
    ws = sheet(wb, "② Nhiệt Góc × Vấn đề")
    tieu_de(ws, "② BIỂU ĐỒ NHIỆT — GÓC TIẾP CẬN × VẤN ĐỀ RĂNG",
            "Mỗi góc quảng cáo kéo về nhóm vấn đề nào. Dùng để chọn góc khi "
            "viết content mới.")
    ma_co = [m for m in VAN_DE_MA if any(r.get("van_de") == m for r in rows)]
    dong_tieu_de(ws, ["Góc tiếp cận"] + ma_co + ["Tổng"])
    r0 = None
    for g in GOC + ["⚠ chưa điền"]:
        hts = theo_goc.get(g, [])
        if not hts:
            continue
        d = dem(hts, "van_de")
        r = dong(ws, [g] + [d[m] for m in ma_co] + [len(hts)])
        r0 = r0 or r
    if r0:
        nhiet(ws, r0, 2, ws.max_row, 1 + len(ma_co))
        cot_phu_vang(ws, r0, ws.max_row, 2 + len(ma_co))
    doc_nhanh(ws, ["⚠ chưa viết — góc nào kéo về nhóm giá trị lớn (TH-03 tầm "
                   "soát, TH-07 polyp), góc nào chỉ kéo về TH-09 hỏi chung.",
                   "Kiểm riêng: góc HÙ BỆNH có kéo về nhiều L6.8 (né kết quả) "
                   "không — post càng đáng sợ thì inbox càng nhiều mà đặt lịch "
                   "càng ít."])
    hoan_thien(ws)

    # sheet 10: nhiet Van de x Rao can
    ws = sheet(wb, "③ Nhiệt Vấn đề × Rào cản")
    tieu_de(ws, "③ BIỂU ĐỒ NHIỆT — VẤN ĐỀ RĂNG × RÀO CẢN",
            "Một hội thoại có thể mang nhiều rào cản → tổng theo hàng LỚN HƠN "
            "số hội thoại là đúng. Dùng để biết nên sửa thông điệp từ gốc hay "
            "chỉ cần trang bị trước kịch bản.")
    rc_ma = [m for m in RAO_CAN_TEN if any(
        m in ma_rao_can(r) for r in rows)]
    dong_tieu_de(ws, ["Nhóm vấn đề"] + ["%s %s" % (m, RAO_CAN_TEN[m][1])
                                        for m in rc_ma] + ["Tổng lượt"])
    r0 = None
    for ma in ma_co:
        hts = [r for r in rows if r.get("van_de") == ma]
        v = [sum(1 for r in hts if m in ma_rao_can(r)) for m in rc_ma]
        r = dong(ws, ["%s %s" % (ma, VAN_DE_TEN[ma])] + v + [sum(v)])
        r0 = r0 or r
    if r0 and rc_ma:
        nhiet(ws, r0, 2, ws.max_row, 1 + len(rc_ma))
        cot_phu_vang(ws, r0, ws.max_row, 2 + len(rc_ma))
    doc_nhanh(ws, ["⚠ chưa viết — nhóm vấn đề nào vướng L6.7 (ngại tiền mê), "
                   "L6.8 (né kết quả), L6.9 (ngờ vệ sinh dây soi) nhiều nhất. "
                   "Ba rào cản này THV đều có bằng chứng để gỡ, nên khoảng cách "
                   "giữa 'mình có bằng chứng' và 'mình có nói ra' là phát hiện "
                   "đáng giá nhất của bảng này."])
    hoan_thien(ws)

    # sheet 11: nhiet Post x Do nong
    ws = sheet(wb, "④ Nhiệt Post × Nóng")
    tieu_de(ws, "④ BIỂU ĐỒ NHIỆT — POST × ĐỘ NÓNG")
    dong_tieu_de(ws, ["Mã post", "Tên post", "HOT", "WARM", "COLD", "Tổng HT",
                      "% HOT", "Đủ mẫu?"])
    r0 = None
    for ten, hts in sorted(theo_post.items(), key=lambda x: -len(x[1])):
        m = len(hts)
        d = dem(hts, "do_nong")
        r = dong(ws, [ps.get(ten, {}).get("ma", "—"), ten, d["HOT"], d["WARM"],
                      d["COLD"], m, pc(d["HOT"], m), du_mau(m)],
                 nen=MO if m < NGUONG_MAU else None)
        r0 = r0 or r
    if r0:
        nhiet(ws, r0, 3, ws.max_row, 5)
        for c in (6, 7, 8):
            cot_phu_vang(ws, r0, ws.max_row, c)
    doc_nhanh(ws, ["⚠ chưa viết.",
                   "Post dưới %d hội thoại: màu vẫn hiện nhưng KHÔNG kết luận "
                   "được." % NGUONG_MAU])
    hoan_thien(ws)

    # sheet 12: mau hoi thoai thuc te
    ws = sheet(wb, "Mẫu hội thoại thực tế")
    tieu_de(ws, "MẪU HỘI THOẠI THỰC TẾ — mỗi nhóm vấn đề tối đa 3 ca",
            "Phần giúp người đọc kiểm tra máy phân loại có đúng không. "
            "Bảng số mà không có ví dụ thì không ai tin được. "
            "⚠ CHE SỐ ĐIỆN THOẠI trong phần trích.")
    dong_tieu_de(ws, ["Nhóm vấn đề", "HT#", "Độ nóng", "Nhóm giá trị", "Có SĐT",
                      "Post", "Trích lời khách"])
    for ma in ma_co:
        for r in [x for x in rows if x.get("van_de") == ma][:3]:
            dong_nong(ws, ["%s %s" % (ma, VAN_DE_TEN[ma]), "HT#%d" % r["stt"],
                           r.get("do_nong", ""), r.get("nhom_gia_tri", ""),
                           "Có" if co_sdt(r) else "Không",
                           ps.get(r.get("post", ""), {}).get(
                               "ma", r.get("post", "")),
                           "⚠ chưa trích — dán 1–2 câu khách gõ, CHE SỐ ĐIỆN THOẠI"],
                          r.get("do_nong", ""), cot_nong=3)
    hoan_thien(ws)

    # sheet 13: du lieu tho
    ws = sheet(wb, "Dữ liệu thô")
    tieu_de(ws, "DỮ LIỆU THÔ — để kiểm chứng lại",
            "Bắt buộc có sheet này. Không có thì không ai kiểm được con số ở "
            "sheet Phân tầng.")
    dong_tieu_de(ws, ["STT HT", "Tên KH", "Ngày", "Thẻ nguồn gốc (nguyên văn)",
                      "Mã post sau chuẩn hoá", "Có SĐT", "Bitmask tín hiệu",
                      "Ghi đè?", "Độ nóng", "Nhóm vấn đề", "Nhóm giá trị",
                      "L-code"])
    for r in rows:
        dong(ws, [r["stt"], r.get("ten", ""), r.get("ngay", ""),
                  r.get("the", "") or "— không có thẻ",
                  ps.get(gom(r), {}).get("ma", gom(r)),
                  "Có" if co_sdt(r) else "Không", "[%s]" % r.get("bitmask", ""),
                  r.get("ghi_de", "") or "—", r.get("do_nong", ""),
                  r.get("van_de", ""), r.get("nhom_gia_tri", ""),
                  r.get("l_code", "")])
    hoan_thien(ws)

    return [ghi(wb, out_dir, "THV_PhanTang_QuangCao_%s.xlsx" % _slug(ky))]


# ------------------------------------------------------------------- R3

TIEU_CHI = [
    ("①", "Phản hồi ≤ 2 phút",
     "Chênh lệch dấu thời gian tin khách → tin NV đầu tiên ≤ 2'"),
    ("②", "Gọi đúng tên dịch vụ / triệu chứng theo post khách bấm vào",
     "Tin mở nhắc đúng dịch vụ, không hỏi chung \"cần tư vấn gì\""),
    ("③", "🚩 SÀNG CỜ ĐỎ",
     "Có hỏi hoặc có nhận ra dấu hiệu cờ đỏ; ca có cờ đỏ được mời khám sớm và "
     "ghi nhận chuyển bác sĩ. BỎ SÓT = không đạt tiêu chí này VÀ trừ nặng ở ⑨"),
    ("④", "Thu đủ 5 thông tin",
     "Triệu chứng + bao lâu · 🚩 có cờ đỏ không · đã khám/soi ở đâu chưa và có "
     "kết quả không · BỆNH NỀN & THUỐC ĐANG DÙNG · thời gian dự kiến"),
    ("⑤", "Tạo tin cậy bằng bằng chứng, đúng rào cản khách mang",
     "≥1 bằng chứng thật (chuyên gia Bạch Mai · Fujifilm VP-7000 + AI · GP Sở "
     "Y tế · bác sĩ gây mê theo dõi riêng · bảng giá công khai), không chỉ tính từ"),
    ("⑥", "DẶN CHUẨN BỊ khi mời khám / khi đã có lịch",
     "Có nhắc việc chuẩn bị để soi được luôn nếu bác sĩ chỉ định. Dữ liệu không "
     "tới mốc có lịch → ⚠ không đo được, KHÔNG cho 0 oan"),
    ("⑦", "Xin số có lý do có lợi cho khách",
     "\"để bác sĩ xem trước và sắp lịch đúng buổi anh/chị tiện\". "
     "❌ \"để gửi ưu đãi\""),
    ("⑧", "Phiếu bàn giao đủ 14 trường",
     "Có 🚩 cờ đỏ · bệnh nền · kết quả nơi khác. Dữ liệu không có phần ghi chú "
     "→ ⚠ không đo được, KHÔNG cho 0 oan"),
    ("⑨", "Không vi phạm an toàn & pháp lý",
     "Không từ cấm · 🚩 KHÔNG TRẤN AN CA CỜ ĐỎ · không chẩn đoán/loại trừ bệnh · "
     "không đọc kết quả · không tư vấn thuốc · không hứa chắc tiền mê · không "
     "báo giá thiếu điều kiện. VI PHẠM → TOÀN HỘI THOẠI 0 ĐIỂM"),
    ("⑩", "Nêu rõ bước tiếp theo",
     "Ai gọi · số nào · lúc mấy giờ (bước B5)"),
]


def r3(rows, ky, dich_vu, out_dir, mau_loc=None):
    n = len(rows)
    tc = [r for r in rows if r.get("tu_cam_nv")]
    co_gio = sum(1 for r in rows if r.get("ngay"))

    cd_all = [r for r in rows if r.get("co_do")]
    cd_sai = [r for r in rows if r.get("tran_an_sai_nv")]

    wb = so_moi()
    ws = sheet(wb, "Cờ đỏ")
    tieu_de(ws, "🚩 CỜ ĐỎ — NHẬN RA HAY BỎ SÓT",
            "SHEET SỐ 1. Đọc trước mọi sheet khác. Một ca nôn ra máu bị trả lời "
            "\"chị uống thuốc dạ dày xem sao\" là chuyện nặng hơn mọi điểm trung "
            "bình trong báo cáo này.")
    bang_co_do(ws, rows)
    trong(ws)
    dong(ws, ["⚠ Script chỉ bắt được CÂU TRẤN AN bằng từ khoá. Việc nhân viên "
              "CÓ NHẬN RA cờ đỏ hay không (có hỏi thêm, có mời khám sớm, có nói "
              "sẽ chuyển bác sĩ) thì cần NGƯỜI ĐỌC từng ca ở cột bên."])
    dong(ws, ["⚠ Ca bị trấn an sai thì việc cần làm là GỌI LẠI KHÁCH ĐÓ HÔM NAY, "
              "không phải đọc con số ở cuối tháng."])
    hoan_thien(ws)

    ws = sheet(wb, "Tổng quan")
    tieu_de(ws, "R3 · CHẤT LƯỢNG TƯ VẤN & ĐÀO TẠO — %s" % dich_vu,
            "Kỳ %s · %d hội thoại · lập ngày %s" % (ky, n, _hom_nay()))
    khoi_canh_bao(ws, "FILE NÀY LÀ KHUNG — chưa phải bảng điểm hoàn chỉnh", [
        "Bảng chấm 10 tiêu chí cần ĐỌC HIỂU từng hội thoại. Script không chấm "
        "được, nên các ô tiêu chí để ⚠ cho người hoặc trợ lý điền.",
        "Phần script ĐÃ làm được và đã điền: quét 🚩 CỜ ĐỎ cho toàn bộ file · "
        "phát hiện câu TRẤN AN SAI trong ca có cờ đỏ · phát hiện TỪ CẤM trong "
        "lời nhân viên (tiêu chí ⑨) · phát hiện ca khách nêu rào cản mà NV "
        "không đưa bằng chứng nào của THV (tiêu chí ⑤).",
        "🚩 Sheet CỜ ĐỎ đọc TRƯỚC sheet này. Mốc nhận diện cờ đỏ là 100%, "
        "không thương lượng — đây là mốc duy nhất của hệ này không chờ THV chốt.",
        "Tiêu chí ⑧ cần phần ghi chú bàn giao nội bộ, tiêu chí ⑥ cần dữ liệu "
        "tới mốc khách đã có lịch. Thiếu → ghi ⚠ không đo được, KHÔNG cho 0 "
        "điểm oan, và chuẩn đạt phải đổi tương ứng.",
        "🔒 FILE NÀY CÓ TÊN NGƯỜI THẬT. Dùng cho ĐÀO TẠO và ĐỊNH TUYẾN. "
        "Không đưa vào nội dung gửi khách, không chia sẻ ra ngoài nhóm quản lý.",
    ])
    trong(ws)
    muc(ws, "Dữ liệu đọc được")
    dong_tieu_de(ws, ["Chỉ số", "Giá trị", "Ghi chú"])
    dong(ws, ["Hội thoại chấm được", n, ""])
    dong(ws, ["Có dấu thời gian", co_gio,
              "Cần cho tiêu chí ①" if co_gio == n
              else "⚠ thiếu %d ca → tiêu chí ① không đo được cho các ca đó"
              % (n - co_gio)])
    dong(ws, ["Có tên phụ trách", sum(1 for r in rows if r.get("nv")),
              "Cần cho sheet Theo người phụ trách"])
    dong(ws, ["Có phần ghi chú bàn giao", 0,
              "⚠ không đo được tiêu chí ⑧ — chuẩn đạt đổi tương ứng"])
    dong(ws, ["🚩 Ca có dấu hiệu cờ đỏ", len(cd_all),
              "Xem sheet Cờ đỏ. Mốc nhận diện: 100%"],
         nen=CANH_BAO if cd_all else TOT)
    dong(ws, ["🚩 Ca bị TRẤN AN SAI", len(cd_sai),
              "Lỗi nặng nhất của hệ. %s"
              % (", ".join("HT#%d" % r["stt"] for r in cd_sai) or "không có")],
         nen=CANH_BAO if cd_sai else TOT)
    dong(ws, ["Điểm trung bình toàn kỳ", CD,
              "⚠ chờ chấm — xem sheet Chấm từng hội thoại"])
    dong(ws, ["% hội thoại đạt ≥8/10", CD, "⚠ chờ chấm"])
    dong(ws, ["Số hội thoại bị 0 điểm (vi phạm ⑨)", len(tc),
              "Script phát hiện được: %s"
              % (", ".join("HT#%d" % r["stt"] for r in tc) or "không có")],
         nen=CANH_BAO if tc else TOT)
    trong(ws)
    muc(ws, "Ba kết luận chính")
    for i in range(1, 4):
        dong(ws, ["%d." % i, "⚠ chưa viết — mỗi kết luận một con số"],
             nen=CANH_BAO)
    hoan_thien(ws)

    sheet_chu_giai(wb, them=[
        ("1 / 0 / ⚠", "Trong bảng chấm: 1 = đạt · 0 = không đạt · "
         "⚠ = không đo được từ dữ liệu hiện có (KHÔNG phải 0 điểm).",
         "Sheet Chấm từng hội thoại"),
        ("Nhóm A/B/C/D", "A hạt nhân, không bỏ sót cờ đỏ (làm mentor) · "
         "B yếu khâu chốt (thiếu ⑥ dặn chuẩn bị, thiếu ⑩) · C yếu khâu bằng "
         "chứng (thiếu ⑤) · D YẾU KHÂU AN TOÀN (có ca bỏ sót cờ đỏ hoặc vi "
         "phạm ⑨) — nhóm D ưu tiên đào tạo TRƯỚC mọi nhóm khác, bất kể điểm "
         "trung bình cao hay thấp.", "Sheet Theo người phụ trách"),
        ("M0 … M5", "Sáu học phần: M0 🚩 sàng cờ đỏ & giới hạn chuyên môn "
         "(LUÔN Ở TUẦN 1 nếu có ca cờ đỏ bị xử lý sai) · M1 mở hội thoại · "
         "M2 bằng chứng ngành tiêu hóa · M3 xin số & xác thực · M4 chốt lịch + "
         "dặn chuẩn bị · M5 phân loại & bàn giao.", "Sheet Kế hoạch đào tạo"),
    ])

    ws = sheet(wb, "Chấm từng hội thoại")
    tieu_de(ws, "CHẤM TỪNG HỘI THOẠI — 10 TIÊU CHÍ",
            "Ghi 1 (đạt) · 0 (không đạt) · ⚠ (không đo được). "
            "Cột trích dẫn BẮT BUỘC có với mọi tiêu chí bị 0 và mọi lỗi cấm. "
            "Bảng điểm không có trích dẫn thì nhân viên không phục và trưởng "
            "nhóm không đào tạo được.")
    dong_tieu_de(ws, ["STT", "Tên KH", "Ngày", "Phụ trách", "Nhóm vấn đề",
                      "Nhóm giá trị", "Độ nóng"]
                 + [k for k, _, _ in TIEU_CHI]
                 + ["Tổng điểm", "Đạt?", "Lỗi cấm mắc phải",
                    "Trượt câu hỏi ngầm?", "Trích dẫn bằng chứng", "Ghi chú"])
    for r in rows:
        vp = r.get("tu_cam_nv") or []
        thieu_hang = ma_rao_can(r) and not r.get("bang_chung_nv")
        o = ["⚠"] * 10
        o[8] = 0 if (vp or r.get("tran_an_sai_nv")) else "⚠"
        if r.get("co_do"):
            # tieu chi ③ sang co do: script chi biet NV co tran an sai hay khong
            o[2] = 0 if r.get("tran_an_sai_nv") else "⚠"
        if thieu_hang:
            o[4] = 0                        # ⑤ bo mat bang chung
        o[6] = "⚠"                          # ⑦ khong co ghi chu
        o[7] = "⚠"                          # ⑧ khong co phieu
        loi = []
        if vp:
            loi.append("Từ cấm: " + ", ".join(vp))
        if thieu_hang:
            loi.append("Bỏ mất bằng chứng đối tác hãng khi khách ngờ vật liệu")
        dong(ws, [r["stt"], r.get("ten", ""), r.get("ngay", ""), r.get("nv", ""),
                  r.get("van_de", ""), r.get("nhom_gia_tri", ""),
                  r.get("do_nong", "")] + o
             + ["0 (vi phạm ⑨)" if vp else "⚠ chờ chấm",
                "KHÔNG ĐẠT" if vp else "⚠ chờ chấm",
                " · ".join(loi) or "⚠ chờ đọc",
                "⚠ chờ đọc — cần đọc hiểu, script không bắt được",
                "⚠ BẮT BUỘC trích nguyên văn cho mọi tiêu chí bị 0"
                if (vp or thieu_hang) else "⚠ chờ chấm",
                "⚠"],
             nen=CANH_BAO if vp else None)
    hoan_thien(ws)

    ws = sheet(wb, "Tiêu chí nào đang hổng")
    tieu_de(ws, "TIÊU CHÍ NÀO ĐANG HỔNG",
            "Sắp xếp theo % đạt tăng dần — tiêu chí hổng nhất lên đầu. "
            "Cột \"Hậu quả\" phải dẫn SỐ THẬT.")
    dong_tieu_de(ws, ["Tiêu chí", "Số HT đạt", "Số HT không đạt",
                      "Số HT không đo được", "% đạt", "Khâu phễu bị ảnh hưởng",
                      "Hậu quả thấy được trong dữ liệu", "Học phần cần dạy"])
    khau = {"①": "Mở hội thoại", "②": "Mở hội thoại", "③": "Khám phá nhu cầu",
            "④": "Tạo tin cậy", "⑤": "Xin số", "⑥": "Xin số",
            "⑦": "Bàn giao", "⑧": "Bàn giao", "⑨": "Pháp lý",
            "⑩": "Kết nối (B5)"}
    hp = {"①": "M1", "②": "M1", "③": "M0", "④": "M1", "⑤": "M2", "⑥": "M4",
          "⑦": "M3", "⑧": "M5", "⑨": "M0", "⑩": "M4"}
    for k, ten, _ in TIEU_CHI:
        if k == "⑨":
            dong(ws, ["%s %s" % (k, ten), n - len(tc), len(tc), 0,
                      pc(n - len(tc), n), khau[k],
                      "%d ca vi phạm → mỗi ca là 0 điểm toàn hội thoại và là "
                      "RỦI RO PHÁP LÝ, không phải lỗi kỹ năng" % len(tc),
                      hp[k]], nen=CANH_BAO if tc else TOT)
        elif k in ("⑦", "⑧"):
            dong(ws, ["%s %s" % (k, ten), 0, 0, n, CD, khau[k],
                      "⚠ không đo được — dữ liệu không có phần ghi chú bàn giao",
                      hp[k]])
        else:
            dong(ws, ["%s %s" % (k, ten), CD, CD, CD, CD, khau[k],
                      "⚠ chờ chấm — dẫn số thật, ví dụ \"28 HT thiếu B5 → "
                      "19 ca trong đó thành L5.3 gọi không bắt máy\"", hp[k]])
    hoan_thien(ws)

    ws = sheet(wb, "Theo người phụ trách")
    tieu_de(ws, "🔒 THEO NGƯỜI PHỤ TRÁCH — DỮ LIỆU NHÂN SỰ NỘI BỘ",
            "Dùng cho ĐÀO TẠO và ĐỊNH TUYẾN. Khi trình bày cho nhóm, ẩn sheet "
            "này hoặc chỉ nói theo nhóm A/B/C/D, không đọc tên kèm điểm trước "
            "cả nhóm. NV dưới %d hội thoại: không xếp nhóm, không kết luận."
            % NGUONG_MAU)
    dong_tieu_de(ws, ["Tên NV", "Số HT", "Điểm TB", "% đạt ≥8/10",
                      "Số HT bị 0 điểm", "Tỷ lệ xin được số",
                      "Tiêu chí mạnh nhất", "Tiêu chí yếu nhất", "Nhóm (A/B/C/D)",
                      "Học phần cần học"])
    for nv, hts in sorted(collections.Counter(
            r.get("nv", "—") for r in rows).items(), key=lambda x: -x[1]):
        hs = [r for r in rows if r.get("nv") == nv]
        m = len(hs)
        vp = [r for r in hs if r.get("tu_cam_nv")]
        thieu = m < NGUONG_MAU
        dong(ws, [nv, m, CD, CD, len(vp),
                  pc(sum(1 for r in hs if co_sdt(r)), m),
                  "⚠ chờ chấm", "⚠ chờ chấm",
                  "⚠ chưa đủ mẫu (%d < %d)" % (m, NGUONG_MAU) if thieu
                  else "⚠ chờ chấm",
                  "M0 (có %d ca vi phạm ngôn từ / an toàn)" % len(vp) if vp
                  else "⚠ chờ chấm"],
             nen=MO if thieu else (CANH_BAO if vp else None))
    hoan_thien(ws)

    ws = sheet(wb, "Kế hoạch đào tạo 4 tuần")
    tieu_de(ws, "KẾ HOẠCH ĐÀO TẠO 4 TUẦN",
            "Chỉ đưa vào học phần nào mà DỮ LIỆU cho thấy đang hổng. "
            "Không rải đều. Học phần không dẫn được số thì không đưa vào.")
    dong_tieu_de(ws, ["Học phần", "Nội dung", "Vì sao cần (dẫn số từ sheet 4)",
                      "Người học", "Mentor đề xuất", "Tuần",
                      "Cách đo kết quả"])
    hoc_phan = [
        ("M0", "🚩 Sàng cờ đỏ & giới hạn chuyên môn — 6 dấu hiệu CĐ · câu hỏi "
               "sàng bằng lời thường · xử lý ca cờ đỏ (mời khám sớm, chuyển bác "
               "sĩ, KHÔNG trấn an, KHÔNG nêu giá) · bốn điều tuyệt đối không "
               "làm: chẩn đoán, loại trừ bệnh, đọc kết quả, tư vấn thuốc"),
        ("M1", "Mở hội thoại — phản hồi 2' · chào theo đúng dịch vụ · "
               "5 câu khám phá (có sàng cờ đỏ và bệnh nền)"),
        ("M2", "Bằng chứng ngành tiêu hóa — chuyên gia Bạch Mai · hệ Fujifilm "
               "+ AI · xử lý \"soi có đau không\" (KHÔNG nói \"không đau\") · "
               "xử lý \"mê có hại không\" · xử lý \"dây soi có sạch không\""),
        ("M3", "Xin số & xác thực — xin có lý do · kiểm Zalo · hỏi khung giờ · "
               "nhắn xác nhận"),
        ("M4", "Chốt lịch + DẶN CHUẨN BỊ — xử lý 9 lý do từ chối · CTA đến khám "
               "(bác sĩ quyết định có soi) · nhắc mở cả Chủ nhật · nhận diện "
               "L6.8 né kết quả và KHÔNG gửi ưu đãi cho nhóm đó"),
        ("M5", "Phân loại & bàn giao — HOT/WARM/COLD · nhóm giá trị G · "
               "🚩 cờ đỏ · phiếu 14 trường"),
    ]
    ngo = [r for r in rows if ma_rao_can(r)]
    ngo_tr = [r for r in ngo if not r.get("bang_chung_nv")]
    cd_sai = [r for r in rows if r.get("tran_an_sai_nv")]
    for ma, nd in hoc_phan:
        if ma == "M0":
            vs = ("%d ca có dấu hiệu cờ đỏ trong kỳ, trong đó %d ca bị TRẤN AN "
                  "SAI. Mốc nhận diện cờ đỏ là 100%%, không thương lượng."
                  % (len([r for r in rows if r.get("co_do")]), len(cd_sai)))
            nguoi = ", ".join(sorted({r.get("nv", "") for r in cd_sai})) or "—"
            do = ("Tỷ lệ nhận diện cờ đỏ, mục tiêu 100%. "
                  "Số ca bị trấn an sai, mục tiêu 0.")
            dong(ws, [ma, nd, vs, nguoi or "cả nhóm",
                      "⚠ chờ chọn — ưu tiên người phụ trách chuyên môn",
                      "TUẦN 1 — bắt buộc nếu có bất kỳ ca bị xử lý sai",
                      do], nen=CANH_BAO)
        elif ma == "M2":
            vs = ("%d ca vi phạm từ cấm · %d/%d ca khách nêu rào cản mà NV "
                  "KHÔNG đưa bằng chứng nào của THV — chỉ dùng tính từ"
                  % (len(tc), len(ngo_tr), len(ngo)))
            nguoi = ", ".join(sorted({r.get("nv", "") for r in tc + ngo_tr})) or "—"
            do = ("Tỷ lệ ca có rào cản mà NV đưa được bằng chứng, mục tiêu ≥70%. "
                  "Số ca vi phạm từ cấm, mục tiêu 0.")
            dong(ws, [ma, nd, vs, nguoi, "⚠ chờ chọn — người có điểm ⑤ cao nhất",
                      "Tuần 2", do], nen=CANH_BAO)
        else:
            dong(ws, [ma, nd, "⚠ chờ chấm — chỉ dạy nếu sheet 4 cho thấy hổng",
                      "⚠ chờ chấm", "⚠ chờ chọn", "⚠", "⚠ nêu con số sẽ đo lại "
                      "sau 4 tuần"])
    hoan_thien(ws)

    ws = sheet(wb, "Rủi ro pháp lý")
    tieu_de(ws, "⚠ RỦI RO PHÁP LÝ — ĐỌC SHEET NÀY TRƯỚC MỌI SHEET KHÁC",
            "Một câu \"cam kết 100%\" hoặc một chữ \"chính hãng\" gắn sai trong "
            "inbox là rủi ro pháp lý ngành y tế, không phải lỗi kỹ năng.")
    dong_tieu_de(ws, ["STT HT", "Ngày", "Phụ trách", "Loại vi phạm",
                      "Trích nguyên văn", "Mức rủi ro", "Việc cần làm"])
    if not tc:
        dong(ws, ["—", "—", "—",
                  "Không phát hiện vi phạm trong %d hội thoại đã quét" % n,
                  "—", "—", "Vẫn cần người đọc lại: script chỉ bắt được từ cấm "
                  "viết đúng chính tả, không bắt được chốt giá cứng hay chẩn "
                  "đoán qua tin nhắn"], nen=TOT)
    for r in tc:
        dong(ws, [r["stt"], r.get("ngay", ""), r.get("nv", ""),
                  "Từ cấm: " + ", ".join(r["tu_cam_nv"]),
                  "⚠ BẮT BUỘC dán nguyên văn câu vi phạm",
                  "CAO", "Gỡ câu đó khỏi mẫu đang dùng · đào tạo M2 · "
                  "kiểm lại các hội thoại khác của người này"], nen=CANH_BAO)
    trong(ws)
    muc(ws, "Loại vi phạm script KHÔNG bắt được — phải người đọc")
    for t in ["🚩 TRẤN AN MỘT CA CÓ CỜ ĐỎ — script bắt được câu trấn an nhưng "
              "không chắc ngữ cảnh; người phải đọc lại từng ca ở sheet Cờ đỏ",
              "Chẩn đoán hoặc LOẠI TRỪ bệnh qua tin nhắn (\"không phải ung thư "
              "đâu\", \"chỉ là viêm thôi\")",
              "Đọc kết quả nội soi / xét nghiệm / giải phẫu bệnh qua inbox",
              "Tư vấn thuốc, liều, phác đồ — kể cả phác đồ diệt HP",
              "Hứa chắc tiền mê được khi chưa biết bệnh nền",
              "Báo giá mà không nói ba điều kiện (ai thực hiện · có tiền mê "
              "không · phụ phí chỉ khi có chỉ định)",
              "Nêu tên bác sĩ ngoài danh sách đã duyệt",
              "Hứa có cơ sở gần khách — THV chỉ có 139 Đại La, Hà Nội"]:
        dong(ws, ["⚠", "", "", t, "", "CAO", "Cần đọc hiểu — xem sheet Chấm "
                  "từng hội thoại, cột tiêu chí ⑨"])
    hoan_thien(ws)

    return [ghi(wb, out_dir, "THV_ChatLuongTuVan_%s.xlsx" % _slug(ky))]


# ------------------------------------------------------------------- R4

def r4(rows, ky, dich_vu, out_dir, so_lieu=None, mau_loc=None):
    n = len(rows)
    sl = so_lieu or {}
    wb = so_moi()

    def phieu(ten):
        v = sl.get(ten)
        return v if v is not None else CD

    ws = sheet(wb, "Một trang cho lãnh đạo")
    tieu_de(ws, "R4 · BÁO CÁO ĐIỀU HÀNH THEO DỊCH VỤ",
            "Kỳ %s · %d inbox · lập ngày %s · đọc hết trong 2 phút"
            % (ky, n, _hom_nay()))
    muc(ws, "Ba kết luận")
    for i in range(1, 4):
        dong(ws, ["%d." % i, "⚠ chưa viết — mỗi kết luận một con số, viết bằng "
                             "lời thường cho người không đọc bảng"], nen=CANH_BAO)
    trong(ws)
    muc(ws, "Phễu toàn kỳ")
    dong_tieu_de(ws, ["Khâu", "Số", "Tỷ lệ chuyển", "Mốc", "Nguồn"])
    sdt = sum(1 for r in rows if co_sdt(r))
    dong(ws, ["Inbox", n, "—", "—", "đếm từ hội thoại"], dam=True)
    dong(ws, ["Có SĐT", sdt, pc(sdt, n), CX + " (P8 §7 chưa chốt)",
              "đếm từ hội thoại"])
    kn, dl, dk, cp = (phieu("ket_noi"), phieu("dat_lich"), phieu("den_kham"),
                      phieu("chot_phac_do"))
    dong(ws, ["Kết nối được (gọi được)", kn,
              pc(kn, sdt) if isinstance(kn, int) else CD, "≥ 78%",
              "phiếu — phải truyền vào"])
    dong(ws, ["Đặt lịch khám", dl,
              pc(dl, kn) if isinstance(kn, int) and isinstance(dl, int) else CD,
              "≥ 50%", "phiếu"])
    dong(ws, ["ĐẾN KHÁM (show-up)", dk,
              pc(dk, dl) if isinstance(dl, int) and isinstance(dk, int) else CD,
              CX, "sổ tiếp nhận phòng khám"],
         nen=CANH_BAO if not isinstance(dk, int) else None)
    dong(ws, ["Chốt phác đồ", cp,
              pc(cp, dk) if isinstance(dk, int) and isinstance(cp, int) else CD,
              CX, "hệ thống điều trị — chỉ số của PHÒNG KHÁM, "
                  "không thuộc trách nhiệm trực page"])
    trong(ws)
    dong(ws, ["⚠ \"Đặt lịch khám\" KHÔNG phải \"đến khám\"",
              "Ở tiêu hóa hai con số này lệch nhau rất nhiều, và khoảng lệch "
              "đó chính là chỗ rò nặng nhất. Không lấy số này thay số kia cho "
              "đủ bảng.", "", "", ""], nen=CANH_BAO)
    trong(ws)
    muc(ws, "Phễu tách theo nhóm giá trị")
    dong_tieu_de(ws, ["Nhóm giá trị", "Inbox", "Có SĐT", "% có SĐT",
                      "Kết nối", "Đặt lịch", "Đến khám", "Nhận định"])
    for gt in ("G1", "G2", "G3"):
        hs = [r for r in rows if r.get("nhom_gia_tri") == gt]
        m = len(hs)
        if not m:
            continue
        s = sum(1 for r in hs if co_sdt(r))
        dong(ws, [gt, m, s, pc(s, m), CD, CD, CD,
                  "⚠ chưa viết" if m >= NGUONG_MAU
                  else "⚠ chưa đủ mẫu (%d < %d)" % (m, NGUONG_MAU)],
             nen=MAU_GIA_TRI.get(gt))
    dong(ws, ["⚠ ĐỪNG GỘP G1/G2/G3", "", "", "", "", "", "",
              "Một kỳ có 200 inbox hỏi khám đầy hơi và 20 inbox combo tầm soát "
              "sẽ cho bảng phễu trông rất đẹp — trong khi 20 ca combo rò hết mà "
              "không ai thấy. Dải giá chênh gần chín lần, nên đây là lỗi đọc số "
              "đặc trưng của ngành này."], nen=CANH_BAO)
    trong(ws)
    bang_co_do(ws, rows)
    khoi_canh_bao_chuan(ws, rows, mau_loc)
    trong(ws)
    muc(ws, "Ba việc tháng tới")
    for i in range(1, 4):
        dong(ws, ["%d." % i, "⚠ chưa viết — việc · ai phụ trách · cách đo kết quả"],
             nen=CANH_BAO)
    hoan_thien(ws)

    sheet_chu_giai(wb)

    ws = sheet(wb, "Phễu theo dịch vụ")
    tieu_de(ws, "PHỄU THEO DỊCH VỤ",
            "Nhóm dưới %d hội thoại: ⚠ chưa đủ mẫu, KHÔNG kết luận khâu rò."
            % NGUONG_MAU)
    dong_tieu_de(ws, ["Nhóm vấn đề (TH-xx)", "Nhóm giá trị", "Inbox", "Có SĐT",
                      "% có SĐT", "Kết nối được", "% kết nối", "Đặt lịch",
                      "% đặt lịch", "Đến khám", "% show-up", "Soi được",
                      "% soi được / đến khám", "Khâu rò nặng nhất",
                      "Chênh so mốc KPI"])
    for ma in VAN_DE_MA:
        hs = [r for r in rows if r.get("van_de") == ma]
        m = len(hs)
        if not m:
            continue
        s = sum(1 for r in hs if co_sdt(r))
        gt = dem(hs, "nhom_gia_tri").most_common(1)[0][0]
        dong(ws, ["%s %s" % (ma, VAN_DE_TEN[ma]), gt, m, s, pc(s, m),
                  CD, CD, CD, CD, CD, CD, CD, CD,
                  "⚠ chưa đủ mẫu" if m < NGUONG_MAU
                  else "⚠ chờ số phiếu để tính",
                  CX + " — P8 §7 chưa chốt mốc cho ngành tiêu hóa"],
             nen=MO if m < NGUONG_MAU else None)
    hoan_thien(ws)

    ws = sheet(wb, "Chân dung theo vấn đề")
    tieu_de(ws, "CHÂN DUNG KHÁCH THEO VẤN ĐỀ & RÀO CẢN",
            "Cột \"% mang rào cản NÉ\" (L6.8) là chỉ số đáng theo nhất của "
            "ngành này: nhóm NÉ không lùi vì tiền hay vì bận, nên mọi nỗ lực "
            "giảm giá và mọi lần nhắc lịch đều trượt. Tỷ lệ NÉ cao thì việc cần "
            "làm là ĐỔI NỘI DUNG, không phải tăng tần suất nhắc.")
    dong_tieu_de(ws, ["Nhóm vấn đề", "Số HT", "Nhóm khách chủ đạo",
                      "Rào cản số 1", "Rào cản số 2", "% mang rào cản NÉ",
                      "NV có đưa bằng chứng THV", "Hàm ý cho nội dung"])
    for ma in VAN_DE_MA:
        hs = [r for r in rows if r.get("van_de") == ma]
        m = len(hs)
        if not m:
            continue
        c = collections.Counter(x["ma"] for r in hs for x in r.get("rao_can", []))
        ngo = sum(1 for r in hs if "L6.8" in set(ma_rao_can(r)))
        hang = sum(1 for r in hs if r.get("bang_chung_nv"))
        top = c.most_common(2)
        def _t(i):
            if len(top) <= i:
                return "—"
            k = top[i][0]
            return "%s %s (%d)" % (k, RAO_CAN_TEN.get(k, ("", ""))[1], top[i][1])
        dong(ws, ["%s %s" % (ma, VAN_DE_TEN[ma]), m,
                  collections.Counter(nhom_dt(r) for r in hs).most_common(1)[0][0],
                  _t(0), _t(1), pc(ngo, m), "%d / %d" % (hang, m),
                  "⚠ chưa viết" if m >= NGUONG_MAU else "⚠ chưa đủ mẫu"],
             nen=MO if m < NGUONG_MAU else None)
    trong(ws)
    dong(ws, ["⚠ Cách đếm rào cản", "Một hội thoại có thể mang nhiều rào cản. "
              "Cột rào cản đếm theo LƯỢT nên tổng lớn hơn số hội thoại là đúng.",
              "", "", "", "", "", ""], nen=CANH_BAO)
    hoan_thien(ws)

    ws = sheet(wb, "Rào cản toàn kỳ")
    tieu_de(ws, "RÀO CẢN TOÀN KỲ")
    dong_tieu_de(ws, ["Rào cản", "Nhóm (SỢ/NGỜ/NGẠI/NÉ)", "L-code", "Số ca",
                      "% trên tổng HT", "Nhóm vấn đề vướng nhiều nhất",
                      "NV có đưa bằng chứng", "Bằng chứng nên dùng",
                      "Việc cần làm"])
    bc = {"L6.7": "Sàng lọc trước mê + BÁC SĨ GÂY MÊ THEO DÕI RIÊNG. "
                  "⛔ Không hứa chắc mê được khi chưa biết bệnh nền",
          "L6.5": "Bản tiền mê — ngủ trong lúc soi. Nói THẬT về cảm giác của "
                  "bản soi thường. ⛔ Không nói \"không đau\"",
          "L6.9": "Quy trình rửa – tiệt khuẩn dây soi, mời khách xem khi đến "
                  "(⚠ mô tả cụ thể chờ THV cấp)",
          "L6.2": "TS.BS Đỗ Anh Giang (nguyên Phó GĐ TT Tiêu hóa – Gan mật BV "
                  "Bạch Mai) · Fujifilm VP-7000 + AI · bảng giá công khai. "
                  "⛔ Không nói xấu tuyến công",
          "L6.8": "Lợi ích của việc BIẾT SỚM, tổn thương nhỏ xử lý ngay trong "
                  "lúc soi · hẹn MỘT MỐC CỤ THỂ. ⛔ KHÔNG gửi ưu đãi giảm giá, "
                  "⛔ không hù bệnh",
          "L6.3": "Bảng giá công khai + ba điều kiện (ai thực hiện · có tiền mê "
                  "không · phụ phí chỉ khi có chỉ định). Bảo hiểm: ⚠ chờ THV cấp",
          "L6.4": "MỞ CẢ CHỦ NHẬT 7h–17h · gộp khám + soi + kết quả trong một buổi",
          "L6.6": "Mời người nhà đi cùng buổi khám",
          "L6.1": "⚠ chưa xác định rào cản — cần khai thác thêm ở bước B2"}
    c = collections.Counter((x["ma"], x["nhom"], x["ten"])
                            for r in rows for x in r.get("rao_can", []))
    for (ma, nh, ten), v in c.most_common():
        hs = [r for r in rows if ma in ma_rao_can(r)]
        xl = sum(1 for r in hs if r.get("bang_chung_nv"))
        dong(ws, ["%s %s" % (ma, ten), nh, ma, v, pc(v, n),
                  dem(hs, "van_de").most_common(1)[0][0] if hs else "—",
                  "%d / %d" % (xl, len(hs)),
                  bc.get(ma, "⚠"), "⚠ chưa viết"],
             nen=CANH_BAO if ma in ("L6.7", "L6.8", "L6.9") else None)
    hoan_thien(ws)

    ws = sheet(wb, "Chất lượng tư vấn")
    tieu_de(ws, "CHẤT LƯỢNG TƯ VẤN — BẢN RÚT GỌN",
            "Chạy R3 rồi thì DÙNG LẠI kết quả, không chấm lại.")
    dong_tieu_de(ws, ["Chỉ số", "Giá trị kỳ này", "Mốc", "Chênh",
                      "Hậu quả thấy được trong dữ liệu"])
    tc = [r for r in rows if r.get("tu_cam_nv")]
    ngo = [r for r in rows if ma_rao_can(r)]
    ngo_tr = [r for r in ngo if not r.get("bang_chung_nv")]
    cd_all = [r for r in rows if r.get("co_do")]
    cd_sai = [r for r in rows if r.get("tran_an_sai_nv")]
    for a, b, m, h in [
        ("🚩 Tỷ lệ xử lý đúng ca cờ đỏ",
         pc(len(cd_all) - len(cd_sai), len(cd_all)) if cd_all else "—",
         "100% — không thương lượng",
         "%d ca cờ đỏ, %d ca bị trấn an sai" % (len(cd_all), len(cd_sai))),
        ("Điểm chấm TB", CD, "≥ 8/10", "⚠ chạy R3"),
        ("% hội thoại đạt ≥8/10", CD, "≥ 8/10", "⚠ chạy R3"),
        ("% có bước B5 đầy đủ", CD, CX, "⚠ chạy R3"),
        ("% thu đủ 5 thông tin", CD, CX, "⚠ chạy R3"),
        ("% có dặn chuẩn bị", CD, CX,
         "⚠ chạy R3 — tiêu chí rẻ nhất để cải thiện, chặn đúng mốc rò nặng nhất"),
        ("% đưa bằng chứng đúng rào cản",
         "%s (ca L6.7 có nhắc hãng)" % pc(len(ngo) - len(ngo_tr), len(ngo))
         if ngo else CD, CX,
         "%d/%d ca khách ngờ vật liệu mà NV không nhắc đối tác hãng"
         % (len(ngo_tr), len(ngo)) if ngo else "—"),
        ("Số ca vi phạm ngôn từ", len(tc), "0",
         "Mỗi ca là 0 điểm toàn hội thoại VÀ là rủi ro pháp lý: %s"
         % (", ".join("HT#%d" % r["stt"] for r in tc) or "—")),
    ]:
        dong(ws, [a, b, m, CD, h], nen=CANH_BAO if a.startswith("Số ca") and tc
             else None)
    hoan_thien(ws)

    ws = sheet(wb, "Hiệu quả quảng cáo")
    tieu_de(ws, "HIỆU QUẢ QUẢNG CÁO — BẢN RÚT GỌN",
            "Chạy R2 rồi thì DÙNG LẠI kết quả. Luôn có cột %G1 — xếp hạng post "
            "chỉ bằng %HOT là quyết sai ngân sách ngành tiêu hóa.")
    dong_tieu_de(ws, ["Mã post", "Góc tiếp cận", "Số HT", "% có SĐT", "% HOT",
                      "% G1", "Khuyến nghị", "Đủ mẫu?"])
    tp = collections.defaultdict(list)
    for r in rows:
        tp[r.get("post", "(không rõ nguồn)")].append(r)
    for ten, hs in sorted(tp.items(), key=lambda x: -len(x[1])):
        m = len(hs)
        d, g = dem(hs, "do_nong"), dem(hs, "nhom_gia_tri")
        dong(ws, [ten, "⚠ chạy R2", m, pc(sum(1 for r in hs if co_sdt(r)), m),
                  pc(d["HOT"], m), pc(g["G1"], m),
                  "CHỜ THÊM DỮ LIỆU" if m < NGUONG_MAU else "⚠ chạy R2",
                  du_mau(m)], nen=MO if m < NGUONG_MAU else None)
    hoan_thien(ws)

    ws = sheet(wb, "Tệp giá trị dài hạn")
    tieu_de(ws, "⭐ TỆP GIÁ TRỊ DÀI HẠN — sheet riêng của ngành tiêu hóa",
            "Phần hay bị bỏ nhưng đáng tiền nhất. Đây là những khách đã TỰ "
            "CHỨNG MINH có nhu cầu thật, mà thường không ai chăm vì họ không "
            "xuất hiện trong báo cáo lead mới.")
    dong_tieu_de(ws, ["Nhóm tệp", "Số HT", "Mô tả", "Vì sao đáng giữ",
                      "Nhịp chạm đề xuất", "Ai phụ trách"])
    wv1 = [r for r in rows if r.get("nhom_gia_tri") == "G1"
           and r.get("do_nong") in ("WARM", "COLD")]
    th02 = [r for r in rows if r.get("van_de") == "TH-02"]
    th03 = [r for r in rows if r.get("van_de") == "TH-03"
            and r.get("ghi_de") != "đã đặt lịch"]
    th11 = [r for r in rows if r.get("van_de") == "TH-11"]
    ne = [r for r in rows if "L6.8" in ma_rao_can(r)]
    nha = [r for r in rows if r.get("dau_hieu_nguoi_nha")]
    for ten, sl_, mt, vs, nh, ai in [
        ("⭐ TH-02 ĐẾN HẸN SOI LẠI", len(th02),
         "Đã cắt polyp · đang theo dõi · bác sĩ đã hẹn mốc soi lại",
         "TỆP ĐÁNG TIỀN NHẤT CỦA NGÀNH. Khác mọi ngành khác: nhóm này KHÔNG cần "
         "tạo nhu cầu — mốc hẹn đã nằm trong phiếu kết quả của chính khách. Họ "
         "gần như chắc chắn soi lại, vấn đề chỉ là soi ở đâu. Mà họ không xuất "
         "hiện trong báo cáo lead mới nên thường không ai nhắc",
         "Nhắc theo MỐC ĐÃ GHI TRONG PHIẾU KẾT QUẢ. ⚠ Không tự nêu số năm chu kỳ "
         "— đó là chỉ định của bác sĩ cho từng ca", "CSKH + phòng khám"),
        ("⭐ Đã đến khám mà chưa soi được", CD,
         "Hoãn tại chỗ: nhịn ăn chưa đủ · ruột chưa sạch · không đủ điều kiện "
         "tiền mê · không có người đưa về · đến rồi không dám soi",
         "Khách đã bỏ công đến tận nơi và đã tốn TOÀN BỘ chi phí quảng cáo. "
         "Phần lớn nguyên nhân là LỖI DẶN DÒ, sửa được bằng một tin nhắn mẫu",
         "⚠ chờ bảng ghi nhận của lễ tân: mỗi ca đến khám mà không soi được, "
         "ghi một dòng lý do", "Lễ tân + CSKH"),
        ("WARM/COLD · G1", len(wv1),
         "Chưa sẵn sàng nhưng là ca combo tầm soát / can thiệp / gói chuyên gia",
         "Giá trị kỳ vọng cao hơn cả HOT·G3. Chu kỳ quyết định dài hơn hẳn",
         "D+3 → D+7 → D+15 → 2 tuần/lần. NUÔI TỚI 90 NGÀY, không hạ tệp ở 30",
         "Trực page + CSKH cặp cố định"),
        ("L6.8 NÉ KẾT QUẢ", len(ne),
         "Biết nên soi nhưng trì hoãn vì sợ phát hiện ra bệnh",
         "Nhóm đông nhất của tệp nguội, và là nhóm DUY NHẤT mà nội dung đúng có "
         "thể gọi lại được — nhưng chỉ khi nhận ra đúng",
         "D+7 → D+21 → D+45, nội dung GIÁO DỤC. NUÔI TỚI 180 NGÀY. "
         "⛔ Không gửi ưu đãi giảm giá", "CSKH + người làm nội dung"),
        ("TH-11 mang kết quả nơi khác đến", len(th11),
         "Đã có kết quả soi / CT / xét nghiệm từ nơi khác",
         "Đã qua giai đoạn \"có cần soi hay không\", chỉ còn chọn nơi làm. "
         "Giá trị cao, chu kỳ ngắn nhất trong mọi tệp",
         "Gọi sớm (HOT theo ghi đè ③), mời bác sĩ đọc kết quả trực tiếp",
         "CSKH"),
        ("TH-03 tầm soát chưa đặt lịch", len(th03),
         "Chưa có triệu chứng, chủ động muốn tầm soát",
         "Nhóm G1 hay bị chấm COLD vì tin nhắn ngắn và không có triệu chứng cấp "
         "— bảng xếp hạng theo độ nóng đẩy họ xuống cuối một cách oan",
         "Nội dung giáo dục theo tuổi và nguy cơ, không hù bệnh", "CSKH"),
        ("Có dấu hiệu người nhà", len(nha),
         "Hội thoại nhắc \"cho bố\", \"cho mẹ\", \"cả nhà\", \"vợ em cũng bị\"",
         "Vừa là tệp LTV, vừa có thể là nhóm NGUY CƠ CAO: yếu tố gia đình trong "
         "tiền sử ung thư tiêu hóa là mã CĐ-6",
         "Mời người nhà cùng tầm soát trong một buổi", "CSKH"),
    ]:
        dong(ws, [ten, sl_, mt, vs, nh, ai],
             nen=CANH_BAO if sl_ == CD else None)
    hoan_thien(ws)

    ws = sheet(wb, "Dữ liệu thô & cách tính")
    tieu_de(ws, "DỮ LIỆU THÔ & CÁCH TÍNH",
            "Bắt buộc có sheet này. Lãnh đạo hỏi \"số này ở đâu ra\" thì mở "
            "sheet này, không phải hỏi lại người làm báo cáo.")
    dong_tieu_de(ws, ["Chỉ số", "Công thức", "Tử số", "Mẫu số", "Nguồn dữ liệu",
                      "Hạn chế khi đọc"])
    for a, b, t, m, ng, hc in [
        ("% có SĐT", "số HT có SĐT / tổng HT", sdt, n,
         "trường \"Có SĐT\" trong file hội thoại, lấy nguyên không suy lại",
         "Nếu mẫu đã lọc \"chỉ HT có số\" thì chỉ số này ra 100% và vô nghĩa"),
        ("% HOT", "số HT chấm HOT / tổng HT",
         dem(rows, "do_nong")["HOT"], n, "chấm 5 tín hiệu + 4 luật ghi đè",
         "Không so sánh được giữa các nhóm chia theo nhóm vấn đề — dùng %HOT* "
         "(xem R2 sheet ①)"),
        ("% G1", "số HT nhóm giá trị V1 / tổng HT",
         dem(rows, "nhom_gia_tri")["G1"], n, "suy từ nhóm vấn đề, xem P4 §3",
         "Ca TH-12 hỏi chung không gán được nhóm giá trị"),
        ("% kết nối", "số gọi được / số đã xin được số", kn, sdt,
         "⚠ phiếu — phải truyền vào bằng --ket-noi",
         "Không có trong file hội thoại"),
        ("% show-up", "số ĐẾN KHÁM / số đặt lịch khám", dk, dl,
         "⚠ sổ tiếp nhận phòng khám — truyền vào bằng --den-kham",
         "KHÔNG lấy số đặt lịch thay thế. Hai con số lệch nhau rất nhiều"),
        ("Số ca vi phạm ngôn từ", "đếm HT có từ cấm trong lời NV",
         len(tc), n, "khớp từ khoá trong tu-dien-van-de-rang.json",
         "Chỉ bắt được từ cấm viết đúng chính tả. Không bắt được chốt giá cứng, "
         "chẩn đoán qua tin nhắn, hay gắn \"chính hãng\" sai — xem R3"),
    ]:
        dong(ws, [a, b, t, m, ng, hc])
    hoan_thien(ws)

    return [ghi(wb, out_dir, "THV_BaoCaoDieuHanh_%s.xlsx" % _slug(ky))]


# ------------------------------------------------------------------- R5

def r5(rows, rows_truoc, ky, ky_truoc, out_dir, cung_mau=None):
    n2, n1 = len(rows), len(rows_truoc)
    wb = so_moi()

    def nguong(m):
        return 10 if m < 30 else (5 if m <= 100 else 3)

    ws = sheet(wb, "Tổng quan & cổng chặn")
    tieu_de(ws, "R5 · SO SÁNH HAI KỲ — %s vs %s" % (ky_truoc, ky),
            "Kỳ 1: %d hội thoại · Kỳ 2: %d hội thoại · lập ngày %s"
            % (n1, n2, _hom_nay()))
    muc(ws, "🛑 CỔNG CHẶN — làm trước mọi thứ, có quyền dừng cả báo cáo")
    dong_tieu_de(ws, ["#", "Câu hỏi", "Trả lời", "Khác nhau thì sao"])
    for i, (q, a, hq) in enumerate([
        ("Hai kỳ có cùng CÁCH LẤY MẪU không? (toàn bộ, hay đã lọc theo độ dài "
         "/ theo có số)",
         cung_mau if cung_mau else "⚠ CHƯA XÁC NHẬN — người lập phải trả lời",
         "DỪNG. Không so được. Chỉ được so trong nội bộ từng kỳ"),
        ("Hai kỳ có cùng PHẠM VI DỊCH VỤ không?", "⚠ chưa xác nhận",
         "Chỉ so phần dịch vụ trùng nhau, ghi rõ đã loại gì"),
        ("Hai kỳ có cùng CÁCH CHẤM không? (cùng 5 tín hiệu, cùng 4 luật ghi đè, cùng cách sàng cờ đỏ)",
         "⚠ chưa xác nhận",
         "Chấm lại kỳ cũ theo chuẩn hiện hành, hoặc dừng"),
        ("Hai kỳ có ĐỘ DÀI tương đương không?", "⚠ chưa xác nhận",
         "Chỉ so chỉ số TỶ LỆ, không so số tuyệt đối"),
    ], start=1):
        dong(ws, [i, q, a, hq],
             nen=CANH_BAO if str(a).startswith("⚠") else None)
    trong(ws)
    dong(ws, ["⚠ KHÁC Ở CÂU ①", "Báo cáo chỉ được trả về MỘT TRANG: vì sao "
              "không so được, và cần làm gì để kỳ sau so được. KHÔNG chạy "
              "tiếp, KHÔNG đưa ra con số chênh lệch nào.", "", ""],
         nen=CANH_BAO)
    trong(ws)
    muc(ws, "Ngưỡng nhiễu đã dùng — chênh dưới ngưỡng thì KHÔNG gọi là thay đổi")
    dong_tieu_de(ws, ["Cỡ mẫu nhóm", "Ngưỡng nhiễu", "Nghĩa"])
    for a, b, c in [
        ("Dưới 30 HT", "10 điểm %", "Chênh dưới 10 điểm % là nhiễu"),
        ("30–100 HT", "5 điểm %", "Chênh dưới 5 điểm % là nhiễu"),
        ("Trên 100 HT", "3 điểm %", "Chênh dưới 3 điểm % là nhiễu"),
    ]:
        dong(ws, [a, b, c])
    dong(ws, ["⚠", "Chênh chưa vượt ngưỡng → ghi \"chưa kết luận được\". "
              "\"Có dấu hiệu cải thiện\" CŨNG là nhận định có hướng — "
              "không được viết.", ""], nen=CANH_BAO)
    trong(ws)
    muc(ws, "So sánh tổng")
    dong_tieu_de(ws, ["Chỉ số", ky_truoc, ky, "Chênh (điểm %)",
                      "Vượt ngưỡng nhiễu?", "Nhận định"])
    for ten, f in [
        ("Số inbox", lambda rs: len(rs)),
        ("% có SĐT", lambda rs: 100.0 * sum(1 for r in rs if co_sdt(r)) / len(rs)),
        ("% HOT", lambda rs: 100.0 * dem(rs, "do_nong")["HOT"] / len(rs)),
        ("% G1", lambda rs: 100.0 * dem(rs, "nhom_gia_tri")["G1"] / len(rs)),
    ]:
        v1, v2 = f(rows_truoc), f(rows)
        if ten == "Số inbox":
            dong(ws, [ten, v1, v2, "—", "—",
                      "Chỉ so số tuyệt đối khi hai kỳ cùng độ dài"])
            continue
        ch = v2 - v1
        ng = nguong(min(n1, n2))
        vuot = abs(ch) >= ng
        dong(ws, [ten, "%.1f%%" % v1, "%.1f%%" % v2, "%+.1f" % ch,
                  "CÓ" if vuot else "KHÔNG (ngưỡng %d)" % ng,
                  "⚠ chưa viết" if vuot else "chưa kết luận được"],
             nen=None if vuot else MO)
    trong(ws)
    khoi_canh_bao(ws, "ĐIỀU KHÔNG SO ĐƯỢC", [
        "Điểm chấm 10 tiêu chí: cần chạy R3 cho CẢ HAI kỳ mới so được.",
        "% đến khám / % chốt phác đồ: cần số phiếu của cả hai kỳ.",
        "Từng post: KHÔNG so được — post hay bị nhân bản và đổi tên giữa các kỳ. "
        "Chỉ so ở mức GÓC TIẾP CẬN.",
        "Không gán nguyên nhân khi chưa có bằng chứng trong dữ liệu. "
        "Chỉ được nói \"X tăng cùng lúc với Y\", không nói \"nhờ Y nên X tăng\".",
    ])
    hoan_thien(ws)

    sheet_chu_giai(wb, them=[
        ("Ngưỡng nhiễu", "Chênh lệch dưới mức dao động tự nhiên thì không gọi "
         "là thay đổi. <30 HT: 10 điểm % · 30–100: 5 · >100: 3.", "Mọi sheet"),
        ("Tương quan ≠ nhân quả", "Báo cáo này chỉ được nói \"X tăng cùng lúc "
         "với Y\". Muốn kết luận nhân quả cần thiết kế khác: giữ nguyên mọi "
         "thứ, chỉ đổi một yếu tố, rồi so.", "Cột Nhận định"),
    ])

    ws = sheet(wb, "So theo chỉ số phễu")
    tieu_de(ws, "SO THEO CHỈ SỐ PHỄU")
    dong_tieu_de(ws, ["Chỉ số", ky_truoc, ky, "Chênh (điểm %)",
                      "Vượt ngưỡng nhiễu?", "Nhận định",
                      "Bằng chứng về nguyên nhân"])
    cs = [("% có SĐT", lambda rs: 100.0 * sum(1 for r in rs if co_sdt(rs and r))
           / len(rs))]
    for k in ("HOT", "WARM", "COLD"):
        cs.append(("% " + k,
                   lambda rs, k=k: 100.0 * dem(rs, "do_nong")[k] / len(rs)))
    for k in ("G1", "G2", "G3"):
        cs.append(("% " + k,
                   lambda rs, k=k: 100.0 * dem(rs, "nhom_gia_tri")[k] / len(rs)))
    for ten, f in cs:
        v1, v2 = f(rows_truoc), f(rows)
        ch = v2 - v1
        ng = nguong(min(n1, n2))
        vuot = abs(ch) >= ng
        dong(ws, [ten, "%.1f%%" % v1, "%.1f%%" % v2, "%+.1f" % ch,
                  "CÓ" if vuot else "KHÔNG (ngưỡng %d)" % ng,
                  "⚠ chưa viết" if vuot else "chưa kết luận được",
                  "⚠ chưa có bằng chứng — không gán nguyên nhân"],
             nen=None if vuot else MO)
    for ten in ("% kết nối", "% đặt lịch khám", "% đến khám", "% chốt phác đồ",
                "Điểm chấm TB", "% đạt ≥8/10"):
        dong(ws, [ten, CD, CD, CD, "—", "⚠ chưa đo được",
                  "Cần số phiếu / chạy R3 cho cả hai kỳ"])
    hoan_thien(ws)

    ws = sheet(wb, "So theo nhóm giá trị")
    tieu_de(ws, "⭐ SO THEO NHÓM GIÁ TRỊ G1/G2/G3 — sheet quan trọng nhất",
            "Một kỳ có thể TĂNG tổng lead mà lại GIẢM lead V1 — tổng trông đẹp "
            "hơn trong khi doanh thu kỳ vọng giảm. Bảng tổng không bắt được "
            "điều đó.")
    dong_tieu_de(ws, ["Nhóm giá trị", "Chỉ số", ky_truoc, ky, "Chênh",
                      "Vượt ngưỡng?", "Nhận định"])
    canh_bao_v1 = False
    for gt in ("G1", "G2", "G3"):
        a1 = dem(rows_truoc, "nhom_gia_tri")[gt]
        a2 = dem(rows, "nhom_gia_tri")[gt]
        p1, p2 = 100.0 * a1 / n1, 100.0 * a2 / n2
        ng = nguong(min(a1, a2) or 1)
        vuot = abs(p2 - p1) >= ng
        dong(ws, [gt, "Số HT", a1, a2, "%+d" % (a2 - a1), "—",
                  "⚠ chỉ so số tuyệt đối khi hai kỳ cùng độ dài"],
             nen=MAU_GIA_TRI.get(gt))
        dong(ws, [gt, "% trên tổng", "%.1f%%" % p1, "%.1f%%" % p2,
                  "%+.1f" % (p2 - p1),
                  "CÓ" if vuot else "KHÔNG (ngưỡng %d)" % ng,
                  "⚠ chưa viết" if vuot else "chưa kết luận được"],
             nen=None if vuot else MO)
        if gt == "G1" and n2 > n1 and a2 < a1:
            canh_bao_v1 = True
    if canh_bao_v1:
        trong(ws)
        dong(ws, ["⚠ PHÁT HIỆN PHẢI ĐƯA LÊN SHEET 1",
                  "Tổng lead TĂNG (%d → %d) nhưng lead nhóm giá trị lớn V1 "
                  "GIẢM (%d → %d). Báo cáo trông đẹp hơn trong khi doanh thu "
                  "kỳ vọng giảm. Tình huống này rất hay xảy ra khi chuyển ngân "
                  "sách sang post banner giá rẻ."
                  % (n1, n2, dem(rows_truoc, "nhom_gia_tri")["G1"],
                     dem(rows, "nhom_gia_tri")["G1"]), "", "", "", "", ""],
             nen=CANH_BAO)
    hoan_thien(ws)

    ws = sheet(wb, "So theo góc tiếp cận")
    tieu_de(ws, "SO THEO GÓC TIẾP CẬN",
            "Chỉ so ở mức GÓC, không so từng post — post hay đổi tên và nhân "
            "bản giữa các kỳ nên không khớp 1-1.")
    dong_tieu_de(ws, ["Góc tiếp cận", "Số HT " + ky_truoc, "Số HT " + ky,
                      "% HOT " + ky_truoc, "% HOT " + ky, "Chênh %HOT",
                      "% G1 " + ky_truoc, "% G1 " + ky, "Chênh %G1",
                      "Vượt ngưỡng?", "Nhận định", "Dùng tiếp hay đổi"])
    dong(ws, ["⚠ chưa có dữ liệu góc tiếp cận", "", "", "", "", "", "", "", "",
              "", "Cần chạy R2 cho cả hai kỳ (R2 cần danh sách post có cột "
              "Góc tiếp cận)", ""], nen=CANH_BAO)
    hoan_thien(ws)

    ws = sheet(wb, "So theo rào cản")
    tieu_de(ws, "SO THEO RÀO CẢN",
            "Chỉ số đáng theo nhất: tỷ lệ ca mang rào cản NGỜ (L6.2 + L6.7) mà "
            "NV CÓ đưa bằng chứng đối tác hãng. Chỉ số này tăng mà % đặt lịch "
            "cũng tăng là bằng chứng GẦN NHẤT cho việc đào tạo có tác dụng — "
            "vẫn là tương quan, không phải nhân quả.")
    dong_tieu_de(ws, ["Rào cản", "Nhóm", "% " + ky_truoc, "% " + ky, "Chênh",
                      "Vượt ngưỡng?", "NV xử lý được (%s → %s)"
                      % (ky_truoc, ky), "Nhận định"])
    for ma, (nh, ten) in RAO_CAN_TEN.items():
        c1 = sum(1 for r in rows_truoc if ma in ma_rao_can(r))
        c2 = sum(1 for r in rows if ma in ma_rao_can(r))
        if not (c1 or c2):
            continue
        p1, p2 = 100.0 * c1 / n1, 100.0 * c2 / n2
        ng = nguong(min(n1, n2))
        vuot = abs(p2 - p1) >= ng
        h1 = sum(1 for r in rows_truoc
                 if ma in ma_rao_can(r) and r.get("bang_chung_nv"))
        h2 = sum(1 for r in rows if ma in ma_rao_can(r) and r.get("bang_chung_nv"))
        xl = "%s → %s" % (pc(h1, c1) if c1 else "—",
                          pc(h2, c2) if c2 else "—")
        dong(ws, ["%s %s" % (ma, ten), nh, "%.1f%%" % p1, "%.1f%%" % p2,
                  "%+.1f" % (p2 - p1),
                  "CÓ" if vuot else "KHÔNG (ngưỡng %d)" % ng, xl,
                  "⚠ chưa viết" if vuot else "chưa kết luận được"],
             nen=None if vuot else MO)
    hoan_thien(ws)

    ws = sheet(wb, "Dữ liệu thô & cách tính")
    tieu_de(ws, "DỮ LIỆU THÔ & CÁCH TÍNH",
            "Không có sheet này thì không ai kiểm được con số chênh lệch.")
    dong_tieu_de(ws, ["Chỉ số", "Công thức", "Tử/mẫu " + ky_truoc,
                      "Tử/mẫu " + ky, "Nguồn", "Hạn chế khi đọc"])
    for ten, ct, f in [
        ("% có SĐT", "HT có SĐT / tổng HT",
         lambda rs: "%d/%d" % (sum(1 for r in rs if co_sdt(r)), len(rs))),
        ("% HOT", "HT chấm HOT / tổng HT",
         lambda rs: "%d/%d" % (dem(rs, "do_nong")["HOT"], len(rs))),
        ("% G1", "HT nhóm V1 / tổng HT",
         lambda rs: "%d/%d" % (dem(rs, "nhom_gia_tri")["G1"], len(rs))),
    ]:
        dong(ws, [ten, ct, f(rows_truoc), f(rows), "rows.json của từng kỳ",
                  "Chỉ so được khi hai kỳ cùng cách lấy mẫu và cùng cách chấm "
                  "— xem cổng chặn sheet 1"])
    hoan_thien(ws)

    return [ghi(wb, out_dir, "THV_SoSanh_%s_vs_%s.xlsx"
                % (_slug(ky_truoc), _slug(ky)))]


# ----------------------------------------------------------------- main

def _slug(s):
    s = re.sub(r"[^0-9A-Za-zÀ-ỹ]+", "-", str(s)).strip("-")
    return s or "ky"


def _hom_nay():
    import datetime
    return datetime.date.today().strftime("%d/%m/%Y")


def main():
    ap = argparse.ArgumentParser(
        description="Xuat file Excel theo khuon reports/R1-R5")
    ap.add_argument("--bao-cao", required=True,
                    choices=["R1", "R2", "R3", "R4", "R5", "tat-ca"])
    ap.add_argument("--rows", required=True, help="rows.json tu phan_loai.py")
    ap.add_argument("--rows-truoc", help="rows.json ky truoc (chi R5)")
    ap.add_argument("--ky", default="chưa ghi kỳ")
    ap.add_argument("--ky-truoc", default="kỳ trước")
    ap.add_argument("--dich-vu", default="Tổng hợp")
    ap.add_argument("--posts", help="file markdown danh sach post (R2)")
    ap.add_argument("--out", default="output")
    ap.add_argument("--mau-loc", help="neu mau DA BI LOC thi ghi ro cach loc, "
                                      "vd \"100 HT chon tu 520, uu tien HT dai\"")
    ap.add_argument("--ket-noi", type=int)
    ap.add_argument("--dat-lich", type=int)
    ap.add_argument("--den-kham", type=int)
    ap.add_argument("--chot-phac-do", type=int)
    a = ap.parse_args()

    rows = doc_rows(a.rows)
    sl = {k: v for k, v in [("ket_noi", a.ket_noi), ("dat_lich", a.dat_lich),
                            ("den_kham", a.den_kham),
                            ("chot_phac_do", a.chot_phac_do)] if v is not None}
    ra = []
    bc = a.bao_cao
    if bc in ("R1", "tat-ca"):
        ra += r1(rows, a.ky, a.dich_vu, a.out, a.mau_loc)
    if bc in ("R2", "tat-ca"):
        ra += r2(rows, a.ky, a.dich_vu, a.out, a.posts, a.mau_loc)
    if bc in ("R3", "tat-ca"):
        ra += r3(rows, a.ky, a.dich_vu, a.out, a.mau_loc)
    if bc in ("R4", "tat-ca"):
        ra += r4(rows, a.ky, a.dich_vu, a.out, sl, a.mau_loc)
    if bc == "R5":
        if not a.rows_truoc:
            raise SystemExit("R5 cần --rows-truoc (rows.json của kỳ trước).")
        ra += r5(rows, doc_rows(a.rows_truoc), a.ky, a.ky_truoc, a.out)

    out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    out.write("\nĐã ghi %d file:\n" % len(ra))
    for p in ra:
        out.write("  %s\n" % p)
    out.write("\nLƯU Ý: ô nào ghi ⚠ là chỗ script không tính được, cần người "
              "hoặc trợ lý đọc hiểu rồi điền.\n"
              "Riêng R3: bảng chấm 10 tiêu chí là KHUNG, chỉ phần phát hiện "
              "từ cấm là đã điền sẵn.\n")
    out.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
