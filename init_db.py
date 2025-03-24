import sqlite3

def create_database():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    cursor = conn.cursor()

    # Create 'users' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        user_type TEXT NOT NULL CHECK(user_type IN ('admin', 'user'))
    )
    """)

    # Create 'firs' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        file_path TEXT,
        status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Reviewed', 'Resolved')),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    create_database()
