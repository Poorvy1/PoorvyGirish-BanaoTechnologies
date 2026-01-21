import json
import smtplib
from email.message import EmailMessage

def send_email(event, context):
    body = json.loads(event["body"])

    email_type = body.get("type")
    to_email = body.get("to_email")

    subject = ""
    content = ""

    if email_type == "SIGNUP_WELCOME":
        subject = "Welcome to Mini HMS"
        content = "Thank you for registering with Mini Hospital Management System."

    elif email_type == "BOOKING_CONFIRMATION":
        subject = "Appointment Confirmed"
        content = "Your appointment has been successfully booked."

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid email type"})
        }

    # EMAIL CONFIG (Gmail SMTP)
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "yourgmail@gmail.com"
    msg["To"] = to_email
    msg.set_content(content)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("yourgmail@gmail.com", "your_app_password")
        server.send_message(msg)
        server.quit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
