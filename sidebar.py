import streamlit as st
import pandas as pd
import base64
from chart_config import load_css

ROLE_PAGES = {
    "CFO":             ["executive","revenue_leakage","claim_denial",
                        "billing_anomaly","forecast","cfo_strategic"],
    "RCM":             ["executive","revenue_leakage","claim_denial",
                        "billing_anomaly","forecast"],
    "Department Head": ["executive","revenue_leakage","claim_denial","billing_anomaly"],
    "Insurance Team":  ["insurance_view"],
}

PAGE_LABELS = {
    "executive":       "Executive Overview",
    "forecast":        "Revenue Forecasting",
    "revenue_leakage": "Revenue Leakage",
    "claim_denial":    "Claim Denial Risk",
    "billing_anomaly": "Billing Anomaly",
    "cfo_strategic":   "CFO Strategic View",
    "insurance_view":  "Insurance Analytics",
}

BADGE = {
    "CFO":            ("rb-cfo",  "CFO"),
    "RCM":            ("rb-rcm",  "RCM"),
    "Department Head":("rb-dept", "Dept Head"),
    "Insurance Team": ("rb-ins",  "Insurance"),
}

_LOGO_B64 = "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"


def sidebar():
    load_css()

    with st.sidebar:
        # ── LOGO — embedded as base64, always visible ──
        st.markdown(f"""
        <div style="text-align:center; padding: 8px 0 4px;">
          <img src="data:image/jpeg;base64,{_LOGO_B64}"
               style="width:170px; height:auto;
                      filter:drop-shadow(0 0 10px rgba(255,215,0,0.3));"
               alt="Medilytics">
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── PROFILE ──
        role     = st.session_state.get("role", "User")
        username = st.session_state.get("username", "—")
        dept     = st.session_state.get("department", "—")
        cls, lbl = BADGE.get(role, ("rb-rcm", role))

        st.markdown(f"""
        <div style="padding:6px 0 4px;">
          <div class="section-label">Logged in as</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:18px;
                      font-weight:700;color:#EFF6FF;margin:3px 0;">{username}</div>
          <span class="role-badge {cls}">{lbl}</span>
        </div>""", unsafe_allow_html=True)

        if role == "Department Head":
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                        color:#00FF87;margin-top:5px;">{dept}</div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── FILTERS ──
        st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)
        page    = st.session_state.get("page", "executive")
        filters = st.session_state.get("filters", {})

        @st.cache_data
        def load_main():
            df = pd.read_csv("data/modified_dataset.csv")
            df["Claim_Submission_Date"] = pd.to_datetime(
                df["Claim_Submission_Date"], dayfirst=True, errors="coerce")
            return df

        @st.cache_data
        def load_pre():
            return pd.read_csv("data/pre_processed_data.csv")

        if page in ["executive","revenue_leakage","billing_anomaly"]:
            df  = load_main()
            mn  = df["Claim_Submission_Date"].min().date()
            mx  = df["Claim_Submission_Date"].max().date()
            filters["date_range"] = st.date_input(
                "Date Range",
                value=filters.get("date_range",(mn,mx)),
                min_value=mn, max_value=mx)
            depts = sorted(df["Department"].dropna().unique().tolist())
            if role in ["CFO","RCM"]:
                filters["department_filter"] = st.selectbox(
                    "Department", ["All"]+depts, index=0)
            elif role == "Department Head":
                filters["department_filter"] = dept
                st.info(dept)
            else:
                filters["department_filter"] = "All"
            ins_opts = sorted(df["Insurance_Type"].dropna().unique().tolist())
            filters["insurance_filter"] = st.selectbox(
                "Insurance Type", ["All"]+ins_opts)

        elif page == "claim_denial":
            df_pre = load_pre()
            depts  = sorted(df_pre["Department"].dropna().unique().tolist())
            filters["risk_filter"] = st.selectbox(
                "Risk Level", ["All","Low","Medium","High"])
            if role in ["CFO","RCM"]:
                filters["department_filter"] = st.selectbox(
                    "Department", ["All"]+depts, index=0)
            elif role == "Department Head":
                filters["department_filter"] = dept
                st.info(dept)
            ins_opts = sorted(df_pre["Insurance_Type"].dropna().unique().tolist())
            filters["insurance_filter"] = st.selectbox(
                "Insurance Type", ["All"]+ins_opts)

        elif page == "forecast":
            st.caption("Showing 6-month ARIMA forecast.")
        elif page in ["cfo_strategic","insurance_view"]:
            st.caption("Role-specific view.")

        st.session_state.filters = filters
        st.divider()

        # ── NAVIGATION ──
        st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
        allowed = ROLE_PAGES.get(role, ["executive"])
        for pg in allowed:
            label = PAGE_LABELS.get(pg, pg)
            if st.button(label, key=f"nav_{pg}", use_container_width=True):
                st.session_state.page    = pg
                st.session_state.filters = {}
                st.rerun()

        st.divider()

        # ── LOGOUT ──
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
