import sqlite3

DB_PATH = "database/ecommerce.db"


def test_invalid_order_id(conn):

    print("=" * 60)
    print("TEST 1 : Invalid Order ID")
    print("=" * 60)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM orders
        WHERE order_id='ORD999999';
    """)

    result = cursor.fetchall()

    if len(result) == 0:
        print("PASS : Invalid order_id handled correctly.\n")
    else:
        print("FAIL\n")


def test_invalid_discount(conn):

    print("=" * 60)
    print("TEST 2 : Discount > 100")
    print("=" * 60)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
        WHERE discount > 100;
    """)

    count = cursor.fetchone()[0]

    if count == 0:
        print("PASS : No discount greater than 100.\n")
    else:
        print("FAIL\n")


def test_zero_quantity(conn):

    print("=" * 60)
    print("TEST 3 : Quantity = 0")
    print("=" * 60)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items
        WHERE quantity <= 0;
    """)

    count = cursor.fetchone()[0]

    if count == 0:
        print("PASS : No zero or negative quantity found.\n")
    else:
        print("FAIL\n")


def test_future_orders(conn):

    print("=" * 60)
    print("TEST 4 : Future Order Dates")
    print("=" * 60)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE order_date > DATE('now');
    """)

    count = cursor.fetchone()[0]

    if count == 0:
        print("PASS : No future order dates.\n")
    else:
        print("FAIL\n")


def main():

    conn = sqlite3.connect(DB_PATH)

    print("\n")
    print("=" * 60)
    print("EDGE CASE TESTING")
    print("=" * 60)

    test_invalid_order_id(conn)
    test_invalid_discount(conn)
    test_zero_quantity(conn)
    test_future_orders(conn)

    conn.close()

    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()