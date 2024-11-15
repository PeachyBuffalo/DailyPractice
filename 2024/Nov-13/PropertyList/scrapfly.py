import httpx

response = httpx.get("some realtor.com url")
# in ScrapFly SDK becomes
from scrapfly import ScrapflyClient, ScrapeConfig
client = ScrapflyClient("YOUR SCRAPFLY KEY")
result = client.scrape(ScrapeConfig(
    "some Realtor.ocm url",
    # we can select specific proxy country
    country="US",
    # and enable anti scraping protection bypass:
    asp=True
))