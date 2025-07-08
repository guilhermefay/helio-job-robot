"""
Frontend de Teste - Sistema HELIO
Interface simples para testar Agentes 0 e 1 com implementações reais
"""

import streamlit as st
import asyncio
import sys
import os
import tempfile
from datetime import datetime
import json

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.services.document_processor import DocumentProcessor
from core.services.ai_validator import AIValidator
from core.services.job_scraper import JobScraper

# Configuração da página
st.set_page_config(
    page_title="HELIO - Teste dos Agentes",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .agent-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .success-box {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 1rem;
        background-color: #e8f5e8;
        color: #2e7d32;
    }
    .error-box {
        border: 2px solid #f44336;
        border-radius: 5px;
        padding: 1rem;
        background-color: #ffeaea;
        color: #c62828;
    }
    .info-box {
        border: 2px solid #2196F3;
        border-radius: 5px;
        padding: 1rem;
        background-color: #e3f2fd;
        color: #1565c0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🚀 HELIO - Sistema de Carreira Meteórica</h1>
        <p>Teste das Implementações Reais - Metodologia Carolina Martins</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Status das APIs
        st.subheader("🔌 Status das APIs")
        
        openai_key = os.getenv('OPENAI_API_KEY', '')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
        
        if openai_key and openai_key != 'your_openai_api_key_here':
            st.success("✅ OpenAI configurada")
        else:
            st.warning("⚠️ OpenAI não configurada")
            
        if anthropic_key and anthropic_key != 'your_anthropic_api_key_here':
            st.success("✅ Anthropic configurada")
        else:
            st.warning("⚠️ Anthropic não configurada")
        
        if not (openai_key and openai_key != 'your_openai_api_key_here') and not (anthropic_key and anthropic_key != 'your_anthropic_api_key_here'):
            st.error("❌ Nenhuma API de IA configurada. Sistema usará fallbacks.")

    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["🩺 Agente 0 - Diagnóstico", "🔍 Agente 1 - MPC", "📊 Resultados Integrados"])
    
    with tab1:
        testar_agente_0()
    
    with tab2:
        testar_agente_1()
    
    with tab3:
        testar_integracao()

def testar_agente_0():
    """Interface para testar o Agente 0 - Diagnóstico"""
    
    st.header("🩺 Agente 0 - Diagnóstico e Onboarding")
    st.markdown("**Teste o processamento real de currículos seguindo a metodologia Carolina Martins**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Upload de Currículo")
        
        # Upload de arquivo
        uploaded_file = st.file_uploader(
            "Escolha um arquivo de currículo",
            type=['pdf', 'docx', 'doc'],
            help="Formatos suportados: PDF, DOCX, DOC"
        )
        
        # Opção de texto direto
        st.subheader("✏️ Ou Cole o Texto do Currículo")
        texto_curriculo = st.text_area(
            "Cole o conteúdo do currículo aqui:",
            height=200,
            placeholder="JOÃO SILVA\nEmail: joao@email.com\nObjetivo: Analista de Marketing\n\nExperiência:\n2020-2024 - Analista - Empresa ABC\n- Gerenciei campanhas com ROI de 150%\n- Liderei equipe de 3 pessoas..."
        )
        
        # Botão de análise
        if st.button("🔍 Analisar Currículo", type="primary"):
            if uploaded_file or texto_curriculo.strip():
                processar_curriculo(uploaded_file, texto_curriculo)
            else:
                st.error("Por favor, faça upload de um arquivo ou cole o texto do currículo.")
    
    with col2:
        st.subheader("📋 O que será analisado:")
        st.markdown("""
        **Estrutura Metodológica (13 Passos):**
        - ✅ Dados Pessoais
        - ✅ Objetivo Profissional  
        - ✅ Resumo/Perfil
        - ✅ Experiências Profissionais
        - ✅ Resultados Quantificados
        - ✅ Formação Acadêmica
        - ✅ Idiomas
        - ✅ Competências Técnicas
        - ✅ Outros Conhecimentos
        - ✅ Trabalho Voluntário
        
        **Validações de Honestidade:**
        - 🔍 Consistência de datas
        - 📊 Informações verificáveis
        - 📝 Nível de detalhamento
        - ⚡ Uso de verbos de ação
        
        **Score de Qualidade:**
        - 🎯 Metodologia (40%)
        - 🎨 Formatação (20%)
        - ✅ Honestidade (30%)
        - 🔑 Palavras-chave (10%)
        """)

def processar_curriculo(uploaded_file, texto_curriculo):
    """Processa o currículo usando o Document Processor real"""
    
    with st.spinner("🔄 Processando currículo..."):
        try:
            processor = DocumentProcessor()
            
            # Determina se é arquivo ou texto
            if uploaded_file:
                # Salva arquivo temporariamente
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Extrai texto do arquivo
                texto_extraido = processor.extrair_texto_documento(tmp_path)
                os.unlink(tmp_path)  # Remove arquivo temporário
                
                if not texto_extraido.strip():
                    st.error("❌ Não foi possível extrair texto do arquivo. Verifique se o arquivo não está corrompido.")
                    return
                
                st.success(f"✅ Texto extraído com sucesso! {len(texto_extraido)} caracteres")
                
            else:
                texto_extraido = texto_curriculo
            
            # Análises
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📊 Análise Estrutural")
                estrutura = processor.analisar_estrutura_curriculo(texto_extraido)
                
                # Score geral
                score = estrutura['score_metodologia']
                if score >= 80:
                    cor = "🟢"
                    status = "Excelente"
                elif score >= 60:
                    cor = "🟡"
                    status = "Bom"
                else:
                    cor = "🔴"
                    status = "Necessita melhorias"
                
                st.markdown(f"""
                <div class="success-box">
                    <h3>{cor} Score Metodológico: {score:.1f}%</h3>
                    <p><strong>Status:</strong> {status}</p>
                    <p><strong>Elementos presentes:</strong> {estrutura['elementos_presentes']}/{estrutura['total_elementos']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Elementos encontrados
                st.subheader("✅ Elementos Encontrados")
                for elemento, presente in estrutura['elementos_encontrados'].items():
                    icon = "✅" if presente else "❌"
                    st.write(f"{icon} {elemento.replace('_', ' ').title()}")
                
                if estrutura['elementos_faltando']:
                    st.subheader("⚠️ Elementos Faltando")
                    for elemento in estrutura['elementos_faltando']:
                        st.write(f"• {elemento.replace('_', ' ').title()}")
            
            with col2:
                st.subheader("🔍 Validação de Honestidade")
                honestidade = processor.verificar_honestidade_curriculo(texto_extraido)
                
                # Status de honestidade
                status_items = [
                    ("Datas consistentes", honestidade['datas_consistentes']),
                    ("Informações verificáveis", honestidade['informacoes_verificaveis']),
                    ("Detalhamento adequado", honestidade['nivel_detalhamento_adequado'])
                ]
                
                for label, status in status_items:
                    icon = "✅" if status else "❌"
                    st.write(f"{icon} {label}")
                
                if honestidade['alertas_inconsistencia']:
                    st.subheader("⚠️ Alertas")
                    for alerta in honestidade['alertas_inconsistencia']:
                        st.warning(f"• {alerta}")
                
                # Indicadores específicos
                if 'indicadores' in honestidade:
                    st.subheader("📈 Indicadores")
                    indicadores = honestidade['indicadores']
                    for key, value in indicadores.items():
                        icon = "✅" if value else "❌"
                        label = key.replace('_', ' ').title()
                        st.write(f"{icon} {label}")
            
            # Palavras-chave extraídas
            st.subheader("🔑 Palavras-chave Extraídas")
            palavras = processor.extrair_palavras_chave_curriculo(texto_extraido)
            
            if palavras:
                # Organiza em colunas
                cols = st.columns(3)
                for i, palavra in enumerate(palavras[:15]):  # Mostra até 15 palavras
                    with cols[i % 3]:
                        st.badge(palavra, outline=True)
            else:
                st.info("Nenhuma palavra-chave identificada automaticamente.")
            
            # Análise de formatação
            st.subheader("🎨 Análise de Formatação")
            formatacao = processor.analisar_formatacao_documento(texto_extraido)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Páginas estimadas", f"{formatacao['tamanho_paginas']}")
            with col2:
                st.metric("Total caracteres", formatacao['metricas_texto']['total_caracteres'])
            with col3:
                st.metric("Seções encontradas", formatacao['estrutura_secoes']['total_secoes'])
            
        except Exception as e:
            st.error(f"❌ Erro ao processar currículo: {str(e)}")

def testar_agente_1():
    """Interface para testar o Agente 1 - MPC"""
    
    st.header("🔍 Agente 1 - Mapa de Palavras-Chave (MPC)")
    st.markdown("**Teste a coleta real de vagas e validação com IA seguindo a metodologia Carolina Martins**")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Configuração da Busca")
        
        # Inputs para busca
        area_interesse = st.selectbox(
            "Área de Interesse",
            ["Marketing", "Tecnologia", "Vendas", "Recursos Humanos", "Financeiro", "Logística", "Jurídico"],
            help="Área principal de atuação"
        )
        
        cargo_objetivo = st.text_input(
            "Cargo Objetivo",
            placeholder="Ex: Analista de Marketing Digital",
            help="Cargo específico que você deseja"
        )
        
        total_vagas = st.slider(
            "Total de Vagas a Coletar",
            min_value=10,
            max_value=100,
            value=50,
            step=10,
            help="Quanto mais vagas, melhor a análise (mas demora mais)"
        )
        
        # Configurações avançadas
        with st.expander("🔧 Configurações Avançadas"):
            localizacao = st.text_input("Localização", value="São Paulo, SP")
            testar_ia = st.checkbox("Testar validação com IA", value=True)
            mostrar_detalhes = st.checkbox("Mostrar detalhes da coleta", value=False)
    
    with col2:
        st.subheader("📋 Processo MPC:")
        st.markdown("""
        **1. Coleta de Vagas (Real):**
        - 🌐 Indeed (web scraping)
        - 💼 InfoJobs (web scraping)  
        - 🔍 Catho (web scraping)
        - 💡 LinkedIn Jobs (limitado)
        
        **2. Extração de Palavras-chave:**
        - 🤖 Análise automática das descrições
        - 📝 Categorização (técnica, comportamental, digital)
        - 📊 Ranking por frequência
        
        **3. Validação com IA:**
        - 🧠 OpenAI GPT-3.5-turbo ou
        - 🔮 Anthropic Claude-3-haiku
        - ✅ Aprovação/rejeição inteligente
        - 💡 Sugestões de melhorias
        
        **4. Priorização Final:**
        - 🎯 Essenciais (70%+ das vagas)
        - ⭐ Importantes (40-69%)
        - 📌 Complementares (<40%)
        """)
    
    # Botão para executar
    if st.button("🚀 Executar MPC Completo", type="primary"):
        if cargo_objetivo.strip():
            executar_mpc(area_interesse, cargo_objetivo, localizacao, total_vagas, testar_ia, mostrar_detalhes)
        else:
            st.error("Por favor, informe o cargo objetivo.")

def executar_mpc(area, cargo, localizacao, total_vagas, testar_ia, mostrar_detalhes):
    """Executa o processo MPC completo"""
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Etapa 1: Coleta de Vagas
        status_text.text("🌐 Coletando vagas reais...")
        progress_bar.progress(20)
        
        scraper = JobScraper()
        vagas = scraper.coletar_vagas_multiplas_fontes(
            area_interesse=area,
            cargo_objetivo=cargo,
            localizacao=localizacao,
            total_vagas_desejadas=total_vagas
        )
        
        progress_bar.progress(50)
        
        if not vagas:
            st.error("❌ Nenhuma vaga foi coletada. Verifique sua conexão com a internet.")
            return
        
        # Etapa 2: Extração de Palavras-chave
        status_text.text("🔍 Extraindo palavras-chave...")
        progress_bar.progress(70)
        
        palavras_contador = scraper.extrair_palavras_chave_descricoes(vagas)
        
        # Categoriza palavras
        palavras_por_categoria = categorizar_palavras(palavras_contador)
        
        # Etapa 3: Validação com IA (opcional)
        resultado_ia = None
        if testar_ia and (palavras_por_categoria['tecnica'] or palavras_por_categoria['comportamental']):
            status_text.text("🤖 Validando com IA...")
            progress_bar.progress(90)
            
            try:
                validator = AIValidator()
                resultado_ia = asyncio.run(validator.validar_palavras_chave(
                    palavras_por_categoria=palavras_por_categoria,
                    area=area,
                    cargo=cargo,
                    contexto_vagas=[vaga['descricao'][:200] for vaga in vagas[:3]]
                ))
            except Exception as e:
                st.warning(f"⚠️ Erro na validação IA: {e}")
        
        progress_bar.progress(100)
        status_text.text("✅ MPC concluído!")
        
        # Exibe resultados
        exibir_resultados_mpc(vagas, palavras_contador, palavras_por_categoria, resultado_ia, mostrar_detalhes)
        
    except Exception as e:
        st.error(f"❌ Erro durante execução do MPC: {str(e)}")
        progress_bar.progress(0)

def categorizar_palavras(palavras_contador):
    """Categoriza palavras-chave por tipo"""
    
    # Categorias baseadas na metodologia Carolina Martins
    categorias = {
        'tecnica': ['excel', 'power bi', 'sql', 'python', 'java', 'javascript', 'tableau', 'sap', 'oracle'],
        'comportamental': ['liderança', 'gestão', 'comunicação', 'negociação', 'analítico', 'estratégico', 'proativo', 'criativo'],
        'digital': ['analytics', 'digital', 'online', 'seo', 'sem', 'social media', 'marketing digital', 'e-commerce']
    }
    
    palavras_por_categoria = {
        'tecnica': [],
        'comportamental': [],
        'digital': [],
        'outras': []
    }
    
    for palavra, freq in palavras_contador.items():
        categorizada = False
        for categoria, lista_palavras in categorias.items():
            if any(cat_palavra in palavra.lower() for cat_palavra in lista_palavras):
                palavras_por_categoria[categoria].append(palavra)
                categorizada = True
                break
        
        if not categorizada:
            palavras_por_categoria['outras'].append(palavra)
    
    return palavras_por_categoria

def exibir_resultados_mpc(vagas, palavras_contador, palavras_por_categoria, resultado_ia, mostrar_detalhes):
    """Exibe os resultados do processo MPC"""
    
    st.subheader("📊 Resultados do MPC")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Vagas Coletadas", len(vagas))
    with col2:
        st.metric("Palavras-chave Únicas", len(palavras_contador))
    with col3:
        fontes = set([vaga.get('fonte', 'unknown') for vaga in vagas])
        st.metric("Fontes Utilizadas", len(fontes))
    with col4:
        if resultado_ia:
            st.metric("Aprovadas pela IA", len(resultado_ia.get('aprovadas', [])))
    
    # Distribuição de fontes
    st.subheader("🌐 Distribuição por Fonte")
    fonte_counts = {}
    for vaga in vagas:
        fonte = vaga.get('fonte', 'unknown')
        fonte_counts[fonte] = fonte_counts.get(fonte, 0) + 1
    
    cols = st.columns(len(fonte_counts))
    for i, (fonte, count) in enumerate(fonte_counts.items()):
        with cols[i]:
            st.metric(fonte.title(), count)
    
    # Palavras-chave por categoria
    st.subheader("🔑 Palavras-chave por Categoria")
    
    tabs = st.tabs(["🔧 Técnicas", "🧠 Comportamentais", "💻 Digitais", "📝 Outras"])
    
    categorias = ['tecnica', 'comportamental', 'digital', 'outras']
    for i, categoria in enumerate(categorias):
        with tabs[i]:
            palavras = palavras_por_categoria[categoria][:20]  # Top 20
            if palavras:
                cols = st.columns(4)
                for j, palavra in enumerate(palavras):
                    with cols[j % 4]:
                        freq = palavras_contador.get(palavra, 1)
                        st.button(f"{palavra} ({freq})", key=f"{categoria}_{j}")
            else:
                st.info("Nenhuma palavra encontrada nesta categoria.")
    
    # Resultados da validação IA
    if resultado_ia:
        st.subheader("🤖 Validação com IA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Palavras Aprovadas:**")
            if resultado_ia.get('aprovadas'):
                for palavra in resultado_ia['aprovadas'][:10]:
                    st.success(f"✓ {palavra}")
            else:
                st.info("Nenhuma palavra aprovada.")
        
        with col2:
            st.markdown("**❌ Palavras Rejeitadas:**")
            if resultado_ia.get('rejeitadas'):
                for item in resultado_ia['rejeitadas'][:5]:
                    if isinstance(item, dict):
                        palavra = item.get('palavra', '')
                        motivo = item.get('motivo', '')
                        st.error(f"✗ {palavra} - {motivo}")
                    else:
                        st.error(f"✗ {item}")
            else:
                st.info("Nenhuma palavra rejeitada.")
        
        # Sugestões da IA
        if resultado_ia.get('sugestoes_novas'):
            st.markdown("**💡 Sugestões da IA:**")
            for sugestao in resultado_ia['sugestoes_novas']:
                st.info(f"💡 {sugestao}")
        
        # Metadados
        with st.expander("🔍 Detalhes da Validação IA"):
            st.write(f"**Modelo usado:** {resultado_ia.get('modelo_usado', 'N/A')}")
            st.write(f"**Confiança:** {resultado_ia.get('confianca', 0):.1%}")
            if resultado_ia.get('comentarios'):
                st.write(f"**Comentários:** {resultado_ia['comentarios']}")
    
    # Detalhes das vagas (opcional)
    if mostrar_detalhes:
        with st.expander("📋 Detalhes das Vagas Coletadas"):
            for i, vaga in enumerate(vagas[:10]):  # Mostra apenas 10 primeiras
                st.markdown(f"**{i+1}. {vaga['titulo']}** - {vaga['empresa']}")
                st.markdown(f"*{vaga['localizacao']} | Fonte: {vaga['fonte']}*")
                st.markdown(f"{vaga['descricao'][:200]}...")
                st.markdown("---")

def testar_integracao():
    """Interface para testar integração completa"""
    
    st.header("📊 Resultados Integrados")
    st.markdown("**Visualize como os Agentes 0 e 1 trabalham juntos**")
    
    st.info("🚧 Em desenvolvimento: Esta seção mostrará a integração completa entre análise de CV e MPC para gerar recomendações personalizadas.")
    
    # Placeholder para funcionalidade futura
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Resumo do CV Analisado")
        st.markdown("""
        - Score de qualidade
        - Elementos presentes/faltantes
        - Palavras-chave atuais
        - Gaps identificados
        """)
    
    with col2:
        st.subheader("🔍 Resultado do MPC")
        st.markdown("""
        - Palavras-chave do mercado
        - Validação com IA
        - Priorização por frequência
        - Recomendações específicas
        """)
    
    st.subheader("🎯 Próximas Funcionalidades")
    st.markdown("""
    - **Gap Analysis:** Comparação entre CV atual e mercado
    - **Recomendações Personalizadas:** Sugestões baseadas na metodologia
    - **Roadmap de Melhoria:** Plano de ação estruturado
    - **Export de Resultados:** PDF com análise completa
    """)

if __name__ == "__main__":
    main()