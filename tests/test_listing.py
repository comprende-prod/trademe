"""Test Listing constructors."""


from pathlib import Path
import pytest
from bs4 import BeautifulSoup
from ..trademe.listing import Listing
from .helpers import listing_match


# Setup
# - Set up path:
html = Path("html")

# - Features of each listing
rent_super_feature = {
    "title": "Balclutha",
    "address": None,
    "price": "$550 per week",
    "features": "3 bedrooms. 1 bathrooms.",
    "link": "https://www.trademe.co.nz/a/property/residential/rent/otago/clutha/balclutha/listing/4324246903?rsqid=054787bff49041ccbdc3d554927f200b-002",
    "availability": "Available: Fri, 20 Oct",
    "agent": " Marietta ",
    "agency": "Could not find agency. Probably a private listing."
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
    "agent": "No agent name provided.",
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
    "link": "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/newtown/listing/4331757012?rsqid=62da1f27acd74ef6a40e4504583964a6-001",
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


def test_rsf():
    path = html / "rent_super_feature.html"
    with open(path, "r") as f:
        soup = BeautifulSoup(f.read())
    # Construct Listing from soup, check vs features
    listing = Listing.from_super_feature(soup)
    assert listing_match(listing, **rent_super_feature)

def test_rp():
    path = html / "rent_premium.html"
    with open(path, "r") as f:
        soup = BeautifulSoup(f.read())
    listing = Listing.from_premium_listing(soup)
    assert listing_match(listing, **rent_premium)

def test_rn():
    path = html / "rent_normal.html"
    with open(path, "r") as f:
        soup = BeautifulSoup(f.read())
    listing = Listing.from_normal_listing(soup)
    assert listing_match(listing, **rent_normal)

def test_ssf():
    path = html / "sale_super_feature.html"
    with open(path, "r") as f:
        soup = BeautifulSoup(f.read())
    listing = Listing.from_super_feature(soup)
    assert listing_match(listing, **sale_super_feature)

def test_sp():
    path = html / "sale_premium.html"
    with open(path, "r") as f:
        soup = BeautifulSoup(f.read())
    listing = Listing.from_premium_listing(soup)
    assert listing_match(listing, **sale_premium)

def test_sn():
    path = html / "sale_normal.html"
    with open(path, "r") as f:
        soup = BeautifulSoup(f.read())
    listing = Listing.from_normal_listing(soup)
    assert listing_match(listing, **sale_normal)

