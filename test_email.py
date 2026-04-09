# Add this test route to your app.py for debugging email issues

@app.route('/test-email')
def test_email():
    """Test email sending functionality"""
    try:
        print(f"Mail Server: {app.config['MAIL_SERVER']}")
        print(f"Mail Port: {app.config['MAIL_PORT']}")
        print(f"Mail Username: {app.config['MAIL_USERNAME']}")
        print(f"Mail Password configured: {'Yes' if app.config['MAIL_PASSWORD'] else 'No'}")
        
        msg = Message(
            'Test Email - Antoine Calculator',
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[app.config['MAIL_USERNAME']],  # Send to yourself for testing
            body='This is a test email to verify Flask-Mail configuration.'
        )
        
        print("Attempting to send test email...")
        mail.send(msg)
        print("Test email sent successfully!")
        
        return "Test email sent successfully! Check your inbox."
        
    except Exception as e:
        print(f"Test email failed: {type(e).__name__}: {str(e)}")
        print(f"Error details: {repr(e)}")
        return f"Test email failed: {str(e)}"
