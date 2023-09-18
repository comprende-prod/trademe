import pytest
from trademe.search import search, make_url


def test_easy():    
    # Typical, "easy" case - Comprende properties for rent
    # - Note this is fragile, and will depend on however many properties are
    #   listed at any given time.
    comprende_rent_url = make_url("rent", search_string="Comprende")
    comprende_rent_listings = search(None, [], comprende_rent_url)

    # Check right number
    assert len(comprende_rent_listings) == 22

    # Check a handful match:
    # - Check it has the first listing that comes up:
    assert any([l.title.lower() == \
                "12D/126 The Terrace, Wellington Central, Wellington".lower() \
                for l in comprende_rent_listings])
    assert any([l.price.lower() == "$490 per week".lower() \
                for l in comprende_rent_listings])
    # - Check the last listing:
    assert any([l.title.lower() == "808/74 Taranaki Street, \
                Wellington Central, Wellington".lower() \
                for l in comprende_rent_listings])
    assert any([l.price.lower() == "$730 per week".lower() for l in \
                comprende_rent_listings])

    # Check all agency attrs are Comprende:
    assert all(l.agency.lower() == "comprende ltd" for l in \
               comprende_rent_listings)


def test_



