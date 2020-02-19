import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time
import datetime
import os

logging.basicConfig(filename='example.log',level=logging.DEBUG)
def printAndLogging(s):
	print(s)
	logging.debug(s)

datetime_str = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
printAndLogging(datetime_str)

printAndLogging(os.getcwd())

with open("accounts.json") as json_file:
	forumAccounts = json.load(json_file)
with open("email.json") as json_file:
	email = json.load(json_file)
senderEmailAccount = email['senderGmailAccount']
senderEmailPassword = email['senderGmailPass']
receiverEmailAccount = email['receiver']
printAndLogging('sender: ' + senderEmailAccount)
printAndLogging('receiver: ' + receiverEmailAccount)
port = 465  # For SSL

ua = UserAgent()
userAgent = ua.random
printAndLogging(userAgent)
options = Options()
options.add_argument('--no-sandbox')
# options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=' + userAgent)

login_url = "https://www.1point3acres.com/bbs"

def autoSign(forumAccountName, forumAccountPassword):
	try:
		driver = webdriver.Chrome(options=options)
		driver.implicitly_wait(3)
		driver.get(login_url)
		account_input = driver.find_element_by_name("username")
		account_input.send_keys(forumAccountName)
		pass_input = driver.find_element_by_name("password")
		pass_input.send_keys(forumAccountPassword)
		pass_input.send_keys(Keys.ENTER)
		time.sleep(2)
		driver.get(login_url)
		time.sleep(3)
		screenshotName = 'image.png'
		driver.save_screenshot(screenshotName)
		point = driver.find_element_by_id("extcreditmenu").text
		printAndLogging('old point' + point)
		newPoint = point
		
		# clear all notifications
		for col in range(1, 5):
			notifactionCol = driver.find_elements(By.XPATH, "//*[@id='myprompt_menu']/li[{}]/a".format(str(col)))
			if len(notifactionCol) > 0:
				try:
					printAndLogging('click ' + str(col))
					notifactionCol[0].click()
					time.sleep(5)
					driver.get(login_url)
					time.sleep(5)
				except Exception as e:
					printAndLogging(e)
		
		# if there is notifications box
		notifications = driver.find_elements(By.XPATH, "//*[@id='myprompt_menu']")
		if len(notifications) > 0:
			printAndLogging('try to set the display to none...')
			try:
				driver.execute_script("document.getElementById('myprompt_menu').style.display='none';")
			except Exception as e:
				printAndLogging(e)
			time.sleep(5)

		signNodes = driver.find_elements(By.XPATH, "//*[@id='um']/p[2]/a[3]/font[text()='签到领奖!']")
		if len(signNodes) > 0:
			signNode = signNodes[0]
			signNode.click()
			time.sleep(3)
			driver.find_element(By.XPATH, "//*[@id='kx']").click()
			signText = '今天把论坛帖子介绍给好基友了~'
			printAndLogging(signText)
			driver.find_element(By.XPATH, "//*[@id='todaysay']").send_keys(signText)
			driver.find_element(By.XPATH, "//*[@id='qiandao']/p/button").click()
			time.sleep(3)
			newPoint = driver.find_element_by_id("extcreditmenu").text
		pointChange = point + ' -> ' + newPoint
		printAndLogging('new point' + newPoint)
		
		message = MIMEMultipart("alternative")
		message["Subject"] = pointChange
		message["From"] = forumAccountName
		message["To"] = receiverEmailAccount
		
		driver.quit()
		if len(signNodes) > 0:
			with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
				server.login(senderEmailAccount, senderEmailPassword)
				server.sendmail(forumAccountName, receiverEmailAccount, message.as_string())
		printAndLogging('Finished successfully!\n\n\n')
	except Exception as inst:
		printAndLogging(type(inst))
		printAndLogging(inst.args)
		printAndLogging(inst)
		printAndLogging('Error happens!\n\n\n')

for i, forumAccount in enumerate(forumAccounts):
	forumAccountName = forumAccount['account']
	forumAccountPassword = forumAccount['password']
	printAndLogging(str(i) + ' - ' + forumAccountName)
	autoSign(forumAccountName, forumAccountPassword)
