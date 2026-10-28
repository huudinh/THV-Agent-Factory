# -*- coding: utf-8 -*-
"""Doc file hoi thoai -> phan loai -> rows.json + bang dem.

Cong cu KIEM TRA DOI CHIEU, khong thay the viec doc hieu cua tro ly.
Script khop tu khoa nen no bat duoc nhung thu hien ro trong chu; nhung sac thai
("de qua Tet em di" la ngai thoi gian hay ne ket qua) thi chi nguoi hoac AI
doc duoc. Xem P6 §2 phan phan biet L6.4 vs L6.8.

Dung de: dem lai con so o DUNG 1 va DUNG 2, xem tro ly co dem lech khong.
Va dung de QUET CO DO mot luot cho ca file - phan nay script lam tot hon nguoi,
vi no khong bo sot dong nao.

CO DO: tu dien co tinh nhan RONG. Tha gan thua con hon bo sot. Danh sach script
in ra la danh sach CAN NGUOI DOC LAI, khong phai ket luan.

Cach dung:
    python phan_loai.py --src <file hoi thoai .md> [--out rows.json] [--tu-dien <file .json>]

Vi du:
    python phan_loai.py --src ../doc/mau-du-lieu/MAU_Hoi-thoai.md
"""
import argparse
import collections
import io
import json
import os
import re
import sys

VN = ("àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợ"
      "ùúủũụưứừửữựỳýỷỹỵđ")
_PAT = {}


def has(text, kw):
    """So khop co bien tu, de 'ho' khong khop trong 'hop'.

    Giu nguyen dau tieng Viet: bo dau roi so khop chuoi con la sai, vi
    'khong' se chua 'hong'.
    """
    pat = _PAT.get(kw)
    if pat is None:
        pat = _PAT[kw] = re.compile(
            r"(?<![\w" + VN + r"])" + re.escape(kw) + r"(?![\w" + VN + r"])")
    return bool(pat.search(text))


def has_any(text, kws):
    return any(has(text, k) for k in kws)


# Tu phu dinh dung cho co do. "khong sut can" KHONG phai dau hieu sut can.
PHU_DINH = ("không", "chưa", "ko", "chẳng", "k ")


def has_kd(text, kw):
    """Nhu has() nhung bo qua lan xuat hien NAM SAU mot tu phu dinh.

    Chi dung cho CO DO va cho cau tran an: o hai cho do, mot ca gan thua
    lam nguoi doc mat thoi gian, con mot ca bo sot thi khac han - nen van
    nhan rong, chi loai dung truong hop phu dinh ngay truoc tu khoa.
    Vi du loai duoc: "khong sut can", "chua sut can", "khong co phan den".
    Khong loai duoc: "em khong bi gi ca, chi sut can thoi" - dung, vi o day
    "sut can" la co that.
    """
    pat = _PAT.get(kw)
    if pat is None:
        pat = _PAT[kw] = re.compile(
            r"(?<![\w" + VN + r"])" + re.escape(kw) + r"(?![\w" + VN + r"])")
    for m in pat.finditer(text):
        truoc = text[max(0, m.start() - 16):m.start()]
        if any(pd in truoc for pd in PHU_DINH):
            continue
        return True
    return False


def has_any_kd(text, kws):
    return any(has_kd(text, k) for k in kws)


# ---------------------------------------------------------------- tach file

RE_HEAD = re.compile(r"^##\s+(\d+)\.\s*(.+?)\s+—\s+(.+?)\s*$")
RE_META = re.compile(r"Phụ trách:\s*(.*?)\s*·\s*Có SĐT:\s*(\S+)\s*·\s*Số tin:\s*(\d+)")
RE_TIN = re.compile(r"^-\s+\*\*(.+?)\s+(KH|NV)(?:\s*\((.*?)\))?:\*\*\s*(.*)$")
RE_THE = re.compile(r"\[Thẻ:\s*(.*?)\]")
RE_QC = re.compile(r"Inbox từ quảng cáo\s+(.+?)\s*[–-]")


