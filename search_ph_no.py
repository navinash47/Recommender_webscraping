# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 20:05:23 2020

@author: navin
"""


import pandas as pd
from googlesearch import search
import re
import sqlite3
from add_department_column import url_request_website_handler
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time 
import re
import csv



  
def search_phone_no_googlemaps(csv_file):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("C:\\bin\chromedriver",options=options)
    
    df= pd.read_csv(csv_file, sep=",")
    df['phone_number']=''
    ph_nos=[]
    for index, row in df.iterrows():
        print("Hospital "+str(index)+" : "+str(row['name']))
        query="https://www.google.com/maps/search/?api=1&query="+str(row['lat'])+","+str(row['long'])+"&query_place_id="+str(row['place_id'])
        driver.get(query)
        content=driver.page_source
        soup=BeautifulSoup(content,features="lxml")
        
        attr=soup.find('button', attrs={'class':'ugiz4pqJLAG__button','data-tooltip':'Copy phone number'})
        if(attr!=None):
            ph_no=attr.find('div',attrs={'class':'ugiz4pqJLAG__primary-text'})
            print(ph_no.text)
            ph_nos.append(ph_no.text)
        else:
            ph_nos.append("nan")
        
            
    df['phone_number']=ph_nos        
    driver.close()
    return df

def search_phone_no_web(csvfile):
       
    df = pd.read_csv(filepath_or_buffer=csvfile, delimiter=",")
    
    # making new column
    if 'phone number' not in df.columns:
        df['phone number']=''
    
    hosp_num=1
    for index,row in df.iterrows():
        print("HOSP Num:",hosp_num," of ",str(len(df))," Name:",row['name'])
        hosp_num=hosp_num+1
    
        if row['phone number']!='':
            print("Number already exists. Skipping.")
            print(row['phone number'])
            continue

        if row['vicinity']!=None:
           vicinity=str(row['vicinity'])
        else:
            vicinity=''
        
        query = str(row['name']) + " " + vicinity + ' phone number'
        print("----"+query+"----")
        d = set()
    
        try:
            url_request_website_handler('https://www.google.com') #check for internet
            for j in search(query,num=5,start=0, stop=5, pause=1):
                try:
                    link = str(j)
                    if '.pdf' in link:
                        print("PDF file. Skipping")
                        continue
                    f=url_request_website_handler(link)
                    myfile = f.text
                    # regex format for indian phone numbers
                    regex_string=r'^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$'
                    for i in re.finditer(regex_string,myfile,re.MULTILINE): 
                        d.add(i.group())

                except Exception as e:
                    print('Fetch Error')
                    print(e)
                
            df['phone number'][index] = ', '.join(d)
            print("Found: "+', '.join(d))
            
        except Exception as e:
            raise e
    
    return df