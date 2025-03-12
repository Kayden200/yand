from flask import Flask, jsonify
import imaplib
import email
import re

app = Flask(__name__)

# Yandex Mail Credentials (Use Environment Variables in Production)
YANDEX_EMAIL = "rylecohner@yandex.com"
YANDEX_PASSWORD = "kirbyisntscared321"  # ⚠️ Use a secure method to store passwords

def get_latest_otp():
    """Connect to Yandex Mail and retrieve the latest OTP from inbox."""
    try:
        # Connect to Yandex IMAP Server
        mail = imaplib.IMAP4_SSL("imap.yandex.com")
        mail.login(YANDEX_EMAIL, YANDEX_PASSWORD)
        mail.select("inbox")

        # Search for Unread Emails
        status, messages = mail.search(None, 'UNSEEN')  # Get unread emails
        message_ids = messages[0].split()

        if not message_ids:
            return {"error": "No unread OTP emails found"}

        # Fetch the latest email
        latest_email_id = message_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract OTP using Regex (Customize if needed)
        otp_match = re.search(r'\b\d{6}\b', msg.get_payload(decode=True).decode())
        otp_code = otp_match.group() if otp_match else "OTP not found"

        mail.logout()
        return {"otp": otp_code}

    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return "Welcome to the Yandex Email API! Available endpoints: /get_otp"

@app.route('/get_otp', methods=['GET'])
def get_otp():
    """Retrieve the latest OTP from Yandex Mail inbox."""
    return jsonify(get_latest_otp())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
