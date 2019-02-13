'''
Python email Sender, with attachments

This code can automatically send emails from your address to any given address.
It can also attach files to the email.

The primary purpose of this script is to send an email to a friend with an
attached music file. Using .bat files and task scheduler, a daily email can be
sent to your friend without any intervention required on your part.
You will need to replace my email and the dummied out password for your email
and password for the code to work.
Currently only works out of the box for gmail addresses.
[Your computer does need to be on and connected to the internet for this to work]
[But this code could easily run on an always on raspberry pi, or an Amazon
server if need be]

###
Code Written by:
Kyle Shepherd
KyleAnthonyShepherd@gmail.com
Aug 8, 2018
###
'''

#### Import Block ####
# the import block imports needed modules, and spits out a json file with
# version numbers so the code can be repeatable
file = open("ModuleVersions.json", 'w')
modules = {}

import os

import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import smtplib

import random

import sys
modules['Python'] = dict([('version', sys.version_info)])

import json
modules['json'] = dict([('version', json.__version__)])

json.dump(modules, file, indent=4, sort_keys=True)
file.close()
#### END Import Block ####

def EmailBody(fromaddr,toaddr,subject,body):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg

def EmailAttachment(msg,file):
    part = MIMEApplication(open(file, "rb").read())
    part.add_header('Content-Disposition', 'attachment',filename=file)
    msg.attach(part)
    return msg

def EmailSend(msg,fromaddr,password,toaddr):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

if __name__ == "__main__":
    files=os.listdir('Music')
    R=random.randrange(0,len(files))
    file='Music/'+files[R]

    fromaddr = "example@gmail.com"
    toaddr = "example@gmail.com"
    subject = "Daily Music Delivery"
    body = "Hey Friend! \n \nHere is awesome music for you"
    msg=EmailBody(fromaddr,toaddr,subject,body)
    file='Music/'+files[R]
    msg=EmailAttachment(msg,file)
    password='DummiedOut'
    EmailSend(msg,fromaddr,password,toaddr)
