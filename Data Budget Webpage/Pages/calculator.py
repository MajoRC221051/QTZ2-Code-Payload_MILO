

# //......Data Budget Calculator Window ........

# 1. Libraries import

import streamlit as st
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="Budget Calculator",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Force to select a cam

# if "cam_selected" not in st.session_state:
#  st.switch("app.py")

# 3. CSS (Style)

st.markdown("""
<style>

[data-testid="stSidebar"] { display: none; }
[data-testid="stSidebarNav"] { display: none; }

.stApp {
    background-color: #f5f7f5;
}

.block-container {
    padding-top: 1rem;
    max-width: 1200px;
}



.main-title{
    font-size: 2rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 1rem;
}



div[data-testid="stSelectbox"],
div[data-testid="stNumberInput"]{
    margin-bottom: 0.6rem;
}

div[data-testid="stSelectbox"] > div,
div[data-testid="stNumberInput"] > div{
    border-radius: 10px;
}


.stNumberInput input{
    text-align:center;
    font-size:16px !important;
    font-weight:600;
}



.metric-grid{
    display:grid;
    grid-template-columns: repeat(4, 1fr);
    gap:1rem;
    margin-top:1rem;
}

.metric-card{
    background:#e6e6e6;
    border-radius:20px;
    padding:1rem;
    text-align:center;
}

.metric-label{
    font-size:0.9rem;
    color:#333;
    margin-bottom:0.5rem;
}

.metric-value{
    font-size:2rem;
    font-weight:700;
    color:#111;
}

.metric-unit{
    font-size:0.9rem;
    color:#555;
}



.stContainer{
    border-radius:15px;
}



.config-box{
    background:#eef3ef;
    padding:1rem;
    border-radius:10px;
    height:100%;
}

.section-title{
    font-size:1.2rem;
    font-weight:600;
    margin-bottom:1rem;
}

</style>
""", unsafe_allow_html=True)

st.title("Data Budget Calculator")
left, right = st.columns(2)

  # 3. Header

#cam_name = st.session_state["cam_selected"]

hcol, bcol = st.columns((6,2))
with hcol:
    st.markdown(
    "<div class='main-title'>Data Budget Calculator</div>",
    unsafe_allow_html=True
)
#with bcol:
    # if st.button("← Volver", use_container_width=True):
    #    st.switch_page("app.py")

# 4. Variables definition

Resolutions = {
     "5 MP — 2592×1944": (2592, 1944),
    "3 MP — 2048×1536": (2048, 1536),
    "1 MP — 1280×960":  (1280, 960),
    "VGA — 640×480":    (640,  480),
    "QVGA — 320×240":   (320,  240),
}

Formats = ["RGB565", "Grayscale", "JPEG (Compressed)"] # Image format

res_sel = st.selectbox(
    "Resolution",
    list(Resolutions.keys())
)

fmt_sel = st.selectbox(
    "Format",
    Formats
)

jpeg_q = st.slider(
    "JPEG Quality",
    10, 100, 80
)

imgs_orbit = st.number_input(
    "Images per orbit",
    min_value=1,
    value=10
)

orbits_day = st.number_input(
    "Orbits per day",
    min_value=1,
    value=15
)

mission_days = st.number_input(
    "Mission days",
    min_value=1,
    value=30
)

stor_gb = st.number_input(
    "Storage (GB)",
    min_value=1,
    value=32
)

#cam_sel = cam_name



CAM_INFO = {
    "OpenMV Cam H7 Plus": {
        "proc":  "STM32H743II @ 480 MHz",
        "ram":   "32 MB SDRAM",
        "flash": "32 MB ext. flash",
        "usd":   "100 MB/s",
        "usb":   "USB 12 Mb/s",
    },
    "OpenMV Cam RT1062": {
        "proc":  "RT1062 @ 600 MHz",
        "ram":   "32 MB SDRAM",
        "flash": "16 MB flash",
        "usd":   "25 MB/s",
        "usb":   "USB-C 480 Mb/s",
    },
}

#cam_sel = st.selectbox(
#    "Camera",
#    list(CAM_INFO.keys())
#)

# c = CAM_INFO[cam_sel]

# 5. Helpers

def bpp(fmt: str, jpeg_q: int) -> float:
    if fmt == "Grayscale":   return 1.0
    if fmt == "RGB565":      return 2.0
    return 2.0 / (jpeg_q / 10.0)

