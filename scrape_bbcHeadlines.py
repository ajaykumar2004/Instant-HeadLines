import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import signal
import sys

from models import Headline  # Import the Headline model from the models module

# Import the sqlalchemy module and create Base
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# Create the database engine and session
engine = create_engine('sqlite:///bbc_news.db')
Session = sessionmaker(bind=engine)

# Function to scrape headlines from BBC News
def scrape_bbc_news():
    url = 'https://www.bbc.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')
    
    # Store headlines in the database
    with Session() as session:
        for headline in headlines:
            title = headline.text.strip()
            timestamp = datetime.now()
            new_headline = Headline(title=title, timestamp=timestamp)
            session.add(new_headline)
        session.commit()

# Run the scraper script once
scrape_bbc_news()

# Handle script termination (Ctrl+C)
def stop_script(signum, frame):
    print("Stopping the script...")
    sys.exit(0)

signal.signal(signal.SIGINT, stop_script)
