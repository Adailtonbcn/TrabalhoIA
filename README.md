# SmartCV - Analisador de Currículos com IA (Google Gemini)

Um Software as a Service (SaaS) desenvolvido com **Streamlit** para análise inteligente de currículos usando **Google Gemini AI**.

## 🎯 Objetivo

Desenvolver uma plataforma web capaz de receber currículos (PDF ou TXT), analisar seu conteúdo usando Google Gemini e gerar feedback detalhado com base em critérios profissionais.

## ✨ Funcionalidades

### 📤 Upload de Currículo
- ✅ Suporte para arquivos **PDF** e **TXT**
- ✅ Interface intuitiva com validação robusta
- ✅ Extração inteligente de texto de PDFs
- ✅ Preview do conteúdo extraído
- ✅ Validação de tamanho (máx. 10MB)

### 🧠 Análise com Google Gemini
- ✅ Processamento via **Google Gemini 1.5 Flash**
- ✅ Análise de **clareza e coesão textual**
- ✅ Avaliação de **estrutura e organização**
- ✅ Identificação de **palavras-chave relevantes**
- ✅ Sugestões de melhoria personalizadas
- ✅ Análise compatível com sistemas **ATS**

### 📊 Feedback Detalhado
- ✅ **Nota geral** com justificativa (0-100)
- ✅ Análise por critérios específicos
- ✅ Identificação de **pontos fortes**
- ✅ Sugestões de **melhorias direcionadas**
- ✅ Análise de palavras-chave **ausentes/presentes**
- ✅ Interface visual com progress bars e métricas

### 📋 Relatório Exportável
- ✅ Exportação em formato **TXT**
- ✅ Relatório completo e resumido
- ✅ Fácil compartilhamento e arquivamento
- ✅ Recomendações personalizadas

## 🛠️ Tecnologias

- **Frontend/Interface**: Streamlit
- **Backend/Processamento**: Python 3.8+
- **API de IA**: Google Gemini 1.5 Flash
- **Parsing de PDF**: PyPDF2
- **Hospedagem**: Streamlit Cloud
- **Controle de Versão**: GitHub

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Conta Google Cloud com API Gemini habilitada
- Git

### Obter API Key do Google Gemini

