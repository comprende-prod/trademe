"""Stores project-level constants."""


# Listings:
SUPER_FEATURE_TAG = "tm-property-super-feature-card"
PREMIUM_TAG = "tm-property-premium-listing-card"
NORMAL_TAG = "tm-property-search-card"

LISTING_TAGS = [SUPER_FEATURE_TAG, PREMIUM_TAG, NORMAL_TAG]

# Listing attributes:

# Common attrbute identifiers:
# - Title
TITLE_TAG = "tm-property-search-card-listing-title"
# - Address
ADDRESS_TAG = "tm-property-search-card-address-subtitle"
# - Price
TAG_PRICE = "div"
PRICE_CLASS = "tm-property-search-card-price-attribute__price"
# - Features
FEATURES_TAG = "ul"
FEATURES_CLASS  = "tm-property-search-card-attribute-icons__features"
FEATURES_KEY = "aria-label"

# Identifiers that differ between listing types:

# - Agent
# --- Super feature:
AGENT_SUPER_FEATURE_TAG = "tg-media-block-content"
AGENT_SUPER_FEATURE_CLASS = "tm-property-super-feature-card__agent-detail--simple o-media-block__content"
# --- Premium listing:
AGENT_PREMIUM_TAG = "div"
AGENT_PREMIUM_CLASS = "tm-property-premium-listing-card__agents-name"
# --- Normal listing:
AGENT_NORMAL_TAG = "tm-property-search-card-agents-name"

# - Agency
# - Common agency tag:
AGENCY_TAG = "img"
# --- Super feature:
AGENCY_SUPER_FEATURE_CLASS = "tm-property-super-feature-card__agent-detail--simple o-media-block__content"
# --- Premium listing:
AGENCY_PREMIUM_CLASS = "tm-property-premium-listing-card__agency-logo ng-star-inserted"
ALT_AGENCY_PREMIUM_CLASS = "tm-property-premium-listing-card__top-agency-logo ng-star-inserted"
# --- Normal listing:
AGENCY_NORMAL_CLASS = "tm-property-search-card__agency-logo ng-star-inserted"
ALT_AGENCY_NORMAL_TAG = "div"
ALT_AGENCY_NORMAL_CLASS = "tm-property-search-card__agency-text ng-star-inserted"

