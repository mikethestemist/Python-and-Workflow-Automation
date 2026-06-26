# to run this script, make an '.env' file and put in your email and app password
# install dot-env, beautiful soup and request

import os
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("GMAIL_USER")
app_password = os.getenv("GMAIL_APP_PASSWORD")

def get_html_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html" and "attachment" not in str(part.get("Content-Disposition")):
                return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
    else:
        if msg.get_content_type() == "text/html":
            return msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')
    return None

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, app_password)
    mail.select("inbox", readonly=True)

    status, messages = mail.search(None, 'X-GM-RAW "unsubscribe"')
    email_ids = messages[0].split()

    # Use a set to automatically filter out duplicate links
    failed_links = set()

    print(f"Processing {len(email_ids)} emails...")

    # Looping through the last 10 emails for this test
    for email_id in email_ids[-10:]:
        status, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        html_body = get_html_body(msg)
        if html_body:
            soup = BeautifulSoup(html_body, "html.parser")
            links = soup.find_all("a", href=True)
            
            for link in links:
                link_text = link.get_text().lower()
                if "unsubscribe" in link_text:
                    url = link['href']
                    
                    try:
                        response = requests.get(url, timeout=10)
                        
                        # If it returns a success code, we assume it worked
                        if response.status_code == 200:
                            print(f"✅ Success: {url[:60]}...")
                        else:
                            # HTTP error (e.g., 404, 500, 403), add to failed set
                            print(f"⚠️ Server Error ({response.status_code}): {url[:60]}...")
                            failed_links.add(url)
                            
                    except Exception as e:
                        # Network error, timeout, or bad URL, add to failed set
                        print(f"❌ Connection Failed: {url[:60]}...")
                        failed_links.add(url)
                        
    # --- SAVE FAILED LINKS TO A FILE ---
    if failed_links:
        output_file = "failed_unsubscribes.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            for link in failed_links:
                f.write(f"{link}\n")
        
        print(f"\nTask complete! Saved {len(failed_links)} unique failed/unconfirmed links to '{output_file}'")
    else:
        print("\nTask complete! All links clicked successfully with no errors.")

except Exception as e:
    print(f"Something went wrong with the script: {e}")
finally:
    try:
        mail.close()
        mail.logout()
    except:
        pass