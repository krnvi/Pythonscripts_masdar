
import os ; import sys ; import smtplib ; import mimetypes ;
from smtplib import SMTP
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart ;
from email import encoders
from email.message import Message ;
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


_from     =   "radiometer.monitor@gmail.com" ;
_to       =   sys.argv[1] ;
_username =   "radiometer.monitor@gmail.com" ;
_password =   'radiometer@123'

_smtp         = "smtp.gmail.com:587" ;
_text_subtype = "plain"

message = """From: <radiometer.monitor@gmail.com>
MIME-Version: 1.0
Content-type: text/html
To: <vkvalappil@masdar.ac.ae>
Subject: Radiometer : Status

<br>
Files Didn't updated for last hour: Please check<br>
<br>
"""
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
      smtpObj.sendmail(_from,_to, message)
      #close connection and session.
      smtpObj.quit()
except SMTPException as error:
      print "Error: unable to send email :  {err}".format(err=error)




