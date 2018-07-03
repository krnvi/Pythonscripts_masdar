#!usr/bin/python
################################################################################################################
import os ;  from dateutil.relativedelta import relativedelta
try:
   import numpy as np ;
except:
   print "Couldn't find numpy, Please install "
   quit()
try:
   import urllib2 as urll2 ;
except:
   print "Couldn't find urllib2, Please install"
   quit()
try :
    import datetime as dt ;
except:
   print "Couldn't find datetime, Please install"
   quit()
try:
   from bs4 import BeautifulSoup ;
except:
   print "Couldn't find bs4, Please install"
   quit()

##################################################################################################################

def fetchData(url_1):
   def readUrl(url):
        web=urll2.Request(url) ;

        htm = urll2.urlopen(web).read() ;  cont=BeautifulSoup(htm,"html.parser") ; #cont=cont.get_text() ; 
        #cont=re.sub('<[^<]+?>','',htm) ;

        #cont=re.sub('Table Display','',cont) ; cont=re.sub('Table Name: Weather','',cont) ; 
        #data=cont.split('\n') ; data=np.array(filter(None,([x.encode('UTF8') for x in data])))
        cont_header=[each.contents[0] for each in cont.findAll(name='th')] ; cont_data=[each.contents[0] for each in cont.findAll(name='td')]
        data1=cont_header+cont_data ; data=np.array([x.encode('UTF8') for x in data1])

        return data

   def getData(url):

       data_1=readUrl(url)
       if data_1.shape[0]==432:
             print "Data download complete: "
             data=data_1.reshape(16,27); #reqData_1=np.concatenate([np.vstack(data[0,:]).T,data[-16:-1,:]],axis=0)  
       else:
             print "Data downloded improper: Download Again"
             getData(url)
       return data

   reqData=getData(url_1)

   return reqData

def writeFile(reqData,path):
    _date=(dt.datetime.strptime(reqData[1,0],'%Y-%m-%d %H:%M:%S.%f')).strftime('%Y-%m-%d_%H-%M-%S') + '_'+\
            (dt.datetime.strptime(reqData[-1,0],'%Y-%m-%d %H:%M:%S.%f')).strftime('%Y-%m-%d_%H-%M-%S') ;

    date=(dt.datetime.strptime(reqData[1,0],'%Y-%m-%d %H:%M:%S.%f')).strftime('%Y-%m-%d')
    outpath=path+date
    if not os.path.exists(outpath):
         os.makedirs(outpath)
    fileNme=outpath+'/MIFS_'+_date+'.csv' ; np.savetxt(fileNme,reqData,fmt='%s',delimiter=',')


def sendAlert(reqData,email_id):
    
    def sendmail(message,email_list) :
           from smtplib import SMTP ; from smtplib import SMTPException ; 
           from email.mime.multipart import MIMEMultipart ; from email.mime.text import MIMEText      

           _from         =   "fog@masdar.ac.ae" ;
           _to           =   email_list;
           _sub          =   "Tdep Alert (CESAM LAB)  "
           _username     =   'fog' ;
           _password     =   'P@ssword322'
           _smtp         =   "mail.masdar.ac.ae:587" ;
           #_text_subtype = "plain"

           mail=MIMEMultipart()
           mail["Subject"]  =  _sub
           mail["From"]     =  _from
           mail["To"]       =  ','.join(_to)
           #body = MIMEMultipart('alternative')
           #body.attach(MIMEText(_content, _text_subtype ))
           mail.attach(MIMEText(message))
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
               print "Using Gmail : Error: unable to send email :  {err}".format(err=error)   
               try:
                   _from         =   "fog.masdar@gmail.com" ;
                   _to           =   email_list;
                   _sub          =   "Tdep Alert (CESAM LAB)  "
                    
                   #_content      =   "WRF TAF DATA"
                   _username     =   'fog.masdar' ;
                   _password     =   'fog@masdar123'
                   _smtp         =   "smtp.gmail.com:587" ;
                   #_text_subtype = "plain"
                   
                   mail=MIMEMultipart()
                   mail["Subject"]  =  _sub
                   mail["From"]     =  _from
                   mail["To"]       =  ','.join(_to)
                   mail.attach(MIMEText(message))
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

               except:
			  print 'error'
           return "Error";    
    
    def mail_body(time_ocs,td,rh) :

        alert_body="""
                        This email is automatically generated by Masdar's fog detection and forecast system. 
    
                        This warning is to advise that Temperature depression has reached less than 3 degree for the below shown timestamp. 
                        
                        Time : {} 
                        RH   : {}
                        Tdep : {}

                        For comments and/or questions; please contact: 

                        Dr. Marouane Temimi, Ph.D., 
                        Associate Professor 
                        Masdar Institute of Science and Technology 
                        Email: mtemimi@masdar.ac.ae     """.format(time_ocs,rh,td)
        return alert_body    
    

    temp_10=reqData[1:,3].astype(float) ; temp_2=reqData[1:,4].astype(float)
    dtemp_10=reqData[1:,5].astype(float) ; dtemp_2=reqData[1:,6].astype(float)
    time_list=reqData[1:,0]
    rh_10=reqData[1:,7]   ; rh_2=reqData[1:,8]
 
    tdep_10=temp_10[-1]-dtemp_10[-1] ; tdep_2=temp_2[-1]-dtemp_2[-1] ; 
    tdep_10=2
    if tdep_10 < 3 :
        print "tdep_10 is less than 3"

        lastT=np.genfromtxt('/home/vkvalappil/Data/masdar_station_data/metStation/scripts/lastalertTime.csv',delimiter=',',dtype='S')[1]
        d1=dt.datetime.strptime(lastT,'%Y-%m-%d %H:%M:%S.%f') ; d2=dt.datetime.strptime(time_list[-1],'%Y-%m-%d %H:%M:%S.%f')
        diff=(d2-d1) ; days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600 # minutes = (seconds % 3600) // 60 ;  seconds = seconds % 60
        
        if hours >5 :
            print hours
            text='Last Alert Time,'+time_list[-1] ; text=text.split(',')  
            fileNme='/home/vkvalappil/Data/masdar_station_data/metStation/scripts/lastalertTime.csv'
            np.savetxt(fileNme,text,fmt='%s',delimiter=',')        
            
            alert=mail_body(time_list[-1],tdep_10,rh_10[-1])
            sendmail(alert,email_id)   
        else:
            print "Alert send with in last 5 hour: Do not send now"
        
    else :
        print "tdep greater than 3"

####################################################################################################################################################################

def main():

    mainpath='/home/vkvalappil/Data/masdar_station_data/' ; datapath=mainpath+'metStation/filedStation/' ;
    #email_id=["mtemimi@masdar.ac.ae","mjweston@masdar.ac.ae",nchaouch@masdar.ac.ae","vkvalappil@masdar.ac.ae"] 
    email_id=["vkvalappil@masdar.ac.ae"]
    
    
    date_2=dt.datetime.now().strftime('%Y-%m-%d%H:%M') ; date_1=(dt.datetime.strptime(date_2,'%Y-%m-%d%H:%M')-relativedelta(minutes=15)).strftime('%Y-%m-%d%H:%M')
    p_2=date_2[0:10]+'T'+date_2[10:]+':00'    ; p_1=date_1[0:10]+'T'+date_1[10:]+':00'

    url='http://10.104.21.30/?command=dataquery&uri=dl:weather&format=html&mode=date-range&p1='+p_1+'&p2='+p_2 ;
    #print url
    data=fetchData(url) ; writeFile(data,datapath) ; sendAlert(data,email_id)
    
if __name__=='__main__':
    main()
    quit()
