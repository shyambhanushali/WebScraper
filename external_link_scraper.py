import requests
from bs4 import BeautifulSoup as bs
import sys
import re


url = sys.argv[1]  # Take in the url from command line which takes 1 argument

'''
Check to determine the domain name of the URL
Domain name will be used to filter between external and non external links
'''
if url.split("://")[1].split(".")[0] == "www":
    domain = url.split("://")[1].split(".")[1]
else:
    domain = url.split("://")[1].split(".")[0]


links = []  # Initialize a list to store all the external links
res = requests.get(url)
response = res.text

soup = bs(res.content,"lxml")  # Creating beautiful soup object for html parsing


'''
Replace all the newlines,tabs and spaces with tabs for easy parsing
'''

response.replace("\n", " ")
response.replace("\t", " ")
response.replace("\r", " ")

'''
Loop to find all external links starting with http
If the URL starts with www, the code checks the next string and
If the next string is same as domain name, the URL is not external and is discarded
'''
for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    unsanitized_link = link.get('href')
    if unsanitized_link.split("://")[1].split(".")[0] == "www" \
            and unsanitized_link.split("://")[1].split(".")[1] != domain:
        sanitized_link = unsanitized_link
        if sanitized_link not in links:  # remove duplicate links
            links.append(sanitized_link)

    elif unsanitized_link.split("://")[1].split(".")[0] != domain:
        sanitized_link = unsanitized_link
        if sanitized_link not in links:  # remove duplicate links
            links.append(sanitized_link)

    else:
        pass

'''
Loop to find all external links starting with https
If the URL starts with www, the code checks the next string and
If the next string is same as domain name, the URL is not external and is discarded
'''
for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
    unsanitized_link = link.get('href')
    if unsanitized_link.split("://")[1].split(".")[0] == "www" \
            and unsanitized_link.split("://")[1].split(".")[1] != domain:

        sanitized_link = unsanitized_link
        if sanitized_link not in links:  # remove duplicate links
            links.append(sanitized_link)

    elif unsanitized_link.split("://")[1].split(".")[0] != domain and unsanitized_link.split("://")[1].split(".")[0] \
            != "www":
        sanitized_link = unsanitized_link
        if sanitized_link not in links:  # remove duplicate links
            links.append(sanitized_link)

    else:
        pass
print("External links discovered: ")
for link in links:
    print(link)
print("=================================================")
print("Number of Unique External links found: " + str(len(links)))
print("=================================================")

