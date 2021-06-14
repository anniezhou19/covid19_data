import json
import requests

url_global = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"
response1 = requests.request("GET", url_global)
global_info = json.loads(response1.text)
print(global_info[0]["data"][-1])
