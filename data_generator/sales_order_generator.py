import random
import csv
from datetime import datetime, timedelta

# Funkcja do generowania zamówień sprzedaży
def generate_sales_orders(inventory_file, customers_file, output_file, num_orders=1000):
    # Wczytaj dane zapasów
    with open(inventory_file, mode="r", encoding="utf-8") as file:
        inventory = [row for row in csv.DictReader(file)]
    fg_inventory = [item for item in inventory if item["Item Type"] == "FG"]  # Wyroby gotowe

    # Wczytaj dane klientów
    with open(customers_file, mode="r", encoding="utf-8") as file:
        customers = [row for row in csv.DictReader(file)]

    # Generowanie zamówień
    sales_orders = []
    start_date = datetime(2025, 1, 12)  # Pierwsza data realizacji
    customer_ids = [customer["Customer ID"] for customer in customers]
    item_ids = [item["Item ID"] for item in fg_inventory]

    for order_id in range(1, num_orders + 1):
        customer_id = random.choice(customer_ids)
        item_id = random.choice(item_ids)
        quantity = random.choices([1, 2, 4], weights=[80, 15, 5])[0]  # Ilość: 80% = 1, 15% = 2, 5% = 4
        delivery_date = start_date + timedelta(days=random.randint(0, 353))  # Rok 2025, od 12.01
        sales_orders.append({
            "Order ID": f"SO-{order_id:04d}",
            "Customer ID": customer_id,
            "Item ID": item_id,
            "Quantity": quantity,
            "Delivery Date": delivery_date.strftime("%Y-%m-%d")
        })

    # Zapis do pliku CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Order ID", "Customer ID", "Item ID", "Quantity", "Delivery Date"])
        writer.writeheader()
        writer.writerows(sales_orders)

    print(f"Sales orders data generated successfully in {output_file}.")

