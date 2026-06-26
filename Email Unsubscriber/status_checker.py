import os
import imaplib
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("GMAIL_USER")
app_password = os.getenv("GMAIL_APP_PASSWORD")

# Count how many unique links we have successfully clicked in the past
successful_clicks = 0
if os.path.exists("successful_unsubscribes.txt"):
    with open("successful_unsubscribes.txt", "r", encoding="utf-8") as f:
        # Using a set eliminates duplicate clicks on the same link
        unique_links = set(line.strip() for line in f if line.strip())
        successful_clicks = len(unique_links)

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, app_password)
    mail.select("inbox", readonly=True)

    # Check Total Unread Emails
    _, unread_msg = mail.search(None, "UNSEEN")
    total_unread = len(unread_msg[0].split())

    # Check Emails still matching "unsubscribe"
    _, unsub_msg = mail.search(None, 'X-GM-RAW "unsubscribe"')
    total_unsub = len(unsub_msg[0].split())

    # Print the updated dashboard
    print("\n" + "="*40)
    print("       GMAIL AUTOMATION STATUS       ")
    print("="*40)
    print(f"📧 Connected Account : {username}")
    print(f"🔵 Total Unread Mails: {total_unread}")
    print(f"📩 Remaining Unsubs  : {total_unsub}")
    print(f"✅ Total Unsubscribed: {successful_clicks} links") # <-- New Stat!
    print("="*40 + "\n")

except Exception as e:
    print(f"❌ Status Check Failed: {e}")
finally:
    try:
        mail.logout()
    except:
        pass
