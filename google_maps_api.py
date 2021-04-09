# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:29:57 2020

@author: navin
"""
import csv
from bs4 import BeautifulSoup
import os 
import requests
import math
import pandas as pd
import datetime
import pytz
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def url_requests_handler(url):
#    headers={'content-type':'application/json',
#            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0'}
    #^^^^ no need to use headers since this is official API
    while 1:
        #API checking while loop
        while 1:
            #internet checking while loop
            try:
                response = requests.get(url=url, timeout=10).json()
                break #if internet works
            except Exception as e:
                print(e)
                print(url)
            print(bcolors.FAIL+"Couldn't fetch in 10 seconds. CHECK THE INTERNET."+bcolors.ENDC)
            print("Will wait for a minute and retry. Press Ctrl+C to Skip waiting.")
            try:
                time.sleep(60)
            except KeyboardInterrupt: #if ctrl+C is pressed
                print("Keyboard Interrupt!!")
                print("Skipping Sleep")
            
        if('error_message' not in response.keys()):
            return response 
            #returns only if there is no error from maps API.
        else:
            key_words=['exceeded','request','quota','API'] # handles daily request quota.
            if all(x in response['error_message'] for x in key_words):
                print(bcolors.WARNING+response['error_message']+bcolors.ENDC)
                print("Looks like requests quota excided. Will Wait for a day.")
                #makes program wait till 2 am (not 12 am) at Mountain View campus of Google
                wait_for_12am_google() 
            else:
                print(bcolors.FAIL+response['error_message']+bcolors.ENDC)
                input("After fixing this problem, press Enter to continue...") 
def wait_for_12am_google():
    time_zone = pytz.timezone("America/Los_Angeles")
    #time in Los Angeles
    time_now = datetime.datetime.now(time_zone) 
    #we will use this to get next day's date
    future_time = time_now + datetime.timedelta(days=1) 
    sleep_till=datetime.datetime(future_time.year,future_time.month,future_time.day,2) #2---> 2am
    #for subtracting, sleep_till and time_now, datatype should be same
    sleep_till=time_zone.localize(sleep_till) 
    time_diff=sleep_till-time_now
    print("Waiting till 2 am in Mountain View.",time_diff.seconds,"s. Press Ctrl+C to Skip waiting.")
    try:
        time.sleep(time_diff.seconds)
        print("Exiting Sleep")
    except KeyboardInterrupt: 
        #if ctrl+C is pressed
        print("Keyboard Interrupt!!")
        print("Skipping Sleep")