# Recruiter Outreach Studio

A local Streamlit app for sending personalized cold emails to recruiters in controlled daily batches. Upload a recruiter CSV, review who is queued for today, and send through Gmail with your resume attached — without double-contacting anyone.

Built for job-search outreach at scale: prioritize high-confidence emails, cap sends per day, and keep a persistent log of every message sent.

---

## Features

- **Daily send cap** — Configurable limit (default 30/day) to stay within Gmail limits and avoid looking spammy
- **Smart queue** — Skips invalid emails, generic aliases, and anyone already contacted; sorts by email confidence (Verified → Pattern High → Pattern Inferred → Generic Alias)
- **Duplicate protection** — Tracks sent addresses in `sent_log.json` across sessions; the same recruiter is never emailed twice
- **Recruiter browser** — Filter by company tier and search by name, company, focus, or title
- **Live batch preview** — See exactly who will receive an email before you hit send
- **Resume attachment** — Automatically attaches your PDF when the file is present locally
- **Progress & history** — Real-time send progress, expandable email template preview, and full sent-history log
- **Rate limiting** — 0.6s delay between sends to reduce Gmail throttling

---

## Requirements

- Python 3.10+
- A Gmail account with [2-Step Verification](https://myaccount.google.com/signinoptions/two-step-verification) enabled
- A Gmail [App Password](https://myaccount.google.com/apppasswords) (not your regular Gmail password)

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/cold-email-tool.git
cd cold-email-tool
pip install -r requirements.txt
```

### 2. Add your resume

Place your resume PDF in the project folder. By default the app looks for:

```
YMM_Technical_Resume_Final_C.pdf
```

Change `RESUME_FILE` in `app.py` if you use a different filename. Emails still send without an attachment if the file is missing, but you'll get a warning in the UI.

### 3. Configure Gmail credentials

Open `app.py` and update the config block at the top:

| Variable | Description |
|----------|-------------|
| `EMAIL_FROM` | Your Gmail address |
| `EMAIL_PASSWORD` | Gmail App Password (16-character code from Google) |
| `RESUME_FILE` | Filename of your resume PDF |
| `DAILY_LIMIT` | Max emails per calendar day |
| `LINKS` | LinkedIn, portfolio, and other URLs inserted into the email body |

> **Security:** Do not commit real credentials to a public repository. For a public repo, use environment variables or Streamlit secrets instead of hardcoding passwords in `app.py`.

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at [http://localhost:8501](http://localhost:8501).

---

## How to use

1. **Upload your recruiter CSV** using the file uploader at the top of the page.
2. **Review the dashboard** — metrics show sent today, remaining quota, total sent ever, and queue size.
3. **Browse recruiters** (left panel) — filter by tier or search; check ✅ Sent vs ⏳ Pending status.
4. **Review today's batch** (right panel) — highest-confidence contacts first, up to your remaining daily limit.
5. **Preview the email** — expand "Email Template Preview" to see subject and body for the next recipient.
6. **Send** — click **Send Emails Now** and wait for progress to complete. Come back tomorrow for the next batch.

---

## CSV format

The app expects a CSV with at least these columns:

| Column | Required | Description |
|--------|----------|-------------|
| `Name` | Yes | Recruiter name (rows with `Generic Alias` are skipped) |
| `Email` | Yes | Valid email address |
| `Company` | Yes | Used in the email body |
| `Email Confidence` | Recommended | `Verified`, `Pattern High`, `Pattern Inferred`, or `Generic Alias` — controls queue priority |
| `Tier` | Optional | Used for filtering (e.g. Finance, Tech) |
| `Focus` | Optional | Shown in browse table; searchable |
| `Title` | Optional | Searchable |

A sample file is included: `early-career-swe-recruiters-top-us-companies.csv`.

---

## Project structure

```
.
├── app.py                                          # Streamlit app + email logic
├── requirements.txt                                # Python dependencies
├── early-career-swe-recruiters-top-us-companies.csv  # Sample recruiter list
├── .gitignore                                      # Ignores logs, PDFs, secrets
├── sent_log.json                                   # Auto-created send history (gitignored)
└── your-resume.pdf                                 # Local only (gitignored)
```

---

## How the queue works

When building today's batch, the app:

1. Drops rows with invalid or missing emails
2. Skips rows where `Name` is `Generic Alias`
3. Skips any email already in `sent_log.json` (case-insensitive)
4. Sorts remaining rows by `Email Confidence` (best first)
5. Takes up to `DAILY_LIMIT` minus what you've already sent today

Each successful send appends the address to today's entry in `sent_log.json`.

---

## Customizing the email

The subject line, body template, and attachment filename are defined in `compose_email()` inside `app.py`. Edit that function to match your background, target roles, and links.

The preview in the UI is read-only; actual sends always use the template in code.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Authentication failed | Use a Gmail **App Password**, not your normal password. Confirm 2FA is on. |
| Resume not attached | Ensure the PDF filename matches `RESUME_FILE` and sits next to `app.py`. |
| Daily limit reached | Wait until the next calendar day, or raise `DAILY_LIMIT` in config. |
| Send failed for one contact | Check the error in the UI; others in the batch may still succeed. Failed sends are not logged as sent. |
| CSV upload does nothing | Confirm required columns exist and emails are valid. |

---

## License

Personal project — fork and adapt for your own job search. Replace email copy, links, and recruiter data with your own before use.
