import os
import smtplib
import json
from email.message import EmailMessage
from typing import List, Optional
from datetime import datetime

# ================= CONFIG =================

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

LOG_FILE = "email_log.jsonl"


# ================= LOGGER =================

def log_email_event(data: dict):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
    except Exception:
        pass


# ================= EMAIL SENDER =================

def send_email(
    subject: str,
    body: str,
    recipients: List[str],
    attachments: Optional[List[str]] = None,
    priority: str = "LOW"
):
    """
    Sends email with:
    - priority tagging
    - logging
    - safe attachment handling
    """

    if not recipients:
        print("⚠️ Email not sent: recipients list is empty")
        return

    if not (SMTP_HOST and SMTP_PORT and SMTP_USER and SMTP_PASS and SMTP_FROM):
        raise RuntimeError(
            "SMTP not configured. Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, SMTP_FROM in .env"
        )

    # 🔥 Add priority tag
    subject = f"[{priority}] {subject}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = ", ".join(recipients)

    # 🔥 Enhanced body
    enhanced_body = f"""
SYSTEM GENERATED ALERT

Priority: {priority}
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

----------------------------------------
{body}
----------------------------------------

(This is an automated system notification)
"""

    msg.set_content(enhanced_body)

    # ================= ATTACHMENTS =================
    attachments = attachments or []

    for path in attachments:
        try:
            if not os.path.exists(path):
                print(f"⚠️ Attachment not found: {path}")
                continue

            with open(path, "rb") as f:
                data = f.read()

            filename = os.path.basename(path)

            msg.add_attachment(
                data,
                maintype="application",
                subtype="octet-stream",
                filename=filename
            )

        except Exception as e:
            print(f"⚠️ Failed to attach {path}: {e}")

    # ================= SEND =================
    try:
        print(f"📧 Sending email to {recipients} with priority {priority}")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)

        print("✅ Email sent successfully")

        # 🔥 LOG SUCCESS
        log_email_event({
            "status": "success",
            "recipients": recipients,
            "priority": priority,
            "subject": subject,
            "time": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Email failed: {e}")

        # 🔥 LOG FAILURE
        log_email_event({
            "status": "failed",
            "error": str(e),
            "recipients": recipients,
            "priority": priority,
            "subject": subject,
            "time": datetime.now().isoformat()
        })