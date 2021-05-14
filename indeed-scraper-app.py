import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

st.title('Indeed Job Site Scraper')

st.markdown("""
This app scrapes [Indeed](https://ca.indeed.com/) for the latest job postings
* _Python libraries used_: streamlit, pandas, requests, BeautifulSoup and csv
""")

##############################################################
# Input
##############################################################

st.sidebar.header('User Input')

title = st.sidebar.text_input('Enter the job title to search')

province = st.sidebar.selectbox('Province or Territory preferred', ("Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Northwest Territories", "Nunavut", "Yukon"))

##############################################################
# Application Logic
##############################################################

baseURL = "https://ca.indeed.com"

query = f"https://ca.indeed.com/jobs?q={title}&l={province}"

# st.write(query.format(title=title))

# st.write(province)

# Read data from Indeed using predefined query
# html = requests.get('https://ca.indeed.com/jobs?q=data%20scientist&l=Ontario').text
html = requests.get(query).text
soup = BeautifulSoup(html, 'lxml')

role_list = []
company_list = []
location_list = []
details_list = []
date_pub_list = []

for job in soup.find_all('div', attrs={'data-tn-component':'organicJob'}):
    role = job.find('h2', class_="title").a.text
    company = job.find('span', class_="company").text
    location = job.find('span', class_="location accessible-contrast-color-location").text
    date_published = job.find('span', class_="date date-a11y").text
    details = job.find('h2', class_="title").a.get('href')

    # Check that the job is either just posted or published today
    if date_published == 'Today' or date_published == 'Just posted':
        role = role.strip()
        company = company.strip()
        location = location.strip()
        link = baseURL+details

        role_list.append(role)
        company_list.append(company)
        location_list.append(location)
        details_list.append(link)
        date_pub_list.append(date_published)
        
        # writer.writerow([role, company, location, link, date_published])

# Write to DataFrame
df = pd.DataFrame(list(zip(role_list, company_list, location_list, details_list, date_pub_list)), 
columns=["Role", "Company", "Location", "Details", "Date Published"])

if df.shape[0] > 1:
    st.header('Recent ' + title + ' jobs')
else:
    st.header('Recent ' + title + ' job')

st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')

st.dataframe(df)