def tach(path):
    """Tach file markdown thanh danh sach hoi thoai."""
    raw = io.open(path, encoding="utf-8").read().splitlines()
    hts, cur = [], None
    for line in raw:
        m = RE_HEAD.match(line)
        if m:
            if cur:
                hts.append(cur)
            cur = {"stt": int(m.group(1)), "ten": m.group(2).strip(),
                   "ngay": m.group(3).strip(), "nv": "", "co_sdt": "",
                   "so_tin": 0, "the": "", "post": "", "kh": [], "nvtin": []}
            continue
        if cur is None:
            continue
        mm = RE_META.search(line)
        if mm:
            cur["nv"] = mm.group(1).strip()
            cur["co_sdt"] = mm.group(2).strip()
            cur["so_tin"] = int(mm.group(3))
            continue
        mt = RE_TIN.match(line)
        if mt:
            noi_dung = mt.group(4)
            mthe = RE_THE.search(noi_dung)
            if mthe and not cur["the"]:
                cur["the"] = mthe.group(1).strip()
                mqc = RE_QC.search(cur["the"])
                cur["post"] = mqc.group(1).strip() if mqc else ""
            # Bo phan [The: ...] khoi chu khach: do la tin tu dong, va headline
            # quang cao trong the se lam lech phan loai (vd the "noi soi khong
            # dau" bi doc thanh khach dang hoi ve tien me).
            noi_dung = RE_THE.sub(" ", noi_dung).strip()
            if not noi_dung:
                continue
            if mt.group(2) == "KH":
                cur["kh"].append(noi_dung)
            else:
                cur["nvtin"].append(noi_dung)
    if cur:
        hts.append(cur)
    return hts


# ------------------------------------------------------------- phan loai

def co_do(text, td):
    """Quet 6 ma co do. Tra ve danh sach [(ma, ten), ...].

    Luat phan biet bat buoc (P4 §2): mau DO TUOI khi di ngoai -> TH-06,
    KHONG phai co do. PHAN DEN -> CD-1, LA co do. Tu dien bat 'di ngoai ra mau'
    o TH-06 nen o day chi can khong cho 'ra mau do' kich CD-1.
    """
    out = []
    for ma, d in td["co_do"].items():
        if ma.startswith("_"):
            continue
        if has_any_kd(text, d["kw"]):
            out.append((ma, d["ten"]))
    return out


def van_de(text, td, co_co_do):
    """Xet nhom van de tieu hoa. TH-01 thang moi nhom khac."""
    if co_co_do:
        return "TH-01", "🚩 CỜ ĐỎ — dấu hiệu cần khám ngay"
    for ma, ten, kws in td["van_de"]:
        if kws and has_any(text, kws):
            return ma, ten
    return "TH-12", "Chưa rõ / hỏi chung"


def nhom_gia_tri(ma_vd, text, td):
    g = td["gia_tri"]
    if has_any(text, g["g1_kw"]):
        return "G1"
    if ma_vd in g["G1"]:
        return "G1"
    if ma_vd in g["G2"]:
        return "G2"
    if ma_vd in g["G3"]:
        return "G3"
    if has_any(text, g["g3_kw"]):
        return "G3"
    return "?"


