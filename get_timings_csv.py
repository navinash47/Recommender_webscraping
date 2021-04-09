from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time 
import re
import csv
def find_timings(query):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    
    
    driver = webdriver.Chrome("C:\\bin\chromedriver",options=options)
    driver.get(query)
    content=driver.page_source
    soup=BeautifulSoup(content,features="lxml")
    
    
    try:
        attr=soup.find('div', attrs={'class':'section-open-hours-container'})
        list_of_days=[]
        for att in attr.findAll('tr', attrs={'class':'lo7U087hsMA__row-row'}):
            day=att.find('th', attrs={'class':'lo7U087hsMA__row-header'})
            
            timings_main=att.find('td', attrs={'class':'lo7U087hsMA__row-data'})
            timings=timings_main.find('ul', attrs={'class':'lo7U087hsMA__row-interval'})
            
            
            list_of_same_day=[]
            for tim in timings.findAll('li'):
                list_of_same_day.append(tim.text)
                
            this_dict={}   
            this_dict[day.text.replace(" ","")]=list_of_same_day
            
            list_of_days.append(this_dict)
            
            
    except:
        attr="none"
        list_of_days=[]
        list_of_days.append({'Monday':["Unknown"]})
        list_of_days.append({'Tuesday':["Unknown"]})
        list_of_days.append({'Wednesday':["Unknown"]})
        list_of_days.append({'Thursday':["Unknown"]})
        list_of_days.append({'Friday':["Unknown"]})
        list_of_days.append({'Saturday':["Unknown"]})
        list_of_days.append({'Sunday':["Unknown"]})
    print(list_of_days)
    return list_of_days
    
    
     
        