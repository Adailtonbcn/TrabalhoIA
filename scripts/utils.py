"""
Utilitários para o SmartCV com Google Gemini
"""

import streamlit as st
import PyPDF2
import io
import json
import re
from typing import Optional, Dict, Any, Tuple
from datetime import datetime

def extract_text_from_pdf(pdf_file) -> Optional[str]:
    """
    Extrai texto de um arquivo PDF com tratamento robusto de erros
    
    Args:
        pdf_file: Arquivo PDF carregado
        
    Returns:
        str: Texto extraído ou None se houver erro
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        total_pages = len(pdf_reader.pages)
        
        # Progress bar para PDFs grandes
        if total_pages > 5:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    # Limpar texto extraído
                    page_text = clean_extracted_text(page_text)
                    text += page_text + "\n"
                
                # Atualizar progress bar
                if total_pages > 5:
                    progress = (page_num + 1) / total_pages
                    progress_bar.progress(progress)
                    status_text.text(f"Processando página {page_num + 1} de {total_pages}")
                    
            except Exception as e:
                st.warning(f"⚠️ Erro ao processar página {page_num + 1}: {str(e)}")
                continue
        
        # Limpar progress bar
        if total_pages > 5:
            progress_bar.empty()
            status_text.empty()
        
        return text.strip() if text.strip() else None
        
    except Exception as e:
        st.error(f"❌ Erro ao processar PDF: {str(e)}")
        return None

def clean_extracted_text(text: str) -> str:
    """
    Limpa e normaliza texto extraído de PDFs
    
    Args:
        text: Texto bruto extraído
        
    Returns:
        str: Texto limpo e normalizado
    """
    if not text:
        return ""
    
    # Remover caracteres de controle
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', text)
    
    # Normalizar quebras de linha
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Remover espaços extras
    text = re.sub(r' +', ' ', text)
    
    # Remover linhas muito curtas (provavelmente lixo)
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if len(line) > 2:  # Manter apenas linhas com mais de 2 caracteres
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def validate_file(uploaded_file) -> Tuple[bool, str]:
    """
    Valida o arquivo carregado
    
    Args:
        uploaded_file: Arquivo carregado pelo Streamlit
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "Nenhum arquivo selecionado"
    
    # Verificar tipo de arquivo
    allowed_types = ['application/pdf', 'text/plain']
    if uploaded_file.type not in allowed_types:
        return False, f"Tipo de arquivo não suportado: {uploaded_file.type}"
    
    # Verificar tamanho do arquivo (10MB max)
    max_size = 10 * 1024 * 1024  # 10MB
    if uploaded_file.size > max_size:
        return False, f"Arquivo muito grande: {uploaded_file.size / 1024 / 1024:.1f}MB (máx: 10MB)"
    
    # Verificar se o arquivo não está vazio
    if uploaded_file.size == 0:
        return False, "Arquivo está vazio"
    
    return True, ""

