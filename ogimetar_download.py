import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--start", dest = "start", help="From what date script should start. example: 01/2016")
parser.add_argument("-e", "--end", dest = "end", help="To what date script should work. example: 05/2016")
parser.add_argument("-i", "--ind",dest ="station", default=12560, help="Station ind number. Default is Katowice(12560)",type=int)
parser.add_argument("-f", "--file",dest = "file", help="To what file script should write")

args = parser.parse_args()

print args
import urllib, urllib.request, calendar, xlwt
from tqdm import *
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime
from bs4 import BeautifulSoup
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Arkusz 1")
def month_iter(start_month, start_year, end_month, end_year):
    start = datetime(start_year, start_month, 1)
    end = datetime(end_year, end_month, 1)
    return ((d.month, d.year) for d in rrule(MONTHLY, dtstart=start, until=end))
date1month, date1year = args.start.split("/")
date2month, date2year = args.end.split("/")
written = 0
iterations = 0

for m in month_iter(int(date1month), int(date1year), int(date2month), int(date2year)):
    daysof = calendar.monthrange(m[1], m[0])[1]
    for day in range(1, daysof+1):
        iterations = iterations +1
pbar=tqdm(total=iterations)
for m in month_iter(int(date1month), int(date1year), int(date2month), int(date2year)):
    daysof = calendar.monthrange(m[1], m[0])[1]
    for day in range(1, daysof+1):
        with urllib.request.urlopen("http://www.ogimet.com/cgi-bin/gsynres?ind="+str(args.station)+"&lang=en&decoded=yes&ndays=1&ano="+str(m[1])+"&mes="+str(m[0])+"&day="+str(day)+"&hora=23") as response:
            html = response.read()
        soup = BeautifulSoup(html, 'lxml')
        tablica = soup.find('table', attrs={'bgcolor':'#d0d0d0'})
        try:
            for tr in range(0,len(tablica.findAll('tr'))-2):
                for td in range(0,18):
                    try:
                        sheet1.write(tr+written, td, tablica.findAll('tr')[tr+1].findAll('td')[td].get_text())
                    except:
                        pass
        except:
            pass
        written = written +24
        pbar.update(1)
book.save(args.file)