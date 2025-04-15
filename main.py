import time
import random
import pandas as pd
from instagrapi import Client
from instagrapi.exceptions import ClientError

# Instagram credentials
USERNAME = "Danzylage"
PASSWORD = "Anshuti1122@"

# Message to send
MESSAGE = """Thanks For Your Query check this channel 🔥 It might change everything!

✅ Accurate Signals
🧠 Smart Risk Control
📈 Real Guidance

Follow me on IG: @_digital_agncy
Join VIP Now: 👉"""

# Load already messaged users
try:
    with open("sent_users.txt", "r") as f:
        sent_users = set(f.read().splitlines())
except FileNotFoundError:
    sent_users = set()

# Load Excel data
df = pd.read_excel("followers.xlsx")
usernames = df["userName"].dropna().unique()

# Login to Instagram
cl = Client()
cl.login(USERNAME, PASSWORD)

def simulate_typing(text):
    # Simulate human typing
    typed = ""
    for char in text:
        typed += char
        time.sleep(random.uniform(0.03, 0.1))
    return typed

# Send messages with delay and logging
for username in usernames:
    if username in sent_users:
        print(f"Already messaged {username}, skipping.")
        continue
    try:
        user_id = cl.user_id_from_username(username)
        cl.direct_send(simulate_typing(MESSAGE), [user_id])
        print(f"✅ Sent message to {username}")
        with open("sent_users.txt", "a") as f:
            f.write(username + "\n")
        time.sleep(random.randint(60, 90))
    except ClientError as e:
        print(f"❌ Failed to send message to {username}: {e}")
        continue