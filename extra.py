
# # def extract_social_media(url):
# #     try:
# #         response = requests.get(url)
# #         response.raise_for_status()  # Raise an exception for bad status codes
# #         soup = BeautifulSoup(response.content, 'html.parser')
# #         links = []
# #         for link in soup.find_all('a'):
# #             href = link.get('href')
# #             if any(platform in href for platform in ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube']):
# #                 links.append({'platform': platform, 'link': href})
# #         return links
# #     except requests.exceptions.RequestException as e:
# #         print(f"Error fetching {url}: {e}")
# #         return []
    
# def extract_social_media(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         links = []
#         for link in soup.find_all('a', class_='social-media__link'):  # Use a class name
#             href = link.get('href')
#             if href is not None:
#                 if any(platform in href for platform in ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube']):
#                     links.append({'platform': platform, 'link': href})
#         return links
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return []    
    
    
    
    
# def extract_tech_stack(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         tech_stack = []
#         for script in soup.find_all('script'):
#             content = script.get_text()
#             if any(keyword in content for keyword in ['React', 'Angular', 'Django', 'WordPress', 'MySQL']):
#                 tech_stack.append(keyword)
#         return tech_stack
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return []

# def extract_meta_data(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         title = soup.find('title').get_text()
#         description = soup.find('meta', attrs={'name': 'description'})
#         description = description.get('content') if description else ''
#         return {'title': title, 'description': description}
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return {}
    
# def extract_payment_gateways(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         gateways = []
#         for img in soup.find_all('img'):
#             src = img.get('src')
#             if any(gateway in src for gateway in ['paypal', 'stripe', 'razorpay']):
#                 gateways.append(gateway)
#         return gateways
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return []
    
    
# def extract_language(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         language = soup.find('html').get('lang')
#         return language
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return ''
    
    
    
# def extract_category(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Count occurrences of keywords
#         keyword_counts = {}
#         for keyword in ['news', 'technology', 'e-commerce', 'blog', 'travel', 'business', 'sports', 'entertainment', 'fashion', 'health']:
#             keyword_counts[keyword] = len(soup.find_all(text=lambda text: keyword in text.lower()))

#         # Assign category based on highest keyword count
#         max_count = max(keyword_counts.values())
#         for keyword, count in keyword_counts.items():
#             if count == max_count:
#                 return keyword

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return 'Unknown'
    
    
# def extract_category(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         text = soup.get_text()

#         # Data Cleaning (Similar to your commented-out topic modeling code)
#         stop_words = set(stopwords.words('english'))
#         lemmatizer = WordNetLemmatizer()
#         tokens = word_tokenize(text)
#         filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words and word.isalnum()]
#         lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
#         cleaned_text = ' '.join(lemmatized_tokens)

#         # Count occurrences of keywords
#         keyword_counts = {}
#         for keyword in ['technology', 'news', 'business', 'sports', 'entertainment', 'fashion', 'health']:
#             keyword_counts[keyword] = cleaned_text.count(keyword)  # Count occurrences in cleaned text

#         # Assign category based on highest keyword count
#         max_count = max(keyword_counts.values())
#         for keyword, count in keyword_counts.items():
#             if count == max_count:
#                 return keyword

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return 'Unknown'
 

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

# def extract_category(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         text = soup.get_text()

#         # Data Cleaning 
#         stop_words = set(stopwords.words('english'))
#         lemmatizer = WordNetLemmatizer()
#         tokens = word_tokenize(text)
#         filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words and word.isalnum()]
#         lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
#         cleaned_text = ' '.join(lemmatized_tokens)

#         # Keyword Analysis
#         keyword_counts = {}
#         keywords = ['technology', 'news', 'business', 'sports', 'entertainment', 'fashion', 'health']
#         for keyword in keywords:
#             keyword_counts[keyword] = cleaned_text.count(keyword)

#         # Find Keywords with Highest Counts
#         max_counts = np.array(list(keyword_counts.values()))  # Convert to NumPy array
#         top_keywords = np.where(max_counts == max_counts.max())  # Find indices of maximum counts
#         top_keywords = [keywords[i] for i in top_keywords[0]]  # Get the keywords at those indices

#         # Return Top Keyword (or "Unknown" if no clear top keyword)
#         if len(top_keywords) == 1:
#             return top_keywords[0]
#         else:
#             return "Multiple Categories Found"  # More specific message

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return 'Error Fetching Website'  # More specific message
#     except Exception as e:  # Handle any other errors during extraction
#         print(f"Error extracting category for {url}: {e}")
#         return 'Error Extracting Category'  # More specific message    
    
# def extract_category(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')
#         text = soup.get_text()

#         # Preprocess Text
#         stop_words = set(stopwords.words('english'))
#         lemmatizer = WordNetLemmatizer()
#         tokens = word_tokenize(text)
#         filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words and word.isalnum()]
#         lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
#         processed_text = ' '.join(lemmatized_tokens)

#         # Create a dictionary and corpus
#         dictionary = Dictionary([processed_text.split()])
#         corpus = [dictionary.doc2bow(processed_text.split())]

#         # Train an LDA model (Adjust num_topics as needed)
#         lda_model = LdaModel(corpus, num_topics=5, id2word=dictionary)