1. **Acesse o Google AI Studio:**
   - Vá para [aistudio.google.com](https://aistudio.google.com)
   - Faça login com sua conta Google

2. **Gere sua API Key:**
   - Clique em "Get API Key"
   - Clique em "Create API Key"
   - Copie a chave gerada

3. **Configure cotas (se necessário):**
   - Acesse [console.cloud.google.com](https://console.cloud.google.com)
   - Habilite a API Generative AI
   - Configure limites de uso

### Instalação Local

1. **Clone o repositório:**
\`\`\`bash
git clone https://github.com/seu-usuario/smartcv-gemini.git
cd smartcv-gemini
\`\`\`

2. **Crie um ambiente virtual:**
\`\`\`bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
\`\`\`

3. **Instale as dependências:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Configure as variáveis de ambiente:**
\`\`\`bash
cp .env.example .env
\`\`\`

Edite o arquivo \`.env\` e adicione sua chave do Gemini:
\`\`\`
GEMINI_API_KEY=sua_chave_gemini_aqui
\`\`\`

5. **Execute a aplicação:**
\`\`\`bash
streamlit run app.py
\`\`\`

6. **Acesse no navegador:**
\`\`\`
http://localhost:8501
\`\`\`

### Deploy no Streamlit Cloud

1. **Fork este repositório**
2. **Acesse [share.streamlit.io](https://share.streamlit.io)**
3. **Conecte sua conta GitHub**
4. **Selecione o repositório e branch**
5. **Configure os secrets:**
   - Vá em "Advanced settings"
   - Adicione: \`GEMINI_API_KEY = "sua_chave_aqui"\`
6. **Deploy automático!**

## 📖 Como Usar

### Passo a Passo Detalhado

1. **📤 Upload do Currículo**
   - Clique em "Browse files" ou arraste o arquivo
   - Formatos aceitos: PDF, TXT
   - Tamanho máximo: 10MB
   - Aguarde a extração do texto

2. **👀 Preview e Validação**
   - Visualize o texto extraído
   - Verifique estatísticas (palavras, caracteres)
   - Confirme se a extração foi bem-sucedida

3. **🧠 Análise com Gemini**
   - Clique em "Analisar Currículo com Gemini"
   - Aguarde o processamento (30-60 segundos)
   - Acompanhe o progresso em tempo real

4. **📊 Visualização dos Resultados**
   - **Nota Geral**: Pontuação de 0-100 com classificação
   - **Análise Detalhada**: Por critérios específicos
   - **Palavras-chave**: Presentes e ausentes
   - **Sugestões**: Melhorias personalizadas

5. **📋 Exportação e Relatórios**
   - Baixe o relatório completo em TXT
   - Ou baixe o resumo executivo
   - Compartilhe ou arquive conforme necessário

## 🎯 Critérios de Análise

### 📝 Clareza e Coesão (0-100)
- **Linguagem clara e objetiva**
- **Ausência de erros gramaticais**
- **Fluidez na leitura**
- **Uso adequado de verbos de ação**
- **Conectividade entre ideias**

### 🏗️ Estrutura e Organização (0-100)
- **Organização lógica das seções**
- **Formatação consistente e profissional**
- **Hierarquia clara de informações**
- **Uso adequado de bullet points**
- **Cronologia adequada (mais recente primeiro)**

### 🔑 Palavras-chave e Relevância (0-100)
- **Presença de termos técnicos relevantes**
- **Habilidades técnicas e soft skills**
- **Compatibilidade com sistemas ATS**
- **Tendências do mercado de trabalho**
- **Palavras-chave por área específica**

## 💰 Custos e Limites

### Google Gemini API (Gratuito)
- **Gemini 1.5 Flash**: 15 requisições/minuto
- **Limite mensal**: Generoso para uso pessoal
- **Custo**: Gratuito até o limite
- **Upgrade**: Disponível para uso comercial

### Streamlit Cloud (Gratuito)
- **Hospedagem**: Gratuita
- **Recursos**: Adequados para MVP
- **Limitações**: Compartilhamento de recursos

## 🔒 Segurança e Privacidade

- ✅ **Chaves de API protegidas** via Streamlit Secrets
- ✅ **Processamento seguro** de arquivos
- ✅ **Não armazenamento** de dados pessoais
- ✅ **Validação robusta** de entrada
- ✅ **Conexão criptografada** com APIs
- ✅ **Limpeza automática** de dados temporários

## 📁 Estrutura do Projeto

\`\`\`
smartcv-gemini/
├── app.py                 # Aplicação principal Streamlit
├── config.py             # Configurações centralizadas
├── utils.py              # Funções utilitárias
├── requirements.txt      # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo Git
├── README.md            # Documentação completa
├── .streamlit/          # Configurações do Streamlit
│   └── config.toml
└── assets/              # Recursos estáticos (se houver)
    └── screenshots/
\`\`\`

## 🎨 Interface e UX

### Design Responsivo
- ✅ Layout adaptável para desktop e mobile
- ✅ Cores baseadas no Google Material Design
- ✅ Componentes intuitivos e acessíveis
- ✅ Feedback visual em tempo real

### Experiência do Usuário
- ✅ Fluxo linear e intuitivo
- ✅ Mensagens de erro claras
- ✅ Progress bars para operações longas
- ✅ Validação em tempo real
- ✅ Tooltips e ajuda contextual

## 🤝 Contribuição

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (\`git checkout -b feature/AmazingFeature\`)
3. **Commit** suas mudanças (\`git commit -m 'Add some AmazingFeature'\`)
4. **Push** para a branch (\`git push origin feature/AmazingFeature\`)
5. Abra um **Pull Request**
