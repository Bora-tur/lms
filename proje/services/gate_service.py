from database import get_connection


def process_entry(database_path, user_id):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")

        active_visit = connection.execute(
            """
            SELECT id
            FROM visits
            WHERE user_id = ? AND exit_time IS NULL
            """,
            (user_id,),
        ).fetchone()

        if active_visit is not None:
            reason = "User is already inside"

            connection.execute(
                """
                INSERT INTO gate_events (user_id, event_type, result, reason)
                VALUES (?, 'entry', 'rejected', ?)
                """,
                (user_id, reason),
            )

            connection.commit()
            return {"success": False, "message": reason}, 409

        cursor = connection.execute(
            "INSERT INTO visits (user_id) VALUES (?)",
            (user_id,),
        )

        connection.execute(
            """
            INSERT INTO gate_events (user_id, event_type, result, reason)
            VALUES (?, 'entry', 'accepted', 'Entry successful')
            """,
            (user_id,),
        )

        connection.commit()

        return {
            "success": True,
            "message": "Entry successful",
            "visit_id": cursor.lastrowid,
        }, 200

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def process_exit(database_path, user_id):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")

        active_visit = connection.execute(
            """
            SELECT id
            FROM visits
            WHERE user_id = ? AND exit_time IS NULL
            ORDER BY entry_time DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

        visit_closed = False

        if active_visit is not None:
            connection.execute(
                """
                UPDATE visits
                SET exit_time = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (active_visit["id"],),
            )
            visit_closed = True

        desk_cursor = connection.execute(
            """
            UPDATE desk_sessions
            SET released_at = CURRENT_TIMESTAMP,
                break_started_at = NULL,
                break_expires_at = NULL
            WHERE user_id = ?
                AND released_at IS NULL
                AND break_expires_at IS NULL
            """,
            (user_id,),
        )

        connection.execute(
            """
            INSERT INTO gate_events (user_id, event_type, result, reason)
            VALUES (?, 'exit', 'accepted', 'Exit successful')
            """,
            (user_id,),
        )

        connection.commit()

        return {
            "success": True,
            "message": "Exit successful",
            "desk_released": desk_cursor.rowcount > 0,
            "visit_closed": visit_closed,
        }, 200

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
