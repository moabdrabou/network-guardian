# --- Network Settings ---
# Replace with your actual network range.
# Example: If your router's IP is 192.168.1.1, your network range might be '192.168.1.0/24'.
# You can find your network by running `ipconfig` (Windows) or `ifconfig`/`ip a` (Linux/macOS)
NETWORK_SCAN_RANGE = '192.168.1.0/24' # IMPORTANT: Change this to your network!

# --- Database Settings ---
DATABASE_NAME = 'known_devices.db'
LOG_DIR = 'logs'
SCAN_LOG_FILE = f'{LOG_DIR}/scan_log.txt'

# --- Notification Settings (Choose one or more) ---
# Option 1: Print to console (always enabled)

# Option 2: Pushover Notification (Recommended for real-time alerts)
# Go to https://pushover.net/ to get your User Key and create an Application to get an API Token.(Requires onetime payment. You can try it for 30 days for free)
PUSHOVER_USER_KEY = 'uz3u5k8wg9kxia4v5vwvwf7of1wepw' # Replace with your Pushover User Key
PUSHOVER_API_TOKEN = 'apcoj79tb8g8rqaczjov3xboygyrbp' # Replace with your Pushover API Token
ENABLE_PUSHOVER = True # Set to True to enable Pushover notifications

# Option 3: Email Notification (Requires SMTP server details)
# EMAIL_SENDER = 'your_email@example.com'
# EMAIL_RECEIVER = 'your_recipient_email@example.com'
# EMAIL_PASSWORD = 'your_email_password' # Use app-specific passwords for better security
# EMAIL_SMTP_SERVER = 'smtp.example.com'
# EMAIL_SMTP_PORT = 587 # or 465 for SSL
# ENABLE_EMAIL = False # Set to True to enable email notifications

# Scan frequency in minutes
SCAN_INTERVAL_MINUTES = 10