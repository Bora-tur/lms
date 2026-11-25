from flask import Flask, jsonify, render_template

from config import Config
from database import init_db
from routes.auth import auth_bp
from routes.desks import desks_bp
from routes.admin import admin_bp
from routes.gate import gate_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app.config["DATABASE_PATH"])

    app.register_blueprint(auth_bp)
    app.register_blueprint(desks_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(gate_bp)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({
            "status": "ok",
            "service": "lms-local",
        })

    return app


app = create_app()


if __name__ == "__main__":
    from services.break_scheduler import start_break_scheduler

    start_break_scheduler(app.config["DATABASE_PATH"])

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False,
    )