def smart_unit(mb: float) -> tuple[float, str]:
    if mb >= 1024: return round(mb / 1024, 2), "GB"
    return round(mb, 2), "MB"

def storage_bar_html(pct: float, over: bool) -> str:
    color   = "#c0392b" if over else ("#e67e22" if pct > 75 else "#1a9fd4")
    clamped = min(pct, 100)
    return (
        f'<div class="stor-bar-track">'
        f'<div style="height:100%;width:{clamped:.1f}%;background:{color};'
        f'border-radius:7px;"></div></div>'
    )




# 7. Mission Calculations

w, h      = Resolutions[res_sel]
bits      = bpp(fmt_sel, jpeg_q)
img_bytes = w * h * bits
img_mb    = img_bytes / (1024 ** 2)
orb_mb    = img_mb * imgs_orbit
day_mb    = orb_mb * orbits_day
tot_mb    = day_mb * mission_days
stor_mb   = stor_gb * 1024
pct       = (tot_mb / stor_mb) * 100
over      = pct > 100

img_v, img_u = smart_unit(img_mb)
orb_v, orb_u = smart_unit(orb_mb)
day_v, day_u = smart_unit(day_mb)
tot_v, tot_u = smart_unit(tot_mb)


# 8. Metric Cards

st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card">
        <div class="metric-label">Image Size</div>
        <div class="metric-value">{img_v}</div>
        <div class="metric-unit">{img_u}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Data per QZ2 Orbit</div>
        <div class="metric-value">{orb_v}</div>
        <div class="metric-unit">{orb_u}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Data per QZ2 Day</div>
        <div class="metric-value">{day_v}</div>
        <div class="metric-unit">{day_u}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">MILO´s Mission Total</div>
        <div class="metric-value">{tot_v}</div>
        <div class="metric-unit">{tot_u}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 9. Storage bar

with st.container(border=True):
    ca, cb = st.columns(2)
    ca.markdown(f"**{tot_v} {tot_u}** usados")
    cb.markdown(
        f"<div style='text-align:right'>de {stor_gb} GB Available</div>",
        unsafe_allow_html=True,
    )
    st.markdown(storage_bar_html(pct, over), unsafe_allow_html=True)
    if over:
        st.error("⚠ The total surpases the available storage. Reduce images or change format")
    else:
        st.caption(f"{pct:.1f}% used")

# 10. CSV (Techanical resumé)

fmt_label = {
    "RGB565":            "RGB565 (2 bpp)",
    "Grayscale":         "Grayscale (1 bpp)",
    "JPEG (Compressed)": f"JPEG (~{bits:.2f} bpp @ {jpeg_q}%)",
}[fmt_sel]

res_short = res_sel.split("—")[0].strip()
#c = CAM_INFO[cam_sel]

rows = [
    # ("Camera",             cam_sel),
    ("Processor",         c["proc"]),
    ("RAM / Flash",        f"{c['ram']} / {c['flash']}"),
    ("Vel. uSD",           c["usd"]),
    ("USB Interface",       c["usb"]),
    ("Resolution",         f"{res_short} ({w}x{h})"),
    ("Format",            fmt_label),
    ("Pixels per image",  f"{w*h}"),
    ("Bytes per image",   f"{int(img_bytes)} B"),
    ("Size per imagen",  f"{img_v} {img_u}"),
    ("Images/orbit",    imgs_orbit),
    ("Data/orbit",       f"{orb_v} {orb_u}"),
    ("Orbits/day",        orbits_day),
    ("Data/day",          f"{day_v} {day_u}"),
    ("Days/mision",     mission_days),
    ("Generated Total",     f"{tot_v} {tot_u}"),
    ("Available Storage", f"{stor_gb} GB"),
    ("Usage",        f"{pct:.1f}%"),
    ("Generated",           datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
]

def build_csv(rows: list) -> bytes:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Parámetro", "Valor"])
    writer.writerow(["Payload-MILO Data Budget — Quetzal-2", ""])
    writer.writerow([])
    for k, v in rows:
        writer.writerow([k, v])
    return buf.getvalue().encode("utf-8-sig")   # utf-8-sig abre bien en Excel

csv_bytes = build_csv(rows)
filename  = f"MILO_DataBudget_{cam_sel.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

st.download_button(
    label="📥 Imprimir desglose técnico (CSV)",
    data=csv_bytes,
    file_name=filename,
    mime="text/csv",
    use_container_width=True,
)
