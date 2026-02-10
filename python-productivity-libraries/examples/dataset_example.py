import dataset
from datetime import datetime, timedelta
import random


def setup_database(db):
    users = db['users']
    products = db['products']
    orders = db['orders']

    users.insert_many([
        {'user_id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'plan': 'pro',
         'created_at': '2025-01-15'},
        {'user_id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'plan': 'free', 'created_at': '2025-03-20'},
        {'user_id': 3, 'name': 'Carol White', 'email': 'carol@example.com', 'plan': 'pro', 'created_at': '2025-06-10'},
        {'user_id': 4, 'name': 'David Lee', 'email': 'david@example.com', 'plan': 'enterprise',
         'created_at': '2024-11-01'},
    ])

    products.insert_many([
        {'product_id': 'P001', 'name': 'Laptop Pro', 'price': 1299.99, 'category': 'Electronics'},
        {'product_id': 'P002', 'name': 'Wireless Mouse', 'price': 49.99, 'category': 'Accessories'},
        {'product_id': 'P003', 'name': 'USB-C Hub', 'price': 79.99, 'category': 'Accessories'},
        {'product_id': 'P004', 'name': 'Monitor 27"', 'price': 449.99, 'category': 'Electronics'},
    ])

    base_date = datetime(2026, 1, 1)
    product_ids = ['P001', 'P002', 'P003', 'P004']
    prices = [1299.99, 49.99, 79.99, 449.99]

    orders_data = []
    for i in range(1, 21):
        pid_idx = (i - 1) % 4
        pid = product_ids[pid_idx]
        price = prices[pid_idx]
        uid = ((i - 1) % 4) + 1
        orders_data.append({
            'order_id': f'ORD-{i:04d}',
            'user_id': uid,
            'product_id': pid,
            'amount': price,
            'status': random.choice(['completed', 'pending', 'refunded']),
            'created_at': (base_date + timedelta(days=i)).strftime('%Y-%m-%d'),
        })

    orders.insert_many(orders_data)
    print(f"Inserted {users.count()} users, {products.count()} products, {orders.count()} orders")


def run_etl_queries(db):
    print("\n--- Query 1: All Pro/Enterprise Users ---")
    for user in db['users'].find(plan=['pro', 'enterprise']):
        print(f"  {user['name']:<20} ({user['plan']})")

    print("\n--- Query 2: Completed Orders ---")
    completed = list(db['orders'].find(status='completed'))
    total_revenue = sum(o['amount'] for o in completed)
    print(f"  Completed orders : {len(completed)}")
    print(f"  Total revenue    : ${total_revenue:,.2f}")

    print("\n--- Query 3: Raw SQL for Aggregation ---")
    result = db.query("""
        SELECT u.name, COUNT(o.order_id) AS order_count, SUM(o.amount) AS total_spent
        FROM orders o
        JOIN users u ON o.user_id = u.user_id
        WHERE o.status = 'completed'
        GROUP BY u.user_id
        ORDER BY total_spent DESC
    """)
    for row in result:
        print(f"  {row['name']:<20} | Orders: {row['order_count']} | Spent: ${row['total_spent']:,.2f}")

    print("\n--- Query 4: Products Needing Restock (mock threshold) ---")
    for product in db['products'].find():
        mock_stock = random.randint(0, 50)
        if mock_stock < 10:
            print(f"  ⚠️  {product['name']:<25} — Only {mock_stock} left!")


def upsert_demo(db):
    print("\n--- Upsert Demo ---")
    users = db['users']

    users.upsert(
        {'user_id': 5, 'name': 'Eve Martinez', 'email': 'eve@example.com', 'plan': 'free'},
        keys=['user_id']
    )
    print(f"  After upsert (new)    : {users.count()} users")

    users.upsert(
        {'user_id': 5, 'name': 'Eve Martinez', 'email': 'eve@example.com', 'plan': 'pro'},
        keys=['user_id']
    )
    eve = users.find_one(user_id=5)
    print(f"  After upsert (update) : Eve's plan → {eve['plan']}")


def main():
    print("=" * 60)
    print("Dataset: Rapid ETL Prototyping")
    print("=" * 60)

    db = dataset.connect('sqlite:///:memory:')

    setup_database(db)
    run_etl_queries(db)
    upsert_demo(db)

    print("\n⚠️  PRODUCTION NOTE:")
    print("  Dataset is ideal for prototyping and ETL scripts.")
    print("  Migrate to SQLAlchemy when schema stabilises.")
    print("  Dataset does NOT handle migrations.")


if __name__ == '__main__':
    main()
