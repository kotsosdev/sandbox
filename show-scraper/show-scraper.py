from bs4 import BeautifulSoup as bs
import requests as reqs

class Show:
    def __init__(self, title, month, day, desc):
        self.title = title
        self.month = month
        self.day = day
        self.desc = desc

    def __str__(self):
        return (
            f'{self.title}\n'
            f'  • Most recent episode: {self.month} {self.day}\n'
            f'  • Description: {self.desc}'
        )
    
    @classmethod
    def from_html(cls, container):
        title = container.find('span', {'class': 'p--small', 'data-qa': 'discovery-media-list-item-title'}).text.strip()

        recent_ep_date = container.find('span', {'class': 'smaller', 'data-qa': 'discovery-media-list-item-start-date'}).text.strip()[16:]
        month, day = recent_ep_date.split()
        day = int(day)

        url = get_url(1, title)
        soup = scrape(url)

        try: 
            desc = soup.find('rt-text', {'data-qa': 'synopsis-value'}).text.strip()
        except AttributeError: 
            desc = None

        return cls(title, month, day, desc)

def get_url(i, title=''): 
    link_title = ''
    if i == 1:
        for char in title.lower():
            if char.isalnum():
                link_title += char
            elif char == ' ':
                link_title += '_'

    urls = [
        'https://www.rottentomatoes.com/browse/tv_series_browse/sort:popular',
        f'https://www.rottentomatoes.com/tv/{link_title}'
    ]
    return urls[i]

def scrape(url):
    res = reqs.get(url)
    if res.status_code == 200: 
        html = res.text
    else:
        print('Failed to get response.')

    soup = bs(html, 'html.parser')
    
    return soup

def get_shows(soup):
    containers = soup.find_all('div', {'class': 'flex-container'})
    shows = [
        Show.from_html(container) 
        for container in containers
    ]

    return shows

def print_movies(shows_info):
    for show in shows_info: 
        print(show.title)

def main():
    url = get_url(0)
    soup = scrape(url)
    shows = get_shows(soup)
    for show in shows: print(f'{show}\n')

if __name__ == '__main__':
    main()