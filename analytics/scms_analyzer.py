"""
AtmoSync SCMS Supply Chain Dataset Cleaning & Predictive Analytics Engine
Processes USAID SCMS Delivery History Dataset, performs data cleaning, handles missing values,
calculates delivery delays, cost-to-weight metrics, and generates executive supply chain summaries.
"""

import os
import re
import pandas as pd
import numpy as np
from typing import Dict, Any, List


class SCMSDatasetAnalyzer:
    """
    SCMS Delivery History Cleaning & Analytics Engine.
    """

    def __init__(self, raw_csv_path: str = r"d:\AtmoSync\data\scms_dataset.csv"):
        self.raw_csv_path = raw_csv_path
        self.cleaned_csv_path = r"d:\AtmoSync\data\scms_cleaned.csv"
        self.df = None
        self.summary_stats = {}

    def clean_and_transform(self) -> pd.DataFrame:
        """
        Cleans raw SCMS delivery history data.
        """
        if not os.path.exists(self.raw_csv_path):
            raise FileNotFoundError(f"Raw SCMS dataset not found at {self.raw_csv_path}")

        # Read CSV handling BOM and encoding
        df = pd.read_csv(self.raw_csv_path, encoding='latin1')
        
        # Clean column names (strip BOM characters and whitespace)
        df.columns = [re.sub(r'[\ufeff\xef\xbb\xbf]', '', c).strip() for c in df.columns]

        # 1. Clean Dates
        date_cols = ['PQ First Sent to Client Date', 'PO Sent to Vendor Date', 
                     'Scheduled Delivery Date', 'Delivered to Client Date', 'Delivery Recorded Date']
        
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce', format='%d-%b-%y')

        # 2. Calculate Delivery Delay (Days)
        df['Delivery_Delay_Days'] = (df['Delivered to Client Date'] - df['Scheduled Delivery Date']).dt.days
        df['On_Time_Status'] = df['Delivery_Delay_Days'].apply(
            lambda d: 'ON_TIME' if pd.isnull(d) or d <= 0 else ('MINOR_DELAY' if d <= 7 else 'CRITICAL_DELAY')
        )

        # 3. Clean Numeric Columns: Freight Cost, Weight, Line Item Insurance
        df['Freight_Cost_USD_Clean'] = pd.to_numeric(df['Freight Cost (USD)'], errors='coerce')
        df['Weight_KG_Clean'] = pd.to_numeric(df['Weight (Kilograms)'], errors='coerce')
        df['Insurance_USD_Clean'] = pd.to_numeric(df['Line Item Insurance (USD)'], errors='coerce')

        # Fill missing Shipment Mode
        df['Shipment Mode'] = df['Shipment Mode'].fillna('Unknown')

        # Impute missing Freight Cost & Weight using median per Shipment Mode & Product Group
        df['Freight_Cost_USD_Clean'] = df.groupby(['Shipment Mode'])['Freight_Cost_USD_Clean'].transform(
            lambda x: x.fillna(x.median())
        ).fillna(0.0)

        df['Weight_KG_Clean'] = df.groupby(['Shipment Mode'])['Weight_KG_Clean'].transform(
            lambda x: x.fillna(x.median())
        ).fillna(0.0)

        df['Insurance_USD_Clean'] = df['Insurance_USD_Clean'].fillna(0.0)

        # 4. Calculate Freight-to-Weight Ratio
        df['Cost_Per_KG_USD'] = np.where(
            df['Weight_KG_Clean'] > 0, 
            np.round(df['Freight_Cost_USD_Clean'] / df['Weight_KG_Clean'], 2), 
            0.0
        )

        self.df = df
        
        # Save cleaned dataset
        os.makedirs(os.path.dirname(self.cleaned_csv_path), exist_ok=True)
        df.to_csv(self.cleaned_csv_path, index=False)
        print(f"[SCMS Analyzer] Cleaned dataset saved to {self.cleaned_csv_path}")

        return df

    def generate_analytics_summary(self) -> Dict[str, Any]:
        """
        Computes aggregate metrics for executive dashboard presentation.
        """
        if self.df is None:
            self.clean_and_transform()

        df = self.df
        total_shipments = len(df)
        total_line_value = round(float(df['Line Item Value'].sum()), 2)
        total_freight_cost = round(float(df['Freight_Cost_USD_Clean'].sum()), 2)
        total_weight_kg = round(float(df['Weight_KG_Clean'].sum()), 2)

        # On-Time Delivery Breakdown
        on_time_counts = df['On_Time_Status'].value_counts().to_dict()
        on_time_pct = round((on_time_counts.get('ON_TIME', 0) / max(1, total_shipments)) * 100.0, 2)

        # Top Countries by Shipment Count
        top_countries = df['Country'].value_counts().head(10).to_dict()

        # Shipment Mode Cost & Delay Metrics
        mode_metrics = []
        for mode, group in df.groupby('Shipment Mode'):
            mode_metrics.append({
                "shipment_mode": mode,
                "shipment_count": len(group),
                "total_freight_usd": round(float(group['Freight_Cost_USD_Clean'].sum()), 2),
                "avg_delay_days": round(float(group['Delivery_Delay_Days'].dropna().mean()), 1) if not group['Delivery_Delay_Days'].dropna().empty else 0.0,
                "on_time_rate_pct": round((len(group[group['On_Time_Status'] == 'ON_TIME']) / max(1, len(group))) * 100.0, 1)
            })

        # Product Group Breakdown
        product_groups = []
        for pg, group in df.groupby('Product Group'):
            product_groups.append({
                "product_group": pg,
                "total_quantity": int(group['Line Item Quantity'].sum()),
                "total_value_usd": round(float(group['Line Item Value'].sum()), 2),
                "shipment_count": len(group)
            })

        return {
            "dataset_name": "SCMS Delivery History (USAID Global Health)",
            "total_shipments": total_shipments,
            "total_line_item_value_usd": total_line_value,
            "total_freight_cost_usd": total_freight_cost,
            "total_weight_kg": total_weight_kg,
            "on_time_delivery_pct": on_time_pct,
            "on_time_distribution": on_time_counts,
            "top_destination_countries": top_countries,
            "shipment_mode_breakdown": mode_metrics,
            "product_group_breakdown": product_groups
        }


# Global instance
scms_analyzer = SCMSDatasetAnalyzer()

if __name__ == "__main__":
    df_clean = scms_analyzer.clean_and_transform()
    summary = scms_analyzer.generate_analytics_summary()
    print("SCMS Analytics Summary Total Shipments:", summary["total_shipments"])
    print("Total Line Item Value USD: $", f"{summary['total_line_item_value_usd']:,}")
    print("On Time Delivery Pct:", summary["on_time_delivery_pct"], "%")
