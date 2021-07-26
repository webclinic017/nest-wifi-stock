import requests 
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText

isArmed = True

def sendEmail(messages):
    msg = MIMEMultipart()
    msg['From'] = 'neststockfinder@gmail.com'
    msg['To'] = 'alphapranav.k@gmail.com'
    msg['Subject'] = 'Nest Wifi refurbished is in stock'
    message = messages
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    with open("credentials.txt") as creds:
            for line in creds:
                mailserver.login("neststockfinder@gmail.com", line)
                break

    mailserver.sendmail('neststockfinder@gmail.com','alphapranav.k@gmail.com',msg.as_string())

    mailserver.quit()

sendEmail('Hello, the server for email alerts for Nest WiFi refurbished is up. This system is made by Pranav.')

while True:
    try:
        link = "https://store.google.com/us/config/refurbished_nest_wifi_2points?hl=en-US"
        r = requests.get(link) 
        soup = BeautifulSoup(r.content, "html5lib")
        text = soup.find_all(
            "div", 
            attrs = {
                "class":"l5zTP ulDiod", 
                "data-test":"status"
            }
        )

        if (text[0].getText() != "Out of stock"):
            if isArmed:
                sendEmail('There is stock for the refurbished Nest WiFi. Look at this link. {}'.format(link))
                isArmed = False
            print("Query complete: In Stock")
        else:
            isArmed = True
            print("Query complete: Out of Stock")

        time.sleep(10)
        
    except:
        pass
    
