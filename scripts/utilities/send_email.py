import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_email_config():
    try:
        with open('email_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Email configuration not found.")
        return None

def send_email(to_email, subject, body):
    config = load_email_config()
    if not config:
        return False
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = config['email']
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add body to email
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()  # Enable security
        server.login(config['email'], config['password'])  # Login with sender's email and password
        
        # Send email
        text = msg.as_string()
        server.sendmail(config['email'], to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    to_email = "ConnectwithPaid@outlook.com"
    subject = "Test message from MyAIEmployee assistant"
    body = "This is a test email to confirm that the email integration is working properly."
    
    success = send_email(to_email, subject, body)
    if success:
        print("Test email sent successfully!")
    else:
        print("Failed to send test email.")