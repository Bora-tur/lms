import sys

from config import Config
from database import get_connection


if len(sys.argv) != 2:
    print("Usage: python make_admin.py USERNAME")
    raise SystemExit(1)

username = sys.argv[1]

connection = get_connection(Config.DATABASE_PATH)

try:
    cursor = connection.execute(
        """
        UPDATE users
        SET role = 'admin'
        WHERE username = ?
        """,
        (username,)
    )

    if cursor.rowcount == 0:
        print("User not found.")
        raise SystemExit(1)

    connection.commit()
    print(f"Admin role assigned to {username}.")

except Exception:
    connection.rollback()
    raise

finally:
    connection.close()
