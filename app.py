# app.py (Atualizado com cache-busting)
from flask import Flask, render_template
import time  # Importa a biblioteca de tempo


def create_app():
    """Cria e configura uma instância da aplicação Flask."""
    app = Flask(__name__)

    from routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    # Esta função injeta variáveis em todos os templates
    @app.context_processor
    def inject_timestamp():
        # Gera um 'timestamp' (número único baseado na hora atual)
        # para forçar o navegador a recarregar ficheiros estáticos.
        return {'timestamp': int(time.time())}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
