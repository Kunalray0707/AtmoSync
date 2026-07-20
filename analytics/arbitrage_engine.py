"""
AtmoSync Arbitrage & Rerouting Recommendation Engine
Calculates net financial gain from diverting container routes based on micro-climate shelf life vs spot prices.
"""

from typing import Dict, Any, List
from analytics.spoilage_engine import calculate_spoilage_metrics

CARGO_WEIGHT_KG = 20000.0  # 20 metric tons per 40ft High Cube Reefer Container
TRANSPORT_COST_PER_KM = 1.85  # USD per km reroute fuel & vessel diversion cost


def evaluate_arbitrage_opportunity(telemetry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates spot prices across alternative destinations and computes net financial delta.
    """
    spoilage = calculate_spoilage_metrics(telemetry)
    
    primary_destination = telemetry.get("destination", "Rotterdam Port")
    current_market_price = float(telemetry.get("market_price", 3.50))
    remaining_rsl_hours = float(spoilage["remaining_shelf_life_hours"])
    spoilage_risk_pct = float(spoilage["spoilage_risk_score_pct"])
    
    # 1. Primary Destination Financial Outlook
    rem_dist_primary = float(telemetry.get("remaining_distance_km", 2000.0))
    gps_speed = float(telemetry.get("gps_speed", 35.0))
    eta_hours_primary = rem_dist_primary / max(gps_speed, 10.0)
    
    # Projected quality multiplier at primary arrival
    hours_headroom_primary = remaining_rsl_hours - eta_hours_primary
    if hours_headroom_primary < 0:
        # Spoiled on arrival -> cargo rejection penalty
        quality_multiplier_primary = max(0.0, 1.0 - (abs(hours_headroom_primary) * 0.08))
    else:
        quality_multiplier_primary = min(1.0, (hours_headroom_primary / remaining_rsl_hours))
        
    projected_revenue_primary = CARGO_WEIGHT_KG * current_market_price * quality_multiplier_primary
    
    # 2. Alternative Port Evaluation
    alternatives = telemetry.get("alternative_destinations", [])
    best_alternative = None
    max_net_profit_delta = 0.0
    
    evaluated_alternatives = []
    
    for alt in alternatives:
        alt_name = alt.get("name", "Alternative Hub")
        extra_km = float(alt.get("extra_km", 200.0))
        alt_distance = max(100.0, rem_dist_primary + extra_km)
        alt_eta_hours = alt_distance / max(gps_speed, 10.0)
        
        # Spot market premium or discount at alternative port (+5% to +25% market differential)
        alt_market_price = current_market_price * (1.12 if extra_km < 0 else 1.08)
        
        alt_headroom = remaining_rsl_hours - alt_eta_hours
        if alt_headroom < 0:
            alt_quality_mult = max(0.0, 1.0 - (abs(alt_headroom) * 0.08))
        else:
            alt_quality_mult = min(1.0, (alt_headroom / remaining_rsl_hours))
            
        alt_gross_revenue = CARGO_WEIGHT_KG * alt_market_price * alt_quality_mult
        reroute_cost = abs(extra_km) * TRANSPORT_COST_PER_KM + 500.0  # port diversion surcharge
        alt_net_revenue = alt_gross_revenue - reroute_cost
        
        net_profit_delta = alt_net_revenue - projected_revenue_primary
        
        alt_data = {
            "destination": alt_name,
            "extra_distance_km": extra_km,
            "eta_hours": round(alt_eta_hours, 1),
            "spot_market_price_per_kg": round(alt_market_price, 2),
            "projected_gross_revenue_usd": round(alt_gross_revenue, 2),
            "reroute_cost_usd": round(reroute_cost, 2),
            "net_revenue_usd": round(alt_net_revenue, 2),
            "net_profit_delta_usd": round(net_profit_delta, 2)
        }
        evaluated_alternatives.append(alt_data)
        
        if net_profit_delta > max_net_profit_delta:
            max_net_profit_delta = net_profit_delta
            best_alternative = alt_data
            
    # 3. Arbitrage Score & Recommendation Logic
    arbitrage_score = min(100.0, max(0.0, (max_net_profit_delta / 5000.0) * 100.0))
    
    if max_net_profit_delta > 3000.0 or (hours_headroom_primary < 0 and max_net_profit_delta > 500.0):
        recommendation = "REROUTE_RECOMMENDED"
    elif hours_headroom_primary < -10:
        recommendation = "URGENT_LIQUIDATION_REQUIRED"
    else:
        recommendation = "MAINTAIN_CURRENT_ROUTE"
        
    return {
        "container_id": telemetry.get("container_id"),
        "shipment_id": telemetry.get("shipment_id"),
        "primary_destination": primary_destination,
        "primary_eta_hours": round(eta_hours_primary, 1),
        "primary_projected_revenue_usd": round(projected_revenue_primary, 2),
        "arbitrage_score": round(arbitrage_score, 1),
        "max_net_profit_delta_usd": round(max_net_profit_delta, 2),
        "recommendation": recommendation,
        "best_alternative_destination": best_alternative,
        "all_evaluated_options": evaluated_alternatives
    }


if __name__ == "__main__":
    test_event = {
        "container_id": "CONT-1002",
        "shipment_id": "SHP-NL-01-202",
        "commodity": "Avocados",
        "temperature": 9.2,
        "humidity": 88.0,
        "destination": "Rotterdam Port",
        "market_price": 3.40,
        "remaining_distance_km": 1500,
        "gps_speed": 30.0,
        "alternative_destinations": [
            {"name": "Hamburg Port", "extra_km": 350},
            {"name": "Antwerp Port", "extra_km": -200}
        ]
    }
    arb_res = evaluate_arbitrage_opportunity(test_event)
    print("Arbitrage Engine Test Result:", arb_res)
