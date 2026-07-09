import sqlite3

DB_PATH = "database/ecommerce.db"


def generate_report():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("E-COMMERCE REPORT GENERATOR")
    print("=" * 60)

    report_type = input(
        "Enter report type (daily/weekly/monthly): "
    ).lower()

    start_date = input(
        "Enter start date (YYYY-MM-DD): "
    )

    end_date = input(
        "Enter end date (YYYY-MM-DD): "
    )

    print("\nGenerating", report_type, "report...\n")

    # -----------------------------------------
    # Total Orders
    # -----------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE order_date
        BETWEEN ? AND ?;
    """, (start_date, end_date))

    total_orders = cursor.fetchone()[0]

    # -----------------------------------------
    # Revenue
    # -----------------------------------------

    cursor.execute("""
        SELECT ROUND(
            SUM(total_amount),
            2
        )
        FROM orders
        WHERE order_date
        BETWEEN ? AND ?;
    """, (start_date, end_date))

    revenue = cursor.fetchone()[0]

    if revenue is None:
        revenue = 0

    # -----------------------------------------
    # Unique Customers
    # -----------------------------------------

    cursor.execute("""
        SELECT COUNT(
            DISTINCT customer_id
        )
        FROM orders
        WHERE order_date
        BETWEEN ? AND ?;
    """, (start_date, end_date))

    unique_customers = cursor.fetchone()[0]

    # -----------------------------------------
    # Top 3 Products
    # -----------------------------------------

    cursor.execute("""

        SELECT

            p.product_name,

            SUM(oi.quantity) AS total_quantity

        FROM order_items oi

        JOIN orders o

            ON oi.order_id = o.order_id

        JOIN products p

            ON oi.product_id = p.product_id

        WHERE o.order_date
        BETWEEN ? AND ?

        GROUP BY p.product_name

        ORDER BY total_quantity DESC

        LIMIT 3;

    """, (start_date, end_date))

    top_products = cursor.fetchall()

    print("=" * 60)
    print("REPORT SUMMARY")
    print("=" * 60)

    print(f"Report Type      : {report_type}")
    print(f"Date Range       : {start_date} to {end_date}")
    print(f"Total Orders     : {total_orders}")
    print(f"Revenue          : ₹{revenue}")
    print(f"Unique Customers : {unique_customers}")

    print("\nTop 3 Products")

    for product in top_products:

        print(
            f"{product[0]}  ->  {product[1]}"
        )

    conn.close()


if __name__ == "__main__":

    generate_report()