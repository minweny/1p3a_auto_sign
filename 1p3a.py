from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import time
with open("accounts.json") as json_file:
	data = json.load(json_file)
	account = data['account']
	password = data['password']
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument('user-agent=' + userAgent)
driver = webdriver.Chrome(chrome_options=options)
driver.get("https://www.1point3acres.com/bbs")
driver.implicitly_wait(3)
account_input = driver.find_element_by_name("username")
account_input.send_keys(account)
pass_input = driver.find_element_by_name("password")
pass_input.send_keys(password)
pass_input.send_keys(Keys.ENTER)
time.sleep(5)
attachment = 'image.png'
driver.save_screenshot(attachment)
point = driver.find_element_by_id("extcreditmenu").text
print(point)
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
	message["Subject"] = point
	message["From"] = account
	message["To"] = receiver
	img.add_header('Content-ID', '<{}>'.format(attachment))
	message.attach(img)
	server.sendmail(account, receiver, message.as_string())
	
