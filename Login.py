import streamlit as st
import pandas as pd

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Hide Streamlit chrome ── */
header[data-testid="stHeader"]  { display:none!important }
[data-testid="stToolbar"]       { display:none!important }
[data-testid="stDecoration"]    { display:none!important }
#MainMenu, footer               { display:none!important }

/* ── Full-page dark background ── */
html, body, .stApp,
[data-testid="stAppViewContainer"] {
    background: #020817 !important;
    min-height: 100vh !important;
}

/* ── Animated grid ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(255,215,0,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,215,0,0.045) 1px, transparent 1px);
    background-size: 52px 52px;
    animation: gridMove 22s linear infinite;
    pointer-events: none; z-index: 0;
}
@keyframes gridMove {
    0%   { background-position: 0 0, 0 0; }
    100% { background-position: 52px 52px, 52px 52px; }
}

/* ── Gold blob top-left ── */
.stApp::after {
    content: '';
    position: fixed; width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(255,215,0,0.13) 0%, transparent 65%);
    top: -180px; left: -160px;
    border-radius: 50%; filter: blur(80px);
    pointer-events: none; z-index: 0;
    animation: blobA 11s ease-in-out infinite alternate;
}
@keyframes blobA {
    0%   { transform: scale(1) translate(0,0); }
    100% { transform: scale(1.2) translate(28px,20px); }
}

/* ── Vertical centering with top margin breathing room ── */
[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
    min-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="stMainBlockContainer"] > div[data-testid="block-container"],
[data-testid="block-container"] {
    padding: 4rem 1rem 2rem !important;
    width: 100% !important;
    max-width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    flex: 1 !important;
}

/* Column row — centre it */
[data-testid="stHorizontalBlock"] {
    width: 100% !important;
    justify-content: center !important;
}

/* ── Blobs (HTML elements) ── */
.blob-cyan {
    position: fixed; width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(0,229,255,0.10) 0%, transparent 65%);
    bottom: -120px; right: -120px;
    border-radius: 50%; filter: blur(80px);
    pointer-events: none; z-index: 0;
    animation: blobB 13s ease-in-out infinite alternate;
}
@keyframes blobB {
    0%   { transform: scale(1) translate(0,0); }
    100% { transform: scale(1.15) translate(-22px,-28px); }
}
.blob-purple {
    position: fixed; width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(167,139,250,0.09) 0%, transparent 65%);
    top: 38%; left: 60%;
    border-radius: 50%; filter: blur(80px);
    pointer-events: none; z-index: 0;
    animation: blobC 9s ease-in-out infinite alternate;
}
@keyframes blobC {
    0%   { transform: scale(1) translate(0,0); }
    100% { transform: scale(1.18) translate(-15px,20px); }
}

/* ── ECG lines ── */
.ecg-wrap {
    position: fixed; inset: 0;
    pointer-events: none; z-index: 1; overflow: hidden;
}
.ecg-line {
    position: absolute; left: 0; right: 0; height: 160px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='160' viewBox='0 0 600 160'%3E%3Cpolyline fill='none' stroke='%23FFD700' stroke-width='1.5' opacity='0.6' stroke-linecap='round' stroke-linejoin='round' points='0,80 55,80 75,80 88,72 100,80 104,72 107,20 109,140 111,65 120,80 175,80 195,80 208,72 220,80 224,72 227,20 229,140 231,65 240,80 295,80 315,80 328,72 340,80 344,72 347,20 349,140 351,65 360,80 415,80 435,80 448,72 460,80 464,72 467,20 469,140 471,65 480,80 535,80 555,80 568,72 580,80 584,72 587,20 589,140 591,65 600,80'/%3E%3C/svg%3E");
    background-repeat: repeat-x; background-size: 600px 160px;
    animation: ecgScroll linear infinite;
}
.ecg-line:nth-child(1) { top: 10%; opacity:0.55; animation-duration: 8s;  }
.ecg-line:nth-child(2) { top: 34%; opacity:0.32; animation-duration: 11s; }
.ecg-line:nth-child(3) { top: 58%; opacity:0.22; animation-duration: 14s; }
.ecg-line:nth-child(4) { top: 80%; opacity:0.15; animation-duration: 17s; }
@keyframes ecgScroll {
    0%   { background-position: 0 0; }
    100% { background-position: -600px 0; }
}

/* ── Login card ── */
.lcard {
    background: rgba(10,22,42,0.93);
    border: 1px solid rgba(255,215,0,0.22);
    border-radius: 20px;
    padding: 36px 42px 28px;
    width: 100%;
    backdrop-filter: blur(28px); -webkit-backdrop-filter: blur(28px);
    box-shadow: 0 0 0 1px rgba(255,215,0,0.08), 0 28px 70px rgba(0,0,0,0.7);
    animation: cardIn .85s cubic-bezier(.22,1,.36,1) both,
               cardGlow 4s ease-in-out 1.2s infinite alternate;
    position: relative; z-index: 10;
    /* breathing room from top edge */
    margin-top: 2rem;
    margin-bottom: 1rem;
}
@keyframes cardIn {
    from { opacity:0; transform: translateY(32px) scale(.97); }
    to   { opacity:1; transform: translateY(0) scale(1); }
}
@keyframes cardGlow {
    0%   { box-shadow: 0 0 0 1px rgba(255,215,0,.09), 0 28px 70px rgba(0,0,0,.7); }
    100% { box-shadow: 0 0 0 1px rgba(255,215,0,.30), 0 28px 70px rgba(0,0,0,.7),
                       0 0 52px rgba(255,215,0,.09); }
}

