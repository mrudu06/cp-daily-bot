 # LeetCode Daily Challenge WhatsApp Bot

This script fetches the "Question of the Day" from LeetCode and sends it to a specified WhatsApp group.

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Group ID**
   - Open `leetcode_bot.py`.
   - Locate the variable `GROUP_ID` at the top.
   - Replace `"YOUR_GROUP_ID_HERE"` with your actual WhatsApp Group ID.
     - *Tip: If your group invite link is `https://chat.whatsapp.com/AbCdEfGhIjKlMnOpQrStUv`, your Group ID is `AbCdEfGhIjKlMnOpQrStUv`.*

3. **WhatsApp Web**
   - Ensure you are logged into WhatsApp Web on your default browser.
   - The script uses `pywhatkit`, which automates the browser.

## Run

```bash
python leetcode_bot.py
```

- The script will calculate a send time of **2 minutes from now**.
- It will open a new browser tab for WhatsApp Web.
- **Do not switch tabs or minimize the window** while it's preparing to send.
