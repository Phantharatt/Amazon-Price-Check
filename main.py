import requests
from bs4 import BeautifulSoup
import smtplib
import os
import time
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

URL = "https://www.amazon.com/MSI-GeForce-RTX-3060-12G/dp/B08WPRMVWB"
#My HTTP  Header
header = {
    "Accept-Language":"en-US,en;q=0.5"
}
def scapping_amazon_price():
    response = requests.get(URL,headers=header)
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")

    print(soup.prettify())

    price = soup.find(name="span",class_="a-price").get_text().strip()
    price = float(price.split("$")[1])

    product_title = soup.find(name="span",id="productTitle").get_text()
    # print(price)
    # print(product_title)
    return price,product_title

data = scapping_amazon_price()

#send email
def check_target_price(price , product_title):
    smtp_address = os.environ.get("SMTP_ADDRESS")
    user_email = os.environ.get("EMAIL_ADDRESS")
    user_password = os.environ.get("EMAIL_PASSWORD")
    email_target = os.environ.get("EMAIL_TARGET")
    
    mail = (f"Subject:AMAZON PRICE ALERT \n\n{product_title} \n\nNow Price: \n {price} \n\nLet's go to buy it in Amazon. \n\n{URL}")
    
    while True:
        price_target =  310 #usd
        check_per_hour = 3600 #3600 = 1h
        current_time = datetime.now().strftime("%d/%m/%y  %H:%M:%S")
        print(f"--- Amazon Price Tracker --- \nTime: {current_time} \nProduct Name: {product_title}\nCurrect Price: {price} usd")
        if price <= price_target:
            with smtplib.SMTP(smtp_address, port=587) as connection:
                connection.starttls()
                connection.login(user=user_email,password=user_password)
                connection.sendmail(user_password,email_target, mail)
                print("Sent Email Complete :)")
            break #exit loop after sent mail
        else:
            print(f"Target price: {price_target} usd\n")
        time.sleep(check_per_hour)

check_target_price(data[0],data[1])

