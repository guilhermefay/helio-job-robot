#!/bin/bash
echo "🧪 Teste rápido do backend HELIO"
echo "================================"

# Teste 1: Health check
echo -e "\n1️⃣ Testando health check..."
curl -s https://helio-job-robot-production.up.railway.app/api/health | python3 -m json.tool

# Teste 2: Coleta normal (vai mostrar logs no Railway)
echo -e "\n2️⃣ Testando coleta (verifique os logs no Railway)..."
curl -X POST https://helio-job-robot-production.up.railway.app/api/agent1/collect-keywords \
  -H "Content-Type: application/json" \
  -H "Origin: https://linekdinagent.vercel.app" \
  -d '{
    "area_interesse": "teste",
    "cargo_objetivo": "teste",
    "localizacao": "são paulo",
    "total_vagas_desejadas": 1
  }' \
  -m 30 -v

echo -e "\n✅ Teste concluído! Verifique os logs no Railway para ver os detalhes."