def cham(ht, ma_vd, text_kh, td, co_co_do):
    """Cham 5 tin hieu + 4 luat ghi de. Tra ve (bitmask, diem, nong, ghi_de, ...)."""
    th = td["tin_hieu"]
    s1 = ma_vd != "TH-12"
    s2 = has_any(text_kh, th["th2_thoi_gian"])
    s4 = has_any(text_kh, th["th4_mo_ta_ro"]) or "[ảnh]" in text_kh
    # (3) chi tinh khi hoi cu the VA da co mo ta tinh trang, hoac da trao doi
    #     tu 3 tin tro len -> tranh dem cau "bao nhieu tien" o tin dau.
    s3 = has_any(text_kh, th["th3_hoi_cu_the"]) and (s4 or len(ht["kh"]) >= 3)
    s5 = ht["co_sdt"].lower().startswith("c")

    bits = [s1, s2, s3, s4, s5]
    diem = sum(1 for b in bits if b)
    bitmask = "".join("1" if b else "0" for b in bits)

    gd = td["ghi_de"]
    ghi_de = ""
    if co_co_do:
        ghi_de = "🚩 cờ đỏ"
    elif has_any(text_kh, gd["da_dat_lich"]):
        ghi_de = "đã đặt lịch"
    elif has_any(text_kh, gd["da_co_ket_qua"]):
        ghi_de = "đã có kết quả nơi khác"
    elif has_any(text_kh, gd["den_hen_soi_lai"]):
        ghi_de = "đến hẹn soi lại"

    if ghi_de in ("🚩 cờ đỏ", "đã đặt lịch", "đã có kết quả nơi khác"):
        nong = "HOT"
    elif ghi_de == "đến hẹn soi lại":
        nong = "HOT" if diem >= 4 else "WARM"
    else:
        nong = "HOT" if diem >= 4 else ("WARM" if diem >= 2 else "COLD")

    # diem4: cham lai khong ke tin hieu (1) -> chong lap vong (P8 §2)
    diem4 = sum(1 for b in bits[1:] if b)
    nong4 = "HOT*" if diem4 >= 3 else ("WARM*" if diem4 >= 1 else "COLD*")

    # do nong KHONG tinh luat ghi de co do -> dung cho cot "% HOT (tru co do)"
    nong_tru_co = ("HOT" if diem >= 4 else ("WARM" if diem >= 2 else "COLD")) \
        if co_co_do else nong
    return bitmask, diem, nong, ghi_de, diem4, nong4, nong_tru_co


def rao_can(text_kh, td):
    out = []
    for ma, d in td["rao_can"].items():
        if ma.startswith("_"):
            continue
        if has_any(text_kh, d["kw"]):
            out.append((ma, d["nhom"], d["ten"]))
    return out


def l_code(ht, rcs, text_kh, td):
    """Suy ma L. Day la DE XUAT, nguoi/AI doc lai van la nguon chot."""
    co_sdt = ht["co_sdt"].lower().startswith("c")
    if co_sdt:
        return "L4.1"
    # THV chi co 1 co so o Ha Noi -> khach NGOAI Ha Noi la L2.5
    if has_any(text_kh, ["ở xa", "tỉnh em", "quê em", "xa Hà Nội", "ở tỉnh"]) \
            and not has_any(text_kh, td["khu_vuc_gan"]["kw"]):
        return "L2.5"
    if rcs:
        return rcs[0][0]
    if len(ht["kh"]) <= 1:
        return "L1.1"
    return "L2.1"


