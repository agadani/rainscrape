#!/usr/bin/python
import urllib
import sys
import datetime
from time import sleep

def get_temp(line,tempstring="Average Temp:"):
  # get a temp out of a farmer formatted table
  return float(line.split(tempstring)[1].split('<td>')[1].split('F')[0])

def get_precip(line):
  #Precipitation Amount:&nbsp;</td><td>0 Inches<
  tempstring = 'Precipitation Amount:'
  if 'Inches' in line:
    return float(line.split(tempstring)[1].split('<td>')[1].split('Inches')[0])
  else:
    return 0.0

def rain_stats(date,source='farmers',years=50,min_year=1900):
  # date should be a tuple of (mm,dd)
  today = datetime.datetime.now()
  rain_list = []
  rainfall_amounts = []
  temps = []
  if today.month > date[0] or (today.month == date[0] and today.day > date[1]): 
    current_year = today.year - 1
  else:
    current_year = today.year
  
  
  if source == 'farmers':
    min_year = 1945
    url_head = 'http://www.farmersalmanac.com/weather-history/17050/'
  start_year = max(min_year,current_year-years)

  month = str(date[0])
  if len(month) == 1:
    month = '0'+month
  day = str(date[1])
  if len(day) == 1:
    day = '0'+day

    '''
    Farmer's table format:
      High Temp:  66.9F
      Low Temp:   55.9F
      Average Temp:   61.5F
      Dewpoint:   49.8F
      Wind Speed:   5.1 Knots
      Precipitation Amount:   n/a
      Snow Depth:   n/a
      Observations:   Rain/Drizzle
    '''

  for year in range(start_year,current_year+1):
    my_url = url_head+str(year)+'/'+month+'/'+day
    page_data = open(urllib.urlretrieve(my_url)[0],'r')
    rain = False
    for line in page_data:
      if "Rain" in line and "Observation" in line:
        rain_list.append(1)
        rainfall_amounts.append(get_precip(line))
        rain = True
      if 'Average Temp' in line:
        temps.append(get_temp(line))
    # Something to slow this down so people don't get annoyed:
    if rain == False:
      rain_list.append(0)
    sleep(2.5)
    print '*',
  
  return rain_list,temps,rainfall_amounts

def clean_date(date):
  if '-' in date:
    m,d = map(int,date.split('-'))
  elif '/' in date:
    m,d = map(int,date.split('/'))
  else:
    print "Bad date format:",date
    sys.exit(1)

  return m,d 

def avg(l):
  return sum(l)/float(len(l))

if __name__ == '__main__':
  # Usage:
  # ./rain_scrape.py 05-30 --years 10
  years = 50
  date = sys.argv[1]
  for i,arg in enumerate(sys.argv):
    if arg=='--years':
      years = int(sys.argv[i+1])

  m,d = clean_date(date)

  rain_stats,temp_stats,rainfall_amounts = rain_stats((m,d),years=years)
  print
  print "Based on the last",years,"years, there is a","%.2f"%(avg(rain_stats)*100),'% risk of rain or drizzle on',m,'-',d,'2015,\n and the average temperature will be',"%.2f"%avg(temp_stats),'F.'
  print "If it does rain, expect","%.4f"%avg(rainfall_amounts),'inches of rain.'


      
