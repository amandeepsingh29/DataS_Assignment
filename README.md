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

1. **Create a MySQL database:** Create a database named `webscp` or create with any other name but remember to change the name of database in connect_to_database() function.
2. **Configure database connection:**
   - Update the `connect_to_database()` function in the script with your MySQL server details (host, user, password).
3. **Create database tables:**
   - The script creates the following tables:
     - `websites`: Stores website URL and category.
     - `social_media`: Stores social media links for each website.
     - `tech_stack`: Stores the technology stack used on each website.
     - `meta`: Stores the title and description of each website.
     - `payment_gateways`: Stores the payment gateways used on each website.
     - `languages`: Stores the language of each website.
4. **Run the script:**
   - Execute the Python script. It will fetch data from the specified list of URLs and store it in the database.

## Usage

1. **Modify the `website_urls` list:** Add or remove URLs to target specific websites.
2. **Run the script:** Execute the script to extract and store data.

## Example

```python
# Example usage
website_urls = [
    'https://www.google.com',
    'https://www.amazon.com',
    'https://www.facebook.com',
    # ... add more URLs
]

# ... rest of the script