from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from scrape_bbcHeadlines import Base, Headline
from models import Headline

app = Flask(__name__)

# Database setup (replace with your database URL)
db_url = 'sqlite:///bbc_news.db'  # Replace with your actual database URL
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

# Define the Headline model
class Headline(Base):
    __tablename__ = 'headlines'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    timestamp = Column(DateTime)

# Route for the homepage (date selection form)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_date = request.form.get('date')
        
        # Convert the selected_date string to a datetime object
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')

        # Query the database to get headlines for the selected date
        with Session() as session:
            headlines = session.query(Headline).filter(Headline.timestamp >= selected_date, Headline.timestamp < selected_date + timedelta(days=1)).all()

        return render_template('headlines.html', selected_date=selected_date, headlines=headlines)
    return render_template('index.html')

# Route for displaying headlines based on selected date
@app.route('/headlines', methods=['GET', 'POST'])
def display_headlines():
    if request.method == 'POST':
        selected_date = request.form.get('date')

        # Convert the selected_date string to a datetime object
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')

        # Query the database to get headlines for the selected date
        with Session() as session:
            headlines = session.query(Headline).filter(Headline.timestamp >= selected_date, Headline.timestamp < selected_date + timedelta(days=1)).all()

        return render_template('headlines.html', selected_date=selected_date, headlines=headlines)
    return redirect('/')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
