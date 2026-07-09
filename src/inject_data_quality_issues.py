import os
import random
import pandas as pd

random.seed(42)


def inject_customer_issues():

    customers = pd.read_csv("data/customers.csv")

    print("\n========== CUSTOMERS ==========")

    duplicates = customers.sample(20, random_state=42)
    customers = pd.concat([customers, duplicates], ignore_index=True)

    customers.loc[
        customers.sample(30, random_state=1).index,
        "email"
    ] = None

    customers.loc[
        customers.sample(25, random_state=2).index,
        "phone"
    ] = None

    customers.loc[
        customers.sample(20, random_state=3).index,
        "customer_name"
    ] = (
        customers.loc[
            customers.sample(20, random_state=3).index,
            "customer_name"
        ] + "   "
    )

    customers.loc[
        customers.sample(20, random_state=4).index,
        "city"
    ] = (
        customers.loc[
            customers.sample(20, random_state=4).index,
            "city"
        ].str.upper()
    )

    customers.to_csv(
        "data/customers_dirty.csv",
        index=False
    )

    print("customers_dirty.csv created")


def inject_product_issues():

    products = pd.read_csv("data/products.csv")

    print("\n========== PRODUCTS ==========")

    duplicates = products.sample(15, random_state=42)

    products = pd.concat(
        [products, duplicates],
        ignore_index=True
    )

    products.loc[
        products.sample(15, random_state=5).index,
        "price"
    ] = None

    products.loc[
        products.sample(10, random_state=6).index,
        "stock"
    ] = -10

    products.loc[
        products.sample(15, random_state=7).index,
        "product_name"
    ] = (
        products.loc[
            products.sample(15, random_state=7).index,
            "product_name"
        ] + "   "
    )

    products.to_csv(
        "data/products_dirty.csv",
        index=False
    )

    print("products_dirty.csv created")


def inject_order_issues():

    orders = pd.read_csv("data/orders.csv")

    print("\n========== ORDERS ==========")

    orders.loc[
        orders.sample(20, random_state=8).index,
        "payment_method"
    ] = "Bitcoin"

    orders.loc[
        orders.sample(10, random_state=9).index,
        "order_status"
    ] = "Unknown"

    orders.loc[
        orders.sample(10, random_state=10).index,
        "order_date"
    ] = None

    orders.to_csv(
        "data/orders_dirty.csv",
        index=False
    )

    print("orders_dirty.csv created")


def inject_order_item_issues():

    items = pd.read_csv("data/order_items.csv")

    print("\n========== ORDER ITEMS ==========")

    items.loc[
        items.sample(20, random_state=11).index,
        "quantity"
    ] = -2

    items.loc[
        items.sample(15, random_state=12).index,
        "discount"
    ] = 200

    items.loc[
        items.sample(10, random_state=13).index,
        "unit_price"
    ] = None

    items.to_csv(
        "data/order_items_dirty.csv",
        index=False
    )

    print("order_items_dirty.csv created")


if __name__ == "__main__":

    os.makedirs("data", exist_ok=True)

    inject_customer_issues()
    inject_product_issues()
    inject_order_issues()
    inject_order_item_issues()

    print("\nAll dirty datasets generated successfully.")