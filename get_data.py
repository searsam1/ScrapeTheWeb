
"""
Step 1:
	Login
"""
import os
from bs4 import BeautifulSoup
#from pw_and_user import username, password
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from string import punctuation, printable


class Edabit():

	sign_in_btn_xpath = r"""//*[@id="Navbar"]/div/div/div/div[1]/button"""
	username_btn_xpath = r"""/html/body/div[2]/div/div[2]/div/div/div[1]/form/div[1]/div/div/input"""
	password_btn_xpath = r"""/html/body/div[2]/div/div[2]/div/div/div[1]/form/div[2]/div/div/input"""
	sign_in_again_btn_xpath = r"""/html/body/div[2]/div/div[2]/div/div/div[1]/form/div[3]"""
	# load_more_btn_xpath = r"""//*[@id="Main"]/div/div/div[2]/div[2]/button"""
	# lang_btn_xpath = r"""//*[@id="Main"]/div/div/div[1]/form/div[1]/div"""
	# python_btn_xpath = r"""//*[@id="Main"]/div/div/div[1]/form/div[1]/div/div/div[2]/div[6]""" 
	instructions_xpath = r"""//*[@id="Main"]/div/div/div[1]/div/div[2]"""
	tests_btn_xpath = r"""//*[@id="Main"]/div/div/div[2]/div/div[1]/div/div/div/div/div[2]"""
	tests_xpath = r"""//*[@id="Main"]/div/div/div[2]/div/div[2]"""
	code_btn_xpath = r"""//*[@id="Main"]/div/div/div[1]/div/div[1]/div[2]/div/div/div/div[3]"""
	code_xpath = r"""//*[@id="Code"]"""
	solutions_btn_xpath = r"""//*[@id="Main"]/div/div/div[1]/div/div[1]/div[2]/div/div/div/div[5]"""

	python_repo = '/Users/111244rfsf/Documents/Repositories/theEdabitProject/python'
	challenge_link = input("Edabit Challenge Link?\n: ")
	tests_script = f"""import unittest

class Test(unittest.TestCase):
	
	checks = [] 
	def assert_equals(a,b,checks=checks):
		print(a,b,sep="  ->  ")
		checks.append(["Fail","Pass"][a==b])
		print("\\t",checks,"\\n")
		"""
	driver = webdriver.Safari()

	def __init__(self,login_url):
		self.login_url = login_url

	def replace_quotes(self,data):
		data = data.replace("\"","\\\"").replace("'","\\'")
		return data

	def login(self):
		self.driver.get(self.login_url)
		self.driver.implicitly_wait(30)
		sign_in_btn = self.driver.find_element(by=By.XPATH, 
			value=self.sign_in_btn_xpath)
		sign_in_btn.click()
		username_field = self.driver.find_element(by=By.XPATH, 
			value=self.username_btn_xpath)
		username_field.send_keys(username, Keys.TAB, password
			)
		sign_in_again_btn = self.driver.find_element(by=By.XPATH, 
			value=self.sign_in_again_btn_xpath)
		sign_in_again_btn.click()
	

	def get_last_word(self,string):
		words = []
		word = "" 
		for char in string:
			if char.isupper():
				if len(word) > 1:
					words.append(word)
				word = char
			else:
				word += char
		if len(word) > 1:
			words.append(word)
		return "\n".join(words)


	def download_challenge(self):
		#self.driver.get('https://edabit.com/challenge/zJSF5EfPe69e9sJAc')
		self.driver.get(self.challenge_link) # for final version.
		time.sleep(3)
		# Challenge Instructions  
		instructions = self.driver.find_element(by=By.XPATH, 
			value=self.instructions_xpath)
		
		# Challenge tests Tab Button
		tests_btn = self.driver.find_element(by=By.XPATH, 
			value=self.tests_btn_xpath)
		tests_btn.click()
		# Actual Tests field
		tests = self.driver.find_element(by=By.XPATH, 
			value=self.tests_xpath)
		
		code_btn = self.driver.find_element(by=By.XPATH, 
			value=self.code_btn_xpath)
		code_btn.click()
		time.sleep(.5)
		code = self.driver.find_element(by=By.XPATH, 
			value=self.code_xpath)
		
		# add \" and \' for bash when writing to a file
		clean_instructions = self.replace_quotes(instructions.text).split('xxxxxxxxxx')[0]
		clean_instructions = " ".join(word if not "PythonLanguages" in word
			else self.get_last_word(word)
			for word in clean_instructions.split()
			)

		# clean the data
		clean_instructions = clean_instructions.replace("Translate","\n\n")
		clean_instructions = clean_instructions.replace("Examples","\n~Examples~\n")
		clean_instructions = clean_instructions.replace("Notes","\n~Notes~\n")
		clean_instructions = clean_instructions.split("Watch a quick demo on how Edabit works")[0]
		clean_instructions = clean_instructions.replace("Published", "\n\tPublished")
		clean_tests = self.replace_quotes(tests.text).split('xxxxxxxxxx')[0]
		clean_code = self.replace_quotes(code.text).split('xxxxxxxxxx')[0]

		# create folder in current directory. 
		function_name = clean_code.split()[1].split("(")[0]
		challenge_name = function_name
		os.chdir(self.python_repo)
		os.mkdir(challenge_name)
		os.chdir(challenge_name)
		# create instructions, code, and test files
		os.system(f"echo $'{clean_instructions}' > instructions.txt")
		os.system(f"echo $'{clean_code}pass' > {function_name}.py")
		with open(f"tests.py", "w") as f:
			f.write(f"from {challenge_name} import {challenge_name}")
			f.write("\n")
			f.write(self.tests_script)
			f.write("\n")
		os.system(f"echo $'{clean_tests}' >> tests.py")

		# open files
		os.system("open instructions.txt")
		os.system("open tests.py")
		os.system(f"open {function_name}.py")

	def close_driver(self):
		self.driver.close()

if __name__ == '__main__':
	e = Edabit("https://edabit.com")
	#e.login()
	e.download_challenge()
	e.close_driver()  



