import pytest
from ..trademe.search import make_url


@pytest.mark.parametrize(
        "sale_or_rent, region, district, suburb",
        [
            ("rente", "", "", ""),
            ("ssssssale", "", "", ""),
            ("", "Wellington", "", "Seatoun"),
            ("", "", "Wellington", "Seatoun"),
            ("", "", "Wellington", ""),
            ("", "", "", "Seatoun")
        ]
)
def test_raises(sale_or_rent, region, district, suburb):
    with pytest.raises(ValueError):
        make_url(sale_or_rent=sale_or_rent, region=region, district=district, 
                 suburb=suburb)


# This is probably unnecessary, but hey it's rigorous:


@pytest.mark.parametrize(
        "expected_output, sale_or_rent, region, district, suburb, kwargs",
        [
            (
                "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/aro-valley/search?",
                "rent",
                "Wellington",
                "Wellington", 
                "aro-valley",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/search?",
                "sale",
                "Wellington",
                "Wellington",
                "aro-valley",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/aro-valley/search?price_min=100000&bedrooms_min=1",
                "sale",
                "Wellington",
                "Wellington",
                "aro-valley",
                {"price_min": 100_000, "bedrooms_min": 1}
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?",
                "rent",
                "Wellington",
                "Wellington",
                "",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/sale/wellington/wellington/search?",
                "sale",
                "Wellington",
                "Wellington",
                "",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/rent/wellington/wellington/search?property_type=townhouse&pets_ok=true",
                "rent",
                "Wellington",
                "Wellington",
                "",
                {"property_type": "townhouse", "pets_ok": "true"}
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/rent/wellington/search?",
                "rent",
                "wellington",
                "",
                "",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/sale/wellington/search?",
                "sale",
                "wellington",
                "",
                "",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/rent/wellington/search?open_homes=true&price_max=650000",
                "rent",
                "wellington",
                "",
                "",
                {"open_homes": "true", "price_max": 650000}
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/rent/search?",
                "rent",
                "",
                "",
                "",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/sale/search?",
                "sale",
                "",
                "",
                "",
                dict()
            ),
            (
                "https://www.trademe.co.nz/a/property/residential/rent/search?property_type=apartment&price_max=700",
                "rent",
                "",
                "",
                "",
                {"property_type": "apartment", "price_max": 700}
            ),
        ]
)
def test_output(expected_output, sale_or_rent, region, district, suburb, 
                kwargs):
    assert make_url(sale_or_rent=sale_or_rent, region=region, district=district, suburb=suburb, **kwargs).lower() == expected_output

