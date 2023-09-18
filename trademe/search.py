"""Contains methods for searching TradeMe, search() and make_url().
"""


from urllib.parse import urlparse, parse_qs, urlencode

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from .constants import SUPER_FEATURE_TAG, PREMIUM_TAG, NORMAL_TAG
from .listing import Listing


# Public methods: -------------------------------------------------------------


def search(
        timeout=None, 
        driver_arguments=["--headless=new", "--start-maximized"], 
        *urls
        ):
    """Searches TradeMe using URLs. 
    
    For each URL, search() paginates until it can't find any more listings, 
    then returns.
    
    Note: search() uses a Chrome webdriver, so it's recommended you have 
    the relevant Chrome drivers downloaded in advance.

    Args:
        timeout: The implicit wait used (in seconds) for the Selenium webdriver
            under the hood.
        driver_arguments: The arguments set for the webdriver.
        *urls: URL strings to be treated as the first page of a set of search
            results, which search() will paginate over.

    Returns:
        A list of Listing objects.
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

    # Use the right constructors to make listings 
    # This for loop is band-aid code, ideally this is map() or list comp:
    all_listings = []
    for url_soups in all_soups:
        for page_soup in url_soups:
            all_listings.extend(_page_soup_to_listings(page_soup))

    return all_listings


def make_url(
        sale_or_rent: str, region: str = "", district: str = "",
        suburb: str = "", **kwargs
):
    """Make URL for search() from search criteria.

    Note there is no data validation for region, district, or suburb names, or
    for kwargs.

    Also note that two-word locations should be spelled with dashes (not
    spaces), e.g. instead of suburb="Aro Valley", do suburb="aro-valley".
    Capitalisation doesn't matter.

    Valid kwargs:
    For rent or sale searches:
        *Integers*:
        - bathrooms_min
        - bathrooms_max
        - bedrooms_min
        - bedrooms_max
        - price_min
        - price_max
        *Other*
        - property_type; can be apartment, carpark, house, townhouse, unit
        - adjacent_suburbs; true/false
        - search_string; can be any string, e.g. "Comprende"
    For rent searches only:
        - available_now; true/false
        - pets_ok; true/false
    For sale searches only:
        - open_homes; true/false
        - new_homes; true/false
    """
    # Handle illegal location (region, district, suburb) inputs:
    # The only legal inputs are:
    # 1. region, district, suburb
    # 2. region, district
    # 3. suburb
    # 4. None of those
    if ((region and district and suburb) or (region and district) or region) \
        == False: 
        # ^ Order of this line is crucial due to short circuit operators.
        if not (region and district and suburb == False):  
            raise ValueError(
                "The only legal inputs are: \
                1. region, district, suburb \
                2. region, district \
                3. suburb \
                4. None of those"
            )
    
    # Check sale_or_rent really is "sale" or "rent":
    if sale_or_rent.lower() not in ("sale", "rent"): 
        raise ValueError("sale_or_rent must be 'sale' or 'rent'.")

    # Starts with sale_or_rent, the only required argument (and first one):
    url = f"https://www.trademe.co.nz/a/property/residential/{sale_or_rent}"
    
    # Append location arguments:
    for arg in (region, district, suburb):
        if arg: url += f"/{arg}"  
        # ^ Crucial that this ONLY happens when arg is Truthy; TradeMe messes
        #   up otherwise (double slashes always take you to the home page).

    # Append this thing, which we need:
    url += "/search?"

    # Handle kwargs:
    # Note that it's also crucial that this happens last; kwargs come at the 
    # end of the URL.
    kwarg_number = 1
    for k, v in kwargs.items():
        # If it's the first kwarg, you don't need to add a "&":
        if kwarg_number == 1:
            url += f"{k}={v}"
        else:
            url += f"&{k}={v}"
        kwarg_number += 1
    
    return url


# Private helper methods: -----------------------------------------------------


def _page_soup_to_listings(page_soup):
    """Converts a page result BeautifulSoup object to a list of Listings."""
    listings = []

    # Find listings: returns ResultSets
    super_features = page_soup.find_all(SUPER_FEATURE_TAG)
    premiums = page_soup.find_all(PREMIUM_TAG)
    normals = page_soup.find_all(NORMAL_TAG)

    # Call constructors:
    super_listings = [Listing.from_super_feature(s) for s in super_features]
    premium_listings = [Listing.from_premium_listing(p) for p in premiums]
    normal_listings = [Listing.from_normal_listing(n) for n in normals]

    # Append Listing objects to list;
    listings.extend(super_listings)
    listings.extend(premium_listings)
    listings.extend(normal_listings)

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
        page_soup = BeautifulSoup(page_source, features="html.parser")

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
    """Checks if page displays a "No results found" message: if so, returns 
    False.
    """
    has_next_page = True

    try:
        no_results = page_soup.find("h2", class_="tm-no-results__heading")
        if "no results found" in no_results.string.lower():
            has_next_page = False
    except AttributeError:  # i.e. if doing None.string.lower()
        pass  # keep has_next_page as True

    return has_next_page

