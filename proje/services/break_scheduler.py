import logging
import threading
import time

from database import get_connection


logger = logging.getLogger(__name__)


def cleanup_expired_breaks(database_path):
    connection = get_connection(database_path)

    try:
        connection.execute("BEGIN IMMEDIATE")

        cursor = connection.execute(
            """
            UPDATE desk_sessions
            SET released_at = CURRENT_TIMESTAMP,
                break_started_at = NULL,
                break_expires_at = NULL
            WHERE released_at IS NULL
              AND break_expires_at IS NOT NULL
              AND break_expires_at <= CURRENT_TIMESTAMP
            """
        )

        connection.commit()
        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def start_break_scheduler(database_path):
    def worker():
        while True:
            try:
                released_count = cleanup_expired_breaks(database_path)

                if released_count:
                    logger.info(
                        "Automatically released %s expired desk session(s)",
                        released_count,
                    )

            except Exception:
                logger.exception("Break cleanup failed")

            time.sleep(5)

    thread = threading.Thread(
        target=worker,
        name="break-cleanup",
        daemon=True,
    )
    thread.start()
    return thread
