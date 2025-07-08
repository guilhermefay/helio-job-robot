# Decisão: Remover Fallback do Sistema

## Por que remover o fallback?

### 1. Falsa sensação de sucesso
- Usuário acha que funcionou mas recebe palavras inúteis
- "desenvolvimento", "experiência", "você" não ajudam em nada

### 2. Invalida todo o método Carolina Martins
- Palavras ruins destroem a eficácia do currículo
- Melhor não ter resultado do que ter resultado ruim

### 3. Transparência é melhor
- Erro claro permite ao usuário tomar ação (configurar API key)
- Não engana o usuário com resultado de baixa qualidade

## O que foi feito

1. **Removido completamente o método de fallback**
   - Deletado `_fallback_analise_basica` (277 linhas de código)
   
2. **Erro mais claro quando IA falha**
   ```python
   raise Exception("Não foi possível analisar as vagas com IA. Por favor, configure pelo menos uma API key (GOOGLE_API_KEY, ANTHROPIC_API_KEY ou OPENAI_API_KEY)")
   ```

3. **Sistema agora é "IA ou nada"**
   - Garante qualidade consistente
   - Força uso correto com API configurada

## Resultado

✅ **COM IA**: Palavras úteis como React.js, Node.js, AWS, Docker
❌ **SEM IA**: Erro claro pedindo configuração de API

Isso está 100% alinhado com a metodologia Carolina Martins que exige QUALIDADE nas palavras-chave!