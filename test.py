from algorithm import (
    Vehicle,
    Listing,
    solve_multi_vehicle_storage,
    LocationResult,
)


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
        LocationResult(location_id="1", listing_ids=["1"], total_price_in_cents=100),
        LocationResult(location_id="2", listing_ids=["2"], total_price_in_cents=150),
        LocationResult(location_id="3", listing_ids=["3"], total_price_in_cents=200),
    ]

    result = solve_multi_vehicle_storage(vehicles, listings)
    assert result == results


def test_algorithm_multiple_listings_needed():
    """Test case where multiple listings are needed at the same location"""
    listings = [
        Listing(
            id="1", location_id="1", length=20, width=20, price_in_cents=100
        ),  # 400 sq ft
        Listing(
            id="2", location_id="1", length=20, width=20, price_in_cents=120
        ),  # 400 sq ft
        Listing(
            id="3", location_id="1", length=20, width=30, price_in_cents=150
        ),  # 600 sq ft
    ]
    vehicles = [
        Vehicle(length=20, quantity=2) # Need 2 * 20*10 = 400 sq ft
    ]

    results = solve_multi_vehicle_storage(vehicles, listings)
    assert len(results) == 1
    assert results[0].location_id == "1"
    assert results[0].listing_ids == ["1"]
    assert results[0].total_price_in_cents == 100


def test_algorithm_no_solution():
    """Test case where no solution exists"""
    listings = [
        Listing(
            id="1", location_id="1", length=10, width=10, price_in_cents=100
        ),
    ]
    vehicles = [
        Vehicle(length=20, quantity=1)
    ]

    results = solve_multi_vehicle_storage(vehicles, listings)
    assert len(results) == 0


if __name__ == "__main__":
    test_algorithm_basic()
    test_algorithm_multiple_listings_needed()
    test_algorithm_no_solution()
    print("All tests passed!")
