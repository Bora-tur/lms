from config import Config
from database import get_connection, init_db


def seed_desks():
    database_path = Config.DATABASE_PATH
    init_db(database_path)

    desks = [
        ("A-01", "1"),
        ("A-02", "1"),
        ("A-03", "1"),
        ("B-01", "2"),
        ("B-02", "2"),
        ("B-03", "2"),
    ]

    connection = get_connection(database_path)

    try:
        connection.executemany(
            """
            INSERT OR IGNORE INTO desks (desk_code, floor)
            VALUES (?, ?)
        """,
            desks,
        )

        connection.commit()
        print("Örnek masalar hazır.")
    finally:
        connection.close()


if __name__ == "__main__":
    seed_desks()
