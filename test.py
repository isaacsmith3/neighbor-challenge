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
    vehicles = [Vehicle(length=20, quantity=2)]  # Need 2 * 20*10 = 400 sq ft

    results = solve_multi_vehicle_storage(vehicles, listings)
    assert len(results) == 1
    assert results[0].location_id == "1"
    assert results[0].listing_ids == ["1"]
    assert results[0].total_price_in_cents == 100


def test_algorithm_no_solution():
    """Test case where no solution exists"""
    listings = [
        Listing(id="1", location_id="1", length=10, width=10, price_in_cents=100),
    ]
    vehicles = [Vehicle(length=20, quantity=1)]

    results = solve_multi_vehicle_storage(vehicles, listings)
    assert len(results) == 0


def test_multiple_vehicle_types():
    """Test case with multiple vehicle types (from README example)"""
    vehicles = [
        Vehicle(length=10, quantity=1),  # 10x10 = 100 sq ft
        Vehicle(length=20, quantity=2),  # 20x10 = 200 sq ft each = 400 sq ft total
        Vehicle(length=25, quantity=1),  # 25x10 = 250 sq ft
    ]
    # Total needed: 100 + 400 + 250 = 750 sq ft

    listings = [
        Listing(
            id="1", location_id="loc1", length=20, width=40, price_in_cents=100
        ),  # 800 sq ft
        Listing(
            id="2", location_id="loc1", length=20, width=20, price_in_cents=80
        ),  # 400 sq ft
        Listing(
            id="3", location_id="loc2", length=30, width=30, price_in_cents=150
        ),  # 900 sq ft
    ]

    results = solve_multi_vehicle_storage(vehicles, listings)

    # Should find 2 locations
    assert len(results) == 2

    # Should be sorted by price (cheapest first)
    assert results[0].total_price_in_cents <= results[1].total_price_in_cents

    # Check that all locations can actually fit the vehicles
    for result in results:
        assert len(result.listing_ids) > 0
        assert result.total_price_in_cents > 0


def test_multiple_listings_optimization():
    """Test case where using multiple smaller listings is cheaper than one large listing"""
    vehicles = [Vehicle(length=20, quantity=5)]  # Need 5 * 20*10 = 1000 sq ft

    listings = [
        Listing(
            id="a", location_id="loc1", length=20, width=30, price_in_cents=100
        ),  # 600 sq ft
        Listing(
            id="b", location_id="loc1", length=20, width=20, price_in_cents=80
        ),  # 400 sq ft
        Listing(
            id="c", location_id="loc1", length=20, width=50, price_in_cents=200
        ),  # 1000 sq ft
    ]

    results = solve_multi_vehicle_storage(vehicles, listings)

    # Should find 1 location
    assert len(results) == 1

    result = results[0]
    assert result.location_id == "loc1"

    # Should use the cheaper combination (listings a+b = $1.80) instead of listing c ($2.00)
    assert result.total_price_in_cents == 180  # 100 + 80
    assert set(result.listing_ids) == {"a", "b"}


def test_exact_fit():
    """Test case where area needed exactly matches area available"""
    vehicles = [Vehicle(length=20, quantity=2)]  # Need 2 * 20*10 = 400 sq ft

    listings = [
        Listing(
            id="exact", location_id="loc1", length=20, width=20, price_in_cents=100
        ),  # Exactly 400 sq ft
        Listing(
            id="oversized", location_id="loc2", length=30, width=20, price_in_cents=150
        ),  # 600 sq ft
    ]

    results = solve_multi_vehicle_storage(vehicles, listings)

    # Should find 2 locations
    assert len(results) == 2

    # Should be sorted by price (exact fit should be cheaper)
    assert results[0].total_price_in_cents == 100
    assert results[0].listing_ids == ["exact"]
    assert results[1].total_price_in_cents == 150
    assert results[1].listing_ids == ["oversized"]


def test_price_sorting():
    """Test case to verify results are sorted by price ascending"""
    vehicles = [Vehicle(length=10, quantity=1)]  # Need 100 sq ft

    listings = [
        Listing(
            id="expensive", location_id="loc1", length=20, width=20, price_in_cents=200
        ),  # 400 sq ft
        Listing(
            id="cheap", location_id="loc2", length=20, width=20, price_in_cents=100
        ),  # 400 sq ft
        Listing(
            id="medium", location_id="loc3", length=20, width=20, price_in_cents=150
        ),  # 400 sq ft
    ]

    results = solve_multi_vehicle_storage(vehicles, listings)

    # Should find 3 locations
    assert len(results) == 3

    # Should be sorted by price ascending
    assert results[0].total_price_in_cents == 100
    assert results[1].total_price_in_cents == 150
    assert results[2].total_price_in_cents == 200


def test_no_solution_comprehensive():
    """Test case where no listings can fit the vehicles"""
    vehicles = [Vehicle(length=50, quantity=1)]  # Need 50*10 = 500 sq ft

    listings = [
        Listing(
            id="too_small1", location_id="loc1", length=20, width=20, price_in_cents=100
        ),  # 400 sq ft
        Listing(
            id="too_small2", location_id="loc2", length=30, width=15, price_in_cents=120
        ),  # 450 sq ft
    ]

    results = solve_multi_vehicle_storage(vehicles, listings)

    # Should find no solutions
    assert len(results) == 0


if __name__ == "__main__":
    test_algorithm_basic()
    test_algorithm_multiple_listings_needed()
    test_algorithm_no_solution()
    test_multiple_vehicle_types()
    test_multiple_listings_optimization()
    test_exact_fit()
    test_price_sorting()
    test_no_solution_comprehensive()
    print("All tests passed!")
