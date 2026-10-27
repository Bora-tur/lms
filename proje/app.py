from flask import Flask, jsonify

from config import Config
from database import init_db
from routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the local database.
    init_db(app.config["DATABASE_PATH"])
    app.register_blueprint(auth_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "lms-local"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
