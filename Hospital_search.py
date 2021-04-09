import csv
from bs4 import BeautifulSoup
import os 
import requests
import math
import pandas as pd
import datetime
import pytz
import time
from google_maps_api import url_requests_handler
# from Filter import fetch_info
from Filter import merge
from add_department_column import fetch_dept
from search_ph_no import search_phone_no_googlemaps
from search_ph_no import search_phone_no_web


# Links=[]
# Hospitals=[] #List to store name of the Hospitals
# Ratings=[] #List to store name of ratings
# Addresses=[] #List to store name of the Adresses
# Phone_nos=[] #List to store name of ratings
# statuses=[]
# schedules=[]
# coordinates=[]

# def ParseQuery(Name):
#     parts=Name.split()
#     query=""
#     for p in parts:
#         query+=p
#         query+="+"
#     return query[:-1]

# def Allot_lists(attr,text_attr):
#     if(text_attr!=None):
#         attr.append(text_attr.text)
#     else:
#         attr.append("none")
        
# def Update_lists(attr,text_attr,index):
#     if(text_attr!=None):
#         if(attr[index]=="none"):
#             attr[index]=text_attr.text
            
# def find_timings(tempsoup):
#     heading=tempsoup.find('div',attr={'class':'cX2WmPgCkHi__summary-line'})
#     status=None
#     if(heading!=None):
#         status=heading.find('span',attr={'class':'cX2WmPgCkHi__section-info-text'})
    
#     main=tempsoup.find('div',attr={'class':'section-open-hours-container'})
#     table={}
#     if(main!=None):
#         for Eachrow in main.findAll('tr',attr={'class':'lo7U087hsMA__row-row'}):
#             day=Eachrow.find('th',attr={'class':'lo7U087hsMA__row-header'})
#             day_status=Eachrow.find('ul',attr={'class':'lo7U087hsMA__row-interval'})
#             if(day!=None and day_status!=None):
#                 table.update({day.text:day_status.text})
#             else:
#                 table.update({'none':'none'})
#     return status,table
    
# def get_data(driver,tempdriver,Hospitals,Ratings,Addresses,Phone_nos,statuses,schedules,coordinates,soup,Links):
#     index=-1
#     for a in soup.findAll('div', attrs={'class':'section-result'}):
#         index=index+1
#         name=a.find('h3', attrs={'class':'section-result-title'})
#         print("Hospital-"+ str(index+1)+" : "+name.text)
#         rating =a.find('span',attrs={'class':'cards-rating-score'})
#         Addplace=a.find('span',attrs={'class':'section-result-location'})
#         Link=ParseQuery(name.text)
        
#         Link="https://www.google.com/maps/search/?api=1&query="+Link
#         Link=Link+'+'+Addplace.text
#         Links.append(Link)
        
#         tempdriver.get(Link)
#         tempcontent = tempdriver.page_source
#         tempsoup = BeautifulSoup(tempcontent,features="lxml")
        
      
#         path=None
#         number=None  
        
#         attr=tempsoup.find('button', attrs={'class':'ugiz4pqJLAG__button','data-tooltip':'Copy address'})
#         if(attr!=None):
#             path=attr.find('div',attrs={'class':'ugiz4pqJLAG__primary-text'})
#         attr=tempsoup.find('button', attrs={'class':'ugiz4pqJLAG__button','data-tooltip':'Copy phone number'})
#         if(attr!=None):
#             number=attr.find('div',attrs={'class':'ugiz4pqJLAG__primary-text'})
            
#         status_now,schedule=find_timings(tempsoup)
        

#         # print(tempdriver.current_url)
#         result = re.search('@(.*)z', tempdriver.current_url)
#         while(result==None):
#             result = re.search('@(.*)z', tempdriver.current_url)
            
#         coordinate=[]
#         coordinate=result.group(1).split(',')
#         coordinates.append(coordinate)
        
#         Allot_lists(Hospitals,name)
#         Allot_lists(Ratings,rating)
#         Allot_lists(Addresses, path)
#         Allot_lists(Phone_nos, number)
#         Allot_lists(statuses, status_now)
#         schedules.append(schedule)
    
# # def update_data(tempdriver, Addresses, Phone_nos, statuses, schedules,Links):
    
