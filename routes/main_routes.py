from flask import Blueprint, render_template, request, jsonify, Response, send_file
from services.pdf_service import generate_pdf
import pandas as pd
import io

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Renderiza a página HTML principal."""
    return render_template('index.html')


# NOVO: Endpoint para gerar e baixar a planilha modelo .xlsx
@main_bp.route('/download-template')
def download_template():
    """Cria e serve um arquivo .xlsx modelo para download."""
    try:
        # Define os cabeçalhos das colunas
        headers = ["Nome", "Identificador", "LINK QR CODE"]
        # Cria um DataFrame do pandas vazio com esses cabeçalhos
        df = pd.DataFrame(columns=headers)

        # Cria um buffer de bytes em memória para salvar o arquivo Excel
        buffer = io.BytesIO()

        # Salva o DataFrame como um arquivo Excel no buffer
        # index=False evita que o pandas salve o índice da linha como uma coluna
        df.to_excel(buffer, index=False)

        # Reposiciona o "cursor" do buffer para o início
        buffer.seek(0)

        # Usa send_file para enviar o buffer como um anexo para download
        return send_file(
            buffer,
            as_attachment=True,
            download_name='modelo_etiquetas.xlsx',  # Nome do arquivo que o usuário verá
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        print(f"ERRO AO GERAR PLANILHA MODELO: {e}")
        return jsonify({"error": "Não foi possível gerar a planilha modelo."}), 500


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
