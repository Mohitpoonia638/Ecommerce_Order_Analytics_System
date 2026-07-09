import pandas as pd
import random
import os
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker("en_IN")

# Make random generation reproducible
random.seed(42)
Faker.seed(42)

NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 300
NUM_ORDERS = 5000
MAX_ITEMS_PER_ORDER = 5

PRODUCT_CATALOG = {
    "Electronics": {
        "Apple": ["iPhone 15", "iPhone 15 Plus", "Apple Watch Series 10"],
        "Samsung": ["Galaxy S24", "Galaxy Tab S9", "Samsung Smart TV"],
        "OnePlus": ["OnePlus 13", "OnePlus Nord CE4"],
        "Dell": ["Inspiron 15", "XPS 13"],
        "HP": ["Pavilion 15", "Victus Laptop"],
        "Boat": ["Airdopes 141", "Stone Speaker"],
        "Sony": ["WH-1000XM5", "PlayStation Controller"]
    },

    "Fashion": {
        "Nike": ["Running Shoes", "Sports T-Shirt"],
        "Adidas": ["Sneakers", "Track Pants"],
        "Puma": ["Hoodie", "Sneakers"],
        "Levi's": ["Jeans", "Denim Jacket"],
        "Allen Solly": ["Formal Shirt"],
        "Titan": ["Analog Watch"]
    },

    "Home & Kitchen": {
        "Prestige": ["Pressure Cooker", "Gas Stove"],
        "Philips": ["Mixer Grinder", "Steam Iron"],
        "LG": ["Microwave Oven"],
        "Kent": ["Water Purifier"],
        "Milton": ["Water Bottle"],
        "Butterfly": ["Cookware Set"]
    },

    "Books": {
        "Penguin": [
            "Atomic Habits",
            "Rich Dad Poor Dad",
            "Clean Code",
            "Python Crash Course",
            "SQL Cookbook"
        ]
    },

    "Beauty": {
        "Lakme": ["Lipstick"],
        "Nivea": ["Face Wash"],
        "Dove": ["Shampoo", "Soap"],
        "Mamaearth": ["Face Cream"],
        "Garnier": ["Vitamin C Serum"]
    }
}

PRICE_RANGE = {
    "Electronics": (2000, 90000),
    "Fashion": (500, 7000),
    "Home & Kitchen": (300, 25000),
    "Books": (200, 2500),
    "Beauty": (150, 3000)
}

MIN_STOCK = 20
MAX_STOCK = 300

ORDER_STATUS = [
    "Delivered",
    "Shipped",
    "Processing",
    "Cancelled",
    "Returned"
]

ORDER_STATUS_WEIGHTS = [
    80,
    10,
    5,
    3,
    2
]

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Cash on Delivery",
    "Wallet"
]

PAYMENT_WEIGHTS = [
    40,
    20,
    15,
    10,
    10,
    5
]

DISCOUNTS = [0, 5, 10, 15, 20]

DISCOUNT_WEIGHTS = [
    45,
    20,
    20,
    10,
    5
]


COLORS = [
    "Black",
    "White",
    "Blue",
    "Red",
    "Silver",
    "Green"
]

STORAGE = [
    "64GB",
    "128GB",
    "256GB",
    "512GB"
]

SIZES = [
    "S",
    "M",
    "L",
    "XL"
]

SHOE_SIZES = [
    "7",
    "8",
    "9",
    "10"
]

def generate_customers():
    customers = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        customers.append({
            "customer_id": f"CUST{customer_id:05}",
            "customer_name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "city": fake.city(),
            "state": fake.state(),
            "registration_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            )
        })

    customer_df = pd.DataFrame(customers)

    os.makedirs("data", exist_ok=True)

    customer_df.to_csv(
        "data/customers.csv",
        index=False
    )

    print(f"Generated {len(customer_df)} customers.")

    return customer_df


def generate_products():

    products = []
    product_id = 1

    for category, brands in PRODUCT_CATALOG.items():

        min_price, max_price = PRICE_RANGE[category]

        for brand, product_list in brands.items():

            for product in product_list:

                variants = []

                if category == "Electronics":

                    for storage in STORAGE:
                        for color in COLORS:
                            variants.append(f"{product} {storage} {color}")

                elif category == "Fashion":

                    if "Shoes" in product or "Sneakers" in product:

                        for size in SHOE_SIZES:
                            variants.append(f"{product} Size-{size}")

                    else:

                        for size in SIZES:
                            variants.append(f"{product} {size}")

                else:

                    variants.append(product)

                for item in variants:

                    products.append({

                        "product_id": f"PROD{product_id:05}",

                        "brand": brand,

                        "category": category,

                        "product_name": item,

                        "price": random.randint(min_price, max_price),

                        "stock": random.randint(MIN_STOCK, MAX_STOCK)

                    })

                    product_id += 1

    product_df = pd.DataFrame(products)

    os.makedirs("data", exist_ok=True)

    product_df.to_csv(
        "data/products.csv",
        index=False
    )

    print(f"Generated {len(product_df)} products.")

    return product_df

def generate_orders(customers_df):

    orders = []

    for order_num in range(1, NUM_ORDERS + 1):

        customer = customers_df.sample(1).iloc[0]

        orders.append({

            "order_id": f"ORD{order_num:06}",

            "customer_id": customer["customer_id"],

            "order_date": fake.date_between(
                start_date="-2y",
                end_date="today"
            ),

            "payment_method": random.choices(
                PAYMENT_METHODS,
                weights=PAYMENT_WEIGHTS,
                k=1
            )[0],

            "order_status": random.choices(
                ORDER_STATUS,
                weights=ORDER_STATUS_WEIGHTS,
                k=1
            )[0],

            
            "total_amount": 0.0
        })

    orders_df = pd.DataFrame(orders)

    os.makedirs("data", exist_ok=True)

    orders_df.to_csv(
        "data/orders.csv",
        index=False
    )

    print(f"Generated {len(orders_df)} orders.")

    return orders_df

def generate_order_items(orders_df, products_df):

    order_items = []
    order_item_id = 1

    for index, order in orders_df.iterrows():

        num_items = random.randint(1, MAX_ITEMS_PER_ORDER)

        selected_products = products_df.sample(
            n=num_items,
            replace=False
        )

        order_total = 0

        for _, product in selected_products.iterrows():

            quantity = random.randint(1, 4)

            discount = random.choices(
                DISCOUNTS,
                weights=DISCOUNT_WEIGHTS,
                k=1
            )[0]

            unit_price = product["price"]

            line_total = quantity * unit_price * (1 - discount / 100)

            order_items.append({

                "order_item_id": f"ITEM{order_item_id:07}",

                "order_id": order["order_id"],

                "product_id": product["product_id"],

                "quantity": quantity,

                "unit_price": unit_price,

                "discount": discount,

                "line_total": round(line_total, 2)

            })

            order_total += line_total

            order_item_id += 1

        orders_df.at[index, "total_amount"] = round(order_total, 2)

    order_items_df = pd.DataFrame(order_items)

    os.makedirs("data", exist_ok=True)

    order_items_df.to_csv(
        "data/order_items.csv",
        index=False
    )

    orders_df.to_csv(
        "data/orders.csv",
        index=False
    )

    print(f"Generated {len(order_items_df)} order items.")

    return order_items_df

if __name__ == "__main__":

    customers_df = generate_customers()

    products_df = generate_products()

    orders_df = generate_orders(customers_df)

    order_items_df = generate_order_items(
        orders_df,
        products_df
    )


