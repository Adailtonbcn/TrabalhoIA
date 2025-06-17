"""
Configurações do SmartCV com Google Gemini
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações da API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"  # Modelo mais rápido e econômico

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    "page_title": "SmartCV - Analisador de Currículos com IA",
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configurações de análise
ANALYSIS_CONFIG = {
    "model": GEMINI_MODEL,
    "temperature": 0.3,
    "max_output_tokens": 2048,
    "top_p": 0.8,
    "top_k": 40
}

# Critérios de pontuação
SCORE_THRESHOLDS = {
    "excellent": 90,
    "very_good": 80,
    "good": 70,
    "regular": 60,
    "poor": 0
}

# Tipos de arquivo aceitos
ALLOWED_FILE_TYPES = ['pdf', 'txt']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Configurações de segurança
SECURITY_CONFIG = {
    "max_content_length": 50000,  # Máximo de caracteres para análise
    "min_content_length": 50,     # Mínimo de caracteres para análise
    "blocked_extensions": ['.exe', '.bat', '.sh', '.cmd'],
    "rate_limit_per_hour": 10     # Máximo de análises por hora por usuário
}

# Mensagens do sistema
SYSTEM_MESSAGES = {
    "welcome": "Bem-vindo ao SmartCV! Faça upload do seu currículo para receber uma análise detalhada.",
    "processing": "Analisando seu currículo com Google Gemini...",
    "success": "Análise concluída com sucesso!",
    "error_api": "Erro na API do Gemini. Tente novamente em alguns minutos.",
    "error_file": "Erro ao processar o arquivo. Verifique se não está corrompido.",
    "error_content": "Conteúdo insuficiente para análise. Mínimo: 50 caracteres."
}
