# Website Data Extractor and Database Storage

This Python script extracts various data points from websites and stores them in a MySQL database.

## Features

- **Social Media Links Extraction:** Extracts Facebook, Twitter, LinkedIn, Instagram, YouTube, and other social media links from a website.
- **Technology Stack Detection:** Identifies front-end and back-end technologies used on the website, including popular frameworks and libraries.
- **Meta Data Extraction:** Retrieves the website's title and description from the `<meta>` tags.
- **Payment Gateway Detection:** Identifies popular payment gateways like PayPal, Stripe, and Razorpay.
- **Language Detection:** Determines the website's primary language.
- **Category Classification:** Analyzes website content to assign a relevant category (e.g., technology, news, business).
- **Database Integration:** Stores extracted data in a MySQL database for easy analysis and retrieval.

## Requirements

- Python 3.x (I used 3.11)
- `requests` library: `pip install requests`
- `beautifulsoup4` library: `pip install beautifulsoup4`
- `mysql-connector-python` library: `pip install mysql-connector-python`
- `nltk` library: `pip install nltk`
- `pandas` library: `pip install pandas`

## Setup

1. **Create a MySQL database:** Create a database named `webscp`.
2. **Clone the Repository** Create a local file with git clone command.
```bash
  git clone https://github.com/amandeepsingh29/DataS_Assignment.git
```

3. **Configure database connection:**
   - Update the `connect_to_database()` function in the script with your MySQL server details (host, user, password).
4. **Create database tables:**
   - The script creates the following tables:
     - `websites`: Stores website URL and category.
     - `social_media`: Stores social media links for each website.
     - `tech_stack`: Stores the technology stack used on each website.
     - `meta`: Stores the title and description of each website.
     - `payment_gateways`: Stores the payment gateways used on each website.
     - `languages`: Stores the language of each website.


#### Database Schema

    The script creates the following tables:

    **1. `websites`**

    - `website_id` (INT AUTO_INCREMENT PRIMARY KEY): Unique identifier for each website.
    - `url` (VARCHAR(255) UNIQUE NOT NULL): URL of the website.
    - `category` (VARCHAR(255) NOT NULL): Category of the website (e.g., technology, news, business).

    **2. `social_media`**

    - `social_media_id` (INT AUTO_INCREMENT PRIMARY KEY): Unique identifier for each social media link.
    - `website_id` (INT NOT NULL): Foreign key referencing the `websites` table.
    - `platform` (VARCHAR(50) NOT NULL): Social media platform (e.g., Facebook, Twitter, LinkedIn).
    - `link` (VARCHAR(255) NOT NULL): URL of the social media link.

    **3. `tech_stack`**

    - `tech_stack_id` (INT AUTO_INCREMENT PRIMARY KEY): Unique identifier for each technology used.
    - `website_id` (INT NOT NULL): Foreign key referencing the `websites` table.
    - `technology` (VARCHAR(50) NOT NULL): Technology used on the website (e.g., React, Django, WordPress).

    **4. `meta`**

    - `meta_id` (INT AUTO_INCREMENT PRIMARY KEY): Unique identifier for each meta data entry.
    - `website_id` (INT NOT NULL): Foreign key referencing the `websites` table.
    - `title` (VARCHAR(255) NOT NULL): Title of the website.
    - `description` (TEXT): Description of the website.

    **5. `payment_gateways`**

    - `payment_gateways_id` (INT AUTO_INCREMENT PRIMARY KEY): Unique identifier for each payment gateway.
    - `website_id` (INT NOT NULL): Foreign key referencing the `websites` table.
    - `gateway` (VARCHAR(50) NOT NULL): Payment gateway used on the website (e.g., PayPal, Stripe).

    **6. `languages`**

    - `language_id` (INT AUTO_INCREMENT PRIMARY KEY): Unique identifier for each language.
    - `website_id` (INT NOT NULL): Foreign key referencing the `websites` table.
    - `language` (VARCHAR(50) NOT NULL): Language of the website (e.g., English, Spanish).

    ## Foreign Key Constraints

    - `social_media`: `website_id` references `websites.website_id`.
    - `tech_stack`: `website_id` references `websites.website_id`.
    - `meta`: `website_id` references `websites.website_id`.
    - `payment_gateways`: `website_id` references `websites.website_id`.
    - `languages`: `website_id` references `websites.website_id`.

## Query for Retrieving Data

```bash
  sql
SELECT 
    w.website_id,
    w.url,
    w.category,
    l.language,
    m.title,
    m.description,
    ts.technology,
    pg.gateway,
    sm.platform,
    sm.link
FROM 
    websites w
LEFT JOIN social_media sm ON w.website_id = sm.website_id
LEFT JOIN tech_stack ts ON w.website_id = ts.website_id
LEFT JOIN meta m ON w.website_id = m.website_id
LEFT JOIN payment_gateways pg ON w.website_id = pg.website_id
LEFT JOIN languages l ON w.website_id = l.website_id;
```



5. **Run the script:**
   - Execute the Python script. It will fetch data from the specified list of URLs and store it in the database.
