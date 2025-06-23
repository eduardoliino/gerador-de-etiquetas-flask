# Gerador de Etiquetas para Equipamentos

![Status](https://img.shields.io/badge/status-concluído-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/eduardoliino/gerador-de-etiquetas-flask/blob/main/LICENSE)

Uma aplicação web construída com Flask e JavaScript para gerar etiquetas de identificação para equipamentos em massa a partir de uma planilha, com pré-visualização em tempo real e opções de layout customizáveis.

---

###  (Demonstração do Projeto)

**[NOTA PARA VOCÊ: Lembre-se de tirar um novo print da tela, mostrando as opções "PDF Único" e "ZIP", e atualizar esta imagem.]**

![Interface do Gerador de Etiquetas mostrando o painel de controle à esquerda e a pré-visualização da etiqueta à direita](![image](https://github.com/user-attachments/assets/475eef55-3dd0-4cc0-82fb-0f24eacff10c)

---

### ✅ Funcionalidades Principais (Atualizado)

*   **Interface Intuitiva:** Painel de controle e área de pré-visualização lado a lado.
*   **Pré-visualização em Tempo Real:** Veja como sua etiqueta ficará enquanto você edita as informações da empresa e o logo.
*   **Geração de Planilha Modelo:** Baixe um modelo `.xlsx` pré-formatado para garantir a importação correta dos dados.
*   **Upload de Dados em Lote:** Faça o upload da planilha preenchida (compatível com `.xlsx` e `.csv`) para gerar dezenas ou centenas de etiquetas de uma só vez.
*   **QR Code Dinâmico:** Cada etiqueta gera automaticamente um QR Code baseado no link fornecido na planilha.
*   **Layouts de PDF Flexíveis:** Escolha entre dois layouts para o PDF final:
    1.  **Etiqueta Centralizada:** Uma etiqueta com bordas, centralizada em uma página A4 (ideal para visualização e impressão única).
    2.  **Página Inteira:** A etiqueta ocupa toda a página A4, otimizada para impressão direta e com layout flexível que se ajusta ao tamanho da logo.
*   **Múltiplos Modos de Saída:** Exporte seu trabalho de duas maneiras:
    1.  **PDF Único:** Todas as etiquetas são consolidadas em um único arquivo PDF.
    2.  **Arquivo ZIP:** Gera um arquivo `.zip` contendo um PDF individual para cada etiqueta.

---

### 🛠️ Tecnologias Utilizadas

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

**1. Clone o Repositório:**
```bash
git clone https://github.com/[SEU-USUARIO/NOME-DO-SEU-REPOSITORIO].git
cd NOME-DO-SEU-REPOSITORIO
```
*(Substitua `[SEU-USUARIO/NOME-DO-SEU-REPOSITORIO]` pelo URL correto do seu projeto)*

**2. Instale as Dependências de Sistema (Passo Crucial!)**

A biblioteca `WeasyPrint` requer algumas dependências que precisam ser instaladas manualmente no seu sistema operacional antes de instalar os pacotes Python.

*   **Para Windows:**
    A maneira mais fácil é instalar um ambiente de execução GTK3. Baixe e instale a última versão do `gtk3-runtime` compatível com sua arquitetura (win64). Após a instalação, **é essencial adicionar a pasta de instalação (ex: `C:\Program Files\GTK3-Runtime Win64\bin`) ao `PATH` do sistema**, para que o Python possa encontrar os arquivos necessários (`.dll`).

*   **Para macOS (usando Homebrew):**
    ```bash
    brew install pango cairo libffi
    ```

*   **Para Linux (Debian/Ubuntu):**
    ```bash
    sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libcairo2 libffi-dev
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

**4. Instale as Dependências Python:**
O arquivo `requirements.txt` contém todas as bibliotecas Python necessárias.
```bash
pip install -r requirements.txt
```

**5. Execute a Aplicação:**
```bash
python app.py
```

**6. Acesse no Navegador:**
Abra seu navegador e acesse **[http://127.0.0.1:5000](http://127.0.0.1:5000)**. A aplicação estará funcionando!

---

### 📂 Estrutura do Projeto (Atualizado)
```
.
├── app.py              # Ponto de entrada da aplicação Flask
├── requirements.txt    # Lista de dependências Python
├── .gitignore          # Arquivos e pastas a serem ignorados pelo Git
├── routes/
│   └── main_routes.py  # Define as rotas (URLs) da aplicação
├── services/
│   └── pdf_service.py  # Lógica principal de geração do PDF e ZIP
├── static/
│   ├── css/
│   │   ├── card_layout.css
│   │   └── fullpage_layout.css
│   └── js/
│       └── main.js     # JavaScript para interatividade do frontend
└── templates/
    └── index.html      # Estrutura HTML da página
```

---

### 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

### 👨‍💻 Autor

Criado por **Eduardo Lino**.
```
