
import requests
from bs4 import BeautifulSoup
import random
import time
import logging
from datetime import datetime


logging.basicConfig(level=logging.INFO)


def get_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com",
        "Accept-Encoding": "gzip, deflate"
    }
    return headers


def fetch_html_response(url, headers):
    try:
        with requests.session() as session:
            response = session.get(url, headers=headers)
            response.raise_for_status()  
            return response.text
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP error occurred: {errh}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Error occurred: {err}")
    return None


def extract_product_links(url, headers):
    response_text = fetch_html_response(url, headers)
    if response_text:
        soup = BeautifulSoup(response_text, "lxml")
        container = soup.find("div", class_="DOjaWF gdgoEp")
        products_links = container.find_all("a", class_="wjcEIp")
        return ["http://www.flipkart.com" + product["href"] for product in products_links] if products_links else []
    return []


def get_products_name(soup):
    product_name_tag = soup.find("span", class_="VU-ZEz")
    return product_name_tag.text.strip() if product_name_tag else None


def get_product_price(soup):
    product_price_tag = soup.find("div", class_="Nx9bqj CxhGGd")
    if product_price_tag:
        return product_price_tag.text.replace("₹", "").replace(",", "").strip() or "Price not available"
    return "Price not available"


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


def get_product_brand(soup):
    product_brand_tag = soup.find("span", class_="B_NuCI")
    return product_brand_tag.text.strip() if product_brand_tag else None


def get_product_highlights(soup):
    product_highlights_container = soup.find("div", class_="xFVion")
    if product_highlights_container:
        product_highlights = product_highlights_container.find_all("li")
        return [highlight.text.strip() for highlight in product_highlights] if product_highlights else []
    return []


def get_product_description(soup):
    product_description = soup.find("div", class_="yN+eNk w9jEaj")
    return product_description.text.strip() if product_description else None


def get_product_skin_type(soup):
    rows = soup.find_all("tr", class_="WJdYP6 row")
    if rows:
        for row in rows:
            label = row.find("td", class_="+fFi1w col col-3-12")
            if label and label.text.strip() == "Skin Type":
                skin_type_td = row.find("td", class_="Izz52n col col-9-12")
                if skin_type_td:
                    skin_type = skin_type_td.find("li", class_="HPETK2")
                    return skin_type.text.strip() or "Skin Type not listed"
    return "Skin Type not found"

def fetch_product_details(product_url, headers):
    response_text = fetch_html_response(product_url, headers)
    if response_text:
        soup = BeautifulSoup(response_text, "lxml")
        product_details = {
            "name": get_products_name(soup),
            "price": get_product_price(soup),
            "brand": get_product_brand(soup),
            "quantity": get_product_quantity(soup),
            "skin_type": get_product_skin_type(soup),
            "highlights": get_product_highlights(soup),
            "description": get_product_description(soup)
        }
        return product_details
    else:
        logging.error(f"Failed to fetch product page for link: {product_url}")
    return None


from concurrent.futures import ThreadPoolExecutor, as_completed

def get_all_product_details():
    headers = get_headers()
    url = "https://www.flipkart.com/search?q=beauty%20products&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    product_links = extract_product_links(url, headers)
    if not product_links:
        logging.warning("No product links found.")
        return []

    all_product_details = []

    def fetch_with_delay(url):
        time.sleep(random.uniform(1, 2))  
        return fetch_product_details(url, headers)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_with_delay, link) for link in product_links]

        for future in as_completed(futures):
            try:
                product_details = future.result()
                if product_details:
                    all_product_details.append(product_details)
                    logging.info(f"Fetched: {product_details['name']}")
            except Exception as e:
                logging.error(f"Exception during fetching: {e}")

    return all_product_details




start_time=datetime.now()
p=get_all_product_details()
end_time=datetime.now()
print(p)
print("Tike taken for the scraping the data ",end_time-start_time)
print(len(p))


"""
   
    def get_all_product_details():
    headers = get_headers()
    url = "https://www.flipkart.com/search?q=beauty%20products&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    
    product_links = extract_product_links(url, headers)
    if not product_links:
        logging.warning("No product links found.")
        return []

    all_product_details = []
    for product_url in product_links:
        time.sleep(random.uniform(5, 7))
        product_details = fetch_product_details(product_url, headers)
        if product_details:
            all_product_details.append(product_details)
            logging.info(f"Fetched details for: {product_details['name']}")
        else:
            logging.error(f"Failed to fetch details for: {product_url}")
    
    return all_product_details

""" 