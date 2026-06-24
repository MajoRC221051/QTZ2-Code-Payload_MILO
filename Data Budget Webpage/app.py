import streamlit as st

st.set_page_config(
    page_title="Payload-MILO Data Budget Calculator",
    page_icon="🛰",
    layout="wide",
)

# Ocultar sidebar y navegación automática de Streamlit
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }
    .block-container { padding-top: 2rem; max-width: 860px; margin: auto; }

    .cam-btn-card {
        background: #c8cfd8;
        border: 1px solid #aaa;
        border-radius: 6px;
        padding: 1.1rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 500;
        text-align: center;
        color: #111;
        cursor: pointer;
        margin-bottom: 0.75rem;
        transition: background 0.15s;
    }
    .cam-btn-card:hover { background: #b0bac7; }

    .select-label {
        text-align: center;
        font-weight: 700;
        color: #1a9fd4;
        font-size: 0.9rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1.25rem;
    }
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        color: #111;
        line-height: 1.15;
        margin-bottom: 0.4rem;
    }
    .main-sub {
        text-align: center;
        color: #bbb;
        font-size: 1rem;
        letter-spacing: 1px;
        margin-bottom: 2rem;
    }
    .logo-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
</style>
""", unsafe_allow_html=True)

# ── Logos (4 imágenes — reemplaza los src con tus archivos) ──────────────────
# Para usar imágenes reales, pon los archivos en la misma carpeta y usa:
#   st.image("logo_laboratorio.png", width=70)
# dentro de cada columna.

logo1, logo2, logo3, logo4, _ = st.columns([1, 1, 1, 1, 2])

with logo1:
    # st.image("logo_laboratorio.png", width=70)
    st.markdown(
        '<div style="width:70px;height:70px;border-radius:50%;background:#003087;'
        'display:flex;align-items:center;justify-content:center;color:white;'
        'font-size:8px;font-weight:700;text-align:center;line-height:1.3;">'
        'LAB<br>AEROES<br>PACIAL</div>',
        unsafe_allow_html=True,
    )

with logo2:
    # st.image("logo_milo.png", width=100)
    st.markdown(
        '<p style="font-size:2rem;font-weight:900;color:#1a9fd4;margin:0;'
        'line-height:70px;">MILO 🛰</p>',
        unsafe_allow_html=True,
    )

with logo3:
    # st.image("logo_ingenieria.png", width=80)
    st.markdown(
        '<p style="font-size:0.6rem;font-weight:700;color:#333;line-height:1.4;'
        'margin:0;padding-top:14px;">DEPARTAMENTO DE<br>'
        '<strong>INGENIERÍA<br>MECÁNICA</strong></p>',
        unsafe_allow_html=True,
    )

with logo4:
    # st.image("logo_uvg.png", width=80)
    st.markdown(
        '<p style="font-size:1.3rem;font-weight:900;color:#003087;'
        'border-left:4px solid #003087;padding-left:6px;margin:0;'
        'padding-top:10px;line-height:1.2;">UVG<br>'
        '<span style="font-size:0.55rem;font-weight:400;">'
        'UNIVERSIDAD<br>DEL VALLE<br>DE GUATEMALA</span></p>',
        unsafe_allow_html=True,
    )

st.divider()

# ── Título ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">Payload-MILO Data Budget<br>Calculator</h1>',
            unsafe_allow_html=True)
st.markdown('<p class="main-sub">Quetzal-2 · Módulo de Cámara</p>',
            unsafe_allow_html=True)
st.markdown('<p class="select-label">Seleccione el componente</p>',
            unsafe_allow_html=True)

# ── Botones de selección ──────────────────────────────────────────────────────
_, c1, c2, _ = st.columns([1, 2, 2, 1])

with c1:
    if st.button("OpenMV Cam RT1062", use_container_width=True, key="btn_rt"):
        st.session_state["cam_selected"] = "OpenMV Cam RT1062"
        st.switch_page("pages/calculadora.py")

with c2:
    if st.button("OpenMV Cam H7 Plus", use_container_width=True, key="btn_h7"):
        st.session_state["cam_selected"] = "OpenMV Cam H7 Plus"
        st.switch_page("pages/calculadora.py")
