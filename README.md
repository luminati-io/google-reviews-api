# Google Reviews API

This repository provides two approaches for collecting Google Reviews data:

1. **Free Scraper**: A lightweight solution for small-scale projects, testing, personal research, and educational purposes.
2. **Bright Data Google Reviews API**: A robust, high-volume solution for enterprise-level, scalable, and reliable data extraction. Part of the [SERP API](https://brightdata.com/products/serp-api).

## Table of Contents

- [Free Scraper](#free-scraper)
   - [Setup](#setup)
   - [Quick Start](#quick-start)
   - [Sample Output](#sample-output)
   - [Limitations](#limitations)
- [Bright Data Enterprise Solution](#bright-data-enterprise-solution)
   - [Getting Started](#getting-started)
   - [Direct API Access](#direct-api-access)
   - [Native Proxy-Based Access](#native-proxy-based-access)
- [Advanced Features](#advanced-features)
   - [Feature ID (fid)](#feature-id-fid)
   - [Localization (hl)](#localization-hl)
   - [Sorting and Filtering](#sorting-and-filtering)
   - [Pagination](#pagination)
- [Support & Resources](#support--resources)

## Free Scraper
A quick-and-easy scraper for those who need to extract reviews on a smaller scale.

<img width="700" alt="scrape-google-reviews-pizza-place" src="https://github.com/luminati-io/google-reviews-api/blob/main/images/420648584-8f8069c4-3521-49d1-ba77-8eb6e840de2b.png" />

### Setup

**Requirements:**

- Python 3.9 or higher
- [Playwright](https://playwright.dev/) for browser automation

**Installation:**

```bash
pip install playwright
playwright install
```

> **New to web scraping?** Check out our [Beginner's Guide to Web Scraping with Python](https://brightdata.com/blog/how-tos/web-scraping-with-python).
> 

### Quick Start

1. Open [google-reviews-scraper.py](https://github.com/luminati-io/Google-Reviews-API/blob/main/google-reviews-scraper/google-reviews-scraper.py) and update the following variables:
    - `url` – The Google Maps URL of the business.
    - `target_reviews` – The number of reviews to scrape.
2. Run the script.

💡 **Pro Tip:** Set `HEADLESS = False` to reduce detection by Google's anti-scraping systems.

### Sample Output

```json
{
    "reviewer_name": "Christopher Huntley (youcancallmemaurice)",
    "reviewer_link": "https://www.google.com/maps/contrib/116348973042381100705/reviews?hl=en-GB",
    "reviewer_image": "https://lh3.googleusercontent.com/a-/ALV-UjXgKzymRM7WTYFkhDuA2_lN5WfE7EYAoBAFPOf2YGxA1e_s72zD9A=w36-h36-p-rp-mo-ba5-br100",
    "rating": 5,
    "date": "a month ago",
    "text": "We took a local tip for the best pizza in Chicago. It's a dive vibe with a very regimented process. The garlic bread was good and the dipping sauce was a nice touch.\n\nPizza came fairly quickly. A standard deep dish with sausage, onion and pepper. Good crust, good flavor for sauce and toppings were perfect.\n\nService was quick and attentive. A great experience.",
    "photos": [
        "https://lh3.googleusercontent.com/geougc-cs/AIHozJIkCwzdm33OdIVsHIJcqdLPauk-Q3Xk0rRjj4SrzOaiMF1L_uQFW4T7jg86meLyB6So7wsJX0Pk6m8NuxUbUF_1OTvutnqJbmwU2olmmiS5Z1A6puOo8oPD6qqBSG0TXO5KyM_B=w300-h450-p",
        "https://lh3.googleusercontent.com/geougc-cs/AIHozJKiYAPlUmW7O1M79DDjuRgbeOJ92t2IqwuUDOXUFOABH6XBoZet4bGsYV_NxK1z2SkaFLktjjaAs1FoI2XMEwjt9uMZKQX2K904RjyymLZ1SA4LKq_a3vttOPJr7bMTJCpEx-Y=w300-h225-p",
        "https://lh3.googleusercontent.com/geougc-cs/AIHozJKvdP93huqqhLlxZZDv3VKpNYVriS8qq8lKoGiFydTTDAgZOtupYcgxfaSu4KPbE4wX16lD4sXMOY10vLRVk8_mrMe2N4Ul9hX1h46-JJ0rCmZcDcXogMr_YlIDIp_ao_S_wxVQgQ=w300-h225-p"
    ],
    "likes_count": "4"
}
```

👉 See the [full JSON output](https://github.com/luminati-io/Google-Reviews-API/blob/main/google-reviews-results/reviews_output.json).


### Limitations

The Free Scraper comes with significant constraints:

- High risk of IP blocks
- Limited request volume
- Frequent CAPTCHAs
- Unreliable for large-scale scraping

You'll need a more advanced solution for reliable, large-scale data collection.

## Bright Data Enterprise Solution

[Bright Data's Google Reviews API](https://brightdata.com/products/serp-api/google-search/reviews) provides structured Google Reviews data with advanced features and scalability. Built on the same advanced technology as the [SERP API](https://brightdata.com/products/serp-api), it offers:

- **Global Location Accuracy:** Tailor results to any location
- **Pay-Per-Success Model:** Only pay for successful requests
- **Real-Time Data:** Get up-to-date reviews in seconds
- **Scalability:** Handle unlimited requests with no volume restrictions
- **Cost Efficiency:** Save on infrastructure and maintenance costs
- **Highest Reliability:** Consistent performance with built-in anti-blocking measures
- **Technical Support:** Expert assistance available when needed

### Getting Started

1. **Prerequisites:**
    - Create a [Bright Data account](https://brightdata.com/) (new users get $5 credit)
    - Obtain your [API key](https://docs.brightdata.com/general/account/api-token)
2. **Setup:** Follow our [step-by-step guide](https://github.com/luminati-io/Google-Reviews-API/blob/main/setup-serp-api-guide.md) to integrate the API
3. **Implementation Methods:**
    - Direct API Access
    - Native Proxy-Based Access

### Direct API Access

Make a direct request to the API endpoint.

**cURL Example:**

```bash
curl https://api.brightdata.com/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_TOKEN" \
  -d '{
        "zone": "ZONE_NAME",
        "url": "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&brd_json=1",
        "format": "raw"
      }'
```

**Python Example:**

```python
import requests
import json

url = "https://api.brightdata.com/request"
headers = {"Content-Type": "application/json", "Authorization": "Bearer API_TOKEN"}

payload = {
    "zone": "ZONE_NAME",
    "url": "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&brd_json=1",
    "format": "raw",
}

response = requests.post(url, headers=headers, json=payload)

with open("serp-direct-api.json", "w") as file:
    json.dump(response.json(), file, indent=4)

print("Response saved to 'serp-direct-api.json'.")
```

👉 See the [full JSON output](https://github.com/luminati-io/Google-Reviews-API/blob/main/google-reviews-api-results/serp-direct-api.json).

> **Note:** Use `brd_json=1` for parsed JSON or `brd_json=html` for parsed JSON + full nested HTML.
> 

### Native Proxy-Based Access

You can also use our proxy routing method:

**cURL Example:**

```bash
curl -i \
  --proxy brd.superproxy.io:33335 \
  --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
  -k \
  "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&brd_json=1"
```

**Python Example:**

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = "brd.superproxy.io"
port = 33335
username = "brd-customer-<customer-id>-zone-<zone-name>"
password = "<zone-password>"
proxy_url = f"http://{username}:{password}@{host}:{port}"

proxies = {"http": proxy_url, "https": proxy_url}
url = "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&brd_json=html"
response = requests.get(url, proxies=proxies, verify=False)

with open("serp-native-proxy.json", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Response saved to 'serp-native-proxy.json'.")
```

👉 See the [full JSON output](https://github.com/luminati-io/Google-Reviews-API/blob/main/google-reviews-api-results/serp-native-proxy.json).

> **Note:** For production environments, load Bright Data's SSL certificate as described in our [SSL Certificate Guide](https://docs.brightdata.com/general/account/ssl-certificate).
>

## Advanced Features
Bright Data's API supports several advanced parameters for fine-tuning your review extraction.

### Feature ID (fid)
<img width="700" alt="scrape-google-reviews-building" src="https://github.com/luminati-io/google-reviews-api/blob/main/images/420657506-0bc3b223-adf4-487a-9c75-11679b16907d.png" />

The feature ID is a unique identifier for the business or location. To find it:

1. Perform a Google search for the business name
2. View the source code of the search results page (right-click and select "View Page Source")
3. Search for "data-fid" within the page
4. The fid will appear in a format like: `"fid":"0x89c259a9b3117469:0xd134e199a405a163"`

### Localization (hl)

<img width="700" alt="google-reviews-scraper-building" src="https://github.com/luminati-io/google-reviews-api/blob/main/images/420665500-0f1b630e-cb2a-4125-a7de-64be656a2f5b.png" />

Specifies the preferred language using a two-letter language code.

**Example:**

```bash
curl --proxy brd.superproxy.io:33335 \
     --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
     "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&hl=fr"
```

This example returns reviews in French.

### Sorting and Filtering

You can sort and filter reviews using query parameters:

1. **sort**: Determines how reviews are sorted.
  
    **Possible values:**
    
    - `sort=qualityScore` (default) - Most relevant reviews first
    - `sort=newestFirst` - Newest reviews first
    - `sort=ratingHigh` - Highest rated reviews first
    - `sort=ratingLow` - Lowest rated reviews first
    
    **Example:**
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
         "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&sort=ratingLow"
    ```
    
    This example returns the lowest-rated reviews first.

2. **filter**: Filters reviews containing a specific keyword.

    **Example:**
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
         "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&filter=excellent"
    ```
    
    This example returns only reviews containing the word "excellent".

### Pagination

Control the number of results and manage pagination with these parameters:

1. **start**: Defines the result offset to manage pagination.
    - `start=0` (default) - First page of results
    - `start=10` - Second page of results
    - `start=20` - Third page of results
    
    **Example:**
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
         "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&start=10"
    ```
    
    This example returns the second page of reviews.
    
2. **num**: Defines the number of results to return per page.
    - `num=10` (default) - Returns 10 results
    - `num=20` - Returns 20 results (maximum)
    
    **Example:**
    
    ```bash
    curl --proxy brd.superproxy.io:33335 \
         --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
         "https://www.google.com/reviews?fid=0x89c259a9b3117469:0xd134e199a405a163&num=20"
    ```
    
    This example returns 20 reviews in one request.

## Support & Resources

- **Documentation**: [SERP API Docs](https://docs.brightdata.com/scraping-automation/serp-api/)
- **SEO Use Cases**: [SEO Tracking and Insights](https://brightdata.com/use-cases/serp-tracking)
- **Additional Guides**: [Web Unlocker API](https://github.com/luminati-io/web-unlocker-api), [SERP API](https://github.com/luminati-io/serp-api), [Google Search API](https://github.com/luminati-io/google-search-api), [Google News Scraper](https://github.com/luminati-io/Google-News-Scraper), [Google Trends API](https://github.com/luminati-io/google-trends-api)
- **Technical Articles**:
    - [Best SERP APIs](https://brightdata.com/blog/web-data/best-serp-apis)
    - [Build a RAG Chatbot with SERP API](https://brightdata.com/blog/web-data/build-a-rag-chatbot)
- **Technical Support**: [Contact Us](mailto:support@brightdata.com)
