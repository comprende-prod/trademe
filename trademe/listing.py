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

    # Handled individually by constructors:
    agent: str = None
    agency: str = None


    # Class methods, to be used as constructors:
    # (Needed because agent and agency have to be located differently for each
    # listing type).


    @classmethod
    def _construct_common_attributes(listing_soup: BeautifulSoup):
        """Helper for constructors."""
        listing = Listing()

        listing.title = listing_soup.find(constants.TITLE_TAG).string
        listing.address = listing_soup.find(constants.ADDRESS_TAG).string
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
    def from_super_feature(listing_soup: BeautifulSoup):
        """Construct Listing object from super feature listing soup."""
        
        listing = Listing._construct_common_attributes(listing_soup)

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
        except KeyError:
            # If not thrown error from code above, it's likely a private 
            # listing:
            listing.agency = \
            "Could not find agency. Probably a private listing."

        return listing


    @classmethod
    def from_premium_listing(listing_soup: BeautifulSoup):
        """Construct Listing object from premium listing soup."""

        listing = Listing._construct_common_attributes(listing_soup)

        # Agent
        try:
            listing.agent = listing.agent = listing_soup.find(
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
        except KeyError:
            # Agency at the top of the listing insteaD:
            listing.agency = listing_soup.find(
                constants.AGENCY_TAG,
                class_=constants.ALT_AGENCY_PREMIUM_CLASS
            )["alt"]
        
        return listing


    @classmethod
    def from_normal_listing(listing_soup: BeautifulSoup):
        """Construct Listing object from normal listing soup."""
        
        listing = Listing._construct_common_attributes(listing_soup)

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
        except KeyError:
            listing.agency = listing_soup.find(
                constants.ALT_AGENCY_NORMAL_TAG,
                class_=constants.ALT_AGENCY_NORMAL_CLASS
            ).string

        return listing

