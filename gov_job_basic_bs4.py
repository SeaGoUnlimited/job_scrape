#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sean_goral
"""
from bs4 import BeautifulSoup
import requests
#import time
import pandas as pd
import re

data = []

def jobitem2dict(jobitem):
    title = job_item.find('a', {'class': 'job-details-link'}).text
    location = job_item.find('div', {'class': 'job-location'}).text
    info = job_item.find_all('div', {'class': 'primaryInfo'})[1].text.strip()
    description = job_item.find('div', {'class': 'description hidden-phone'}).text.strip()
    posted = job_item.find('div', {'class': 'termInfo'}).text
    posted = re.sub("[^a-zA-Z0-9_]+", " ", posted)
    posted = re.sub("Continuous Share", '',posted)
    posted = re.sub("Share", '',posted)
    try:
        closes = re.split(' ago ',posted)[1]
    except IndexError:
        closes = 'na'
    try:
        posted = re.split(' Closes ',posted)[0]
    except IndexError:
        posted = posted
    jobitemdict = {'Title':title, 'Location':location, 'Info':info, 'Posted':posted, 'Closes':closes, 'Description':description}
    return jobitemdict 

for i in range(0, 50):
    url = 'https://www.governmentjobs.com/jobs?page=' + str(i) + '&keyword=specialist&location=california'    
    page = requests.get(url)        
    soup = BeautifulSoup(page.content, "html.parser")        
    job_div = soup.find('div', {'id': 'job-list-container'})
    job_items = job_div.find_all('li', attrs={'class': 'job-item'})
    
    for job_item in job_items:        
        jobitemdict = jobitem2dict(job_item)
        data.append(jobitemdict )    

df = pd.DataFrame(data)
print(df)   
df.to_csv("ca_specialists_jobs.csv",header=True,columns=['Title','Location','Info','Posted', 'Closes','Description'],index=False)
