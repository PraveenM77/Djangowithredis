import requests
from bs4 import BeautifulSoup
import logging
import time
import random

logging.basicConfig(level=logging.INFO)


def get_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com",
        "Accept-Encoding": "gzip, deflate"
    }
    return headers


def fetch_connection(url):
    
    try:
        headers=get_headers()
        response = requests.get(url,headers)
        if response.status_code == 200:
            logging.info("Connected")
            return response.text
        else:
            logging.error(f"Status code is {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Connection Error: {e}")
        return None

def fetch_product_links(url):
    try:
        
        response_text = fetch_connection(url)
        if response_text is None:
            logging.error("Failed to retrieve the page content.")
            return None
        
        soup = BeautifulSoup(response_text, "lxml")
        container = soup.find("div", class_="DOjaWF gdgoEp")
        if not container:
            logging.warning("Product container not found.")
            return None

        target_link = container.find_all('a', class_="VJA3rP")
        if not target_link:
            logging.warning("No product links found.")
            return None

        product_links = ["https://www.flipkart.com" + link["href"] for link in target_link]
        logging.info(f"Found {len(product_links)} product links.")

    except Exception as e:
        logging.error(f" Connection Error: {e}")
        return None
    return product_links

def get_product_name(soup):
    product_name=soup.find("span", class_="VU-ZEz")
    return product_name.text.strip() if product_name else None
    

def get_product_price(soup):
    product_price=soup.find("div", class_="Nx9bqj CxhGGd")
    return float(product_price.text.replace("₹","").replace(",","").strip()) if product_price else None

def get_product_brand(soup):
    product_brand_tag = soup.find("span", class_="VU-ZEz")
    return product_brand_tag.text.strip()[:10] if product_brand_tag else None
"""


def get_product_quantity(soup):
    rows = soup.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        if len(columns) == 2:
            label = columns[0].get_text(strip=True)
            value_list = columns[1].find_all("li")
            if "Quantity" in label:
                if value_list:
                    return value_list[0].get_text(strip=True)
                else:
                    return columns[1].get_text(strip=True)
    return "Quantity not found"

"""

def get_product_quantity(soup):
    rows = soup.find_all("tr", class_="WJdYP6 row")
    if rows:
        for row in rows:
            label = row.find("td", class_="+fFi1w col col-3-12")
            if label and label.text.strip() == "Quantity":
                quantity_td = row.find("td", class_="Izz52n col col-9-12")
                quantity = quantity_td.find("li", class_="HPETK2")
                return quantity.text.strip() or "Quantity is not listed"
    return "Quantity not found"
    
url = "https://www.flipkart.com/search?q=skin+products&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"
product_links=fetch_product_links(url)

if product_links:
    for product in product_links:
        response_text=fetch_connection(product)
        soup=BeautifulSoup(response_text,"lxml")
        time.sleep(random.uniform(2, 3))
        print(get_product_name(soup))
        print(get_product_price(soup))
        print(get_product_brand(soup))
        print(get_product_quantity(soup))
       


