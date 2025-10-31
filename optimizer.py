# optimizer.py
import math
import pandas as pd
from utils.db_utils import fetch_table

# Configurable constants
ORDERING_COST = 100  # cost per order
SERVICE_LEVEL_Z = 1.65  # 95% service level


def calculate_eoq(D, S, H):
    """Economic Order Quantity"""
    return math.sqrt((2 * D * S) / H)


def calculate_safety_stock(std_demand, lead_time):
    """Safety stock = Z * std_dev * sqrt(lead_time)"""
    return SERVICE_LEVEL_Z * std_demand * math.sqrt(lead_time)


def run_inventory_optimization():
    products_df = fetch_table("products")
    demand_df = fetch_table("demand")

    results = []

    for _, product in products_df.iterrows():
        pid = product["id"]
        name = product["name"]
        unit_cost = product["unit_cost"]
        holding_cost = product["holding_cost"]
        lead_time = product["lead_time_days"]

        # Estimate average & std demand
        product_demand = demand_df[demand_df["product_id"] == pid]["quantity"]
        avg_daily_demand = product_demand.mean()
        std_daily_demand = product_demand.std()

        annual_demand = avg_daily_demand * 365
        H = unit_cost * holding_cost

        eoq = calculate_eoq(annual_demand, ORDERING_COST, H)
        safety_stock = calculate_safety_stock(std_daily_demand, lead_time)
        reorder_point = avg_daily_demand * lead_time + safety_stock

        results.append(
            {
                "product_id": pid,
                "product_name": name,
                "EOQ": round(eoq, 2),
                "Reorder_Point": round(reorder_point, 2),
                "Safety_Stock": round(safety_stock, 2),
                "Avg_Daily_Demand": round(avg_daily_demand, 2),
                "Lead_Time": lead_time,
            }
        )

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = run_inventory_optimization()
    print(df)
