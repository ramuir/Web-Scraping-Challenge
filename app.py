from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from splinter import Browser
import pandas as pd 

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    mars_facts = mongo.db.mars_facts.find_one()
    return render_template("index.html", mars_facts=mars_facts)


@app.route("/scrape")
def scrapers():
    mars_facts = mongo.db.mars_facts
    mars_scrape = scrape_mars.scrape()
    mars_facts.update({}, mars_scrape, upsert=True)
   
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)