# ScrapeTheWeb
With Python

A collection of python scripts where I scrape the web for data!
Some are using selenium and some the requests module.

This is the script I use to get my headers when I am sending 
a request not using selenium.
```
import requests
#from bs4 import BeautifulSoup
def scrape_headers(headers):

    res = {i.split(": ")[0].strip(":") : i.split(": ")[1].strip(":") 
              for i in headers.split("\n")
              if i
        }
    return res

headers = """
method : GET
"""
# url = "www.1234.com"
# head = scrape_headers(headers)
# r = requests.get(url,headers=head)
# soup = BeautifulSoup(r.text,'lxml')
# parse soup .text
```