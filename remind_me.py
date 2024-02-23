import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

# Email configuration
email_from = 'reminder@smartgurucool.com'
email_to = 'me@kmranrg.com'
smtp_server = 'smtp.office365.com'
smtp_port = 587
smtp_username = 'me@kmranrg.com'
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
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.sendmail(email_from, email_to, msg.as_string())
        print("Email sent successfully!")

        # Quit the SMTP server
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

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

    email_content = f"""\
    Timestamp: {timestamp}

    Completed Tasks:
    {''.join(completed_tasks)}

    In Progress Tasks:
    {''.join(inprogress_tasks)}

    To Do Tasks:
    {''.join(todo_tasks)}
    """
    return email_content

# Function to send email with task status
def send_task_status_email():
    subject = "Task Status Update"
    message = generate_email_content()
    send_email(subject, message)

# Schedule the reminder every 8 hours
schedule.every(8).hours.do(send_task_status_email)

# Main loop to run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
