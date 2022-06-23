# %%
from time import sleep
import subprocess
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%
class Edabit():

    link = subprocess.run(['osascript', '-e ' 'tell app "safari"\
                        to get the url of the current tab of window 1']
        , capture_output=True).stdout

    def __init__(self,link=link):
        self.driver = webdriver.Safari()
        self.driver.get(link.decode())

    def wait_until_vis(self,xpath,wait_time=20):
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(
                (By.XPATH, xpath)))    

    def find_by_xpath(self, xpath):
        return self.driver.find_element(By.XPATH,xpath)

    def control_string_len(string,block_length=75):
        blocks = [] 
        if len(string) > block_length:
            for i in range(0, len(string), block_length):
                block = string[i:i+block_length]
                blocks.append(block)
        writable_string = "-\n".join(blocks)
        return writable_string



# %%
eda = Edabit()

eda.wait_until_vis('//*[@id="Main"]/div/div/div[1]/div/div[2]/div[1]/div/div[1]/div[1]/h2')
source1 = eda.driver.page_source

eda.find_by_xpath('//*[@id="Main"]/div/div/div[1]/div/div[1]/div[2]/div/div/div/div[3]').click()
source2 = eda.driver.page_source

eda.find_by_xpath('//*[@id="Main"]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]').click()
sleep(.23)
source3 = eda.driver.page_source


# %%
soup = BeautifulSoup(source2, 'lxml')
code = soup.textarea.text

# %%
soup = BeautifulSoup(source1, 'lxml')

title = soup.find('h2').text
author = soup.find('a', style="color: rgb(41, 135, 205); font-weight: 700;").text
objective = "\n".join(i.text for i in soup.find_all(['p','li']))
examples = soup.pre.text

for i in [title, objective, author, examples, code]:
    print()
    print(i)
    print()