#     for index in range(len(Links)):      
#         tempdriver.get(Links[index])
#         tempcontent = tempdriver.page_source
#         path=None
#         number=None 
#         status_now=None
#         flag=False
        
#         if(Addresses[index]!="none" and Phone_nos[index]!="none"):
#             flag=True
#             # print(tempdriver.current_url)
#             result = re.search('@(.*)z', tempdriver.current_url)
#             while(result==None):
#                  result = re.search('@(.*)z', tempdriver.current_url)
#                  tempcontent = tempdriver.page_source
        
#         tempsoup = BeautifulSoup(tempcontent,features="lxml")
        
            
#         attr=tempsoup.find('button', attrs={'class':'ugiz4pqJLAG__button','data-tooltip':'Copy address'})
#         if(attr!=None and Addresses[index]=="none"):
#             print("indexes empty:"+str(index))
#             path=attr.find('div',attrs={'class':'ugiz4pqJLAG__primary-text'})
#         attr=tempsoup.find('button', attrs={'class':'ugiz4pqJLAG__button','data-tooltip':'Copy phone number'})
#         if(attr!=None and Phone_nos[index]=="none"):
#             number=attr.find('div',attrs={'class':'ugiz4pqJLAG__primary-text'})
            
#         if(schedules[index]==None):   
#             status_now,schedule=find_timings(tempsoup)
#         if(flag):
 
               
#             Update_lists(Addresses, path,index)
#             Update_lists(Phone_nos, number,index)
#             Update_lists(statuses, status_now,index)
            
#         if(schedules[index]==None):
#             schedules[index]=schedule

# def fetch_info(apikey,final_csv):
#     df= pd.read_csv(filepath_or_buffer=final_csv, delimiter=",")
#     df=df_cleaner(df)
#     phone=[]
#     for index,row in df.iterrows():
#         print("Fetching phno for "+str(index)+" out of "+str(len(df)-1))        
#         place_id=str(row['place_id'])
#         urlx='https://maps.googleapis.com/maps/api/path/details/json?placeid='+place_id+'&fields=name,rating,formatted_address,formatted_phone_number,review,opening_hours&key='+apikey
#         responsex = url_requests_handler(urlx)        
#         try:
#             ph_no=responsex['result']['formatted_phone_number']
#         except:
#             ph_no=''  
#         phone.append(ph_no)
#         print (ph_no)
        
#         try:
#             rating=responsex['result']['rating']
#         except:
#             rating=''         
            
#         df['rating'][index]=rating
        
        
#     if 'phone_number' not in df.columns:
#         df['phone_number']=phone
#     else:
#         df=df.drop(columns='phone_number')
#         df['phone_number']=phone
#     return df

def csv_write(lat1,long1,radius,path,apikey):
    csvfile =open('hospitals_in_'+path+'.csv','a',encoding='utf-8')
    writer = csv.writer(csvfile, delimiter='$')
    
    url = 'https://maps.googleapis.com/maps/api/path/nearbysearch/json?location='+lat1+','+long1+'&radius='+radius+'&type=hospital&key='+apikey
    #url call for the API
    response = url_requests_handler(url)
    for obj in response['results']:
        # print(obj['name'])
        new_row=[]
        try:
            new_row.append(obj['name'].strip('|'))
        except:
            new_row.append("NA")
        try:
            new_row.append(obj['geometry']['location']['lat'])
        except:
            new_row.append("NA")
        try:
            new_row.append(obj['geometry']['location']['lng'])
        except:
            new_row.append("NA")
        try:
            new_row.append(obj['rating'])
        except:
            new_row.append("NA")
        try:
            new_row.append(obj['vicinity'])
        except:
            new_row.append("") #so that NA also wont be searched along with the name
        try:
            new_row.append(obj['place_id'])
        except:
            new_row.append("NA")
        try:
            new_row.append(str(obj['opening_hours']['open_now']))
        except:
            new_row.append("NA")
        writer.writerow(new_row)

    while 'next_page_token' in response:
        URL = url + '&pagetoken=' + response['next_page_token']
        print('waiting next page')
        time.sleep(1)
        response = url_requests_handler(URL)
        for obj in response['results']:
            # print(obj['name'])
            new_row=[]
            try:
                new_row.append(obj['name'].strip('|'))
            except:
                new_row.append("NA")
            try:
                new_row.append(obj['geometry']['location']['lat'])
            except:
                new_row.append("NA")
            try:
                new_row.append(obj['geometry']['location']['lng'])
            except:
                new_row.append("NA")
            try:
                new_row.append(obj['rating'])
            except:
                new_row.append("NA")
            try:
                new_row.append(obj['vicinity'])
            except:
                new_row.append("") #so that NA also wont be searched along with the name
            try:
                new_row.append(obj['place_id'])
            except:
                new_row.append("NA")
            try:
                new_row.append(str(obj['opening_hours']['open_now']))
            except:
                new_row.append("NA")

            writer.writerow(new_row)
