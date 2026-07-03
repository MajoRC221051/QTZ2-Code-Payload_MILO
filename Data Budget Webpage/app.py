import streamlit as st
import csv
import io
from datetime import datetime
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

st.set_page_config(
    page_title="Budget Calculator",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent

# //......Ventana / Vista control........

if "view" not in st.session_state:
    st.session_state["view"] = "home"

if "cam_selected" not in st.session_state:
    st.session_state["cam_selected"] = None

if "prev_view" not in st.session_state:
    st.session_state["prev_view"] = "home"


# ==================================================================
# ESTILOS COMPARTIDOS (botones, tarjetas, layout general)
# ==================================================================
def inject_global_css():
    st.markdown("""
        <style>

            /* ---------- Botones (look profesional) ---------- */
            .stButton>button {
                background: linear-gradient(180deg, #6B7280 0%, #374151 100%);
                color: #FFFFFF;
                border: none;
                width: 100%;
                padding: 0.75rem 1.2rem;
                font-size: 15px;
                font-weight: 600;
                letter-spacing: 0.2px;
                border-radius: 10px;
                box-shadow: 0 2px 6px rgba(21, 101, 192, 0.35);
                transition: all 0.18s ease-in-out;
            }
            .stButton>button:hover {
                background: linear-gradient(180deg, #1E88E5 0%, #0D47A1 100%);
                box-shadow: 0 4px 10px rgba(13, 71, 161, 0.45);
                transform: translateY(-1px);
                color: #FFFFFF;
                border: none;
            }
            .stButton>button:active {
                transform: translateY(0px);
                box-shadow: 0 2px 4px rgba(13, 71, 161, 0.35);
            }
            .stButton>button:focus:not(:active) {
                color: #FFFFFF;
                border: none;
                box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.35);
            }

            /* Botones secundarios, ej. Back / About */
            .secondary-btn .stButton>button {
                background: #FFFFFF;
                color: #1565C0;
                border: 1.5px solid #BBDEFB;
                box-shadow: none;
                white-space: nowrap;
            }
            .secondary-btn .stButton>button:hover {
                background: #E3F2FD;
                border: 1.5px solid #90CAF9;
                color: #0D47A1;
                box-shadow: none;
                transform: none;
            }

            /* Botones de descarga */
            .stDownloadButton>button {
                background: #FFFFFF;
                color: #1565C0;
                border: 1.5px solid #BBDEFB;
                width: 100%;
                padding: 0.75rem 1.2rem;
                font-size: 15px;
                font-weight: 600;
                border-radius: 10px;
                transition: all 0.18s ease-in-out;
            }
            .stDownloadButton>button:hover {
                background: #1565C0;
                color: #FFFFFF;
                border: 1.5px solid #1565C0;
                transform: translateY(-1px);
            }

            .stApp {
                background-color: #FFFFFF;
            }

        </style>
    """, unsafe_allow_html=True)


def render_logo_row():
    st.markdown("""
        <style>
            .st-key-logo_card {
                background-color: #F1F3F5;
                border-radius: 16px;
                padding: 1rem 1.5rem;
                margin-bottom: 2rem;
            }
            /* Todas las imagenes del bloque de logos comparten la misma altura
               y se alinean verticalmente al centro, sin importar su proporcion */
            .st-key-logo_card [data-testid="stHorizontalBlock"] {
                align-items: center;
            }
            .st-key-logo_card [data-testid="column"] {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .st-key-logo_card [data-testid="stImage"] {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
            }
            .st-key-logo_card [data-testid="stImage"] img {
                height: 48px;
                width: auto;
                max-width: 100%;
                object-fit: contain;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.container(key="logo_card"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image(str(BASE_DIR / "logo_uvg.png"))
        with col2:
            st.image(str(BASE_DIR / "logo_milo.png"))
        with col3:
            st.image(str(BASE_DIR / "logo_mecanica.png"))
        with col4:
            st.image(str(BASE_DIR / "logo-lab.png"))


# ==================================================================
# VENTANA 1: HOME
# ==================================================================
def render_home():
    inject_global_css()
    st.markdown("""
                    <style>
                        .hero-title {
                            text-align: center;
                            color: #0D47A1;
                            font-weight: 800;
                            font-size: 2.6rem;
                            letter-spacing: -0.5px;
                            margin-bottom: 0.3rem;
                        }
                        .hero-subtitle {
                            text-align: center;
                            color: #6B7280;
                            font-size: 1.1rem;
                            margin-bottom: 1.5rem;
                        }
                        .section-label {
                            text-align: center;
                            color: #1E293B;
                            font-weight: 700;
                            font-size: 1.3rem;
                            margin-bottom: 1.2rem;
                        }
                        .st-key-card_rt1062, .st-key-card_h7plus {
                            background-color: #EAF7EF;
                            border-radius: 14px;
                            padding: 1.5rem 1rem 1rem 1rem;
                            text-align: center;
                            margin-bottom: 0.5rem;
                        }
                    </style>
                """, unsafe_allow_html=True)

    render_logo_row()

    st.sidebar.title("Payload-MILO Data Budget Calculator")

    top_l, top_r = st.columns((6, 1))
    with top_r:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state["prev_view"] = "home"
            st.session_state["view"] = "about"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='hero-title'>Payload-MILO Data Budget Calculator</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Tool for calculating the payload's data budget</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='section-label'>Select the component</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.container(key="card_rt1062"):
            if st.button("OpenMV Cam RT1062"):
                st.session_state["cam_selected"] = "OpenMV Cam RT1062"
                st.session_state["view"] = "calculator"
                st.rerun()
    with col2:
        with st.container(key="card_h7plus"):
            if st.button("OpenMV Cam H7 Plus"):
                st.session_state["cam_selected"] = "OpenMV Cam H7 Plus"
                st.session_state["view"] = "calculator"
                st.rerun()


# ==================================================================
# VENTANA 2: CALCULATOR
# ==================================================================
def render_calculator():

    # //......Data Budget Calculator Window ........

    inject_global_css()

    # 3. CSS (Style)

    st.markdown("""
    <style>

    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }

    .stApp {
        background-color: #FFFFFF;
    }

    .block-container {
        padding-top: 1rem;
        max-width: 1200px;
    }

    .main-title{
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 1rem;
    }

    .st-key-camera_panel, .st-key-mission_panel {
        background-color: #EAF7EF;
        border-radius: 18px;
        padding: 1.3rem 1.5rem 0.5rem 1.5rem;
        margin-bottom: 1rem;
    }

    .panel-title{
        font-size:1.1rem;
        font-weight:700;
        color:#1E293B;
        margin-bottom:1rem;
    }

    div[data-testid="stSelectbox"],
    div[data-testid="stNumberInput"],
    div[data-testid="stSlider"]{
        margin-bottom: 0.2rem;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSlider"] label{
        color:#1E293B !important;
        font-weight:600;
    }

    div[data-testid="stSelectbox"] > div,
    div[data-testid="stNumberInput"] > div{
        border-radius: 10px;
        background-color:#FFFFFF;
    }

    .stNumberInput input{
        text-align:center;
        font-size:16px !important;
        font-weight:600;
    }

    .field-range{
        font-size:0.78rem;
        color:#6B7280;
        margin-top:-0.6rem;
        margin-bottom:1rem;
    }

    .metric-grid{
        display:grid;
        grid-template-columns: repeat(4, 1fr);
        gap:1rem;
        margin-top:1.5rem;
        margin-bottom: 1.5rem;
    }

    .metric-card{
        background:#F1F3F5;
        border-radius:20px;
        padding:1.2rem;
        text-align:center;
    }

    .metric-label{
        font-size:0.9rem;
        color:#6B7280;
        margin-bottom:0.5rem;
    }

    .metric-value{
        font-size:2rem;
        font-weight:700;
        color:#1E293B;
    }

    .metric-unit{
        font-size:0.9rem;
        color:#9CA3AF;
    }

    .stContainer{
        border-radius:15px;
    }

    .section-title{
        font-size:1.2rem;
        font-weight:600;
        margin-bottom:1rem;
    }

    /* Header con boton Back / About: evita que el texto se corte */
    div[data-testid="column"] .secondary-btn .stButton>button{
        min-width: 100px;
        white-space: nowrap;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    /* Barra de almacenamiento tipo "slider" */
    .stor-bar-track{
        width:100%;
        height:14px;
        background:#EDEFF2;
        border-radius:7px;
        overflow:hidden;
        margin: 0.6rem 0 0.3rem 0;
    }

    </style>
    """, unsafe_allow_html=True)

    # 3. Header

    cam_sel = st.session_state["cam_selected"]

    hcol, bcol1, bcol2 = st.columns((5, 1, 1))
    with hcol:
        st.markdown(
        "<div class='main-title'>Data Budget Calculator</div>",
        unsafe_allow_html=True
    )
    with bcol1:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state["prev_view"] = "calculator"
            st.session_state["view"] = "about"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with bcol2:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("← Back", use_container_width=True):
            st.session_state["view"] = "home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Variables definition

    Resolutions = {
         "5 MP — 2592×1944": (2592, 1944),
        "3 MP — 2048×1536": (2048, 1536),
        "1 MP — 1280×960":  (1280, 960),
        "VGA — 640×480":    (640,  480),
        "QVGA — 320×240":   (320,  240),
    }

    Formats = ["RGB565", "Grayscale", "JPEG (Compressed)"] # Image format

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

    col_cam, col_mission = st.columns(2)

    with col_cam:
        with st.container(key="camera_panel"):
            st.markdown('<div class="panel-title">📷 Camera Configuration</div>', unsafe_allow_html=True)

            cam_sel = st.selectbox(
                "Camera",
                list(CAM_INFO.keys()),
                index=list(CAM_INFO.keys()).index(cam_sel) if cam_sel in CAM_INFO else 0
            )
            st.session_state["cam_selected"] = cam_sel

            fmt_sel = st.selectbox(
                "Image Format",
                Formats
            )

            res_sel = st.selectbox(
                "Resolution",
                list(Resolutions.keys())
            )

            jpeg_q = st.slider(
                "JPEG Quality",
                10, 100, 80
            )

    with col_mission:
        with st.container(key="mission_panel"):
            st.markdown('<div class="panel-title">🛰️ Mission Parameters</div>', unsafe_allow_html=True)

            imgs_orbit = st.number_input(
                "Images per orbit",
                min_value=1, max_value=100, value=10
            )
            st.markdown('<div class="field-range">Min: 1 — Max: 100</div>', unsafe_allow_html=True)

            orbits_day = st.number_input(
                "Orbits per day",
                min_value=1, max_value=30, value=15
            )
            st.markdown('<div class="field-range">Min: 1 — Max: 30</div>', unsafe_allow_html=True)

            mission_days = st.number_input(
                "Mission duration (days)",
                min_value=1, max_value=365, value=20
            )
            st.markdown('<div class="field-range">Min: 1 — Max: 365</div>', unsafe_allow_html=True)

            stor_gb = st.number_input(
                "Available storage (GB)",
                min_value=1, max_value=128, value=32
            )
            st.markdown('<div class="field-range">Min: 1 — Max: 128</div>', unsafe_allow_html=True)

    c = CAM_INFO[cam_sel]

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
            <div class="metric-value">{img_v}<span class="metric-unit">{img_u}</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Data per Orbit</div>
            <div class="metric-value">{orb_v}<span class="metric-unit">{orb_u}</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Data per Day</div>
            <div class="metric-value">{day_v}<span class="metric-unit">{day_u}</span></div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Mission Total</div>
            <div class="metric-value">{tot_v}<span class="metric-unit">{tot_u}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 9. Storage bar + slider

    with st.container(border=True):
        st.markdown('<div class="panel-title" style="margin-bottom:0.4rem;">💾 Storage usage</div>', unsafe_allow_html=True)
        ca, cb = st.columns(2)
        ca.markdown(f"**{tot_v} {tot_u}** used")
        cb.markdown(
            f"<div style='text-align:right'>of {stor_gb} GB available</div>",
            unsafe_allow_html=True,
        )
        st.markdown(storage_bar_html(pct, over), unsafe_allow_html=True)
        if over:
            st.error("⚠ The total exceeds the available storage. Reduce images or change format")
        else:
            st.caption(f"{pct:.1f}% used")

        # Slider adicional (solo lectura visual) que muestra el nivel de memoria usado
        st.slider(
            "Memory used (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(min(pct, 100.0)),
            disabled=True,
            format="%.1f%%",
        )

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    # 10. CSV (Technical summary)

    fmt_label = {
        "RGB565":            "RGB565 (2 bpp)",
        "Grayscale":         "Grayscale (1 bpp)",
        "JPEG (Compressed)": f"JPEG (~{bits:.2f} bpp @ {jpeg_q}%)",
    }[fmt_sel]

    res_short = res_sel.split("—")[0].strip()
    c = CAM_INFO[cam_sel]

    rows = [
        # ("Camera",             cam_sel),
        ("Processor",         c["proc"]),
        ("RAM / Flash",        f"{c['ram']} / {c['flash']}"),
        ("SD Speed",           c["usd"]),
        ("USB Interface",       c["usb"]),
        ("Resolution",         f"{res_short} ({w}x{h})"),
        ("Format",            fmt_label),
        ("Pixels per image",  f"{w*h}"),
        ("Bytes per image",   f"{int(img_bytes)} B"),
        ("Size per image",  f"{img_v} {img_u}"),
        ("Images/orbit",    imgs_orbit),
        ("Data/orbit",       f"{orb_v} {orb_u}"),
        ("Orbits/day",        orbits_day),
        ("Data/day",          f"{day_v} {day_u}"),
        ("Mission days",     mission_days),
        ("Generated Total",     f"{tot_v} {tot_u}"),
        ("Available Storage", f"{stor_gb} GB"),
        ("Usage",        f"{pct:.1f}%"),
        ("Generated",           datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ]

    def build_csv(rows: list) -> bytes:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Parameter", "Value"])
        writer.writerow(["Payload-MILO Data Budget — Quetzal-2", ""])
        writer.writerow([])
        for k, v in rows:
            writer.writerow([k, v])
        return buf.getvalue().encode("utf-8-sig")   # utf-8-sig opens correctly in Excel

    csv_bytes = build_csv(rows)
    filename  = f"MILO_DataBudget_{cam_sel.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            label="📥 Print Technical Breakdown (CSV)",
            data=csv_bytes,
            file_name=filename,
            mime="text/csv",
            use_container_width=True,
        )

    # 11. PDF (Technical Report)


    def build_pdf():
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        # elements is a list that will hold the content of the PDF
        elements = []

        title = Paragraph(
            "<b><font color='#1E88E5' size=18>"
            "Payload-MILO Data Budget Report"
            "</font></b>",
            styles["Heading1"],
        )

        elements.append(title)
        elements.append(Spacer(1, 0.25 * inch))

        data = [
            ["Parameter", "Value"],
        ]
        
        for k, v in rows:
            data.append([str(k), str(v)])

        table = Table(data, colWidths=[180, 280])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1E88E5")),
            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

            ("TOPPADDING",(0,1),(-1,-1),8),

            ("BOTTOMPADDING",(0,1),(-1,-1),8),
        ]))

        elements.append(table)
        elements.append(Spacer(1,0.3*inch))

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    pdf = build_pdf()

    with dl2:
        st.download_button(
            "📄 Download Technical Report (PDF)",
            data=pdf,
            file_name=f"MILO_DataBudget_{cam_sel}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# ==================================================================
# VENTANA 3: ABOUT
# ==================================================================
def render_about():
    inject_global_css()

    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        .about-title{
            font-size: 2rem;
            font-weight: 700;
            color: #1E293B;
            margin-bottom: 0.2rem;
        }
        .about-subtitle{
            color:#6B7280;
            font-size:1rem;
            margin-bottom:1.2rem;
        }
        .about-card{
            background-color:#F8F9FA;
            border-radius:16px;
            padding:1.4rem 1.6rem;
            margin-bottom:1.2rem;
        }
        .about-card h4{
            color:#0D47A1;
            margin-top:0;
            margin-bottom:0.8rem;
        }
        .param-table{
            width:100%;
            border-collapse:collapse;
        }
        .param-table th{
            text-align:left;
            color:#1E293B;
            font-size:0.85rem;
            text-transform:uppercase;
            letter-spacing:0.4px;
            padding:0.5rem 0.6rem;
            border-bottom:2px solid #E2E8F0;
        }
        .param-table td{
            padding:0.55rem 0.6rem;
            border-bottom:1px solid #EDF2F7;
            font-size:0.92rem;
            color:#1E293B;
            vertical-align:top;
        }
        .param-table td.sym{
            font-weight:700;
            color:#1565C0;
            white-space:nowrap;
        }
        </style>
    """, unsafe_allow_html=True)

    render_logo_row()

    top_l, top_r = st.columns((6, 1))
    with top_r:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("← Back", use_container_width=True):
            st.session_state["view"] = st.session_state.get("prev_view", "home")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='about-title'>About Payload-MILO Data Budget Calculator</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='about-subtitle'>What this tool is, how it works, and what each parameter means.</div>",
        unsafe_allow_html=True,
    )

    # ---- Que es la herramienta ----
    with st.container():
        st.markdown("""
            <div class="about-card">
                <h4>🛰️ What is this tool?</h4>
                <p style="color:#334155; line-height:1.6;">
                The <b>Payload-MILO Data Budget Calculator</b> is a support tool for the MILO payload team.
                It estimates how much image data the onboard camera will generate during a mission and
                compares that volume against the satellite's available on-board storage. This helps the
                team choose a camera, image format, resolution and mission cadence that keep the data
                budget within the storage limits of the platform.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # ---- Metodologia (basada en la formulacion del payload) ----
    with st.container():
        st.markdown("""
            <div class="about-card">
                <h4>📐 Methodology</h4>
                <p style="color:#334155; line-height:1.6; margin-bottom:0.8rem;">
                The data budget is built up in stages: first the size of a single image, then the data
                produced per orbit, per day, and finally over the full mission. The core relationships are:
                </p>
        """, unsafe_allow_html=True)

        st.latex(r"N_{id} = N_{o} \times N_{io}")
        st.latex(r"T_{id} = N_{id} \times \big[N_b \times (1+\alpha)\big]")

        st.markdown("""
                <table class="param-table">
                    <tr><th>Symbol</th><th>Meaning</th></tr>
                    <tr><td class="sym">I<sub>r</sub></td><td>Total image resolution (pixels).</td></tr>
                    <tr><td class="sym">I<sub>b</sub></td><td>Image block / colour depth (RGB, grayscale, etc.).</td></tr>
                    <tr><td class="sym">N<sub>b</sub></td><td>Number of bytes generated per image.</td></tr>
                    <tr><td class="sym">α</td><td>Data and telemetry overhead percentage (headers, housekeeping, protocol overhead).</td></tr>
                    <tr><td class="sym">N<sub>o</sub></td><td>Number of orbits per day.</td></tr>
                    <tr><td class="sym">N<sub>io</sub></td><td>Number of images captured per orbit.</td></tr>
                    <tr><td class="sym">N<sub>id</sub></td><td>Number of images captured per day (N<sub>o</sub> × N<sub>io</sub>).</td></tr>
                    <tr><td class="sym">T<sub>id</sub></td><td>Total data generated per day, including overhead.</td></tr>
                </table>
                <p style="color:#64748B; font-size:0.85rem; margin-top:0.8rem;">
                In the calculator, image size is derived from resolution × bits-per-pixel (which depends on
                the selected format and, for JPEG, the compression quality). That per-image size is then
                scaled by images/orbit, orbits/day and mission duration to obtain the mission total, which
                is compared against the available storage.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # ---- Parametros de la calculadora ----
    with st.container():
        st.markdown("""
            <div class="about-card">
                <h4>⚙️ Calculator parameters</h4>
                <table class="param-table">
                    <tr><th>Parameter</th><th>Description</th></tr>
                    <tr><td class="sym">Camera</td><td>Selects the OpenMV camera model (RT1062 or H7 Plus), which sets the processor, RAM/flash and interface speeds used in the technical report.</td></tr>
                    <tr><td class="sym">Image Format</td><td>Pixel encoding used to store each image: RGB565 (2 bytes/pixel), Grayscale (1 byte/pixel), or JPEG (compressed, size depends on quality).</td></tr>
                    <tr><td class="sym">Resolution</td><td>Image width × height in pixels. Higher resolution means larger images and more data generated.</td></tr>
                    <tr><td class="sym">JPEG Quality</td><td>Compression quality (10–100%) used only when JPEG format is selected; higher quality produces larger files.</td></tr>
                    <tr><td class="sym">Images per orbit</td><td>Number of images captured during a single orbit.</td></tr>
                    <tr><td class="sym">Orbits per day</td><td>Number of orbits the satellite completes in one day.</td></tr>
                    <tr><td class="sym">Mission duration (days)</td><td>Total planned length of the mission, in days.</td></tr>
                    <tr><td class="sym">Available storage (GB)</td><td>On-board storage capacity available for payload images.</td></tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

    # ---- Resultados ----
    with st.container():
        st.markdown("""
            <div class="about-card">
                <h4>📊 Results</h4>
                <table class="param-table">
                    <tr><th>Metric</th><th>Description</th></tr>
                    <tr><td class="sym">Image Size</td><td>Data generated by a single image, given resolution and format.</td></tr>
                    <tr><td class="sym">Data per Orbit</td><td>Image size × images per orbit.</td></tr>
                    <tr><td class="sym">Data per Day</td><td>Data per orbit × orbits per day.</td></tr>
                    <tr><td class="sym">Mission Total</td><td>Data per day × mission duration — the full data budget for the mission.</td></tr>
                    <tr><td class="sym">Storage usage</td><td>Mission total as a percentage of the available on-board storage; a warning appears if it exceeds 100%.</td></tr>
                </table>
                <p style="color:#64748B; font-size:0.85rem; margin-top:0.8rem;">
                You can export the full technical breakdown as a CSV file or a formatted PDF report
                from the calculator window.
                </p>
            </div>
        """, unsafe_allow_html=True)


# ==================================================================
# ROUTER
# ==================================================================
if st.session_state["view"] == "home":
    render_home()
elif st.session_state["view"] == "about":
    render_about()
else:
    render_calculator()
