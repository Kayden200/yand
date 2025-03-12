import random
import imaplib
import email
import re

# Set of used numbers to avoid duplicates
used_numbers = set()
min_number = 500

# Generate a unique Yandex email
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
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8")

            # Extract OTP from the email body
            otp_match = re.search(r"\b\d{4,6}\b", body)
            if otp_match:
                return otp_match.group(0)  # Return the OTP

        return "No OTP found in unread emails."

    except Exception as e:
        return f"Error fetching OTP: {e}"

# Main execution in Termux
if __name__ == "__main__":
    print("1. Generate a unique email")
    print("2. Check OTP from Yandex inbox")
    choice = input("Choose an option (1/2): ")

    if choice == "1":
        print("Generated Email:", generate_unique_email())
    elif choice == "2":
        email_address = "rylecohner@yandex.com"  # Replace with your Yandex email
        email_password = "hvxgkrgfcsggfqyw"  # Replace with your password
        print("Fetching OTP...")
        otp = get_yandex_otp(email_address, email_password)
        print("OTP:", otp)
    else:
        print("Invalid choice. Exiting.")
