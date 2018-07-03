#!/usr/bin/python

import os ; import sys ; import numpy as np ; import datetime ; import urllib2

########################################################################################################################
main='/home/vkvalappil/Data/' ; output=main+'/metarData/' ; scripts=main+'/workspace/pythonScripts/'

date=str(sys.argv[1]) ; startts = datetime.datetime.strptime(date,'%Y%m%d')
#endts = datetime.datetime(2017, 06, 1)

lstFile=scripts+'metar_surf.csv'
points=np.genfromtxt(lstFile,delimiter=',',dtype='S')

if not os.path.exists(output+date[0:4]+'/'+date[0:6]) :
    os.makedirs(output+date[0:4]+'/'+date[0:6])


for code, loc in points:

    url="https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"

    url+="station=%s&data=all&" %(code)


    url+= startts.strftime('year1=%Y&month1=%m&day1=%d&')
    url+= startts.strftime('year2=%Y&month2=%m&day2=%d&')
    url+= "tz=Etc%2FUTC&format=comma&latlon=yes&direct=no&report_type=1&report_type=2"


    data = urllib2.urlopen(url) ; data=data.read() ; data=data.split('\n',5)[-1]

    outfile = '%s%s/%s/%s_%s.csv' % (output,date[0:4],date[0:6],loc, startts.strftime("%Y%m%d"))

    out = open(outfile, 'w')
    out.write(data)
    out.close()


quit()
