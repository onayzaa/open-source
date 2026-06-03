import sqlite3

DB_NAME = "app.db"  # single place to change the database name


def create_database():
    """Create the database and users table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL,
            age  INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database ready.")


def add_user(name: str, age: int):
    """Insert a new user into the database."""
    if not name.strip():
        print("Error: name cannot be empty.")
        return
    if age < 0:
        print("Error: age cannot be negative.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (name, age)
    )

    conn.commit()
    print(f"User '{name}' added with ID {cursor.lastrowid}.")
    conn.close()


def get_all_users() -> list[dict]:
    """Return all users as a list of dicts."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row          # lets us access columns by name
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return rows


def get_user_by_id(user_id: int) -> dict | None:
    """Return a single user by ID, or None if not found."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    conn.close()
    return dict(row) if row else None


def update_user(user_id: int, name: str = None, age: int = None):
    """Update a user's name and/or age by ID."""
    if name is None and age is None:
        print("Nothing to update.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if name and age is not None:
        cursor.execute(
            "UPDATE users SET name = ?, age = ? WHERE id = ?",
            (name, age, user_id)
        )
    elif name:
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    else:
        cursor.execute("UPDATE users SET age  = ? WHERE id = ?", (age,  user_id))

    if cursor.rowcount == 0:
        print(f"No user found with ID {user_id}.")
    else:
        print(f"User {user_id} updated.")

    conn.commit()
    conn.close()


def delete_user(user_id: int):
    """Delete a user by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

    if cursor.rowcount == 0:
        print(f"No user found with ID {user_id}.")
    else:
        print(f"User {user_id} deleted.")

    conn.commit()
    conn.close()


# ── quick demo ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    create_database()

    add_user("Ali",   23)
    add_user("Sara",  30)
    add_user("Ahmed", 25)

    print("\nAll users:", get_all_users())

    update_user(1, name="Ali Raza", age=24)
    print("\nUpdated user 1:", get_user_by_id(1))

    delete_user(2)
    print("\nAfter deleting user 2:", get_all_users())













