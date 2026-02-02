import unittest
from unittest.mock import patch, MagicMock
import cp_bot
import datetime

class TestCPBot(unittest.TestCase):

    def test_format_reminder_message(self):
        """Test formatting message with multiple contests."""
        sample_contests = [
            {
                'title': 'Weekly Contest 100',
                'start_time': datetime.datetime(2023, 10, 27, 12, 0),
                'platform': 'LeetCode'
            },
            {
                'title': 'Starters 50',
                'start_time': datetime.datetime(2023, 10, 27, 20, 0),
                'platform': 'CodeChef'
            }
        ]
        
        message = cp_bot.format_reminder_message(sample_contests)
        
        self.assertIn("Upcoming Contest Reminder", message)
        self.assertIn("LeetCode*: Weekly Contest 100", message)
        self.assertIn("CodeChef*: Starters 50", message)
        self.assertIn("2023-10-27 12:00 PM", message)

    @patch('cp_bot.requests.post')
    def test_leetcode_fetcher(self, mock_post):
        """Test LeetCode fetcher parsing."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'data': {
                'contestV2UpcomingContests': [
                    {'title': 'LC Contest', 'startTime': 1700000000, 'duration': 5400}
                ]
            }
        }
        mock_post.return_value = mock_response

        fetcher = cp_bot.LeetCodeFetcher()
        results = fetcher.fetch_contests()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'LC Contest')
        self.assertEqual(results[0]['platform'], 'LeetCode')

    @patch('cp_bot.requests.get')
    def test_codechef_fetcher(self, mock_get):
        """Test CodeChef fetcher parsing."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'future_contests': [
                {'contest_name': 'CC Contest', 'contest_start_date': '04 Feb 2026 20:00:00'}
            ]
        }
        mock_get.return_value = mock_response

        fetcher = cp_bot.CodeChefFetcher()
        results = fetcher.fetch_contests()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'CC Contest')
        self.assertEqual(results[0]['platform'], 'CodeChef')
        self.assertEqual(results[0]['start_time'].year, 2026)

    @patch('builtins.print')
    @patch('cp_bot.pywhatkit.sendwhatmsg_to_group')
    @patch.object(cp_bot.LeetCodeFetcher, 'fetch_contests')
    @patch.object(cp_bot.CodeChefFetcher, 'fetch_contests')
    def test_run_bot_integration(self, mock_cc, mock_lc, mock_send, mock_print):
        """Test that the bot aggregates results and sends message."""
        tomorrow = datetime.datetime.now().date() + datetime.timedelta(days=1)
        start_dt = datetime.datetime.combine(tomorrow, datetime.time(10, 0))
        
        mock_lc.return_value = [{
            'title': 'Tomorrow LC',
            'start_time': start_dt,
            'platform': 'LeetCode'
        }]
        mock_cc.return_value = []
        
        cp_bot.run_bot()
        
        mock_send.assert_called_once()
        args, _ = mock_send.call_args
        self.assertIn("Tomorrow LC", args[1])

if __name__ == '__main__':
    unittest.main()
