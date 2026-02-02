import requests
import pywhatkit
import datetime
import time

# REPLACE THIS WITH YOUR ACTUAL GROUP ID
# You can find this in the group invite link: chat.whatsapp.com/<GROUP_ID>
GROUP_ID = ""

LEETCODE_URL = "https://leetcode.com/graphql"


def fetch_upcoming_contests():
    """Fetches upcoming contests from LeetCode GraphQL API."""
    query = """
    query {
        contestV2UpcomingContests {
            title
            startTime
            duration
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

def format_contest_message(contest):
    """Formats the contest reminder message."""
    title = contest['title']
    start_time_unix = contest['startTime']
    
    # Convert timestamp to local readable format
    start_time = datetime.datetime.fromtimestamp(start_time_unix)
    formatted_time = start_time.strftime("%Y-%m-%d %I:%M %p")
    
    message = f"🏆 *Upcoming LeetCode Contest Reminder* 🏆\n\n"
    message += f"📅 *Event:* {title}\n"
    message += f"⏰ *Time:* {formatted_time}\n\n"
    message += f"⚠️ *Don't forget to register and participate!*\n"
    message += f"� *Please share a screenshot of your rank/participation after the contest!*"
    
    return message

def send_contest_reminder():
    """Checks for contests tomorrow and sends a reminder."""
    print("Fetching Upcoming Contests...")
    data = fetch_upcoming_contests()
    
    if not data or 'data' not in data or 'contestV2UpcomingContests' not in data['data']:
        print("Failed to fetch contest data.")
        return

    contests = data['data']['contestV2UpcomingContests']
    
    # Check for contests happening "tomorrow"
    now = datetime.datetime.now()
    tomorrow = now.date() + datetime.timedelta(days=1)
    
    contest_to_notify = None
    
    for contest in contests:
        start_time_unix = contest['startTime']
        contest_date = datetime.datetime.fromtimestamp(start_time_unix).date()
        
        if contest_date == tomorrow:
            contest_to_notify = contest
            break
            
    if not contest_to_notify:
        print(f"No contest found for tomorrow ({tomorrow}).")
        print("Existing contests:")
        for c in contests:
            ts = datetime.datetime.fromtimestamp(c['startTime'])
            print(f"- {c['title']} at {ts}")
        return

    message = format_contest_message(contest_to_notify)
    print("\n--- Generated Message ---")
    print(message)
    print("-------------------------\n")

    # Calculate time 2 minutes from now for sending
    send_time = now + datetime.timedelta(minutes=2)
    
    print(f"Scheduling message for {send_time.hour:02d}:{send_time.minute:02d}...")
    
    try:
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
    # The user requested to replace functionality ("instead..."), so we run the contest reminder.
    send_contest_reminder()
