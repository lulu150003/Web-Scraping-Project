# Load libraries
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import pandas as pd

# Create values Selenium
USERNAME = #raw_input("Enter username: ") 
PASSWORD = #raw_input("Enter password: ") 
linkedin = 'https://www.linkedin.com'

# Open Selenium
browser = webdriver.Firefox()
browser.get(linkedin)
time.sleep(3)
# Identify email and password inputs and enter in information
email = browser.find_element_by_name('session_key')
password = browser.find_element_by_name('session_password')
email.send_keys(USERNAME + Keys.RETURN)
password.send_keys(PASSWORD + Keys.RETURN)
# Go to profile page and scroll to the bottom of the page to load elements of page
time.sleep(3)

#Create Large Loop

#Read csv
import csv
r = pd.read_csv("output_search.csv")

# Function to identify driver
def driving(x):
    if x.lower().find('data') != -1 or x.lower().find('scien') != -1 or x.lower().find('Data') != -1 or x.lower().find('Scien') != -1 or x.lower().find('machine') != -1:
        return(1)
    else:
        return(0)

    
# Create driver column
r['driver'] = list(map(driving, r['title']))
#Remove value 0
r = r[r.driver != 0]


#create empty data frame
Exp_df = pd.DataFrame(columns = ['profile', 'exp_title', 'exp_company', 'exp_dates'])
Edu_df = pd.DataFrame(columns = ['profile', 'ed_name', 'ed_deg', 'ed_dates'])
Ski_df = pd.DataFrame(columns = ['profile', 'skill'])

#Create big loop
#for link in r.loc[0:5,'profile']:
for link in r.loc[:,'profile']:
    if link == 'https://www.linkedin.com#':     #if it equal link then skip
        continue 
    time.sleep(2)
# This section is where you put in the profile link (loaded from the csv file) and browse to it
    search = link
    browser.get(search)
    time.sleep(2)
    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(.75)
    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(.75)
    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(.75)
    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(.75)
    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #raw = urlopen(link).read()
    #page = BeautifulSoup(raw, "html.parser")
    page = BeautifulSoup(browser.page_source, 'lxml')
    
#Experience Section  
    titles = page.find_all('div', class_ = "pv-entity__position-group-pager")
    companies = page.find_all('span', class_ = "pv-entity__secondary-title")
    dates = page.find_all('h4', class_ = "pv-entity__date-range")

    #Put scraped data into exp_df

    arraylen1 = len(page.find_all('div', class_ = "pv-entity__position-group-pager"))

    profile = link
    exp_titles = list(map(lambda x: x.h3.text.strip(), titles))[0:arraylen1]
    exp_companies = list(map(lambda x: x.text.strip(), companies))[0:arraylen1]
    exp_dates = list(map(lambda x: x.text.strip().split('\n')[-1], dates))[0:arraylen1]
    
 #Education Section 
    institution = page.find_all('div', class_ = "pv-entity__degree-info")
    degree = page.find_all('p', class_ = "pv-entity__degree-name")
    dates = page.find_all('p', class_ = "pv-entity__dates")
 
    #Put scraped data into edu_df
    
    arraylen2 = len(page.find_all('div', class_ = "pv-entity__degree-info"))

    profile = link
    ed_name = list(map(lambda x: x.text.strip().split('\n')[-1], institution))[0:arraylen2]
    ed_deg = list(map(lambda x: x.text.strip().split('\n')[-1], degree))[0:arraylen2]
    ed_dates = list(map(lambda x: x.text.strip().split('\n')[-1], dates))[0:arraylen2]
    if len(ed_dates) < arraylen2:
        ed_dates = 'NA'
 #Skill Section 
    skill = page.find_all('span', class_ = "pv-skill-category-entity__name-text")
    
    #Put scraped data into a ski_df
    
    arraylen3 = len(page.find_all('span', class_ = "pv-skill-category-entity__name-text"))
        
    profile = link
    skill = list(map(lambda x: x.text.strip(), skill))[0:arraylen3]
    try:
        temp1 = pd.DataFrame({'profile':profile, 'exp_title':exp_titles, 'exp_company':exp_companies, 'exp_dates':exp_dates})
        temp2 = pd.DataFrame({'profile':profile, 'ed_name':ed_name, 'ed_deg':ed_deg, 'ed_dates':ed_dates}) 
        temp3 = pd.DataFrame({'profile':profile, 'skill':skill})
        Exp_df = Exp_df.append(temp1)
        Edu_df = Edu_df.append(temp2)
        Ski_df = Ski_df.append(temp3)
        print(link, 'completed')
    except:
        print(link, 'skipped')
        continue


# Reset dataframe index
Exp_df.reset_index()
Edu_df.reset_index()
Ski_df.reset_index()
        
# Export results
Exp_df.to_csv("output_experience.csv", index = False,sep='\t', encoding='utf-8')
Edu_df.to_csv("output_education.csv", index = False,sep='\t', encoding='utf-8')
Ski_df.to_csv("output_skills.csv", index = False,sep='\t', encoding='utf-8')

# Close Selenium
browser.quit()

