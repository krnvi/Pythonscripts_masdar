#/usr/bin/env python
#################################################################################################################
import os ; import sys ; 
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
   print "Couldn't find urllib2, Please install"
   quit()
try:    
    import re ;
except:
   print "Couldn't find urllib2, Please install"
   quit()    
    
try:    
   import bs4 ; 
except:
   print "Couldn't find urllib2, Please install"
   quit()

##################################################################################################################

def fetchData(url_1):
   def readUrl(url):   
        web=urll2.Request(url) ;

        htm = urll2.urlopen(web).read() ;  cont=bs4.BeautifulSoup(htm) ; cont=cont.get_text() ; 
        #cont=re.sub('<[^<]+?>','',htm) ;

        cont=re.sub('Table Display','',cont) ; cont=re.sub('Table Name: Weather','',cont) ; 
        data=cont.split('\n') ; data=np.array(filter(None,([x.encode('UTF8') for x in data])))
        return data

   def getData(url):
       
       data_1=readUrl(url)    
       if data_1.shape[0]==459:    
             print "Data download complete: "
             data=data_1.reshape(17,27); reqData_1=np.concatenate([np.vstack(data[0,:]).T,data[-16:-1,:]],axis=0)  
       else:
             print "Data downloded improper: Download Again"
             getData(url)
       return reqData_1    
       
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

def main():
    
    mainpath='/home/Data/masdar_station_data/' ; datapath=mainpath+'metStation/filedStation/' ;
    url='http://10.104.21.30/?command=TableDisplay&table=Weather&records=16' ; 
    
    data=fetchData(url) ; writeFile(data,datapath)

if __name__=='__main__':
    main()
    #quit()



