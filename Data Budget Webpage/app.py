import streamlit as st
st.markdown("""
                <style>
                    
                    .stButton>button {
                        background-color: #1E88E5;
                        color: white;
                        border: none;
                        width: 100%;
                        
                        
                        padding: 0.9rem 1.2rem;
                        font-size: 16px;
                        border-radius: 10px;
                        transition:0.2s;
                    }
                    .stButton>button:hover {
                        background-color: #1565C0;
                        transform: scale(1.05);
                    }
                    .stApp {
                        background: linear-gradient(180deg, #F5F9FF 0%, #FFFFFF 35%);
                    }
                    .logo-card {
                        background-color: #FFFFFF;
                        border-radius: 16px;
                        padding: 1.2rem 1rem;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
                        margin-bottom: 2rem;
                    }
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
                    .component-card {
                        background-color: #FFFFFF;
                        border-radius: 14px;
                        padding: 1.5rem 1rem 1rem 1rem;
                        box-shadow: 0 4px 14px rgba(0,0,0,0.07);
                        text-align: center;
                        margin-bottom: 0.5rem;
                    }
                </style>
            """, unsafe_allow_html=True)
from pathlib import Path
import streamlit as st
BASE_DIR = Path(__file__).resolve().parent
st.markdown('<div class="logo-card">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image(BASE_DIR / "logo_uvg.png", width=60)
with col2:
    st.image(BASE_DIR / "logo_milo.png", width=120)
with col3:
    st.image(BASE_DIR / "logo_mecanica.png", width=90)
with col4:
    st.image(BASE_DIR / "logo-lab.png", width=60)
st.markdown('</div>', unsafe_allow_html=True)
st.sidebar.title("Payload-MILO Data Budget Calculator")
st.markdown("<div class='hero-title'>Payload-MILO Data Budget Calculator</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Herramienta para el cálculo del presupuesto de datos del payload</div>", unsafe_allow_html=True)
st.divider()
st.markdown("<div class='section-label'>Seleccione el componente</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="component-card">', unsafe_allow_html=True)
    if st.button("OpenMV Cam RT1062"):
        st.session_state["cam_selected"] = "OpenMV Cam RT1062"
        st.switch_page("calculator.py")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="component-card">', unsafe_allow_html=True)
    if st.button("OpenMV Cam H7 Plus"):
        st.session_state["cam_selected"] = "OpenMV Cam H7 Plus"
        st.switch_page("calculator.py")
    st.markdown('</div>', unsafe_allow_html=True)
