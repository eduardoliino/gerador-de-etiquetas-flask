# services/pdf_service.py
import pandas as pd
import qrcode
import base64
from io import BytesIO
from weasyprint import HTML, CSS


def create_single_label_html(item_data, template_data):
    nome_equipamento = item_data.get('nome', 'N/A')
    identificador = item_data.get('identificador', 'N/A')
    link_qr_code = item_data.get('link qr code', '')

    if not link_qr_code:
        print(
            f"Aviso: 'LINK QR CODE' não encontrado para o item: {nome_equipamento}")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(link_qr_code or 'https://auvo.com.br')
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    buffered_qr = BytesIO()
    qr_img.save(buffered_qr, format="PNG")
    qr_base64 = base64.b64encode(buffered_qr.getvalue()).decode('utf-8')

    return f"""
        <div class="etiqueta">
            <div class="logo-container">
                <img class="logo" src="{template_data.get('logo_base64', '')}" style="width: {template_data.get('logo_height', '80px')}; height: {template_data.get('logo_height', '80px')};" alt="Logo">

            </div>
            
            <div class="main-content">
                <div class="company-info">
                    <p class="info-text company-name">{template_data.get('company_name', '')}</p>
                    <p class="info-text">{template_data.get('company_phone', '')}</p>
                    <p class="info-text">{template_data.get('company_email', '')}</p>
                </div>

                <div class="qr-code">
                    <img src="data:image/png;base64,{qr_base64}" alt="QR Code">
                </div>
            </div>
            
            <div class="bottom-container">
                <div>
                     <p class="equipment-label">Nome do equipamento</p>
                     <p class="equipment-value">{nome_equipamento}</p>
                </div>
                <div>
                     <p class="equipment-label">Identificador</p>
                     <p class="equipment-value">{identificador}</p>
                </div>
            </div>
        </div>
    """


def generate_pdf(form_data, files):
    sheet_file = files.get('sheet')
    if not sheet_file:
        raise ValueError("Arquivo de planilha não encontrado.")

    try:
        df = pd.read_excel(sheet_file) if sheet_file.filename.endswith(
            ('.xls', '.xlsx')) else pd.read_csv(sheet_file)
        df.columns = [str(col).strip().lower() for col in df.columns]
        spreadsheet_data = df.to_dict(orient='records')
    except Exception as e:
        raise ValueError(f"Erro ao ler a planilha: {e}")

    logo_base64 = ""
    if 'logo' in files:
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

    page_template = '<div class="page">{}</div>'
    all_pages_html = "".join([
        page_template.format(create_single_label_html(item, template_data))
        for item in spreadsheet_data
    ])

    combined_css_string = """
        @page {
            size: A4;
            margin: 0;
        }
        body { 
            font-family: 'Inter', sans-serif; 
            margin: 0;
        }
        .page {
            width: 210mm;
            height: 297mm;
            page-break-after: always;
            border: 3mm solid #d1d5db;
            box-sizing: border-box;
        }
        .etiqueta {
            width: 100%;
            height: 100%;
            background-color: white;
            padding: 2cm;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
        }
        .logo-container {
            width: 100%;
            min-height: 100px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .logo {
            object-fit: cover;
            border-radius: 6px;
        }
        .main-content {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .company-info {
            margin-bottom: 1cm;
            text-align: center;
        }
        .info-text {
            font-size: 18pt;
            line-height: 1.5;
        }
        .company-name {
            font-weight: 600;
            font-size: 20pt;
        }
        .qr-code {
            width: 80mm;
            height: 80mm;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .qr-code > img {
            width: 100%;
            height: 100%;
        }
        .bottom-container {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 12px;
            text-align: center;
        }
        .equipment-label {
            font-size: 16pt;
            color: #4b5563;
        }
        .equipment-value {
            font-weight: 700;
            font-size: 26pt;
            margin-top: 4px;
            word-break: break-word;
        }
    """

    html_doc = HTML(string=f"<html><body>{all_pages_html}</body></html>")
    css_doc = CSS(string=combined_css_string)
    return html_doc.write_pdf(stylesheets=[css_doc])
