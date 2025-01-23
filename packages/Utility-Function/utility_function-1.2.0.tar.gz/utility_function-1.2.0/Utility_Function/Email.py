import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    def __init__(self, email, subject, sendto, password, zhenwen, smtp_server, port):
        self.smtp_server = smtp_server
        self.email = email
        self.subject = subject
        self.sendto = sendto
        self.password = password
        self.zhenwen = zhenwen
        self.port = port

    def send_email(self):
        server = None
        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(self.email, self.password)

            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = self.sendto
            message["Subject"] = self.subject
            message.attach(MIMEText(self.zhenwen, "plain"))

            server.sendmail(self.email, self.sendto, message.as_string())
            print("邮件发送成功！")
        except Exception:
            pass
        finally:
            if server is not None:
                server.quit()
