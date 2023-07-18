# Wakatime Team Member Daily Report Generator

This Python script generates a daily report for the team lead to monitor the hourly work of team members. It tracks the number of hours spent by team members on various projects and sends the report to a Telegram group and the director's email.

## Prerequisites

Before running the script, ensure that you have the following dependencies installed:

- time
- pytz
- email
- smtplib
- requests
- datetime

## Configuration

To use this script, you need to set up the configuration in the config.py file. Please complete the following information:

### User Information

Provide the names of team members as keys and their respective Wakatime API keys as values in the USERS dictionary:

```python
USERS = {
    'Max': '.............',
    # Add more users here if needed
}
```

### Time Configuration

Set the timezone and the time when you want the script to send the report:

```python
TIME_ZONE = 'Asia/Tehran'
SEND_AT_HOUR = 0
SEND_AT_MINUTE = 0
SEND_AT_SECOND = 0
SEND_AT_MICROSECOND = 0
```

### Telegram Bot and Chat Information

Configure the Telegram bot token and chat ID:

```python
BOT_TOKEN = '473681081:xxxxxxxxxxx'
CHAT_ID = '-xxxxxxxxxxx'
```

### Date Range for the Coding Activity Report

Set the start and end dates for the coding activity report. By default, it will be set to today's date:

```python
TODAY = datetime.now().strftime('%Y-%m-%d')
START_DATE = TODAY
END_DATE = TODAY
```

### Email Configuration

Provide the necessary information for sending the daily report via email:

```python
EMAIL_SUBJECT = f"Coding Activity Report - {TODAY}"
EMAIL_SENDER = 'max@asrez.com'
EMAIL_RECEIVERS = [
  'maxbasecode@gmail.com',
  '98@hi2.in'
]
EMAIL_PASSWORD = 'XXXX'
```

## How to Run

- Install the required dependencies mentioned in the "Prerequisites" section.

- Configure the config.py file with the necessary information.

- Run the script. It will generate the daily report for team members and send it to the Telegram group and email recipients based on the configured schedule.

- Please make sure to keep the script running daily to get the regular reports as scheduled.

Note: Replace the placeholder values marked with ............., xxxxxxxxxxx, and XXXX in the `config.py` file with the actual API keys, tokens, chat IDs, and passwords for proper functionality.

Copyright 2023, Max Base
