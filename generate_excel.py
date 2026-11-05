# coding: utf-8
import json
import os
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load properties
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "data", "properties.json")
with open(json_path, "r", encoding="utf-8") as f:
    props = json.load(f)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "진주퀸 매물관리대장"

# Ensure grid lines are visible
ws.views.sheetView[0].showGridLines = True

# Title Row (A1:Q1)
ws.merge_cells("A1:Q1")
title_cell = ws["A1"]
title_cell.value = f"진주퀸공인중개사사무소 전체 매물관리대장 (적요·동호수 포함) - {datetime.date.today().strftime('%Y년 %m월 %d일 기준')}"
title_cell.font = Font(name="맑은 고딕", size=15, bold=True, color="0F172A")
title_cell.alignment = Alignment(vertical="center", horizontal="left")
ws.row_dimensions[1].height = 36

# Subtitle Info Row (A2:Q2)
ws.merge_cells("A2:Q2")
sub_cell = ws["A2"]
sub_cell.value = "대표공인중개사: 황선숙 | 등록번호: 48170-2017-00038 | 연락처: 010-4670-7248 / 055-761-7248 | 소재지: 진주시 에나로 146, 105호 (라온프라이빗시티) | [보안] 적요란은 관리자 전용 정보입니다."
sub_cell.font = Font(name="맑은 고딕", size=9, color="475569")
sub_cell.alignment = Alignment(vertical="center", horizontal="left")
ws.row_dimensions[2].height = 20

# Header definition (17 columns)
headers = [
    ("No.", 6),
    ("매물상태", 12),
    ("네이버 매물번호", 16),
    ("매물유형", 12),
    ("거래유형", 10),
    ("매물명 (단지명/호칭)", 34),
    ("적요 (동·호수 / 비공개 메모)", 28), # Column 7: 관리자 전용 적요
    ("거래금액", 22),
    ("보증금(만원)", 13),
    ("월세(만원)", 12),
    ("소재지 위치", 26),
    ("전용면적(㎡/평)", 16),
    ("층수 / 방향", 16),
    ("관리비", 16),
    ("등록사진수", 11),
    ("중개사 매물특징 및 상세설명", 60),
    ("대표사진 링크", 30)
]

header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
header_memo_fill = PatternFill(start_color="78350F", end_color="78350F", fill_type="solid") # Warm Dark Amber
header_font = Font(name="맑은 고딕", size=10, bold=True, color="FFFFFF")
thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

ws.row_dimensions[4].height = 26
for col_idx, (h_name, width) in enumerate(headers, 1):
    cell = ws.cell(row=4, column=col_idx, value=h_name)
    cell.fill = header_memo_fill if col_idx == 7 else header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border
    col_letter = get_column_letter(col_idx)
    ws.column_dimensions[col_letter].width = width

# Style fills
sold_fill = PatternFill(start_color="FFE4E6", end_color="FFE4E6", fill_type="solid") # soft rose
sold_font = Font(name="맑은 고딕", size=10, bold=True, color="BE123C") # red
active_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # soft green
active_font = Font(name="맑은 고딕", size=10, bold=True, color="15803D") # green
memo_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # soft amber
memo_font = Font(name="맑은 고딕", size=9.5, bold=True, color="92400E")
data_font = Font(name="맑은 고딕", size=9, color="1E293B")

