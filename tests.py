clean = lambda x : x.replace("\n","").replace("\t","").replace(" ","")

sign_in_btn_xpath = clean(r"""
	//*[@id="Navbar"]/div/
	div/div/div[1]/button
	""")

print(sign_in_btn_xpath)