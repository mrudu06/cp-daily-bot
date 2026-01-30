import requests
import pywhatkit
import datetime
import time

# REPLACE THIS WITH YOUR ACTUAL GROUP ID
# You can find this in the group invite link: chat.whatsapp.com/<GROUP_ID>
GROUP_ID = "YOUR_GROUP_ID_HERE"

LEETCODE_URL = "https://leetcode.com/graphql"

def fetch_daily_question():
    """Fetches the daily coding challenge from LeetCode GraphQL API."""
    query = """
    query questionOfToday {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
                title
                difficulty
                topicTags { name }
            }
        }
    }
    """
    try:
        response = requests.post(LEETCODE_URL, json={'query': query})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from LeetCode: {e}")
        return None

def format_message(data):
    """Formats the data into a nice WhatsApp message."""
    if not data or 'data' not in data or 'activeDailyCodingChallengeQuestion' not in data['data']:
        return None

    challenge = data['data']['activeDailyCodingChallengeQuestion']
    date = challenge['date']
    link = "https://leetcode.com" + challenge['link']
    question = challenge['question']
    title = question['title']
    difficulty = question['difficulty']
    
    # helper for topics
    tags = [tag['name'] for tag in question['topicTags']]
    tags_str = ", ".join(tags)

    message = f"🚀 *LeetCode Daily Challenge* - {date} 🚀\n\n"
    message += f"📅 *Problem:* {title}\n"
    message += f"🧩 *Difficulty:* {difficulty}\n"
    message += f"🏷️ *Topics:* {tags_str}\n\n"
    message += f"🔗 *Link:* {link}"
    
    return message

def send_whatsapp_message():
    """Main function to fetch data and send the WhatsApp message."""
    print("Fetching Daily Challenge...")
    data = fetch_daily_question()
    
    if not data:
        print("Failed to fetch data.")
        return

    message = format_message(data)
    if not message:
        print("Failed to format message.")
        return
    
    print("\n--- Generated Message ---")
    print(message)
    print("-------------------------\n")

    # Calculate time 2 minutes from now
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=2)
    
    print(f"Scheduling message for {send_time.hour:02d}:{send_time.minute:02d}...")
    print("Please ensure you are logged into WhatsApp Web.")
    
    try:
        # pywhatkit.sendwhatmsg_to_group will open the browser and send the message
        # wait_time is the time (in seconds) it waits for the code to be scanned/web to load before typing.
        # send_time.hour and send_time.minute specify WHEN to send.
        pywhatkit.sendwhatmsg_to_group(
            GROUP_ID, 
            message, 
            send_time.hour, 
            send_time.minute,
            wait_time=20,
            tab_close=True
        )
        print("Message scheduled/sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    send_whatsapp_message()
