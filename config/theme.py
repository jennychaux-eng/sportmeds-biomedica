
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

* { font-family: 'DM Sans', sans-serif !important; }

.main .block-container {
    background-color: #ffffff !important;
    padd-top: 1.2rem !important;
    max-width: 100% !important;
}
.main { background-color: #ffffff !important; }
[data-testid="stAppViewContainer"] { background-color: #ffffff !important; }
[data-testid="stAppViewBlockContainer"] { background-color: #ffffff !important; }
section.main { background-color: #ffffff !important; }

section[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e8edf5 !important;
}
section[data-testid="stSidebar"] * { color: #0D2B52 !important; }
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] button * {
    color: white !important;
}
section[data-testid="stSidebar"] .stButton > button,
section[data-testid="stSidebar"] button {
    background: linear-gradient(135deg, #0D2B52, #1a8fd1) !important;
    border: none !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #F0F4F9 !important;
    border: 1px solid #dce5f0 !important;
    border-radius: 8px !important;
    color: #0D2B52 !important;
}
section[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #8a9bb5 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #e8edf5 !important;
    margin: 0.6rem 0 !important;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #0D2B52 !important;
    font-size: 0.95rem !important;
    margin: 0.3rem 0 !important;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: white;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(13,43,82,0.09);
}
.topbar-title { font-size: 1.05rem; font-weight: 700; color: #0D2B52; }
.topbar-crumb { font-size: 0.72rem; color: #8a9bb5; margin-top: 1px; }
.topbar-user  { font-size: 0.83rem; font-weight: 600; color: #0D2B52; }

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 1rem;
}
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 12px rgba(13,43,82,0.09);
    display: flex;
    align-items: center;
    gap: 0.9rem;
    border-top: 3px solid #1a8fd1;
    transition: transform .15s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-icon {
    font-size: 1.7rem;
    background: rgba(26,143,209,0.1);
    border-radius: 10px;
    width: 50px; height: 50px;
    display: flex; align-items: center;
    justify-content: center; flex-shrink: 0;
}
.kpi-val   { font-size: 1.55rem; font-weight: 700; color: #0D2B52; line-height: 1; }
.kpi-label { font-size: 0.75rem; color: #8a9bb5; margin-top: 3px; }
.kpi-delta { font-size: 0.7rem; margin-top: 3px; }
.up   { color: #27ae60; }
.down { color: #e74c3c; }

.card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.1rem 0.6rem;
    box-shadow: 0 2px 12px rgba(13,43,82,0.09);
}
.card-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #0D2B52;
    border-bottom: 1px solid #eef2f7;
    padding-bottom: 0.4rem;
    margin-bottom: 0.5rem;
}

.stButton > button {
    background: linear-gradient(135deg, #0D2B52, #1a8fd1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextInput input, .stTextArea textarea {
    border-radius: 8px !important;
    border: 1px solid #dce5f0 !important;
}

.main .stTextInput label,
.main .stTextArea label,
.main .stSelectbox label,
.main .stNumberInput label,
.main .stDateInput label,
.main .stSlider label,
.main .stMarkdown p,
.main h4, .main h3, .main h2,
[data-testid="stForm"] label,
[data-testid="stForm"] p {
    color: #0D2B52 !important;
    font-weight: 500 !important;
}

[data-testid="stTabs"] button { color: #8a9bb5 !important; }
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0D2B52 !important;
    font-weight: 700 !important;
}

.npr-box {
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-top: 0.8rem;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

[data-testid="collapsedControl"],
button[data-testid="collapsedControl"],
div[data-testid="collapsedControl"],
button[title*="sidebar"],
button[aria-label*="sidebar"],
button[aria-label*="Sidebar"],
button[title*="Sidebar"],
button[title*="toggle"],
button[aria-label*="toggle"],
button[aria-label*="Toggle"],
button[title*="Toggle"] {
    position: relative !important;
    background: linear-gradient(135deg, #0D2B52, #1a8fd1) !important;
    border-radius: 999px !important;
    padding: 0 !important;
    box-shadow: 0 14px 32px rgba(13, 43, 82, 0.24) !important;
    overflow: visible !important;
    width: 52px !important;
    height: 52px !important;
    min-width: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: transform .2s ease, background .2s ease !important;
    cursor: pointer !important;
    border: none !important;
}
[data-testid="collapsedControl"]:hover,
button[data-testid="collapsedControl"]:hover,
div[data-testid="collapsedControl"]:hover,
button[title*="sidebar"]:hover,
button[aria-label*="sidebar"]:hover,
button[aria-label*="Sidebar"]:hover,
button[title*="Sidebar"]:hover,
button[title*="toggle"]:hover,
button[aria-label*="toggle"]:hover,
button[aria-label*="Toggle"]:hover,
button[title*="Toggle"]:hover {
    background: linear-gradient(135deg, #1a8fd1, #0D2B52) !important;
    transform: translateX(2px) !important;
}
[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] span,
button[data-testid="collapsedControl"] svg,
button[data-testid="collapsedControl"] span,
div[data-testid="collapsedControl"] svg,
div[data-testid="collapsedControl"] span,
button[title*="sidebar"] svg,
button[aria-label*="sidebar"] svg,
button[aria-label*="Sidebar"] svg,
button[title*="Sidebar"] svg,
button[title*="toggle"] svg,
button[aria-label*="toggle"] svg,
button[aria-label*="Toggle"] svg,
button[title*="Toggle"] svg {
    display: none !important;
}
[data-testid="collapsedControl"]::before,
button[data-testid="collapsedControl"]::before,
div[data-testid="collapsedControl"]::before,
button[title*="sidebar"]::before,
button[aria-label*="sidebar"]::before,
button[aria-label*="Sidebar"]::before,
button[title*="Sidebar"]::before,
button[title*="toggle"]::before,
button[aria-label*="toggle"]::before,
button[aria-label*="Toggle"]::before,
button[title*="Toggle"]::before {
    content: none !important;
}

[data-testid="collapsedControl"]::after,
button[data-testid="collapsedControl"]::after,
div[data-testid="collapsedControl"]::after,
button[title*="sidebar"]::after,
button[aria-label*="sidebar"]::after,
button[aria-label*="Sidebar"]::after,
button[title*="Sidebar"]::after,
button[title*="toggle"]::after,
button[aria-label*="toggle"]::after,
button[aria-label*="Toggle"]::after,
button[title*="Toggle"]::after {
    content: "☰" !important;
    position: absolute !important;
    font-size: 1.2rem !important;
    color: white !important;
    width: auto !important;
    height: auto !important;
    line-height: 1 !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    background: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)
