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
It might change everything!
✅ Accurate Signals
🧠 Smart Risk Control
📈 Real Guidance

Follow me on IG: @_digital_agncy
Join VIP Now: 👉"""

# --- Auto-login ---
cl = Client()
SESSION_FILE = f"{USERNAME}_session.json"

def login():
    global cl
    try:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings(SESSION_FILE)
            print("✅ Session restored.")
        else:
            raise Exception("No session file found.")
    except:
        print("🔁 Logging in again...")
        cl = Client()
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ Logged in and session saved.")

# --- Load data ---
try:
    with open("sent_users.txt", "r") as f:
        sent_users = set(f.read().splitlines())
except FileNotFoundError:
    sent_users = set()

df = pd.read_excel("followers.xlsx")
usernames = df["userName"].dropna().unique()

# --- Helper Functions ---

def simulate_typing(text):
    typed = ""
    for char in text:
        typed += char
        time.sleep(random.uniform(0.03, 0.1))
    return typed

def already_chatted(username):
    try:
        user_id = cl.user_id_from_username(username)
        threads = cl.direct_threads(selected_filter="unread", amount=10)
        for thread in threads:
            if thread.users[0].username == username:
                print(f"💬 {username} has already chatted.")
                return True
    except:
        pass
    return False

# --- Send Messages ---
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
        cl.direct_send(simulate_typing(MESSAGE), [user_id])
        print(f"✅ Sent message to {username}")
        sent_users.add(username)
        with open("sent_users.txt", "a") as f:
            f.write(username + "\n")
        sent_count += 1
    except ClientError as e:
        print(f"❌ Failed to message {username}: {e}")
        continue

    # Delay between messages
    time.sleep(random.randint(60, 90))

    # Pause after every 5 messages
    if sent_count % 5 == 0:
        print("🕑 Sleeping 2 minutes to prevent blocking...")
        time.sleep(120)
