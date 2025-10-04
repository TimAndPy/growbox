"""
Database initialization script for GrowBox IoT Control System.
Creates SQLite database with schema from data-model.md.
"""

import sqlite3
import os
from pathlib import Path


def get_database_path():
    """Get the path to the SQLite database file."""
    # Store database in project root/data directory
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir / "growbox.db"


def create_schema(conn):
    """Create database schema with all required tables."""
    cursor = conn.cursor()

    # Enable WAL mode for better concurrent access
    cursor.execute("PRAGMA journal_mode=WAL")

    # Table 1: sensor_readings (time-series data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            sensor_type TEXT NOT NULL CHECK(sensor_type IN ('temperature', 'humidity', 'light', 'water')),
            value REAL NOT NULL,
            unit TEXT NOT NULL,
            status TEXT DEFAULT 'valid' CHECK(status IN ('valid', 'error', 'stale'))
        )
    """)

    # Indexes for sensor_readings
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sensor_timestamp ON sensor_readings(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sensor_type_timestamp ON sensor_readings(sensor_type, timestamp)")

    # Table 2: device_states (device control event log)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            device_type TEXT NOT NULL CHECK(device_type IN ('lights', 'ventilation', 'pump', 'heater', 'co2')),
            state TEXT NOT NULL CHECK(state IN ('on', 'off', 'auto')),
            command_source TEXT CHECK(command_source IN ('local', 'remote', 'auto', 'failsafe')),
            triggered_by TEXT
        )
    """)

    # Indexes for device_states
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_device_timestamp ON device_states(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_device_type_timestamp ON device_states(device_type, timestamp)")

    # Table 3: growth_cycles (plant growth phase tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS growth_cycles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_date DATE NOT NULL,
            end_date DATE,
            phase TEXT NOT NULL CHECK(phase IN ('vegetative', 'flowering')),
            light_schedule TEXT NOT NULL,
            target_temp_min REAL,
            target_temp_max REAL,
            target_humidity_min REAL,
            target_humidity_max REAL,
            active BOOLEAN DEFAULT 1
        )
    """)

    # Unique constraint: only one active cycle at a time
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_active_cycle ON growth_cycles(active) WHERE active = 1")

    # Table 4: target_parameters (user-configurable environmental targets)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS target_parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parameter_name TEXT UNIQUE NOT NULL,
            min_value REAL,
            max_value REAL,
            warning_threshold REAL,
            unit TEXT NOT NULL
        )
    """)

    # Index for target_parameters
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_parameter_name ON target_parameters(parameter_name)")

    # Table 5: system_status (singleton for system health)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_status (
            id INTEGER PRIMARY KEY CHECK(id = 1),
            connection_state TEXT CHECK(connection_state IN ('online', 'offline')),
            last_mqtt_publish DATETIME,
            last_mqtt_receive DATETIME,
            last_sensor_read DATETIME,
            auto_mode_enabled BOOLEAN DEFAULT 0,
            active_alerts TEXT,
            uptime_seconds INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    print("[OK] Database schema created successfully")


def seed_default_data(conn):
    """Insert default data for initial setup."""
    cursor = conn.cursor()

    # Insert default target parameters
    default_targets = [
        ('temperature', 22.0, 25.0, 2.0, 'celsius'),
        ('humidity', 60.0, 70.0, 5.0, 'percent'),
        ('water_level', 30.0, 100.0, 10.0, 'liters'),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO target_parameters (parameter_name, min_value, max_value, warning_threshold, unit)
        VALUES (?, ?, ?, ?, ?)
    """, default_targets)

    # Insert default system status (singleton)
    cursor.execute("""
        INSERT OR IGNORE INTO system_status (id, connection_state, auto_mode_enabled)
        VALUES (1, 'offline', 0)
    """)

    # Insert default growth cycle (vegetative phase)
    cursor.execute("""
        INSERT OR IGNORE INTO growth_cycles (start_date, phase, light_schedule, target_temp_min, target_temp_max, target_humidity_min, target_humidity_max, active)
        VALUES (DATE('now'), 'vegetative', '18/6', 22.0, 25.0, 60.0, 70.0, 1)
    """)

    conn.commit()
    print("[OK] Default data seeded successfully")


def initialize_database(db_path=None):
    """
    Initialize the GrowBox database.

    Args:
        db_path: Optional custom database path. If None, uses default location.

    Returns:
        Path to the initialized database.
    """
    if db_path is None:
        db_path = get_database_path()

    # Create connection
    conn = sqlite3.connect(db_path)

    try:
        print(f"Initializing database at: {db_path}")
        create_schema(conn)
        seed_default_data(conn)
        print("[OK] Database initialization complete")
        return db_path
    finally:
        conn.close()


if __name__ == "__main__":
    # Run initialization when script is executed directly
    db_path = initialize_database()
    print(f"\nDatabase ready at: {db_path}")
    print("\nYou can connect to it with:")
    print(f"  sqlite3 {db_path}")
