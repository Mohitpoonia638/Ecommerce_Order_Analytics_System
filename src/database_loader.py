import os
import sqlite3
import pandas as pd


DB_PATH = "database/ecommerce.db"


def load_database():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    print("=" * 50)
    print("LOADING DATABASE")
    print("=" * 50)

    customers = pd.read_csv("data/customers_clean.csv")
    products = pd.read_csv("data/products_clean.csv")
    orders = pd.read_csv("data/orders_clean.csv")
    order_items = pd.read_csv("data/order_items_clean.csv")

    customers.to_sql(
        "customers",
        conn,
        if_exists="replace",
        index=False
    )

    products.to_sql(
        "products",
        conn,
        if_exists="replace",
        index=False
    )

    orders.to_sql(
        "orders",
        conn,
        if_exists="replace",
        index=False
    )

    order_items.to_sql(
        "order_items",
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Customers Loaded   : {len(customers)}")
    print(f"Products Loaded    : {len(products)}")
    print(f"Orders Loaded      : {len(orders)}")
    print(f"Order Items Loaded : {len(order_items)}")

    conn.commit()
    conn.close()

    print()
    print("Database created successfully.")
    print(f"Location : {DB_PATH}")
    print("=" * 50)


if __name__ == "__main__":
    load_database()