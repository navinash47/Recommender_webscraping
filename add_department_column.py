# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:32:02 2020

@author: navin
"""

import pandas as pd
import requests
import time
import csv
import re
import os
from bs4 import BeautifulSoup
from Filter import df_cleaner


def connected_to_internet(url='https://www.google.com/', timeout=5):
    # used for checking internet connection
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
    return False

def url_request_website_handler(url):
        # If the program fails to connect to the Internet, it will wait for a minute and retries
    headers={'content-type':'application/json',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}
    while 1:
        try:
            response = requests.get(url=url, headers=headers,timeout=120)
            return response
        except Exception as e:
            # print(e)
            if connected_to_internet():
                return ' '
      
        print("Will wait for a minute and retry. Press Ctrl+C to Skip waiting.")
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Keyboard Interrupt!!")
            print("Skipping Sleep")

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
    


def fetch_dept(final_csv):

    df= pd.read_csv(filepath_or_buffer=final_csv, delimiter=",")
    df=df_cleaner(df)
    if 'Dept' in df.columns:
        df=df.drop(columns='Dept')
    # reading list of all departments
    with open('dept.csv') as f:
        reader = csv.reader(f)
        your_list = list(reader)    
    
    #creating a column
    df['Dept']=""
    department=[]
    hosp_num=0
    for index,row in df.iterrows():
        #for every hospital
        
        if row['vicinity']!=None:
            vicinity=str(row['vicinity'])
        else:
            vicinity=''
        query = str(row['name']) + " " + vicinity + ' department'
        te=''
        d = set()
        # if(index==1):break
        hosp_num=hosp_num+1
        try:
            url_request_website_handler('https://www.google.com') #check for internet before searching
            # 'search' is from the google search library
            print("HOSTPITAL NUMBER ----",hosp_num," of ",str(len(df))," Name:",row['name'])
            i=-1
            for j in search(query,num=5,start=0, stop=5, pause=0.01):
                try:
                    # j itself is the link in search results
                    i=i+1
                    te=""
                    
                    print("Website "+str(i+1)+" : "+j)
                    link = str(j)
                    if '.pdf' in link:
                        print("PDF file. Skipping")
                        continue
                    
                    # elif "justdial" in link:
                    #     continue
                    f=url_request_website_handler(link)
                    myfile = f.text
                    for dept in your_list:
                        # using regex
                        searchObj = re.search( dept[0], myfile, re.M|re.I)
                        if searchObj: #if searchObj is not null
                            d.add(dept[0])
                    
                except Exception as e:
                    print()
                    # print('Fetch Error')
                    # print(e)
            
                for obj in list(d):
                    te = obj +','+ te
            # putting the dataframe
            df.loc[index,"Dept"]=str(te)
            print(df.loc[index,"Dept"])
            print("--------------------------------------------------------------")
        except Exception as e:
            raise e
   
   
    return df



