"""Compares search() with TradeMe's online search results.

Therefore, this is *fragile*.

Hence, I'd say that you shouldn't run these automatically e.g. every time you
push origin.
"""


import pytest
from ..trademe.search import search, make_url
from ..trademe.listing import Listing


# Set up search:
# - Set up listing fixtures:
@pytest.fixture(scope="session")
def sale_listings():
    sale_url = make_url("sale", "wellington", "wellington", "aro-valley", adjacent_suburbs="true", price_min=1_600_000, bedrooms_min=1)
    return search(None, ["--headless=new", "--start-maximized"], sale_url)


@pytest.fixture(scope="session")
def rent_listings():
    rent_url = make_url("rent", "wellington", "wellington", price_min=1074, bedrooms_min=3, bedrooms_max=5)
    return search(None, ["--headless=new", "--start-maximized"], rent_url)


# Example listings 
# - Sale
sale_super_feature = {
    "title": "CENTRAL KELBURN TREASURE",
    "address": "Kelburn, Wellington",
    "price": "Enquiries over $2,295,000",
    "features": "5 bedrooms. 3 bathrooms. floor area 235 meters square. land area 889 meters square.",
    "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/kelburn/listing/4335671136?rsqid=713994d3930244788a5d73c19ff960c4-001",
    "availability": None,
    "agent": " Phil Mears ",
    "agency": "Tommy's Real Estate Limited, (Licensed: REAA 2008)"
}
sale_premium = {
    "title": "GREAT EXPECTATIONS - FULFILLED!",
    "address": "Mount Victoria, Wellington",
    "price": "Enquiries over $1,895,000",
    "features": "4 bedrooms. 2 bathrooms. floor area 175 meters square. land area 239 meters square.",
    "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/mount-victoria/listing/4322275169?rsqid=713994d3930244788a5d73c19ff960c4-001",
    "availability": None,
    "agent": " Bill Mathieson & Angela Liu ",
    "agency": "Tommy's Real Estate Limited, (Licensed: REAA 2008)"
}
sale_normal = {
    "title": "LUXURY PENTHOUSE - HYDE LANE",
    "address": "11 Courtenay Place, Wellington Central, Wellington",
    "price": "Enquiries over $3,880,000",
    "features": "4 bedrooms. 2 bathrooms. floor area 216 meters square.",
    "link": "https://www.trademe.co.nz/a/property/new-homes/new-apartment/wellington/wellington/wellington-central/listing/3381591142?rsqid=46b014824eac43949e167b8adbfd745c-002",
    "availability": None,
    "agent": None,
    "agency": "Tommy's Real Estate Limited, (Licensed: REAA 2008)"
}

# - Rent
rent_super_feature = {
    "title": "Kelburn",
    "address": None,
    "price": "$1,075 per week",
    "features": "4 bedrooms. 1 bathrooms.",
    "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/kelburn/listing/4332207817?rsqid=b7754c46e54c4b59a77afac22fb01b4f-001",
    "availability": "Available: Fri, 1 Dec",
    "agent": " Matt ",
    "agency": None
}
rent_premium = {
    "title": "12 Bunker Way, Seatoun Heights, Wellington",
    "address": None,
    "price": "$1,150 per week",
    "features": "5 bedrooms. 2 bathrooms.",
    "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/seatoun-heights/listing/4329808730?rsqid=b7754c46e54c4b59a77afac22fb01b4f-001",
    "availability": "Available: Thu, 19 Oct",
    "agent": " Charmaine Dixon ",
    "agency": "Powell & Co Property Management"
}
rent_normal = {
    "title": "2/2 Sugarloaf Road, Brooklyn, Wellington",
    "address": None,
    "price": "$1,495 per week",
    "features": "5 bedrooms. 1 bathrooms.",
    "link": "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/brooklyn/listing/4300213096?rsqid=737910711316442f82d87c23bd9fac3a-003",
    "availability": "Available: Now",
    "agent": None,
    "agent": "Property Management Wellington"
}


# Check number of results
def test_num_sale_results(sale_listings):
    assert len(sale_listings) in (29, 30, 31, 32)


def test_num_rent_results(rent_listings):
    assert len(rent_listings) in (69, 70, 71, 72)


# Check listing examples in results
@pytest.mark.parametrize(
    "listing", [sale_super_feature, sale_premium, sale_normal]
)
def test_sale_results_present(listing, sale_listings):
    """Test listing dicts above in sale_listings"""
    l = Listing()
    for k, v in listing.items():
        l.__setattr__(k, v) 
    assert l in sale_listings


@pytest.mark.parametrize(
    "listing", [rent_super_feature, rent_premium, rent_normal]
)
def test_rent_results_present(listing, rent_listings):
    l = Listing()
    for k, v in listing.items():
        l.__setattr__(k, v)
    assert l in rent_listings


# Now going to run through attrs, because more descriptive:
@pytest.mark.parametrize(
    "listing", [sale_super_feature, sale_premium, sale_normal, 
                rent_super_feature, rent_premium, rent_normal]
)
@pytest.mark.parametrize(
    "attribute", ["title", "address", "price", "features", "link",
                  "availability", "agent", "agency"]
)
def test_attribute_present(listing, attribute, sale_listings, 
                           rent_listings):
    match = False
    all_listings = sale_listings + rent_listings  # Shouldn't be done EVERY iteration...
    all_attrs = [getattr(l, attribute) for l in all_listings]
    for attr in all_attrs:
        if getattr(listing, attribute) == attr: 
            match = True
    assert match
    
    