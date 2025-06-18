# services/pdf_service.py
import pandas as pd
import qrcode
import base64
from io import BytesIO
from weasyprint import HTML, CSS

# --- HTML e CSS TEMPLATES ---
# Este CSS será aplicado a cada etiqueta individualmente.
LABEL_CSS = """
    body { margin: 0; font-family: 'Inter', sans-serif; }
    .etiqueta {
        width: 70mm;
        height: 112mm; /* Proporção 1:1.6 */
        border: 1px solid #d1d5db;
        background-color: white;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        box-sizing: border-box; /* Garante que padding não aumente o tamanho */
    }
    .logo-container {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 12px;
    }
    .logo {
        max-width: 100%;
        object-fit: contain;
    }
    .info-text { font-size: 14.4px; line-height: 1.4; color: #1f2937; }
    .qr-code { margin: 20px 0; }
    .equipment-label { font-size: 12.8px; color: #4b5563; }
    .equipment-value { font-weight: 700; font-size: 18px; color: #111827; margin-top: 2px; word-break: break-all; }
    .company-name { font-weight: 600; }
    .bottom-container { margin-top: auto; display: flex; flex-direction: column; gap: 8px; }
"""


def create_single_label_html(item_data, template_data):
    """Cria o HTML para uma única etiqueta."""

    # Gera o QR Code para o link da linha atual
    qr_img = qrcode.make(item_data.get('LINK QR CODE', ''))
    buffered_qr = BytesIO()
    qr_img.save(buffered_qr, format="PNG")
    qr_base64 = base64.b64encode(buffered_qr.getvalue()).decode('utf-8')

    return f"""
        <div class="etiqueta">
            <div class="logo-container" style="height: {template_data.get('logo_height', '50px')};">
                <img class="logo" src="{template_data.get('logo_base64', '')}" style="max-height: {template_data.get('logo_height', '50px')};">
            </div>
            
            <div style="margin: 10px 0;">
                <p class="info-text company-name">{template_data.get('company_name', '')}</p>
                <p class="info-text">{template_data.get('company_phone', '')}</p>
                <p class="info-text">{template_data.get('company_email', '')}</p>
            </div>

            <div class="qr-code">
                <img src="data:image/png;base64,{qr_base64}">
            </div>
            
            <div class="bottom-container">
                <div>
                     <p class="equipment-label">Nome do equipamento</p>
                     <p class="equipment-value">{item_data.get('Nome do equipamento', 'N/A')}</p>
                </div>
                <div>
                     <p class="equipment-label">Identificador</p>
                     <p class="equipment-value">{item_data.get('Identificador', 'N/A')}</p>
                </div>
            </div>
        </div>
    """


def generate_pdf(form_data, files):
    """Função principal que orquestra a criação do PDF."""

    # 1. Ler a planilha
    sheet_file = files.get('sheet')
    if not sheet_file:
        raise ValueError("Arquivo de planilha não encontrado.")

    try:
        df = pd.read_excel(sheet_file) if sheet_file.filename.endswith(
            ('.xls', '.xlsx')) else pd.read_csv(sheet_file)
        spreadsheet_data = df.to_dict(orient='records')
    except Exception as e:
        raise ValueError(f"Erro ao ler a planilha: {e}")

    # 2. Preparar dados do template
    logo_base64 = ""
    if 'logo' in files:
        logo_file = files['logo']
        logo_bytes = logo_file.read()
        logo_base64 = f"data:{logo_file.mimetype};base64,{base64.b64encode(logo_bytes).decode('utf-8')}"

    template_data = {
        "company_name": form_data.get('company_name'),
        "company_phone": form_data.get('company_phone'),
        "company_email": form_data.get('company_email'),
        "logo_height": form_data.get('logo_height', '50px'),
        "logo_base64": logo_base64,
        "layout_mode": form_data.get('layout_mode', 'grid')
    }

    # 3. Gerar HTML de todas as etiquetas
    all_labels_html = "".join([create_single_label_html(
        item, template_data) for item in spreadsheet_data])

    # 4. Definir CSS da página com base no modo de layout
    layout_mode = template_data['layout_mode']
    page_css = ""
    if layout_mode == 'grid':
        page_css = """
            @page { size: A4; margin: 1cm; }
            body { 
                display: grid; 
                grid-template-columns: repeat(3, 1fr); 
                gap: 5mm;
                align-content: start;
            }
            .etiqueta { border: 1px dashed #ccc; width: 63.5mm; height: 93mm; padding: 10px;}
        """
    elif layout_mode == 'single':
        page_css = """
            @page { size: 70mm 112mm; margin: 0; }
            .etiqueta { border: none; }
        """
    elif layout_mode == 'fullpage':
        page_css = """
            @page { size: A4; margin: 0; }
            .etiqueta { width: 210mm; height: 297mm; border: none; padding: 2cm; }
        """

    # 5. Combinar CSS e gerar o PDF
    final_css = CSS(string=LABEL_CSS + page_css)
    html_doc = HTML(string=f"<html><body>{all_labels_html}</body></html>")

    pdf_bytes = html_doc.write_pdf(stylesheets=[final_css])
    return pdf_bytes
