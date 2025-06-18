# routes/main_routes.py
from flask import Blueprint, render_template, request, jsonify, Response
from services.pdf_service import generate_pdf

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Renderiza a página HTML principal."""
    return render_template('index.html')


@main_bp.route('/generate', methods=['POST'])
def generate_labels():
    """
    Endpoint para receber os dados do formulário e da planilha,
    e retornar o PDF gerado.
    """
    try:
        # Passa os dados do formulário e os arquivos para o serviço de geração
        pdf_bytes = generate_pdf(request.form, request.files)

        # Retorna o PDF como uma resposta de download
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment;filename=etiquetas.pdf'}
        )

    except ValueError as ve:
        # Erro de validação (ex: planilha faltando)
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # Outros erros de servidor
        print(f"ERRO INESPERADO: {e}")  # Log do erro no console do servidor
        return jsonify({"error": "Ocorreu um erro interno ao gerar o PDF."}), 500
