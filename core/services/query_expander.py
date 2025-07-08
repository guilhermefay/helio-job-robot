"""
Query Expander V2 - Sistema HELIO
Expansão inteligente de queries com foco em produção
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class QueryExpanderV2:
    """
    Expande queries de cargo de forma inteligente e contextual
    """
    
    def __init__(self):
        # Base de conhecimento de expansões
        self.expansoes_base = {
            # Tecnologia
            "desenvolvedor": [
                "Software Engineer",
                "Desenvolvedor de Software",
                "Full Stack Developer",
                "Backend Developer",
                "Frontend Developer",
                "Engenheiro de Software",
                "Software Developer",
                "Programador"
            ],
            "analista": [
                "Analista de Sistemas",
                "Systems Analyst",
                "Business Analyst",
                "Analista de Negócios",
                "Data Analyst",
                "Analista de Dados",
                "Analista de TI"
            ],
            "devops": [
                "DevOps Engineer",
                "Site Reliability Engineer",
                "SRE",
                "Infrastructure Engineer",
                "Cloud Engineer",
                "Platform Engineer"
            ],
            "data": [
                "Data Scientist",
                "Data Engineer",
                "Analytics Engineer",
                "Machine Learning Engineer",
                "ML Engineer",
                "BI Analyst",
                "Business Intelligence"
            ],
            
            # Gestão
            "gerente": [
                "Manager",
                "Gerente de Projetos",
                "Project Manager",
                "Product Manager",
                "Team Lead",
                "Tech Lead",
                "Coordenador"
            ],
            "coordenador": [
                "Coordinator",
                "Team Lead",
                "Supervisor",
                "Líder de Equipe",
                "Gestor"
            ],
            
            # Marketing
            "marketing": [
                "Marketing Analyst",
                "Digital Marketing",
                "Growth Marketing",
                "Marketing Manager",
                "Social Media Manager",
                "Content Marketing",
                "Performance Marketing"
            ],
            
            # Design
            "designer": [
                "UX Designer",
                "UI Designer",
                "Product Designer",
                "UX/UI Designer",
                "Visual Designer",
                "Web Designer",
                "Graphic Designer"
            ],
            
            # Vendas
            "vendas": [
                "Sales Executive",
                "Account Executive",
                "Business Development",
                "Sales Representative",
                "Inside Sales",
                "Vendedor",
                "Consultor de Vendas"
            ],
            
            # Suporte/Atendimento
            "suporte": [
                "Support Analyst",
                "Customer Success",
                "Technical Support",
                "Help Desk",
                "Service Desk",
                "Customer Support"
            ]
        }
        
        # Modificadores por nível
        self.niveis = {
            "junior": ["Junior", "Jr", "Entry Level", "Júnior", "Trainee", "Estágio"],
            "pleno": ["Pleno", "Mid Level", "Mid-Level", "Intermediate"],
            "senior": ["Senior", "Sr", "Sênior", "Lead", "Principal", "Staff"]
        }
        
        # Mapeamento área -> termos relacionados
        self.termos_por_area = {
            "tecnologia": ["Tech", "IT", "Software", "Digital", "Development"],
            "marketing": ["Marketing", "Growth", "Digital", "Brand", "Content"],
            "vendas": ["Sales", "Commercial", "Business", "Revenue"],
            "financeiro": ["Finance", "Financial", "Accounting", "Treasury"],
            "rh": ["HR", "People", "Talent", "Human Resources"],
            "operacoes": ["Operations", "Ops", "Process", "Supply Chain"]
        }
    
    def expandir_cargo(self, cargo: str, area: str = "") -> List[str]:
        """
        Expande um cargo em múltiplas variações relevantes
        
        Args:
            cargo: Cargo original (ex: "desenvolvedor")
            area: Área de atuação para contexto adicional
            
        Returns:
            Lista de variações do cargo ordenadas por relevância
        """
        cargo_lower = cargo.lower().strip()
        expansoes = set()
        
        # 1. Adicionar cargo original
        expansoes.add(cargo)
        
        # 2. Buscar expansões diretas
        for termo_base, variacoes in self.expansoes_base.items():
            if termo_base in cargo_lower:
                expansoes.update(variacoes)
                
                # Se encontrou match, também adicionar com níveis
                nivel_detectado = self._detectar_nivel(cargo_lower)
                if not nivel_detectado:
                    # Adicionar principais níveis se não especificado
                    for variacao in variacoes[:3]:  # Top 3 variações
                        expansoes.add(f"{variacao} Pleno")
                        expansoes.add(f"{variacao} Senior")
                break
        
        # 3. Se não encontrou expansão direta, criar variações genéricas
        if len(expansoes) <= 1:
            base = cargo.replace("junior", "").replace("pleno", "").replace("senior", "").strip()
            
            # Variações em português
            expansoes.update([
                base,
                f"Especialista em {base}",
                f"Analista de {base}",
                f"Consultor de {base}"
            ])
            
            # Variações em inglês se aplicável
            if area and area.lower() in ["tecnologia", "tech", "ti"]:
                expansoes.update([
                    f"{base} Engineer",
                    f"{base} Developer",
                    f"{base} Specialist"
                ])
        
        # 4. Adicionar termos específicos da área
        if area:
            area_lower = area.lower()
            termos_area = self.termos_por_area.get(area_lower, [])
            
            # Combinar com termos da área
            base_limpo = cargo.split()[0] if ' ' in cargo else cargo
            for termo in termos_area[:2]:  # Top 2 termos da área
                expansoes.add(f"{termo} {base_limpo}")
        
        # 5. Remover duplicatas e ordenar por relevância
        expansoes_lista = list(expansoes)
        
        # Priorizar: cargo original primeiro, depois mais específicos
        if cargo in expansoes_lista:
            expansoes_lista.remove(cargo)
            expansoes_lista.insert(0, cargo)
        
        # Limitar quantidade para otimizar buscas
        return expansoes_lista[:15]
    
    def _detectar_nivel(self, cargo: str) -> str:
        """
        Detecta o nível de senioridade no cargo
        """
        cargo_lower = cargo.lower()
        
        for nivel, termos in self.niveis.items():
            for termo in termos:
                if termo.lower() in cargo_lower:
                    return nivel
        
        return ""
    
    def sugerir_cargos_relacionados(self, cargo: str, limite: int = 5) -> List[str]:
        """
        Sugere cargos relacionados para ampliar a busca
        
        Args:
            cargo: Cargo base
            limite: Quantidade máxima de sugestões
            
        Returns:
            Lista de cargos relacionados
        """
        sugestoes = []
        cargo_lower = cargo.lower()
        
        # Mapeamento de cargos relacionados
        relacoes = {
            "desenvolvedor": ["arquiteto de software", "tech lead", "engenheiro de dados"],
            "analista": ["coordenador", "especialista", "consultor"],
            "designer": ["diretor de arte", "ux researcher", "product designer"],
            "gerente": ["diretor", "head", "coordenador"],
            "vendedor": ["account manager", "business development", "customer success"]
        }
        
        for base, relacionados in relacoes.items():
            if base in cargo_lower:
                sugestoes.extend(relacionados)
                break
        
        return sugestoes[:limite]