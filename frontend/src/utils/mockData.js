// Mock de dados para testes rápidos da análise
export const MOCK_COLLECTION_DATA = {
  demo_mode: false,
  estatisticas: {
    totalVagas: 5,
    vagasAnalisadas: 5,
    vagasPorFonte: {
      'Indeed': 5
    },
    tempoColeta: '12 segundos',
    ultimaAtualizacao: new Date().toISOString()
  },
  fontes: ['Indeed'],
  transparencia: {
    fontes_utilizadas: ['Indeed'],
    metodo_coleta: 'Mock para teste',
    filtros_aplicados: 'Cargo: Desenvolvedor, Localização: São Paulo',
    observacoes: 'Dados de teste para desenvolvimento'
  },
  vagas: [
    {
      titulo: "Desenvolvedor Full Stack Python/React",
      empresa: "TechCorp Solutions",
      descricao: `Buscamos desenvolvedor full stack com sólida experiência em:

• Python (Django, Flask, FastAPI)
• React.js, TypeScript, Next.js
• PostgreSQL, MongoDB, Redis
• Docker, Kubernetes, AWS
• CI/CD com GitLab/GitHub Actions
• Metodologias ágeis (Scrum, Kanban)

Requisitos:
- 3+ anos de experiência em desenvolvimento web
- Conhecimento em arquitetura de microsserviços
- Experiência com testes automatizados (pytest, jest)
- Inglês intermediário/avançado
- Comunicação e trabalho em equipe

Diferenciais:
- Certificações AWS
- Experiência com Machine Learning
- Conhecimento em DevOps`,
      localizacao: "São Paulo, SP - Híbrido",
      link: "https://example.com/vaga1",
      fonte: "Indeed",
      publicada: "2 dias atrás"
    },
    {
      titulo: "Engenheiro de Dados Senior - Python",
      empresa: "DataFlow Analytics",
      descricao: `Procuramos engenheiro de dados experiente para:

• Desenvolvimento de pipelines de dados com Python
• Apache Spark, Airflow, Kafka
• AWS (S3, EMR, Glue, Redshift)
• SQL avançado e modelagem dimensional
• ETL/ELT em grande escala

Tecnologias utilizadas:
- Python (pandas, numpy, PySpark)
- Apache Airflow para orquestração
- Docker e Kubernetes
- Terraform para IaC
- Databricks, Snowflake

Requisitos:
- 4+ anos em engenharia de dados
- Experiência com Big Data
- Conhecimento em Data Warehousing
- SQL avançado`,
      localizacao: "São Paulo, SP - Remoto",
      link: "https://example.com/vaga2",
      fonte: "Indeed",
      publicada: "1 dia atrás"
    },
    {
      titulo: "Desenvolvedor Backend Python - Microserviços",
      empresa: "MicroTech",
      descricao: `Vaga para desenvolvedor backend especializado em:

• Python (FastAPI, Django REST)
• Arquitetura de microserviços
• PostgreSQL, MongoDB
• Redis para cache
• RabbitMQ, Apache Kafka
• Docker e Kubernetes
• AWS ou Azure

Responsabilidades:
- Desenvolver APIs RESTful robustas
- Implementar padrões de design
- Otimizar performance de aplicações
- Colaborar em code reviews

Stack técnico:
- Python 3.9+, FastAPI, SQLAlchemy
- PostgreSQL, Redis
- Docker, Kubernetes
- GitLab CI/CD
- Monitoring com Prometheus`,
      localizacao: "Rio de Janeiro, RJ - Presencial",
      link: "https://example.com/vaga3",
      fonte: "Indeed",
      publicada: "3 horas atrás"
    },
    {
      titulo: "DevOps Engineer - Python/AWS",
      empresa: "CloudOps Brasil",
      descricao: `Buscamos DevOps Engineer com foco em:

• Automação com Python
• AWS (EC2, ECS, Lambda, S3)
• Terraform, CloudFormation
• Docker, Kubernetes
• Jenkins, GitLab CI/CD
• Monitoring e alertas

Ferramentas principais:
- Python para automação
- Terraform para infraestrutura
- Ansible para configuração
- Prometheus + Grafana
- ELK Stack para logs

Requisitos:
- 3+ anos em DevOps/SRE
- Experiência com cloud AWS
- Scripts Python para automação
- Conhecimento em Linux`,
      localizacao: "Brasília, DF - Híbrido",
      link: "https://example.com/vaga4",
      fonte: "Indeed",
      publicada: "5 horas atrás"
    },
    {
      titulo: "Cientista de Dados - Python/ML",
      empresa: "AI Labs",
      descricao: `Cientista de dados para projetos de machine learning:

• Python (pandas, scikit-learn, TensorFlow)
• Análise estatística avançada
• Machine Learning e Deep Learning
• SQL para análise de dados
• Jupyter Notebooks, MLflow

Projetos típicos:
- Modelos de recomendação
- Análise preditiva
- NLP e processamento de texto
- Computer vision

Ferramentas utilizadas:
- Python (pandas, numpy, scipy)
- TensorFlow, PyTorch, scikit-learn
- SQL (PostgreSQL, BigQuery)
- Docker para deploy de modelos
- Git para versionamento

Background desejado:
- Formação em exatas/computação
- Experiência com dados reais
- Conhecimento estatístico sólido`,
      localizacao: "São Paulo, SP - Remoto",
      link: "https://example.com/vaga5",
      fonte: "Indeed",
      publicada: "1 dia atrás"
    }
  ]
};

export const MOCK_SEARCH_CONFIG = {
  cargo: 'Desenvolvedor Python',
  localizacao: 'São Paulo, SP',
  quantidade: 100,
  segmentos: 'Tecnologia, Startups',
  tipoVaga: 'todos',
  raio: '25',
  nivel: 'todos',
  tipoContrato: 'todos',
  diasPublicacao: 'todos',
  ordenar: 'date',
  modalidade: 'todos'
};