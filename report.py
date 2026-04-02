import requests
from datetime import date, timedelta
import holidays

WEBHOOK_URL = "https://ihoban.webhook.office.com/webhookb2/a49ad71b-a0fb-44a5-9b78-6ba30d9bafed@204624d4-2187-4615-829e-51e1e5503ef3/IncomingWebhook/e8fd8cb750434d1395472718f1ed6fa7/c0c15cf7-cf72-467c-9e03-02cb7ad6a256/V2l8YBTFcXGc3VHEOwSEVHlH4mTR1Jd1tB0RmBFSExsOk1"
FILE_LINK = "https://ihoban.sharepoint.com/sites/msteams_c62637/_layouts/15/guestaccess.aspx?share=IQCus3CG0UkGTZbySimHnM8yAcetni83ZPwy6A8TrLlzzoA&e=t38dm8"

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

payload = {
    "text": title + "\n" + FILE_LINK
}

requests.post(WEBHOOK_URL, json=payload)
