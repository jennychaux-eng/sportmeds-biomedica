import streamlit as st

def topbar(titulo, ruta):
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">{titulo}</div>
            <div class="topbar-crumb">INICIO › {ruta}</div>
        </div>
        <div class="topbar-user">👤 &nbsp; </div>
    </div>
    """, unsafe_allow_html=True)
