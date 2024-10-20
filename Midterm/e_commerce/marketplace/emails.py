import smtplib
from e_commerce.settings import GOOGLE_EMAIL, GOOGLE_EMAIL_APP_PASSWORD


def send_email(sent_to, email_subject, email_body):
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    try:
        smtpserver.ehlo()
        smtpserver.login(GOOGLE_EMAIL, GOOGLE_EMAIL_APP_PASSWORD)
        email_text = f"Subject: {email_subject}\n\n{email_body}"
        smtpserver.sendmail(GOOGLE_EMAIL, sent_to, email_text)
    except Exception as e:
        print(f"Error on sending email: {e}")
    finally:
        smtpserver.close()
