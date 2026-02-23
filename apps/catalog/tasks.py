"""Celery tasks for catalog app."""

from celery import shared_task

from apps.catalog.telegram_notify import notify_telegram_application


@shared_task(bind=True, ignore_result=True)
def send_application_to_telegram(self, form_type: str, payload: dict):
    """
    Send form submission to Telegram chat.
    form_type: 'contact' | 'dealer'
    payload: dict with form fields (e.g. name, phone, email, message or name, company, email, message).
    """
    notify_telegram_application(form_type, payload)
