# services/pdf_service.py
import pandas as pd
import qrcode
import base64
from io import BytesIO
from weasyprint import HTML, CSS

# --- CSS DEFINITIONS ---

# Folha de estilo para o layout de "Etiqueta Centralizada"
CSS_CARD_LAYOUT = """
    @page { size: A4; margin: 0; }
    body { font-family: 'Inter', sans-serif; margin: 0; }
    .page-container {
        width: 210mm; height: 297mm;
        page-break-after: always;
        display: flex; justify-content: center; align-items: center;
    }
    .etiqueta {
        width: 74mm; min-height: 118mm;
        background-color: white;
        border: 1px solid #d1d5db;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        padding: 10mm;
        box-sizing: border-box;
        display: flex; flex-direction: column; align-items: center; text-align: center;
    }
    /* ... (resto do css do card) */
    .logo-container { margin-bottom: 5mm; }
    .logo-container img { max-width: 100%; max-height: 100%; object-fit: contain; }
    .company-info { margin: 2mm 0; }
    .info-text { font-size: 9pt; line-height: 1.4; color: #1f2937; }
    .company-name { font-weight: 700; }
    .qr-code { margin: 5mm 0; width: 40mm; height: 40mm; }
    .qr-code img { width: 100%; height: 100%; }
    .bottom-container { margin-top: auto; width: 100%; display: flex; flex-direction: column; gap: 4mm; }
    .equipment-label { font-size: 8pt; color: #4b5563; }
    .equipment-value { font-weight: 700; font-size: 11pt; color: #111827; margin-top: 1mm; word-break: break-all; }
"""

# Folha de estilo para o layout de "Página Inteira"
CSS_FULLPAGE_LAYOUT = """
    @page { size: A4; margin: 0; }
    body { font-family: 'Inter', sans-serif; margin: 0; }
    .page-container {
        width: 210mm; height: 297mm;
        page-break-after: always;
        /* Adicionado para manter a borda dentro da página */
        padding: 5mm; 
        box-sizing: border-box;
    }
    .etiqueta {
        width: 100%; height: 100%;
        padding: 20mm; /* Ajustado por causa do padding da página */
        box-sizing: border-box;
        display: flex; flex-direction: column; align-items: center; text-align: center;
        
        /* ALTERADO: Borda adicionada */
        border: 1px solid #d1d5db;
    }
    .logo-container { margin-bottom: 10mm; }
    .logo-container img { max-width: 80%; object-fit: contain; }
    .company-info { margin-bottom: 10mm; }
    .info-text { font-size: 14pt; line-height: 1.5; color: #1f2937; }
    .company-name { font-weight: 600; font-size: 16pt; }
    .qr-code { margin: 10mm 0; width: 70mm; height: 70mm; }
    .qr-code img { width: 100%; height: 100%; }
    .bottom-container { margin-top: auto; width: 100%; display: flex; flex-direction: column; gap: 8mm; }
    .equipment-label { font-size: 14pt; color: #4b5563; }
    .equipment-value { font-weight: 700; font-size: 24pt; color: #111827; margin-top: 1mm; word-break: break-all; }
"""


def create_single_label_html(item_data, template_data):
    nome_equipamento = item_data.get('nome', 'N/A')
    identificador = item_data.get('identificador', 'N/A')
    link_qr_code = item_data.get('link qr code', '')

    qr = qrcode.QRCode(
        version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(link_qr_code or 'https://auvo.com.br')
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    buffered_qr = BytesIO()
    qr_img.save(buffered_qr, format="PNG")
    qr_base64 = base64.b64encode(buffered_qr.getvalue()).decode('utf-8')

    # O HTML agora é universal para ambos os layouts. O CSS fará a diferenciação.
    return f"""
      <div class="page-container">
        <div class="etiqueta">
            <div class="logo-container">
                <img src="{template_data.get('logo_base64', '')}"
                     style="height: {template_data.get('logo_height', '80px')};"
                     alt="Logo">
            </div>
            <div class="company-info">
                <p class="info-text company-name">{template_data.get('company_name', '')}</p>
                <p class="info-text">{template_data.get('company_phone', '')}</p>
                <p class="info-text">{template_data.get('company_email', '')}</p>
            </div>
            <div class="qr-code">
                <img src="data:image/png;base64,{qr_base64}" alt="QR Code">
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

    all_pages_html = "".join([create_single_label_html(
        item, template_data) for item in spreadsheet_data])

    # Lógica para escolher a folha de estilo correta
    # Padrão para 'card' por segurança
    layout_choice = form_data.get('layout_style', 'card')

    if layout_choice == 'fullpage':
        final_css_string = CSS_FULLPAGE_LAYOUT
    else:
        final_css_string = CSS_CARD_LAYOUT

    html_doc = HTML(string=f"<html><body>{all_pages_html}</body></html>")
    css_doc = CSS(string=final_css_string)

    return html_doc.write_pdf(stylesheets=[css_doc])
