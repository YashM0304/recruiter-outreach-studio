"""
⚡ Recruiter Outreach Studio — Email Sender
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import smtplib
import json
import re
import time
from email.message import EmailMessage
from datetime import date
from pathlib import Path

# ── CONFIG — update paths if needed ─────────────────────────────────────────
EMAIL_FROM     = "yash.m.malpathak@gmail.com"
EMAIL_PASSWORD = "ubwu kzer xoba qlde"          # Gmail App Password
RESUME_FILE    = "YMM_Technical_Resume_Final_C.pdf"  # place in same folder as app.py
DAILY_LIMIT    = 30
LOG_FILE       = "sent_log.json"

LINKS = {
    "linkedin":   "https://www.linkedin.com/in/yash-malpathak/",
    "portfolio":  "https://yash-malpathak.vercel.app/",

}

CONF_PRIORITY = {"Verified": 0, "Pattern High": 1, "Pattern Inferred": 2, "Generic Alias": 3}

# ── Helpers ──────────────────────────────────────────────────────────────────
def load_log():
    if Path(LOG_FILE).exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return {}

def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def get_sent_today(log):
    return set(log.get(str(date.today()), []))

def get_all_sent(log):
    s = set()
    for v in log.values():
        s.update(v)
    return s

def mark_sent(log, email_addr):
    today = str(date.today())
    log.setdefault(today, [])
    if email_addr not in log[today]:
        log[today].append(email_addr)

def is_valid_email(e):
    return isinstance(e, str) and bool(re.match(r"[^@]+@[^@]+\.[^@]+", e))

def build_queue(df, all_sent, limit):
    rows = []
    for _, r in df.iterrows():
        email = str(r.get("Email", "")).strip()
        name  = str(r.get("Name",  "")).strip()
        if not is_valid_email(email):     continue
        if name == "Generic Alias":       continue
        if email.lower() in [s.lower() for s in all_sent]: continue
        conf = r.get("Email Confidence", "")
        rows.append({**r.to_dict(), "_order": CONF_PRIORITY.get(conf, 3)})
    rows.sort(key=lambda x: x["_order"])
    return rows[:limit]

def compose_email(to_email, rec_name, company):
    first   = (rec_name or "there").split()[0] if rec_name != "Generic Alias" else "there"
    subject = "Cybersecurity Full-Time Opportunities – Yash Malpathak | UW MS '26"
    body    = f"""Hi {first},

I hope you are doing well. I'm Yash, an M.S. Cybersecurity Engineering student at the University of Washington (graduating 2026), reaching out about full-time security opportunities at {company}. I can work on OPT for 3 years post-graduation and will require visa sponsorship only after OPT ends.

A few highlights:
- Cybersecurity Engineering Intern, Secure AIs Corporation (Summer 2025) — built a Python PII detection pipeline (~80% accuracy) and ran 200+ adversarial prompt-injection tests, reducing successful exploits by ~60%.
- Master's thesis at UW on enhancing technology fingerprinting using human-generated OSINT (job postings, LinkedIn, GitHub) as a complement to tool-based reconnaissance — demonstrated a 94.1% average coverage gain over Nmap/WhatWeb-only baselines across 12 organizations.
- ISO 27001:2022 Certified Lead Implementer & Lead Auditor | ISO 42001:2023 AI Systems Lead Implementer — hands-on across GRC, cloud security (AWS/GCP), and DevSecOps pipelines.
- Academic security research: C++ malware development and research, Linux kernel Netfilter firewall, stack-based buffer overflow exploitation, Ethereum re-entrancy attacks.

I've attached my resume. If there are open full-time security roles — defensive, offensive, GRC, or cloud — I'd love a quick 15-minute chat, or happy to apply through the official portal if you can point me in the right direction.

LinkedIn:  {LINKS["linkedin"]}
Portfolio: {LINKS["portfolio"]}

