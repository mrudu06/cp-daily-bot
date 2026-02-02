# CP Daily Bot - Contest Reminder

This script checks for upcoming competitive programming contests from **LeetCode** and **CodeChef** and sends a reminder to a specific WhatsApp group if any contests are scheduled for **tomorrow**.

## Features
- **Multi-Platform Support**: Checks both LeetCode and CodeChef.
- **Contest Check**: Fetches upcoming contests via their APIs.
- **Reminder**: Sends a message only if a contest is found for the next day.
- **Message Content**: Includes Platform, Contest Title, Time, and a request for screenshots.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Group ID**
   - Open `cp_bot.py`.
   - Locate the variable `GROUP_ID` at the top.
   - Replace `"YOUR_GROUP_ID_HERE"` with your actual WhatsApp Group ID.

3. **WhatsApp Web**
   - Ensure you are logged into WhatsApp Web on your default browser.

## Run

```bash
python cp_bot.py
```

- The script checks if there is a contest **tomorrow**.
- If found, it schedules a message for **2 minutes from now**.
- It will open a new browser tab for WhatsApp Web.
- **Do not switch tabs or minimize the window** while it's preparing to send.
