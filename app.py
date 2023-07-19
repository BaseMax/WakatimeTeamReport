`
import time
import pytz
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from config import *

def send_telegram_message(bot_token, chat_id, message):
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {'chat_id': chat_id, 'text': message, 'parse_mode': 'MarkdownV2'}
    response = requests.post(url, data=params)
    if response.status_code == 200:
        print("Telegram message sent successfully!")
    else:
        print(f"Error sending Telegram message: {response.text}")

def generate_telegram_report(report):
    today_scaped = datetime.now().strftime('%Y-%m-%d').replace("-", "/")
    telegram_body = f"*Coding Activity Report* {today_scaped}\n\n"

    for user, data in report:
        total_hours = data['total_hours']
        total_time = data['total_time']
        telegram_body += f"*{user}*: {total_time}\n"

    return telegram_body

# Function to get the current time in Asia/Tehran timezone
def get_teheran_time():
    tehran_tz = pytz.timezone(TIME_ZONE)
    return datetime.now(tehran_tz)

# Function to retrieve coding activity for a user
def get_user_coding_activity(user_id):
    base_url = f'https://wakatime.com/api/v1/users/current/summaries?timezone=Asia/Tehran&start={START_DATE}&end={END_DATE}&api_key={user_id}'
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to generate the report
def generate_report():
    cache_coding_activity = {}
    for user, api_key in USERS.items():
        print("Checking", user)
        coding_activity = get_user_coding_activity(api_key)
        if coding_activity is not None:
            total_time = coding_activity[0].get('grand_total', {"text": "None"})['text']
            total_hours = sum(item['grand_total']['total_seconds'] / 3600 for item in coding_activity)
            project_names = ', '.join(set(item.get('name', '') for item in coding_activity[0].get('projects', [])))
            project_times = ', '.join(set(item.get('text', '') for item in coding_activity[0].get('projects', [])))

            # Use project_names as key and project_times as value, sort based on project_times
            project_data = dict(zip(project_names.split(', '), project_times.split(', ')))
            sorted_projects = sorted(project_data.items(), key=lambda x: x[1])  # TODO: We have bug! Please review and fix me.

            # Use project_names as key and project_times as value, sort refer to project_times
            cache_coding_activity[user] = {
                "total_time": total_time,
                "total_hours": total_hours,
                "projects": sorted_projects
            }
        else:
            cache_coding_activity[user] = {
                "total_time": "0 secs",
                "total_hours": 0,
                "projects": []
            }
    # Sort cache_coding_activity by total_hours
    sorted_cache = sorted(cache_coding_activity.items(), key=lambda x: x[1]['total_hours'], reverse=True)

    return sorted_cache

# Function to generate the email report
def generate_email_report(report):
    css_style = """
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
            }

            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }

            th {
                background-color: #f2f2f2;
            }

            h2 {
                color: #007BFF;
            }
        </style>
    """
email_body = f"""
        <html>
            <head>
                {css_style}
            </head>
            <body>
                <h2>Coding Activity Report</h2>
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Total Hours Worked</th>
                        <th>Projects</th>
                    </tr>
    """

for user, data in report:
    total_hours = data['total_hours']
    total_time = data['total_time']
    projects = data['projects']
    # Convert the list of tuples into a formatted string
    project_info = ',<br>'.join(f"{project[0]} ({project[1]})" for project in projects)
    email_body += f"<tr><td><b>{user}</b></td><td>{total_time}</td><td>{project_info}</td></tr>"

email_body += """
            </table>
          </body>
        </html>
    """
    return email_body

# Send the email
def send_email_report(email_receiver, email_content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_SENDER
    msg['To'] = email_receiver

    html_part = MIMEText(email_content, 'html')
    msg.attach(html_part)

    try:
        server = smtplib.SMTP_SSL('asrez.com', 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email_receiver, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Run the script daily
tehran_time = get_teheran_time()
schedule_time = tehran_time.replace(hour=SEND_AT_HOUR, minute=SEND_AT_MINUTE, second=SEND_AT_SECOND, microsecond=SEND_AT_MICROSECOND)
current_time = tehran_time
if current_time > schedule_time:
    schedule_time += timedelta(days=1)
time_diff = (schedule_time - current_time).total_seconds()
time_diff_hours = time_diff // 3600

# Wait until the scheduled time
print(f"Next email will be sent in {time_diff_hours} hours.")
# time.sleep(time_diff)

# Get report
report = generate_report()

# Send the email report
email_content = generate_email_report(report)
for email_receiver in EMAIL_RECEIVERS:
    send_email_report(email_receiver, email_content)

# Call the function to send the Telegram message
telegram_message = generate_telegram_report(report)
print(telegram_message)
send_telegram_message(BOT_TOKEN, CHAT_ID, telegram_message)
