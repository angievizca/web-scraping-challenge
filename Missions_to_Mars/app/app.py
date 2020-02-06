from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars


app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/marsdb"
mongo=PyMongo(app)

@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template("index", mars=mars)

@app.route('/scrape')
def scrape():
    mars=mongo.db.mars
    mars_data=scrape_mars.scrape_all()
    mars.update({},mars_data, upsert=True)
    return "scraping sucessful!"

if __name__=="__main__":
    app.run()


