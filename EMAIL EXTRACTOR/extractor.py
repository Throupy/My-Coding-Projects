from bs4 import BeautifulSoup
from validate_email import validate_email
import requests
import re
import csv
import time
urls_to_parse = ["https://github.com/Throupy/My-Coding-Projects/blob/master/EMAIL%20EXTRACTOR/sample_files.md", "https://youtube.com"]

def write_data(emails):
    """This function writes the data to the CSV file"""
    with open('emails.csv', mode='a') as email_file:
        email_writer = csv.writer(email_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for email in emails[0]:
            email_writer.writerow([email])   

def parse(page):
    """Parses the HTML to find email addresses"""
    emails = [] #Empty set of emails
    soup = BeautifulSoup(page.content, "html.parser") #parse the page
    new_emails = ["[*]Emails found:"] + re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soup.text, re.I) #find emails with regex
    print("\n".join([x for x in new_emails if (len(new_emails) != 1)]) + '\n');time.sleep(1)
    emails.append(new_emails) #add emails to the list
    for email in emails[0][1:]: #for each email in the set verify the email is valid
        if validate_email(str(email), verify=True): #verify = true uses DNS to find out if that email actually exists
            print(f"{email} is valid")
        else:
            print(f"{email} isn't valid")
            emails[0].remove(email)

    write_data(emails)

for url in urls_to_parse:
    page = requests.get(url) #Set url to page
    parse(page)
    urls_to_parse.remove(url)
