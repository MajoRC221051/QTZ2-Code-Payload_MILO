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
                    .main-title {
                        text-align: center;
                        color: #1E88E5;
                        font-weight: 700;
                        margin-bottom: 0.2rem;
                    }
                    .main-subtitle {
                        text-align: center;
                        color: #555555;
                        margin-bottom: 1.5rem;
                    }
                </style>
            """, unsafe_allow_html=True)
from pathlib import Path
import streamlit as st
BASE_DIR = Path(__file__).resolve().parent
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image(BASE_DIR / "logo_uvg.png", width=60)
with col2:
    st.image(BASE_DIR / "logo_milo.png", width=120)
with col3:
    st.image(BASE_DIR / "logo_mecanica.png", width=90)
with col4:
    st.image(BASE_DIR / "logo-lab.png", width=60)
st.sidebar.title("Payload-MILO Data Budget Calculator")
st.markdown("<h1 class='main-title'>Payload-MILO Data Budget Calculator</h1>", unsafe_allow_html=True)
st.divider()
st.markdown("<h3 class='main-subtitle'>Seleccione el componente</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    if st.button("OpenMV Cam RT1062"):
        st.session_state["cam_selected"] = "OpenMV Cam RT1062"
        st.switch_page("pages/calculator.py")
with col2:
    if st.button("OpenMV Cam H7 Plus"):
        st.session_state["cam_selected"] = "OpenMV Cam H7 Plus"
        st.switch_page("pages/calculator.py")
