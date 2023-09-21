"""Fragile warning! Tests that serach() comes up with the right results.

Because this checks against existing results, these tests are necessarily 
fragile. 
If you want things to get automatically tested (e.g. every time you push
origin), I would do that with test_listing and test_make_url, but not this.
"""


import pytest
from ..trademe.search import search
from .helpers import listing_match


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
def test_sale_number_close():
    # Should only be higher (my code counts duplicate listings, but the number 
    # I paste in from TradeMe search results doesn't)
    assert len(sale_listings) in (28, 29, 30, 31, 32)


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

