# Implementation Plan: Database Setup for Spendly Application

## Context
This implementation plan outlines the work needed to bring the database layer in line with the specifications in `specs/01-database-setup.md`. The current implementation in `database/db.py` is a basic stub that does not meet the requirements for the Spendly expense tracker application. This plan details the specific changes required to implement a working SQLite database with proper schema, functions, and initialization.

## Summary of Required Changes
Two files need to be modified:
1. `database/db.py` - Update all three functions to match specifications exactly
2. `app.py` - Add database initialization on application startup

## Detailed Implementation Plan

### 1. database/db.py Updates

#### get_db() Function
- **Status**: Already compliant with specifications
- **No changes needed**: Correctly opens connection to `expense_tracker.db`, sets `row_factory = sqlite3.Row`, enables `PRAGMA foreign_keys = ON`, and returns connection

#### init_db() Function
Update to match exact schema from specs:

**Users Table:**
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT DEFAULT datetime('now')
)
```

**Expenses Table:**
```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    created_at TEXT DEFAULT datetime('now'),
    FOREIGN KEY (user_id) REFERENCES users (id)
)
```

**Changes from current implementation:**
- Column name: `password` → `password_hash` in users table
- Timestamp format: `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` → `TEXT DEFAULT datetime('now')` for both tables' created_at columns
- Date column: `DATE NOT NULL` → `TEXT NOT NULL` (to enforce YYYY-MM-DD format)
- Foreign key: Remove `ON DELETE CASCADE` (not specified in specs)
- Keep performance indexes on `expenses(user_id)` and `expenses(date)` as harmless optimization

#### seed_db() Function
Complete reimplementation to match specifications:

**Steps:**
1. Check if users table already contains data:
   ```python
   cursor = db.execute('SELECT COUNT(*) FROM users')
   if cursor.fetchone()[0] > 0:
       return  # Prevent duplicate seeding
   ```

2. Import and use proper password hashing:
   ```python
   from werkzeug.security import generate_password_hash
   hashed_password = generate_password_hash('demo123')
   ```

3. Insert exactly one demo user:
   ```python
   db.execute(
       'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
       ('Demo User', 'demo@spendly.com', hashed_password)
   )
   user_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
   ```

4. Insert exactly 8 sample expenses with these specifics:
   - All linked to the demo user (user_id from above)
   - Use ONLY these categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
   - Ensure at least one expense per category (7 categories × 1 expense = 7, plus 1 additional expense in any category = 8 total)
   - Spread dates across current month in YYYY-MM-DD format
   - Mix of expenses with and without descriptions
   - Use parameterized queries only

   **Example expense data:**
   ```
   (user_id, 1250.50, 'Food', 'Groceries and dining', '2026-10-05')
   (user_id, 45.00, 'Transport', 'Metro recharge', '2026-10-06')
   (user_id, 2500.00, 'Bills', 'Electricity bill', '2026-10-01')
   (user_id, 150.00, 'Health', 'Pharmacy', '2026-10-04')
   (user_id, 89.99, 'Entertainment', 'Movie tickets', '2026-10-03')
   (user_id, 1200.00, 'Shopping', 'Winter jacket', '2026-10-02')
   (user_id, 2200.00, 'Shopping', 'Winter boots', '2026-10-07')  # Second shopping expense
   (user_id, 500.00, 'Other', 'Birthday gift', NULL, '2026-10-08')
   ```

5. Commit transaction after both inserts

### 2. app.py Updates

**Add imports** (after Flask import):
```python
from database.db import get_db, init_db, seed_db
```

**Modify main execution block** to initialize database on startup:
```python
if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
```

## Verification Criteria
After implementation, verify:
1. Database file `expense_tracker.db` created on app startup
2. Tables match exact schema from specs (verified via SQLite `.schema` command)
3. Demo user exists with correctly hashed password (not plaintext "demo123")
4. Exactly 8 sample expenses exist with proper categorization and dating
5. No duplicate data on repeated app startups (seed data only inserted once)
6. Foreign key constraints enforced (invalid user_id inserts fail)
7. Unique email constraint works (duplicate email inserts fail)
8. Date format consistently YYYY-MM-DD in expenses table
9. Application starts without errors

## Dependencies
- No new pip packages required
- Uses existing dependencies:
  - sqlite3 (Python standard library)
  - werkzeug.security (already installed via requirements.txt)

## Implementation Sequence
1. Update `database/db.py` with corrected schema and function implementations
2. Update `app.py` with database imports and initialization calls
3. Test by running the application and verifying all verification criteria