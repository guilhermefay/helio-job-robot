#!/usr/bin/env python3
"""
Teste real simulando o fluxo completo do Agent 1
"""
import asyncio
import json
from datetime import datetime
from core.services.ai_keyword_extractor import AIKeywordExtractor

# Simular vagas reais coletadas do Indeed
vagas_reais = []

# Vamos criar 100 vagas variadas e realistas
cargos_base = [
    "Desenvolvedor React Pleno",
    "Frontend Developer Senior", 
    "Full Stack Developer",
    "React Native Developer",
    "UI/UX Developer"
]

empresas = [
    "Tech Solutions BR", "Digital Agency", "Startup Fintech",
    "E-commerce Leader", "Software House", "Consultoria TI",
    "Banco Digital", "EdTech Brasil", "HealthTech", "AgTech"
]

# Gerar 100 vagas com variações realistas
for i in range(100):
    cargo_idx = i % len(cargos_base)
    empresa_idx = i % len(empresas)
    
    # Variar requisitos baseado no índice
    requisitos_base = """
Requisitos obrigatórios:
- React.js com Hooks e Context API
- JavaScript ES6+ e/ou TypeScript
- HTML5, CSS3, Responsive Design
- Git e versionamento de código
- Consumo de APIs REST
- Inglês técnico
"""
    
    requisitos_extras = []
    
    # Adicionar requisitos variados
    if i % 2 == 0:
        requisitos_extras.append("- Node.js e Express")
    if i % 3 == 0:
        requisitos_extras.append("- Redux ou MobX para gerenciamento de estado")
    if i % 4 == 0:
        requisitos_extras.append("- Testes unitários com Jest e React Testing Library")
    if i % 5 == 0:
        requisitos_extras.append("- Docker e containerização")
    if i % 6 == 0:
        requisitos_extras.append("- AWS ou Google Cloud Platform")
    if i % 7 == 0:
        requisitos_extras.append("- Next.js ou Gatsby")
    if i % 8 == 0:
        requisitos_extras.append("- GraphQL e Apollo")
    if i % 9 == 0:
        requisitos_extras.append("- CI/CD com Jenkins ou GitHub Actions")
    if i % 10 == 0:
        requisitos_extras.append("- Styled Components ou Emotion")
    
    diferenciais = []
    if i % 3 == 0:
        diferenciais.append("- Experiência com metodologias ágeis (Scrum/Kanban)")
    if i % 4 == 0:
        diferenciais.append("- Conhecimento em React Native")
    if i % 5 == 0:
        diferenciais.append("- Certificações em cloud computing")
    
    descricao = f"""{requisitos_base}
{chr(10).join(requisitos_extras)}

Diferenciais:
{chr(10).join(diferenciais) if diferenciais else '- Experiência em startups'}

Oferecemos:
- Salário competitivo
- Trabalho remoto flexível
- Benefícios completos
- Ambiente colaborativo
"""
    
    vagas_reais.append({
        "titulo": f"{cargos_base[cargo_idx]} - {i+1}",
        "empresa": empresas[empresa_idx],
        "descricao": descricao,
        "data": datetime.now().isoformat()
    })

