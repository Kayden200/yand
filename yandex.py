from flask import Flask, jsonify
import random
import pyotp

app = Flask(__name__)

# Store generated emails and OTPs
generated_emails = {}
used_numbers = set()
min_number = 500

def generate_unique_number():
    """Generate a unique random number for email alias."""
    while True:
        random_number = random.randint(min_number, 1000000)
        if random_number not in used_numbers:
            used_numbers.add(random_number)
            return random_number

@app.route('/')
def home():
    return "Welcome to the Yandex Email API! Available endpoints: /generate_email, /check_otp"

@app.route('/generate_email', methods=['GET'])
def generate_email():
    """Generate a unique Yandex alias email."""
    email_counter = generate_unique_number()
    email = f"rylecohner+{email_counter}@yandex.com"
    
    # Generate and store OTP for this email
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()
    generated_emails[email] = otp

    return jsonify({"generated_email": email, "otp": otp})

@app.route('/check_otp/<email>', methods=['GET'])
def check_otp(email):
    """Check if an OTP exists for a generated email."""
    otp = generated_emails.get(email)
    if otp:
        return jsonify({"email": email, "otp": otp})
    else:
        return jsonify({"error": "OTP not found for this email"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
