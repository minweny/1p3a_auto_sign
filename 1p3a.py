import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
def printAndLogging(s):
	print(s)
	logging.debug(s)

def autoSign():
	from selenium import webdriver
	import json
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.chrome.options import Options
	from fake_useragent import UserAgent
	import time
	import datetime
	datetime_object = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	printAndLogging(datetime_object)
	import os
	printAndLogging(os.getcwd())
	with open("accounts.json") as json_file:
		data = json.load(json_file)
		account = data['account']
		password = data['password']
	options = Options()
	options.add_argument('--no-sandbox')
	options.add_argument('--headless')
	options.add_argument('--disable-dev-shm-usage')
	ua = UserAgent()
	userAgent = ua.random
	printAndLogging(userAgent)
	options.add_argument('user-agent=' + userAgent)
	driver = webdriver.Chrome(options=options)
	driver.get("https://www.1point3acres.com/bbs")
	driver.implicitly_wait(3)
	account_input = driver.find_element_by_name("username")
	account_input.send_keys(account)
	pass_input = driver.find_element_by_name("password")
	pass_input.send_keys(password)
	pass_input.send_keys(Keys.ENTER)
	time.sleep(2)
	driver.get("https://www.1point3acres.com/bbs")
	time.sleep(3)
	attachment = 'image.png'
	driver.save_screenshot(attachment)
	point = driver.find_element_by_id("extcreditmenu").text
	printAndLogging('old point' + point)
	from selenium.webdriver.common.by import By
	signNodes = driver.find_elements(By.XPATH, "//*[@id='um']/p[2]/a[3]/font[text()='签到领奖!']")
	if len(signNodes) > 0:
		signNode = signNodes[0]
		signNode.send_keys(Keys.ENTER)
		time.sleep(3)
		driver.find_element(By.XPATH, "//*[@id='kx']").click()
		signText = '今天把论坛帖子介绍给好基友了~'
		printAndLogging(signText)
		driver.find_element(By.XPATH, "//*[@id='todaysay']").send_keys(signText)
		driver.find_element(By.XPATH, "//*[@id='qiandao']/p/button").click()
		time.sleep(3)
		newPoint = driver.find_element_by_id("extcreditmenu").text
		pointChange = point + ' -> ' + newPoint + ' : ' + datetime_object
		printAndLogging('new point' + newPoint)
		import smtplib, ssl
		from email.mime.text import MIMEText
		from email.mime.multipart import MIMEMultipart
		from email.mime.image import MIMEImage
		port = 465  # For SSL
		with open("emails.json") as json_file:
			data = json.load(json_file)
			account = data['senderGmailAccount']
			password = data['senderGmailPass']
			receiver = data['receiver']
		with open(attachment, 'rb') as png:
			img = MIMEImage(png.read())
		with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
			server.login(account, password)
			message = MIMEMultipart("alternative")
			message["Subject"] = pointChange
			message["From"] = account
			message["To"] = receiver
			img.add_header('Content-ID', '<{}>'.format(attachment))
			message.attach(img)
			server.sendmail(account, receiver, message.as_string())
	printAndLogging('Finished successfully!\n\n\n')
	time.sleep(1)
	driver.quit()
try:
	autoSign()
except Exception as inst:
	printAndLogging(type(inst))
	printAndLogging(inst.args)
	printAndLogging(inst)
	printAndLogging('Error happens!\n\n\n')
