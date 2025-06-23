from flask import Blueprint, render_template, request, jsonify, Response, send_file, current_app
from services.pdf_service import generate_labels_from_data
import pandas as pd
import io

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/download-template')
def download_template():
    """Cria e serve um arquivo .xlsx modelo para download."""
    try:
        df = pd.DataFrame(columns=["nome", "identificador", "link qr code"])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name='modelo_etiquetas.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        print(f"ERRO AO GERAR PLANILHA MODELO: {e}")
        return jsonify({"error": "Não foi possível gerar a planilha modelo."}), 500


@main_bp.route('/generate', methods=['POST'])
def generate_labels_route():
    """
    Recebe os dados do formulário e chama o serviço para gerar o arquivo final.
    """
    try:

        static_folder_path = current_app.static_folder
        file_bytes, mimetype, filename = generate_labels_from_data(
            request.form, request.files, static_folder_path)

        return Response(
            file_bytes,
            mimetype=mimetype,
            headers={'Content-Disposition': f'attachment;filename={filename}'}
        )
    except (ValueError, FileNotFoundError) as ve:

        return jsonify({"error": str(ve)}), 400
    except Exception as e:

        print(f"ERRO INESPERADO NA ROTA /generate: {type(e).__name__}: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor."}), 500