def giai_doan(ma_vd, rcs, text_kh, td):
    if ma_vd == "TH-02" or has_any(text_kh, ["đã soi rồi", "soi xong", "sau khi soi",
                                             "kết quả của em", "uống thuốc theo đơn"]):
        return "CS"
    if rcs:
        return "S3"
    th = td["tin_hieu"]
    if ma_vd != "TH-12" and (has_any(text_kh, th["th4_mo_ta_ro"])
                             or "[ảnh]" in text_kh):
        return "S2"
    return "S1"


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="file hoi thoai .md")
    ap.add_argument("--out", default="rows.json")
    ap.add_argument("--tu-dien", default=None)
    a = ap.parse_args()

    td_path = a.tu_dien or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tu-dien-tieu-hoa.json")
    td = json.load(io.open(td_path, encoding="utf-8"))

    hts = tach(a.src)
    if not hts:
        sys.stderr.write("Khong tach duoc hoi thoai nao. Kiem dinh dang file.\n")
        return 1

    rows = []
    for ht in hts:
        text_kh = "\n".join(ht["kh"]).lower()
        text_nv = "\n".join(ht["nvtin"]).lower()
        cds = co_do(text_kh, td)
        ma_vd, ten_vd = van_de(text_kh, td, bool(cds))
        gt = nhom_gia_tri(ma_vd, text_kh, td)
        bitmask, diem, nong, ghi_de, diem4, nong4, nong_tru_co = cham(
            ht, ma_vd, text_kh, td, bool(cds))
        rcs = rao_can(text_kh, td)
        rows.append({
            "stt": ht["stt"], "ten": ht["ten"], "ngay": ht["ngay"],
            "nv": ht["nv"], "so_tin": ht["so_tin"], "co_sdt": ht["co_sdt"],
            "the": ht["the"], "post": ht["post"] or ("(thẻ không phải QC)"
                                                     if ht["the"] else "(không rõ nguồn)"),
            "co_do": [{"ma": m, "ten": t} for m, t in cds],
            "van_de": ma_vd, "ten_van_de": ten_vd, "nhom_gia_tri": gt,
            "bitmask": bitmask, "diem": diem, "do_nong": nong, "ghi_de": ghi_de,
            "diem4": diem4, "nong4": nong4, "nong_tru_co_do": nong_tru_co,
            "rao_can": [{"ma": m, "nhom": n, "ten": t} for m, n, t in rcs],
            "l_code": l_code(ht, rcs, text_kh, td),
            "giai_doan": giai_doan(ma_vd, rcs, text_kh, td),
            "tu_cam_nv": [k for k in td["tu_cam"] if has(text_nv, k)],
            "tran_an_sai_nv": [k for k in td["tran_an_sai"]["kw"]
                               if has(text_nv, k)] if cds else [],
            "bang_chung_nv": [k for k in td["bang_chung_thv"]["kw"]
                              if has(text_nv, k)],
            "dau_hieu_nguoi_nha": has_any(text_kh, td["dau_hieu_nguoi_nha"]),
        })

    io.open(a.out, "w", encoding="utf-8").write(
        json.dumps(rows, ensure_ascii=False, indent=1))

    # ------------------------------------------------- bang dem
    n = len(rows)
    out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    def p(s=""):
        out.write(s + "\n")

    def dem(key):
        return collections.Counter(r[key] for r in rows)

    co_sdt = sum(1 for r in rows if r["co_sdt"].lower().startswith("c"))

    # ---- CO DO len dau tien, truoc moi con so khac
    cd_rows = [r for r in rows if r["co_do"]]
    tran_an = [r for r in cd_rows if r["tran_an_sai_nv"]]
    p("=" * 66)
    p("  CO DO  —  doc truoc moi con so khac")
    p("=" * 66)
    p("Ca co dau hieu co do   %d / %d" % (len(cd_rows), n))
    if cd_rows:
        for r in cd_rows:
            ma = " ".join(c["ma"] for c in r["co_do"])
            canh = "  <== NV TRAN AN SAI" if r["tran_an_sai_nv"] else ""
            p("    HT#%-3d %-18s %-14s SDT:%-5s %s%s"
              % (r["stt"], r["ten"][:18], ma, r["co_sdt"], r["l_code"], canh))
        p()
        p("  Trong do BI TRAN AN SAI: %d  <-- loi nang nhat cua he (P5 §1)" % len(tran_an))
        for r in tran_an:
            p("      HT#%-3d %-16s : %s" % (r["stt"], r["nv"],
                                            ", ".join(r["tran_an_sai_nv"])))
        p()
        p("  LUU Y: day la ket qua KHOP TU KHOA, tu dien co tinh nhan RONG.")
        p("  Danh sach nay la danh sach CAN NGUOI DOC LAI, khong phai ket luan.")
        p("  Mau DO TUOI khi di ngoai -> TH-06, khong phai co do. PHAN DEN -> co do.")
    else:
        p("  Khong phat hien ca nao theo 6 ma CD-1..CD-6.")
        p("  Van phai ghi khoi co do trong bao cao, ghi ro 'da sang %d hoi thoai'." % n)
    p()

    p("=" * 66)
    p("  DOI CHIEU CON SO  —  %s" % os.path.basename(a.src))
    p("=" * 66)
    p("Tach duoc            %d hoi thoai" % n)
    p("Co SDT               %d  (%.1f%%)" % (co_sdt, 100.0 * co_sdt / n))
    p("Khong co SDT         %d  (%.1f%%)" % (n - co_sdt, 100.0 * (n - co_sdt) / n))
    p("Co the nguon QC      %d" % sum(1 for r in rows if r["post"].startswith("QC")))
    p("The khong phai QC    %d" % sum(1 for r in rows if "không phải QC" in r["post"]))
    p("Khong ro nguon       %d" % sum(1 for r in rows if "không rõ nguồn" in r["post"]))
    p()
    p("-- DO NONG " + "-" * 54)
    for k in ("HOT", "WARM", "COLD"):
        v = dem("do_nong")[k]
        p("  %-6s %3d  (%.1f%%)" % (k, v, 100.0 * v / n))
    gd = [r for r in rows if r["ghi_de"]]
    p("  trong do %d ca do LUAT GHI DE:" % len(gd))
    for k, v in collections.Counter(r["ghi_de"] for r in gd).items():
        p("      %-36s %d" % (k, v))
    p()
    p("-- DO NONG TRU CO DO  (dung de so sanh post / nhom) " + "-" * 14)
    for k in ("HOT", "WARM", "COLD"):
        v = collections.Counter(r["nong_tru_co_do"] for r in rows)[k]
        p("  %-6s %3d  (%.1f%%)" % (k, v, 100.0 * v / n))
    p()
    p("-- NHOM GIA TRI " + "-" * 49)
    for k in ("G1", "G2", "G3", "?"):
        v = dem("nhom_gia_tri")[k]
        if v:
            p("  %-3s %3d  (%.1f%%)" % (k, v, 100.0 * v / n))
    p()
    p("-- NHOM VAN DE TIEU HOA " + "-" * 41)
    v = dem("van_de")["TH-01"]
    if v:
        p("  %-7s %-40s %d" % ("TH-01", "CO DO", v))
    for ma, ten, _ in td["van_de"]:
        v = dem("van_de")[ma]
        if v:
            p("  %-7s %-40s %d" % (ma, ten, v))
    p()
    p("-- GIAI DOAN " + "-" * 52)
    for k in ("S1", "S2", "S3", "CS"):
        v = dem("giai_doan")[k]
        if v:
            p("  %-3s %d" % (k, v))
    p()
    p("-- RAO CAN  (mot HT co the mang nhieu -> tong > %d la dung) " % n + "-" * 5)
    c = collections.Counter()
    cn = collections.Counter()
    for r in rows:
        for rc in r["rao_can"]:
            c[(rc["ma"], rc["ten"])] += 1
            cn[rc["nhom"]] += 1
    for (ma, ten), v in sorted(c.items(), key=lambda x: -x[1]):
        p("  %-6s %-36s %d" % (ma, ten, v))
    p("  theo nhom: " + " · ".join("%s %d" % (k, v) for k, v in cn.most_common()))
    p()
    p("  LUU Y L6.8 (NE KET QUA): tu dien chi bat duoc tin hieu be mat.")
    p("  L6.4 (ban) va L6.8 (ne ket qua) noi cung mot cau 'de em sap xep da'.")
    p("  Phan biet bang: sau khi lui co hoi tiep ve lich khong (P6 §2). NGUOI DOC.")
    p()
    p("-- CANH BAO NGON TU " + "-" * 45)
    tc = [r for r in rows if r["tu_cam_nv"]]
    p("  HT co TU CAM trong loi nhan vien: %d" % len(tc))
    for r in tc:
        p("      HT#%-3d %-16s %s" % (r["stt"], r["nv"], ", ".join(r["tu_cam_nv"])))
    kbc = [r for r in rows
           if r["rao_can"] and not r["bang_chung_nv"]]
    p("  HT khach CO RAO CAN ma NV khong dua bang chung nao cua THV: %d" % len(kbc))
    for r in kbc[:15]:
        p("      HT#%-3d %-16s %s" % (r["stt"], r["nv"],
                                      " ".join(rc["ma"] for rc in r["rao_can"])))
    if len(kbc) > 15:
        p("      ... va %d ca nua" % (len(kbc) - 15))
    nn = [r for r in rows if r["dau_hieu_nguoi_nha"]]
    p("  HT co dau hieu NGUOI NHA (tep LTV): %d" % len(nn))
    p()
    p("-- POST " + "-" * 57)
    for k, v in collections.Counter(r["post"] for r in rows).most_common():
        cb = "" if v >= 10 else "   <-- chua du mau, khong xep hang"
        p("  %-34s %3d%s" % (k[:34], v, cb))
    p()
    p("Da ghi %s  (%d dong)" % (a.out, n))
    p()
    p("LUU Y: day la ket qua KHOP TU KHOA, dung de doi chieu con so.")
    p("Phan loai chot van la cua nguoi doc / tro ly. Lech thi tin ban doc tay.")
    out.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
