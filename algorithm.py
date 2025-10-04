"""
Multi-Vehicle Storage Algorithm

Notes:
- First fit decreasing won't work for this problem because we need to find the cheapest combination of listings per location.
- We can use a dynamic programming approach to find the cheapest combination of listings per location.

My outlined steps are as follows:
1. Parse input
2. Group listings by location
3. For each location, use a greedy approach to find the cheapest combination of listings
4. Return the results

"""

from typing import List, Dict, Tuple
from dataclasses import dataclass

VEHICLE_WIDTH = 10


@dataclass
class Listing:
    id: str
    location_id: str
    length: int
    width: int
    price_in_cents: int


@dataclass
class Vehicle:
    length: int
    quantity: int
    width: int = VEHICLE_WIDTH


@dataclass
class VehicleRequest:
    vehicles: List[Vehicle]


@dataclass
class LocationResult:
    location_id: str
    listing_ids: List[str]
    total_price_in_cents: int


def group_listings_by_location(listings: List[Listing]) -> Dict[str, List[Listing]]:
    listings_by_location: dict[str, List[Listing]] = {}

    for listing in listings:
        if listing.location_id not in listings_by_location:
            listings_by_location[listing.location_id] = []
        listings_by_location[listing.location_id].append(listing)

    return listings_by_location


def sort_by_price(listings: List[Listing]) -> List[Listing]:
    return sorted(listings, key=lambda x: x.price_in_cents)


def solve_multi_vehicle_storage(
    vehicles: List[Vehicle], listings: List[Listing]
) -> List[LocationResult]:
    listings_by_location = group_listings_by_location(listings)
    results = []

    for location_id, location_listings in listings_by_location.items():
        price, listing_ids = greedy_solve_location(vehicles, location_listings)

        # Only include the locations that fit. Catching the failed attempt for a solution.
        if price > 0 and listing_ids:
            results.append(
                LocationResult(
                    location_id=location_id,
                    listing_ids=listing_ids,
                    total_price_in_cents=price,
                )
            )

    results.sort(key=lambda x: x.total_price_in_cents)
    return results


def greedy_solve_location(
    vehicles: List[Vehicle], listings: List[Listing]
) -> Tuple[int, List[str]]:
    """
    Find the cheapest combination of listings that can store all vehicles.
    Uses a greedy approach: sort listings by total price, then select cheapest ones that provide enough area.
    """
    if not vehicles or not listings:
        return 0, []

    # Calculate total area needed for all vehicles
    total_area_needed = sum(
        vehicle.length * vehicle.width * vehicle.quantity for vehicle in vehicles
    )

    # Sort listings by total price (cheapest first)
    sorted_listings = sorted(listings, key=lambda x: x.price_in_cents)

    selected_listings = []
    total_area_covered = 0


    total_cost = 0
    for listing in sorted_listings:
        if total_area_covered >= total_area_needed:
            break

        selected_listings.append(listing)
        total_area_covered += listing.length * listing.width
        total_cost += listing.price_in_cents

    # Check if they actually fit all vehicles
    if total_area_covered < total_area_needed:
        return 0, []  # Failed attempt for a solution. Will be caught by the caller.

    return total_cost, [listing.id for listing in selected_listings]
