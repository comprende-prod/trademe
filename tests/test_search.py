"""Tests make_url() and search().

Note that testing search() is necessarily fragile (because search results 
change), but make_url() is not.
"""


import pytest
from ..trademe.search import search, make_url
from .helpers import listing_match


# Testing make_url() ----------------------------------------------------------


def test_make_url_raises():
    with pytest.raises(ValueError):
        # sale_or_rent:
        make_url("rente")
        make_url("ssssale")

        # Location args:
        # Bad cases include:
        # 1. region and suburb
        make_url(region="Wellington", suburb="Seatoun")
        # 2. district and suburb
        make_url(district="Wellington", suburb="Seatoun")
        # 3. district
        make_url(district="Wellington")
        # 4. suburb
        make_url(suburb="Seatoun")


def test_make_url():
    """Test valid inputs produce correct output."""
    # Valid cases:
    # 1. region, district, suburb
    # 2. region, district
    # 3. region
    # 4. all((region, district, suburb)) == False

    # For each, check sale and rent work too.

    # For each, check kwargs work.

    # 1 - rent
    assert make_url("rent", "Wellington", "Wellington", "aro-valley").lower() == "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/aro-valley/search?"
    # 1 - sale
    assert make_url("sale", "Wellington", "Wellington", "aro-valley").lower() == "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/search?"
    # 1 - kwargs
    assert make_url("sale", "Wellington", "Wellington", "aro-valley", price_min=100000, bedrooms_min=1).lower() in ("https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/search?price_min=100000&bedrooms_min=1", "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/search?bedrooms_min=1&price_min=100000")

    # 2 - rent
    assert make_url("rent", "wellington", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?"
    # 2 - sale
    assert make_url("sale", "wellington", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/search?"
    # 2 - kwargs
    assert make_url("rent", "wellington", "wellington", property_type="townhouse", pets_ok="true").lower() in ("https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?property_type=townhouse&pets_ok=true", "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?pets_ok=true&property_type=townhouse")

    # 3 - rent
    assert make_url("rent", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/rent/wellington/search?"
    # 3 - sale
    assert make_url("sale", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/sale/wellington/search?"
    # 3 - kwargs
    assert make_url("sale", "wellington", open_homes="true", price_max="650000").lower() in  ("https://www.trademe.co.nz/a/property/residential/sale/wellington/search?open_homes=true&price_max=650000", "https://www.trademe.co.nz/a/property/residential/sale/wellington/search?price_max=650000&open_homes=true")

    # 4 - rent
    assert make_url("rent").lower() == "https://www.trademe.co.nz/a/property/residential/rent/search?"
    # 4 - sale
    assert make_url("sale").lower() == "https://www.trademe.co.nz/a/property/residential/sale/search?"
    # 4 - kwargs
    assert make_url("rent", propert_type="apartment", price_max=700).lower() in ("https://www.trademe.co.nz/a/property/residential/rent/search?property_type=apartment&price_max=700", "https://www.trademe.co.nz/a/property/residential/rent/search?price_max=700&property_type=apartment")


# Testing search() ------------------------------------------------------------


# We want to test:
# - Pagination
# - Ability to construct from all kinds of listings
# - Searching for URLS property (using kwargs etc)
# - Rent AND sale.

# Therefore, we test for the following searches: 
# - Rent listing; multiple pages; multiple kinds of listing; 
#   complex search criteria.
# - Sale listing; multiple pages; multiple kinds of listing;
#   complex search criteria.


# Do search:
# - Sale
sale_url = make_url("sale", "wellington", "wellington", "aro-valley", adjacent_suburbs="true", price_min=1600000, bedrooms_min=1)
#sale_listings = search(urls=sale_url)
sale_listings = search(None, ["--headless=new", "--start-maximized"], sale_url)
# - Rent
rent_url = make_url("rent", "wellington", "wellington", price_min=1074, bedrooms_min=3, bedrooms_max=5)
rent_listings = search(None, ["--headless=new", "--start-maximized"], rent_url)


# Sale tests:
def test_sale_number_results():
    assert len(sale_listings) == 28


def test_sale_super_feature_present():
    sale_super_feature = {
        "title": "GREAT EXPECTATIONS - FULFILLED!",
        "address": "Mount Victoria, Wellington",
        "price": "Enquiries over $1,895,000",
        "features": "4 bedrooms. 2 bathrooms. floor area 175 meters square. land area 239 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/mount-victoria/listing/4322275169?rsqid=9e5e441bc00a4ae8a747db30a159d6d6-006",
        "availability": None,
        "agent": " Bill Mathieson & Angela Liu",
        "agency": "Tommy's Real Estate Limited, (Licensed: REAA 2008)"
    }
    assert any([listing_match(sl, **sale_super_feature) for sl in sale_listings])

def test_sale_premium_present():
    sale_premium = {
        "title": "10 Bed - 2 Flat - Loan Interest Deductible",
        "address": "31 Devon Street, Aro Valley, Wellington",
        "price": "Enquiries over $1,650,000",
        "features": "6 bedrooms. 4 bathrooms. floor area 140 meters square. land area 455 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/listing/4212308245?rsqid=9e5e441bc00a4ae8a747db30a159d6d6-006",
        "availability": None,
        "agent": " Paul Dickason & Charles Lindsay ",
        "agency": "Professionals; Redcoats Limited (Wellington City)"
    }
    assert any([listing_match(sl, **sale_premium) for sl in sale_listings])

def test_sale_normal_present():
    sale_normal = {
        "title": "LUXURY PENTHOUSE - HYDE LANE",
        "address": "11 Courtenay Place, Wellington Central, Wellington",
        "price": "Enquiries over $3,880,000",
        "features": "4 bedrooms. 2 bathrooms. floor area 216 meters square.",
        "link": "https://www.trademe.co.nz/a/property/new-homes/new-apartment/wellington/wellington/wellington-central/listing/3381591142?rsqid=533ec8d3e5884ceaa63ce34cbc48cac0-007",
        "availability": None,
        "agent": "No agent name provided.",
        "agency": "Tommy's Real Estate Limited, (Licensed: REAA 2008)"
    }
    assert any([listing_match(sl, **sale_normal) for sl in sale_listings])


# Rent tests:
def test_rent_number_results():
    assert len(rent_listings) == 83

def test_rent_super_feature_present():
    rent_super_feature = {
        "title": "Kelburn",
        "address": None,
        "price": "$1,075 per week",
        "features": "4 bedrooms. 1 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/kelburn/listing/4332207817?rsqid=a11b4f31f800458e84e2696a87a31596-003",
        "availability": "Available: Fri, 1 Dec",
        "agent": " Matt ",
        "agency": "Could not find agency. Probably a private listing."
    }
    assert any([listing_match(rl, **rent_super_feature) for rl in rent_listings])

def test_rent_premium_present():
    rent_premium = {
        "title": "12 Bunker Way, Seatoun Heights, Wellington",
        "address": None,
        "price": "$1,150 per week",
        "features": "5 bedrooms. 2 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/seatoun-heights/listing/4329808730?rsqid=04ca5858016c41d5b4742f5ac5395388-001",
        "availability": "Available: Thu, 19 Oct",
        "agent": " Charmaine Dixon ",
        "agency": "Powell & Co Property Management"
    }
    assert any([listing_match(rl, **rent_premium) for rl in rent_listings])

def test_rent_normal_present():
    rent_normal = {
        "title": "Te Aro, Wellington",
        "address": None,
        "price": "$1,050 per week",
        "features": "4 bedrooms. 1 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/te-aro/listing/4291384317?rsqid=04ca5858016c41d5b4742f5ac5395388-001",
        "availability": "Available: Now",
        "agent": "No agent name provided.",
        "agency": "Clo Property Management Ltd"
    }
    assert any([listing_match(rl, **rent_normal) for rl in rent_listings])

