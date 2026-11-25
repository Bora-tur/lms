from flask import Blueprint, current_app, jsonify, session

from services.gate_service import process_entry, process_exit


gate_bp = Blueprint("gate", __name__, url_prefix="/api/gate")


@gate_bp.post("/entry")
def gate_entry():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Login required"}), 401

    result, status_code = process_entry(
        current_app.config["DATABASE_PATH"],
        user_id,
    )

    return jsonify(result), status_code


@gate_bp.post("/exit")
def gate_exit():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Login required"}), 401

    result, status_code = process_exit(
        current_app.config["DATABASE_PATH"],
        user_id,
    )

    return jsonify(result), status_code
