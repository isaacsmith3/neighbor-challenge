import json
from algorithm import Listing

with open("listings.json", "r") as f:
    listings_data = json.load(f)

listings = [
    Listing(
        id=item["id"],
        location_id=item["location_id"],
        length=item["length"],
        width=item["width"],
        price_in_cents=item["price_in_cents"],
    )
    for item in listings_data
]