#         # Get the dominant topic
#         dominant_topic = lda_model.get_document_topics(corpus[0])[0][0]

#         # Map Topic to Category (This is where your knowledge is key)
#         topic_to_category_mapping = {
#             0: 'Technology',
#             1: 'News',
#             2: 'E-commerce',
#             3: 'Travel',
#             4: 'Entertainment'
#         }

#         category = topic_to_category_mapping.get(dominant_topic, 'Unknown')
#         return category

#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return 'Unknown' 





    
    # db = connect_to_database()
    # cursor = db.cursor()

    # for url in website_urls:
    #     # Extract Data
    #     social_media_data = extract_social_media(url)
    #     tech_stack_data = extract_tech_stack(url)
    #     meta_data = extract_meta_data(url)
    #     payment_gateways_data = extract_payment_gateways(url)
    #     language_data = extract_language(url)
    #     category_data = extract_category(url)

    #     # Store Data in Database (Illustrative Example - You'll need to adapt this)
    #     try:
    #         # Insert Website Data
    #         cursor.execute(
    #             "INSERT INTO websites (url, category) VALUES (%s, %s)",
    #             (url, category_data)
    #         )
    #         website_id = cursor.lastrowid

    #         # Insert Social Media Data
    #         if social_media_data != 'Not Found':
    #             for item in social_media_data:
    #                 cursor.execute(
    #                     "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
    #                     (website_id, item['platform'], item['link'])
    #                 )
    #         else:
    #             cursor.execute(
    #                 "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
    #                 (website_id, 'Not Found', 'Not Found')
    #             )

    #         # Insert Tech Stack Data
    #         if tech_stack_data != 'Not Found':
    #             for tech in tech_stack_data:
    #                 cursor.execute(
    #                     "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
    #                     (website_id, tech)
    #                 )
    #         else:
    #             cursor.execute(
    #                 "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
    #                 (website_id, 'Not Found', 'Not Found')
    #             )

    #         # Insert Meta Data
    #         if meta_data != 'Not Found':
    #             cursor.execute(
    #                 "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
    #                 (website_id, meta_data['title'], meta_data['description'])
    #             )
    #         else:
    #             cursor.execute(
    #                 "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
    #                 (website_id, 'Not Found', 'Not Found')
    #             )

    #         # Insert Payment Gateways Data
    #         if payment_gateways_data != 'Not Found':
    #             for gateway in payment_gateways_data:
    #                 cursor.execute(
    #                     "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)",
    #                     (website_id, gateway)
    #                 )
    #         else:
    #             cursor.execute(
    #                 "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)",
    #                 (website_id, 'Not Found', 'Not Found')
    #             )

    #         # Insert Language Data
    #         if language_data != 'Not Found':
    #             cursor.execute(
    #                 "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
    #                 (website_id, language_data)
    #             )
    #         else:
    #             cursor.execute(
    #                 "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
    #                 (website_id, 'Not Found', 'Not Found')
    #             )

    #         db.commit()
    #         print(f"Data for {url} inserted successfully.")
    #     except mysql.connector.Error as err:
    #         print(f"Error inserting data for {url}: {err}")
    #         db.rollback()

    # cursor.close()
    # db.close()
    # db = connect_to_database()
    # cursor = db.cursor()

    # for url in website_urls:
    #     # Extract Data
    #     social_media_data = extract_social_media(url)
    #     tech_stack_data = extract_tech_stack(url)
    #     meta_data = extract_meta_data(url)
    #     payment_gateways_data = extract_payment_gateways(url)
    #     language_data = extract_language(url)
    #     category_data = extract_category(url)

    #     # Store Data in Database (Illustrative Example - You'll need to adapt this)
    #     try:
    #         # Insert Website Data
    #         cursor.execute(
    #             "INSERT INTO websites (url, category) VALUES (%s, %s)",
    #             (url, category_data)
    #         )
    #         website_id = cursor.lastrowid

    #         # Insert Social Media Data
    #         for item in social_media_data:
    #             cursor.execute(
    #                 "INSERT INTO social_media (website_id, platform, link) VALUES (%s, %s, %s)",
    #                 (website_id, item['platform'], item['link'])
    #             )

    #         # Insert Tech Stack Data
    #         for tech in tech_stack_data:
    #             cursor.execute(
    #                 "INSERT INTO tech_stack (website_id, technology) VALUES (%s, %s)",
    #                 (website_id, tech)
    #             )

    #         # Insert Meta Data
    #         cursor.execute(
    #             "INSERT INTO meta (website_id, title, description) VALUES (%s, %s, %s)",
    #             (website_id, meta_data['title'], meta_data['description'])
    #         )

    #         # Insert Payment Gateways Data
    #         for gateway in payment_gateways_data:
    #             cursor.execute(
    #                 "INSERT INTO payment_gateways (website_id, gateway) VALUES (%s, %s)",
    #                 (website_id, gateway)
    #             )

    #         # Insert Language Data
    #         cursor.execute(
    #             "INSERT INTO languages (website_id, language) VALUES (%s, %s)",
    #             (website_id, language_data)
    #         )

    #         db.commit()
    #         print(f"Data for {url} inserted successfully.")
    #     except mysql.connector.Error as err:
    #         print(f"Error inserting data for {url}: {err}")
    #         db.rollback()

    # cursor.close()
    # db.close()