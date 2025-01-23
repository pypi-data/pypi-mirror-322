from flask import send_file

from .blueprints.user.routes import user_bp


def register_routes(app):
    """Initialize blueprints and routes"""

    @app.route("/manifest.json")
    def serve_manifest():
        return send_file("static/manifest.json", mimetype="application/json")

    @app.route("/service-worker.js")
    def serve_sw():
        return send_file("static/service-worker.js", mimetype="application/javascript")

    app.register_blueprint(user_bp)
