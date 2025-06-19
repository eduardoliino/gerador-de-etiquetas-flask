document.addEventListener('DOMContentLoaded', () => {
    // --- VERIFICAÇÃO INICIAL DE ELEMENTOS ---
    const getElement = (id) => {
        const el = document.getElementById(id);
        if (!el) {
            const errorMessage = `Erro Crítico: O elemento com o ID '#${id}' não foi encontrado no seu ficheiro 'index.html'. Verifique se o ID está correto.`;
            console.error(errorMessage);
            alert(errorMessage);
            throw new Error(errorMessage);
        }
        return el;
    };

    let elements;
    try {
        elements = {
            logoUpload: getElement('logo-upload'),
            logoSizeSlider: getElement('logo-size'),
            companyNameInput: getElement('company-name'),
            companyPhoneInput: getElement('company-phone'),
            companyEmailInput: getElement('company-email'),
            generateSheetBtn: getElement('generate-sheet-btn'),
            fileUploadInput: getElement('fileUpload'),
            generateFinalBtn: getElement('generate-final-btn'),
            generateWarning: getElement('generate-warning'),
            previewLogo: getElement('preview-logo'),
            previewLogoContainer: getElement('preview-logo-container'),
            previewCompanyName: getElement('preview-company-name'),
            previewCompanyPhone: getElement('preview-company-phone'),
            previewCompanyEmail: getElement('preview-company-email'),
            previewEquipmentName: getElement('preview-equipment-name'),
            previewEquipmentId: getElement('preview-equipment-id'),
            qrCodeContainer: getElement('preview-qr-code')
        };
    } catch (error) {
        return; // Para a execução se um elemento não for encontrado.
    }
    
    // --- ESTADO DA APLICAÇÃO ---
    let uploadedSheetFile = null;
    let uploadedLogoFile = null;

    // --- QR CODE DE PRÉ-VISUALIZAÇÃO ---
    new QRCode(elements.qrCodeContainer, {
        text: 'PREVIEW_QR_CODE', width: 140, height: 140, correctLevel: QRCode.CorrectLevel.H
    });

    // --- EVENT LISTENERS ---

    elements.logoUpload.addEventListener('change', (event) => {
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
    elements.previewLogo.style.width = `${size}px`;
    elements.previewLogo.style.height = `${size}px`;
    elements.previewLogo.style.objectFit = 'cover';
    elements.previewLogo.style.borderRadius = '8px';
    
    });
    
    const updatePreviewText = (input, preview, defaultText) => {
        preview.textContent = input.value || defaultText;
    };

    elements.companyNameInput.addEventListener('input', () => updatePreviewText(elements.companyNameInput, elements.previewCompanyName, 'Nome da Empresa'));
    elements.companyPhoneInput.addEventListener('input', () => updatePreviewText(elements.companyPhoneInput, elements.previewCompanyPhone, 'Telefone'));
    elements.companyEmailInput.addEventListener('input', () => updatePreviewText(elements.companyEmailInput, elements.previewCompanyEmail, 'E-mail'));
    
    elements.generateSheetBtn.addEventListener('click', () => {
        const headers = ["Nome", "Identificador", "LINK QR CODE"];
        const csvContent = "data:text/csv;charset=utf-8," + headers.join(",");
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "modelo_etiquetas.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    elements.fileUploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];

        if (file) {
            uploadedSheetFile = file;
            elements.generateFinalBtn.disabled = false;
            elements.generateWarning.classList.add('hidden');
            elements.previewEquipmentName.textContent = "Dados da Planilha...";
            elements.previewEquipmentId.textContent = "Carregados";
        } else {
            uploadedSheetFile = null;
            elements.generateFinalBtn.disabled = true;
            elements.generateWarning.classList.remove('hidden');
        }
    });

    elements.generateFinalBtn.addEventListener('click', async () => {
        if (!uploadedSheetFile) {
            alert("Erro: Nenhum ficheiro de planilha carregado. Por favor, faça o upload de um ficheiro.");
            return;
        }

        elements.generateFinalBtn.textContent = 'Gerando...';
        elements.generateFinalBtn.disabled = true;

        const formData = new FormData();
        formData.append('sheet', uploadedSheetFile);
        if (uploadedLogoFile) formData.append('logo', uploadedLogoFile);
        
        formData.append('company_name', elements.companyNameInput.value);
        formData.append('company_phone', elements.companyPhoneInput.value);
        formData.append('company_email', elements.companyEmailInput.value);
        formData.append('logo_height', elements.previewLogoContainer.style.height);

        try {
            const response = await fetch('/generate', { method: 'POST', body: formData });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `O servidor retornou o erro ${response.status}`);
            }
            const pdfBlob = await response.blob();
            const url = window.URL.createObjectURL(pdfBlob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'etiquetas.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
        } catch (error) {
            console.error("Erro ao gerar PDF:", error);
            alert(`Falha na geração: ${error.message}`);
        } finally {
            elements.generateFinalBtn.textContent = 'Gerar e Baixar PDF';
            if (uploadedSheetFile) elements.generateFinalBtn.disabled = false;
        }
    });
});
