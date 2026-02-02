import requests
import json

def check_contests():
    url = "https://leetcode.com/graphql"
    query = """
    query {
        upcomingContests {
            title
            startTime
            duration
        }
    }
    """
    try:
        response = requests.post(url, json={'query': query})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
        
    query2 = """
    query {
        contestV2UpcomingContests {
            title
            startTime
            duration
        }
    }
    """
    try:
        response = requests.post(url, json={'query': query2})
        print(f"Status Code 2: {response.status_code}")
        print(f"Response 2: {response.text}")
    except Exception as e:
        print(f"Error 2: {e}")

if __name__ == "__main__":
    check_contests()
