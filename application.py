#imports    

from flask import Flask, redirect, render_template,session
from flask import request as http_request
from flask.helpers import flash
from flask_session import Session
from tempfile import mkdtemp
import json
from requests import request
import os
import datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import operator
from helper import apology
from cs50 import SQL


#parameters realted to apis
API_KEY="b6f642c5ac2a40a5b3483ab45738aeaf"
base_url="https://newsapi.org/v2/everything"

#for fedding date_time in sql db
date_time_now=datetime.datetime.now().replace(microsecond=0)
#calculating todays date and day before yesterday
end_day=datetime.date.today()
day_gap=datetime.timedelta(days=5)
start_day= end_day - day_gap


# configuring flask app
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#configuring sql db through cs50
db=SQL("sqlite:///details.db")

#configuring api_key



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

  

@app.route("/login",methods=["POST","GET"])
def login():

    session.clear()
    #if users visit through form
    if http_request.method=="POST":

        #taking email and password from users
        email=http_request.form.get("email")
        password=http_request.form.get("password")

        #checking if they have entered usrename or password or not.,
        if not email:
            return apology("must provide email", 403)
        elif not password:
            return apology("must provide password", 403)

        #searching database for user email
        row=db.execute("SELECT * FROM users WHERE email = ?", email)
        print(row)
        #checking if user entered right password or username exists or not
        if len(row) != 1 or not check_password_hash(row[0]["hash"],password):
            return apology("invalid username or password")

        #remebering the logged in user_id and username
        session["user_id"]=row[0]["user_id"]
        session["username"]=row[0]["username"]

        flash("sucessfully logged in!!")
        return redirect("/feedback")
    # if user visits through link or redirect
    return render_template("login.html")


#logging out route 
@app.route("/logout")
def logout():
    #clearing any session data
    session.clear()
    flash("logged out")
    return redirect("/")

# route for register
@app.route("/register",methods=["GET", "POST"])
def register():
    
#if user visits through submitting form
    if http_request.method=="POST":

        #taking all users input
        username = http_request.form.get("username")
        email = http_request.form.get("email")
        password = http_request.form.get("password")
        confirm_pass = http_request.form.get("confirmation")

        #checking if users have provided input or not
        if not username:
            return apology("must provide username", 403)
        elif not email:
            return apology("must provide email", 403)
        elif not password:
            return apology("must provide password", 403)

        #chceking if users have entered same password or not
        elif password!=confirm_pass:
            return apology("password and confirmation must be the same", 403)

        #checking if username is availiabe or not
        rows=db.execute("SELECT * FROM users WHERE email = ?",email)
        if len(rows) != 0:
            return apology("Email already exists")

        #adding users into database and storing passwords as hash not actual password
        db.execute("INSERT INTO users(username,hash, email) VALUES(?,?,?)", username, generate_password_hash(password), email)
        # making users login just by registring 
        row=db.execute("SELECT * FROM users WHERE email=?",email)

       # storinf user user_id and username in feedback
        session["user_id"]=row[0]["user_id"]
        session["username"]=row[0]["username"]

        #redirecting users to login page
        flash("registered sucessful")
        return redirect("/feedback")
    return render_template("register.html")


#route for feedback form
@app.route("/feedback", methods=["GET", "POST"])
def feedback():

    #queying db for all prevoius feedbacks
    feedback_all=db.execute("SELECT feedback,date_time,username,rating FROM feedback ")
    print(feedback_all)
    #sorting them on the basis of date and time
    feedback_all.sort(key=operator.itemgetter("date_time"))

    #if users posts feedback 
    if http_request.method=="POST":
        
        #checking if user_id is in session or not i.e he is logged in or not
        if session.get("user_id") is None:
            return redirect("/login")
        
        #getting user rating
        rating=http_request.form["option"]
        
            
        # getting feedback from users
        feedback=http_request.form["feedback"]
        

        #checking whether users provide feedback and rating or not
        if not feedback:
            return apology("provide feedbck",403)
        if not rating:
            return apology("provide rating",403)

        #for fedding date_time in sql db
        date_time_now=datetime.datetime.now().replace(microsecond=0)
        
        # also taking user_id and username ffrom session for
        db.execute("INSERT INTO feedback (feedback,rating,date_time,username,id) VALUES(?,?,?,?,?)",feedback,rating,date_time_now,session.get("username"),session.get("user_id"))
        flash("Posted feedback")
        return redirect("/feedback")

    return render_template("feedback.html",feedback_all=feedback_all)

if __name__ == '__main__':
    app.run(debug=True)