import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.26 Safari/537.36'

header = {'user-agent': user_agent}

host = 'https://maoyan.com'

myurl = host + '/films?showType=3'

response = requests.get(myurl, headers=header)

bs_info = bs(response.text, 'html.parser')


def getMovieDetail(url):
    detailUrl = host + url
    detail_header = {'user-agent': user_agent, 'referer': myurl}
    response = requests.get(detailUrl, headers=detail_header)
    movie_detail = bs(response.text, 'html.parser')
    divtag = movie_detail.find_all(
        'div', attrs={'class': 'movie-brief-container'})[0]
    movie_name = divtag.find_all('h1', attrs={'class': 'name'})[0].text
    lutag = divtag.find_all('ul')[0]
    category = ''
    for atag in lutag.find_all('li')[0].find_all('a'):
        s = atag.text.replace(' ', '')
        category = category + s + ' '
    showtime = lutag.find_all('li')[2]
    return {'name': movie_name, 'category': category, 'showtime': showtime.text}


movie_count = 10

movie_list = []

for itag in bs_info.find_all('div', attrs={'class': 'movie-item-hover'}):
    for atag in itag.find_all('a'):
        if movie_count < 1:
            break
        movie_detail = getMovieDetail(atag.get('href'))
        movie_list.append(movie_detail)
        movie_count -= 1

movie_db = pd.DataFrame(data=movie_list)

movie_db.to_csv('./movie_db.csv', encoding='utf8', index=False, header=False)
