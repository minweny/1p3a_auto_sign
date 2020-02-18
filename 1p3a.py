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
time.sleep(2)
driver.get("https://www.1point3acres.com/bbs")
time.sleep(5)
attachment = 'image.png'
driver.save_screenshot(attachment)
point = driver.find_element_by_id("extcreditmenu").text
print('old point', point)
from selenium.webdriver.common.by import By
#newPoint = point
#needSignOn = True
signNodes = driver.find_elements(By.XPATH, "//*[@id='um']/p[2]/a[3]/font[text()='签到领奖!']")
if len(signNodes) > 0:
    signNode = signNodes[0]
    signNode.send_keys(Keys.ENTER)
    time.sleep(5)
    driver.find_element(By.XPATH, "//*[@id='kx']").click()
    import datetime
    datetime_object = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    signText = '今天把论坛帖子介绍给好基友了~'
    print(signText)
    driver.find_element(By.XPATH, "//*[@id='todaysay']").send_keys(signText)
    driver.find_element(By.XPATH, "//*[@id='qiandao']/p/button").click()
    time.sleep(5)
    newPoint = driver.find_element_by_id("extcreditmenu").text
    pointChange = point + ' -> ' + newPoint + ' : ' + datetime_object
    print('new point', newPoint)
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
	
