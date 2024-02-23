# Feb 23, 2024: Created by Kumar Anurag <me@kmranrg.com>

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Email configuration
email_from = 'reminder@smartgurucool.com'
email_to = 'me@kmranrg.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'smartgurucool@gmail.com'
smtp_password = open('pwd.txt').read()

# Function to send email
def send_email(subject, message):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = subject

        # Add message body
        msg.attach(MIMEText(message, 'html'))

        # Send the email
        server.sendmail(email_from, email_to, msg.as_string())
        print(f"At {time.strftime('%Y-%m-%d %H:%M:%S')}, email sent successfully!")

        # Quit the SMTP server
        server.quit()
    except Exception as e:
        print("At {time.strftime('%Y-%m-%d %H:%M:%S')}, failed to send email:", e)

# Function to read tasks from files
def read_tasks(filename):
    with open(filename, 'r') as file:
        tasks = file.readlines()
    return tasks

# Function to generate email content
def generate_email_content():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    completed_tasks = read_tasks('completed.txt')
    inprogress_tasks = read_tasks('inprogress.txt')
    todo_tasks = read_tasks('todo.txt')

    # Format the email content in HTML with CSS styling
    email_content = f"""
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        line-height: 1.6;
      }}
      .container {{
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 5px;
      }}
      .banner {{
        background-color: black;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
      }}
      .footer {{
        background-color: black;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
        font-size: 14px;
        margin-top: 20px;
      }}
      .title {{
        font-size: 16px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
      }}
      .timestamp {{
        font-size: 12px;
        font-weight: bold;
        color: #333;
        text-align: right;
      }}
      .list {{
        padding-left: 20px;
      }}
      .list-item {{
        margin-bottom: 5px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="banner">
        <p style="font-size: 24px;">Task Status Update</p>
      </div>
      <p class="timestamp"><strong>Timestamp (IST):</strong> {timestamp}</p>
      <p>Hello Anurag,</p>
      <p>Please find the status mentioned below.</p>
      
      <p class="title">Completed Tasks:</p>
      <ol class="list">
        {''.join(f"<li class='list-item'>{task.strip()}</li>" for task in completed_tasks)}
      </ol>
      
      <p class="title">In Progress Tasks:</p>
      <ol class="list">
        {''.join(f"<li class='list-item'>{task.strip()}</li>" for task in inprogress_tasks)}
      </ol>
      
      <p class="title">To Do Tasks:</p>
      <ol class="list">
        {''.join(f"<li class='list-item'>{task.strip()}</li>" for task in todo_tasks)}
      </ol>
      
      <p class="footer">SmartGurucool</p>
    </div>
  </body>
</html>
"""
    return email_content

# Send email with task status
subject = "Task Status Update"
message = generate_email_content()
send_email(subject, message)
