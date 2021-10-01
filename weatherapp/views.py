from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests


def get_html_content(city):
    USER_AGENT = 'Chrome/44.0.2403.157'
    LANGUAGE = 'en-US; en; q = 0.5'
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace('', '+')
    html_content = session.get('https://www.google.com/search?q=weather+in+{}'.format(city)).text
    return html_content


def home(request):
    weather_data = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        html_content = get_html_content(city)
        soup = BeautifulSoup(html_content, 'html.parser')
        weather_data = dict()
        weather_data['region'] = soup.find('div', attrs={'id':'wob_loc'}).text
        weather_data['day_time'] = soup.find('div', attrs={'id': 'dts'}).text
        weather_data['weather'] = soup.find('span', attrs={'id': 'wob_dcp'}).text
        weather_data['temperature'] = soup.find('span', attrs={'id': 'wob_t'}).text
    print(weather_data)
    return render(request, 'home.html', {'weather': weather_data})
