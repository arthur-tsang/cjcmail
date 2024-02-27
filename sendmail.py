"""
Script to send emails about our fortnightly cosmology journal club. Speaker data comes from the spreadsheet linked in `spreadsheetfinder.py` and our basic email template is stored as `template.html`. This script automatically picks the speaker info for the next event in the future (defined by comparing dates), prints the info to the terminal, and prints the destination email address. If this looks good, entering the 16-character App ID is sufficient to send the email. I believe no pip installations are required for this main functionality.

To create an app password, make sure 2-step in the google account settings is enabled and go here:
https://myaccount.google.com/u/1/apppasswords

"""

import re
import csv
import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import getpass

from sheetfinder import download_speaker_csv

def template_fill(dico):
    ## TODO: add alternate template (and corresponding dico format) for guest speakers

    keys = ['date', 'speaker', 'topic', 'mod']
    assert all(key in dico for key in keys)

    with open('template.html', 'r') as f:
        template = ''.join(f.readlines())

        for key in keys:
            template = re.sub('{' + key + '}', dico[key], template)

    ## Read zoom link from `zoomlink.txt`
    try:
        with open('zoomlink.txt', 'r') as f:
            zoomlink = ''.join(f.readlines()).strip()
            assert len(zoomlink) > 0
            print(f'Zoom link: {zoomlink}')
            
    except (FileNotFoundError, AssertionError) as e:
        print('ERROR: Need to create a file zoomlink.txt containing just the zoom link')
        raise e
        
    template = re.sub('{zoomlink}', zoomlink, template)
            
    return template

def send_email(subject, body):
    """
    Sends an email to the list with the given subject and body
    """
    ## TODO: add cc as an optional argument
    ## TODO: add alternate template for guest speakers

    # Sender and receiver details
    snabela = '@'
    from_address = 'atsang' + snabela + 'g.harvard.edu'

    to_address = 'arthurltsang' + snabela + 'gmail.com'
    # to_address = 'cosmo-journal-club' + snabela + 'lists.fas.harvard.edu'

    print(f'About to email {to_address}')
    print('If this is correct, please confirm by answering the following prompt')
    print('(You can set up an App ID at https://myaccount.google.com/u/1/apppasswords )')
    password = getpass.getpass(f'App ID for {from_address}: ')

    # Setting up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # Adding the body to the email
    msg.attach(MIMEText(body, 'html '))

    # Create SMTP session for sending the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your SMTP server host and port
        server.starttls()  # Secure the connection
        server.login(from_address, password)  # Authentication
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(from_address, to_address, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def send_email_using_template(dico):
    """
    Sends an email using our template (see `template_fill`)
    """
    subject_template = 'Harvard D-F-K Cosmology Journal Club: {date}, 5-6PM Eastern'
    subject = re.sub('{date}', dico['date'], subject_template)

    body = template_fill(dico)

    print(dico)

    send_email(subject, body)

def get_today_dico():
    """Gets the dictionary of info for the next speaker in the future (based on
    today's date). Note this function assumes a certain date format in the csv,
    like "Tuesday, February 27, 2024".
    """
    
    today = datetime.date.today()
    csv_date_format = "%A, %B %d, %Y"

    with open('speakers.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            speaker_date = datetime.datetime.strptime(row['date'], csv_date_format).date()
            if speaker_date < today:
                continue
            else:
                return row

    raise ValueError('All dates in speaker csv are in the past')

if __name__ == '__main__':
    download_speaker_csv() # the google doc spreadsheet is the master copy
    
    today_dico = get_today_dico() # gets info for next speaker in the future

    send_email_using_template(today_dico) # sends email (if user provides password)
