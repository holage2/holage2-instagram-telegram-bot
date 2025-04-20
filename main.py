import time
import random
import pandas as pd
import os
from instagrapi import Client
from instagrapi.exceptions import ClientError

# Instagram credentials
USERNAME = "Danzylage"
PASSWORD = "Anshuti1122@"

# Message to send
MESSAGE = """Thanks For Your Query check this channel 🔥 
It might change everything! ✅ Accurate Signals 🧠 Smart Risk Control 📈 Real Guidance 
Follow me on IG: @_digital_agncy 
Join VIP Now: 👉 https://t.me/felix_roma"""

# Session file
SESSION_FILE = f"{USERNAME}_session.json"

# --- Auto-login with session restoration ---
def login():
    global cl
    cl = Client()
    try:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            print("✅ Session restored.")
        else:
            raise Exception("No session file.")
    except Exception as e:
        print("🔁 Re-logging in...")
        cl = Client()
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ Logged in fresh and session saved.")
    cl.dump_settings(SESSION_FILE)

# --- Simulate human typing ---
def simulate_typing(text):
    typed_text = ""
    for char in text:
        typed_text += char
        time.sleep(random.uniform(0.02, 0.07))  # Human typing simulation
    return typed_text

# --- Check if user already messaged ---
def already_chatted(username):
    try:
        user_id = cl.user_id_from_username(username)
        threads = cl.direct_threads(amount=20)
        for thread in threads:
            for user in thread.users:
                if user.username == username:
                    print(f"💬 {username} already chatted with you.")
                    return True
    except Exception:
        pass
    return False

# --- Load sent users and usernames ---
try:
    with open("sent_users.txt", "r") as f:
        sent_users = set(f.read().splitlines())
except FileNotFoundError:
    sent_users = set()

df = pd.read_excel("followers.xlsx")
usernames = df["userName"].dropna().unique()

# --- Start process ---
login()
sent_count = 0

for username in usernames:
    if username in sent_users:
        print(f"⏭️ Already messaged {username}, skipping.")
        continue

    if already_chatted(username):
        print(f"⏭️ {username} already messaged you, skipping.")
        continue

    try:
        user_id = cl.user_id_from_username(username)
        message_text = simulate_typing(MESSAGE)
        cl.direct_send(message_text, [user_id])
        print(f"✅ Sent to {username}")
        sent_users.add(username)

        with open("sent_users.txt", "a") as f:
            f.write(username + "\n")

        sent_count += 1

        # Anti-detection delay (90 to 120 seconds)
        delay = random.randint(90, 120)
        print(f"⏳ Waiting {delay} seconds before next...")
        time.sleep(delay)

        # Stress-free break every 5 messages
        if sent_count % 5 == 0:
            print("😴 Cooling down for 3 minutes...")
            time.sleep(180)

    except ClientError as e:
        print(f"❌ Error messaging {username}: {e}")
        continue
