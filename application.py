import os
import pandas as pd
import json
import csv
from flask import Flask, flash, redirect, render_template, request, session
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    # general report
    url_global = "https://coronavirus-19-api.herokuapp.com/all"
    response1 = requests.request("GET", url_global)
    global_info = json.loads(response1.text)

    # data table
    url_countries = "https://coronavirus-19-api.herokuapp.com/countries"
    response2 = requests.request("GET", url_countries)
    countries_info = json.loads(response2.text)

    return render_template("index.html", global_info=global_info)

@app.route("/data_table")
def data_table():
    # data table
    url_countries = "https://coronavirus-19-api.herokuapp.com/countries"
    response2 = requests.request("GET", url_countries)
    countries_info = json.loads(response2.text)

    return render_template("data_table.html", countries_info=countries_info)

@app.route("/vaccination")
def vaccination():
    url_vaccination = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"
    response3 = requests.request("GET", url_vaccination)
    vaccin_info = json.loads(response3.text)
    return render_template("vaccination.html", vaccin_info=vaccin_info)