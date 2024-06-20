import requests
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

website_list = [
    'https://github.com/marcoceppi'
]

def check_scraping_allowed(url):
    
    robots_url = urljoin(url, "robots.txt")
    rp = RobotFileParser()

    try:
        rp.set_url(robots_url)
        rp.read()
        # Correct the usage of can_fetch
        if rp.can_fetch("*", url): 
            return True, f"Scraping likely allowed on {url} (based on robots.txt)."
        else:
            return False, f"Scraping likely disallowed on {url} (based on robots.txt)."
    except Exception as e:
        return None, f"Error checking robots.txt for {url}: {e}"

for website in website_list:
    allowed, message = check_scraping_allowed(website)
    print(message) 