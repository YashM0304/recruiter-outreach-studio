# ⚡ Recruiter Outreach Studio — Setup Guide

## 1. Install dependencies (one time only)
```bash
pip install streamlit pandas
```

## 2. Folder structure
Put all of these in the **same folder**:
```
📁 your-folder/
├── app.py
├── early-career-swe-recruiters-top-us-companies.csv
└── YMM_Technical_Resume_Final_C.pdf
```

## 3. Run the app
```bash
streamlit run app.py
```
Your browser opens automatically at http://localhost:8501

## 4. Use it
1. Upload the CSV using the file uploader
2. See your batch of 30 (highest-confidence emails first)
3. Hit **🚀 Send Emails Now**
4. Done — come back tomorrow for the next 30

## Notes
- Sent emails are tracked in `sent_log.json` (auto-created)
- The same recruiter will never be emailed twice
- 0.6s delay between sends to avoid Gmail rate limiting
- Gmail allows 500 emails/day — 30/day is well within limits
