from flask import Flask, render_template
import time
import os


def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)

    app.secret_key = os.urandom(24)

    from routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_timestamp():
        return {'timestamp': int(time.time())}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
