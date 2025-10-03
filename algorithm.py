"""
Multi-Vehicle Storage Algorithm

This module implements the core algorithm for finding the cheapest combination
of storage listings that can accommodate multiple vehicles at each location.
"""

from typing import List, Dict, Tuple, Set
import json
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
