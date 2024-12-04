import sqlite3
from flask import current_app, g

def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def get_db():
    """Open a new database connection."""
    if 'sqlite_db' not in g:
        db_filename = current_app.config['DATABASE_FILENAME']
        print(f"Using database: {db_filename}")  # Debugging line to check db filename
        g.sqlite_db = sqlite3.connect(str(db_filename))
        g.sqlite_db.row_factory = dict_factory
    return g.sqlite_db

def close_db(error=None):
    """Close the database at the end of a request."""
    db = g.pop('sqlite_db', None)
    if db is not None:
        db.commit()
        db.close()

def init_db():
    """Create the database tables if they don't exist."""
    db = get_db()
    # Ensure the 'documents' table is created if it doesn't exist
    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                docid INTEGER PRIMARY KEY,
                title VARCHAR(150),
                summary VARCHAR(250),
                url VARCHAR(150)
            )
        """)
        db.commit()
        print("Documents table created successfully (if it didn't exist).")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
