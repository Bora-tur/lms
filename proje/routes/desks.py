from flask import Blueprint, current_app, jsonify, request, session

desks_bp = Blueprint("desks", __name__, url_prefix="/api/desks")

from services.desk_service import (
    DeskError,
    list_desks,
    select_desk,
    release_user_desk,
    start_break,
    resume_from_break,
)

desks_bp = Blueprint("desks", __name__, url_prefix="/api/desks")


@desks_bp.get("/")
def get_desks():
    desks = list_desks(current_app.config["DATABASE_PATH"])
    return jsonify({"desks": desks})


@desks_bp.post("/<int:desk_id>/select")
def choose_desk(desk_id):
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Önce giriş yapmalısınız."}), 401

    try:
        result = select_desk(
            current_app.config["DATABASE_PATH"],
            user_id,
            desk_id,
        )
        return jsonify(result), 201
    except DeskError as error:
        return jsonify({"error": str(error)}), 409


@desks_bp.post("/release")
def release_desk():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Önce giriş yapmalısınız."}), 401

    released = release_user_desk(
        current_app.config["DATABASE_PATH"],
        user_id,
    )

    if not released:
        return jsonify({"message": "Aktif bir masanız yok."}), 200

    return jsonify({"message": "Masa bırakıldı."}), 200


@desks_bp.post("/break")
def begin_break():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Login required."}), 401

    try:
        result = start_break(
            current_app.config["DATABASE_PATH"],
            user_id,
        )
        return jsonify(result), 200
    except DeskError as error:
        return jsonify({"error": str(error)}), 409


@desks_bp.post("/break/resume")
def return_from_break():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Login required."}), 401

    try:
        result, status_code = resume_from_break(
            current_app.config["DATABASE_PATH"],
            user_id,
        )
        return jsonify(result), status_code
    except DeskError as error:
        return jsonify({"error": str(error)}), 409
