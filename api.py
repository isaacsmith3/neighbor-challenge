import fastapi  # type: ignore
from algorithm import solve_multi_vehicle_storage, Vehicle
import uvicorn  # type: ignore
import listings
from typing import List
from pydantic import BaseModel
import os


class VehicleRequest(BaseModel):
    length: int
    quantity: int


app = fastapi.FastAPI()


@app.post("/")
def solve_multi_vehicle_storage_api(vehicles: List[VehicleRequest]):

    vehicle_objects = [Vehicle(length=v.length, quantity=v.quantity) for v in vehicles] # Convert Pydantic models to Vehicle dataclasses


    results = solve_multi_vehicle_storage(vehicle_objects, listings.listings)

    return [
        {
            "location_id": r.location_id,
            "listing_ids": r.listing_ids,
            "total_price_in_cents": r.total_price_in_cents,
        }
        for r in results
    ]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
