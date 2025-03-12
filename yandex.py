import random
import requests

# Yandex credentials
YANDEX_EMAIL = "rylecohner@yandex.com"
YANDEX_PASSWORD = "kirbyisntscared321"

def generate_email():
    """Generate a Yandex email alias with a random number."""
    random_number = random.randint(100000, 999999)
    email_alias = f"rylecohner+{random_number}@yandex.com"
    print(f"Generated Email: {email_alias}")
    return email_alias

def check_otp(email):
    """Check for OTP messages in Yandex Mail."""
    session = requests.Session()
    
    # Replace with your Yandex Mail API authentication logic
    login_url = "https://passport.yandex.com/auth"
    inbox_url = "https://mail.yandex.com/api/v2.0/json/messages"
    
    payload = {
        "login": YANDEX_EMAIL,
        "passwd": YANDEX_PASSWORD
    }

    # Log in to Yandex
    response = session.post(login_url, data=payload)
    if response.status_code != 200:
        print("Login failed!")
        return None

    # Fetch emails
    response = session.get(inbox_url)
    if response.status_code == 200:
        messages = response.json().get("messages", [])
        for msg in messages:
            if email in msg["to"]:
                print(f"OTP Message: {msg['subject']}")
                return msg["subject"]
    else:
        print("Failed to fetch emails.")

    return None

# Run the script in Termux
if __name__ == "__main__":
    email = generate_email()
    otp = check_otp(email)

    if otp:
        print(f"OTP Found: {otp}")
    else:
        print("No OTP found.")
