from db import c, conn

def is_admin(user_id, ADMIN_ID):
    return user_id == ADMIN_ID

def add_user(telegram_id, subuser_id, package_key, gb_allocated):
    c.execute("INSERT OR REPLACE INTO users VALUES (?,?,?,?,?)",
              (telegram_id, subuser_id, package_key, gb_allocated, 0))
    conn.commit()

def update_gb(telegram_id, gb_used):
    c.execute("UPDATE users SET gb_used=? WHERE telegram_id=?", (gb_used, telegram_id))
    conn.commit()

def set_country(telegram_id, code, name):
    c.execute("INSERT OR REPLACE INTO countries VALUES (?,?,?)",
              (telegram_id, code, name))
    conn.commit()

def get_gb(telegram_id):
    c.execute("SELECT gb_allocated, gb_used FROM users WHERE telegram_id=?", (telegram_id,))
    return c.fetchone()
