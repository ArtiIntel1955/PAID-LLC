# Email Configuration Notes

## Issue Encountered
When attempting to send an email via PowerShell's Send-MailMessage cmdlet, we received an authentication error:
"5.7.57 Client not authenticated to send mail. The server response was: 5.7.53 SMTP; Client was rejected. Authenticated users only."

## Outlook/Office 365 SMTP Requirements
- For Office 365 accounts, modern authentication is often required
- The account may need to have SMTP authentication specifically enabled
- May require using OAuth2 instead of basic authentication

## Alternative Solutions
1. Enable SMTP AUTH for the mailbox (requires admin rights)
2. Use the Microsoft Graph API instead of SMTP
3. Use an app password if two-factor authentication is enabled
4. Consider using a dedicated email management tool

## Current Status
Email receiving (IMAP) should still work, but sending emails via SMTP requires additional configuration due to Office 365 security policies.