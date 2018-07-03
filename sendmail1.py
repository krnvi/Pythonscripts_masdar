#!/usr/bin/python

import os ; import sys ; import smtplib ; import mimetypes ;
from smtplib import SMTP
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart ;
from email import encoders
from email.message import Message ;
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


_from     =   "radiometer.monitor@gmail.com" ;
_to       =   str(sys.argv[1])                                #"vkvalappil@masdar.ac.ae" ;
_sub      =   "Radiometer : Status"
_content  =   str(sys.argv[2])                                #"Files Didn't updated for last hour: Please check"
_username =   'radiometer.monitor' ;
_password =   'radiometer@123'
_smtp         = "smtp.gmail.com:587" ;
_text_subtype = "plain"


mail=MIMEMultipart('alternative')
mail["Subject"]  =  _sub
mail["From"]     =  _from
mail["To"]       =  _to
mail.attach(MIMEText(_content, _text_subtype ))

try:
      smtpObj = SMTP(_smtp)
      #Identify yourself to GMAIL ESMTP server.
      smtpObj.ehlo()
      #Put SMTP connection in TLS mode and call ehlo again.
      smtpObj.starttls()
      smtpObj.ehlo()
      #Login to service
      smtpObj.login(user=_username, password=_password)
      #Send email
      smtpObj.sendmail(_from, _to, mail.as_string())
      #close connection and session.
      smtpObj.quit()
except SMTPException as error:
      print "Error: unable to send email :  {err}".format(err=error)

