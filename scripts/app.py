import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import json
from datetime import datetime
import os
from typing import Dict, List, Any

# Configuração da página
st.set_page_config(
    page_title="SmartCV - Analisador de Currículos com IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #4285f4 0%, #34a853 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4285f4;
    }
    
    .score-excellent { border-left-color: #34a853 !important; }
    .score-good { border-left-color: #fbbc04 !important; }
    .score-poor { border-left-color: #ea4335 !important; }
    
    .suggestion-box {
        background: #e8f0fe;
        border: 1px solid #4285f4;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .strength-box {
        background: #e6f4ea;
        border: 1px solid #34a853;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .improvement-box {
        background: #fef7e0;
        border: 1px solid #fbbc04;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .gemini-badge {
        background: linear-gradient(45deg, #4285f4, #34a853);
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class CVAnalyzer:
    def __init__(self):
        self.gemini_model = None
        self.setup_gemini()
    
    def setup_gemini(self):
        """Configura o cliente Google Gemini"""
        api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                return True
            except Exception as e:
                st.error(f"Erro ao configurar Gemini: {str(e)}")
                return False
        else:
            st.error("⚠️ Chave da API Google Gemini não configurada!")
            return False
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extrai texto de arquivo PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    st.warning(f"Erro ao processar página {page_num + 1}: {str(e)}")
                    continue
            return text.strip()
        except Exception as e:
            st.error(f"Erro ao processar PDF: {str(e)}")
            return ""
    
    def analyze_cv(self, content: str) -> Dict[str, Any]:
        """Analisa o currículo usando Google Gemini"""
        if not self.gemini_model:
            return None
        
        prompt = f"""
        Você é um especialista em análise de currículos e recursos humanos com mais de 15 anos de experiência. 
        Analise o currículo fornecido de forma detalhada e crítica, retornando uma análise em formato JSON válido com a seguinte estrutura EXATA:

        {{
          "overallScore": [número de 0 a 100],
          "clarity": {{
            "score": [número de 0 a 100],
            "feedback": "[feedback detalhado sobre clareza e coesão do texto]",
            "suggestions": ["sugestão 1", "sugestão 2", "sugestão 3"]
          }},
          "structure": {{
            "score": [número de 0 a 100],
            "feedback": "[feedback sobre organização e estrutura]",
            "suggestions": ["sugestão 1", "sugestão 2", "sugestão 3"]
          }},
          "keywords": {{
            "score": [número de 0 a 100],
            "missing": ["palavra-chave ausente 1", "palavra-chave ausente 2"],
            "present": ["palavra-chave presente 1", "palavra-chave presente 2"],
            "suggestions": ["sugestão 1", "sugestão 2"]
          }},
          "improvements": ["melhoria 1", "melhoria 2", "melhoria 3"],
          "strengths": ["ponto forte 1", "ponto forte 2", "ponto forte 3"],
          "summary": "[resumo geral da análise em 2-3 frases]"
        }}

        CRITÉRIOS DE AVALIAÇÃO:
        
        1. CLAREZA E COESÃO (0-100):
        - Linguagem clara, objetiva e profissional
        - Ausência de erros gramaticais e ortográficos
        - Fluidez na leitura e conectividade entre ideias
        - Uso adequado de verbos de ação
        
        2. ESTRUTURA E ORGANIZAÇÃO (0-100):
        - Organização lógica das seções (dados pessoais, objetivo, experiência, formação, habilidades)
        - Formatação consistente e profissional
        - Hierarquia clara de informações
        - Uso adequado de bullet points e espaçamento
        - Cronologia adequada (mais recente primeiro)
        
        3. PALAVRAS-CHAVE E RELEVÂNCIA (0-100):
        - Presença de termos técnicos relevantes para a área
        - Habilidades técnicas e soft skills mencionadas
        - Compatibilidade com tendências do mercado de trabalho
        - Uso de palavras-chave que passam por sistemas ATS
        
        INSTRUÇÕES IMPORTANTES:
        - Seja específico e construtivo nas sugestões
        - Considere o contexto brasileiro do mercado de trabalho
        - Foque em melhorias práticas e implementáveis
        - Retorne APENAS o JSON válido, sem texto adicional
        - Use aspas duplas em todas as strings
        - Não use quebras de linha dentro das strings JSON

        CURRÍCULO PARA ANÁLISE:
        {content}
        """
        
        try:
            response = self.gemini_model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Limpar possíveis caracteres extras do Gemini
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
            
            result_text = result_text.strip()
            
            # Parse do JSON
            analysis = json.loads(result_text)
            
            # Validação básica da estrutura
            required_keys = ['overallScore', 'clarity', 'structure', 'keywords', 'improvements', 'strengths', 'summary']
            for key in required_keys:
                if key not in analysis:
                    raise ValueError(f"Chave obrigatória '{key}' não encontrada na resposta")
            
            return analysis
            
        except json.JSONDecodeError as e:
            st.error(f"Erro ao processar resposta da IA: {str(e)}")
            st.error(f"Resposta recebida: {result_text[:500]}...")
            return None
        except Exception as e:
            st.error(f"Erro na análise com Gemini: {str(e)}")
            return None

def get_score_color(score: int) -> str:
    """Retorna o emoji baseado na pontuação"""
    if score >= 80:
        return "🟢"
    elif score >= 60:
        return "🟡"
    else:
        return "🔴"

def get_score_class(score: int) -> str:
    """Retorna a classe CSS baseada na pontuação"""
    if score >= 80:
        return "score-excellent"
    elif score >= 60:
        return "score-good"
    else:
        return "score-poor"

def get_score_level(score: int) -> str:
    """Retorna o nível baseado na pontuação"""
    if score >= 90:
        return "Excelente"
    elif score >= 80:
        return "Muito Bom"
    elif score >= 70:
        return "Bom"
    elif score >= 60:
        return "Regular"
    else:
        return "Precisa Melhorar"

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 SmartCV</h1>
        <h3>Analisador de Currículos com Inteligência Artificial</h3>
        <p>Powered by <span class="gemini-badge">Google Gemini</span></p>
        <p>Receba feedback detalhado e melhore seu currículo com IA</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar o analisador
    analyzer = CVAnalyzer()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Como Usar")
        st.markdown("""
        **Passo a passo:**
        1. 📤 **Upload**: Faça upload do seu currículo
        2. 👀 **Preview**: Verifique o conteúdo extraído
        3. 🧠 **Análise**: Clique em "Analisar Currículo"
        4. 📊 **Resultados**: Explore as análises detalhadas
        5. 📋 **Relatório**: Baixe o relatório completo
        
        **Formatos aceitos:**
        - 📄 PDF (recomendado)
        - 📝 TXT (texto simples)
        
        **Máximo:** 10MB por arquivo
        """)
        
        st.markdown("---")
        
        st.header("🎯 Critérios Analisados")
        st.markdown("""
        **📝 Clareza e Coesão**
        - Linguagem profissional
        - Gramática e ortografia
        - Fluidez do texto
        
        **🏗️ Estrutura**
        - Organização lógica
        - Formatação consistente
        - Hierarquia de informações
        
        **🔑 Palavras-chave**
        - Termos técnicos relevantes
        - Compatibilidade com ATS
        - Habilidades em demanda
        """)
        
        st.markdown("---")
        
        # Status da API
        st.header("⚙️ Status do Sistema")
        if analyzer.gemini_model:
            st.success("✅ Google Gemini conectado")
            st.info("🚀 Modelo: Gemini 1.5 Flash")
        else:
            st.error("❌ Gemini não configurado")
            st.warning("Configure GEMINI_API_KEY")
    
    # Upload de arquivo
    st.header("📤 Upload do Currículo")
    
    uploaded_file = st.file_uploader(
        "Escolha seu arquivo de currículo",
        type=['pdf', 'txt'],
        help="Formatos aceitos: PDF, TXT | Tamanho máximo: 10MB",
        accept_multiple_files=False
    )
    
    if uploaded_file is not None:
        # Validação do arquivo
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
            st.error("❌ Arquivo muito grande! Máximo permitido: 10MB")
            return
        
        # Informações do arquivo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Nome", uploaded_file.name[:20] + "..." if len(uploaded_file.name) > 20 else uploaded_file.name)
        with col2:
            st.metric("📏 Tamanho", f"{uploaded_file.size / 1024:.1f} KB")
        with col3:
            file_type = "PDF" if uploaded_file.type == "application/pdf" else "TXT"
            st.metric("📋 Formato", file_type)
        
        # Extrair texto do arquivo
        with st.spinner("📖 Extraindo texto do arquivo..."):
            if uploaded_file.type == "application/pdf":
                content = analyzer.extract_text_from_pdf(uploaded_file)
            else:
                content = str(uploaded_file.read(), "utf-8")
        
        if content and len(content.strip()) > 50:
            # Estatísticas do conteúdo
            word_count = len(content.split())
            char_count = len(content)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Palavras", f"{word_count:,}")
            with col2:
                st.metric("📊 Caracteres", f"{char_count:,}")
            with col3:
                estimated_time = max(10, word_count // 100)
                st.metric("⏱️ Tempo estimado", f"{estimated_time}s")
            
            # Preview do conteúdo
            with st.expander("👀 Preview do Conteúdo Extraído", expanded=False):
                preview_text = content[:1500] + "..." if len(content) > 1500 else content
                st.text_area(
                    "Conteúdo extraído do arquivo:",
                    preview_text,
                    height=300,
                    disabled=True
                )
                
                if len(content) > 1500:
                    st.info(f"Mostrando primeiros 1.500 caracteres de {len(content):,} totais")
            
            # Botão de análise
            st.markdown("---")
            
            if st.button(
                "🧠 Analisar Currículo com Gemini",
                type="primary",
                use_container_width=True,
                disabled=not analyzer.gemini_model
            ):
                if not analyzer.gemini_model:
                    st.error("❌ Configure a API do Google Gemini para continuar")
                    st.info("Adicione sua GEMINI_API_KEY nas configurações")
                    return
                
                # Análise com progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("🔄 Enviando currículo para análise...")
                    progress_bar.progress(25)
                    
                    status_text.text("🧠 Gemini analisando conteúdo...")
                    progress_bar.progress(50)
                    
                    analysis = analyzer.analyze_cv(content)
                    progress_bar.progress(75)
                    
                    if analysis:
                        status_text.text("✅ Processando resultados...")
                        progress_bar.progress(100)
                        
                        # Salvar na sessão
                        st.session_state['analysis'] = analysis
                        st.session_state['content'] = content
                        st.session_state['filename'] = uploaded_file.name
                        
                        status_text.empty()
                        progress_bar.empty()
                        
                        st.success("🎉 Análise concluída com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.error("❌ Falha na análise. Tente novamente.")
                        
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Erro durante a análise: {str(e)}")
                    
        elif content:
            st.warning("⚠️ Conteúdo muito curto para análise. Mínimo: 50 caracteres.")
        else:
            st.error("❌ Não foi possível extrair texto do arquivo. Verifique se o arquivo não está corrompido.")
    
    # Mostrar resultados da análise
    if 'analysis' in st.session_state:
        analysis = st.session_state['analysis']
        filename = st.session_state.get('filename', 'currículo')
        
        st.markdown("---")
        st.header("📊 Resultados da Análise")
        
        # Nota geral com destaque
        st.subheader("🎯 Avaliação Geral")
        
        score = analysis['overallScore']
        level = get_score_level(score)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.progress(score / 100)
            st.markdown(f"**Resumo:** {analysis['summary']}")
            
            # Barra de contexto
            if score >= 80:
                st.success(f"🎉 Parabéns! Seu currículo está em excelente estado.")
            elif score >= 60:
                st.info(f"👍 Bom currículo! Algumas melhorias podem torná-lo ainda melhor.")
            else:
                st.warning(f"⚠️ Seu currículo precisa de algumas melhorias importantes.")
        
        with col2:
            st.markdown(f"""
            <div class="metric-card {get_score_class(score)}" style="text-align: center;">
                <h1 style="margin: 0; font-size: 2.5rem;">{get_score_color(score)} {score}</h1>
                <p style="margin: 0; font-size: 1.2rem; font-weight: bold;">{level}</p>
                <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">de 100 pontos</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Análise detalhada em abas
        st.markdown("---")
        st.subheader("🔍 Análise Detalhada")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Clareza & Estrutura",
            "🔑 Palavras-chave",
            "💡 Sugestões & Melhorias",
            "📋 Relatório Completo"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            # Análise de Clareza
            with col1:
                st.markdown("### 📝 Clareza e Coesão")
                clarity_score = analysis['clarity']['score']
                
                st.progress(clarity_score / 100)
                st.markdown(f"""
                **Pontuação:** {get_score_color(clarity_score)} **{clarity_score}/100** ({get_score_level(clarity_score)})
                
                **Análise:**
                {analysis['clarity']['feedback']}
                """)
                
                st.markdown("**💡 Sugestões de Melhoria:**")
                for i, suggestion in enumerate(analysis['clarity']['suggestions'], 1):
                    st.markdown(f"""
                    <div class="suggestion-box">
                        <strong>{i}.</strong> {suggestion}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Análise de Estrutura
            with col2:
                st.markdown("### 🏗️ Estrutura e Organização")
                structure_score = analysis['structure']['score']
                
                st.progress(structure_score / 100)
                st.markdown(f"""
                **Pontuação:** {get_score_color(structure_score)} **{structure_score}/100** ({get_score_level(structure_score)})
                
                **Análise:**
                {analysis['structure']['feedback']}
                """)
                
                st.markdown("**💡 Sugestões de Melhoria:**")
                for i, suggestion in enumerate(analysis['structure']['suggestions'], 1):
                    st.markdown(f"""
                    <div class="suggestion-box">
                        <strong>{i}.</strong> {suggestion}
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 🔑 Análise de Palavras-chave")
            
            keywords_score = analysis['keywords']['score']
            st.progress(keywords_score / 100)
            st.markdown(f"**Pontuação:** {get_score_color(keywords_score)} **{keywords_score}/100** ({get_score_level(keywords_score)})")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ✅ Palavras-chave Identificadas")
                if analysis['keywords']['present']:
                    for keyword in analysis['keywords']['present']:
                        st.markdown(f"🟢 **{keyword}**")
                else:
                    st.info("Nenhuma palavra-chave relevante identificada")
            
            with col2:
                st.markdown("#### ❌ Palavras-chave Ausentes")
                if analysis['keywords']['missing']:
                    for keyword in analysis['keywords']['missing']:
                        st.markdown(f"🔴 **{keyword}**")
                else:
                    st.success("Todas as palavras-chave importantes estão presentes!")
            
            st.markdown("---")
            st.markdown("#### 💡 Recomendações para Palavras-chave")
            for i, suggestion in enumerate(analysis['keywords']['suggestions'], 1):
                st.markdown(f"""
                <div class="suggestion-box">
                    <strong>🔑 {i}.</strong> {suggestion}
                </div>
                """, unsafe_allow_html=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ⭐ Pontos Fortes Identificados")
                for i, strength in enumerate(analysis['strengths'], 1):
                    st.markdown(f"""
                    <div class="strength-box">
                        <strong>✅ {i}.</strong> {strength}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 🔧 Oportunidades de Melhoria")
                for i, improvement in enumerate(analysis['improvements'], 1):
                    st.markdown(f"""
                    <div class="improvement-box">
                        <strong>🔧 {i}.</strong> {improvement}
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### 📋 Relatório Completo para Download")
            
            # Gerar relatório detalhado
            report = f"""
RELATÓRIO DE ANÁLISE DE CURRÍCULO - SmartCV
{'='*60}

📄 INFORMAÇÕES GERAIS
Data da Análise: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
Arquivo Analisado: {filename}
Powered by: Google Gemini AI

🎯 AVALIAÇÃO GERAL
Nota Final: {analysis['overallScore']}/100 ({get_score_level(analysis['overallScore'])})

Resumo Executivo:
{analysis['summary']}

{'='*60}
📊 ANÁLISE DETALHADA POR CRITÉRIO
{'='*60}

📝 CLAREZA E COESÃO: {analysis['clarity']['score']}/100 ({get_score_level(analysis['clarity']['score'])})
{'-'*40}
{analysis['clarity']['feedback']}

💡 Sugestões de Melhoria:
{chr(10).join([f"   • {s}" for s in analysis['clarity']['suggestions']])}

🏗️ ESTRUTURA E ORGANIZAÇÃO: {analysis['structure']['score']}/100 ({get_score_level(analysis['structure']['score'])})
{'-'*40}
{analysis['structure']['feedback']}

💡 Sugestões de Melhoria:
{chr(10).join([f"   • {s}" for s in analysis['structure']['suggestions']])}

🔑 PALAVRAS-CHAVE E RELEVÂNCIA: {analysis['keywords']['score']}/100 ({get_score_level(analysis['keywords']['score'])})
{'-'*40}

✅ Palavras-chave Identificadas:
{chr(10).join([f"   • {k}" for k in analysis['keywords']['present']]) if analysis['keywords']['present'] else "   • Nenhuma palavra-chave relevante identificada"}

❌ Palavras-chave Ausentes (Recomendadas):
{chr(10).join([f"   • {k}" for k in analysis['keywords']['missing']]) if analysis['keywords']['missing'] else "   • Todas as palavras-chave importantes estão presentes"}

💡 Recomendações:
{chr(10).join([f"   • {s}" for s in analysis['keywords']['suggestions']])}

{'='*60}
⭐ PONTOS FORTES IDENTIFICADOS
{'='*60}
{chr(10).join([f"✅ {s}" for s in analysis['strengths']])}

{'='*60}
🔧 OPORTUNIDADES DE MELHORIA
{'='*60}
{chr(10).join([f"🔧 {s}" for s in analysis['improvements']])}

{'='*60}
📈 RECOMENDAÇÕES FINAIS
{'='*60}

Com base na análise realizada pelo Google Gemini, seu currículo recebeu a nota {analysis['overallScore']}/100.

{
"Parabéns! Seu currículo está muito bem estruturado. Continue refinando os detalhes para mantê-lo sempre atualizado." if analysis['overallScore'] >= 80
else "Seu currículo tem uma boa base. Implemente as sugestões apresentadas para melhorar sua competitividade no mercado." if analysis['overallScore'] >= 60
else "Recomendamos focar nas melhorias sugeridas, especialmente nas áreas com menor pontuação. Um currículo bem otimizado pode fazer toda a diferença no processo seletivo."
}

Lembre-se:
• Mantenha seu currículo sempre atualizado
• Adapte-o para cada vaga específica
• Use palavras-chave relevantes para sua área
• Mantenha a formatação limpa e profissional
• Destaque suas conquistas com dados quantitativos

---
Relatório gerado automaticamente pelo SmartCV
Analisador de Currículos com Inteligência Artificial
Powered by Google Gemini | Desenvolvido com Streamlit

Para mais análises, visite: https://smartcv.streamlit.app
            """
            
            # Mostrar preview do relatório
            st.text_area(
                "Preview do Relatório:",
                report,
                height=400,
                disabled=True
            )
            
            # Botões de download
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📥 Baixar Relatório Completo (.txt)",
                    data=report,
                    file_name=f"SmartCV_Relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # Relatório resumido
                summary_report = f"""
SMARTCV - RELATÓRIO RESUMIDO
Data: {datetime.now().strftime('%d/%m/%Y')}
Arquivo: {filename}

NOTA GERAL: {analysis['overallScore']}/100

PONTUAÇÕES:
• Clareza: {analysis['clarity']['score']}/100
• Estrutura: {analysis['structure']['score']}/100  
• Palavras-chave: {analysis['keywords']['score']}/100

PRINCIPAIS MELHORIAS:
{chr(10).join([f"• {s}" for s in analysis['improvements'][:3]])}

Powered by Google Gemini
                """
                
                st.download_button(
                    label="📄 Baixar Resumo (.txt)",
                    data=summary_report,
                    file_name=f"SmartCV_Resumo_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p><strong>SmartCV - Analisador de Currículos com IA</strong></p>
        <p>Powered by <span class="gemini-badge">Google Gemini</span> | Desenvolvido com ❤️ usando Streamlit</p>
        <p><em>Transformando currículos com Inteligência Artificial</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
