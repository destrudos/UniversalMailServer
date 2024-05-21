import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Przechowuj adresy e-mail i hasła w słowniku
email_passwords = {
    "administratorek@localhost": "admin_password",
    "user1@localhost": "user1_password",
    "user2@localhost": "user2_password"
}

def send_email_with_attachment(to_address, password, attachment_path):
    # Sprawdź hasło (w rzeczywistości powinieneś zaszyfrować hasło lub użyć bardziej bezpiecznej metody)
    if email_passwords.get(to_address) != password:
        print("Authentication failed: Invalid password")
        return

    msg = MIMEMultipart()
    msg['Subject'] = 'Test Email with Attachment'
    msg['From'] = 'example@example.com'
    msg['To'] = to_address

    body = MIMEText('This is the body of the email', 'plain')
    msg.attach(body)

    # Wczytaj zawartość pliku CSV
    with open(attachment_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), _subtype="csv")
        attachment.add_header('Content-Disposition', 'attachment', filename='attachment.csv')
        msg.attach(attachment)

    with smtplib.SMTP('localhost', 1026) as server:
        server.send_message(msg)

if __name__ == "__main__":
    attachment_path = 'attachment.csv'  # Upewnij się, że ten plik istnieje w bieżącym katalogu
    send_email_with_attachment('administratorek@localhost', 'admin_password', attachment_path)
