# ePDG Discovery Script
from bs4 import BeautifulSoup
import requests
import json
import socket

all_mnc_mcc_data = []

print("")
print("")
print("")
print("")

print("Starting ePDG discovery...")
print("Fetching the latest database of MNCs and MCCs")

# Grab the webpage
page = requests.get("https://www.mcc-mnc.com/")
# Setup the HTML parser
soup = BeautifulSoup(page.content, 'html.parser')
# Find all table rows
all_rows = soup.find_all('tbody')[0].find_all('tr')
# Iterate over all MNC/MCC rows
for i in range(0, len(all_rows)):

    # Get current mcc
    current_mcc = str(all_rows[i].find_all('td')[0].get_text()).zfill(3)
    # Get current mnc
    current_mnc = str(all_rows[i].find_all('td')[1].get_text()).zfill(3)
    # Generate the current URL based off the MNC and MCC
    current_url = "epdg.epc.mnc"+current_mnc+".mcc"+current_mcc+".pub.3gppnetwork.org"
    current_ip = ""
    try:
        # Find the current url
        current_ip = socket.gethostbyname(current_url)
        print(current_url + " - " + current_ip)
    except:
        # Generated when the DNS is not found
        print(current_url + " was not found.")
    # Get the text from each tag
    current_mcc_mnc = {
        "mcc": current_mcc,
        "mnc": current_mnc,
        "iso": all_rows[i].find_all('td')[2].get_text(),
        "country": all_rows[i].find_all('td')[3].get_text(),
        "country_code": all_rows[i].find_all('td')[4].get_text(),
        "network": all_rows[i].find_all('td')[5].get_text(),
        "epdg": current_url,
        "epdg_ip": current_ip
    }
    # Store it into the a python list
    all_mnc_mcc_data.append(current_mcc_mnc)

# Store all of this into a JSON file.
f = open("mcc_mnc_dump.json", "w")
f.write(json.dumps(all_mnc_mcc_data))
f.close()

print("Done.")