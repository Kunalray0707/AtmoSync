"""
AtmoSync Enterprise IoT Sensor Simulator Engine
Simulates container-level reefer micro-climate telemetry, thermal kinetics, route progress, and market pricing dynamics.
"""

import math
import random
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Generator

from simulator.config import COMMODITIES, ROUTES


class ContainerSimulator:
    """Simulates an individual cold-chain reefer container carrying perishables."""
    
    def __init__(self, container_id: str, shipment_id: str, route_info: Dict[str, Any], commodity_name: str):
        self.container_id = container_id
        self.shipment_id = shipment_id
        self.route = route_info
        self.commodity = commodity_name
        self.commodity_profile = COMMODITIES[commodity_name]
        
        # Route progress tracking
        self.progress_pct = random.uniform(0.05, 0.85)  # Current route progression (0.0 to 1.0)
        self.start_lat, self.start_lon = self.route["start_coords"]
        self.end_lat, self.end_lon = self.route["end_coords"]
        self.total_distance = self.route["distance_km"]
        
        # Thermal & micro-climate states
        self.target_temp = self.commodity_profile["optimum_temp"]
        self.current_temp = self.target_temp + random.uniform(-0.5, 0.5)
        self.target_humidity = self.commodity_profile["optimum_humidity"]
        self.current_humidity = self.target_humidity + random.uniform(-2.0, 2.0)
        
        # Operational states
        self.door_open = False
        self.door_open_timer = 0
        self.battery_level = random.uniform(75.0, 100.0)
        self.compressor_fault = False
        self.sensor_health = "HEALTHY"
        
        # Base spot prices
        self.base_market_price = self.commodity_profile["base_price_per_kg"]
        self.current_market_price = self.base_market_price * random.uniform(0.95, 1.15)
        
        # Speed (km/h) - Cargo ship or reefer truck
        self.avg_speed = 35.0 if "Port" in self.route["origin"] else 85.0

    def step(self) -> Dict[str, Any]:
        """Advance container state by 1 simulation step (e.g. 1-10 seconds) and generate telemetry."""
        now = datetime.now(timezone.utc)
        
        # 1. Update route progress
        distance_covered = (self.avg_speed / 3600.0) * 10  # simulated distance delta
        self.progress_pct += (distance_covered / self.total_distance)
        if self.progress_pct >= 1.0:
            self.progress_pct = 0.05  # Loop shipment reset
            
        remaining_distance = round(self.total_distance * (1.0 - self.progress_pct), 2)
        
        # Interpolate GPS coordinates
        cur_lat = round(self.start_lat + (self.end_lat - self.start_lat) * self.progress_pct + random.uniform(-0.002, 0.002), 6)
        cur_lon = round(self.start_lon + (self.end_lon - self.start_lon) * self.progress_pct + random.uniform(-0.002, 0.002), 6)
        
        # ETA calculation
        remaining_hours = remaining_distance / max(self.avg_speed, 10.0)
        eta_timestamp = (now + timedelta(hours=remaining_hours)).isoformat()
        
        # 2. Simulate thermal micro-climate physics
        # Random fault injections (1% chance of door open, 0.5% compressor malfunction)
        if not self.door_open and random.random() < 0.015:
            self.door_open = True
            self.door_open_timer = random.randint(3, 8)
            
        if self.door_open:
            self.door_open_timer -= 1
            self.current_temp += random.uniform(0.4, 0.9)  # Inrush of ambient heat
            self.current_humidity += random.uniform(-1.5, 1.5)
            if self.door_open_timer <= 0:
                self.door_open = False
                
        if not self.compressor_fault and random.random() < 0.005:
            self.compressor_fault = True
            self.sensor_health = "DEGRADED"
            
        if self.compressor_fault:
            self.current_temp += random.uniform(0.1, 0.3)  # Gradual heat leak
            if random.random() < 0.05:  # Auto-recovery after some time
                self.compressor_fault = False
                self.sensor_health = "HEALTHY"
        else:
            # Normal compressor oscillation around target
            diff = self.target_temp - self.current_temp
            self.current_temp += diff * 0.15 + random.uniform(-0.08, 0.08)
            
        # Humidity fluctuations
        h_diff = self.target_humidity - self.current_humidity
        self.current_humidity += h_diff * 0.1 + random.uniform(-0.3, 0.3)
        self.current_humidity = max(50.0, min(99.9, self.current_humidity))
        
        # 3. Battery drain & CO2 emissions
        self.battery_level = round(max(5.0, self.battery_level - 0.002), 2)
        ambient_temp = round(22.0 + 8.0 * math.sin(self.progress_pct * math.pi * 4) + random.uniform(-2, 2), 1)
        co2_rate = round(12.5 + (self.current_temp - self.target_temp) * 1.5 + (self.avg_speed * 0.15), 2)
        fuel_rate = round(28.0 + random.uniform(-1.5, 1.5), 1)
        
        # Ambient weather condition
        weather_states = ["Clear", "Partly Cloudy", "Rain", "High Temperature Wave", "Storm"]
        weather_cond = random.choice(weather_states) if random.random() < 0.05 else "Clear"
        
        # Spot Market price dynamic movement
        price_drift = random.uniform(-0.02, 0.03)
        self.current_market_price = round(max(0.5, self.current_market_price + price_drift), 2)
        
        # Construct telemetry event
        telemetry = {
            "timestamp": now.isoformat(),
            "container_id": self.container_id,
            "shipment_id": self.shipment_id,
            "latitude": cur_lat,
            "longitude": cur_lon,
            "commodity": self.commodity,
            "temperature": round(self.current_temp, 2),
            "humidity": round(self.current_humidity, 2),
            "door_open": self.door_open,
            "battery": self.battery_level,
            "gps_speed": round(self.avg_speed + random.uniform(-2, 2), 1),
            "ambient_temperature": ambient_temp,
            "ambient_humidity": round(max(40.0, min(95.0, self.current_humidity + random.uniform(-10, 10))), 1),
            "weather_condition": weather_cond,
            "market_price": self.current_market_price,
            "destination": self.route["destination"],
            "origin": self.route["origin"],
            "remaining_distance_km": remaining_distance,
            "estimated_arrival": eta_timestamp,
            "fuel_consumption_l_per_100km": fuel_rate,
            "co2_emission_kg_hr": co2_rate,
            "sensor_health": self.sensor_health,
            "alternative_destinations": self.route["alternative_ports"]
        }
        return telemetry


