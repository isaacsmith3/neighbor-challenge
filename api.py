import fastapi # type: ignore
from algorithm import solve_multi_vehicle_storage, Vehicle, VehicleRequest
import uvicorn # type: ignore
import listings
from typing import List

app = fastapi.FastAPI()

@app.post("/")
def solve_multi_vehicle_storage_api(vehicles: List[VehicleRequest]):

    vehicle_objects = [Vehicle(length=v.length, quantity=v.quantity) for v in vehicles]

    results = solve_multi_vehicle_storage(vehicle_objects, listings.listings)

    result = [
        {
            "location_id": r.location_id,
            "listing_ids": r.listing_ids,
            "total_price_in_cents": r.total_price_in_cents,
        }
        for r in results
    ]

    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
