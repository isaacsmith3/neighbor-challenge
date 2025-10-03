from algorithm import Vehicle, Listing, VehicleRequest, solve_multi_vehicle_storage, LocationResult

def test_algorithm_basic():
    listings = [
        Listing(id="1", location_id="1", length=20, width=30, price_in_cents=100),
        Listing(id="2", location_id="2", length=20, width=30, price_in_cents=150),
        Listing(id="3", location_id="3", length=20, width=30, price_in_cents=200),
        Listing(id="4", location_id="1", length=20, width=40, price_in_cents=100),
        Listing(id="5", location_id="2", length=20, width=10, price_in_cents=150),
        Listing(id="6", location_id="3", length=20, width=20, price_in_cents=200),
    ]
    vehicles = [
        Vehicle(length=20, quantity=3),
    ]

    results = [
        LocationResult(location_id="1", listing_ids=["1", "4"], total_price_in_cents=300),
        LocationResult(location_id="2", listing_ids=["2", "5"], total_price_in_cents=350),
        LocationResult(location_id="3", listing_ids=["3", "6"], total_price_in_cents=350),
    ]

    result = solve_multi_vehicle_storage(vehicles, listings)
    assert result == results


if __name__ == "__main__":
    test_algorithm_basic()