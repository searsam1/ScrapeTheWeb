
# by alecSears
import os

import clipboard

from bs4 import BeautifulSoup
#from pw_and_user import username, password
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from string import punctuation, printable
challenge_link = clipboard.paste() # <---- Ran from inside Automator

class Edabit():


	# for better readability 
	# otherwise the xpaths get way 2 long
	clean = lambda x : x.replace("\n","").replace("\t","").replace(" ","")
	driver = webdriver.Safari()
	driver.get(challenge_link)


	sign_in_btn_xpath = clean(r"""
	//*[@id="Navbar"]/div/
	div/div/div[1]/button
	""")
	username_btn_xpath = clean(r"""
	/html/body/div[2]/div/div[2]
	/div/div/div[1]/form/
	div[1]/div/div/input
	""")
	password_btn_xpath = clean(r"""
	/html/body/div[2]/div/
	div[2]/div/div/div[1]/form
	/div[2]/div/div/input
	""")
	sign_in_again_btn_xpath = clean(r"""
	/html/body/div[2]/div
	/div[2]/div/div/div[1]
	/form/div[3]
	""")
	#--------------------for loading solutions--------------------
	# load_more_btn_xpath = clean(r"""
	# //*[@id="Main"]/div/div
	# /div[2]/div[2]/button
	# """)
	# lang_btn_xpath = clean(r"""
	# //*[@id="Main"]/div/div
	# /div[1]/form/div[1]/div
	# """)
	# python_btn_xpath = clean(r"""
	# //*[@id="Main"]/div/div/
	# div[1]/form/div[1]/
	# div/div/div[2]/div[6]
	# """)
	#------------------------------------------------------------
	instructions_xpath = clean(r"""
	//*[@id="Main"]/div/
	div/div[1]/div/div[2]
	""")
	tests_btn_xpath = clean(r"""
	//*[@id="Main"]/div/div
	/div[2]/div/div[1]/div
	/div/div/div/div[2]
	""")
	tests_xpath = clean(r"""
	//*[@id="Main"]/div
	/div/div[2]/div/div[2]
	""")
	code_btn_xpath = clean(r"""
	//*[@id="Main"]/div/div/div[1]
	/div/div[1]/div[2]
	/div/div/div/div[3]
	""")
	code_xpath = clean(r"""//*[@id="Code"]""")
	
	solutions_btn_xpath = clean(r"""
	//*[@id="Main"]/div/div/div[1]
	/div/div[1]/div[2]
	/div/div/div/div[5]
	""")

	python_repo = clean("""
	/Users/111244rfsf/Documents/Repositories/
	theEdabitProject/theEdabitProjectRepo/Python
	""")

	tests_script = f"""import unittest

class Test(unittest.TestCase):
	
	checks = [] 
	def assert_equals(a,b,message=None,checks=checks):
		print(a,b,sep="  ->  ")
		checks.append(["Fail","Pass"][a==b])
		print("\\t",checks,"\\n")
"""
	def replace_quotes(self,data):
		# add \" and \' for bash when writing to a file
		data = data.replace("\"","\\\"").replace("'","\\'")
		return data

	def login(self):
		# get(load) the url supplied by the user
		# deprecated
		# not really sure if this works
		self.driver.implicitly_wait(30)
		
		# click sign in button
		sign_in_btn = self.driver.find_element(by=By.XPATH, 
			value=self.sign_in_btn_xpath)
		sign_in_btn.click()

		# fill in username and password
		username_field = self.driver.find_element(by=By.XPATH, 
			value=self.username_btn_xpath)
		
		# tab to get to password // fill password
		username_field.send_keys(username, Keys.TAB, password
			)
		
		# login
		sign_in_again_btn = self.driver.find_element(by=By.XPATH, 
			value=self.sign_in_again_btn_xpath)
		sign_in_again_btn.click()
	

	def get_last_word(self,string):
		""" 
		Split a string by title case with no spaces.
		Ex. "MyNameIsJohnSmith"
				-- > 
					My Name Is John Smith
		"""
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

		# Wait for Challenge to load
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
		
		# click code btn to get function name (thats in code)
		code_btn = self.driver.find_element(by=By.XPATH, 
			value=self.code_btn_xpath)
		code_btn.click()
		time.sleep(.5)
		
		# code field where the function name is defined.
		# We need this for the filename(the filename is the 
		# name of the function), and to start the 
		# put in the new script. 
		code = self.driver.find_element(by=By.XPATH, 
			value=self.code_xpath)
		
		# get the instructions to the challenge
		# instruc short for instruction
		instruc_txt = instructions.text

		# add \" and \' for bash when writing to a file
		# using replace quotes
		clean_instructions = self.replace_quotes(instruc_txt).split('xxxxxxxxxx')[0]
		clean_instructions = " ".join(word if not "PythonLanguages" in word
			else self.get_last_word(word)
			for word in clean_instructions.split()
			)

		# clean the data
		# when I scrape edabit the text comes in a little dirty. 
		clean_instructions = clean_instructions.replace("Translate","\n\n")
		clean_instructions = clean_instructions.replace("Examples","\n~Examples~\n")
		clean_instructions = clean_instructions.replace("Notes","\n~Notes~\n")
		clean_instructions = clean_instructions.split("Watch a quick demo on how Edabit works")[0]
		clean_instructions = clean_instructions.replace("Published", "\n\tPublished")
		clean_tests = self.replace_quotes(tests.text).split('xxxxxxxxxx')[0]
		clean_code = self.replace_quotes(code.text).split('xxxxxxxxxx')[0]

		# create folder in current directory. 
		function_name = clean_code.split()[1].split("(")[0] # <<- only works for python
		challenge_name = function_name
		
		# --OS-- <chrdir>, <mkdir>
		os.chdir(self.python_repo)
		os.mkdir(challenge_name)
		os.chdir(challenge_name) # <-- We are now in the Python REPO
		
		# create instructions, code, and test files
		os.system(f"echo $'{clean_instructions}' > instructions.txt")
		os.system(f"echo $'{clean_code}pass' > {function_name}.py")
		with open(f"tests.py", "w") as f:
			# so we can separate the function from the tests
			# might be removed in later version 
			f.write(f"from {challenge_name} import {challenge_name}")
			f.write("\n")
			# needs to be more dynamic
			# (more than python capable)
			f.write(self.tests_script)
			f.write("\n")
		
		# create the tests file
		os.system(f"echo $'{clean_tests}' >> tests.py")

		# open files
		os.system("open instructions.txt")
		os.system("open tests.py")
		os.system(f"open {function_name}.py")

		# Git add, commit, push
		os.chdir(self.python_repo) # <-- so it updates old challenges
		os.system("git add .")
		os.system(f"git commit -m 'Add -->{function_name}<--'")
		os.system("git push")

	def close_driver(self):
		# probably should make this automatic
		self.driver.close()

if __name__ == '__main__':
	e = Edabit()
	#e.login()
	e.download_challenge()
	e.close_driver()  
# Fri May 13 00:31:03 MDT 2022 
# last edit
# 