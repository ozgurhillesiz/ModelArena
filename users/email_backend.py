import json
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class BrevoAPIBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        api_key = settings.BREVO_API_KEY
        if not api_key:
            return 0

        sent = 0
        for message in email_messages:
            # Gönderen adı ve adresi ayıkla
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