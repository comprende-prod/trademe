

def listing_match(listing, **kwargs):
    matches = True
    for k, v in kwargs.items():
        if getattr(listing, k) != v:
            matches = False
            break
    return matches