def coordinates_path(places,apikey,coordinates):
    #making list of coodinates on the path
    place_1=places.split("__and__")[0]
    place_2=places.split("__and__")[1]
    
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place_1+'&key='+apikey)
    resp_json_payload = response.json()
    lat1 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
    long1 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])    
    
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+place_2+'&key='+apikey)
    resp_json_payload = response.json()
    lat2 = str(resp_json_payload['results'][0]['geometry']['location']['lat'])
    long2 = str(resp_json_payload['results'][0]['geometry']['location']['lng'])    
    
    lata = float(lat1)
    latb = float(lat2)
    longa = float(long1)
    longb = float(long2)
    #cdist = math.sqrt(((long2-long1)*(long2-long1))  +  ((lat2-lat1)*(lat2-lat1)))
    dlon = longb - longa
    dlat = latb - lata
    R = 6373.0 #approximate radius of earth
    a = math.sin(dlat / 2)**2 + math.cos(lata) * math.cos(latb) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c * 1000
    divs = int(distance/45000)
    
    templat=lata
    templong=longa    
    for i in range(divs):
        coordinates.append((templat,templong))
        templong=templong+(longb-longa)/(divs+1)
        templat=templat+(latb-lata)/(divs+1)
    return coordinates
    

def hosp_fetch_google_maps_api(path,apikey,final_csv):
    radius=str(5000)

    #making csv files
    if not os.path.isfile('hospitals_in_'+path+'.csv'):
        csvfile = open('hospitals_in_'+path+'.csv','w')
        writer = csv.writer(csvfile, delimiter='$')
        writer.writerow(["name","lat","long","rating","vicinity","place_id","open_status","Website"])
        csvfile.close()
    else:
        print('hospitals_in_'+path+'.csv'," already exits")
    
    #making list of coordinates
    coordinates=[]
    coordinates=coordinates_path(path,apikey,coordinates)
    
    #finding hospitals around every lat,long
    iteration_number=0
    total_iterations=len(coordinates)
    for (templat,templong) in coordinates:
        print('Iteration '+str(iteration_number)+' of '+str(total_iterations))
        csv_write(str(templat),str(templong),radius,path,apikey)
        iteration_number=iteration_number+1
    
    #dropping duplicates
    file_name = 'hospitals_in_'+path+'.csv'
    file_name_output = final_csv
    df = pd.read_csv(file_name, sep="$")
    df.drop_duplicates(subset=None, inplace=True)
    df.to_csv(file_name_output)
    
def main_func(): 
    input_place1=input("Enter the City 1 : ")
    input_place2=input("Enter the City 2 : ")
    path=input_place1+"__and__"+input_place2
    
    apikey='AIzaSyANve4D244SJWLUesBDKk8c9w_CPJCf2AU'
    # apikey="AIzaSyCWmN2ssnrkdNKq9w8cMcBHUVkwSpRh9ag"
    final_csv='hospitals_in_'+path+'_without duplicates.csv'
    
    hosp_fetch_google_maps_api(path, apikey,final_csv)
    
    df=merge(final_csv)
    df.drop_duplicates(subset=None, inplace=True)
    df.to_csv(final_csv)
    '''
    use functions   from add_department_column import fetch_dept(final_csv) #for adding department column
                    from search_ph_no import search_phone_no_googlemaps(final_csv) #for adding more phone nos by google maps website
                    from search_ph_no import search_phone_no_web(final_csv) #for adding more phone nos by webscraping by search

    Also this timings csv also can be added from get_timings_csv.py import def find_timings(query="https://www.google.com/maps/search/?api=1&query="+str(row['lat'])+","+str(row['long'])+"&query_place_id="+str(row['place_id'])) 
    '''
    return df,final_csv,path


