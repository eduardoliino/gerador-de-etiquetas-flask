import pandas as pd
import qrcode
import base64
import zipfile
import re
from io import BytesIO
from weasyprint import HTML, CSS
from pathlib import Path


def create_single_label_html(item_data, template_data):
    """Cria o HTML para uma única etiqueta."""
    nome_equipamento = item_data.get('nome', 'N/A')
    identificador = item_data.get('identificador', 'N/A')
    link_qr_code = item_data.get('link qr code', '')

    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(link_qr_code or 'about:blank')
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    buffered_qr = BytesIO()
    qr_img.save(buffered_qr, format="PNG")
    qr_base64 = base64.b64encode(buffered_qr.getvalue()).decode('utf-8')

    def sanitize(text):
        return str(text).replace('<', '<').replace('>', '>')

    return f'''
      <div class="page-container">
        <div class="etiqueta">
            <div class="logo-container">
                <img src="{template_data['logo_base64']}" style="height: {sanitize(template_data.get('logo_height', '80px'))};" alt="Logo">
            </div>
            <div class="company-info">
                <p class="info-text company-name">{sanitize(template_data.get('company_name', ''))}</p>
                <p class="info-text">{sanitize(template_data.get('company_phone', ''))}</p>
                <p class="info-text">{sanitize(template_data.get('company_email', ''))}</p>
            </div>
            <div class="qr-code"><img src="data:image/png;base64,{qr_base64}" alt="QR Code"></div>
            <div class="bottom-container">
                <div>
                    <p class="equipment-label">Nome do equipamento</p>
                    <p class="equipment-value">{sanitize(nome_equipamento)}</p>
                </div>
                <div>
                    <p class="equipment-label">Identificador</p>
                    <p class="equipment-value">{sanitize(identificador)}</p>
                </div>
            </div>
        </div>
      </div>
    '''


def generate_zip_file(html_pages_data, css_doc):
    """Cria um arquivo ZIP com um PDF para cada etiqueta."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, (page_html, item_id) in enumerate(html_pages_data):
            safe_filename = re.sub(
                r'[^a-zA-Z0-9_.-]', '_', item_id or 'etiqueta')
            pdf_bytes = HTML(
                string=f"<html><body>{page_html}</body></html>").write_pdf(stylesheets=[css_doc])
            zip_file.writestr(f"{safe_filename}_{i+1}.pdf", pdf_bytes)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()



def generate_labels_from_data(form_data, files, static_path_base):
    """Função principal que orquestra a geração de etiquetas."""
    sheet_file = files.get('sheet')
    if not sheet_file:
        raise ValueError("Nenhum arquivo de planilha foi enviado.")

    try:
        df = pd.read_excel(sheet_file, engine='openpyxl') if sheet_file.filename.endswith(
            '.xlsx') else pd.read_csv(sheet_file)
        df.columns = [str(col).strip().lower() for col in df.columns]
    except Exception as e:
        raise ValueError(
            f"Não foi possível ler a planilha. Verifique o formato. Erro: {e}")

    required_columns = ['nome', 'identificador', 'link qr code']
    missing_columns = [
        col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"As seguintes colunas obrigatórias não foram encontradas: {', '.join(missing_columns)}")

    df.fillna('', inplace=True)
    spreadsheet_data = df.to_dict(orient='records')

    logo_base64 = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
    if 'logo' in files and files['logo'].filename:
        logo_file = files['logo']
        logo_bytes = logo_file.read()
        logo_base64 = f"data:{logo_file.mimetype};base64,{base64.b64encode(logo_bytes).decode('utf-8')}"

    template_data = {
        "company_name": form_data.get('company_name'),
        "company_phone": form_data.get('company_phone'),
        "company_email": form_data.get('company_email'),
        "logo_base64": logo_base64,
        "logo_height": form_data.get('logo_height', '80px'),
    }

    
    layout_choice = form_data.get('layout_style', 'card')
    css_path = Path(static_path_base) / 'css' / f"{layout_choice}_layout.css"

    if not css_path.is_file():
       
        error_message = f"Arquivo de estilo não encontrado! O sistema buscou por '{css_path}'. Verifique se o arquivo existe e se a estrutura de pastas está correta (a pasta 'static' deve estar no mesmo nível do seu 'app.py')."
        raise FileNotFoundError(error_message)
    css_doc = CSS(filename=str(css_path))

    html_pages = [(create_single_label_html(item, template_data),
                   item.get('identificador')) for item in spreadsheet_data]

    output_mode = form_data.get('output_mode', 'single')
    if output_mode == 'multiple':
        file_bytes = generate_zip_file(html_pages, css_doc)
        mimetype = 'application/zip'
        filename = 'etiquetas.zip'
    else:
        full_html = "".join([page[0] for page in html_pages])
        file_bytes = HTML(
            string=f"<html><body>{full_html}</body></html>").write_pdf(stylesheets=[css_doc])
        mimetype = 'application/pdf'
        filename = 'etiquetas.pdf'

    return file_bytes, mimetype, filename
