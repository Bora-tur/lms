import sqlite3

from flask import Blueprint, current_app, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_connection

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    password_hash = generate_password_hash(password)
    connection = get_connection(current_app.config["DATABASE_PATH"])

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (username, email, password_hash),
        )
        connection.commit()

        return jsonify({"message": "User registered", "user_id": cursor.lastrowid}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists"}), 409

    finally:
        connection.close()


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400

    connection = get_connection(current_app.config["DATABASE_PATH"])

    try:
        user = connection.execute(
            """
            SELECT id, username, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()
    finally:
        connection.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    session.clear()
    session["user_id"] = user["id"]

    return jsonify(
        {
            "message": "Login successful",
            "user": {"id": user["id"], "username": user["username"]},
        }
    )


@auth_bp.post("/logout")
def logout():
    session.clear()

    return jsonify({"message": "Logged out"})


@auth_bp.get("/me")
def me():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Authentication required"}), 401

    connection = get_connection(current_app.config["DATABASE_PATH"])

    try:
        user = connection.execute(
            "SELECT id, username, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    finally:
        connection.close()

    if user is None:
        session.clear()
        return jsonify({"error": "User not found"}), 401

    return jsonify(
        {
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
            }
        }
    )
