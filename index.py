 #!/usr/bin/python3.5.1
from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
import datetime
import os
import json
import time
import urllib2

app = Flask(__name__)

def get_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=10&units=metric&APPID=c2241ec238defba0f521309a842348f1'.format(city)
    response = urllib2.urlopen(url).read()
    return response

@app.route("/")
def index():
    searchcity = request.args.get("searchcity")

    if not searchcity:
        searchcity = request.cookies.get('last_city')

    if not searchcity:
        searchcity = 'London'

    data = json.loads(get_weather(searchcity))

    try:
        city = data['city']['name']
    except KeyError:
        return render_template('invalid_city.html', user_input=searchcity)

    country = data['city']['country']
    forecast_list = []

    for d in data.get('list'):
        day = time.strftime('%d %B', time.localtime(d.get('dt')))
        mini = d.get('temp').get('min')
        maxi = d.get('temp').get('max')
        description = d.get('weather')[0].get('description')
        forecast_list.append((day, mini, maxi, description))

    response = make_response(render_template('index.html', forecast_list=forecast_list, city=city, country=country))

    if request.args.get('remember'):
        response.set_cookie("last_city", "{},{}".format(city, country), expires=datetime.datetime.today() + datetime.timedelta(days=365))
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    app.run(host='0.0.0.0', port=port, debug=True)