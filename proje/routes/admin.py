from flask import Blueprint, current_app, jsonify, request, session

from database import get_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def is_admin():
    user_id = session.get("user_id")

    if user_id is None:
        return False

    connection = get_connection(current_app.config["DATABASE_PATH"])

    try:
        user = connection.execute(
            "SELECT role FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        return user is not None and user["role"] == "admin"
    finally:
        connection.close()


@admin_bp.before_request
def require_admin():
    if session.get("user_id") is None:
        return jsonify({"error": "Authentication required"}), 401

    if not is_admin():
        return jsonify({"error": "Admin access required"}), 403


@admin_bp.get("/desks")
def get_all_desks():
    connection = get_connection(current_app.config["DATABASE_PATH"])

    try:
        rows = connection.execute("""
            SELECT
                d.id,
                d.desk_code,
                d.floor,
                d.is_active,
                ds.user_id AS occupied_by,
                ds.selected_at,
                ds.break_expires_at
            FROM desks AS d
            LEFT JOIN desk_sessions AS ds
                ON ds.desk_id = d.id
                AND ds.released_at IS NULL
            ORDER BY d.floor, d.desk_code
        """).fetchall()

        return jsonify({
            "desks": [dict(row) for row in rows]
        }), 200
    finally:
        connection.close()


@admin_bp.post("/desks")
def create_desk():
    data = request.get_json(silent=True) or {}

    desk_code = data.get("desk_code")
    floor = data.get("floor")

    if not isinstance(desk_code, str) or not desk_code.strip():
        return jsonify({"error": "desk_code is required"}), 400

    if floor is not None and not isinstance(floor, str):
        return jsonify({"error": "floor must be a string"}), 400

    connection = get_connection(current_app.config["DATABASE_PATH"])

    try:
        cursor = connection.execute(
            """
            INSERT INTO desks (desk_code, floor)
            VALUES (?, ?)
            """,
            (desk_code.strip(), floor.strip() if floor else None)
        )
        connection.commit()

        return jsonify({
            "message": "Desk created",
            "desk_id": cursor.lastrowid
        }), 201

    except Exception as error:
        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            return jsonify({"error": "Desk code already exists"}), 409

        raise
    finally:
        connection.close()


@admin_bp.patch("/desks/<int:desk_id>")
def update_desk(desk_id):
    data = request.get_json(silent=True) or {}

    allowed_fields = {"desk_code", "floor", "is_active"}
    if not data or not set(data.keys()).issubset(allowed_fields):
        return jsonify({"error": "Invalid update fields"}), 400

    updates = {}

    if "desk_code" in data:
        value = data["desk_code"]
        if not isinstance(value, str) or not value.strip():
            return jsonify({"error": "Invalid desk_code"}), 400
        updates["desk_code"] = value.strip()

    if "floor" in data:
        value = data["floor"]
        if value is not None and not isinstance(value, str):
            return jsonify({"error": "Invalid floor"}), 400
        updates["floor"] = value.strip() if value else None

    if "is_active" in data:
        value = data["is_active"]
        if value not in (0, 1, True, False):
            return jsonify({"error": "is_active must be 0 or 1"}), 400
        updates["is_active"] = int(value)

    connection = get_connection(current_app.config["DATABASE_PATH"])

    try:
        desk = connection.execute(
            "SELECT id FROM desks WHERE id = ?",
            (desk_id,)
        ).fetchone()

        if desk is None:
            return jsonify({"error": "Desk not found"}), 404

        fields = ", ".join(f"{field} = ?" for field in updates)
        values = list(updates.values()) + [desk_id]

        connection.execute(
            f"UPDATE desks SET {fields} WHERE id = ?",
            values
        )
        connection.commit()

        return jsonify({"message": "Desk updated"}), 200

    except Exception as error:
        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            return jsonify({"error": "Desk code already exists"}), 409

        raise
    finally:
        connection.close()
