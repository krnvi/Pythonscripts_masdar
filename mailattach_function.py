

def sendmail(file_taf,email_list) :
           from smtplib import SMTP ; from smtplib import SMTPException ; 
           from email.mime.multipart import MIMEMultipart ; from email.mime.text import MIMEText      

           _from         =   "alerts.cesamlab@gmail.com" ;
           _to           =   email_list;
           _sub          =   "TAF (WRF CESAM LAB)  "
           _attach       =   file_taf
           #_content      =   "WRF TAF DATA"
           _username     =   'alerts.cesamlab' ;
           _password     =   'alert@123'
           _smtp         = "smtp.gmail.com:587" ;
           #_text_subtype = "plain"

           mail=MIMEMultipart()
           mail["Subject"]  =  _sub
           mail["From"]     =  _from
           mail["To"]       =  ','.join(_to)
           #body = MIMEMultipart('alternative')
           #body.attach(MIMEText(_content, _text_subtype ))
           mail.attach(MIMEText(file(_attach).read()))
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