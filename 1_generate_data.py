import random
from datetime import datetime

# Sample data lists to pick from
PRODUCTS = [
    ("Laptop", "Electronics", 800),
    ("Mouse", "Electronics", 25),
    ("Keyboard", "Electronics", 50),
    ("Desk Chair", "Furniture", 150),
    ("Coffee Maker", "Kitchen", 40),
    ("Running Shoes", "Apparel", 75),
]

PAYMENT_METHODS = ["Card", "UPI", "PayPal", "Net Banking"]
CITIES = ["New York", "San Francisco", "Chicago", "Seattle", "Austin"]
STATUSES = ["Completed", "Pending", "Cancelled"]


def generate_order(order_id):
    """Generates a single sales order dictionary."""
    product, category, price = random.choice(PRODUCTS)
    quantity = random.randint(1, 4)
    total_amount = round(quantity * price, 2)

    order = {
        "order_id": order_id,
        "customer_id": f"CUST_{random.randint(101, 120)}",
        "product": product,
        "category": category,
        "quantity": quantity,
        "price": price,
        "total_amount": total_amount,
        "payment_method": random.choice(PAYMENT_METHODS),
        "city": random.choice(CITIES),
        "status": random.choice(STATUSES),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return order


if __name__ == "__main__":
    print("--- Generating 5 Sample Orders ---")
    
    for i in range(1, 6):
        order = generate_order(order_id=1000 + i)
        print(f"\nOrder #{i}:")
        for key, value in order.items():
            print(f"  {key}: {value}")
