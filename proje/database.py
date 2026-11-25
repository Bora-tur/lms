import sqlite3
from pathlib import Path


def get_connection(database_path):
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db(database_path):

    connection = get_connection(database_path)

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student'
                    CHECK (role IN ('student', 'admin')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS qr_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT,
                revoked_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                exit_time TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS gate_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_type TEXT NOT NULL
                    CHECK (event_type IN ('entry', 'exit')),
                result TEXT NOT NULL
                    CHECK (result IN ('accepted', 'rejected')),
                reason TEXT,
                occurred_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS desks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                desk_code TEXT NOT NULL UNIQUE,
                floor TEXT,
                is_active INTEGER NOT NULL DEFAULT 1
                    CHECK (is_active IN (0, 1)),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS desk_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                desk_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                selected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                released_at TEXT,
                break_started_at TEXT,
                break_expires_at TEXT,
                FOREIGN KEY (desk_id) REFERENCES desks(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_visits_user_id
                ON visits(user_id);

            CREATE INDEX IF NOT EXISTS idx_visits_exit_time
                ON visits(exit_time);

            CREATE INDEX IF NOT EXISTS idx_gate_events_occurred_at
                ON gate_events(occurred_at);

            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_one_active_desk_per_user
                ON desk_sessions(user_id)
                WHERE released_at IS NULL;

            CREATE UNIQUE INDEX IF NOT EXISTS
                idx_one_active_user_per_desk
                ON desk_sessions(desk_id)
                WHERE released_at IS NULL;
        """)
        migrate_users(connection)
        migrate_desk_sessions(connection)
        connection.commit()
    finally:
        connection.close()


def migrate_desk_sessions(connection):
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(desk_sessions)").fetchall()
    }

    if "break_started_at" not in columns:
        connection.execute("ALTER TABLE desk_sessions ADD COLUMN break_started_at TEXT")

    if "break_expires_at" not in columns:
        connection.execute("ALTER TABLE desk_sessions ADD COLUMN break_expires_at TEXT")



def migrate_users(connection):
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }

    if "role" not in columns:
        connection.execute(
            """
            ALTER TABLE users
            ADD COLUMN role TEXT NOT NULL DEFAULT 'student'
            CHECK (role IN ('student', 'admin'))
            """
        )
