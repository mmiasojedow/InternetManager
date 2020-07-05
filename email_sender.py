import datetime
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'your.raspberry.pi@email.com'
password = 'your.raspberry.pi.email.password'
send_to_email = 'your@email.com'
subject = 'Daily raport'
message = 'Send from Raspberry Pi \n \n'
date = datetime.datetime.now().strftime('%d.%m')

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

# Setup the attachment
files = [
    (f'./wifi_history/wifi_history_{date}.txt', 'wifi_history.txt'),
    (f'./speed_history/speed_history_{date}.txt', 'speed_history.txt')
    ]

for file in files:
    attachment = open(file[0], 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {file[1]}')

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()
