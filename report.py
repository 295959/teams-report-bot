import os
import smtplib
from email.mime.text import MIMEText
from datetime import date, timedelta

import holidays

GMAIL_ADDRESS = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
CHANNEL_EMAIL = os.environ["CHANNEL_EMAIL"]
FILE_LINK = os.environ["FILE_LINK"]

kr_holidays = holidays.country_holidays("KR")
weekdays = ["월", "화", "수", "목", "금", "토", "일"]


def get_next_business_day(today):
    d = today + timedelta(days=1)

    while d.weekday() >= 5 or d in kr_holidays:
        d += timedelta(days=1)

    return d


today = date.today()
target = get_next_business_day(today)

date_text = f"{target.month}/{target.day}({weekdays[target.weekday()]})"

title = f"프라계열 주요현안 일일보고 {date_text}"

html = f"""
<html>
<body>

<h3>📊 {title}</h3>

<p>
<a href="{FILE_LINK}">📂 보고서 열기</a>
</p>

</body>
</html>
"""

msg = MIMEText(html, "html", "utf-8")

msg["Subject"] = title
msg["From"] = GMAIL_ADDRESS
msg["To"] = CHANNEL_EMAIL

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
    server.send_message(msg)

print("메일 전송 완료")
