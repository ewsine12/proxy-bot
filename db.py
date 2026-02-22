import sqlite3

conn = sqlite3.connect("proxybot.db", check_same_thread=False)
c = conn.cursor()

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    telegram_id INTEGER PRIMARY KEY,
    subuser_id TEXT,
    package_key TEXT,
    gb_allocated REAL,
    gb_used REAL
)
""")

# Countries table
c.execute("""
CREATE TABLE IF NOT EXISTS countries(
    telegram_id INTEGER PRIMARY KEY,
    country_code TEXT,
    country_name TEXT
)
""")

conn.commit()
