"""
Extrator de palavras-chave com processamento em lotes
"""
import os
import json
import asyncio
import google.generativeai as genai
from typing import List, Dict, Any
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BatchKeywordExtractor:
    def __init__(self):
        # Configurar Gemini
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("✅ Gemini configurado para processamento em lotes")
        else:
            raise ValueError("GOOGLE_API_KEY não configurada")
        
        # Configuração de segurança
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    
    async def extract_keywords_batch(
        self, 
        vagas: List[Dict[str, Any]], 
        cargo: str,
        batch_size: int = 10,
        callback: callable = None
    ) -> Dict[str, Any]:
        """
        Extrai palavras-chave processando vagas em lotes
        
        Args:
            vagas: Lista completa de vagas
            cargo: Cargo objetivo
            batch_size: Tamanho de cada lote (padrão 10)
            callback: Função para reportar progresso
        """
        total_vagas = len(vagas)
        
        print(f"\n🚀 PROCESSAMENTO EM LOTES")
        print(f"📊 Total de vagas: {total_vagas}")
        print(f"📦 Tamanho do lote: {batch_size}")
        print(f"🔢 Total de lotes: {(total_vagas + batch_size - 1) // batch_size}")
        
        # Dividir em lotes
        lotes = []
        for i in range(0, total_vagas, batch_size):
            lote = vagas[i:i + batch_size]
            lotes.append(lote)
        
        # Processar cada lote
        todos_resultados = []
        palavras_consolidadas = Counter()
        
        for idx, lote in enumerate(lotes, 1):
            if callback:
                await callback(f"Processando lote {idx} de {len(lotes)}...")
            
            print(f"\n📦 Processando lote {idx}/{len(lotes)} ({len(lote)} vagas)")
            
            try:
                # Processar lote
                resultado_lote = await self._processar_lote(lote, cargo, idx)
                
                if resultado_lote:
                    todos_resultados.append(resultado_lote)
                    
                    # Consolidar palavras
                    for palavra in resultado_lote.get('palavras', []):
                        termo = palavra['termo']
                        freq = palavra.get('frequencia', 1)
                        palavras_consolidadas[termo] += freq
                
                # Delay entre lotes para evitar rate limit
                if idx < len(lotes):
                    await asyncio.sleep(1)
                    
            except Exception as e:
                print(f"❌ Erro no lote {idx}: {e}")
                continue
        
        # Consolidar resultados finais
        resultado_final = self._consolidar_resultados(
            palavras_consolidadas,
            todos_resultados,
            total_vagas
        )
        
        print(f"\n✅ Processamento concluído!")
        print(f"📊 Total de palavras únicas: {len(palavras_consolidadas)}")
        print(f"🏆 Top 10 palavras mais frequentes:")
        
        for termo, freq in palavras_consolidadas.most_common(10):
            print(f"   • {termo}: {freq} menções")
        
        return resultado_final
    
    async def _processar_lote(self, lote: List[Dict], cargo: str, numero_lote: int) -> Dict:
        """Processa um lote de vagas"""
        
        # Preparar texto do lote
        texto_lote = self._preparar_texto_lote(lote)
        
        # Criar prompt simplificado
        prompt = f"""Analise estas {len(lote)} vagas de {cargo} e extraia palavras-chave técnicas.

{texto_lote}

Retorne APENAS JSON com palavras-chave e suas frequências:
{{"palavras": [{{"termo": "React", "frequencia": 3}}, {{"termo": "JavaScript", "frequencia": 2}}]}}"""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 1000,
                    "candidate_count": 1
                },
                safety_settings=self.safety_settings
            )
            
            # Extrair JSON
            texto = response.text
            texto = texto.replace('```json', '').replace('```', '').strip()
            
            resultado = json.loads(texto)
            print(f"   ✅ Lote {numero_lote}: {len(resultado.get('palavras', []))} palavras extraídas")
            
            return resultado
            
        except Exception as e:
            print(f"   ❌ Erro ao processar lote {numero_lote}: {e}")
            return None
    
    def _preparar_texto_lote(self, lote: List[Dict]) -> str:
        """Prepara texto resumido do lote"""
        textos = []
        
        for i, vaga in enumerate(lote, 1):
            titulo = vaga.get('titulo', '')
            desc = vaga.get('descricao', '')[:200]  # Limitar descrição
            textos.append(f"Vaga {i}: {titulo}. {desc}...")
        
        return "\n".join(textos)
    
    def _consolidar_resultados(
        self, 
        palavras_consolidadas: Counter,
        todos_resultados: List[Dict],
        total_vagas: int
    ) -> Dict:
        """Consolida resultados de todos os lotes"""
        
        # Top 10 palavras mais frequentes
        top_10 = []
        for termo, freq in palavras_consolidadas.most_common(10):
            top_10.append({
                "termo": termo,
                "frequencia": freq,
                "percentual": round((freq / total_vagas) * 100, 1),
                "categoria": self._categorizar_termo(termo)
            })
        
        # Categorizar todas as palavras
        categorias = {
            "linguagens": [],
            "frameworks": [],
            "ferramentas": [],
            "metodologias": [],
            "outros": []
        }
        
        for termo, freq in palavras_consolidadas.items():
            categoria = self._categorizar_termo(termo)
            categorias[categoria].append({
                "termo": termo,
                "frequencia": freq
            })
        
        # Ordenar cada categoria por frequência
        for cat in categorias:
            categorias[cat].sort(key=lambda x: x['frequencia'], reverse=True)
        
        return {
            "success": True,
            "total_vagas_analisadas": total_vagas,
            "total_lotes_processados": len(todos_resultados),
            "total_palavras_unicas": len(palavras_consolidadas),
            "top_10_palavras_chave": top_10,
            "categorias": categorias,
            "timestamp": datetime.now().isoformat(),
            "modelo_usado": "gemini-2.0-flash-exp-batch"
        }
    
    def _categorizar_termo(self, termo: str) -> str:
        """Categoriza um termo"""
        termo_lower = termo.lower()
        
        # Linguagens
        linguagens = ['javascript', 'typescript', 'python', 'java', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'css', 'html', 'sql']
        if any(lang in termo_lower for lang in linguagens):
            return "linguagens"
        
        # Frameworks
        frameworks = ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'nest', 'next', 'nuxt', 'rails', 'laravel']
        if any(fw in termo_lower for fw in frameworks):
            return "frameworks"
        
        # Ferramentas
        ferramentas = ['git', 'docker', 'kubernetes', 'jenkins', 'jira', 'figma', 'vscode', 'postman', 'aws', 'azure', 'gcp']
        if any(tool in termo_lower for tool in ferramentas):
            return "ferramentas"
        
        # Metodologias
        metodologias = ['agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'solid', 'rest', 'api', 'microservices']
        if any(met in termo_lower for met in metodologias):
            return "metodologias"
        
        return "outros"