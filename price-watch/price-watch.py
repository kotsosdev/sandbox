from bs4 import BeautifulSoup as bs
import requests
from time import sleep
from random import choice, uniform

from utils import clear_console, timestamp, log, json_load, json_save

def get_soups(urls):
    headers_list = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us",
            "Connection": "keep-alive",
            "Referer": "https://www.apple.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Referer": "https://www.reddit.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.instagram.com/"
        },
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://news.ycombinator.com/",
            "Connection": "keep-alive"
        }
    ]

    soups = []
    timestamps = []
    for url in urls:
        headers = choice(headers_list)
        delay = uniform(3,6)
        sleep(delay)

        try: 
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                log(f"Non-200 status code. {response.status_code}, {url}")

                soups.append(None)
                timestamps.append(timestamp())
                continue
            
        except ConnectionResetError:
            log(f"Request blocked. {url}")

            soups.append(None)
            timestamps.append(timestamp())
            continue
        
        except ConnectionError:
            log(f"No connection. {url}")

            soups.append(None)
            timestamps.append(timestamp())
            continue

        except Exception as e:
            log(f"Failed to fetch response. {e}, {url}")

            soups.append(None)
            timestamps.append(timestamp())
            continue
        
        soup = bs(response.content, "html.parser")
        soups.append(soup)
        timestamps.append(timestamp())

    return soups, timestamps

def find_prices(soups):
    prices = []
    for soup in soups:
        if not soup:
            prices.append(None)
            continue

        pricebox = soup.find("span", {"class": "a-price aok-align-center reinventPricePriceToPayMargin priceToPay"})

        if pricebox:
            dollars = pricebox.find("span", class_="a-price-whole")
            cents = pricebox.find("span", class_="a-price-fraction")

        else:
            log("Failed to find pricebox. Possible junk page.")
            prices.append(None)
            continue

        if dollars and cents:
            dollars = dollars.text.strip(". ")
            cents = cents.text.strip(". ")

            try:
                str_price = f"{dollars}.{cents}"
                price = float(str_price.replace(",", ""))
                prices.append(price)
            except ValueError:
                log(f"Failed to create price float. {str_price}")
                prices.append(None)

        else:
            log("Failed to find price in soup.")
            prices.append(None)

    return prices

def find_sales(soups):
    sales = []
    for soup in soups:
        if not soup:
            sales.append(None)
            continue

        sale = soup.find("span", {"aria-hidden": "true", "class": ["savingsPercentage"]}) 

        if sale:
            try:
                sale = sale.text.strip("-% ")
                sale = float(sale) / 100
                sales.append(sale)
            except (TypeError, ValueError):
                log(f"Failed to create sale float. {sale}")
                sales.append(None)
        
        else:
            sales.append(0.0)

    return sales

def add_snaps(data, prices, sales, timestamps):
    if not (len(data) == len(prices) == len(sales) == len(timestamps)):
        log("Collected data was not the same length.")
        return None

    snapshots = []
    for price, sale, time in zip(prices, sales, timestamps):
        snapshot = {
            "price": price,
            "sale": sale if price is not None else None,
            "timestamp": time
        }
        snapshots.append(snapshot)

    for info, snapshot in zip(data.values(), snapshots):
        info["snapshots"].append(snapshot)

    return data

def main():
    clear_console()
    data = json_load()
    soups, timestamps = get_soups(list(data))

    prices, sales = find_prices(soups), find_sales(soups)
    add_snaps(data, prices, sales, timestamps)

    if json_save(data):
        log("Saved data as json. :D")
    else:
        log(f"Unserializable object encountered.")

if __name__ == "__main__":
    main()