def validate_content(content: str) -> Tuple[bool, str]:
    """
    Valida o conteúdo extraído
    
    Args:
        content: Conteúdo do currículo
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not content or not content.strip():
        return False, "Conteúdo vazio"
    
    # Verificar tamanho mínimo
    if len(content.strip()) < 50:
        return False, "Conteúdo muito curto para análise (mínimo: 50 caracteres)"
    
    # Verificar tamanho máximo
    if len(content) > 50000:
        return False, "Conteúdo muito longo (máximo: 50.000 caracteres)"
    
    # Verificar se não é apenas espaços ou caracteres especiais
    clean_content = re.sub(r'[^\w\s]', '', content)
    if len(clean_content.strip()) < 30:
        return False, "Conteúdo não contém texto suficiente para análise"
    
    return True, ""

def format_score_display(score: int) -> Dict[str, str]:
    """
    Formata a exibição da pontuação
    
    Args:
        score: Pontuação (0-100)
        
    Returns:
        dict: Informações de formatação
    """
    if score >= 90:
        return {
            "emoji": "🟢",
            "color": "#34a853",
            "level": "Excelente",
            "class": "score-excellent",
            "description": "Currículo excepcional!"
        }
    elif score >= 80:
        return {
            "emoji": "🟢", 
            "color": "#34a853",
            "level": "Muito Bom",
            "class": "score-excellent",
            "description": "Currículo muito bem estruturado"
        }
    elif score >= 70:
        return {
            "emoji": "🟡",
            "color": "#fbbc04",
            "level": "Bom",
            "class": "score-good",
            "description": "Bom currículo com potencial"
        }
    elif score >= 60:
        return {
            "emoji": "🟡",
            "color": "#fbbc04",
            "level": "Regular",
            "class": "score-good",
            "description": "Currículo adequado, mas pode melhorar"
        }
    else:
        return {
            "emoji": "🔴",
            "color": "#ea4335",
            "level": "Precisa Melhorar",
            "class": "score-poor",
            "description": "Currículo precisa de melhorias importantes"
        }

def validate_analysis_response(response_text: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """
    Valida e processa a resposta da análise do Gemini
    
    Args:
        response_text: Resposta bruta do Gemini
        
    Returns:
        tuple: (is_valid, parsed_data, error_message)
    """
    try:
        # Limpar possíveis marcadores de código
        clean_text = response_text.strip()
        if clean_text.startswith('```json'):
            clean_text = clean_text[7:]
        if clean_text.endswith('```'):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        # Tentar fazer parse do JSON
        data = json.loads(clean_text)
        
        # Validar estrutura obrigatória
        required_keys = ['overallScore', 'clarity', 'structure', 'keywords', 'improvements', 'strengths', 'summary']
        for key in required_keys:
            if key not in data:
                return False, None, f"Chave obrigatória '{key}' não encontrada"
        
        # Validar sub-estruturas
        for section in ['clarity', 'structure']:
            if not isinstance(data[section], dict):
                return False, None, f"Seção '{section}' deve ser um objeto"
            
            required_sub_keys = ['score', 'feedback', 'suggestions']
            for sub_key in required_sub_keys:
                if sub_key not in data[section]:
                    return False, None, f"Chave '{sub_key}' não encontrada em '{section}'"
        
        # Validar keywords
        if not isinstance(data['keywords'], dict):
            return False, None, "Seção 'keywords' deve ser um objeto"
        
        keywords_keys = ['score', 'missing', 'present', 'suggestions']
        for key in keywords_keys:
            if key not in data['keywords']:
                return False, None, f"Chave '{key}' não encontrada em 'keywords'"
        
        # Validar tipos de dados
        score_fields = ['overallScore', 'clarity.score', 'structure.score', 'keywords.score']
        for field in score_fields:
            if '.' in field:
                section, key = field.split('.')
                value = data[section][key]
            else:
                value = data[field]
            
            if not isinstance(value, (int, float)) or not (0 <= value <= 100):
                return False, None, f"Campo '{field}' deve ser um número entre 0 e 100"
        
        # Validar arrays
        array_fields = ['improvements', 'strengths', 'clarity.suggestions', 'structure.suggestions', 'keywords.suggestions', 'keywords.missing', 'keywords.present']
        for field in array_fields:
            if '.' in field:
                section, key = field.split('.')
                value = data[section][key]
            else:
                value = data[field]
            
            if not isinstance(value, list):
                return False, None, f"Campo '{field}' deve ser uma lista"
        
        return True, data, ""
        
    except json.JSONDecodeError as e:
        return False, None, f"Erro ao decodificar JSON: {str(e)}"
    except Exception as e:
        return False, None, f"Erro na validação: {str(e)}"

def generate_report_text(analysis: Dict[str, Any], filename: str = "", detailed: bool = True) -> str:
    """
    Gera o texto do relatório completo ou resumido
    
    Args:
        analysis: Resultado da análise
        filename: Nome do arquivo analisado
        detailed: Se deve gerar relatório detalhado ou resumido
        
    Returns:
        str: Relatório formatado
    """
    timestamp = datetime.now().strftime('%d/%m/%Y às %H:%M')
    
    if detailed:
        return f"""
RELATÓRIO DETALHADO DE ANÁLISE DE CURRÍCULO - SmartCV
{'='*65}

📄 INFORMAÇÕES DA ANÁLISE
Data: {timestamp}
Arquivo: {filename or 'Não especificado'}
Modelo de IA: Google Gemini 1.5 Flash
Versão do SmartCV: 2.0

🎯 AVALIAÇÃO GERAL
Nota Final: {analysis['overallScore']}/100 ({format_score_display(analysis['overallScore'])['level']})

Resumo Executivo:
{analysis['summary']}

{'='*65}
📊 ANÁLISE DETALHADA POR CRITÉRIO
{'='*65}

📝 CLAREZA E COESÃO
Pontuação: {analysis['clarity']['score']}/100 ({format_score_display(analysis['clarity']['score'])['level']})
{'-'*45}
{analysis['clarity']['feedback']}

💡 Sugestões de Melhoria:
{chr(10).join([f"   • {s}" for s in analysis['clarity']['suggestions']])}

🏗️ ESTRUTURA E ORGANIZAÇÃO
Pontuação: {analysis['structure']['score']}/100 ({format_score_display(analysis['structure']['score'])['level']})
{'-'*45}
{analysis['structure']['feedback']}

💡 Sugestões de Melhoria:
{chr(10).join([f"   • {s}" for s in analysis['structure']['suggestions']])}

🔑 PALAVRAS-CHAVE E RELEVÂNCIA
Pontuação: {analysis['keywords']['score']}/100 ({format_score_display(analysis['keywords']['score'])['level']})
{'-'*45}

✅ Palavras-chave Identificadas:
{chr(10).join([f"   • {k}" for k in analysis['keywords']['present']]) if analysis['keywords']['present'] else "   • Nenhuma palavra-chave relevante identificada"}

