from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from database import db
from titlecase import titlecase
import requests
from bs4 import BeautifulSoup
import random
import re
import time
import urllib.parse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

def make_flipkart_url(query):
    encoded_query = urllib.parse.quote(query)
    return f"https://www.flipkart.com/search?q={encoded_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

def make_amazon_url(query):
    encoded_query = urllib.parse.quote(query)
    return f"https://www.amazon.in/s?k={encoded_query}"

def make_zara_url(query):
    return f"https://www.zara.com/in/en/search?searchTerm={urllib.parse.quote(query)}"

def make_hm_url(query):
    encoded_query = urllib.parse.quote_plus(query)
    return f"https://www2.hm.com/en_in/search-results.html?q={encoded_query}"

def fetch_product_info(choice, site):
    if site == 'amazon':
        return fetch_from_amazon(choice)
    elif site == 'flipkart':
        return fetch_from_flipkart(choice)
    elif site == 'hm':
        return fetch_from_hm(choice)
    elif site == 'zara':
        return fetch_from_zara(choice)
    else:
        return []


def fetch_from_hm(query):
    search_url = make_hm_url(query.lower())
    print(f"Fetching from HM ... with this url: {search_url}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    items = soup.select('article.f02d6c')
    products = []
    for item in items[:15]:
        div_tag = item.select_one('div.bb9826')
        image_tag = None
        if div_tag:
            span_tag = div_tag.select_one('span')
            if span_tag:
                image_tag = span_tag.select_one('img')
        image_tag = item.select_one('img')
        image_url = "https://via.placeholder.com/150"
        if image_tag:
            if 'src' in image_tag.attrs:
                image_url = image_tag['src']
            elif 'data-src' in image_tag.attrs:
                image_url = image_tag['data-src']
            elif 'data-srcset' in image_tag.attrs:
                srcset = image_tag['data-srcset']
                image_url = srcset.split(",")[-1].split()[0]
            elif 'srcset' in image_tag.attrs:
                srcset = image_tag['srcset']
                image_url = srcset.split(",")[-1].split()[0]
        title_tag = item.select_one('h3.fe9348')
        title = title_tag.text.strip() if title_tag else ""
        price_tag = item.select_one('span.e7d91d')
        price = price_tag.text.strip() if price_tag else "₹799"

        print(f"{title} .......... {image_url} .......... {price}")

        products.append({
            "name": title,
            "title": title,
            "description": title,
            "price": price,
            "rating": str(round(random.uniform(3.0, 5.0), 1)),
            "delivery": f"Delivery by {random.randint(2, 5)} days",
            "image": image_url
        })

    random.shuffle(products)
    return products[:10]


def fetch_from_zara(query):
    search_url = make_zara_url(query.lower())
    print(f"Fetching from Zara ... with this url: {search_url}")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    items = soup.select('section.product-grid > ul > li')
    if items:
        print("Something there.")
    else:
        print("No items found.")
    products = []
    for item in items[:50]:
        title_tag = item.select_one('div.product-grid-product-info__main-info > a > h3')
        image_tag = item.select_one('img.media-image__image.media__wrapper--media')
        image_url = "https://via.placeholder.com/150"
        if image_tag:
            if 'src' in image_tag.attrs:
                image_url = image_tag['src']
            elif 'data-src' in image_tag.attrs:
                image_url = image_tag['data-src']
        title_one = title_tag.text.strip() if title_tag else ""
        title = titlecase(title_one)
        price_tag = item.select_one('span.money-amount__main')
        price = price_tag.text.strip() if price_tag else "₹799"

        print(f"{title} .......... {image_url} .......... {price}")

        products.append({
            "name": title,
            "title": title,
            "description": title,
            "price": price,
            "rating": str(round(random.uniform(3.0, 5.0), 1)),
            "delivery": f"Delivery by {random.randint(2, 5)} days",
            "image": image_url
        })

    random.shuffle(products)
    return products[:50]


def fetch_from_flipkart(query):
    search_url = make_flipkart_url(query.lower())
    print(f"Fetching from flipkart ... with this url: {search_url}")
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    items = soup.select('div._1sdMkc.LFEi7Z')
    products = []
    for item in items[:15]:
        image = item.select_one('img._53J4C-')
        title_tag = item.select_one('a.WKTcLC.BwBZTg')
        price_tag = item.select_one('div.Nx9bqj')

        title = title_tag.text.strip() if title_tag else ""
        image_url = image['src'] if image and 'src' in image.attrs else "https://via.placeholder.com/150"
        price = price_tag.text.strip() if price_tag else "₹799"

        print(f"{title} .......... {image_url} .......... {price}")

        products.append({
            "name": title,
            "title": title,
            "description": title,
            "price": price,
            "rating": str(round(random.uniform(3.0, 5.0), 1)),
            "delivery": f"Delivery by {random.randint(2, 5)} days",
            "image": image_url
        })

    random.shuffle(products)
    return products[:10]


def fetch_from_amazon(query):
    search_url = make_amazon_url(query.lower())
    print(f"Fetching from Amazon... {search_url}")
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    items = soup.select('div.s-widget-container')
    products = []
    for item in items[:15]:
        a_tag = item.select_one('h2.a-size-base-plus')
        title_tag = a_tag.select_one('span') if a_tag else None
        price_tag = item.select_one('span.a-price-whole')
        image = item.select_one('img.s-image')

        title = title_tag.text.strip() if title_tag else ""
        price = price_tag.text.strip() if price_tag else "₹899"
        image_url = image['src'] if image and 'src' in image.attrs else "https://via.placeholder.com/150"

        print(f"{title} .......... {image_url} .......... {price}")

        products.append({
            "name": title,
            "title": title,
            "description": title,
            "price": price,
            "rating": str(round(random.uniform(3.0, 5.0), 1)),
            "delivery": f"Delivery by {random.randint(2, 5)} days",
            "image": image_url
        })

    random.shuffle(products)
    return products[:10]