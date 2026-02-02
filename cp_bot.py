import requests
import pywhatkit
import datetime
import time

# REPLACE THIS WITH YOUR ACTUAL GROUP ID
GROUP_ID = "YOUR_GROUP_ID_HERE"

class PlatformFetcher:
    def fetch_contests(self):
        raise NotImplementedError

    def get_platform_name(self):
        raise NotImplementedError

class LeetCodeFetcher(PlatformFetcher):
    def get_platform_name(self):
        return "LeetCode"

    def fetch_contests(self):
        url = "https://leetcode.com/graphql"
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
            response = requests.post(url, json={'query': query})
            response.raise_for_status()
            data = response.json()
            if 'data' in data and 'contestV2UpcomingContests' in data['data']:
                return self._parse_contests(data['data']['contestV2UpcomingContests'])
            return []
        except Exception as e:
            print(f"Error fetching LeetCode data: {e}")
            return []

    def _parse_contests(self, contests_data):
        parsed = []
        for c in contests_data:
            start_dt = datetime.datetime.fromtimestamp(c['startTime'])
            parsed.append({
                'title': c['title'],
                'start_time': start_dt,
                'platform': 'LeetCode'
            })
        return parsed

class CodeChefFetcher(PlatformFetcher):
    def get_platform_name(self):
        return "CodeChef"
        
    def fetch_contests(self):
        url = "https://www.codechef.com/api/list/contests/all"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if 'future_contests' in data:
                return self._parse_contests(data['future_contests'])
            return []
        except Exception as e:
            print(f"Error fetching CodeChef data: {e}")
            return []

    def _parse_contests(self, contests_data):
        parsed = []
        for c in contests_data:
            # Format: "04 Feb 2026  20:00:00"
            date_str = c['contest_start_date']
            try:
                # Handle potential double spaces
                date_str = " ".join(date_str.split())
                start_dt = datetime.datetime.strptime(date_str, "%d %b %Y %H:%M:%S")
                parsed.append({
                    'title': c['contest_name'],
                    'start_time': start_dt,
                    'platform': 'CodeChef'
                })
            except ValueError:
                print(f"Could not parse date: {date_str}")
        return parsed

def format_reminder_message(contests):
    """Formats a message for multiple contests."""
    if not contests:
        return None

    message = f"🏆 *Upcoming Contest Reminder* 🏆\n\n"
    
    for contest in contests:
        title = contest['title']
        platform = contest['platform']
        start_time = contest['start_time'].strftime("%Y-%m-%d %I:%M %p")
        
        message += f"🚩 *{platform}*: {title}\n"
        message += f"⏰ *Time:* {start_time}\n"
        message += "----------------\n"

    message += f"\n⚠️ *Don't forget to register and participate!*\n"
    message += f"📸 *Please share a screenshot of your rank/participation after the contest!*"
    
    return message

def run_bot():
    print("Fetching upcoming contests from all platforms...")
    
    fetchers = [LeetCodeFetcher(), CodeChefFetcher()]
    tomorrow_contests = []
    
    now = datetime.datetime.now()
    tomorrow = now.date() + datetime.timedelta(days=1)
    print(f"Checking for contests on: {tomorrow}")

    for fetcher in fetchers:
        print(f"Checking {fetcher.get_platform_name()}...")
        contests = fetcher.fetch_contests()
        for c in contests:
            if c['start_time'].date() == tomorrow:
                tomorrow_contests.append(c)
                print(f"  -> Found: {c['title']} at {c['start_time']}")

    if not tomorrow_contests:
        print("No contests found for tomorrow.")
        return

    message = format_reminder_message(tomorrow_contests)
    print("\n--- Generated Message ---")
    print(message)
    print("-------------------------\n")

    # Calculate time 2 minutes from now
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
        print("Message scheduled successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    run_bot()
