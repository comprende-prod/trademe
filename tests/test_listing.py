"""Test Listing constructors."""


from functools import lru_cache
from pathlib import Path
import pytest
from bs4 import BeautifulSoup
from ..trademe.listing import Listing


# Setup
# - Set up path:
html = Path("tests/html")

def test_html_exists():
    assert html.exists()

# - Features of each listing
rent_super_feature = {
    "title": "Balclutha",
    "address": None,
    "price": "$550 per week",
    "features": "3 bedrooms. 1 bathrooms.",
    "link": "https://www.trademe.co.nz/a/property/residential/rent/otago/clutha/balclutha/listing/4324246903?rsqid=054787bff49041ccbdc3d554927f200b-002",
    "availability": "Available: Fri, 20 Oct",
    "agent": " Marietta ",
    "agency": None
}

rent_premium = {
    "title": "118a Anderson Road, Wanaka, Wanaka",
    "address": None,
    "price": "$400 per week",
    "features": "1 bedrooms. 1 bathrooms.",
    "link": "https://www.trademe.co.nz/a/property/residential/rent/otago/wanaka/wanaka/listing/4332904134?rsqid=054787bff49041ccbdc3d554927f200b-002",
    "availability": "Available: Tue, 10 Oct",
    "agent": " Liane Wiesner ",
    "agency": "Bayleys Property Management Wanaka"
}

rent_normal = {
    "title": "4 Bay Road, Palm Beach, Waiheke Island",
    "address": None,
    "price": "$775 per week",
    "features": "1 bedrooms. 1 bathrooms.",
    "link": "https://www.trademe.co.nz/a/property/residential/rent/auckland/waiheke-island/palm-beach/listing/4117008125?rsqid=834adc0142844278ab2085091e927932-003",
    "availability": "Available: Now",
    "agent": None,
    "agency": " Private listing "
}

sale_super_feature = {
    "title": "Newtown Gem - Location and Opportunity",
    "address": "Newtown, Wellington",
    "price": "Deadline sale",
    "features": "3 bedrooms. 1 bathrooms. floor area 90 meters square. land area 220 meters square.",
    "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/newtown/listing/4324065029?rsqid=62da1f27acd74ef6a40e4504583964a6-001",
    "availability": None,
    "agent": " Michael Hinds ",
    "agency": "Just Paterson Real Estate Ltd MREINZ, (Licensed: REAA 2008)"
}

sale_premium = {
    "title": "MODERN, STYLISH AND SUNNY IN NEWTOWN",
    "address": "8/239 Adelaide Road, Newtown, Wellington",
    "price": "Deadline sale",
    "features": "2 bedrooms. 1 bathrooms. floor area 84 meters square.",
    "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/newtown/listing/4331757012?rsqid=a3270af5645a45b8a71a7d1743a5c4c1-001",
    "availability": None,
    "agent": " Chris Day & Rachel Aislabie ",
    "agency": "Lowe & Co"
}

sale_normal = {
    "title": "Masina – Dual Key",
    "address": "211/80 Riddiford Street, Newtown, Wellington",
    "price": "$860,000",
    "features": "2 bedrooms. 2 bathrooms. floor area 77 meters square.",
    "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/newtown/listing/3888296961?rsqid=a3270af5645a45b8a71a7d1743a5c4c1-001",
    "availability": None,
    "agent": " Paul Charlett",
    "agency": "One Agency (Innov8 Ltd), (Licensed: REAA 2008)"
}


# Tests:


@pytest.mark.parametrize(
    "html_path, listing_attrs", 
    [
        ("rent_super_feature.html", rent_super_feature),
        ("rent_premium.html", rent_premium),
        ("rent_normal.html", rent_normal),
        ("sale_super_feature.html", sale_super_feature),
        ("sale_premium.html", sale_premium),
        ("sale_normal.html", sale_normal)
    ]
)
class TestConstructors:


    @classmethod
    @lru_cache
    def make_listing(self, html_path) -> Listing:
        path = html / html_path
        with open(path, "r") as f:
            soup = BeautifulSoup(f.read(), features="html.parser")
        if "super" in html_path:
            listing = Listing.from_super_feature(soup)
        elif "premium" in html_path:
            listing = Listing.from_premium_listing(soup)
        else: 
            listing = Listing.from_normal_listing(soup)
        return listing


    # In a hurry, can't make this prettier:


    def test_title(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert listing.title == listing_attrs["title"]


    def test_address(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert listing.address == listing_attrs["address"]

    
    def test_price(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert listing.price == listing_attrs["price"]


    def test_features(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert listing.features == listing_attrs["features"]


    def test_link(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert listing.link == listing_attrs["link"]


    def test_availability(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert str(listing.availability).strip() == str(listing_attrs["availability"]).strip()


    def test_agent(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert str(listing.agent).strip() == str(listing_attrs["agent"]).strip()


    def test_agency(self, html_path, listing_attrs):
        listing = TestConstructors.make_listing(html_path)
        assert str(listing.agency).strip() == str(listing_attrs["agency"]).strip()

