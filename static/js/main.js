document.addEventListener('DOMContentLoaded', () => {
    // Função auxiliar para pegar elementos do DOM
    const getElement = (id, required = true) => {
        const el = document.getElementById(id);
        if (!el && required) {
            console.error(`Elemento essencial #${id} não foi encontrado. Verifique o index.html.`);
            throw new Error(`Elemento essencial #${id} não encontrado.`);
        }
        return el;
    };

    // --- Seleção de Elementos ---
    const elements = {
        logoUploadInput: getElement('logo-upload'),
        logoSizeSlider: getElement('logo-size'),
        companyNameInput: getElement('company-name'),
        companyPhoneInput: getElement('company-phone'),
        companyEmailInput: getElement('company-email'),
        fileUploadInput: getElement('fileUpload'),
        generateSheetBtn: getElement('generate-sheet-btn'),
        generateFinalBtn: getElement('generate-final-btn'),
        generateWarning: getElement('generate-warning'),
        logoSizeValue: getElement('logo-size-value', false), // Este não é essencial
        fileUploadName: getElement('file-upload-name', false), // Nem este
        previewLogo: getElement('preview-logo'),
        previewLogoContainer: getElement('preview-logo-container'),
        previewCompanyName: getElement('preview-company-name'),
        previewCompanyPhone: getElement('preview-company-phone'),
        previewCompanyEmail: getElement('preview-company-email'),
        qrCodeContainer: getElement('preview-qr-code')
    };
    
    let uploadedSheetFile = null;
    let uploadedLogoFile = null;

    const qrCode = new QRCode(elements.qrCodeContainer, {
        text: 'https://seusite.com', width: 144, height: 144, correctLevel: QRCode.CorrectLevel.H
    });

    const updatePreviewText = (input, preview, defaultText) => {
        preview.textContent = input.value.trim() || defaultText;
    };
    
    // --- Event Listeners ---
    elements.logoUploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            uploadedLogoFile = file;
            const reader = new FileReader();
            reader.onload = (e) => { elements.previewLogo.src = e.target.result; };
            reader.readAsDataURL(file);
        }
    });

    elements.logoSizeSlider.addEventListener('input', (event) => {
        const size = event.target.value;
        elements.previewLogoContainer.style.height = `${size}px`;
        if (elements.logoSizeValue) elements.logoSizeValue.textContent = size;
    });
    
    elements.companyNameInput.addEventListener('input', () => updatePreviewText(elements.companyNameInput, elements.previewCompanyName, 'Nome da Empresa'));
    elements.companyPhoneInput.addEventListener('input', () => updatePreviewText(elements.companyPhoneInput, elements.previewCompanyPhone, 'Telefone'));
    elements.companyEmailInput.addEventListener('input', () => updatePreviewText(elements.companyEmailInput, elements.previewCompanyEmail, 'E-mail'));
    
    elements.generateSheetBtn.addEventListener('click', () => { window.location.href = '/download-template'; });
    
    elements.fileUploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (elements.fileUploadName) {
            elements.fileUploadName.textContent = file ? file.name : "Nenhum ficheiro selecionado";
        }
        if (file) {
            uploadedSheetFile = file;
            elements.generateFinalBtn.disabled = false;
            elements.generateWarning.style.display = 'none';
        } else {
            uploadedSheetFile = null;
            elements.generateFinalBtn.disabled = true;
            elements.generateWarning.style.display = 'block';
        }
    });

    elements.generateFinalBtn.addEventListener('click', async () => {
        if (!uploadedSheetFile) return alert("Por favor, faça o upload de uma planilha.");

        const originalBtnText = elements.generateFinalBtn.textContent;
        elements.generateFinalBtn.textContent = 'Gerando...';
        elements.generateFinalBtn.disabled = true;

        const formData = new FormData();
        formData.append('sheet', uploadedSheetFile);
        if (uploadedLogoFile) formData.append('logo', uploadedLogoFile);
        
        formData.append('company_name', elements.companyNameInput.value);
        formData.append('company_phone', elements.companyPhoneInput.value);
        formData.append('company_email', elements.companyEmailInput.value);
        formData.append('logo_height', elements.previewLogoContainer.style.height);

        const layoutStyle = document.querySelector('input[name="layout-option"]:checked').value;
        const outputMode = document.querySelector('input[name="output-mode"]:checked').value;
        formData.append('layout_style', layoutStyle);
        formData.append('output_mode', outputMode);

        try {
            const response = await fetch('/generate', { method: 'POST', body: formData });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro do servidor: ${response.status}`);
            }

            const downloadFilename = outputMode === 'multiple' ? 'etiquetas.zip' : 'etiquetas.pdf';
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = downloadFilename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

        } catch (error) {
            alert(`Falha na geração do arquivo: ${error.message}`);
        } finally {
            elements.generateFinalBtn.textContent = originalBtnText;
            if(uploadedSheetFile) {
                elements.generateFinalBtn.disabled = false;
            }
        }
    });
});