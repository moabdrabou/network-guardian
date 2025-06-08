import sqlite3
import os
from config import DATABASE_NAME, LOG_DIR, SCAN_LOG_FILE

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def setup_database():
    """Creates the necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table for storing known (authorized) devices
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS known_devices (
            mac_address TEXT PRIMARY KEY,
            ip_address TEXT,
            hostname TEXT,
            description TEXT DEFAULT 'Unknown',
            first_seen TEXT,
            last_seen TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database '{DATABASE_NAME}' initialized.")

def add_known_device(mac, ip, hostname, description):
    """Adds a device to the known_devices table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute('''
            INSERT OR REPLACE INTO known_devices (mac_address, ip_address, hostname, description, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (mac, ip, hostname, description, now, now))
        conn.commit()
        print(f"Added/Updated known device: {mac} ({hostname})")
    except sqlite3.Error as e:
        print(f"Database error adding known device: {e}")
    finally:
        conn.close()

def get_known_devices():
    """Retrieves all known devices from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT mac_address FROM known_devices')
    known_macs = {row['mac_address'] for row in cursor.fetchall()}
    conn.close()
    return known_macs

def log_scan_event(message):
    """Logs scan events to a text file."""
    os.makedirs(LOG_DIR, exist_ok=True)
    from datetime import datetime
    with open(SCAN_LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")