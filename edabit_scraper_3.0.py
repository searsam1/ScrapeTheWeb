# %%
#Alec Sears
from datetime import datetime
from time import sleep
import os
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
        , capture_output=True).stdout.strip(b'\n').decode()        

    def __init__(self,link=link):
        self.driver = webdriver.Safari()
        self.driver.get(link)
        self.id = link.split("/")[-1]

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
file_exts = {
    "C++" : [".cpp","CPP"],
    "C#" : [".cs","csharp"],
    "Java" : [".java","java"],
    "JavaScript" : [".js","javaScript"],
    "PHP" : [".php","php"],
    "Python" : [".py", "python"],
    "Ruby" : [".rb","ruby"],
    "Swift" : [".swift","swift"]
}

file_ext = eda.find_by_xpath('//*[@id="Main"]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div[1]/div/div[1]')
ext = file_exts[file_ext.text][0]
ext_loc = file_exts[file_ext.text][1]



# %%
soup = BeautifulSoup(source2, 'lxml')
code = soup.textarea.text



# %%
soup = BeautifulSoup(source3, 'lxml')
# still in alpha stages
tests_file = soup.find_all(class_="six wide column")[0].text
tests_file = tests_file.split("\n")
tests_file[-1] = tests_file[-1].split("xxxxxxxxxx")[0]

# %%
soup = BeautifulSoup(source1, 'lxml')

title = soup.find('h2').text
author = soup.find('a', style="color: rgb(41, 135, 205); font-weight: 700;").text
objective = "\n".join(i.text for i in soup.find_all(['p','li']))
examples = soup.pre.text

arr = [title, author, objective, examples, code]


hash = eda.id

os.chdir(f"/Users/111244rfsf/Documents/Repositories/theEdabitProject/theEdabitProjectRepo/{ext_loc}")

try:
    os.mkdir(hash)
except FileExistsError:
    pass

os.chdir(hash)

with open("readme.md", "w") as f:
    f.write("# " + title + "\n<br><br>\n")
    f.write("## " + author +"\n<br><br>\n")
    f.write("### \"\"\"" + objective +"\"\"\"\n<br><br>\n")
    f.write(f"[{eda.id}]({eda.link})" +"\n<br><br>\n")
    f.write("```" + examples + "\n```\n" + "\n<br><br>\n" )


with open(f"code{ext}", "w") as f:
    f.write(code)
    for i in tests_file:
        f.write("\n\n")
        f.write(i)
os.system("open readme.md")
os.system(f"open -a Visual\\ Studio\\ Code code{ext}")
eda.driver.close()

# Git add, commit, push
os.system('echo ".DS_Store" > .gitignore')
os.chdir("/Users/111244rfsf/Documents/Repositories/theEdabitProject/theEdabitProjectRepo")
os.system("git pull")
os.system("git add .")
os.system(f"git commit -m 'Create Challenge : {eda.id} on {datetime.now()}'")
os.system("git push")

# %%