for row_idx, prop in enumerate(props, 5):
    ws.row_dimensions[row_idx].height = 24
    is_sold = prop.get("status") == "SOLD"
    
    # 1. No.
    c1 = ws.cell(row=row_idx, column=1, value=row_idx - 4)
    c1.alignment = Alignment(horizontal="center", vertical="center")
    
    # 2. 매물상태
    status_label = "거래완료" if is_sold else "진행중 (추천)"
    c2 = ws.cell(row=row_idx, column=2, value=status_label)
    c2.fill = sold_fill if is_sold else active_fill
    c2.font = sold_font if is_sold else active_font
    c2.alignment = Alignment(horizontal="center", vertical="center")

    # 3. 네이버 매물번호
    c3 = ws.cell(row=row_idx, column=3, value=prop.get("naverArticleNo") or "-")
    c3.alignment = Alignment(horizontal="center", vertical="center")

    # 4. 매물유형
    c4 = ws.cell(row=row_idx, column=4, value=prop.get("category", "-"))
    c4.alignment = Alignment(horizontal="center", vertical="center")

    # 5. 거래유형
    c5 = ws.cell(row=row_idx, column=5, value=prop.get("transactionType", "-"))
    c5.alignment = Alignment(horizontal="center", vertical="center")

    # 6. 매물명
    c6 = ws.cell(row=row_idx, column=6, value=prop.get("title", "-"))
    c6.alignment = Alignment(horizontal="left", vertical="center")
    c6.font = Font(name="맑은 고딕", size=9.5, bold=True, color="0F172A")

    # 7. 적요 (동·호수 / 비공개 메모)
    memo_val = prop.get("adminMemo", "") or "-"
    c7 = ws.cell(row=row_idx, column=7, value=memo_val)
    c7.alignment = Alignment(horizontal="left", vertical="center")
    c7.font = memo_font
    c7.fill = memo_fill

    # 8. 거래금액
    c8 = ws.cell(row=row_idx, column=8, value=prop.get("priceFormatted", "-"))
    c8.alignment = Alignment(horizontal="center", vertical="center")
    c8.font = Font(name="맑은 고딕", size=9.5, bold=True, color="B45309")

    # 9. 보증금
    dep_val = prop.get("deposit", 0)
    c9 = ws.cell(row=row_idx, column=9, value=f"{dep_val:,}" if dep_val else "-")
    c9.alignment = Alignment(horizontal="right", vertical="center")

    # 10. 월세
    rent_val = prop.get("monthlyRent", 0)
    c10 = ws.cell(row=row_idx, column=10, value=f"{rent_val:,}" if rent_val else "-")
    c10.alignment = Alignment(horizontal="right", vertical="center")

    # 11. 소재지 위치
    c11 = ws.cell(row=row_idx, column=11, value=prop.get("location", "-"))
    c11.alignment = Alignment(horizontal="left", vertical="center")

    # 12. 전용면적
    ex_m2 = prop.get("exclusiveArea", "-")
    ex_py = prop.get("exclusiveAreaPyeong", "-")
    c12 = ws.cell(row=row_idx, column=12, value=f"{ex_m2}㎡ ({ex_py}평)")
    c12.alignment = Alignment(horizontal="center", vertical="center")

    # 13. 층수 / 방향
    floor_dir = f"{prop.get('floor', '-')} / {prop.get('direction', '-')}"
    c13 = ws.cell(row=row_idx, column=13, value=floor_dir)
    c13.alignment = Alignment(horizontal="center", vertical="center")

    # 14. 관리비
    c14 = ws.cell(row=row_idx, column=14, value=prop.get("maintenanceFee", "-"))
    c14.alignment = Alignment(horizontal="center", vertical="center")

    # 15. 등록사진수
    imgs = prop.get("images", [])
    c15 = ws.cell(row=row_idx, column=15, value=f"{len(imgs)}장")
    c15.alignment = Alignment(horizontal="center", vertical="center")

    # 16. 중개사 매물설명
    desc_val = prop.get("description", "").replace("\n", " ")
    c16 = ws.cell(row=row_idx, column=16, value=desc_val[:200])
    c16.alignment = Alignment(horizontal="left", vertical="center")

    # 17. 대표사진 링크
    first_img = imgs[0] if imgs else ""
    c17 = ws.cell(row=row_idx, column=17, value=first_img)
    if first_img.startswith("http"):
        c17.hyperlink = first_img
        c17.font = Font(name="맑은 고딕", size=8.5, color="2563EB", underline="single")
    c17.alignment = Alignment(horizontal="left", vertical="center")

    # Borders & base font for all cells in this row
    for col_i in range(1, len(headers) + 1):
        c = ws.cell(row=row_idx, column=col_i)
        c.border = thin_border
        if col_i not in [2, 6, 7, 8, 17]:
            c.font = data_font

output_path = os.path.join(BASE_DIR, "진주퀸공인중개사_매물관리대장.xlsx")
wb.save(output_path)
print(f"Excel file created successfully: {output_path} (Total properties: {len(props)})")
