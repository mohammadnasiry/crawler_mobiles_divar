import requests
from bs4 import BeautifulSoup
import pandas as pd

# for save informatiion
Mobile_Data = []

# Function to create mobile list entry
def Create_Mobile(MobileName, info, Link):
    Mobile_Data.append({
        'Title': MobileName,
        'INFO' : info,
        'Link': Link
    })

# loop to crawl
for i in range(1):  # number of page
    url = f"https://divar.ir/s/mashhad/mobile-phones?page={i}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        all_links = soup.find_all("a", href=True)
        divar_links = [link["href"] for link in all_links if link['href'].startswith('/v')]
        print(f"Found {len(divar_links)} mobile ad links on page {i}.\n")

        for link in divar_links:
            mobile_url = "https://divar.ir" + link
            response = requests.get(mobile_url)
            if response.status_code == 200:
                soup2 = BeautifulSoup(response.text, "html.parser")
                print(f"Processing URL: {mobile_url}\n")
                try:
                    # Title
                    name = soup2.find_all('div', {'class': 'kt-page-title__texts'})
                    for box in name:
                        name_title = box.find_all('h1') 
                        for i in name_title:
                            title = i.get_text().replace('\u200c', ' ')
                            print(title )
                    
                    # Price
                    info_box = soup2.find_all('div', {'class' : 'kt-base-row kt-base-row--large kt-unexpandable-row'})
                    for box1 in info_box:
                        info_tag = box1.find_all('p') 
                        for i in info_tag:
                            info = i.get_text().replace('\u200c', ' ')
                            print(info )
              
                    # Store information in the dictionary
                    Create_Mobile(title, info, mobile_url)

                except Exception as e:
                    print(f"Error extracting data from {mobile_url}: {e}\n")
            else:
                print(f"Failed to load mobile page: {response.status_code} - URL: {mobile_url}\n")
    else:
        print(f"Failed to load main page: {response.status_code}\n")

# number of mobile records
print(f"Total number of mobile records: {len(Mobile_Data)}\n")

# make a  Dataframe
df = pd.DataFrame(Mobile_Data)
# print top of Dataframe
print(df.head())

# save mobile data in excel
df.to_excel('Mobile_Data.xlsx', engine='openpyxl')
# save mobile data in .csv
df.to_csv('Mobile_Data.csv', encoding='utf-8-sig')

print("Data saved to Mobile_Data_Updated.xlsx and Mobile_Data_Updated.csv\n")
