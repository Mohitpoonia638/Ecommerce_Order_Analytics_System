import pandas as pd
import os


def clean_customers():

    customers = pd.read_csv("data/customers_dirty.csv")

    print("=" * 50)
    print("CUSTOMER CLEANING STARTED")
    print("=" * 50)

    rows_before = len(customers)

    # -----------------------------
    # Remove duplicate customers
    # -----------------------------

    duplicate_count = customers.duplicated(
        subset="customer_id"
    ).sum()

    customers = customers.drop_duplicates(
        subset="customer_id"
    )

    # -----------------------------
    # Remove extra spaces
    # -----------------------------

    customers["customer_name"] = (
        customers["customer_name"]
        .str.strip()
    )

    # -----------------------------
    # Standardize city names
    # -----------------------------

    customers["city"] = (
        customers["city"]
        .str.title()
    )

    # -----------------------------
    # Fill missing email
    # -----------------------------

    missing_email = customers["email"].isna().sum()

    customers["email"] = customers.apply(
        lambda row:
        f"{row['customer_id'].lower()}@generated.com"
        if pd.isna(row["email"])
        else row["email"],
        axis=1
    )

    # -----------------------------
    # Fill missing phone
    # -----------------------------

    missing_phone = customers["phone"].isna().sum()

    customers["phone"] = customers["phone"].fillna("9999999999")

    rows_after = len(customers)

    os.makedirs("data", exist_ok=True)

    customers.to_csv(
        "data/customers_clean.csv",
        index=False
    )

    print()
    print("Cleaning Report")
    print("-" * 30)
    print(f"Rows Before Cleaning : {rows_before}")
    print(f"Rows After Cleaning  : {rows_after}")
    print(f"Duplicates Removed   : {duplicate_count}")
    print(f"Emails Filled        : {missing_email}")
    print(f"Phones Filled        : {missing_phone}")
    print()
    print("customers_clean.csv created successfully.")
    print("=" * 50)


def clean_products():

    products = pd.read_csv("data/products_dirty.csv")

    print("=" * 50)
    print("PRODUCT CLEANING STARTED")
    print("=" * 50)

    rows_before = len(products)

    # -----------------------------
    # Remove duplicate products
    # -----------------------------
    duplicate_count = products.duplicated(
        subset="product_id"
    ).sum()

    products = products.drop_duplicates(
        subset="product_id"
    )

    # -----------------------------
    # Fill missing prices
    # -----------------------------
    missing_prices = products["price"].isna().sum()

    median_price = products["price"].median()

    products["price"] = products["price"].fillna(
        median_price
    )

    # -----------------------------
    # Fix negative stock
    # -----------------------------
    negative_stock = (products["stock"] < 0).sum()

    products.loc[
        products["stock"] < 0,
        "stock"
    ] = (
        products.loc[
            products["stock"] < 0,
            "stock"
        ].abs()
    )

    # -----------------------------
    # Remove extra spaces
    # -----------------------------
    products["product_name"] = (
        products["product_name"]
        .str.strip()
    )

    rows_after = len(products)

    products.to_csv(
        "data/products_clean.csv",
        index=False
    )

    print()
    print("Cleaning Report")
    print("-" * 30)
    print(f"Rows Before Cleaning : {rows_before}")
    print(f"Rows After Cleaning  : {rows_after}")
    print(f"Duplicates Removed   : {duplicate_count}")
    print(f"Prices Filled        : {missing_prices}")
    print(f"Negative Stock Fixed : {negative_stock}")
    print()
    print("products_clean.csv created successfully.")
    print("=" * 50)   

def clean_orders():

    orders = pd.read_csv("data/orders_dirty.csv")

    print("=" * 50)
    print("ORDER CLEANING STARTED")
    print("=" * 50)

    rows_before = len(orders)

    valid_payment_methods = [
        "UPI",
        "Credit Card",
        "Debit Card",
        "Net Banking",
        "Cash on Delivery",
        "Wallet"
    ]

    valid_status = [
        "Delivered",
        "Shipped",
        "Processing",
        "Cancelled",
        "Returned"
    ]

    invalid_payment = (~orders["payment_method"].isin(valid_payment_methods)).sum()

    orders.loc[
        ~orders["payment_method"].isin(valid_payment_methods),
        "payment_method"
    ] = "UPI"

    invalid_status = (~orders["order_status"].isin(valid_status)).sum()

    orders.loc[
        ~orders["order_status"].isin(valid_status),
        "order_status"
    ] = "Processing"

    missing_dates = orders["order_date"].isna().sum()

    orders["order_date"] = orders["order_date"].fillna(
        pd.Timestamp.today().date()
    )

    rows_after = len(orders)

    orders.to_csv(
        "data/orders_clean.csv",
        index=False
    )

    print()
    print("Cleaning Report")
    print("-" * 30)
    print(f"Rows Before Cleaning : {rows_before}")
    print(f"Rows After Cleaning  : {rows_after}")
    print(f"Invalid Payments Fixed : {invalid_payment}")
    print(f"Invalid Status Fixed   : {invalid_status}")
    print(f"Missing Dates Filled   : {missing_dates}")
    print()
    print("orders_clean.csv created successfully.")
    print("=" * 50)

def clean_order_items():

    items = pd.read_csv("data/order_items_dirty.csv")

    print("=" * 50)
    print("ORDER ITEMS CLEANING STARTED")
    print("=" * 50)

    rows_before = len(items)

    # -----------------------------
    # Fix negative quantity
    # -----------------------------
    negative_quantity = (items["quantity"] <= 0).sum()

    items.loc[
        items["quantity"] <= 0,
        "quantity"
    ] = 1

    # -----------------------------
    # Fix invalid discount
    # -----------------------------
    invalid_discount = (
        (items["discount"] < 0) |
        (items["discount"] > 100)
    ).sum()

    items.loc[
        (items["discount"] < 0) |
        (items["discount"] > 100),
        "discount"
    ] = 0

    # -----------------------------
    # Fill missing unit price
    # -----------------------------
    missing_price = items["unit_price"].isna().sum()

    median_price = items["unit_price"].median()

    items["unit_price"] = items["unit_price"].fillna(
        median_price
    )

    # -----------------------------
    # Recalculate line total
    # -----------------------------
    items["line_total"] = (
        items["quantity"]
        * items["unit_price"]
        * (100 - items["discount"])
        / 100
    )

    rows_after = len(items)

    items.to_csv(
        "data/order_items_clean.csv",
        index=False
    )

    print()
    print("Cleaning Report")
    print("-" * 30)
    print(f"Rows Before Cleaning : {rows_before}")
    print(f"Rows After Cleaning  : {rows_after}")
    print(f"Negative Quantity Fixed : {negative_quantity}")
    print(f"Invalid Discount Fixed : {invalid_discount}")
    print(f"Missing Prices Filled  : {missing_price}")
    print()
    print("order_items_clean.csv created successfully.")
    print("=" * 50)

if __name__ == "__main__":

    clean_customers()
    clean_products()
    clean_orders()
    clean_order_items()    