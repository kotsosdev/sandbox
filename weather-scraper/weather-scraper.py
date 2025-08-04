import requests
from bs4 import BeautifulSoup as bs

class Forecast:
    def __init__(self, temp, conds, w_speed, hum, hours):
        self.temp = temp
        self.conds = conds
        self.hours = hours
        self.w_speed = w_speed
        self.hum = hum

    def __str__(self):
        if self.hours == 0:
            title = 'Right Now:'
        elif self.hours == 1:
            title = 'In an Hour:'
        else:
            title = f'In {self.hours} Hrs:'

        return f"""\
{title}
    • Temperature: {self.temp}
    • Conditions: {self.conds}
    • Wind Speed: {self.w_speed}
    • Humidity: {self.hum}"""

def get_url():
    return 'https://www.timeanddate.com/weather/@4905259/hourly'

def scrape(url):
    response = requests.get(url)
    if response.status_code != 200: 
        print('Scrape failed!')
        return None

    return bs(response.content, 'html.parser')

def condition_split(raw):
    conds = raw[:-1].split('.')
    return ', '.join(cond.strip() for cond in conds)

def get_weather(soup):
    forecast = []
    table = soup.find('table', class_='zebra tb-wt fw va-m tb-hover')
    i = 0

    for row in table.find_all('tr'):
        cells = row.find_all('td')

        if len(cells) >= 3:
            hourly_forecast = Forecast(
                temp=cells[1].text.strip(),
                conds=condition_split(cells[2].text.strip()),
                w_speed=cells[4].text.strip(),
                hum=cells[6].text.strip(),
                hours=i
            )

            forecast.append(hourly_forecast)
            i += 1

    return forecast

def main():
    url = get_url()
    soup = scrape(url)
    hours = get_weather(soup)
    for hour in hours: print(hour)

if __name__ == '__main__':
    main()