❌ Palavras-chave Ausentes (Sugeridas):
{chr(10).join([f"   • {k}" for k in analysis['keywords']['missing']]) if analysis['keywords']['missing'] else "   • Todas as palavras-chave importantes estão presentes"}

💡 Recomendações:
{chr(10).join([f"   • {s}" for s in analysis['keywords']['suggestions']])}

{'='*65}
⭐ PONTOS FORTES IDENTIFICADOS
{'='*65}
{chr(10).join([f"✅ {s}" for s in analysis['strengths']])}

{'='*65}
🔧 OPORTUNIDADES DE MELHORIA
{'='*65}
{chr(10).join([f"🔧 {s}" for s in analysis['improvements']])}

{'='*65}
📈 RECOMENDAÇÕES FINAIS
{'='*65}

Com base na análise realizada, seu currículo recebeu a nota {analysis['overallScore']}/100.

{get_final_recommendation(analysis['overallScore'])}

PRÓXIMOS PASSOS RECOMENDADOS:
1. Implemente as sugestões de maior impacto primeiro
2. Revise a formatação e estrutura geral
3. Adicione palavras-chave relevantes para sua área
4. Quantifique suas conquistas com números e resultados
5. Adapte o currículo para cada vaga específica

DICAS EXTRAS:
• Mantenha o currículo sempre atualizado
• Use verbos de ação no início das descrições
• Destaque resultados mensuráveis
• Mantenha consistência na formatação
• Revise ortografia e gramática cuidadosamente

---
Relatório gerado automaticamente pelo SmartCV
Analisador de Currículos com Inteligência Artificial
Powered by Google Gemini | Desenvolvido com Streamlit

© 2024 SmartCV - Todos os direitos reservados
Para mais análises: https://smartcv.streamlit.app
        """
    else:
        return f"""
SMARTCV - RELATÓRIO RESUMIDO
{'='*35}

📄 Arquivo: {filename or 'Não especificado'}
📅 Data: {timestamp}
🤖 IA: Google Gemini

🎯 NOTA GERAL: {analysis['overallScore']}/100
Classificação: {format_score_display(analysis['overallScore'])['level']}

📊 PONTUAÇÕES DETALHADAS:
• Clareza e Coesão: {analysis['clarity']['score']}/100
• Estrutura: {analysis['structure']['score']}/100  
• Palavras-chave: {analysis['keywords']['score']}/100

🔧 PRINCIPAIS MELHORIAS:
{chr(10).join([f"• {s}" for s in analysis['improvements'][:5]])}

⭐ PRINCIPAIS PONTOS FORTES:
{chr(10).join([f"• {s}" for s in analysis['strengths'][:3]])}

---
SmartCV - Powered by Google Gemini
        """

def get_final_recommendation(score: int) -> str:
    """
    Retorna recomendação final baseada na pontuação
    
    Args:
        score: Pontuação geral
        
    Returns:
        str: Recomendação personalizada
    """
    if score >= 90:
        return """
🎉 EXCELENTE! Seu currículo está em estado excepcional. Continue refinando os pequenos detalhes e mantendo-o sempre atualizado. Você está no caminho certo para se destacar no mercado de trabalho.
        """
    elif score >= 80:
        return """
👍 MUITO BOM! Seu currículo tem uma base sólida e está bem estruturado. Implemente as sugestões apresentadas para alcançar a excelência e se destacar ainda mais no processo seletivo.
        """
    elif score >= 70:
        return """
📈 BOM POTENCIAL! Seu currículo tem uma boa base, mas há oportunidades claras de melhoria. Foque nas sugestões de maior impacto para aumentar significativamente sua competitividade.
        """
    elif score >= 60:
        return """
⚠️ ATENÇÃO NECESSÁRIA! Seu currículo precisa de melhorias importantes. Dedique tempo para implementar as sugestões apresentadas, especialmente nas áreas com menor pontuação.
        """
    else:
        return """
🚨 REVISÃO URGENTE! Seu currículo precisa de uma reformulação significativa. Recomendamos focar primeiro na estrutura básica e clareza, depois nas palavras-chave e detalhes específicos.
        """

def get_content_statistics(content: str) -> Dict[str, Any]:
    """
    Calcula estatísticas do conteúdo
    
    Args:
        content: Texto do currículo
        
    Returns:
        dict: Estatísticas do conteúdo
    """
    if not content:
        return {}
    
    words = content.split()
    sentences = re.split(r'[.!?]+', content)
    paragraphs = content.split('\n\n')
    
    return {
        "characters": len(content),
        "characters_no_spaces": len(content.replace(' ', '')),
        "words": len(words),
        "sentences": len([s for s in sentences if s.strip()]),
        "paragraphs": len([p for p in paragraphs if p.strip()]),
        "avg_words_per_sentence": len(words) / max(len([s for s in sentences if s.strip()]), 1),
        "reading_time_minutes": max(1, len(words) // 200)  # ~200 palavras por minuto
    }
