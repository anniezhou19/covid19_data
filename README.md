# CS50 FINAL PROJECT TITLE: Covid-19 Tracker

### Video Demo:  <https://youtu.be/q5Avpnln4vg>
### Our github public repository: <https://github.com/anniezhou19/covid19_data.git>

### Description:
#### Covid-19 has badly impacted to our daily life in the whole world and we all suffered more or less from it. That's how the idea comes that to create a web app with live updating datas.
#### Covid-19 Tracker is intended to show the live covid-19 and vaccination statistics around the world combined with live news related to covid-19. It includes the google translator through which user can choose all different languages for the website.
#### This project is completed by both me and my project partner Anurag Choudhary from CS50 facebook community. I have done for the homepage, datatable and vaccination pages, and Anurag  has finished for the news, feedback and register pages.

### Usage:
- Type in command line: flask run
- If you want to give us your feedback and leave a message, then you need to register and login

#### We use config.py and .gitignore to hide our api key in our github public repository

### Features:
- Flask
- SQL

#### We use flask web framework based in Python and manage SQL database with sqlite.

### Explanation of our files:
- application.py: amongst a bunch of imports, there are also helper function for the apology and config which is to save our api key. We create a .gitignore file in our github public repository to hide the config.py and details.db files. The file configures CS50's SQL module to use details.db, user's register information and feedback message will be saved into our database.
- helper.py: implementation of apology.
- config.py: save api key for
- requirements.txt: the packages on which this app will depend.
- detail.db: we need two tables for our database, table users contains user_id, email, hash, username and Primary Key on user_id, table feedback contains id, username, feedback, rating, email, date_time and feedback_id.
- /static: includes styles.css for the style and data.js for google translator function.
- /templates:this file contains all the html pages for the website, and layout.html is to control the view of webpage.

### Our Cooperation:
- Hong Zhou: index.html, data_table.html, vaccination.html, data.js, config.py and related functions in application.py
- Anurag Choudhary: news.html, feedback.html, register.html, login.html and related functions in application.py
- Together: application.py, helper.py, styles.css, layout.html, apology.html, detail.db,


### API for live information about COVID-19

#### GET https://coronavirus-19-api.herokuapp.com/all -> global info
#### GET https://coronavirus-19-api.herokuapp.com/countries -> all countries info
#### https://ourworldindata.org/covid-cases -> daily new confirm chart
#### https://ourworldindata.org/covid-vaccinations -> daily share of people vaccinated against Covid19
#### GET https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json -> global vaccination data
#### GET https://newsapi.org/docs/endpoints/everything -> live coronavirus news

### References
<a id="1">[1]</a>
Mathieu, E., Ritchie, H., Ortiz-Ospina, E. et al. A global database of COVID-19 vaccinations.
Nat Hum Behav (2021). https://doi.org/10.1038/s41562-021-01122-8
<a id="1">[2]</a>
https://github.com/javieraviles/covidAPI
