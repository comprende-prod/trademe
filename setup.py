import setuptools


setuptools.setup(
    name="trademe",
    version="0.1.0",
    author="Ethan Beri",
    author_email="ethandberi01@gmail.com",
    description="Scrapes TradeMe residential properties.",
    url="https://github.com/comprende-prod/trademe",
    license="GNU GPLv3",
    packages=["trademe"],
    install_requires=["selenium", "bs4", "urllib3", "dataclasses"]
)

