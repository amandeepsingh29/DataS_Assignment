import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk 
import numpy as np 
import re
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# from gensim.corpora import Dictionary
# from gensim.models import LdaModel


def extract_social_media(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        links = []
        for link in soup.find_all('a', class_='Link--primary'):  # Use a class name
            href = link.get('href')
            if href is not None:
                # Determine platform based on URL patterns
                if 'facebook.com' in href:
                    platform = 'Facebook'
                elif 'twitter.com' in href:
                    platform = 'Twitter'
                elif 'linkedin.com' in href:
                    platform = 'LinkedIn'
                elif 'instagram.com' in href:
                    platform = 'Instagram'
                elif 'youtube.com' in href:
                    platform = 'YouTube'
                else:
                    platform = 'Other'  # Default to "Other" if platform not recognized

                links.append({'platform': platform, 'link': href})

        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "Error fetching"
    except Exception as e:
        print(f"Error extracting social media for {url}: {e}")
        return 'Not Found'

def extract_tech_stack(url):
    try:
        # Fetch the website's HTML content
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        headers = response.headers

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Check for front-end technologies
        front_end_techs = ['react', 'angular', 'vue', 'nextjs', 'ember', 'backbone', 'polymer', 'preact']
        front_end_tech = check_script_links(soup, front_end_techs)
        if front_end_tech:
            return front_end_tech

        # Check for back-end technologies
        back_end_techs = ['django', 'laravel', 'symfony', 'express', 'spring', 'aspnet', 'flask', 'rails']
        back_end_tech = check_script_links(soup, back_end_techs)
        if back_end_tech:
            return back_end_tech

        # Check for other technologies
        if soup.find('meta', {'name': 'generator', 'content': re.compile(r'wordpress', re.I)}):
            return 'WordPress'
        elif soup.find('meta', {'name': 'generator', 'content': re.compile(r'drupal', re.I)}):
            return 'Drupal'
        elif soup.find('script', src=lambda src: 'shopify' in str(src).lower()):
            return 'Shopify'
        elif soup.find('script', src=lambda src: 'magento' in str(src).lower()):
            return 'Magento'
        elif soup.find('meta', {'name': 'generator', 'content': re.compile(r'joomla', re.I)}):
            return 'Joomla'

        # Check for basic HTML and CSS
        if not soup.find('script') and not soup.find('link', rel='stylesheet'):
            return 'HTML and CSS'

        # Check server headers
        server_header = headers.get('Server')
        if server_header:
            server_header = server_header.lower()
            if 'nginx' in server_header:
                return 'Nginx'
            elif 'apache' in server_header:
                return 'Apache'
            elif 'iis' in server_header:
                return 'IIS'

        # Check for popular JS libraries
        if soup.find('script', src=lambda src: 'jquery' in str(src).lower()):
            return 'jQuery'
        elif soup.find('script', src=lambda src: 'bootstrap' in str(src).lower()):
            return 'Bootstrap'

        else:
            return 'Unknown'

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def check_script_links(soup, tech_list):
    for tech in tech_list:
        if soup.find('script', src=lambda src: tech in str(src).lower()) or \
           soup.find('link', href=lambda href: tech in str(href).lower()):
            return tech.capitalize()
    return None

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
        # print(language)
        return language
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        # print(language)
        return ''
    except Exception as e:  # Handle any other errors during extraction
        print(f"Error extracting language for {url}: {e}")
        # print(language)
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
            keyword_string = ""
            for keyword in top_keywords:
                if keyword_string == "":
                    keyword_string += keyword   
                else:
                    keyword_string += "," + keyword
            
            return keyword_string # More specific message

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
    'https://bcmschools.org/Home/Index/',
    'https://github.com/rimjhimittal',
    'https://www.bbc.com',
    'https://www.cnn.com',
    'https://www.aljazeera.com',
    'https://www.washingtonpost.com',
    'https://www.theguardian.com',
    'https://www.wired.com',
    'https://www.mashable.com',
    'https://www.buzzfeed.com',
    'https://www.polygon.com',
    'https://www.ebay.com',
    'https://www.walmart.com',
    'https://www.google.com',
    'https://www.apple.com',
    'https://www.facebook.com',
    'https://www.github.com',
    'https://www.reddit.com',
    'https://www.mozilla.org',
    'https://www.ibm.com',
    'https://www.medium.com',
    'https://www.wordpress.com',
    'https://www.tumblr.com',
    'https://www.blogspot.com',
    'https://www.lifehacker.com',
    'https://www.makeuseof.com',
    'https://www.entrepreneur.com',
    'https://www.forbes.com',
    'https://www.booking.com',
    'https://www.lonelyplanet.com',
    'https://www.nationalgeographic.com',
    'https://www.bloomberg.com',
    'https://www.cnbc.com',
    'https://www.mayoclinic.org',
    'https://www.healthline.com',
    'https://www.nhs.uk',
    'https://www.khanacademy.org',
    'https://www.coursera.org',
    'https://www.edx.org',
    'https://github.com/NebulaTris',
    'https://www.harvard.edu',
    'https://www.stanford.edu',
    'https://www.whitehouse.gov',
    'https://www.usaid.gov',
    'https://www.redcross.org',
    'https://www.greenpeace.org',
    'https://www.harvard.edu/academics',
    'https://www.whitehouse.gov/briefing-room',
    'https://www.usaid.gov/what-we-do',
    'https://www.redcross.org/about-us/who-we-are',
    'https://www.greenpeace.org/usa/issues',
    'https://www.mlb.com/news',
    'https://www.nba.com/news',
    'https://www.nfl.com/news',
    'https://www.wikipedia.org/wiki/Main_Page',
    'https://www.pinterest.com/explore/',
    'https://www.deviantart.com/popular',
    'https://www.soundcloud.com/discover',
    'https://www.nba.com',
    'https://www.nfl.com',
    'https://www.wikipedia.org',
    'https://www.pinterest.com',
    'https://github.com/Jijnash-Kashyap',
    'https://www.deviantart.com',
    'https://www.soundcloud.com',
    'https://www.nytimes.com/section/world',
    'https://www.cnn.com/world',
    'https://www.theguardian.com/world',
    'https://www.washingtonpost.com/world',
    'https://www.npr.org/sections/world',
    'https://www.mashable.com/tech',
    'https://www.walmart.com/browse/electronics',
    'https://www.cnbc.com/markets',
    'https://www.entrepreneur.com/topic/business',
    'https://www.mayoclinic.org/diseases-conditions',
    'https://www.healthline.com/health',
    'https://www.nhs.uk/conditions',
    'https://www.khanacademy.org/science',
    'https://www.coursera.org/courses?query=%20science',
    'https://www.google.com/search?q=google+products',
    'https://www.apple.com/shop/buy-mac/macbook-air',
    'https://www.facebook.com/business',
    'https://www.github.com/explore',
    'https://www.stackoverflow.com/questions/tagged/python',
    'https://www.reddit.com/r/programming',
    'https://www.mozilla.org/en-US/firefox/new/',
    'https://www.ibm.com/cloud/paas',
    'https://www.medium.com/topic/technology',
    'https://www.wordpress.com/start/how-to-start-a-blog/',
    'https://www.lifehacker.com/tech',
    'https://www.makeuseof.com/tag/productivity',
    'https://github.com/krishnaik06/Roadmap-To-Become-Data-Analyst-2024',
    'https://www.entrepreneur.com/topic/startups',
    'https://www.forbes.com/technology',
    'https://github.com/manpreet171',
    'https://www.nationalgeographic.com/travel',
    'https://github.com/k26rahul',
    'https://github.com/terrytangyuan',
    'https://github.com/kubeflow',
    'https://github.com/marcoceppi'
]
    
    db = connect_to_database()
    cursor = db.cursor()

    for url in website_urls:
        # Extract Data
        social_media_data = extract_social_media(url)
        if social_media_data=="Error fetching":
            continue;
        else:
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
            
            social_media_data = extract_social_media(url)
            

            # Insert Social Media Data
            if social_media_data=="Error fetching":
                continue
            elif social_media_data != 'Not Found' and social_media_data!=[]:
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
            if tech_stack_data != 'Unknown' and tech_stack_data!=[]:
                cursor.execute(
                    "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
                    (website_id, tech_stack_data)
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
            if language_data != 'Not Found' and language_data=="None" and language_data!=[]:
                cursor.execute(
                    "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
                    (website_id, language_data)
                )
            elif language_data==[] or language_data=="None":
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
    