Best,
Yash Mahesh Malpathak"""

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = EMAIL_FROM
    msg["To"]      = to_email
    msg.set_content(body)

    resume = Path(RESUME_FILE)
    if resume.exists():
        with open(resume, "rb") as f:
            msg.add_attachment(
                f.read(), maintype="application", subtype="pdf",
                filename="Yash_Malpathak_Resume.pdf"
            )
    return msg, subject, body

def smtp_send(msg):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
        srv.login(EMAIL_FROM, EMAIL_PASSWORD)
        srv.send_message(msg)

# ── Page setup ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="⚡ Recruiter Outreach", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #080c14; }
    section[data-testid="stSidebar"] { background-color: #0c1018; border-right: 1px solid #1f2937; }
    .stMetric { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 14px 18px; }
    .stMetric label { color: #6b7280 !important; font-size: 12px !important; }
    .stMetric [data-testid="stMetricValue"] { color: #f59e0b !important; font-size: 28px !important; font-weight: 700 !important; }
    .stMetric [data-testid="stMetricDelta"] { color: #6b7280 !important; }
    .stButton > button {
        background: #10b981 !important; color: #ffffff !important; font-weight: 700 !important;
        border: none !important; border-radius: 10px !important; width: 100%;
        padding: 14px !important; font-size: 16px !important; margin-top: 8px;
    }
    .stButton > button p, .stButton > button span, .stButton > button div {
        color: #ffffff !important;
    }
    .stButton > button:hover { background: #059669 !important; color: #ffffff !important; }
    .stButton > button:hover p, .stButton > button:hover span { color: #ffffff !important; }
    .stButton > button:disabled { background: #1f2937 !important; color: #6b7280 !important; }
    .stButton > button:disabled p, .stButton > button:disabled span { color: #6b7280 !important; }
    .stDataFrame, [data-testid="stDataFrame"] { border: 1px solid #1f2937; border-radius: 12px; }
    .stTextInput > div > div { background: #111827 !important; border-color: #1f2937 !important; color: #e5e7eb !important; border-radius: 8px !important; }
    .stSelectbox > div > div { background: #111827 !important; border-color: #1f2937 !important; color: #e5e7eb !important; border-radius: 8px !important; }
    .stTextArea > div > div { background: #0c1018 !important; border-color: #1f2937 !important; color: #d1d5db !important; font-size: 13px !important; border-radius: 8px !important; }
    .stFileUploader { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 6px 12px; }
    .stProgress > div > div { background: #f59e0b !important; }
    .stAlert { border-radius: 10px !important; }
    hr { border-color: #1f2937 !important; }
    h1, h2, h3 { color: #f3f4f6 !important; }
    p, label, .stMarkdown { color: #9ca3af !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#f59e0b;margin-bottom:0'>⚡ Recruiter Outreach Studio</h1>",
    unsafe_allow_html=True
)
st.caption(f"**{EMAIL_FROM}**  ·  Yash Mahesh Malpathak  ·  UW MS Cybersecurity Engineering '26")
st.divider()

# ── Load tracking log ────────────────────────────────────────────────────────
log           = load_log()
sent_today    = get_sent_today(log)
all_sent      = get_all_sent(log)
remaining_today = max(0, DAILY_LIMIT - len(sent_today))

# ── CSV upload ───────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = None

uploaded = st.file_uploader(
    "📋 Upload Recruiter CSV",
    type="csv",
    help="Upload the early-career-swe-recruiters CSV"
)
if uploaded:
    st.session_state.df = pd.read_csv(uploaded)

df = st.session_state.df

if df is None:
    st.info("⬆ Upload your recruiter CSV above to get started.")
    st.stop()

# ── Stats row ─────────────────────────────────────────────────────────────────
queue_preview = build_queue(df, all_sent, DAILY_LIMIT)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Sent Today",        len(sent_today),        f"/ {DAILY_LIMIT} daily limit")
c2.metric("Remaining Today",   remaining_today)
c3.metric("Total Sent Ever",   len(all_sent))
c4.metric("Ready in Queue",    len(queue_preview))
st.divider()

# ── Left / Right layout ───────────────────────────────────────────────────────
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.subheader("🔍 Browse Recruiters")

    fa, fb = st.columns([1, 2])
    with fa:
        tier_opts = ["All"] + sorted(df["Tier"].dropna().unique().tolist())
        tier_sel  = st.selectbox("Tier", tier_opts)
    with fb:
        search = st.text_input("Search", placeholder="Name, company, skill, focus...")

    view = df[df["Name"] != "Generic Alias"].copy()
    if tier_sel != "All":
        view = view[view["Tier"] == tier_sel]
    if search:
        q = search.lower()
        view = view[view.apply(
            lambda r: any(q in str(r.get(c, "")).lower() for c in ["Name","Company","Focus","Title"]),
            axis=1
        )]

    def status_badge(email):
        if email in all_sent:   return "✅ Sent"
        return "⏳ Pending"

    view = view.copy()
    view["Status"] = view["Email"].apply(status_badge)
    view["Conf."]  = view.get("Email Confidence", pd.Series(dtype=str)).fillna("")

    show = ["Name", "Company", "Tier", "Conf.", "Focus", "Status"]
    available = [c for c in show if c in view.columns]
    st.dataframe(
        view[available].reset_index(drop=True),
        use_container_width=True,
        height=340,
        hide_index=True
    )

with right:
    st.subheader("📬 Today's Outgoing Batch")

    if not queue_preview:
        st.success("🎉 All recruiters contacted! No one left in the queue.")
    else:
        batch_to_send = queue_preview[:remaining_today]

        q_display = pd.DataFrame([{
            "Name":     r.get("Name", ""),
            "Company":  r.get("Company", ""),
            "Email":    r.get("Email", ""),
            "Conf.":    r.get("Email Confidence", ""),
        } for r in batch_to_send])
        st.dataframe(q_display, use_container_width=True, height=220, hide_index=True)

        if remaining_today <= 0:
            st.warning(f"✋ Daily limit of {DAILY_LIMIT} reached. Come back tomorrow!")
        else:
            # Resume check
            resume_exists = Path(RESUME_FILE).exists()
            if not resume_exists:
                st.warning(
                    f"⚠ Resume not found at `{RESUME_FILE}` — "
                    "place your PDF in the same folder as app.py. "
                    "Emails will send **without** attachment until then."
                )

            st.markdown(
                f"<p style='color:#6b7280;font-size:13px;margin-top:4px'>"
                f"Will send to <b style='color:#f59e0b'>{len(batch_to_send)}</b> recruiters · "
                f"highest-confidence emails first</p>",
                unsafe_allow_html=True
            )

            if st.button(f"🚀 Send {len(batch_to_send)} Emails Now"):
                prog    = st.progress(0, text="Preparing...")
                log_box = st.empty()
                success, failed = [], []

                for i, rec in enumerate(batch_to_send):
                    addr    = rec["Email"]
                    name    = rec["Name"]
                    company = rec["Company"]
                    try:
                        msg, _, _ = compose_email(addr, name, company)
                        smtp_send(msg)
                        mark_sent(log, addr)
                        success.append(f"{name} @ {company}")
                        log_box.success(f"✅ {i+1}/{len(batch_to_send)} — {name} @ {company}")
                    except Exception as e:
                        failed.append(f"{name} @ {company}: {e}")
                        log_box.error(f"❌ {name} @ {company} — {e}")

                    prog.progress((i + 1) / len(batch_to_send), text=f"Sending {i+1} / {len(batch_to_send)}...")
                    time.sleep(0.6)   # prevents Gmail rate-limiting

                save_log(log)
                prog.progress(1.0, text="Done!")

                if success:
                    st.balloons()
                    st.success(f"✅ Sent {len(success)} emails successfully!")
                if failed:
                    st.error(f"❌ {len(failed)} failed:\n" + "\n".join(failed))

                time.sleep(1.5)
                st.rerun()

st.divider()

# ── Email preview ─────────────────────────────────────────────────────────────
with st.expander("📧 Email Template Preview", expanded=False):
    if queue_preview:
        sample = queue_preview[0]
        _, subj, body = compose_email(sample["Email"], sample["Name"], sample["Company"])
        st.markdown(f"**Subject:** `{subj}`")
        st.text_area("Body (editable for reference only — actual sends use the template above)",
                     body, height=380)
    else:
        st.info("Upload CSV to preview the email template.")

# ── Sent history ──────────────────────────────────────────────────────────────
with st.expander("📋 Full Sent History", expanded=False):
    if log:
        rows = []
        for d, emails in sorted(log.items(), reverse=True):
            for e in emails:
                match = df[df["Email"] == e]
                name    = match.iloc[0]["Name"]    if not match.empty else "—"
                company = match.iloc[0]["Company"] if not match.empty else "—"
                rows.append({"Date": d, "Name": name, "Company": company, "Email": e})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No emails sent yet.")
