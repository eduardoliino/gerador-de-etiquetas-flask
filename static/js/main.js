// static/js/main.js

// Executa o código quando o conteúdo da página estiver totalmente carregado
document.addEventListener('DOMContentLoaded', () => {
    // --- ELEMENTOS DO DOM ---
    const logoUpload = document.getElementById('logo-upload');
    const logoSizeSlider = document.getElementById('logo-size');
    const companyNameInput = document.getElementById('company-name');
    const companyPhoneInput = document.getElementById('company-phone');
    const companyEmailInput = document.getElementById('company-email');
    const generateSheetBtn = document.getElementById('generate-sheet-btn');
    const fileUploadInput = document.getElementById('fileUpload');
    const layoutModeSelect = document.getElementById('layout-mode');
    const generateFinalBtn = document.getElementById('generate-final-btn');
    const generateWarning = document.getElementById('generate-warning');
    
    // --- ELEMENTOS DA PRÉ-VISUALIZAÇÃO ---
    const previewLogo = document.getElementById('preview-logo');
    const previewLogoContainer = document.getElementById('preview-logo-container');
    const previewCompanyName = document.getElementById('preview-company-name');
    const previewCompanyPhone = document.getElementById('preview-company-phone');
    const previewCompanyEmail = document.getElementById('preview-company-email');
    const previewEquipmentName = document.getElementById('preview-equipment-name');
    const previewEquipmentId = document.getElementById('preview-equipment-id');
    const qrCodeContainer = document.getElementById('preview-qr-code');

    let uploadedFile = null;
    let logoFile = null;

    // --- QR CODE DE PRÉ-VISUALIZAÇÃO ---
    const qr = new QRCode(qrCodeContainer, {
        text: 'PREVIEW_QR_CODE',
        width: 140,
        height: 140,
        correctLevel: QRCode.CorrectLevel.H
    });

    // --- ATUALIZAÇÕES EM TEMPO REAL ---

    logoUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            logoFile = file; // Armazena o arquivo do logo
            const reader = new FileReader();
            reader.onload = (e) => {
                previewLogo.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    logoSizeSlider.addEventListener('input', (event) => {
        const size = event.target.value;
        previewLogoContainer.style.height = `${size}px`;
        previewLogo.style.maxHeight = `${size}px`;
    });
    
    companyNameInput.addEventListener('input', (e) => { previewCompanyName.textContent = e.target.value || 'Nome da Empresa'; });
    companyPhoneInput.addEventListener('input', (e) => { previewCompanyPhone.textContent = e.target.value || 'Telefone'; });
    companyEmailInput.addEventListener('input', (e) => { previewCompanyEmail.textContent = e.target.value || 'E-mail'; });
    
    // --- LÓGICA DE ARQUIVOS ---

    // Botão para baixar a planilha modelo
    generateSheetBtn.addEventListener('click', () => {
        const headers = ["Nome do equipamento", "Identificador", "LINK QR CODE"];
        const csvContent = "data:text/csv;charset=utf-8," + headers.join(",");
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "modelo_etiquetas.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    // Lida com o upload da planilha
    fileUploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            uploadedFile = file;
            generateFinalBtn.disabled = false;
            generateWarning.classList.add('hidden');
            // Opcional: Ler a primeira linha para atualizar a pré-visualização
            // (requer uma biblioteca de parsing de CSV/XLSX no frontend ou um endpoint no backend)
            previewEquipmentName.textContent = "Dados da Planilha...";
            previewEquipmentId.textContent = "Carregados";
        } else {
            uploadedFile = null;
            generateFinalBtn.disabled = true;
            generateWarning.classList.remove('hidden');
        }
    });

    // --- GERAÇÃO FINAL ---
    generateFinalBtn.addEventListener('click', async () => {
        if (!uploadedFile) {
            alert("Por favor, faça o upload de uma planilha preenchida.");
            return;
        }

        // Mostrar estado de carregamento
        generateFinalBtn.textContent = 'Gerando...';
        generateFinalBtn.disabled = true;

        const formData = new FormData();
        
        // Adicionar a planilha
        formData.append('sheet', uploadedFile);

        // Adicionar o logo, se existir
        if (logoFile) {
            formData.append('logo', logoFile);
        }
        
        // Adicionar dados do template
        formData.append('company_name', companyNameInput.value);
        formData.append('company_phone', companyPhoneInput.value);
        formData.append('company_email', companyEmailInput.value);
        formData.append('logo_height', previewLogoContainer.style.height); // Envia a altura do logo
        formData.append('layout_mode', layoutModeSelect.value);

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || "Ocorreu um erro no servidor.");
            }

            // Receber o PDF como um blob
            const pdfBlob = await response.blob();
            const url = window.URL.createObjectURL(pdfBlob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'etiquetas.pdf'; // Nome do arquivo para download
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            
        } catch (error) {
            console.error("Erro ao gerar PDF:", error);
            alert(`Falha na geração: ${error.message}`);
        } finally {
            // Restaurar botão
            generateFinalBtn.textContent = 'Gerar e Baixar PDF';
            if(uploadedFile) generateFinalBtn.disabled = false;
        }
    });
});
