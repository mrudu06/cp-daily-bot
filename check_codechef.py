import requests
import json

def check_codechef_contests():
    url = "https://www.codechef.com/api/list/contests/all"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        # Check for 'future_contests'
        if 'future_contests' in data:
            print(f"Found {len(data['future_contests'])} future contests.")
            for contest in data['future_contests'][:3]: # Print first 3
                print(f"- {contest.get('contest_name')} starts at {contest.get('contest_start_date')}")
        else:
            print("No 'future_contests' key found.")
            print(f"Keys: {data.keys()}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_codechef_contests()
