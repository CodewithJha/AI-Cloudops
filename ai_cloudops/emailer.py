import smtplib
from email.mime.text import MIMEText
from tkinter import simpledialog, messagebox
from .config import email_config


def send_email_interactive():
    recipient_email = simpledialog.askstring(
        "Recipient's Email", "Enter the recipient's email address:"
    )
    if not recipient_email:
        messagebox.showerror("Error", "Recipient email is required.")
        return

    subject = simpledialog.askstring("Email Subject", "Enter the email subject:") or ""
    body = simpledialog.askstring("Email Body", "Enter the email body:") or ""

    try:
        send_email(recipient_email, subject, body)
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as exc:
        messagebox.showerror("Error", f"Failed to send email: {exc}")


def send_email(to_address: str, subject: str, body: str):
    if not email_config.username or not email_config.password or not email_config.from_address:
        raise RuntimeError("SMTP credentials are not configured. Check your .env.")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_config.from_address
    msg["To"] = to_address

    server = smtplib.SMTP(email_config.host, email_config.port, timeout=30)
    try:
        server.starttls()
        server.login(email_config.username, email_config.password)
        server.sendmail(email_config.from_address, [to_address], msg.as_string())
    finally:
        server.quit()

