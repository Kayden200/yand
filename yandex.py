import random
import imaplib
import email
import re
import os

# Set Yandex credentials (Use environment variables for security)
YANDEX_EMAIL = os.getenv("YANDEX_EMAIL", "rylecohner@yandex.com")
YANDEX_PASSWORD = os.getenv("YANDEX_PASSWORD", "kirbyisntscared321")

used_numbers = set()
min_number = 500

# Generate Unique Yandex Email
def generate_unique_email():
    while True:
        random_number = random.randint(min_number, 1000000)
        if random_number not in used_numbers:
            used_numbers.add(random_number)
            return f"rylecohner+{random_number}@yandex.com"

# Fetch OTP from Yandex Email
def get_yandex_otp():
    try:
        mail = imaplib.IMAP4_SSL("imap.yandex.com")  # Yandex IMAP server
        mail.login(YANDEX_EMAIL, YANDEX_PASSWORD)  # Login to Yandex account
        mail.select("INBOX")  # Select inbox

        # Search for unread emails
        result, data = mail.search(None, "UNSEEN")
        email_ids = data[0].split()

        for e_id in email_ids[::-1]:  # Check newest unread emails first
            result, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract email content
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8")

            # Extract OTP (Modify regex if needed)
            otp_match = re.search(r"\b\d{4,6}\b", body)
            if otp_match:
                return otp_match.group(0)  # Return the OTP

        return "No OTP found in unread emails."

    except Exception as e:
        return f"Error fetching OTP: {e}"

# CLI Menu
def main():
    while True:
        print("\nOptions:")
        print("1. Generate a unique Yandex email")
        print("2. Check OTP from Yandex inbox")
        print("3. Exit")

        choice = input("Enter choice (1-3): ")
        
        if choice == "1":
            print("Generated Email:", generate_unique_email())
        elif choice == "2":
            print("Latest OTP:", get_yandex_otp())
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
