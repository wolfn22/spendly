import sqlite3
from pathlib import Path
from flask import g

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
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create expenses table
    db.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Create indexes for better query performance
    db.execute('''
        CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)
    ''')

    db.execute('''
        CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date)
    ''')

    db.commit()

def seed_db():
    """Inserts sample data for development"""
    db = get_db()

    # Check if we already have users to avoid duplicate seeding
    cursor = db.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        # Insert sample users
        sample_users = [
            ('Nitish Kumar', 'nitish@example.com', 'hashed_password_1'),
            ('Priya Sharma', 'priya@example.com', 'hashed_password_2'),
            ('Arjun Singh', 'arjun@example.com', 'hashed_password_3')
        ]

        db.executemany(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            sample_users
        )

        # Get the user IDs for seeding expenses
        user_ids = [row[0] for row in db.execute('SELECT id FROM users').fetchall()]

        # Insert sample expenses
        sample_expenses = [
            # Nitish's expenses
            (user_ids[0], 1250.50, 'Food & Dining', 'Lunch at restaurant', '2026-10-01'),
            (user_ids[0], 45.00, 'Transport', 'Metro card recharge', '2026-10-02'),
            (user_ids[0], 1200.00, 'Shopping', 'New shoes', '2026-10-03'),
            (user_ids[0], 89.99, 'Entertainment', 'Movie tickets', '2026-10-04'),

            # Priya's expenses
            (user_ids[1], 2500.00, 'Utilities', 'Electricity bill', '2026-10-01'),
            (user_ids[1], 320.00, 'Food & Dining', 'Groceries', '2026-10-02'),
            (user_ids[1], 150.00, 'Health', 'Pharmacy', '2026-10-03'),

            # Arjun's expenses
            (user_ids[2], 1800.00, 'Food & Dining', 'Monthly groceries', '2026-10-01'),
            (user_ids[2], 500.00, 'Transport', 'Fuel', '2026-10-02'),
            (user_ids[2], 2200.00, 'Shopping', 'Winter jacket', '2026-10-03'),
        ]

        db.executemany(
            'INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)',
            sample_expenses
        )

        db.commit()
        print("Database seeded with sample data")
    else:
        print("Database already contains data, skipping seed")