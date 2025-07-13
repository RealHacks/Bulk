import pandas as pd
import time
from email.mime.text import MIMEText
import base64

def send_bulk_emails(service, excel_path, html_path, delay):
    df = pd.read_excel(excel_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    sent_count = 0
    for _, row in df.iterrows():
        message = MIMEText(html_content, 'html')
        message['to'] = row['Email']
        message['subject'] = row.get('Subject', 'No Subject')
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw}
        service.users().messages().send(userId='me', body=body).execute()
        sent_count += 1
        time.sleep(delay)
    return sent_count