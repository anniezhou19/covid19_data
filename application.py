#imports    

from flask import Flask, redirect, render_template, request
import json
from requests import request
import os
import datetime

#parameters realted to apis
API_KEY=os.getenv("API_KEY")
base_url="https://newsapi.org/v2/everything"

#calculating todays date and day before yesterday
end_day=datetime.date.today()
two_day=datetime.timedelta(days=5)
start_day= end_day - two_day

# configuring flask app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

#setting up routes
@app.route("/")
def index():
    # general report
    url_global = "https://coronavirus-19-api.herokuapp.com/all"
    response1 = request("GET", url_global)
    global_info = json.loads(response1.text)

    # data table
    url_countries = "https://coronavirus-19-api.herokuapp.com/countries"
    response2 = request("GET", url_countries)
    countries_info = json.loads(response2.text)

    return render_template("index.html", global_info=global_info)

@app.route("/data_table")
def data_table():
    # data table
    url_countries = "https://coronavirus-19-api.herokuapp.com/countries"
    response2 = request("GET", url_countries)
    countries_info = json.loads(response2.text)

    return render_template("data_table.html", countries_info=countries_info)

@app.route("/vaccination")
def vaccination():
    url_vaccination = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"
    response3 = request("GET", url_vaccination)
    vaccin_info = json.loads(response3.text)
    return render_template("vaccination.html", vaccin_info=vaccin_info)

# route for news 
@app.route("/news")
def news():
    
    #APi for covid  and vaccination news
   
    url_news= f"{base_url}?qInTitle=+vaccination%20AND%20+coronavirus&from={end_day}&to={start_day}&sortBy=popularity,relevancy&apiKey={API_KEY}&language=en&pageSize=12"
    #calling api to get response and converting into json format
    response_news_covid=request("GET",url_news)
    data=response_news_covid.json()

    #sending the data to fronttend
    news_data_covid=data["articles"]
    return render_template("news.html",news_data_covid=news_data_covid)

   # f"{base_url}?qInTitle=+vaccination%20AND%20+coronavirus&from=2021-05-15&to=2021-05-17&sortBy=popularity,relevancy&apiKey={API_KEY}&language=en&pageSize=12"


#route for feedback form
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")