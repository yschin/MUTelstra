from ptv import *
from victraffic import *
from weather import *
from ASX import *
from GuardianHTMLParser import *
from twendrHTMLParser import *
import sqlite3
 
conn = sqlite3.connect('environment.db')
conn.text_factory = str
cursor = conn.cursor()

# remove previous data
cursor.execute("DELETE FROM GuardianNews")
cursor.execute("DELETE FROM VicTraffic")
cursor.execute("DELETE FROM ASX")
cursor.execute("DELETE FROM ptv")
cursor.execute("DELETE FROM weather")
cursor.execute("DELETE FROM TwitterTrend")

# dictionary output of victraffic
VicTraffic_list = []
for items in dictofdicts:
    VicTraffic_list.append((dictofdicts[items]['Type'],dictofdicts[items]['Location'],dictofdicts[items]['Area'],dictofdicts[items]['From'],dictofdicts[items]['To'],dictofdicts[items]['Near'],dictofdicts[items]['Info1'],dictofdicts[items]['Info2'],dictofdicts[items]['Info3'],dictofdicts[items]['Started'],dictofdicts[items]['Updated']))

# dictionary output of ASX
ASX_list = []
for items in ASXdict:
    ASX_list.append((ASXdict[items]['name'],ASXdict[items]['price'],ASXdict[items]['detprice']))   

# dictionary output of ptv
ptv_list = []
for keys in data_d:
    if keys == 'MTRAM':
        ptv_list.append((keys,str(data_d[keys]['routeDisruption']).strip('{[]}'),data_d[keys]['time']['type'],str(data_d[keys]['time']['start']).strip('()'),str(data_d[keys]['time']['end']).strip('()')))
    if keys == 'MBUS':
        ptv_list.append((keys,str(data_d[keys]['routes']).strip('[]'),data_d[keys]['disruption_type'],str(data_d[keys]['time']['start']).strip('()'),data_d[keys]['time']['type']))
    if keys == 'MTRAIN' :
        if 'end' in data_d[keys]['dates']:
            ptv_list.append((keys,str(data_d[keys]['lines']).strip('[]'),data_d[keys]['dates']['type'],str(data_d[keys]['dates']['start']).strip('()'),str(data_d[keys]['dates']['end']).strip('()')))
        else:
            ptv_list.append((keys,str(data_d[keys]['lines']).strip('[]'),data_d[keys]['dates']['type'],str(data_d[keys]['dates']['start']).strip('()'),''))       

# dictionary output of weather
weather_list = []
for keys in weather_d:
    weather_list.append((keys,weather_d[keys]['Max Temp'],weather_d[keys]['Min Temp'],weather_d[keys]['Forecast']))

# dictionary output of guardianHTMLParser
news_list = []
for items in newsdict:
    news_list.append((str(newsdict[items]['title']),str(newsdict[items]['storyURL']),str(newsdict[items]['subtitle']),str(newsdict[items]['URL'])))

# dictionary output for twendr
trend_list = []
for trends in trend_result[0]['trends']:
        trend_list.append((str(trends['name']),str(trends['query']),str(trends['url']),str(trends['promoted_content']),str(trends['events'])))
    

#insert all data into database
cursor.executemany("INSERT INTO GuardianNews VALUES (?,?,?,?)",news_list)
cursor.executemany("INSERT INTO VicTraffic VALUES (?,?,?,?,?,?,?,?,?,?,?)",VicTraffic_list)
cursor.executemany("INSERT INTO ASX VALUES (?,?,?)",ASX_list)
cursor.executemany("INSERT INTO ptv VALUES (?,?,?,?,?)",ptv_list)    
cursor.executemany("INSERT INTO weather VALUES (?,?,?,?)",weather_list)
cursor.executemany("INSERT INTO TwitterTrend VALUES (?,?,?,?,?)",trend_list)
conn.commit()
conn.close()

