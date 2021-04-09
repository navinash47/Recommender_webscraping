# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 12:58:00 2020

@author: navin
"""
import pandas as pd
import csv
import requests
import time
from google_maps_api import url_requests_handler

def df_cleaner(df): #dropping any unncesary or useless columns
    if 'Unnamed: 0' in df.columns:
        df=df.drop(columns='Unnamed: 0')

    # the below two are not necessary. These were kept to make the 1st type of db file I made compatible
    if 'opening hours' in df.columns:
        df=df.drop(columns='opening hours')
    if 'Website' in df.columns:
        df=df.drop(columns='Website')
    if 'address' in df.columns:
        df=df.rename(columns={'address':'vicinity'})
    
    return df

def merge(final_csv):
    global dfs
    df= pd.read_csv(filepath_or_buffer=final_csv, delimiter=",")
    dfs=[]
    
    dfs.append(df_cleaner(df))

    # concatenating all dataframes
    final_df = pd.DataFrame(dfs[0])
    for i in range(1,len(dfs)):
        final_df=final_df.append(dfs[i])

    final_df=final_df.drop_duplicates()
    final_df=final_df.drop_duplicates(subset=['place_id'])

    #FILTERING

    #removing bad entries
    doesnt_contain=["Shop","Store","Homeopathy","Clinic","Dental","Ayurvedic","Animal","veterinary"]
    final_df=final_df[~final_df['name'].str.contains('|'.join(doesnt_contain),case=False)]
    
    #Keeping only hospitals
    does_contain=["Hospital","Hospitals","Health Centre"]
    final_df=final_df[final_df['name'].str.contains('|'.join(does_contain),case=False)]
    final_df=final_df.reset_index()
    final_df=final_df.drop(columns='index')
    
#    cols = ['name', 'phone number', 'lat', 'long', 'rating', 'vicinity','Dept','place_id']
#    final_df=final_df[cols]
    

    return final_df


