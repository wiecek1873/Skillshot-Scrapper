import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.com/s?k=python+programming+books"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

products = soup.find_all("div", class_="s-result-item")
for product in products:
    title = product.find("h2").text.strip()
    price = product.find("span", class_="a-offscreen")
    if price:
        price = price.text.strip()
    else:
        price = "Price not available"
    print(f"Title: {title}\nPrice: {price}\n")