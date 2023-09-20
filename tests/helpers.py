from trademe.listing import Listing


def listing_match(listing: Listing, **kwargs):
    matches = True
    for k, v in kwargs.items():
        if listing.get(k) != v:  # Can do this becaues all attrs are str
            matches = False
            break
    return matches

