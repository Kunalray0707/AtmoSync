"""
AtmoSync Simulator Configuration
Defines commodity sensitivity profiles, shipping routes, port locations, and simulation physics parameters.
"""

# Commodity baseline thermal profiles and shelf-life parameters
COMMODITIES = {
    "Avocados": {
        "optimum_temp": 5.0,  # Celsius
        "max_temp": 12.0,
        "min_temp": 3.0,
        "optimum_humidity": 85.0,  # %
        "base_shelf_life_days": 21,
        "activation_energy": 55.0,  # kJ/mol (Arrhenius decay constant)
        "base_price_per_kg": 3.40,
        "spoilage_threshold_days": 4
    },
    "Strawberries": {
        "optimum_temp": 1.0,
        "max_temp": 4.0,
        "min_temp": 0.0,
        "optimum_humidity": 92.0,
        "base_shelf_life_days": 7,
        "activation_energy": 70.0,
        "base_price_per_kg": 5.80,
        "spoilage_threshold_days": 1.5
    },
    "Bananas": {
        "optimum_temp": 13.5,
        "max_temp": 15.0,
        "min_temp": 12.5,
        "optimum_humidity": 90.0,
        "base_shelf_life_days": 18,
        "activation_energy": 48.0,
        "base_price_per_kg": 1.60,
        "spoilage_threshold_days": 3
    },
    "Blueberries": {
        "optimum_temp": 0.5,
        "max_temp": 2.5,
        "min_temp": -0.5,
        "optimum_humidity": 95.0,
        "base_shelf_life_days": 14,
        "activation_energy": 65.0,
        "base_price_per_kg": 7.20,
        "spoilage_threshold_days": 2.5
    },
    "Table Grapes": {
        "optimum_temp": -0.5,
        "max_temp": 1.5,
        "min_temp": -1.0,
        "optimum_humidity": 92.0,
        "base_shelf_life_days": 30,
        "activation_energy": 50.0,
        "base_price_per_kg": 2.90,
        "spoilage_threshold_days": 5
    },
    "Leafy Greens": {
        "optimum_temp": 1.0,
        "max_temp": 3.0,
        "min_temp": 0.0,
        "optimum_humidity": 98.0,
        "base_shelf_life_days": 10,
        "activation_energy": 62.0,
        "base_price_per_kg": 4.10,
        "spoilage_threshold_days": 2
    }
}

# Major Global Logistics Routes & Destinations
ROUTES = [
    {
        "shipment_prefix": "SHP-NL-01",
        "origin": "Guayaquil Port (Ecuador)",
        "destination": "Rotterdam Port (Netherlands)",
        "start_coords": (-2.27, -79.90),
        "end_coords": (51.95, 4.14),
        "distance_km": 9850,
        "alternative_ports": [
            {"name": "Hamburg Port (Germany)", "coords": (53.54, 9.98), "extra_km": 420},
            {"name": "Antwerp Port (Belgium)", "coords": (51.26, 4.33), "extra_km": 110}
        ]
    },
    {
        "shipment_prefix": "SHP-US-02",
        "origin": "Salinas Valley (USA)",
        "destination": "Chicago Freight Hub (USA)",
        "start_coords": (36.67, -121.65),
        "end_coords": (41.87, -87.62),
        "distance_km": 3450,
        "alternative_ports": [
            {"name": "Denver Hub (USA)", "coords": (39.73, -104.99), "extra_km": -1200},
            {"name": "Kansas City Hub (USA)", "coords": (39.09, -94.57), "extra_km": -800}
        ]
    },
    {
        "shipment_prefix": "SHP-ES-03",
        "origin": "Algeciras Port (Spain)",
        "destination": "London Gateway (UK)",
        "start_coords": (36.13, -5.44),
        "end_coords": (51.50, 0.46),
        "distance_km": 2150,
        "alternative_ports": [
            {"name": "Le Havre Port (France)", "coords": (49.49, 0.10), "extra_km": -350},
            {"name": "Dunkirk Port (France)", "coords": (51.03, 2.37), "extra_km": -180}
        ]
    },
    {
        "shipment_prefix": "SHP-OM-04",
        "origin": "Salalah Port (Oman)",
        "destination": "Singapore Port (Singapore)",
        "start_coords": (16.94, 54.00),
        "end_coords": (1.26, 103.84),
        "distance_km": 5600,
        "alternative_ports": [
            {"name": "Port Klang (Malaysia)", "coords": (3.00, 101.40), "extra_km": -300},
            {"name": "Jebel Ali (UAE)", "coords": (24.98, 55.06), "extra_km": -3200}
        ]
    }
]