/* Gold brand heading */
.lbrand {
    font-family: 'Rajdhani', sans-serif;
    font-size: 38px; font-weight: 700;
    color: #FFD700; letter-spacing: 6px;
    text-transform: uppercase; text-align: center;
    text-shadow: 0 0 30px rgba(255,215,0,0.45);
    animation: fadeD .8s ease .1s both;
    margin-bottom: 4px;
}
@keyframes fadeD {
    from { opacity:0; transform:translateY(-10px); }
    to   { opacity:1; transform:translateY(0); }
}
.laccent {
    height: 2px;
    background: linear-gradient(90deg, transparent, #FFD700 40%, transparent);
    border-radius: 2px; margin-bottom: 16px;
    animation: lineX 1.1s ease .35s both; transform-origin: center;
}
@keyframes lineX {
    from { transform: scaleX(0); opacity:0; }
    to   { transform: scaleX(1); opacity:1; }
}
.ltag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 3px; color: #475569;
    text-transform: uppercase; text-align: center; margin-bottom: 8px;
    animation: fadeD .7s ease .25s both;
}

/* ── Inputs scoped to middle column ── */
[data-testid="column"]:nth-child(2) .stTextInput > label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: 1.3px !important; text-transform: uppercase !important;
    color: #64748B !important;
}
[data-testid="column"]:nth-child(2) .stTextInput input {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(255,255,255,.10) !important;
    border-radius: 8px !important; color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important; font-size: 14px !important;
    transition: border-color .2s, box-shadow .2s, background .2s !important;
}
[data-testid="column"]:nth-child(2) .stTextInput input:focus {
    border-color: #FFD700 !important;
    box-shadow: 0 0 0 3px rgba(255,215,0,.11) !important;
    background: rgba(255,215,0,.03) !important;
}
[data-testid="column"]:nth-child(2) .stTextInput input::placeholder {
    color: #8BA3BF !important;
}
[data-testid="column"]:nth-child(2) .stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    border: none !important; border-radius: 8px !important; color: #fff !important;
    font-family: 'Rajdhani', sans-serif !important; font-size: 15px !important;
    font-weight: 700 !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; height: 48px !important; width: 100% !important;
    box-shadow: 0 4px 22px rgba(99,102,241,.42) !important;
    transition: transform .18s, box-shadow .18s !important;
    margin-top: 6px !important;
}
[data-testid="column"]:nth-child(2) .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,.58) !important;
}

.lfooter {
    text-align: center; margin-top: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px; letter-spacing: 2px; color: #1E293B; text-transform: uppercase;
    position: relative; z-index: 10;
}
</style>
<div class="blob-cyan"></div>
<div class="blob-purple"></div>
<div class="ecg-wrap">
  <div class="ecg-line"></div>
  <div class="ecg-line"></div>
  <div class="ecg-line"></div>
  <div class="ecg-line"></div>
</div>
"""


def show_login():
    for k, v in [("logged_in", False), ("role", None), ("username", None),
                 ("department", None), ("page", "executive"), ("filters", {})]:
        if k not in st.session_state:
            st.session_state[k] = v

    users = pd.read_csv("data/users.csv")
    users = users.loc[:, ~users.columns.str.startswith("Unnamed")]
    users.columns = [c.strip() for c in users.columns]

    st.markdown(_CSS, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        # Brand card (header section only)
        st.markdown("""
        <div class="lcard">
          <div class="lbrand">MEDILYTICS</div>
          <div class="laccent"></div>
          <div class="ltag">Healthcare Revenue Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        # Inputs + button rendered natively by Streamlit (below card)
        username = st.text_input("Username", placeholder="Enter your username",
                                 key="lg_user")
        password = st.text_input("Password", placeholder="Enter your password",
                                 type="password", key="lg_pass")

        if st.button("Sign In", use_container_width=True, key="lg_btn"):
            _auth(username.strip(), password.strip(), users)

        st.markdown(
            '<div class="lfooter">Medilytics v2.0 &nbsp;&middot;&nbsp; '
            'Secure Healthcare Analytics</div>',
            unsafe_allow_html=True
        )


def _auth(username: str, password: str, users: pd.DataFrame):
    """
    Authenticate user against users.csv.
    CSV columns: username, password, role, department
    Passwords stored as plain strings — cast to str for safety.
    """
    if not username or not password:
        st.error("Please enter both username and password.")
        return

    match = users[
        (users["username"] == username) &
        (users["password"].astype(str) == password)
    ]

    if not match.empty:
        row = match.iloc[0]
        st.session_state.logged_in  = True
        st.session_state.username   = username
        st.session_state.role       = row["role"]
        st.session_state.department = row["department"]
        st.rerun()
    else:
        st.error("Invalid credentials — please check username and password.")
