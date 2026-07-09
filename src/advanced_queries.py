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
    # Query 7
    # Running Revenue by Category
    # -------------------------------------------------

    query7 = """
    SELECT

        p.category,

        o.order_date,

        ROUND(
            SUM(oi.line_total),
            2
        ) AS daily_revenue,

        ROUND(
            SUM(
                SUM(oi.line_total)
            ) OVER(
                PARTITION BY p.category
                ORDER BY o.order_date
            ),
            2
        ) AS running_total

    FROM order_items oi

    JOIN orders o
        ON oi.order_id = o.order_id

    JOIN products p
        ON oi.product_id = p.product_id

    GROUP BY
        p.category,
        o.order_date;
    """

    run_query(
        conn,
        query7,
        "07_running_total.csv",
        "Running Revenue"
    )

    # -------------------------------------------------
    # Query 8
    # DENSE_RANK
    # -------------------------------------------------

    query8 = """
    SELECT

        p.category,

        p.product_name,

        ROUND(
            SUM(oi.line_total),
            2
        ) AS revenue,

        DENSE_RANK() OVER(

            PARTITION BY p.category

            ORDER BY
            SUM(oi.line_total) DESC

        ) AS rank_in_category

    FROM order_items oi

    JOIN products p

        ON oi.product_id=p.product_id

    GROUP BY

        p.category,
        p.product_name;
    """

    run_query(
        conn,
        query8,
        "08_dense_rank.csv",
        "Dense Rank"
    )

    # -------------------------------------------------
    # Query 9
    # LAG
    # -------------------------------------------------

    query9 = """
    SELECT

        customer_id,

        order_date,

        LAG(order_date)
        OVER(

            PARTITION BY customer_id

            ORDER BY order_date

        ) AS previous_order

    FROM orders;
    """

    run_query(
        conn,
        query9,
        "09_lag.csv",
        "LAG Analysis"
    )

    # -------------------------------------------------
    # Query 10
    # Monthly Revenue CTE
    # -------------------------------------------------

    query10 = """
    WITH monthly_revenue AS (

        SELECT

            customer_id,

            strftime('%Y-%m',order_date) AS month,

            SUM(total_amount) AS revenue

        FROM orders

        GROUP BY

            customer_id,
            month

    )

    SELECT *

    FROM monthly_revenue

    ORDER BY

        month,
        revenue DESC;
    """

    run_query(
        conn,
        query10,
        "10_cte.csv",
        "CTE Monthly Revenue"
    )

        # -------------------------------------------------
    # Query 11
    # NTILE Customer Segmentation
    # -------------------------------------------------

    query11 = """
    WITH customer_value AS (

        SELECT

            customer_id,

            SUM(total_amount) AS total_value

        FROM orders

        GROUP BY customer_id

    )

    SELECT

        customer_id,

        ROUND(total_value,2) AS total_value,

        NTILE(4) OVER(
            ORDER BY total_value DESC
        ) AS quartile

    FROM customer_value;
    """

    run_query(
        conn,
        query11,
        "11_ntile_segmentation.csv",
        "Customer Segmentation"
    )

    # -------------------------------------------------
    # Query 12
    # Year over Year Revenue
    # -------------------------------------------------

    query12 = """
    WITH yearly AS(

        SELECT

            strftime('%Y',order_date) AS year,

            strftime('%m',order_date) AS month,

            SUM(total_amount) AS revenue

        FROM orders

        GROUP BY year,month

    )

    SELECT

        year,

        month,

        ROUND(revenue,2) AS revenue,

        ROUND(

            LAG(revenue)
            OVER(

                PARTITION BY month

                ORDER BY year

            ),

            2

        ) AS prev_year_revenue

    FROM yearly;
    """

    run_query(
        conn,
        query12,
        "12_yoy.csv",
        "Year over Year Revenue"
    )

    # -------------------------------------------------
    # Query 13
    # First and Last Purchase
    # -------------------------------------------------

    query13 = """
    SELECT

        customer_id,

        MIN(order_date) AS first_purchase,

        MAX(order_date) AS latest_purchase

    FROM orders

    GROUP BY customer_id;
    """

    run_query(
        conn,
        query13,
        "13_first_last_purchase.csv",
        "First & Last Purchase"
    )

    # -------------------------------------------------
    # Query 14
    # Cumulative Revenue
    # -------------------------------------------------

    query14 = """
    SELECT

        customer_id,

        ROUND(total_amount,2) AS revenue,

        ROUND(

            SUM(total_amount)
            OVER(

                ORDER BY total_amount DESC

            ),

            2

        ) AS cumulative_revenue

    FROM orders

    ORDER BY total_amount DESC;
    """

    run_query(
        conn,
        query14,
        "14_cumulative_distribution.csv",
        "Cumulative Revenue"
    )

    # -------------------------------------------------
    # Query 15
    # Cohort Analysis
    # -------------------------------------------------

    query15 = """
    SELECT

        strftime('%Y-%m',registration_date) AS cohort,

        COUNT(*) AS customers

    FROM customers

    GROUP BY cohort

    ORDER BY cohort;
    """

    run_query(
        conn,
        query15,
        "15_cohort.csv",
        "Customer Cohorts"
    )

    # -------------------------------------------------
    # Query 16
    # Frequently Bought Together
    # -------------------------------------------------

    query16 = """
    SELECT

        oi1.product_id AS product_a,

        oi2.product_id AS product_b,

        COUNT(*) AS times_bought_together

    FROM order_items oi1

    JOIN order_items oi2

        ON oi1.order_id = oi2.order_id

    WHERE oi1.product_id < oi2.product_id

    GROUP BY

        oi1.product_id,

        oi2.product_id

    ORDER BY

        times_bought_together DESC

    LIMIT 20;
    """

    run_query(
        conn,
        query16,
        "16_bought_together.csv",
        "Frequently Bought Together"
    )

    conn.close()


if __name__ == "__main__":
    main()