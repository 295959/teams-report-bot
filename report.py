import requests
from datetime import date, timedelta
import holidays
import time

WEBHOOK_URL = "https://ihoban.webhook.office.com/webhookb2/77c1f4c7-6e1a-41a2-bb16-a8d22b28c9fc@204624d4-2187-4615-829e-51e1e5503ef3/IncomingWebhook/d6b42a9b617d48fe936e96a4a0d007eb/c0c15cf7-cf72-467c-9e03-02cb7ad6a256/V2BguZhvkPu2FjNXh-aukWsj5T8NTIEWHM_eoYj_ACE_41"
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
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.2",
                "body": [
                    {
                        "type": "TextBlock",
                        "text": f"📊 {title}",
                        "weight": "Bolder",
                        "size": "Medium",
                        "wrap": True
                    }
                ],
                "actions": [
                    {
                        "type": "Action.OpenUrl",
                        "title": "📂 보고서 열기",
                        "url": FILE_LINK
                    }
                ]
            }
        }
    ]
}

for attempt in range(1, 4):
    response = requests.post(WEBHOOK_URL, json=payload, timeout=30)

    print("Teams status:", response.status_code)
    print("Teams response:", response.text)

    if 200 <= response.status_code < 300:
        break

    print(f"전송 실패, {attempt}/3회 시도")
    time.sleep(10)

else:
    raise Exception(f"Teams 전송 실패: {response.status_code} / {response.text}")
