"""
Extrator Profissional de Palavras-Chave - Sistema HELIO
Corrige os problemas da extração genérica seguindo metodologia Carolina Martins
"""

import re
from typing import List, Dict, Set, Tuple
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.tree import Tree

class KeywordExtractorPro:
    """
    Extrator avançado que captura competências específicas, não termos genéricos
    """
    
    def __init__(self):
        # Download necessário do NLTK (fazer apenas uma vez)
        try:
            nltk.data.find('tokenizers/punkt')
        except:
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            nltk.download('maxent_ne_chunker')
            nltk.download('words')
        
        # Stop words expandidas - o que NÃO queremos
        self.stop_words_expandidas = {
            # Stop words padrão PT
            'de', 'da', 'do', 'das', 'dos', 'e', 'em', 'para', 'com', 'por',
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
            'que', 'qual', 'quais', 'quando', 'onde', 'como', 'porque',
            'mas', 'ou', 'se', 'então', 'assim', 'também', 'ainda',
            
            # Termos genéricos que não são competências
            'empresa', 'vaga', 'oportunidade', 'profissional', 'experiência',
            'conhecimento', 'habilidade', 'competência', 'requisito', 'área',
            'atividade', 'responsabilidade', 'diferencial', 'desejável',
            'obrigatório', 'necessário', 'importante', 'fundamental',
            
            # Verbos genéricos
            'realizar', 'executar', 'desenvolver', 'atuar', 'trabalhar',
            'auxiliar', 'apoiar', 'participar', 'colaborar',
            
            # CRÍTICO: Adjetivos genéricos que estavam poluindo
            'estratégico', 'analítico', 'proativo', 'dinâmico', 'inovador',
            'criativo', 'organizado', 'responsável', 'comprometido'
        }
        
        # Padrões para capturar competências reais
        self.padroes_competencias = {
            'linguagens': re.compile(r'\b(Python|Java|JavaScript|TypeScript|C\+\+|C#|Ruby|Go|Rust|PHP|Swift|Kotlin|Scala|R|MATLAB|Julia)\b', re.I),
            'frameworks_web': re.compile(r'\b(React|Angular|Vue\.?js|Django|Flask|FastAPI|Spring|Express|Rails|Laravel|ASP\.NET|Next\.?js|Nuxt)\b', re.I),
            'databases': re.compile(r'\b(MySQL|PostgreSQL|MongoDB|Redis|Cassandra|Oracle|SQL Server|DynamoDB|Firestore|MariaDB|SQLite|Neo4j)\b', re.I),
            'cloud': re.compile(r'\b(AWS|Azure|GCP|Google Cloud|EC2|S3|Lambda|CloudFormation|Terraform|Docker|Kubernetes|OpenShift)\b', re.I),
            'ferramentas_dados': re.compile(r'\b(Pandas|NumPy|Scikit-learn|TensorFlow|PyTorch|Keras|Spark|Hadoop|Tableau|Power BI|Looker|Databricks)\b', re.I),
            'metodologias': re.compile(r'\b(Scrum|Kanban|SAFe|XP|Lean|Six Sigma|PMBOK|ITIL|DevOps|CI/CD|TDD|BDD|DDD)\b', re.I),
            'ferramentas_dev': re.compile(r'\b(Git|GitHub|GitLab|Bitbucket|Jenkins|CircleCI|Travis|Jira|Confluence|VS Code|IntelliJ|Eclipse)\b', re.I),
            'protocolos': re.compile(r'\b(REST|GraphQL|SOAP|gRPC|WebSocket|HTTP/2|OAuth|JWT|SAML|OpenAPI|Swagger)\b', re.I),
            'mobile': re.compile(r'\b(iOS|Android|React Native|Flutter|Xamarin|SwiftUI|Jetpack Compose)\b', re.I),
            'seguranca': re.compile(r'\b(OWASP|SSL/TLS|Penetration Testing|Vulnerability Assessment|SIEM|WAF|Firewall|IDS/IPS)\b', re.I),
            'design': re.compile(r'\b(Figma|Sketch|Adobe XD|Photoshop|Illustrator|After Effects|Premiere|InDesign|Canva)\b', re.I),
            'marketing_tools': re.compile(r'\b(Google Analytics|Google Ads|Facebook Ads|LinkedIn Ads|HubSpot|Salesforce|Marketo|MailChimp|SEMrush|Ahrefs)\b', re.I),
            'erp_crm': re.compile(r'\b(SAP|Oracle ERP|Microsoft Dynamics|Salesforce CRM|HubSpot CRM|Pipedrive|Zoho)\b', re.I),
            'bi_analytics': re.compile(r'\b(Power BI|Tableau|Looker|QlikView|Sisense|Domo|Google Data Studio|Metabase)\b', re.I)
        }
        
        # Termos compostos importantes
        self.termos_compostos = {
            'desenvolvimento': ['desenvolvimento web', 'desenvolvimento mobile', 'desenvolvimento full stack', 
                               'desenvolvimento backend', 'desenvolvimento frontend', 'desenvolvimento de software'],
            'gestao': ['gestão de projetos', 'gestão de produtos', 'gestão de equipes', 'gestão ágil',
                      'gestão de riscos', 'gestão de mudanças', 'gestão de configuração'],
            'analise': ['análise de dados', 'análise de negócios', 'análise de sistemas', 'análise de requisitos',
                       'análise de performance', 'análise de métricas', 'análise preditiva'],
            'engenharia': ['engenharia de software', 'engenharia de dados', 'engenharia de machine learning',
                          'engenharia de confiabilidade', 'engenharia de segurança'],
            'arquitetura': ['arquitetura de software', 'arquitetura de sistemas', 'arquitetura de microsserviços',
                           'arquitetura cloud', 'arquitetura serverless', 'arquitetura orientada a eventos']
        }
    
    def extrair_palavras_chave_profissionais(self, texto: str) -> List[str]:
        """
        Extrai palavras-chave profissionais específicas, não genéricas
        """
        palavras_extraidas = set()
        texto_lower = texto.lower()
        
        # 1. Extrair competências técnicas específicas
        for categoria, padrao in self.padroes_competencias.items():
            matches = padrao.findall(texto)
            for match in matches:
                # Mantém o case original para tecnologias
                palavras_extraidas.add(match)
        
        # 2. Extrair termos compostos relevantes
        for categoria, termos in self.termos_compostos.items():
            for termo in termos:
                if termo in texto_lower:
                    palavras_extraidas.add(termo)
        
        # 3. Usar POS tagging para encontrar substantivos técnicos
        tokens = word_tokenize(texto)
        pos_tags = pos_tag(tokens)
        
        # Captura substantivos próprios (tecnologias, ferramentas)
        for i, (word, tag) in enumerate(pos_tags):
            # NNP = substantivo próprio, NN = substantivo comum
            if tag in ['NNP', 'NNPS'] and len(word) > 2:
                # Verifica se não é stop word
                if word.lower() not in self.stop_words_expandidas:
                    palavras_extraidas.add(word)
            
            # Captura padrões como "Certified Scrum Master"
            if i < len(pos_tags) - 2:
                if tag == 'NNP' and pos_tags[i+1][1] == 'NNP':
                    compound = f"{word} {pos_tags[i+1][0]}"
                    if pos_tags[i+2][1] == 'NNP':
                        compound += f" {pos_tags[i+2][0]}"
                    palavras_extraidas.add(compound)
        
        # 4. Capturar certificações
        cert_patterns = [
            r'(PMP|PMI-ACP|CSM|PSM|AWS Certified|Azure Certified|Google Cloud Certified)',
            r'(ITIL|COBIT|Six Sigma Green Belt|Six Sigma Black Belt)',
            r'(CPA|CFA|FRM|CISA|CISSP|CEH)',
            r'(OCA|OCP|MCSA|MCSE|CCNA|CCNP)'
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, texto, re.I)
            palavras_extraidas.update(matches)
        
        # 5. Remover palavras genéricas que passaram
        palavras_filtradas = []
        for palavra in palavras_extraidas:
            palavra_lower = palavra.lower()
            
            # Remove se for stop word
            if palavra_lower in self.stop_words_expandidas:
                continue
                
            # Remove se for muito curta
            if len(palavra) < 3:
                continue
                
            # Remove se for apenas número
            if palavra.isdigit():
                continue
                
            palavras_filtradas.append(palavra)
        
        return palavras_filtradas
    
    def categorizar_competencias(self, palavras: List[str]) -> Dict[str, List[str]]:
        """
        Categoriza as competências de forma correta
        """
        categorias = {
            'tecnicas': [],  # Linguagens, frameworks, metodologias
            'ferramentas': [],  # Softwares, plataformas, ferramentas
            'comportamentais': []  # Apenas soft skills reais, não adjetivos
        }
        
        # Mapeamento correto
        ferramentas_set = {
            'excel', 'power bi', 'tableau', 'jira', 'confluence', 'git', 'github',
            'vs code', 'intellij', 'photoshop', 'illustrator', 'figma', 'sketch',
            'google analytics', 'google ads', 'hubspot', 'salesforce', 'sap'
        }
        
        comportamentais_reais = {
            'liderança de equipes', 'gestão de conflitos', 'comunicação executiva',
            'negociação internacional', 'apresentação para C-level', 'mentoria',
            'facilitação de workshops', 'gestão de stakeholders'
        }
        
        for palavra in palavras:
            palavra_lower = palavra.lower()
            
            # Classificação correta
            if palavra_lower in ferramentas_set or any(tool in palavra_lower for tool in ferramentas_set):
                categorias['ferramentas'].append(palavra)
            elif palavra_lower in comportamentais_reais:
                categorias['comportamentais'].append(palavra)
            else:
                # Todo o resto é técnico (linguagens, frameworks, metodologias)
                categorias['tecnicas'].append(palavra)
        
        return categorias
    
    def calcular_relevancia(self, palavra: str, frequencia: int, total_vagas: int) -> float:
        """
        Calcula relevância real baseada na especificidade
        """
        # Frequência relativa
        freq_relativa = frequencia / total_vagas
        
        # Bonus por especificidade
        especificidade = 0.0
        
        # Tecnologias específicas ganham bonus
        if any(palavra in padrao.pattern for padrao in self.padroes_competencias.values()):
            especificidade += 0.3
        
        # Termos compostos são mais específicos
        if ' ' in palavra:
            especificidade += 0.2
        
        # Certificações são muito específicas
        if any(cert in palavra.upper() for cert in ['AWS', 'PMP', 'ITIL', 'CERTIFIED']):
            especificidade += 0.2
        
        # Cálculo final
        relevancia = (freq_relativa * 0.5) + especificidade
        
        return min(relevancia, 1.0)