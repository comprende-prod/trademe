"""Contains Listing class."""


from dataclasses import dataclass
from bs4 import BeautifulSoup
from . import constants


@dataclass
class Listing:
    """Turns html into listing data.
    
    Provides constructors for different types of listings.
    """
    # In _construct_common_attributes:
    title: str = None
    address: str = "same as title"
    price: str = None
    features: str = None
    link: str = None
    availability: str = "n/a"
    parking: str = "n/a"  
    # ^ Set some to "n/a" so you don't end up with Nones, since others 
    #   are guaranteed to not stay None.

    # Handled individually by constructors:
    agent: str = None
    agency: str = None


    # Class methods, to be used as constructors:
    # (Needed because agent and agency have to be located differently for each
    # listing type).


    @classmethod
    def _construct_common_attributes(cls, listing_soup):
        """Helper for constructors."""
        listing = cls()

        # More complicated attributes: ----------------------------------------

        # As mentioned in constants.py, TradeMe uses the same tag for rent
        # listings' availability AND sales listings' addresses.
        # - If string.lower() has "available" in it, it's a rent listing
        #   and you need to set the `availability` attribute.
        # - Else, it's an address, so set address.
        address_or_availability = listing_soup.find(constants.ADDRESS_TAG).string
        if "available" in address_or_availability.lower():
            listing.availability = address_or_availability
        else:
            listing.address = address_or_availability

        # Parking is also slightly more complicated:
        # - find all relevant list items in listing_soup
        # - check if they have a parking icon
        # - if so, get their span string
        list_items = listing_soup.find_all(
            "li", 
            class_="tm-property-search-card-attribute-icons__metric ng-star-in\
                serted"
        )
        parking_li = None
        for li in list_items:
            # Get icon:
            icon = li.find("tg-icon")
            if icon.get("alt").lower() == "total parking":
                parking_li = li
                break
        if parking_li is not None:
            # Then get span
            span = parking_li.find(
                "span", 
                class_="tm-property-search-card-attribute-icons__metric-value"
            )
            try: 
                listing.parking = span.string
            except AttributeError:  
                # If it somehow has an icon but no number of parking spaces
                pass

        # Less complicated attributes: ---------------------------------------- 
        
        listing.link = cls._get_link(listing_soup)
        listing.title = listing_soup.find(constants.TITLE_TAG).string
        listing.price = listing_soup.find(
            constants.TAG_PRICE, 
            class_=constants.PRICE_CLASS
        ).string
        # Note that `features` picks up virtually everything except parking:
        # e.g. bedrooms, bathrooms, floor area, etc.
        listing.features = listing_soup.find(  
            constants.FEATURES_TAG,
            class_=constants.FEATURES_CLASS
        )[constants.FEATURES_KEY]

        return listing
    

    @classmethod
    def _get_link(cls, listing_tag):
        # Don't worry about it being unsafe, there'll always be an href:
        href = listing_tag.find("a")["href"]  
        if href.startswith("/a/") == False:
            # Then add "/a/":
            href = "/a/" + href
        return constants.TM_BASE_URL + href


    @classmethod
    def from_super_feature(cls, listing_soup):
        """Construct Listing object from super feature listing soup."""
        
        listing = cls._construct_common_attributes(listing_soup)

        # Agent
        # No handling needed:
        listing.agent = listing_soup.find(
            constants.AGENT_SUPER_FEATURE_TAG,
            class_=constants.AGENT_SUPER_FEATURE_CLASS
        ).string

        # Agency
        agency_element = listing_soup.find(
            constants.AGENCY_TAG,
            class_=constants.AGENCY_SUPER_FEATURE_CLASS
        )
        try:
            listing.agency = agency_element["alt"]
        except (KeyError, TypeError):
            # ^ TypeError *sounds* weird, but we include it because you'll get
            #   a TypeError if agency_element is None above.

            # If not thrown error from code above, it's likely a private 
            # listing:
            listing.agency = \
            "Could not find agency. Probably a private listing."

        return listing


    @classmethod
    def from_premium_listing(cls, listing_soup):
        """Construct Listing object from premium listing soup."""

        listing = cls._construct_common_attributes(listing_soup)

        # Agent
        try:
            listing.agent = listing_soup.find(
                constants.AGENT_PREMIUM_TAG,
                class_=constants.AGENT_PREMIUM_CLASS
            ).string
        except AttributeError as e:
            raise e("This is probably a premium listing with a novel layout \
                    for agents. (E.g. maybe it's a private listing).")
        
        # Agency
        try:
            # Agency in normal place:
            listing.agency = listing_soup.find(
                constants.AGENCY_TAG,
                class_=constants.AGENCY_PREMIUM_CLASS
            )["alt"]
        except (KeyError, TypeError):
            # Agency at the top of the listing insteaD:
            listing.agency = listing_soup.find(
                constants.AGENCY_TAG,
                class_=constants.ALT_AGENCY_PREMIUM_CLASS
            )["alt"]
        
        return listing


    @classmethod
    def from_normal_listing(cls, listing_soup):
        """Construct Listing object from normal listing soup."""
        
        listing = cls._construct_common_attributes(listing_soup)

        # Agent
        try:
            listing.agent = listing_soup.find(
                constants.AGENT_NORMAL_TAG
            ).string
        except AttributeError:
            listing.agent = "No agent name provided."

        # Agency
        try:
            # Try getting agency from logos:
            listing.agency = listing_soup.find(
                constants.AGENCY_TAG,
                class_=constants.AGENCY_NORMAL_CLASS
            )["alt"]
        except (KeyError, TypeError): 
            listing.agency = listing_soup.find(
                constants.ALT_AGENCY_NORMAL_TAG,
                class_=constants.ALT_AGENCY_NORMAL_CLASS
            ).string

        return listing

