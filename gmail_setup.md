# Gmail App Password Setup Guide

## Step 1: Enable 2-Factor Authentication (2FA)
1. Go to: https://myaccount.google.com/security
2. Find "2-Step Verification" and click on it
3. If not enabled, click "Get Started" and follow the setup process
4. You'll need to verify your phone number during setup

## Step 2: Generate App Password
1. After 2FA is enabled, go to: https://myaccount.google.com/apppasswords
2. You may need to sign in again
3. Under "Select app", choose "Mail"
4. Under "Select device", choose "Other (Custom name)"
5. Enter a name like: "Flask Antoine Calculator"
6. Click "Generate"
7. Copy the 16-character password (it will look like: xxxx xxxx xxxx xxxx)
8. **Important:** Remove the spaces when adding to .env file

## Step 3: Update Your .env File
Create or update your .env file in the project root:

```bash
# Database
DB_PASSWORD=your_mysql_password

# Gmail Configuration
MAIL_USERNAME=your_gmail_address@gmail.com
MAIL_PASSWORD=your_16_character_app_password_without_spaces
```

Example:
```bash
MAIL_USERNAME=john.doe@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop  # Remove spaces: abcdefghijklmnop
```

## Step 4: Test the Configuration
1. Restart your Flask application
2. Try registering a new user
3. Check the console output for debugging information
4. Check your email inbox for the verification code

## Common Issues & Solutions

### Issue: "SMTPAuthenticationError"
**Cause:** Using regular Gmail password instead of App Password
**Solution:** Generate a new App Password and use that instead

### Issue: "SMTPServerDisconnected"
**Cause:** Network connectivity or firewall issues
**Solution:** Check internet connection and firewall settings

### Issue: No email received
**Cause:** Email in spam folder or incorrect recipient
**Solution:** Check spam folder and verify email address

### Issue: "smtplib.SMTPException"
**Cause:** Gmail security settings blocking access
**Solution:** 
1. Ensure 2FA is enabled
2. Generate fresh App Password
3. Check "Less secure app access" is OFF (should be off with App Passwords)

## Testing Checklist
- [ ] 2FA enabled on Google Account
- [ ] App Password generated (16 characters)
- [ ] App password added to .env file (without spaces)
- [ ] Flask app restarted
- [ ] Console shows mail configuration values
- [ ] Email appears in inbox (not spam)
- [ ] Verification code works on verify page

## Debugging Information
The updated code will print these debug messages to console:
- Mail Server: smtp.gmail.com
- Mail Port: 587
- Mail Username: your_gmail@gmail.com
- Recipient: user_email@gmail.com
- "Attempting to send email..."
- "Email sent successfully!" OR error details

This will help you identify exactly where the process fails.
