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
    address: str = None
    price: str = None
    features: str = None
    availability: str = "n/a"

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

        listing.title = listing_soup.find(constants.TITLE_TAG).string

        # As mentioned in constants.py, TradeMe uses the same tag for rent
        # listings' availability AND sales listings' addresses.
        # - If string.lower() has "available" in it, it's a rent listing
        #   and you need to set the `availability` attribute.
        # - Else, it's an address, so set address.
        address_or_availability = listing.find(constants.ADDRESS_TAG).string
        if "available" in address_or_availability.lower():
            listing.availability = address_or_availability
        else:
            listing.address = address_or_availability

        # Other attributes:
        listing.price = listing_soup.find(
            constants.TAG_PRICE, 
            class_=constants.PRICE_CLASS
        ).string
        listing.features = listing_soup.find(
            constants.FEATURES_TAG,
            class_=constants.FEATURES_CLASS
        )[constants.FEATURES_KEY]

        return listing


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

