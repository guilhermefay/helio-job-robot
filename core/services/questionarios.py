"""
Questionários da Metodologia Carolina Martins

Implementa os questionários de diagnóstico baseados nas transcrições:
1. Questionário de Sabotadores (mencionado na Aula 2)
2. Questionário de Experiência Profissional vs Mercado
3. Questionário de Situação de Carreira
4. Validação de Expectativas (70% de aderência)
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class TipoPergunta(str, Enum):
    ESCALA = "escala"  # 1-5 ou 1-10
    MULTIPLA_ESCOLHA = "multipla_escolha"
    TEXTO_LIVRE = "texto_livre"
    BOOLEAN = "boolean"
    DATA = "data"
    NUMERO = "numero"

class QuestionarioSabotadores:
    """
    Questionário dos Sabotadores baseado na metodologia Carolina Martins
    Identifica padrões limitantes mencionados na Aula 2
    """
    
    @staticmethod
    def get_perguntas() -> Dict[str, Dict[str, Any]]:
        """Retorna perguntas para identificação de sabotadores"""
        return {
            # Hiper-racional
            "q1": {
                "texto": "Tendo dificuldade para tomar decisões porque sempre quero analisar mais dados?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hiper_racional"
            },
            "q2": {
                "texto": "Costumo adiar ações importantes porque quero ter certeza absoluta?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hiper_racional"
            },
            "q3": {
                "texto": "Prefiro analisar a situação do que partir para a ação?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hiper_racional"
            },
            
            # Hiper-realizador (Perfeccionista)
            "q4": {
                "texto": "Sinto que meu trabalho nunca está bom o suficiente?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hiper_realizador"
            },
            "q5": {
                "texto": "Prefiro fazer tudo sozinho para garantir que seja feito corretamente?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hiper_realizador"
            },
            "q6": {
                "texto": "Fico estressado quando não posso controlar todos os detalhes?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hiper_realizador"
            },
            
            # Controlador
            "q7": {
                "texto": "Tenho dificuldade em delegar tarefas importantes?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "controlador"
            },
            "q8": {
                "texto": "Fico ansioso quando não sei como uma situação vai se desenrolar?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "controlador"
            },
            "q9": {
                "texto": "Prefiro liderar a ser liderado?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "controlador"
            },
            
            # Hipervigilante
            "q10": {
                "texto": "Costumo pensar primeiro nos riscos e problemas de uma situação?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hipervigilante"
            },
            "q11": {
                "texto": "Tenho dificuldade em confiar totalmente nas pessoas?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hipervigilante"
            },
            "q12": {
                "texto": "Estou sempre alerta para possíveis ameaças ou problemas?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "hipervigilante"
            },
            
            # Inquieto
            "q13": {
                "texto": "Tenho dificuldade em manter foco em uma tarefa por muito tempo?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "inquieto"
            },
            "q14": {
                "texto": "Gosto de ter várias atividades acontecendo ao mesmo tempo?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "inquieto"
            },
            "q15": {
                "texto": "Fico entediado facilmente com rotinas?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "inquieto"
            },
            
            # Complacente
            "q16": {
                "texto": "Evito conflitos mesmo quando sei que estou certo?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "complacente"
            },
            "q17": {
                "texto": "Prefiro manter a paz do que expressar minha opinião?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "complacente"
            },
            "q18": {
                "texto": "Tenho dificuldade em dizer 'não' para pedidos dos outros?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "complacente"
            },
            
            # Juiz
            "q19": {
                "texto": "Sou muito crítico comigo mesmo quando cometo erros?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "juiz"
            },
            "q20": {
                "texto": "Noto facilmente os defeitos e falhas nas pessoas?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "juiz"
            },
            "q21": {
                "texto": "Tenho padrões muito altos para mim e para os outros?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "juiz"
            },
            
            # Vítima
            "q22": {
                "texto": "Sinto que as coisas ruins sempre acontecem comigo?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "vitima"
            },
            "q23": {
                "texto": "Acredito que fatores externos são responsáveis pelos meus problemas?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "vitima"
            },
            "q24": {
                "texto": "Sinto que não tenho controle sobre os resultados da minha vida?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "vitima"
            },
            
            # Agradador
            "q25": {
                "texto": "Preciso que todos gostem de mim?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "agradador"
            },
            "q26": {
                "texto": "Mudo meu comportamento dependendo de com quem estou?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "agradador"
            },
            "q27": {
                "texto": "Fico muito incomodado quando alguém não gosta de mim?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "agradador"
            },
            
            # Evitador
            "q28": {
                "texto": "Deixo para depois tarefas que considero difíceis ou desagradáveis?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "evitador"
            },
            "q29": {
                "texto": "Evito situações onde posso ser rejeitado ou criticado?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "evitador"
            },
            "q30": {
                "texto": "Prefiro ficar na zona de conforto a arriscar coisas novas?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 5, "labels": ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]},
                "sabotador": "evitador"
            }
        }

class QuestionarioExperiencia:
    """
    Questionário de Experiência baseado na distinção Carolina Martins:
    - Experiência Profissional (específica da área)
    - Experiência de Mercado (total)
    """
    
    @staticmethod
    def get_perguntas() -> Dict[str, Dict[str, Any]]:
        """Retorna perguntas sobre experiência profissional"""
        return {
            "exp_1": {
                "texto": "Qual sua área de atuação principal atualmente?",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"min_length": 2, "max_length": 100}
            },
            "exp_2": {
                "texto": "Qual área você gostaria de atuar (objetivo de carreira)?",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"min_length": 2, "max_length": 100}
            },
            "exp_3": {
                "texto": "Há quanto tempo você está no mercado de trabalho (total, incluindo todas as áreas)?",
                "tipo": TipoPergunta.NUMERO.value,
                "unidade": "anos",
                "obrigatorio": True,
                "validacao": {"min": 0, "max": 50}
            },
            "exp_4": {
                "texto": "Há quanto tempo você atua especificamente na sua área atual?",
                "tipo": TipoPergunta.NUMERO.value,
                "unidade": "anos",
                "obrigatorio": True,
                "validacao": {"min": 0, "max": 50}
            },
            "exp_5": {
                "texto": "Qual seu cargo atual?",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"min_length": 2, "max_length": 100}
            },
            "exp_6": {
                "texto": "Qual cargo você gostaria de atingir?",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"min_length": 2, "max_length": 100}
            },
            "exp_7": {
                "texto": "Qual sua situação atual de emprego?",
                "tipo": TipoPergunta.MULTIPLA_ESCOLHA.value,
                "opcoes": [
                    {"valor": "empregado", "texto": "Empregado CLT"},
                    {"valor": "freelancer", "texto": "Freelancer/Consultor"},
                    {"valor": "desempregado", "texto": "Desempregado"},
                    {"valor": "estudante", "texto": "Estudante"},
                    {"valor": "empreendedor", "texto": "Empreendedor"}
                ],
                "obrigatorio": True
            },
            "exp_8": {
                "texto": "Como você avalia sua satisfação no emprego atual? (1-10)",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 10, "labels": ["Muito insatisfeito", "Muito satisfeito"]},
                "condicao": {"campo": "exp_7", "valor": "empregado"}
            },
            "exp_9": {
                "texto": "Há quanto tempo você está fora do mercado de trabalho?",
                "tipo": TipoPergunta.NUMERO.value,
                "unidade": "meses",
                "validacao": {"min": 0, "max": 120},
                "condicao": {"campo": "exp_7", "valor": "desempregado"}
            },
            "exp_10": {
                "texto": "Qual o principal motivo para mudança de emprego?",
                "tipo": TipoPergunta.MULTIPLA_ESCOLHA.value,
                "opcoes": [
                    {"valor": "crescimento", "texto": "Crescimento profissional"},
                    {"valor": "salario", "texto": "Melhoria salarial"},
                    {"valor": "insatisfacao", "texto": "Insatisfação atual"},
                    {"valor": "mudanca_area", "texto": "Mudança de área"},
                    {"valor": "localizacao", "texto": "Mudança de localização"},
                    {"valor": "empresa", "texto": "Busca por empresa melhor"},
                    {"valor": "desafio", "texto": "Novos desafios"}
                ],
                "obrigatorio": True
            }
        }

class QuestionarioExpectativas:
    """
    Questionário para validar expectativas baseado no critério dos 70%
    mencionado por Carolina Martins
    """
    
    @staticmethod
    def get_perguntas() -> Dict[str, Dict[str, Any]]:
        """Retorna perguntas para alinhamento de expectativas"""
        return {
            "exp_1": {
                "texto": "Você tem pelo menos 70% dos requisitos técnicos que normalmente são pedidos para o cargo que deseja?",
                "tipo": TipoPergunta.ESCALA.value,
                "escala": {"min": 1, "max": 10, "labels": ["0-10%", "90-100%"]},
                "obrigatorio": True
            },
            "exp_2": {
                "texto": "Quanto tempo você está disposto a investir na busca por uma nova oportunidade?",
                "tipo": TipoPergunta.MULTIPLA_ESCOLHA.value,
                "opcoes": [
                    {"valor": "1_mes", "texto": "Até 1 mês"},
                    {"valor": "3_meses", "texto": "Até 3 meses"},
                    {"valor": "6_meses", "texto": "Até 6 meses"},
                    {"valor": "1_ano", "texto": "Até 1 ano"},
                    {"valor": "sem_pressa", "texto": "Sem pressa definida"}
                ],
                "obrigatorio": True
            },
            "exp_3": {
                "texto": "Qual sua disponibilidade para estudar/se capacitar durante o processo?",
                "tipo": TipoPergunta.MULTIPLA_ESCOLHA.value,
                "opcoes": [
                    {"valor": "sem_tempo", "texto": "Não tenho tempo"},
                    {"valor": "1_hora_dia", "texto": "1 hora por dia"},
                    {"valor": "2_horas_dia", "texto": "2 horas por dia"},
                    {"valor": "fins_semana", "texto": "Apenas fins de semana"},
                    {"valor": "integral", "texto": "Dedicação integral"}
                ],
                "obrigatorio": True
            },
            "exp_4": {
                "texto": "Orçamento disponível para investimento em cursos/certificações (R$)?",
                "tipo": TipoPergunta.NUMERO.value,
                "validacao": {"min": 0, "max": 50000},
                "obrigatorio": False
            },
            "exp_5": {
                "texto": "Você está disposto a aceitar um cargo de nível inferior ao objetivo para ganhar experiência na área?",
                "tipo": TipoPergunta.BOOLEAN.value,
                "obrigatorio": True
            },
            "exp_6": {
                "texto": "Flexibilidade geográfica - estaria disposto a se mudar?",
                "tipo": TipoPergunta.MULTIPLA_ESCOLHA.value,
                "opcoes": [
                    {"valor": "nao", "texto": "Não, apenas na minha cidade"},
                    {"valor": "mesmo_estado", "texto": "Dentro do mesmo estado"},
                    {"valor": "brasil", "texto": "Qualquer lugar do Brasil"},
                    {"valor": "exterior", "texto": "Brasil ou exterior"}
                ],
                "obrigatorio": True
            },
            "exp_7": {
                "texto": "Preferência de regime de trabalho?",
                "tipo": TipoPergunta.MULTIPLA_ESCOLHA.value,
                "opcoes": [
                    {"valor": "presencial", "texto": "Presencial"},
                    {"valor": "hibrido", "texto": "Híbrido"},
                    {"valor": "remoto", "texto": "Remoto"},
                    {"valor": "flexivel", "texto": "Flexível"}
                ],
                "obrigatorio": True
            }
        }

class QuestionarioDetalhado:
    """
    Questionário detalhado para coleta completa de informações
    baseado na metodologia Carolina Martins
    """
    
    @staticmethod
    def get_perguntas_completas() -> Dict[str, Dict[str, Any]]:
        """Retorna questionário completo estruturado"""
        questionario = {}
        
        # Seção 1: Dados Básicos
        questionario.update({
            "nome": {
                "secao": "dados_basicos",
                "texto": "Nome completo",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"min_length": 2, "max_length": 255}
            },
            "email": {
                "secao": "dados_basicos", 
                "texto": "Email profissional",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"}
            },
            "telefone": {
                "secao": "dados_basicos",
                "texto": "Telefone com DDD",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"pattern": r"^\(\d{2}\)\s\d{4,5}-\d{4}$"}
            },
            "linkedin": {
                "secao": "dados_basicos",
                "texto": "URL do LinkedIn",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True,
                "validacao": {"pattern": r"^https://[a-z]{2,3}\.linkedin\.com/in/.*"}
            },
            "cidade": {
                "secao": "dados_basicos",
                "texto": "Cidade",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True
            },
            "estado": {
                "secao": "dados_basicos",
                "texto": "Estado",
                "tipo": TipoPergunta.TEXTO_LIVRE.value,
                "obrigatorio": True
            }
        })
        
        # Seção 2: Experiência (Carolina Martins)
        questionario.update(QuestionarioExperiencia.get_perguntas())
        
        # Seção 3: Sabotadores
        questionario.update(QuestionarioSabotadores.get_perguntas())
        
        # Seção 4: Expectativas
        questionario.update(QuestionarioExpectativas.get_perguntas())
        
        return questionario
    
    @staticmethod
    def validar_respostas(respostas: Dict[str, Any]) -> Dict[str, List[str]]:
        """Valida respostas do questionário"""
        erros = {}
        perguntas = QuestionarioDetalhado.get_perguntas_completas()
        
        for pergunta_id, config in perguntas.items():
            resposta = respostas.get(pergunta_id)
            erros_pergunta = []
            
            # Verifica obrigatoriedade
            if config.get("obrigatorio", False) and not resposta:
                erros_pergunta.append("Campo obrigatório")
                continue
            
            # Pula validação se não obrigatório e vazio
            if not resposta and not config.get("obrigatorio", False):
                continue
            
            # Validações específicas por tipo
            tipo = config["tipo"]
            validacao = config.get("validacao", {})
            
            if tipo == TipoPergunta.TEXTO_LIVRE.value:
                if "min_length" in validacao and len(str(resposta)) < validacao["min_length"]:
                    erros_pergunta.append(f"Mínimo {validacao['min_length']} caracteres")
                if "max_length" in validacao and len(str(resposta)) > validacao["max_length"]:
                    erros_pergunta.append(f"Máximo {validacao['max_length']} caracteres")
                if "pattern" in validacao:
                    import re
                    if not re.match(validacao["pattern"], str(resposta)):
                        erros_pergunta.append("Formato inválido")
            
            elif tipo == TipoPergunta.NUMERO.value:
                try:
                    valor = float(resposta)
                    if "min" in validacao and valor < validacao["min"]:
                        erros_pergunta.append(f"Valor mínimo: {validacao['min']}")
                    if "max" in validacao and valor > validacao["max"]:
                        erros_pergunta.append(f"Valor máximo: {validacao['max']}")
                except ValueError:
                    erros_pergunta.append("Deve ser um número")
            
            elif tipo == TipoPergunta.ESCALA.value:
                try:
                    valor = int(resposta)
                    escala = config.get("escala", {})
                    if valor < escala.get("min", 1) or valor > escala.get("max", 5):
                        erros_pergunta.append(f"Valor deve estar entre {escala.get('min', 1)} e {escala.get('max', 5)}")
                except ValueError:
                    erros_pergunta.append("Deve ser um número inteiro")
            
            elif tipo == TipoPergunta.MULTIPLA_ESCOLHA.value:
                opcoes_validas = [op["valor"] for op in config.get("opcoes", [])]
                if resposta not in opcoes_validas:
                    erros_pergunta.append("Opção inválida")
            
            # Adiciona erros se houver
            if erros_pergunta:
                erros[pergunta_id] = erros_pergunta
        
        return erros
    
    @staticmethod
    def calcular_completude(respostas: Dict[str, Any]) -> float:
        """Calcula percentual de completude do questionário"""
        perguntas = QuestionarioDetalhado.get_perguntas_completas()
        total_perguntas = len(perguntas)
        respondidas = sum(1 for pid in perguntas.keys() if respostas.get(pid))
        
        return (respondidas / total_perguntas) * 100 if total_perguntas > 0 else 0.0