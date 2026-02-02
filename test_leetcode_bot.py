import unittest
from unittest.mock import patch, MagicMock
import leetcode_bot
import datetime

class TestLeetCodeBot(unittest.TestCase):

    def test_format_contest_message(self):
        """Test formatting contest message."""
        # Contest time: 2023-10-27 12:00:00 (approx)
        start_time = 1698408000 
        sample_contest = {
            'title': 'Weekly Contest 999',
            'startTime': start_time,
            'duration': 5400
        }
        
        message = leetcode_bot.format_contest_message(sample_contest)
        
        self.assertIn("Weekly Contest 999", message)
        self.assertIn("Don't forget to register", message)
        self.assertIn("share a screenshot", message)

    @patch('leetcode_bot.requests.post')
    def test_fetch_upcoming_contests_success(self, mock_post):
        """Test fetching contests successfully."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        expected_json = {'data': {'contestV2UpcomingContests': []}}
        mock_response.json.return_value = expected_json
        mock_post.return_value = mock_response

        result = leetcode_bot.fetch_upcoming_contests()
        self.assertEqual(result, expected_json)

    @patch('builtins.print')
    @patch('leetcode_bot.pywhatkit.sendwhatmsg_to_group')
    @patch('leetcode_bot.fetch_upcoming_contests')
    def test_send_contest_reminder_found(self, mock_fetch, mock_sendwhatmsg, mock_print):
        """Test sending logic when a contest is tomorrow."""
        # Set "Tomorrow" to match the contest date
        tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
        # Create a timestamp for tomorrow at noon
        tomorrow_noon = datetime.datetime.combine(tomorrow_date, datetime.time(12, 0))
        timestamp = int(tomorrow_noon.timestamp())
        
        mock_fetch.return_value = {
            'data': {
                'contestV2UpcomingContests': [
                    {
                        'title': 'Next Day Contest',
                        'startTime': timestamp,
                        'duration': 5400
                    }
                ]
            }
        }
        
        leetcode_bot.send_contest_reminder()
        
        # Should call sendwhatmsg since contest is "tomorrow"
        mock_sendwhatmsg.assert_called_once()
    
    @patch('builtins.print')
    @patch('leetcode_bot.pywhatkit.sendwhatmsg_to_group')
    @patch('leetcode_bot.fetch_upcoming_contests')
    def test_send_contest_reminder_not_found(self, mock_fetch, mock_sendwhatmsg, mock_print):
        """Test logic when NO contest is tomorrow."""
        # Contest is today (not tomorrow)
        today_date = datetime.date.today()
        today_noon = datetime.datetime.combine(today_date, datetime.time(12, 0))
        timestamp = int(today_noon.timestamp())
        
        mock_fetch.return_value = {
            'data': {
                'contestV2UpcomingContests': [
                    {
                        'title': 'Today Contest',
                        'startTime': timestamp,
                        'duration': 5400
                    }
                ]
            }
        }
        
        leetcode_bot.send_contest_reminder()
        
        
        # Should NOT call sendwhatmsg
        mock_sendwhatmsg.assert_not_called()


if __name__ == '__main__':
    unittest.main()
