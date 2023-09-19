"""Tests make_url() and search().

Note that testing search() is necessarily fragile (because search results 
change), but make_url() is not.
"""


import pytest
from trademe.search import search, make_url
from trademe.listing import Listing


# Helper: NOT SURE IF THIS WILL ACTUALLY BE USEFUL, BUT IT'S THE RIGHT IDEA.
def _listing_match(listing: Listing, **kwargs):
    for k, v in kwargs.items():
        assert listing.k == v


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
    assert make_url("rent", "Wellington", "Wellington", "aro-valley").lower() == "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/aro-valley"
    # 1 - sale
    assert make_url("sale", "Wellington", "Wellington", "aro-valley").lower() == "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley"
    # 1 - kwargs
    assert make_url("sale", "Wellington", "Wellington", "aro-valley", price_min=100000, bedrooms_min=1) in ("https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/search?price_min=100000&bedrooms_min=1", "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/search?bedrooms_min=1&price_min=100000")

    # 2 - rent
    assert make_url("rent", "wellington", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington"
    # 2 - sale
    assert make_url("sale", "wellington", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington"
    # 2 - kwargs
    assert make_url("rent", "wellington", "wellington", property_type="townhouse", pets_ok="true").lower() in ("https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?property_type=townhouse&pets_ok=true", "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?pets_ok=true&property_type=townhouse")

    # 3 - rent
    assert make_url("rent", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/rent/wellington"
    # 3 - sale
    assert make_url("sale", "wellington").lower() == "https://www.trademe.co.nz/a/property/residential/sale/wellington"
    # 3 - kwargs
    assert make_url("sale", "wellington", open_homes="true", price_max="650000") in  ("https://www.trademe.co.nz/a/property/residential/sale/wellington/search?open_homes=true&price_max=650000", "https://www.trademe.co.nz/a/property/residential/sale/wellington/search?price_max=650000&open_homes=true")

    # 4 - rent
    assert make_url("rent").lower() == "https://www.trademe.co.nz/a/property/residential/rent/search"
    # 4 - sale
    assert make_url("sale").lower() == "https://www.trademe.co.nz/a/property/residential/sale/search"
    # 4 - kwargs
    assert make_url("rent", propert_type="apartment", price_max=700) in ("https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?property_type=apartment&price_max=700", "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?price_max=700&property_type=apartment")


# Testing search() ------------------------------------------------------------

# Tests search() by doing searches, and matching a) number of results, and b)
# features of particular results.

# Needs to cover:
# - Single page of results AND multiple pages.
# - All kinds of listings (super feature, premium listing, normal lisitngs).
# - Sale AND rent.
# - Using kwargs.

# Ideal cases:
# one page, all 3 kinds of listing
# multi page, all 3 kinds of listing
# one of the above for sale, one for rent; both using 2+ kwargs


def _listing_match(listing: Listing, **kwargs):
    matches = True
    for k, v in kwargs.items():
        if listing.k != v:  # Can do this becaues all attrs are str
            matches = False
            break
    return matches


# For searches with one page of results:


def test_single_page_sale():
    # Gives us all three kinds of listings on one page.
    url = make_url("sale", "wellington", "wellington", "wellington-central", adjacent_suburbs="true", bedrooms_min=3, parking_min=1, price_min=1700000)
    listings = search(urls=url)

    # Check number of results:
    assert len(listings) == 17

    # Check each kind of listing:

    # - Super feature
    super_feature = {
        "title": "GREAT EXPECTATIONS - FULFILLED!",
        "address": "Mount Victoria, Wellington",
        "price": "Enquiries over $1,895,000",
        "features": "4 bedrooms. 2 bathrooms. floor area 175 meters square. land area 239 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/newtown/listing/4330039465",
        "availability": None,
        "agent": " Bill Mathieson & Angela Liu",
        "agency": "Tommy's Real Estate Limited, (Licensed: REAA 2008)"
    }
    assert any([_listing_match(l, **super_feature) for l in listings])

    # - Premium
    premium_listing = {
        "title": "Hataitai Home & Income or The Perfect Family Home",
        "address": "118 Overtoun Terrace, Hataitai, Wellington",
        "price": "For sale by tender",
        "features": "4 bedrooms. 4 bathrooms. floor area 319 meters square. land area 701 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/hataitai/listing/4310826745",
        "availability": None,
        "agent": " Stuart Gray ",
        "agency": "Ray White Group Leaders Wellington"
    }
    assert any([_listing_match(l, **premium_listing) for l in listings])

    # - Normal
    normal_listing = {
        "title": "5 Reasons To Snap Up This CBD Character H+I Beauty",
        "address": " Aurora Terrace, Kelburn, Wellington",
        "price": "Price by negotiation",
        "features": "5 bedrooms. 2 bathrooms. floor area 180 meters square. land area 326 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/kelburn/listing/4308285412",
        "availability": None,
        "agent": None,
        "agency": "SELL WELLINGTON Real Estate"
    }
    assert any([_listing_match(l, **normal_listing) for l in listings])


def test_single_page_rent():
    # Searching for Newtown only tests for premium and normal listings.
    url = make_url("rent", "wellington", "wellington", "newtown", bedrooms_min=2, bedrooms_max=3, price_min=600)
    listings = search(urls=url)

    # Check number of results:
    assert len(listings) == 18

    # Check each kind of listing:

    # - Premium
    premium_listing = {
        "title": "22D Hall Street, Newtown, Wellington",
        "address": None,
        "price": "$620 per week",
        "features": "2 bedrooms. 1 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/newtown/listing/4330039465",
        "availability": "Available: Wed, 18 Oct",
        "agent": " Anita O'Brien ",
        "agency": "Powell & Co Property Management"
    }
    assert any([_listing_match(l, **premium_listing) for l in listings])
    
    # - Normal lisitng
    normal_listing = {
        "title": "23 Paeroa Street, Newtown, Wellington",
        "address": None,
        "price": "$1,100 per week",
        "features": "3 bedrooms. 2 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/newtown/listing/4260348138",
        "availability": "Available: Sat, 13 Apr",
        "agent": " myRent.co.nz ",
        "agency": "myRent.co.nz Ltd"
    }
    assert any([_listing_match(l, **normal_listing) for l in listings])


# For searches with multiple pages of results:


def test_multiple_pages_sale():
    """Blatant copy+paste from single page, but looks for the same listings. 
    
    Changed URL so that it includes more search results.
    """
    # Gives us all three kinds of listings on one page.
    url = make_url("sale", "wellington", "wellington", "wellington-central", adjacent_suburbs="true", bedrooms_min=3, parking_min=1, price_min=1100000)
    listings = search(urls=url)

    # Check number of results:
    assert len(listings) == 36

    # Check each kind of listing:

    # - Super feature
    super_feature = {
        "title": "GREAT EXPECTATIONS - FULFILLED!",
        "address": "Mount Victoria, Wellington",
        "price": "Enquiries over $1,895,000",
        "features": "4 bedrooms. 2 bathrooms. floor area 175 meters square. land area 239 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/newtown/listing/4330039465",
        "availability": None,
        "agent": " Bill Mathieson & Angela Liu",
        "agency": "Tommy's Real Estate Limited, (Licensed: REAA 2008)"
    }
    assert any([_listing_match(l, **super_feature) for l in listings])

    # - Premium
    premium_listing = {
        "title": "Hataitai Home & Income or The Perfect Family Home",
        "address": "118 Overtoun Terrace, Hataitai, Wellington",
        "price": "For sale by tender",
        "features": "4 bedrooms. 4 bathrooms. floor area 319 meters square. land area 701 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/hataitai/listing/4310826745",
        "availability": None,
        "agent": " Stuart Gray ",
        "agency": "Ray White Group Leaders Wellington"
    }
    assert any([_listing_match(l, **premium_listing) for l in listings])

    # - Normal
    normal_listing = {
        "title": "5 Reasons To Snap Up This CBD Character H+I Beauty",
        "address": " Aurora Terrace, Kelburn, Wellington",
        "price": "Price by negotiation",
        "features": "5 bedrooms. 2 bathrooms. floor area 180 meters square. land area 326 meters square.",
        "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/kelburn/listing/4308285412",
        "availability": None,
        "agent": None,
        "agency": "SELL WELLINGTON Real Estate"
    }
    assert any([_listing_match(l, **normal_listing) for l in listings])


def test_multiple_pages_rent():
    """Again, partly copy+pasted from single page rent test.
    
    BUT:
    - Changed URL for more results (multiple pages).
    - Added super feature.
    """ 
    # Searching for Newtown only tests for premium and normal listings.
    url = make_url("rent", "wellington", "wellington", "newtown", bedrooms_min=1, bathrooms_min=1)
    listings = search(urls=url)

    # Check number of results:
    assert len(listings) == 46  # CHANGE THIS BIT

    # Check each kind of listing:

    # - Super feature
    super_feature = {
        "title": "Newtown",
        "address": None,
        "price": "$1,350 per week",
        "features": "5 bedrooms. 1 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/newtown/listing/4320850329",
        "availability": "Available: Now",
        "agent": None,
        "agency": None
    }
    assert any([_listing_match(l, **super_feature) for l in listings])

    # - Premium
    premium_listing = {
        "title": "22D Hall Street, Newtown, Wellington",
        "address": None,
        "price": "$620 per week",
        "features": "2 bedrooms. 1 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/newtown/listing/4330039465",
        "availability": "Available: Wed, 18 Oct",
        "agent": " Anita O'Brien ",
        "agency": "Powell & Co Property Management"
    }
    assert any([_listing_match(l, **premium_listing) for l in listings])
    
    # - Normal lisitng
    normal_listing = {
        "title": "23 Paeroa Street, Newtown, Wellington",
        "address": None,
        "price": "$1,100 per week",
        "features": "3 bedrooms. 2 bathrooms.",
        "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/newtown/listing/4260348138",
        "availability": "Available: Sat, 13 Apr",
        "agent": " myRent.co.nz ",
        "agency": "myRent.co.nz Ltd"
    }
    assert any([_listing_match(l, **normal_listing) for l in listings])

