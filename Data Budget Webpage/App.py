import streamlit as st

st.set_page_config(
    page_title=" QUETZAL 2 | Payload-MILO Data Budget Calculator",
    page_icon="🛰",
    layout="wide",
)


# Selection buttons
_, c1, c2, _ = st.columns([1, 2, 2, 1])

with c1:
    if st.button("OpenMV Cam RT1062", use_container_width=True, key="btn_rt"):
        st.session_state["cam_selected"] = "OpenMV Cam RT1062"
        st.switch_page("pages/calculadora.py")

with c2:
    if st.button("OpenMV Cam H7 Plus", use_container_width=True, key="btn_h7"):
        st.session_state["cam_selected"] = "OpenMV Cam H7 Plus"
        st.switch_page("pages/calculadora.py")
