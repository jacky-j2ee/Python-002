import requests
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup as bs

USER_AGENT_LIST=[
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
import random
user_agent = random.choice(USER_AGENT_LIST)

header = {'user-agent': user_agent}

host = 'https://maoyan.com'

myurl = host + '/films?showType=3'

response = requests.get(myurl, headers=header)

bs_info = bs(response.text, 'html.parser')

def getMovieDetail(url):
    detailUrl = host + url
    user_agent = random.choice(USER_AGENT_LIST)
    detail_header = {'user-agent': user_agent, 'referer': myurl}
    response = requests.get(detailUrl, headers=detail_header)
    movie_detail = bs(response.text, 'html.parser')
    divtag = movie_detail.find_all(
        'div', attrs={'class': 'movie-brief-container'})[0]
    movie_name = divtag.find_all('h1', attrs={'class': 'name'})[0].text
    ultag = divtag.find_all('ul')[0]
    category = ''
    for atag in ultag.find_all('li')[0].find_all('a'):
        s = atag.text.replace(' ', '')
        category = category + s + ' '
    showtime = ultag.find_all('li')[2]
    return {'name': movie_name, 'category': category, 'showtime': showtime.text}

movie_count = 10

movie_list = []

for itag in bs_info.find_all('div', attrs={'class': 'movie-item-hover'}):
    for atag in itag.find_all('a'):
        if movie_count < 1:
            break
        movie_detail = getMovieDetail(atag.get('href'))
        sleep(3)
        movie_list.append(movie_detail)
        movie_count -= 1

movie_db = pd.DataFrame(data=movie_list)

movie_db.to_csv('./movie_db.csv', encoding='utf8', index=False, header=False)
