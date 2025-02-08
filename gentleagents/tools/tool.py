from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from gentleagents.loadenv.loadenv import SENDER_EMAIL, SENDER_PASSWORD
import smtplib

def add_numbers(a: int, b: int) -> int:
    """Use this function to add two numbers.
    
    Args:
        a: int: The first number
        b: int: The second number

    Returns:
        int: sum of a + b
    """
    return a + b

def sub_numbers(a: int, b: int) -> int:
    """Use this function to subtract two numbers.
    
    Args:
        a: int: The first number
        b: int: The second number

    Returns:
        int: result of a - b
    """
    return a - b

def send_email(recipient: str, subject: str, content: str) -> str: 
    """Use this function to send an email.

    Args:
        recipient:str: the recipients' email, comma seperated if multiple
        subject:str: the email subject
        content:str: the email body
    """
    
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(content, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, message.as_string())
        
        status = f"Successfully sent email to {recipient}"
        return status
    except Exception as e:
        print(f"Error in Email tool: {str(e)}")
        status = "Failed to send email."
        return status