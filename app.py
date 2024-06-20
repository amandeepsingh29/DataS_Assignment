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

# Constants for platform and technology detection
SOCIAL_MEDIA_PLATFORMS = {
    'facebook.com': 'Facebook',
    'twitter.com': 'Twitter',
    'linkedin.com': 'LinkedIn',
    'instagram.com': 'Instagram',
    'youtube.com': 'YouTube'
}

FRONT_END_TECHNOLOGIES = ['react', 'angular', 'vue', 'nextjs', 'ember', 'backbone', 'polymer', 'preact']
BACK_END_TECHNOLOGIES = ['django', 'laravel', 'symfony', 'express', 'spring', 'aspnet', 'flask', 'rails']
CMS_TECHNOLOGIES = ['wordpress', 'drupal', 'shopify', 'magento', 'joomla']
JS_LIBRARIES = ['jquery', 'bootstrap']
SERVER_HEADERS = {'nginx': 'Nginx', 'apache': 'Apache', 'iis': 'IIS'}

def extract_social_media(url):
    """Extracts social media links from a website."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        links = []
        for link in soup.find_all('a', class_='Link--primary'):
            href = link.get('href')
            if href:
                for platform_url, platform_name in SOCIAL_MEDIA_PLATFORMS.items():
                    if platform_url in href:
                        links.append({'platform': platform_name, 'link': href})
                        break
                else:
                    links.append({'platform': 'Other', 'link': href})

        return links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "Error fetching"
    except Exception as e:
        print(f"Error extracting social media for {url}: {e}")
        return 'Not Found'

def extract_tech_stack(url):
    """Extracts the technology stack used by a website."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        headers = response.headers

        # Check for front-end technologies
        front_end_tech = check_script_links(soup, FRONT_END_TECHNOLOGIES)
        if front_end_tech:
            return front_end_tech

        # Check for back-end technologies
        back_end_tech = check_script_links(soup, BACK_END_TECHNOLOGIES)
        if back_end_tech:
            return back_end_tech

        # Check for CMS technologies
        for cms in CMS_TECHNOLOGIES:
            if soup.find('meta', {'name': 'generator', 'content': re.compile(cms, re.I)}):
                return cms.capitalize()
            elif soup.find('script', src=lambda src: cms in str(src).lower()):
                return cms.capitalize()

        # Check for basic HTML and CSS
        if not soup.find('script') and not soup.find('link', rel='stylesheet'):
            return 'HTML and CSS'

        # Check server headers
        server_header = headers.get('Server')
        if server_header:
            server_header = server_header.lower()
            for header_key, header_value in SERVER_HEADERS.items():
                if header_key in server_header:
                    return header_value

        # Check for popular JS libraries
        for js_library in JS_LIBRARIES:
            if soup.find('script', src=lambda src: js_library in str(src).lower()):
                return js_library.capitalize()

        return 'Unknown'

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def check_script_links(soup, tech_list):
    """Checks for script or link tags containing specific technologies."""
    for tech in tech_list:
        if soup.find('script', src=lambda src: tech in str(src).lower()) or \
           soup.find('link', href=lambda href: tech in str(href).lower()):
            return tech.capitalize()
    return None

def extract_meta_data(url):
    """Extracts title and description meta tags from a website."""
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
    except Exception as e:
        print(f"Error extracting meta data for {url}: {e}")
        return 'Not Found'

def extract_payment_gateways(url):
    """Extracts payment gateway logos from a website."""
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
    except Exception as e:
        print(f"Error extracting payment gateways for {url}: {e}")
        return 'Not Found'

