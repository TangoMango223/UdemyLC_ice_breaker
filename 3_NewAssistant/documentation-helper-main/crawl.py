# Let's try this

from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv


# Get envs:
load_dotenv()

# Initialize the FirecrawlApp with your API key
app = FirecrawlApp(api_key= os.environ["FIRECRAWL_API_KEY"])

# Scrape a single URL
url = 'https://python.langchain.com/v0.2/docs/integrations/chat/'
scraped_data = app.scrape_url(url)

# Crawl a website
crawl_url = 'https://python.langchain.com/v0.2/docs/integrations/chat/'
crawl_params = {
    'crawlerOptions': {
        'excludes': ['blog/*'],
        'includes': [], # leave empty for all pages
        'limit': 5,
    }
}

# Complete the crawl
crawl_result = app.crawl_url(crawl_url, params=crawl_params)

print(crawl_result)