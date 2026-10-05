import sqlite3
from pathlib import Path
from flask import g
from werkzeug.security import generate_password_hash

DATABASE = 'expense_tracker.db'

def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # Enable foreign key constraints
        g.db.execute('PRAGMA foreign_keys = ON')
    return g.db

def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS"""
    db = get_db()

    # Create users table
    db.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    # Create expenses table
    db.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    # Create indexes for better query performance
    db.execute("CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)")

    db.commit()

def seed_db():
    """Inserts sample data for development"""
    db = get_db()

    # Check if we already have users to avoid duplicate seeding
    cursor = db.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]

    if user_count > 0:
        return  # Prevent duplicate seeding

    # Hash the password using werkzeug
    hashed_password = generate_password_hash('demo123')

    # Insert exactly one demo user
    db.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', hashed_password)
    )
    user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

    # Insert exactly 8 sample expenses for the demo user
    sample_expenses = [
        # Food category
        (user_id, 1250.50, 'Food', 'Groceries and dining out', '2026-10-05'),
        # Transport category
        (user_id, 45.00, 'Transport', 'Metro card recharge', '2026-10-06'),
        # Bills category
        (user_id, 2500.00, 'Bills', 'Electricity bill', '2026-10-01'),
        # Health category
        (user_id, 150.00, 'Health', 'Pharmacy and vitamins', '2026-10-04'),
        # Entertainment category
        (user_id, 89.99, 'Entertainment', 'Movie tickets', '2026-10-03'),
        # Shopping category (first item)
        (user_id, 1200.00, 'Shopping', 'Winter jacket', '2026-10-02'),
        # Shopping category (second item - to make 8 total)
        (user_id, 2200.00, 'Shopping', 'Winter boots', '2026-10-07'),
        # Other category
        (user_id, 500.00, 'Other', None, '2026-10-08')  # NULL description
    ]

    db.executemany(
        'INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
        sample_expenses
    )

    db.commit()
    print("Database seeded with sample data")