class IoTTelemetryFleet:
    """Manages a fleet of simulated IoT reefer containers."""
    
    def __init__(self, fleet_size: int = 20):
        self.containers: List[ContainerSimulator] = []
        commodity_keys = list(COMMODITIES.keys())
        
        for i in range(1, fleet_size + 1):
            container_id = f"CONT-{1000 + i}"
            route = ROUTES[i % len(ROUTES)]
            shipment_id = f"{route['shipment_prefix']}-{200 + i}"
            commodity = commodity_keys[i % len(commodity_keys)]
            
            self.containers.append(
                ContainerSimulator(container_id, shipment_id, route, commodity)
            )
            
    def generate_fleet_snapshot(self) -> List[Dict[str, Any]]:
        """Return single frame of telemetry events across all containers."""
        return [container.step() for container in self.containers]

    def stream_telemetry(self, interval: float = 1.0) -> Generator[Dict[str, Any], None, None]:
        """Continuous generator yielding individual container telemetry events."""
        while True:
            for container in self.containers:
                yield container.step()
            time.sleep(interval)


class IoTSimulator(IoTTelemetryFleet):
    """Backward-compatible alias used by the legacy FastAPI application."""

    def __init__(self, num_containers: int = 20):
        super().__init__(fleet_size=num_containers)


# Standalone runner for testing simulator
if __name__ == "__main__":
    fleet = IoTTelemetryFleet(fleet_size=5)
    snapshot = fleet.generate_fleet_snapshot()
    print(f"Generated telemetry snapshot for {len(snapshot)} containers:")
    print(snapshot[0])
