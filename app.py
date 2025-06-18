# app.py
# Ponto de entrada da aplicação Flask.

from flask import Flask


def create_app():
    """
    Cria e configura uma instância da aplicação Flask (App Factory Pattern).
    """
    # Cria a instância da aplicação
    app = Flask(__name__)

    # Importa o blueprint de rotas
    from routes.main_routes import main_bp

    # Registra o blueprint na aplicação. Todas as rotas definidas em main_bp
    # agora estarão ativas na aplicação.
    app.register_blueprint(main_bp)

    return app


# Bloco de execução principal
if __name__ == '__main__':
    # Cria a aplicação usando a factory
    app = create_app()
    # Executa o servidor em modo de depuração
    app.run(debug=True, host='0.0.0.0', port=5000)
