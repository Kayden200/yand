import random
import imaplib
import email
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

used_numbers = set()
min_number = 500

# Generate unique Yandex email
def generate_unique_email():
    while True:
        random_number = random.randint(min_number, 1000000)
        if random_number not in used_numbers:
            used_numbers.add(random_number)
            return f"rylecohner+{random_number}@yandex.com"

# Fetch OTP from Yandex Email
def get_yandex_otp(email_address, email_password):
    try:
        mail = imaplib.IMAP4_SSL("imap.yandex.com")  # Yandex IMAP server
        mail.login(email_address, email_password)  # Login to Yandex account
        mail.select("INBOX")  # Select inbox
        
        # Search for unread emails
        result, data = mail.search(None, "UNSEEN")
        email_ids = data[0].split()

        for e_id in email_ids[::-1]:  # Check newest unread emails first
            result, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract email content
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8")

            # Extract OTP from the email body (modify regex as needed)
            import re
            otp_match = re.search(r"\b\d{4,6}\b", body)
            if otp_match:
                return otp_match.group(0)  # Return the OTP

        return "No OTP found in unread emails."
    
    except Exception as e:
        return f"Error fetching OTP: {e}"

# Flask Route: Generate Unique Email
@app.route('/generate_email', methods=['GET'])
def generate_email():
    email = generate_unique_email()
    return jsonify({"email": email})

# Flask Route: Check Yandex Emails for OTP
@app.route('/check_otp', methods=['POST'])
def check_otp():
    email_address = "rylecohner@yandex.com"  # Your Yandex email
    email_password = "kirbyisntscared321"  # Replace with your Yandex password
    
    otp = get_yandex_otp(email_address, email_password)
    return jsonify({"otp": otp})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