async def executar_analise():
    """Executa análise completa das vagas"""
    print("🚀 TESTE REAL - ANÁLISE DE 100 VAGAS")
    print("=" * 60)
    print(f"📊 Total de vagas simuladas: {len(vagas_reais)}")
    print(f"🏢 Empresas diferentes: {len(set(v['empresa'] for v in vagas_reais))}")
    print(f"💼 Tipos de cargo: {len(set(v['titulo'].split(' - ')[0] for v in vagas_reais))}")
    
    # Criar extrator
    extrator = AIKeywordExtractor()
    
    print("\n🤖 Iniciando análise com IA...")
    print("⏳ Isso pode levar 1-2 minutos para processar todos os lotes...")
    
    try:
        # Callback para mostrar progresso
        async def mostrar_progresso(msg):
            print(f"   📍 {msg}")
        
        # Executar análise
        inicio = datetime.now()
        resultado = await extrator.extrair_palavras_chave_ia(
            vagas=vagas_reais,
            cargo_objetivo="desenvolvedor react",
            area_interesse="tecnologia frontend",
            callback_progresso=mostrar_progresso
        )
        fim = datetime.now()
        tempo_total = (fim - inicio).total_seconds()
        
        print(f"\n✅ ANÁLISE CONCLUÍDA EM {tempo_total:.1f} SEGUNDOS!")
        print("=" * 60)
        
        # Mostrar metadados
        meta = resultado.get('analise_metadados', {})
        print(f"\n📊 METADADOS DA ANÁLISE:")
        print(f"   Total de vagas: {meta.get('total_vagas', 0)}")
        print(f"   Palavras únicas: {resultado.get('total_palavras_unicas', 0)}")
        print(f"   Modelo usado: {resultado.get('modelo_usado', 'N/A')}")
        print(f"   Data: {meta.get('data_analise', 'N/A')}")
        
        # TOP 10 Palavras-chave
        print(f"\n🏆 TOP 10 PALAVRAS-CHAVE MAIS IMPORTANTES:")
        print("-" * 60)
        print(f"{'Rank':<5} {'Palavra-chave':<20} {'Freq':<6} {'%':<6} {'Categoria':<15}")
        print("-" * 60)
        
        for i, palavra in enumerate(resultado.get('top_10_palavras_chave', [])[:10], 1):
            termo = palavra.get('termo', 'N/A')
            freq = palavra.get('frequencia', 0)
            perc = palavra.get('percentual', 0)
            cat = palavra.get('categoria', 'N/A')
            print(f"{i:<5} {termo:<20} {freq:<6} {perc:<6} {cat:<15}")
        
        # Análise por categoria
        print(f"\n📈 ANÁLISE POR CATEGORIA:")
        categorias = resultado.get('categorias', {})
        
        for categoria, termos in categorias.items():
            if termos and len(termos) > 0:
                print(f"\n🏷️  {categoria.upper()} ({len(termos)} termos):")
                # Mostrar top 5 de cada categoria
                for termo_info in termos[:5]:
                    if isinstance(termo_info, dict):
                        termo = termo_info.get('termo', 'N/A')
                        freq = termo_info.get('frequencia', 0)
                        print(f"   • {termo} ({freq}x)")
                    else:
                        print(f"   • {termo_info}")
                
                if len(termos) > 5:
                    print(f"   ... e mais {len(termos) - 5} termos")
        
        # Insights para o candidato
        print(f"\n💡 INSIGHTS PARA O CANDIDATO:")
        print("-" * 60)
        
        # Identificar skills essenciais (>60%)
        essenciais = [p for p in resultado.get('top_10_palavras_chave', []) 
                      if p.get('percentual', 0) > 60]
        
        if essenciais:
            print(f"\n✅ Skills ESSENCIAIS (presentes em >60% das vagas):")
            for skill in essenciais:
                print(f"   • {skill['termo']} ({skill['percentual']}%)")
        
        # Identificar skills importantes (30-60%)
        importantes = [p for p in resultado.get('top_10_palavras_chave', []) 
                       if 30 <= p.get('percentual', 0) <= 60]
        
        if importantes:
            print(f"\n📌 Skills IMPORTANTES (presentes em 30-60% das vagas):")
            for skill in importantes:
                print(f"   • {skill['termo']} ({skill['percentual']}%)")
        
        # Salvar resultado completo
        output_file = f'analise_completa_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'data_analise': datetime.now().isoformat(),
                    'total_vagas': len(vagas_reais),
                    'tempo_processamento': f"{tempo_total:.1f}s"
                },
                'resultado': resultado
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Análise completa salva em: {output_file}")
        
    except Exception as e:
        print(f"\n❌ ERRO NA ANÁLISE: {type(e).__name__}")
        print(f"   Detalhes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Iniciando teste real do Agent 1...")
    asyncio.run(executar_analise())