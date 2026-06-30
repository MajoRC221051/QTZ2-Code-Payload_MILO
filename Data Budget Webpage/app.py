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
                </style>
            """, unsafe_allow_html=True)

st.logo("logo-lab.png", size="large")
st.sidebar.title("Payload-MILO Data Budget Calculator")
st.title(" :blue[Payload-MILO] Data Budget Calculator", text_alignment="center")

st.divider()

st.subheader("Seleccione el componente")
col1, col2 = st.columns(2)

with col1:
    if st.button("OpenMV Cam RT1062"):
        st.session_state["cam_selected"] = "OpenMV Cam RT1062"
        st.switch_page("Pages/calculator.py")
with col2:
    if st.button("OpenMV Cam H7 Plus"):
        st.session_state["cam_selected"] = "OpenMV Cam H7 Plus"
        st.switch_page("Pages/calculator.py")



