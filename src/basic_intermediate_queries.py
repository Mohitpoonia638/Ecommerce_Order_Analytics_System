import os
import sqlite3
import pandas as pd

DB_PATH = "database/ecommerce.db"


def run_query(conn, query, output_file, title):

    print("=" * 60)
    print(title)
    print("=" * 60)

    df = pd.read_sql_query(query, conn)

    os.makedirs("reports", exist_ok=True)

    df.to_csv(
        f"reports/{output_file}",
        index=False
    )

    print(df.head(10))
    print()
    print(f"Saved : reports/{output_file}")
    print()


def main():

    conn = sqlite3.connect(DB_PATH)

    # -------------------------------------------------
    # Query 1
    # Total Revenue Per Category
    # -------------------------------------------------

    query1 = """
    SELECT
        p.category,
        ROUND(
            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount/100.0)
            ),
            2
        ) AS total_revenue

    FROM order_items oi

    JOIN products p
    ON oi.product_id = p.product_id

    GROUP BY p.category

    ORDER BY total_revenue DESC;
    """

    run_query(
        conn,
        query1,
        "01_revenue_by_category.csv",
        "Revenue By Category"
    )

    # -------------------------------------------------
    # Query 2
    # Top 10 Customers
    # -------------------------------------------------

    query2 = """
    SELECT

        c.customer_id,

        c.customer_name,

        ROUND(
            SUM(o.total_amount),
            2
        ) AS total_spent

    FROM customers c

    JOIN orders o

    ON c.customer_id = o.customer_id

    GROUP BY

        c.customer_id,
        c.customer_name

    ORDER BY total_spent DESC

    LIMIT 10;
    """

    run_query(
        conn,
        query2,
        "02_top_customers.csv",
        "Top 10 Customers"
    )

    # -------------------------------------------------
    # Query 3
    # Monthly Order Count
    # -------------------------------------------------

    query3 = """
    SELECT

        strftime('%Y-%m', order_date) AS month,

        COUNT(*) AS total_orders

    FROM orders

    GROUP BY month

    ORDER BY month DESC

    LIMIT 12;
    """

    run_query(
        conn,
        query3,
        "03_monthly_orders.csv",
        "Monthly Orders"
    )

        # -------------------------------------------------
    # Query 4
    # Customers who placed orders but never had any delivered order
    # -------------------------------------------------

    query4 = """
    SELECT DISTINCT
        c.customer_id,
        c.customer_name
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    HAVING SUM(
        CASE
            WHEN o.order_status='Delivered' THEN 1
            ELSE 0
        END
    ) = 0;
    """

    run_query(
        conn,
        query4,
        "04_customers_no_delivery.csv",
        "Customers With No Delivered Orders"
    )

    # -------------------------------------------------
    # Query 5
    # Products with more returns than purchases
    # -------------------------------------------------

    query5 = """
    SELECT
        p.product_name,

        SUM(
            CASE
                WHEN o.order_status='Returned'
                THEN oi.quantity
                ELSE 0
            END
        ) AS returned,

        SUM(
            CASE
                WHEN o.order_status='Delivered'
                THEN oi.quantity
                ELSE 0
            END
        ) AS delivered

    FROM order_items oi

    JOIN orders o
        ON oi.order_id=o.order_id

    JOIN products p
        ON oi.product_id=p.product_id

    GROUP BY p.product_id,p.product_name

    HAVING returned > delivered

    ORDER BY returned DESC;
    """

    run_query(
        conn,
        query5,
        "05_more_returns_than_sales.csv",
        "Products With More Returns Than Deliveries"
    )

    # -------------------------------------------------
    # Query 6
    # Return rate by category
    # -------------------------------------------------

    query6 = """
    SELECT

        p.category,

        ROUND(
            100.0 *
            SUM(
                CASE
                    WHEN o.order_status='Returned'
                    THEN oi.quantity
                    ELSE 0
                END
            ) /

            SUM(oi.quantity),

            2

        ) AS return_rate

    FROM order_items oi

    JOIN orders o
        ON oi.order_id=o.order_id

    JOIN products p
        ON oi.product_id=p.product_id

    GROUP BY p.category

    ORDER BY return_rate DESC;
    """

    run_query(
        conn,
        query6,
        "06_return_rate_by_category.csv",
        "Return Rate By Category"
    )

    conn.close()


if __name__ == "__main__":
    main()