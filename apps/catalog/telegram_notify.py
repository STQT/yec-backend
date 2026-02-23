"""Telegram notifications for form submissions (no Celery dependency)."""

import json
import logging
import urllib.error
import urllib.request
from urllib.parse import urlencode

from django.conf import settings

logger = logging.getLogger(__name__)


def _send_telegram_message(text: str) -> bool:
    """Send message to Telegram chat. Returns True on success."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)
    if not token or not chat_id:
        logger.warning(
            "Telegram notify skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set "
            "(token=%s, chat_id=%s)",
            "set" if token else "empty",
            "set" if chat_id else "empty",
        )
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urlencode({"chat_id": chat_id, "text": text, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            if resp.status != 200:
                logger.warning("Telegram API HTTP %s: %s", resp.status, body[:500])
                return False
            result = json.loads(body) if body else {}
            if not result.get("ok"):
                logger.warning(
                    "Telegram API error: %s",
                    result.get("description", body[:300]),
                )
                return False
            logger.info("Telegram notification sent to chat_id=%s", chat_id)
            return True
    except (urllib.error.URLError, OSError) as e:
        logger.warning("Telegram request failed: %s", e)
        return False
    except json.JSONDecodeError as e:
        logger.warning("Telegram API invalid JSON: %s", e)
        return False


def notify_telegram_application(form_type: str, payload: dict) -> None:
    """
    Build message and send form submission to Telegram chat.
    form_type: 'contact' | 'dealer'
    payload: dict with form fields.
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
