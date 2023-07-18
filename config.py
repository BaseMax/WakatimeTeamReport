# Set user information with their respective Wakatime API keys
USERS = {
	'Max': '.............',
}

TIME_ZONE = 'Asia/Tehran'

# Telegram Bot Token and Chat ID
bot_token = '473681081:xxxxxxxxxxx'
chat_id = '-xxxxxxxxxxx'

# Set start and end date for coding activity report
today = datetime.now().strftime('%Y-%m-%d')
# today = '2023/07/16'
start_date = today
end_date = today

# Set email parameters
email_subject = f"Coding Activity Report - {today}"
email_sender = 'max@asrez.com'
email_receivers = [
  'maxbasecode@gmail.com',
  '98@hi2.in'
]
email_password = 'XXXX'
