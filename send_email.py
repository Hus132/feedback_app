# Import the smtplib module for sending emails
import smtplib
# Import MIMEText for creating email messages with HTML content
from email.mime.text import MIMEText

# Define a function to send an email with feedback details
def send_mail(customer, dealer, rating, comments):
    port = 2525  # Specify the SMTP port for Mailtrap
    smtp_server = "sandbox.smtp.mailtrap.io"  # SMTP server address for Mailtrap
    login = '07f42ffe5ee026'  # Login credentials for the SMTP server
    password = 'ae0a4f62676608'  # Password for the SMTP server
    # Construct the email body with feedback details in HTML format
    message = (f"<h3> New feedback submission </h3> <ul><li>{customer}</li> <li>{dealer}</li> <li>{rating}</li>"
               f"<li>{comments}</li></ul>")
    sender_email = "Private Person <from@example.com>"  # Sender's email address
    receiver_email = "A Test User <to@example.com>"  # Receiver's email address
    msg = MIMEText(message, 'html')  # Create an email message object with HTML content
    msg['Subject'] = 'lexus feedback'  # Set the email subject
    msg['From'] = sender_email  # Set the sender's email address in the message
    msg['To'] = receiver_email  # Set the receiver's email address in the message

    # Establish a connection to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Start TLS encryption for secure communication
        server.login(login, password)  # Log in to the SMTP server with credentials
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email