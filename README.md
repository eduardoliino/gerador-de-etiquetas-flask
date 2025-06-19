# Gerador de Etiquetas para Equipamentos

![Status](https://img.shields.io/badge/status-concluído-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)

Uma aplicação web construída com Flask e JavaScript para gerar etiquetas de identificação em massa a partir de uma planilha, com pré-visualização em tempo real e opções de layout customizáveis.

---

### Pré-visualização do Projeto


Screenshot da Aplicação![image](https://github.com/user-attachments/assets/3ed42315-7c1d-4f05-9edf-b28d1f516675)

---

###  Funcionalidades Principais

*   **Interface Intuitiva:** Painel de controle e área de pré-visualização lado a lado.
*   **Pré-visualização em Tempo Real:** Veja como sua etiqueta ficará enquanto você edita as informações da empresa e o logo.
*   **Geração de Planilha Modelo:** Baixe um modelo `.xlsx` pré-formatado para garantir a importação correta dos dados.
*   **Upload de Dados em Lote:** Faça o upload da planilha preenchida (compatível com `.xlsx` e `.csv`) para gerar dezenas ou centenas de etiquetas de uma só vez.
*   **QR Code Dinâmico:** Cada etiqueta gera automaticamente um QR Code baseado no link fornecido na planilha.
*   **Layouts de PDF Flexíveis:** Escolha entre dois layouts para o PDF final:
    1.  **Etiqueta Centralizada:** Uma etiqueta com bordas, centralizada em uma página A4 (ideal para visualização e impressão única).
    2.  **Página Inteira:** A etiqueta ocupa toda a página A4, otimizada para impressão direta em papel especial.

---

###  Tecnologias Utilizadas

*   **Backend:**
    *   **Python 3**
    *   **Flask:** Micro-framework web para servir a aplicação e as rotas.
    *   **Pandas:** Para ler e processar os dados das planilhas (`.xlsx`, `.csv`).
    *   **WeasyPrint:** Para converter HTML e CSS em arquivos PDF.
    *   **qrcode[pil]:** Para gerar as imagens de QR Code.
*   **Frontend:**
    *   **HTML5**
    *   **Tailwind CSS:** Framework CSS para um design moderno e responsivo.
    *   **JavaScript (Vanilla):** Para a interatividade da página, manipulação de DOM e comunicação com o backend (via `fetch`).

---

###  Como Executar o Projeto

Siga os passos abaixo para executar a aplicação localmente.

**1. Pré-requisitos:**
*   Você precisa ter o **Python 3.8 ou superior** instalado.
*   Você precisa ter o `pip` (gerenciador de pacotes do Python) instalado.

**2. Clone o Repositório:**
```bash
git clone https://github.com/seu-usuario/nome-do-seu-repositorio.git
cd nome-do-seu-repositorio
```

**3. Crie e Ative um Ambiente Virtual (Recomendado):**
*   **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   **macOS / Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**4. Instale as Dependências:**
O arquivo `requirements.txt` contém todas as bibliotecas Python necessárias.
```bash
pip install -r requirements.txt
```

**5. Execute a Aplicação:**
```bash
python app.py
```

**6. Acesse no Navegador:**
Abra seu navegador e acesse [http://127.0.0.1:5000](http://127.0.0.1:5000). A aplicação estará funcionando!

---

###  Estrutura do Projeto
```
.
├── app.py              # Ponto de entrada da aplicação Flask
├── requirements.txt    # Lista de dependências Python
├── .gitignore          # Arquivos e pastas a serem ignorados pelo Git
├── routes/
│   └── main_routes.py  # Define as rotas (URLs) da aplicação
├── services/
│   └── pdf_service.py  # Lógica principal de geração do PDF
├── static/
│   └── js/
│       └── main.js     # JavaScript para interatividade do frontend
└── templates/
    └── index.html      # Estrutura HTML da página
```

---

###  Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

###  Autor

Criado por **[Eduardo Lino]**.
