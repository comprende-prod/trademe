"""Contains single_suburb_search and make_suburb_url, plus helpers."""


import requests
from urllib.parse import urlparse, ParseResult, parse_qs, urlencode
from bs4 import BeautifulSoup
from . import constants
from .listing import Listing


def single_suburb_search(suburb_url, **search_keys):
    """Search TradeMe, one suburb at a time. 
    
    Use make_suburb_url for 'suburb_url'.

    Accepts keywords like 'price_min', 'search_string' (for keywords in
    listings), 'property_type', etc.
    """

    s = requests.Session()

    # Gives us AJAX-loaded HTML:
    headers = {
        #"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "accept": "text/javascript"
    }  

    first_page_response = _get_first_page_response(s, suburb_url, headers, 
                                                   **search_keys)
    
    page_sources = _get_page_sources(s, first_page_response)

    # Get listings from page source
    page_soups = [BeautifulSoup(source) for source in page_sources]

    listings = []

    for page in page_soups:
        # Super features:
        super_features = page.find_all(constants.SUPER_FEATURE_TAG)
        if super_features:
            listings.extend(
                [Listing.from_super_feature(s) for s in super_features]
            )

        # Premium listings:
        premium_listings = page.find_all(constants.PREMIUM_TAG)
        if premium_listings:
            listings.extend(
                [Listing.from_premium_listing(p) for p in premium_listings]
            )

        # Normal listings:
        normal_listings = page.find_all(constants.NORMAL_TAG)
        if normal_listings:
            listings.extend(
                [Listing.from_normal_listing(n) for n in premium_listings]
            )

    # Return listings
    s.close()
    return listings


def make_suburb_url(sale_or_rent: str, region: str, district: str, suburb: str):
    """Helper for making base URL for search. No data validation yet."""
    url = f"https://www.trademe.co.nz/a/property/residential/{sale_or_rent}/{region}/{district}/{suburb}/search?"
    return url    


def _get_first_page_response(s: requests.Session, suburb_url: str, 
                             headers: dict, **search_keys):
    
    r = s.get(url=suburb_url, headers=headers, params=search_keys)
    return r


def _get_page_sources(s: requests.Session, 
                      first_page_response: requests.Response) -> list:

    sources = []

    current_response = first_page_response

    while _has_next_page(current_response):
        # I.e., the current page isn't empty
        # Get source from current page
        source = current_response.text
        sources.append(source)

        # Get next page:
        current_response = _get_next_page(s, current_response)

    return sources


def _get_next_page(s: requests.Session, current_response: requests.Response):
    # (Basically just copied this bit from the internet).

    u = urlparse(current_response.url)
    params = parse_qs(u.query)
    params["page"] += 1
    res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, 
                      params=u.params, query=urlencode(params), 
                      fragment=u.fragment)
    # Get next page:
    next_page_response = s.get(res.geturl())
    
    return next_page_response


def _has_next_page(response: requests.Response):
    """Returns False if this page of search ('response') has no results."""
    has_next_page = False
    for tag in (constants.SUPER_FEATURE_TAG, constants.PREMIUM_TAG, 
                constants.NORMAL_TAG):
        if tag in response.text: has_next_page = True
    return has_next_page

