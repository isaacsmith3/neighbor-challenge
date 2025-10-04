import fastapi
from algorithm import solve_multi_vehicle_storage, Vehicle
import uvicorn
import listings
from typing import List
from pydantic import BaseModel


class VehicleRequest(BaseModel):
    length: int
    quantity: int


app = fastapi.FastAPI()

@app.post("/")
def solve_multi_vehicle_storage_api(vehicles: List[VehicleRequest]):
    # Convert Pydantic models to Vehicle dataclasses
    vehicle_objects = [Vehicle(length=v.length, quantity=v.quantity) for v in vehicles]
    
    # Call the algorithm
    results = solve_multi_vehicle_storage(vehicle_objects, listings.listings)
    
    # Convert results to dictionaries for JSON serialization
    return [{"location_id": r.location_id, "listing_ids": r.listing_ids, "total_price_in_cents": r.total_price_in_cents} for r in results]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)