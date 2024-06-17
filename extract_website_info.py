import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
# from gensim.corpora import Dictionary
# from gensim.models import LdaModel
from nltk.corpus import stopwords  # For stop word removal
from nltk.stem import WordNetLemmatizer  # For lemmatization
from nltk.tokenize import word_tokenize  # For word tokenization
import nltk  # Make sure you have nltk installed: `pip install nltk`
import numpy as np  # For NumPy's array functions


nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


def extract_social_media(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        for link in soup.find_all('a', class_='social-media__link'):  # Use a class name
            href = link.get('href')
            if href is not None:
                if any(platform in href for platform in ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube']):
                    links.append({'platform': platform, 'link': href})
        # print(soup)
        # print(links)
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    except Exception as e:  # Handle any other errors during extraction
        print(f"Error extracting social media for {url}: {e}")
        return 'Not Found'

def extract_tech_stack(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        tech_stack = []
        for script in soup.find_all('script'):
            content = script.get_text()
            if any(keyword in content for keyword in ['React', 'Angular', 'Django', 'WordPress', 'MySQL']):
                tech_stack.append(keyword)
        return tech_stack
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    except Exception as e:  # Handle any other errors during extraction
        print(f"Error extracting tech stack for {url}: {e}")
        return 'Not Found' 

def extract_meta_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').get_text()
        description = soup.find('meta', attrs={'name': 'description'})
        description = description.get('content') if description else ''
        return {'title': title, 'description': description}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {}
    except Exception as e:  # Handle any other errors during extraction
        print(f"Error extracting meta data for {url}: {e}")
        return 'Not Found' 

def extract_payment_gateways(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        gateways = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if any(gateway in src for gateway in ['paypal', 'stripe', 'razorpay']):
                gateways.append(gateway)
        return gateways
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []
    except Exception as e:  # Handle any other errors during extraction
        print(f"Error extracting payment gateways for {url}: {e}")
        return 'Not Found' 

def extract_language(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        language = soup.find('html').get('lang')
        return language
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ''
    except Exception as e:  # Handle any other errors during extraction
        print(f"Error extracting language for {url}: {e}")
        return 'Not Found' 

def extract_category(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        # Data Cleaning 
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        tokens = word_tokenize(text)
        filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words and word.isalnum()]
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        cleaned_text = ' '.join(lemmatized_tokens)

        # Keyword Analysis
        keyword_counts = {}
        keywords = ['technology', 'news', 'business', 'sports', 'entertainment', 'fashion', 'health']
        for keyword in keywords:
            keyword_counts[keyword] = cleaned_text.count(keyword)

        # Find Keywords with Highest Counts
        max_counts = np.array(list(keyword_counts.values()))  # Convert to NumPy array
        top_keywords = np.where(max_counts == max_counts.max())  # Find indices of maximum counts
        top_keywords = [keywords[i] for i in top_keywords[0]]  # Get the keywords at those indices

        # Return Top Keyword (or "Unknown" if no clear top keyword)
        if len(top_keywords) == 1:
            return top_keywords[0]
        else:
            return "Multiple Categories Found"  # More specific message

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return 'Error Fetching Website'  # More specific message
    except Exception as e:  # Handle any other errors during extraction
        print(f"Error extracting category for {url}: {e}")
        return 'Error Extracting Category'  # More specific message 

def connect_to_database():
    mydb = mysql.connector.connect(
        host="localhost",  # Or your server's IP address
        user="root",
        password="",
        database="webscp"
    )
    return mydb



if __name__ == "__main__":

    website_urls = [
    # "https://github.com/amandeepsingh29"
    # "https://www.bbc.com",
    # "https://www.cnn.com",
    # "https://www.nytimes.com",
    # "https://www.reuters.com",
    # "https://www.aljazeera.com",
    # "https://www.washingtonpost.com",
    "https://www.theguardian.com"
    # "https://www.espn.com",
    # "https://www.wired.com",
    # "https://www.techcrunch.com",
    # "https://www.npr.org",
    # "https://www.theverge.com",
    # "https://www.mashable.com",
    # "https://www.buzzfeed.com",
    # "https://www.polygon.com",
    # "https://www.amazon.com",
    # "https://www.ebay.com",
    # "https://www.walmart.com",
    # "https://www.target.com",
    # "https://www.bestbuy.com",
    # "https://www.etsy.com",
    # "https://www.shopify.com",
    # "https://www.asos.com",
    # "https://www.zara.com",
    # "https://www.uniqlo.com",
    # "https://www.aliexpress.com",
    # "https://www.microsoft.com",
    # "https://www.google.com",
    # "https://www.apple.com",
    # "https://www.facebook.com",
    # "https://www.twitter.com",
    # "https://www.linkedin.com",
    # "https://www.github.com",
    # "https://www.stackoverflow.com",
    # "https://www.reddit.com",
    # "https://www.mozilla.org",
    # "https://www.oracle.com",
    # "https://www.ibm.com",
    # "https://www.medium.com",
    # "https://www.wordpress.com",
    # "https://www.tumblr.com",
    # "https://www.blogspot.com",
    # "https://www.lifehacker.com",
    # "https://www.makeuseof.com",
    # "https://www.entrepreneur.com",
    # "https://www.forbes.com",
    # "https://www.inc.com",
    # "https://www.tripadvisor.com",
    # "https://www.expedia.com",
    # "https://www.booking.com",
    # "https://www.lonelyplanet.com",
    # "https://www.nationalgeographic.com",
    # "https://www.hotels.com",
    # "https://www.bloomberg.com",
    # "https://www.investopedia.com",
    # "https://www.wallstreetjournal.com",
    # "https://www.cnbc.com",
    # "https://www.entrepreneur.com",
    # "https://www.mayoclinic.org",
    # "https://www.webmd.com",
    # "https://www.healthline.com",
    # "https://www.nhs.uk",
    # "https://www.who.int",
    # "https://www.khanacademy.org",
    # "https://www.coursera.org",
    # "https://www.edx.org",
    # "https://www.harvard.edu",
    # "https://www.stanford.edu",
    # "https://www.whitehouse.gov",
    # "https://www.un.org",
    # "https://www.usaid.gov",
    # "https://www.redcross.org",
    # "https://www.greenpeace.org",
    # "https://www.mlb.com",
    # "https://www.nba.com",
    # "https://www.nfl.com",
    # "https://www.fifa.com",
    # "https://www.olympics.com",
    # "https://www.imdb.com",
    # "https://www.wikipedia.org",
    # "https://www.pinterest.com",
    # "https://www.etsy.com",
    # "https://www.deviantart.com",
    # "https://www.bandcamp.com",
    # "https://www.soundcloud.com",
    # "https://www.nytimes.com/section/world", 
    # "https://www.cnn.com/world",
    # "https://www.bbc.com/news/world",
    # "https://www.aljazeera.com/news/world",
    # "https://www.theguardian.com/world",
    # "https://www.washingtonpost.com/world",
    # "https://www.reuters.com/world",
    # "https://www.npr.org/sections/world",
    # "https://www.theverge.com/tech",
    # "https://www.wired.com/topic/tech",
    # "https://www.techcrunch.com/startups",
    # "https://www.mashable.com/tech",
    # "https://www.polygon.com/reviews",
    # "https://www.amazon.com/Best-Sellers",
    # "https://www.ebay.com/b/Electronics",
    # "https://www.walmart.com/browse/electronics",
    # "https://www.target.com/c/electronics/-/N-fn4Z1z0yeylZi82",
    # "https://www.bestbuy.com/site/electronics",
    # "https://www.etsy.com/c/jewelry-and-accessories",
    # "https://www.shopify.com/industries/fashion",
    # "https://www.asos.com/women/new-in/cat/pge13002",
    # "https://www.zara.com/us/en/woman-new-arrivals-c752.html",
    # "https://www.uniqlo.com/us/en/women",
    # "https://www.aliexpress.com/category/200000340/women-s-clothing.html",
    # "https://www.microsoft.com/en-us/surface",
    # "https://www.google.com/search?q=google+products",
    # "https://www.apple.com/shop/buy-mac/macbook-air",
    # "https://www.facebook.com/business",
    # "https://www.twitter.com/business",
    # "https://www.linkedin.com/business",
    # "https://www.github.com/explore",
    # "https://www.stackoverflow.com/questions/tagged/python",
    # "https://www.reddit.com/r/programming",
    # "https://www.mozilla.org/en-US/firefox/new/",
    # "https://www.oracle.com/cloud/database",
    # "https://www.ibm.com/cloud/paas",
    # "https://www.medium.com/topic/technology",
    # "https://www.wordpress.com/start/how-to-start-a-blog/",
    # "https://www.tumblr.com/tagged/art",
    # "https://www.blogspot.com/platform/about",
    # "https://www.lifehacker.com/tech",
    # "https://www.makeuseof.com/tag/productivity",
    # "https://www.entrepreneur.com/topic/startups",
    # "https://www.forbes.com/technology",
    # "https://www.inc.com/entrepreneurship",
    # "https://www.tripadvisor.com/Tourism",
    # "https://www.expedia.com/Things-to-Do",
    # "https://www.booking.com/city/usa.html",
    # "https://www.lonelyplanet.com/destinations",
    # "https://www.nationalgeographic.com/travel",
    # "https://www.hotels.com/travel",
    # "https://www.bloomberg.com/markets",
    # "https://www.investopedia.com/terms/s/stockmarket.asp",
    # "https://www.wallstreetjournal.com/markets",
    # "https://www.cnbc.com/markets",
    # "https://www.entrepreneur.com/topic/business",
    # "https://www.mayoclinic.org/diseases-conditions",
    # "https://www.webmd.com/a-to-z-guides",
    # "https://www.healthline.com/health",
    # "https://www.nhs.uk/conditions",
    # "https://www.who.int/news-room/fact-sheets",
    # "https://www.khanacademy.org/science",
    # "https://www.coursera.org/courses?query=data%20science",
    # "https://www.edx.org/course/subject/computer-science",
    # "https://www.harvard.edu/academics",
    # "https://www.stanford.edu/dept/engineering/",
    # "https://www.whitehouse.gov/briefing-room",
    # "https://www.un.org/en/sections/issues-depth/",
    # "https://www.usaid.gov/what-we-do",
    # "https://www.redcross.org/about-us/who-we-are",
    # "https://www.greenpeace.org/usa/issues",
    # "https://www.mlb.com/news",
    # "https://www.nba.com/news",
    # "https://www.nfl.com/news",
    # "https://www.fifa.com/about-fifa/news",
    # "https://www.olympics.com/ioc/news",
    # "https://www.imdb.com/chart/top/",
    # "https://www.wikipedia.org/wiki/Main_Page",
    # "https://www.pinterest.com/explore/",
    # "https://www.etsy.com/shop/featured",
    # "https://www.deviantart.com/popular",
    # "https://www.bandcamp.com/discover",
    # "https://www.soundcloud.com/discover"
]
    
    db = connect_to_database()
    cursor = db.cursor()

    for url in website_urls:
        # Extract Data
        social_media_data = extract_social_media(url)
        tech_stack_data = extract_tech_stack(url)
        meta_data = extract_meta_data(url)
        payment_gateways_data = extract_payment_gateways(url)
        language_data = extract_language(url)
        category_data = extract_category(url)

        # Store Data in Database 
        try:
            # Insert Website Data
            cursor.execute(
                "INSERT INTO websites (url, category) VALUES (%s, %s)",
                (url, category_data)
            )
            website_id = cursor.lastrowid

            # Insert Social Media Data
            if social_media_data != 'Not Found' and social_media_data!=[]:
                for item in social_media_data:
                    cursor.execute(
                        "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
                        (website_id, item['platform'], item['link'])
                    )
            elif social_media_data==[]:
                cursor.execute(
                        "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
                        (website_id,"-","-")
                    )    
            else:
                cursor.execute(
                    "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
                    (website_id, 'Not Found', 'Not Found')
                )
                 
            # Insert Tech Stack Data
            if tech_stack_data != 'Not Found' and tech_stack_data!=[]:
                for tech in tech_stack_data:
                    cursor.execute(
                        "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
                        (website_id, tech)
                    )
            elif tech_stack_data==[]:
                cursor.execute(
                        "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
                        (website_id, '-')
                    )
            else:
                cursor.execute(
                    "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
                    (website_id, 'Not Found')
                )

            # Insert Meta Data
            if meta_data != 'Not Found' and meta_data!=[]:
                cursor.execute(
                    "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
                    (website_id, meta_data['title'], meta_data['description'])
                )
            elif meta_data==[]:
                cursor.execute(
                    "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
                    (website_id, '-','-')
                )
            else:
                cursor.execute(
                    "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
                    (website_id, 'Not Found', 'Not Found')
                )

            # Insert Payment Gateways Data
            if payment_gateways_data != 'Not Found' and payment_gateways_data!=[]:
                for gateway in payment_gateways_data:
                    cursor.execute(
                        "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)",
                        (website_id, gateway)
                    )
            elif payment_gateways_data==[]:
                cursor.execute(
                        "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)",
                        (website_id, '-')
                    )
            else:
                cursor.execute(
                    "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)",
                    (website_id, 'Not Found')
                )

            # Insert Language Data
            if language_data != 'Not Found' and language_data!=[]:
                cursor.execute(
                    "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
                    (website_id, language_data)
                )
            elif language_data==[]:
                cursor.execute(
                    "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
                    (website_id, '-')
                )
            else:
                cursor.execute(
                    "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
                    (website_id, 'Not Found')
                )

            db.commit()
            print(f"Data for {url} inserted successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting data for {url}: {err}")
            db.rollback()

    cursor.close()
    db.close()
    