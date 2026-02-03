import json
import imaplib

def load_email_config():
    try:
        with open('email_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Email configuration not found.")
        return None

def check_inbox():
    config = load_email_config()
    if not config:
        return False
    
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        
        # Login
        mail.login(config['email'], config['password'])
        
        # Select mailbox
        mail.select('INBOX')
        
        # Search for all emails in inbox
        status, messages = mail.search(None, 'ALL')
        
        if status == 'OK':
            email_ids = messages[0].split()
            print(f"You have {len(email_ids)} emails in your inbox")
            
            if len(email_ids) > 0:
                # Get the latest 5 emails as a sample
                latest_emails = email_ids[-5:]  # Last 5 emails
                
                for i, email_id in enumerate(reversed(latest_emails)):
                    status, msg_data = mail.fetch(email_id, '(RFC822.HEADER)')
                    if status == 'OK':
                        print(f"\n--- Email {i+1} ---")
                        print(f"ID: {email_id.decode()}")
                        
                        # Note: For a full implementation, we would parse the email headers here
                        
            else:
                print("No emails found in inbox")
        else:
            print("Could not retrieve emails")
        
        # Logout
        mail.logout()
        return True
        
    except Exception as e:
        print(f"Error checking email: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking email inbox...")
    success = check_inbox()
    if success:
        print("\nEmail inbox check completed successfully!")
    else:
        print("\nFailed to check email inbox.")