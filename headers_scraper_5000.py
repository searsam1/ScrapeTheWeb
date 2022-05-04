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
