"""
ModelArena - Brevo API Email Backend
======================================
Django'nun varsayılan SMTP backend'i yerine Brevo HTTP API'sini kullanır.
Render gibi SMTP portlarını (587) engelleyen ortamlarda çalışmak için
tasarlanmıştır. Port 443 (HTTPS) üzerinden mail gönderir.
"""

import json
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class BrevoAPIBackend(BaseEmailBackend):
    """
    Brevo (eski adıyla Sendinblue) HTTP API üzerinden email gönderen backend.
    settings.py'de EMAIL_BACKEND olarak tanımlanır.
    """

    def send_messages(self, email_messages):
        """
        Email mesajlarını Brevo API'ye POST eder.
        Başarılı gönderim sayısını döndürür.
        """
        api_key = settings.BREVO_API_KEY
        if not api_key:
            return 0

        sent = 0
        for message in email_messages:
            # Gönderen adı ve adresini ayıkla
            from_email = message.from_email
            if '<' in from_email:
                from_name = from_email.split('<')[0].strip()
                from_addr = from_email.split('<')[1].replace('>', '').strip()
            else:
                from_name = 'ModelArena'
                from_addr = from_email

            payload = {
                "sender": {"name": from_name, "email": from_addr},
                "to": [{"email": addr} for addr in message.to],
                "subject": message.subject,
                "textContent": message.body,
            }

            try:
                # Brevo API endpoint'ine istek at (timeout: 10 saniye)
                response = requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    headers={
                        "api-key": api_key,
                        "Content-Type": "application/json",
                        "accept": "application/json",
                    },
                    data=json.dumps(payload),
                    timeout=10,
                )
                if response.status_code in (200, 201):
                    sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent