#/usr/bin/env python
#################################################################################################################
import os ; import sys ; from dateutil.relativedelta import relativedelta
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

        htm = urll2.urlopen(web).read() ;  cont=bs4.BeautifulSoup(htm,"html.parser") ; #cont=cont.get_text() ; 
        #cont1=re.sub('<[^<]+?>','',htm) ;

        #cont=re.sub('Table Display','',cont) ; cont=re.sub('Table Name: Weather','',cont) ; cont.encode('UTF8'); 
        #data=cont.split('\n') ; data=np.array(filter(None,([x.encode('UTF8') for x in data])))

        cont_header=[each.contents[0] for each in cont.findAll(name='th')] ; cont_data=[each.contents[0] for each in cont.findAll(name='td')]
        data1=cont_header+cont_data ; data=np.array([x.encode('UTF8') for x in data1])
       
        return data

   def getData(url):
        data_1=readUrl(url)    
        if data_1.shape[0]==384:    
             print "Data download complete: "
             data=data_1.reshape(16,24); #reqData_1=np.concatenate([np.vstack(data[0,:]).T,data[-16:-1,:]],axis=0)
        else:
             print "Data downloded improper: Download Again"
             getData(url_1)
        return data    

   reqData=getData(url_1)        
   return reqData

    
def writeFile(reqData,path):   
    _date=(dt.datetime.strptime(reqData[1,0],'%Y-%m-%d %H:%M:%S.%f')).strftime('%Y-%m-%d_%H-%M-%S') + '_'+\
            (dt.datetime.strptime(reqData[-1,0],'%Y-%m-%d %H:%M:%S.%f')).strftime('%Y-%m-%d_%H-%M-%S')   ;
    
    date=(dt.datetime.strptime(reqData[1,0],'%Y-%m-%d %H:%M:%S.%f')).strftime('%Y-%m-%d')
    outpath=path+date
    if not os.path.exists(outpath):
         os.makedirs(outpath)
    fileNme=outpath+'/beamDown_'+_date+'.csv' ; np.savetxt(fileNme,reqData,fmt='%s',delimiter=',')

def main():
    
    mainpath='/home/Data/masdar_station_data/' ; datapath=mainpath+'metStation/beamdownStation/' ;

    date_2=dt.datetime.now().strftime('%Y-%m-%d%H:%M') ; date_1=(dt.datetime.strptime(date_2,'%Y-%m-%d%H:%M')-relativedelta(minutes=15)).strftime('%Y-%m-%d%H:%M')
    p_2=date_2[0:10]+'T'+date_2[10:]+':00'    ; p_1=date_1[0:10]+'T'+date_1[10:]+':00'
    
    url='http://10.104.2.31/?command=dataquery&uri=dl:weather&format=html&mode=date-range&p1='+p_1+'&p2='+p_2 ; 
    data=fetchData(url) ; writeFile(data,datapath)

if __name__=='__main__':
    main()
    #quit()