def extract_language(url):
    """Extracts the language of a website."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        language = soup.find('html').get('lang')
        return language
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ''
    except Exception as e:
        print(f"Error extracting language for {url}: {e}")
        return 'Not Found'

def extract_category(url):
    """Extracts the category of a website using keyword analysis."""
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
        keywords = ['technology', 'news', 'business', 'sports', 'entertainment', 'fashion', 'health', 'travel', 'education', 'politics', 'music', 'art', 'science']
        for keyword in keywords:
            keyword_counts[keyword] = cleaned_text.count(keyword)

        # Find Keywords with Highest Counts
        max_counts = np.array(list(keyword_counts.values()))
        top_keywords = np.where(max_counts == max_counts.max())
        top_keywords = [keywords[i] for i in top_keywords[0]]

        # Return Top Keyword (or "Unknown" if no clear top keyword)
        if len(top_keywords) == 1:
            return top_keywords[0]
        else:
            return ', '.join(top_keywords)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return 'Error Fetching Website'
    except Exception as e:
        print(f"Error extracting category for {url}: {e}")
        return 'Error Extracting Category'

def connect_to_database():
    """Connects to the MySQL database."""
    mydb = mysql.connector.connect(
        host="localhost",  # Or your server's IP address
        user="root",
        password="",
        database="webscp"
    )
    return mydb

if __name__ == "__main__":
    website_urls = [
        "https://medium.com/@grantpiperwriting/why-cant-robots-click-the-i-m-not-a-robot-box-on-websites-370f239ba7f4",
        "https://github.com/TheOdinProject",
        "https://github.com/freeCodeCamp",
        "https://github.com/facebook",
        "https://github.com/google",
        "https://github.com/microsoft",
        "https://github.com/tensorflow",
        "https://github.com/vuejs",
        "https://github.com/facebook/react",
        "https://github.com/angular",
        "https://github.com/nodejs",
        "https://github.com/kubernetes",
        "https://github.com/docker",
        "https://github.com/mozilla",
        "https://github.com/apache",
        "https://github.com/python",
        "https://github.com/javascript",
        "https://github.com/rust-lang",
        "https://github.com/golang",
        "https://github.com/opencv",
        "https://github.com/pytorch",
        "https://medium.com/swlh/mastering-git-and-github-a-beginners-guide-e987061f9540",
        "https://medium.com/swlh/the-future-of-programming-5-trends-to-watch-92474826c603",
        "https://medium.com/swlh/building-a-simple-api-with-node-js-and-express-24468e02e196",
        "https://medium.com/swlh/understanding-data-structures-and-algorithms-a-beginners-guide-302120f49947",
        "https://medium.com/swlh/the-power-of-design-patterns-in-software-development-a-beginners-guide-3294a470c32d",
        "https://medium.com/swlh/how-to-build-a-portfolio-website-for-developers-a-step-by-step-guide-25f29509d221",
        "https://medium.com/swlh/the-importance-of-code-reviews-in-software-development-a-beginners-guide-81502083394c",
        "https://medium.com/swlh/understanding-agile-development-methodologies-a-beginners-guide-d724295b904c",
        "https://medium.com/swlh/the-rise-of-low-code-and-no-code-development-a-look-at-the-future-of-software-development-4929f1255447",
        "https://medium.com/towards-data-science/a-beginners-guide-to-machine-learning-e94034417d31",
        "https://medium.com/towards-data-science/understanding-the-basics-of-artificial-intelligence-a-beginners-guide-826688989060",
        "https://medium.com/towards-data-science/the-power-of-deep-learning-a-practical-guide-for-beginners-c95e26613013",
        "https://medium.com/towards-data-science/building-a-simple-machine-learning-model-with-python-a-step-by-step-guide-for-beginners-56f85277c81b",
        "https://medium.com/towards-data-science/understanding-the-different-types-of-machine-learning-algorithms-a-beginners-guide-e34502777746",
        "https://medium.com/towards-data-science/the-importance-of-data-cleaning-and-preprocessing-in-machine-learning-a-beginners-guide-983223269657",
        "https://medium.com/towards-data-science/the-future-of-data-science-trends-to-watch-in-2024-and-beyond-45015461a368",
        "https://medium.com/towards-data-science/building-a-recommendation-system-with-machine-learning-a-beginners-guide-3883e134697c",
        "https://medium.com/towards-data-science/understanding-the-basics-of-natural-language-processing-nlp-a-beginners-guide-8903871519f6",
        "https://medium.com/towards-data-science/the-power-of-data-visualization-in-data-science-a-beginners-guide-5496734f896e",
        "https://medium.com/swlh/how-to-build-a-successful-career-in-tech-a-guide-for-beginners-and-experienced-professionals-alike-5734558c018b",
        "https://medium.com/swlh/the-importance-of-continuous-learning-in-the-tech-industry-a-guide-for-developers-and-professionals-alike-32782418395f",
        "https://medium.com/swlh/how-to-ace-your-next-tech-interview-a-guide-for-developers-and-professionals-alike-206017c34616",
        "https://medium.com/swlh/the-importance-of-networking-in-the-tech-industry-a-guide-for-developers-and-professionals-alike-137149325a88",
        "https://medium.com/swlh/how-to-develop-a-growth-mindset-for-success-a-guide-for-developers-and-professionals-alike-752680362272",
        "https://medium.com/swlh/the-importance-of-time-management-for-developers-a-guide-for-developers-and-professionals-alike-172366773409",
        "https://medium.com/swlh/how-to-stay-motivated-as-a-developer-a-guide-for-developers-and-professionals-alike-35043473539e",
        "https://medium.com/swlh/the-importance-of-building-a-personal-brand-in-tech-a-guide-for-developers-and-professionals-alike-278258103369",
        "https://medium.com/swlh/how-to-find-a-mentor-in-the-tech-industry-a-guide-for-developers-and-professionals-alike-426343396708",
        "https://medium.com/swlh/the-importance-of-giving-back-to-the-tech-community-a-guide-for-developers-and-professionals-alike-252790939742",
        "https://medium.com/swlh/the-future-of-work-how-ai-is-transforming-the-job-market-a-look-at-the-future-of-work-77743961480d",
        "https://medium.com/swlh/the-importance-of-cybersecurity-in-the-digital-age-a-guide-for-individuals-and-businesses-alike-88248495899",
        "https://medium.com/swlh/the-impact-of-blockchain-technology-on-the-world-a-look-at-the-future-of-blockchain-technology-256249431686",
        "https://medium.com/swlh/the-rise-of-the-metaverse-what-it-means-for-the-future-a-look-at-the-future-of-the-metaverse-186167265897",
        "https://medium.com/swlh/the-importance-of-sustainability-in-the-tech-industry-a-guide-for-developers-and-professionals-alike-71260931369",
        "https://medium.com/swlh/the-future-of-education-how-technology-is-transforming-learning-a-look-at-the-future-of-education-254134360066",
        "https://medium.com/swlh/the-power-of-storytelling-in-the-digital-age-a-guide-for-writers-and-marketers-alike-48736151608",
        "https://medium.com/swlh/the-importance-of-building-a-strong-personal-brand-a-guide-for-individuals-and-businesses-alike-75129807781",
        "https://medium.com/swlh/the-future-of-marketing-how-technology-is-changing-the-game-a-look-at-the-future-of-marketing-31826049042",
        "https://medium.com/swlh/the-importance-of-diversity-and-inclusion-in-the-tech-industry-a-guide-for-developers-and-professionals-alike-95238130330",
        "https://en.wikipedia.org/wiki/Earth",
        "https://en.wikipedia.org/wiki/Moon",
        "https://en.wikipedia.org/wiki/Sun",
        "https://en.wikipedia.org/wiki/Human",
        "https://en.wikipedia.org/wiki/History",
        "https://en.wikipedia.org/wiki/Science",
        "https://en.wikipedia.org/wiki/Technology",
        "https://en.wikipedia.org/wiki/Art",
        "https://en.wikipedia.org/wiki/Music",
        "https://en.wikipedia.org/wiki/Literature",
        "https://en.wikipedia.org/wiki/Philosophy",
        "https://en.wikipedia.org/wiki/Religion",
        "https://en.wikipedia.org/wiki/Politics",
        "https://en.wikipedia.org/wiki/Economics",
        "https://en.wikipedia.org/wiki/Psychology",
        "https://en.wikipedia.org/wiki/Biology",
        "https://en.wikipedia.org/wiki/Chemistry",
        "https://en.wikipedia.org/wiki/Physics",
        "https://en.wikipedia.org/wiki/Mathematics",
        "https://en.wikipedia.org/wiki/Computer_science",
        "https://en.wikipedia.org/wiki/United_States",
        "https://en.wikipedia.org/wiki/China",
        "https://en.wikipedia.org/wiki/India",
        "https://en.wikipedia.org/wiki/United_Kingdom",
        "https://en.wikipedia.org/wiki/Germany",
        "https://en.wikipedia.org/wiki/France",
        "https://en.wikipedia.org/wiki/Japan",
        "https://en.wikipedia.org/wiki/Russia",
        "https://en.wikipedia.org/wiki/Canada",
        "https://en.wikipedia.org/wiki/Australia",
        "https://en.wikipedia.org/wiki/World_War_II",
        "https://en.wikipedia.org/wiki/World_War_I",
        "https://en.wikipedia.org/wiki/Cold_War",
        "https://en.wikipedia.org/wiki/Internet",
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Climate_change",
        "https://en.wikipedia.org/wiki/Global_warming",
        "https://en.wikipedia.org/wiki/Democracy",
        "https://en.wikipedia.org/wiki/Capitalism",
        "https://en.wikipedia.org/wiki/Socialism",
        "https://en.wikipedia.org/wiki/Communism",
        "https://en.wikipedia.org/wiki/Evolution",
        "https://en.wikipedia.org/wiki/Quantum_mechanics",
        "https://en.wikipedia.org/wiki/Relativity",
        "https://en.wikipedia.org/wiki/Big_Bang",
        "https://en.wikipedia.org/wiki/Black_hole",
        "https://en.wikipedia.org/wiki/DNA",
        "https://en.wikipedia.org/wiki/Gene",
        "https://en.wikipedia.org/wiki/Cell",
        "https://en.wikipedia.org/wiki/Atom",
        "https://en.wikipedia.org/wiki/Element",
        "https://en.wikipedia.org/wiki/Periodic_table",
        "https://en.wikipedia.org/wiki/Human_genome",
        "https://en.wikipedia.org/wiki/Brain",
        "https://en.wikipedia.org/wiki/Consciousness",
        "https://en.wikipedia.org/wiki/Time",
        "https://en.wikipedia.org/wiki/Space",
        "https://en.wikipedia.org/wiki/Universe",
        "https://en.wikipedia.org/wiki/Galaxy",
        "https://en.wikipedia.org/wiki/Star",
        "https://en.wikipedia.org/wiki/Planet",
        "https://en.wikipedia.org/wiki/Solar_System",
        "https://en.wikipedia.org/wiki/Light",
        "https://en.wikipedia.org/wiki/Color",
        "https://en.wikipedia.org/wiki/Sound"
    ]


    db = connect_to_database()
    cursor = db.cursor()

    for url in website_urls:
        # Extract Data
        social_media_data = extract_social_media(url)
        if social_media_data == "Error fetching":
            continue
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

            # Insert Social Media Data
            if social_media_data != 'Not Found' and social_media_data != []:
                for item in social_media_data:
                    cursor.execute(
                        "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
                        (website_id, item['platform'], item['link'])
                    )
            elif social_media_data == []:
                cursor.execute(
                    "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
                    (website_id, "-", "-")
                )
            else:
                cursor.execute(
                    "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
                    (website_id, 'Not Found', 'Not Found')
                )

            # Insert Tech Stack Data
            if tech_stack_data != 'Unknown' and tech_stack_data != []:
                cursor.execute(
                    "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
                    (website_id, tech_stack_data)
                )
            elif tech_stack_data == []:
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
            if meta_data != 'Not Found' and meta_data != []:
                cursor.execute(
                    "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
                    (website_id, meta_data['title'], meta_data['description'])
                )
            elif meta_data == []:
                cursor.execute(
                    "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
                    (website_id, '-', '-')
                )
            else:
                cursor.execute(
                    "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
                    (website_id, 'Not Found', 'Not Found')
                )

            # Insert Payment Gateways Data
            if payment_gateways_data != 'Not Found' and payment_gateways_data != []:
                for gateway in payment_gateways_data:
                    cursor.execute(
                        "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)",
                        (website_id, gateway)
                    )
            elif payment_gateways_data == []:
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
            if language_data != 'Not Found' and language_data != "None" and language_data != []:
                cursor.execute(
                    "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
                    (website_id, language_data)
                )
            elif language_data == [] or language_data == "None":
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