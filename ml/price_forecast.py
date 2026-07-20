"""
AtmoSync Commodity Spot Price Forecaster
Generates multi-day price trajectory forecasts across target market destinations 
to identify profitable arbitrage rerouting windows.
"""

from typing import Dict, Any, List
import random
from datetime import datetime, timedelta


class PriceForecaster:
    """
    Time-Series Commodity Spot Price Forecaster.
    """

    BASE_MARKET_PRICES = {
        "Avocados": {"Rotterdam": 3400.0, "Hamburg": 3650.0, "Antwerp": 3320.0, "Le Havre": 3580.0},
        "Strawberries": {"Rotterdam": 4800.0, "Hamburg": 5100.0, "Antwerp": 4700.0, "Le Havre": 4950.0},
        "Salmon": {"Rotterdam": 9200.0, "Hamburg": 9800.0, "Antwerp": 9100.0, "Le Havre": 9500.0},
        "Vaccines": {"Rotterdam": 125000.0, "Hamburg": 128000.0, "Antwerp": 124000.0, "Le Havre": 127000.0},
        "Bananas": {"Rotterdam": 1450.0, "Hamburg": 1600.0, "Antwerp": 1420.0, "Le Havre": 1550.0}
    }

    def forecast_prices(self, commodity: str, days_ahead: int = 7) -> Dict[str, Any]:
        """
        Generates daily price forecasts per destination market over specified forecast horizon.
        """
        commodity_prices = self.BASE_MARKET_PRICES.get(commodity, self.BASE_MARKET_PRICES["Avocados"])
        
        forecast_results = {}
        today = datetime.now()

        for market, base_price in commodity_prices.items():
            daily_series = []
            current_price = base_price
            
            for d in range(days_ahead):
                date_str = (today + timedelta(days=d)).strftime("%Y-%m-%d")
                # Trend + seasonal micro fluctuations
                trend = (d * 12.5) if market == "Hamburg" else (d * -5.0 if market == "Antwerp" else d * 3.0)
                noise = (random.random() - 0.48) * (base_price * 0.015)
                projected_price = round(base_price + trend + noise, 2)
                
                daily_series.append({
                    "date": date_str,
                    "day_offset": d,
                    "price_per_ton": projected_price
                })
            
            forecast_results[market] = daily_series

        return {
            "commodity": commodity,
            "forecast_horizon_days": days_ahead,
            "generated_at": today.isoformat(),
            "markets": forecast_results
        }


price_forecaster = PriceForecaster()

if __name__ == "__main__":
    fc = price_forecaster.forecast_prices("Avocados", days_ahead=7)
    print("Price Forecast Test Result:", fc["commodity"], "Markets:", list(fc["markets"].keys()))
