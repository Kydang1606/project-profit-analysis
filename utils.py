# utils.py
from constants import HOURLY_RATES

def calculate_costs(data: dict, profit_margin_percent: float) -> dict:
    # Hourly cost
    cost_worker = data["Worker Hours"] * HOURLY_RATES["Worker"]
    cost_office = data["Office Hours"] * HOURLY_RATES["Office"]
    cost_cnc = data["CNC Hours"] * HOURLY_RATES["CNC"]
    cost_robot = data["Robot Hours"] * HOURLY_RATES["Robot"]
    cost_autoclave = data["Autoclave Hours"] * HOURLY_RATES["Autoclave"]

    # Total machine cost
    total_machine_cost = cost_cnc + cost_robot + cost_autoclave

    # Sum of all
    cost_material = data["Material Cost"]
    total_cost = cost_worker + cost_office + total_machine_cost + cost_material

    # Estimated price before profit
    base_price = total_cost

    # Estimated selling price
    profit = (profit_margin_percent / 100) * base_price
    selling_price = base_price + profit

    return {
        "Cost (Worker)": cost_worker,
        "Cost (Office)": cost_office,
        "Cost (Machines)": total_machine_cost,
        "Cost (Material)": cost_material,
        "Total Cost": total_cost,
        "Base Price": base_price,
        "Selling Price": selling_price,
    }
