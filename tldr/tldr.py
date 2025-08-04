from transformers import pipeline

from bs4 import BeautifulSoup as bs
import requests

from time import sleep
import os

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def good_request(code):
    if code == 200:
        return True
    elif code == 404:
        print("This url does not exist.")
        sleep(1)
        return False
    else:
        print("This url failed.")
        sleep(1)
        return False

def get_url():
    while True:
        clear_console()
        url = f"https://www.bbc.com/news/articles/{input('BBC article ID: ')}"
        code = requests.get(url).status_code

        if good_request(code):
            clear_console()
            return url

def scrape(url):
    response = requests.get(url)
    code = response.status_code
    
    if good_request(code): 
        soup = bs(response.text, "html.parser")
        return soup
    else:
        raise RuntimeError
    
def get_news(soup):
    article = soup.find("article")
    blocks = article.find_all("p", {"class": ["sc-9a00e533-0", "hxuGS"]})

    news = " ".join(block.text for block in blocks)

    return news

def summarize(news):
    model = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")
    summary = model(news, max_length=150, min_length=50)

    return summary[0]["summary_text"]

def finish(summary):
    clear_console()
    sentences = summary.strip().split(" .")
    summary = ".".join(sentences)
    print(summary)

    input("Press Enter to continue... ")

def main():
    url = get_url()
    soup = scrape(url)
    news = get_news(soup)
    summary = summarize(news)
    finish(summary)

if __name__ == "__main__":
    main()