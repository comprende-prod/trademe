"""Contains methods for searching TradeMe.
"""


from urllib.parse import urlparse, parse_qs, urlencode

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from .constants import LISTING_TAGS, SUPER_FEATURE_TAG, PREMIUM_TAG, NORMAL_TAG
from .listing import Listing


# Public methods: -------------------------------------------------------------


def search_without_async(timeout=None, 
                         driver_arguments=["--headless=new", 
                                           "--start-maximized"], 
                         *urls):
    """Searches TradeMe using URLs. 
    
    For each URL, it paginates until it can't find any other listings, then 
    returns.
    
    Note:
    - This does NOT use asyncio. So it's likely unsuitable slow for large 
      searches.
    - This uses a Chrome webdriver, so it's recommended that you have the 
      relevant Chrome drivers installed.

    Args:
        timeout: The implicit wait used (in seconds) for the Selenium webdriver
            under the hood.
        driver_arguments: The arguments set for the webdriver.
        *urls: NOTE THESE ARE FIRST PAGES AND STUFF!!!

    Returns:
        blah blah blah
    
    Raises:
        Probably an InvalidArgumentError for the selenium driver arguments?
    """
    # Get BeautifulSoups for each page of each URL:
    all_soups = []  # Stores lists of BeautifulSoups for each URL in *urls.
    for url in urls:
        soups = _get_page_soups(
            url, 
            timeout=timeout, 
            driver_arguments=driver_arguments
        )
        all_soups.append(soups)

    print(all_soups[0][1])  # num urls and pages is right

    # Use the right constructors to make listings (doesn't need to be in loop)
    all_listings = \
        [[_page_soup_to_listings(page_soup) for page_soup in url_soups] \
        for url_soups in all_soups]

    return all_listings


# make_suburb_url() and make_kwarg_url() shoudl probably just be one method, 
# but anyway.


def make_suburb_url(sale_or_rent: str, region: str, district: str, suburb: str, 
             **kwargs):
    """Make URL from common search parameters and keyword arguments.
    
    Note that kwargs not validated. 

    Should probably have used urlparse, but I don't have that kinda time bud.

    Some valid kwargs include:
    price_min: minimum price (valid for sale or rent); e.g. price_min=50.
    search_string: what you might type in the search bar; e.g 
        search_string=comprende.

    Args:
        sale_or_rent: Can be "sale" or "rent".
        region: Region searching in, e.g. "wellington", "auckland", etc.
        district: District searching in, e.g. "upper-hutt", "wellington".
        suburb: Suburb searching in, e.g. "aro-valley".

    Returns:
        URL to be used for searching.
    """
    url = f"https://www.trademe.co.nz/a/property/residential/{sale_or_rent}/{region}/{district}/{suburb}/search?"
    if kwargs:  # unsure if this is needed
        kwarg_number = 1
        for k, v in kwargs.items():
            if kwarg_number > 1:
                # If it's not the first kwarg, you need to add "&":
                url += f"&{k}={v}"
            else:
                url += f"{k}={v}"
            kwarg_number += 1  # increment kwarg_number
    return url


def make_kwarg_url(sale_or_rent: str, **kwargs):
    """Like make_suburb_url(), but less stuff."""
    url = f"https://www.trademe.co.nz/a/property/residential/{sale_or_rent}/search?"
    if kwargs:  # unsure if this is needed
        kwarg_number = 1
        for k, v in kwargs.items():
            if kwarg_number > 1:
                # If it's not the first kwarg, you need to add "&":
                url += f"&{k}={str(v)}"
            else:
                url += f"{k}={str(v)}"
            kwarg_number += 1  # increment kwarg_number
    return url  

# Do much later
def search_using_async(timeout=None, driver_arguments=["--headless=new"], 
                       *urls):
    """Uh, coming soon. Idk how to use this stuff yet."""
    pass


# Private helper methods: -----------------------------------------------------


def _page_soup_to_listings(page_soup) -> list[Listing]:
    listings = []
    # Super features:
    super_features = page_soup.find_all(SUPER_FEATURE_TAG)
    if super_features:
        listings.extend(
            [Listing.from_super_feature(s) for s in super_features]
        )

    # Premium listings:
    premium_listings = page_soup.find_all(PREMIUM_TAG)
    if premium_listings:
        listings.extend(
            [Listing.from_premium_listing(p) for p in premium_listings]
        )

    # Normal listings:
    normal_listings = page_soup.find_all(NORMAL_TAG)
    if normal_listings:
        listings.extend(
            [Listing.from_normal_listing(n) for n in premium_listings]
        )
    return listings


def _get_page_soups(url,
                    timeout=None, 
                    driver_arguments=["--headless=new", "--start-maximized"]
                    ) -> list[BeautifulSoup]:
    """For a particular URL, will return a list of BeautifulSoup of each page. 

    Originally, getting page source was decouples from making BeautifulSoups of
    page results. However, because of how convenient it is to use .find() to 
    check for the next page, I've made this method return BeautifulSoups 
    instead.
    
    Args:
        url: URL of search (e.g. a single suburb search).
        timeout: The implicit wait used (in seconds) for the Selenium webdriver
            under the hood.
        driver_arguents: Arguments for the webdriver.
    """
    # Set up driver
    options = ChromeOptions()
    for driver_argument in driver_arguments:
        options.add_argument(driver_argument)
            
    driver = webdriver.Chrome(options=options)

    if timeout: driver.implicitly_wait(timeout)

    # Get source, and paginate
    soups = []
    current_url = url  # current_url set to first page URL.
    has_next_page = True  # set True by default, but this doesn't mess it up.
    while has_next_page:
        # Read source
        driver.get(current_url)
        page_source = driver.page_source
        page_soup = BeautifulSoup(page_source)

        # Check if next page:
        has_next_page = _has_next_page(page_soup)
        
        if has_next_page:
            # If there IS a next page, change current_url for the next loop:
            current_url = _get_next_page_url(current_url)

            # Appending page_soup down here because we don't want to return
            # empty pages:
            soups.append(page_soup)

    # Quit driver
    driver.quit()

    return soups

# Trying a new version:
def _get_next_page_url(current_url):
    """This works, basically by magic."""
    parsed = urlparse(current_url)
    query_dict = parse_qs(parsed.query)

    try:
        # ...to find the current page
        query_dict["page"][0] = int(query_dict["page"][0]) + 1
    except KeyError:
        # Means it's on the first page, so next page needs to be 2.
        query_dict["page"] = [2]

    query_new = urlencode(query_dict, doseq=True)  # No clue
    parsed=parsed._replace(query=query_new)
    next_page_url = (parsed.geturl())  # Not sure why this is in parentheses?

    return next_page_url


def _has_next_page(page_soup):
    """Checks if any of LISTING_TAGS are present in page_soup."""
    has_next_page = False
    if any([page_soup.find(tag) for tag in LISTING_TAGS]):
        has_next_page = True
    return has_next_page

