import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep

def chat_gpt(prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
    except (requests.exceptions.RequestException, json.JSONDecodeError) as err:
        print(f"An error occurred: {err}")
        return None
    else:
        return response.json().get('choices', [{}])[0].get('message', {}).get('content')

def send_email(api_key, username, password, to):
    while True:
        subject = "Grammar with explanation"
        body = chat_gpt("introduce one topic to me use English, and show me the chinses" +
                        " meaning of some not common words, finally use Chinese to summary", api_key)

        if body is None:
            print("No content to send, skipping this iteration.")
            sleep(60*60*3)  # wait for 3 hours
            continue

        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login(username, password)
            text = msg.as_string()
            server.sendmail(username, to, text)
            server.quit()
        except smtplib.SMTPException as err:
            print(f"An error occurred while sending the email: {err}")
        else:
            print("Email sent successfully!")

        sleep(60*60*3)  # wait for 3 hours

# Prompt the user for their API key and email information
api_key = input("Enter your OpenAI API key: ")
username = input("Enter your email address: ")
password = input("Enter your email password: ")
to = input("Enter the recipient's email address: ")

# Call the function to start sending emails
send_email(api_key, username, password, to)
