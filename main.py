import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.amazon.com/MSI-GeForce-RTX-3060-12G/dp/B08WPRMVWB"
# Write your code below this line 👇

#My HTTP  Header
header = {
    "Accept-Language":"en-US,en;q=0.5"
}

response = requests.get(URL,headers=header)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

print(soup.prettify())

price = soup.find(name="span",class_="a-price").get_text().strip()
price = float(price.split("$")[1])

product_title = soup.find(name="span",id="productTitle").get_text()
# print(price)
# print(product_title)

#send email

smtp_address = os.environ.get("SMTP_ADDRESS")
user_email = os.environ.get("EMAIL_ADDRESS")
user_password = os.environ.get("EMAIL_PASSWORD")
email_target = os.environ.get("EMAIL_TARGET")
mail = (f"Subject:AMAZON PRICE ALERT \n\n{product_title} \n\nNow Price: \n {price} \n\nLet's go to buy it in Amazon. \n\n{URL}")
if price < 320:
    with smtplib.SMTP(smtp_address, port=587) as connection:
        connection.starttls()
        connection.login(user=user_email,password=user_password)
        connection.sendmail(user_password,email_target, mail)
        print("Sent Email Complete :)")
