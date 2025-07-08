"""
Query Expander - Sistema HELIO
Expande queries genéricas para melhorar a coleta de vagas
"""

from typing import List, Dict, Any

class QueryExpander:
    """
    Expande queries genéricas em múltiplas variações
    para melhorar a coleta de vagas
    """
    
    def __init__(self):
        # Dicionário de expansões por termo genérico
        self.expansoes = {
            "desenvolvedor": [
                "Desenvolvedor de Software",
                "Desenvolvedor Full Stack",
                "Desenvolvedor Backend",
                "Desenvolvedor Frontend",
                "Software Engineer",
                "Engenheiro de Software",
                "Programador",
                "Developer"
            ],
            "analista": [
                "Analista de Sistemas",
                "Analista de Negócios",
                "Analista de Dados",
                "Business Analyst",
                "Data Analyst",
                "Analista de TI",
                "Analista de Processos"
            ],
            "gestor": [
                "Gerente de Projetos",
                "Project Manager",
                "Coordenador",
                "Supervisor",
                "Team Lead",
                "Líder Técnico"
            ],
            "designer": [
                "Designer UX/UI",
                "Product Designer",
                "UX Designer",
                "UI Designer",
                "Designer Gráfico",
                "Web Designer"
            ],
            "marketing": [
                "Analista de Marketing",
                "Marketing Digital",
                "Social Media",
                "Growth Marketing",
                "Marketing Manager",
                "Especialista em Marketing"
            ],
            "vendas": [
                "Vendedor",
                "Executivo de Vendas",
                "Sales Executive",
                "Account Executive",
                "Consultor de Vendas",
                "Representante Comercial"
            ],
            "suporte": [
                "Suporte Técnico",
                "Help Desk",
                "Service Desk",
                "Analista de Suporte",
                "Technical Support",
                "Customer Success"
            ]
        }
        
        # Localizações padrão para o Brasil
        self.localizacoes_brasil = [
            "Brasil",
            "São Paulo, SP",
            "Rio de Janeiro, RJ",
            "Belo Horizonte, MG",
            "Porto Alegre, RS",
            "Curitiba, PR",
            "Brasília, DF",
            "Salvador, BA",
            "Recife, PE",
            "Fortaleza, CE",
            "Remote - Brazil",
            "Remoto - Brasil"
        ]
    
    def expandir_query(self, cargo: str, area_interesse: str = "") -> List[str]:
        """
        Expande uma query genérica em múltiplas variações
        
        Args:
            cargo: Cargo original (ex: "desenvolvedor")
            area_interesse: Área de interesse adicional
            
        Returns:
            Lista de variações da query
        """
        cargo_lower = cargo.lower().strip()
        queries = []
        
        # Verifica se há expansão direta
        for termo_generico, expansoes in self.expansoes.items():
            if termo_generico in cargo_lower:
                queries.extend(expansoes)
                break
        
        # Se não encontrou expansão, usa variações do cargo original
        if not queries:
            queries = [
                cargo,
                f"{cargo} Júnior",
                f"{cargo} Pleno",
                f"{cargo} Sênior",
                f"{cargo} Senior",
                f"{cargo} Jr",
                f"{cargo} Pl",
                f"{cargo} Sr"
            ]
        
        # Adiciona área de interesse se fornecida
        if area_interesse:
            area_lower = area_interesse.lower()
            
            # Expansões específicas por área
            if "tecnologia" in area_lower or "ti" in area_lower:
                if "desenvolvedor" in cargo_lower:
                    queries.extend([
                        "Software Developer",
                        "Full Stack Developer",
                        "Backend Developer",
                        "Frontend Developer",
                        "Web Developer",
                        "Mobile Developer"
                    ])
            elif "dados" in area_lower:
                queries.extend([
                    "Data Scientist",
                    "Data Engineer",
                    "Data Analyst",
                    "Business Intelligence",
                    "BI Analyst"
                ])
        
        # Remove duplicatas mantendo a ordem
        seen = set()
        unique_queries = []
        for q in queries:
            if q.lower() not in seen:
                seen.add(q.lower())
                unique_queries.append(q)
        
        return unique_queries[:10]  # Limita a 10 queries
    
    def expandir_localizacao(self, localizacao: str) -> List[str]:
        """
        Expande localização para incluir variações
        
        Args:
            localizacao: Localização original
            
        Returns:
            Lista de localizações expandidas
        """
        if not localizacao or localizacao.lower() in ["", "brasil", "brazil"]:
            # Retorna principais cidades do Brasil
            return self.localizacoes_brasil[:5]
        
        # Adiciona variações da localização
        localizacoes = [localizacao]
        
        # Adiciona "Remoto" se não estiver presente
        if "remoto" not in localizacao.lower() and "remote" not in localizacao.lower():
            localizacoes.append(f"{localizacao} - Remoto")
            localizacoes.append("Remoto - Brasil")
        
        return localizacoes
    
    def gerar_combinacoes(self, cargo: str, area_interesse: str, localizacao: str) -> List[Dict[str, str]]:
        """
        Gera todas as combinações de cargo e localização
        
        Args:
            cargo: Cargo original
            area_interesse: Área de interesse
            localizacao: Localização original
            
        Returns:
            Lista de dicionários com combinações cargo/localização
        """
        queries = self.expandir_query(cargo, area_interesse)
        localizacoes = self.expandir_localizacao(localizacao)
        
        # Limita combinações para não sobrecarregar
        max_combinacoes = 15
        combinacoes = []
        
        for i, query in enumerate(queries[:5]):  # Top 5 queries
            for j, loc in enumerate(localizacoes[:3]):  # Top 3 localizações
                if len(combinacoes) >= max_combinacoes:
                    break
                    
                combinacoes.append({
                    "cargo": query,
                    "localizacao": loc,
                    "prioridade": 10 - i - j  # Maior prioridade para primeiras combinações
                })
        
        return combinacoes


# Exemplo de uso
if __name__ == "__main__":
    expander = QueryExpander()
    
    # Teste com "desenvolvedor"
    print("=== Expansão de 'desenvolvedor' ===")
    queries = expander.expandir_query("desenvolvedor", "tecnologia")
    for q in queries:
        print(f"  • {q}")
    
    print("\n=== Combinações para coleta ===")
    combinacoes = expander.gerar_combinacoes("desenvolvedor", "tecnologia", "Brasil")
    for c in combinacoes:
        print(f"  • {c['cargo']} em {c['localizacao']} (prioridade: {c['prioridade']})")