import asyncio
from aiosmtpd.controller import Controller
from email import message_from_bytes
from email.policy import default
import pandas as pd
from io import BytesIO

# Przechowuj adresy e-mail i hasła w słowniku
email_passwords = {
    "administratorek@localhost": "admin_password",
    "user1@localhost": "user1_password",
    "user2@localhost": "user2_password"
}

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mailfrom = envelope.mail_from
        rcpttos = envelope.rcpt_tos
        data = envelope.content

        print('Peer:', peer)
        print('Mail from:', mailfrom)
        print('Rcpt to:', rcpttos)

        msg = message_from_bytes(data, policy=default)

        # Sprawdź, czy adres e-mail jest w słowniku
        for rcptto in rcpttos:
            if rcptto in email_passwords:
                print(f"Message received for {rcptto}:")
                print(msg.get_body(preferencelist=('plain')).get_content())
                for part in msg.iter_attachments():
                    content_type = part.get_content_type()
                    if content_type == 'text/csv' or content_type == 'application/csv':
                        csv_data = part.get_payload(decode=True)
                        df = pd.read_csv(BytesIO(csv_data))
                        print(f"Załącznik zawiera {df.shape[1]} kolumn oraz {df.shape[0]} wierszy")
                    else:
                        print(f"Attachment of type {content_type} ignored.")
            else:
                print(f"Unknown recipient: {rcptto}")
                return '550 Unknown recipient'

        return '250 Message accepted for delivery'

def run_server():
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=1026)
    controller.start()

    print("SMTP server is running. Press Ctrl+C to stop.")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == "__main__":
    run_server()
