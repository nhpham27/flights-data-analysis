import io, time, json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def retrieve_html(url):
    """
    Return the raw HTML at the specified URL.

    Args:
        url (string): 

    Returns:
        status_code (integer):
        raw_html (string): the raw HTML content of the response, properly encoded according to the HTTP headers.
    """
    
    try:
        data = requests.get(url)
    except Exception as x:
        return None
    return (data.status_code, data.text)

def location_search_params(api_key, location, **kwargs):
    """
    Construct url, headers and url_params. Reference API docs (link above) to use the arguments
    """
    # What is the url endpoint for search?
    url = 'https://api.yelp.com/v3/businesses/search'
    # How is Authentication performed?
    headers = {'Authorization' : 'Bearer ' + api_key}
    # SPACES in url is problematic. How should you handle location containing spaces?
    location = location.replace(' ', '+')
    url_params = {'location' : location}
    # Include keyword arguments in url_params
    url_param = url_params.update(kwargs.items()) 
    
    return url, headers, url_params

def paginated_restaurant_search_requests(api_key, location, total):
    """
    Returns a list of tuples (url, headers, url_params) for paginated search of all restaurants
    Args:
        api_key (string): Your Yelp API Key for Authentication
        location (string): Business Location
        total (int): Total number of items to be fetched
    Returns:
        results (list): list of tuple (url, headers, url_params)
    """
    # HINT: Use total, offset and limit for pagination
    # You can reuse function location_search_params(...)
    request_list = []
    # What is the url endpoint for search?
    url = 'https://api.yelp.com/v3/businesses/search'
    # How is Authentication performed?
    headers = {'Authorization' : 'Bearer ' + api_key}
    # SPACES in url is problematic. How should you handle location containing spaces?
    no_space_location = location.replace(' ', '+')
    temp = total
    curr_offset = 0
    limit = 10
    categories = 'restaurants'
    while True:
        url_params = {'location' : no_space_location}
        # Include keyword arguments in url_params
        request_list.append(location_search_params(api_key, 
                                                   location, 
                                                   offset=curr_offset, 
                                                   limit=limit, 
                                                   categories=categories))
        if total - curr_offset <= limit:
            break
        curr_offset += 10

    return request_list
    
#     return 

def parse_api_response(data):
    """
    Parse Yelp API results to extract restaurant URLs.
    
    Args:
        data (string): String of properly formatted JSON.

    Returns:
        (list): list of URLs as strings from the input JSON.
    """
    
    #[YOUR CODE HERE]
    if isinstance(data, str):
        temp = json.loads(data)
        links = list(map(lambda x:x["url"], temp["businesses"]))
    else:
        links = list(map(lambda x:x["url"], data["businesses"]))
    return links

def parse_page(html):
    """
    Parse the reviews on a single page of a restaurant.
    
    Args:
        html (string): String of HTML corresponding to a Yelp restaurant

    Returns:
        tuple(list, string): a tuple of two elements
            first element: list of dictionaries corresponding to the extracted review information
            second element: URL for the next page of reviews (or None if it is the last page)
    """
    soup = BeautifulSoup(html,'html.parser')
    url_next = soup.find('link',rel='next')
    if url_next:
        url_next = url_next.get('href')
    else:
        url_next = None

    reviews = soup.find_all('div', itemprop="review")
    reviews_list = []
    # HINT: print reviews to see what http tag to extract
    for review in reviews:
        review_item = {}
        for tag in review.find_all("meta"):
            if tag['itemprop'] == "author":
                review_item.update({'author':tag['content']})
            if tag['itemprop'] == "ratingValue":
                review_item.update({'rating':float(tag['content'])})
            if tag['itemprop'] == "datePublished":
                review_item.update({'date':tag['content']})
        description_tag = review.find("p", itemprop="description")
        review_item.update({'description':description_tag.getText()})
        reviews_list.append(review_item)
    return reviews_list, url_next

# 4% credits
def extract_reviews(url, html_fetcher):
    """
    Retrieve ALL of the reviews for a single restaurant on Yelp.

    Parameters:
        url (string): Yelp URL corresponding to the restaurant of interest.
        html_fetcher (function): A function that takes url and returns html status code and content
        

    Returns:
        reviews (list): list of dictionaries containing extracted review information
    """
    reviews = []
    #[YOUR CODE HERE]
    code, html = html_fetcher(url)
    # HINT: Use function `parse_page(html)` multiple times until no next page exists
    #[YOUR CODE HERE]
    while code == 200:
        arr, next_url = parse_page(html)
        reviews += arr
        if next_url is None:
            break
        code, html = html_fetcher(next_url)
    
    return reviews