"""Celery tasks for catalog app."""

import json
import urllib.error
import urllib.request
from urllib.parse import urlencode

from celery import shared_task
from django.conf import settings


def _send_telegram_message(text: str) -> bool:
    """Send message to Telegram chat. Returns True on success."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)
    if not token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urlencode({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except (urllib.error.URLError, OSError):
        return False


@shared_task(bind=True, ignore_result=True)
def send_application_to_telegram(self, form_type: str, payload: dict):
    """
    Send form submission to Telegram chat.
    form_type: 'contact' | 'dealer'
    payload: dict with form fields (e.g. name, phone, email, message or name, company, email, message).
    """
    if form_type == "contact":
        lines = [
            "📩 <b>Новая заявка (обратная связь)</b>",
            f"Имя: {payload.get('name', '—')}",
            f"Телефон: {payload.get('phone', '—')}",
            f"Email: {payload.get('email', '—')}",
            f"Сообщение: {payload.get('message', '—') or '—'}",
        ]
    elif form_type == "dealer":
        lines = [
            "🏢 <b>Новая заявка на дилерство</b>",
            f"Имя: {payload.get('name', '—')}",
            f"Компания: {payload.get('company', '—')}",
            f"Email: {payload.get('email', '—')}",
            f"Сообщение: {payload.get('message', '—') or '—'}",
        ]
    else:
        lines = ["📋 Заявка", json.dumps(payload, ensure_ascii=False, indent=2)]

    text = "\n".join(lines)
    _send_telegram_message(text)
