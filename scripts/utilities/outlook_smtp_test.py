import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

def load_email_config():
    try:
        with open('email_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Email configuration not found.")
        return None

def test_smtp_connection():
    config = load_email_config()
    if not config:
        return False
    
    try:
        # Create SMTP session with SSL
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        
        # Print server capabilities
        server.ehlo()  # Can usually omit this
        server.starttls()  # Enable encryption
        server.ehlo()  # Can usually omit this
        
        # Try to login
        server.login(config['email'], config['password'])
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config['email']
        msg['To'] = "ConnectwithPaid@outlook.com"
        msg['Subject'] = "Test message from MyAIEmployee assistant"
        
        body = "This is a test email to confirm that the email integration is working properly."
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print("Email sent successfully!")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        print("This suggests the credentials might be incorrect or the account requires special configuration.")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"Recipient was refused: {e}")
        return False
    except Exception as e:
        print(f"General error: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("Testing SMTP connection...")
    success = test_smtp_connection()
    if not success:
        print("\nPossible solutions:")
        print("1. Verify your app password is correct")
        print("2. Ensure your Outlook account allows 'Less secure app access' or has Modern Authentication configured")
        print("3. Consider using Microsoft Graph API instead of SMTP")