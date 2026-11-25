from database import get_connection


class DeskError(Exception):
    """Masa islemleri sirasinda olusan beklenen hatalar."""


def expire_breaks(connection):
    """10 dakikasi dolan molalari sonlandir."""
    connection.execute("""
        UPDATE desk_sessions
        SET released_at = CURRENT_TIMESTAMP,
            break_started_at = NULL,
            break_expires_at = NULL
        WHERE released_at IS NULL
          AND break_expires_at IS NOT NULL
          AND break_expires_at <= CURRENT_TIMESTAMP
    """)


def list_desks(database_path):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")
        expire_breaks(connection)

        rows = connection.execute("""
            SELECT
                d.id,
                d.desk_code,
                d.floor,
                d.is_active,
                CASE
                    WHEN ds.id IS NULL THEN 0
                    ELSE 1
                END AS is_occupied,
                ds.user_id AS occupied_by,
                u.username AS occupied_by_username,
                CASE
                    WHEN d.is_active = 0 THEN 'inactive'
                    WHEN ds.id IS NULL THEN 'available'
                    WHEN ds.break_expires_at IS NOT NULL
                        THEN 'on_break'
                    ELSE 'occupied'
                END AS status,
                ds.break_expires_at
            FROM desks AS d
            LEFT JOIN desk_sessions AS ds
                ON ds.desk_id = d.id
                AND ds.released_at IS NULL
            LEFT JOIN users AS u
                ON u.id = ds.user_id
            ORDER BY d.floor, d.desk_code
        """).fetchall()

        connection.commit()
        return [dict(row) for row in rows]

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def select_desk(database_path, user_id, desk_id):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")
        expire_breaks(connection)

        desk = connection.execute(
            """
            SELECT id, is_active
            FROM desks
            WHERE id = ?
        """,
            (desk_id,),
        ).fetchone()

        if desk is None or desk["is_active"] != 1:
            raise DeskError("Masa bulunamadi veya kullanima kapali.")

        existing = connection.execute(
            """
            SELECT id
            FROM desk_sessions
            WHERE user_id = ? AND released_at IS NULL
        """,
            (user_id,),
        ).fetchone()

        if existing is not None:
            raise DeskError("Zaten aktif bir masaniz var.")

        occupied = connection.execute(
            """
            SELECT id
            FROM desk_sessions
            WHERE desk_id = ? AND released_at IS NULL
        """,
            (desk_id,),
        ).fetchone()

        if occupied is not None:
            raise DeskError("Bu masa baska bir kullanici tarafindan secilmis.")

        connection.execute(
            """
            INSERT INTO desk_sessions (desk_id, user_id)
            VALUES (?, ?)
        """,
            (desk_id, user_id),
        )

        connection.commit()
        return {"message": "Masa basariyla secildi."}

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def release_user_desk(database_path, user_id):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")

        cursor = connection.execute(
            """
            UPDATE desk_sessions
            SET released_at = CURRENT_TIMESTAMP,
                break_started_at = NULL,
                break_expires_at = NULL
            WHERE user_id = ?
              AND released_at IS NULL
        """,
            (user_id,),
        )

        connection.commit()
        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def start_break(database_path, user_id):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")
        expire_breaks(connection)

        cursor = connection.execute(
            """
            UPDATE desk_sessions
            SET break_started_at = CURRENT_TIMESTAMP,
                break_expires_at = datetime(
                    CURRENT_TIMESTAMP, '+10 minutes'
                )
            WHERE user_id = ?
              AND released_at IS NULL
              AND break_expires_at IS NULL
        """,
            (user_id,),
        )

        if cursor.rowcount == 0:
            raise DeskError("Aktif masaniz yok veya zaten moladasiniz.")

        connection.commit()
        return {"message": "Mola basladi.", "duration_minutes": 10}

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def resume_from_break(database_path, user_id):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")
        expire_breaks(connection)

        cursor = connection.execute(
            """
            UPDATE desk_sessions
            SET break_started_at = NULL,
                break_expires_at = NULL
            WHERE user_id = ?
              AND released_at IS NULL
              AND break_expires_at IS NOT NULL
        """,
            (user_id,),
        )

        if cursor.rowcount == 0:
            connection.commit()
            return {"message": ("Aktif molaniz yok veya mola suresi dolmus.")}, 409

        connection.commit()
        return {"message": "Masaniza geri dondunuz."}, 200

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
