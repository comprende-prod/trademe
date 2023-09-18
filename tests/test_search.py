import pytest
from trademe.search import search, make_url



# INSTEAD OF A BUNCH OF LIST COMPREHENSIONS AND STUFF, WHY NOT WRITE A THING
# THAT JUST NEEDS ONE LIST COMP. E.G. A FUNC WITH MULTIPLE ASSERTS.







def test_easy():    
    """Typical, "easy" case - Comprende properties for rent."""
    # - Note this is fragile, and will depend on however many properties are
    #   listed at any given time.
    comprende_rent_url = make_url("rent", search_string="Comprende")
    comprende_rent_listings = search(None, [], comprende_rent_url)

    # Check right number of listings
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


def test_more_features():
    """More complicated - Wellington, Te Aro properties for sale, price $200k+, 
    bedrooms 2+, bathrooms 1+.
    
    Good because it tests all kinds of listings (super feature, premium, 
    normal).
    """
    te_aro_url = make_url("sale", "Wellington", "Wellington", "te-aro", 
                          price_min=200000, bedrooms_min=2, bathrooms_min=1)
    te_aro_listings = search(None, [], te_aro_url)

    # Check right number of listings
    assert len(te_aro_listings) == 57

    # Check a handful match:
    # Super feature:
    assert any([l.title.lower() == "This Stylish City Penthouse will be SOLD!"\
               .lower() for l in te_aro_listings])
    assert any([l.price.lower() == "Enquiries over $865,000".lower() \
                for l in te_aro_listings])
    # Premium:
    assert any([l.title.lower() == "IN DEFIANCE OF CONVENTION".lower() \
                for l in te_aro_listings])
    assert any([l.address.lower() == "2B/4 Clyde Quay Wharf, Te Aro, \
                Wellington".lower() for l in te_aro_listings])
    # Normal:



