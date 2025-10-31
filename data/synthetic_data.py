# data/synthetic_data.py
import random
import datetime


def generate_data():
    # 5 products
    products = [
        (1, "Widget A", 25.0, 0.5, 5),
        (2, "Widget B", 40.0, 0.7, 7),
        (3, "Gadget C", 15.0, 0.3, 3),
        (4, "Gizmo D", 30.0, 0.6, 4),
        (5, "Device E", 55.0, 1.0, 8),
    ]

    # 2 warehouses
    warehouses = [(1, "East Coast DC", 5000), (2, "West Coast DC", 4000)]

    # inventory levels
    inventory = []
    for p in products:
        for w in warehouses:
            current_stock = random.randint(200, 800)
            reorder_point = random.randint(150, 300)
            inventory.append((p[0], w[0], current_stock, reorder_point))

    # 60 days of demand data per product
    demand = []
    start_date = datetime.date(2024, 1, 1)
    for p in products:
        mean_demand = random.randint(50, 100)
        std_dev = mean_demand * 0.2
        for i in range(60):
            date = start_date + datetime.timedelta(days=i)
            quantity = max(0, int(random.gauss(mean_demand, std_dev)))
            demand.append((str(date), p[0], quantity))

    return products, warehouses, inventory, demand
