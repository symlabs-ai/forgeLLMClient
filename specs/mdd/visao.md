# Visao do Produto — ForgeLLMClient

## 1. Intencao Central

Libertar desenvolvedores e empresas do vendor lock-in de LLMs, oferecendo uma camada estavel, leve e previsivel sobre APIs instáveis — tornando modelos de IA tao intercambiaveis quanto bancos de dados.

---

## 2. Problema de Mercado

O ecossistema de LLMs está em caos controlado:

- **APIs instáveis**: provedores mudam endpoints, formatos e comportamentos sem aviso
- **Falta de padronizacao**: Tool Calling, Context Management e limites de tokens variam entre provedores
- **Vendor lock-in**: empresas ficam refens de 1-2 provedores sem plano B
- **Custo de troca alto**: migrar de provedor exige reescrever código, adaptar formatos, perder contexto
- **Precos voláteis**: custos mudam drasticamente de um mes para outro

Hoje, trocar de LLM é como trocar de banco de dados inteiro — absurdo e caro.

---

## 3. Hipotese de Valor

> "Toda empresa que vive de LLM vai inevitavelmente precisar de uma camada estavel sobre APIs instáveis."

Se oferecermos uma interface única, normalizada e com fallback automático, as empresas ganharao:

- **Independencia**: escolher provedores por mérito, nao por acoplamento
- **Previsibilidade**: código que sobrevive a mudancas de API
- **Portabilidade**: trocar de modelo em runtime sem perder contexto
- **Soberania**: controle total sobre o stack de IA

---

## 4. Publico-Alvo e Contexto

### Early Adopters

| Perfil | Contexto | Dor Principal |
|--------|----------|---------------|
| **Startups multi-LLM** | Já usam >1 provedor | Reduzir custo e complexidade |
| **Times enterprise** | Compliance exige alternativas | Precisam de fallback e auditoria |
| **Devs solo avancados** | Constroem automacoes | Querem controle fino sem frameworks pesados |

### Momento da Dor

A dor explode quando:
- Troca de provedor (migracao forcada)
- Deploy em producao (escala e custo)
- Provedor dobra o preco ou descontinua modelo
- API quebra compatibilidade (acontece frequentemente)

---

## 5. Paisagem Competitiva

| Solucao | Problema |
|---------|----------|
| **SDKs nativos** (OpenAI, Anthropic) | Lock-in total, sem portabilidade |
| **LangChain** | Pesado, mágico, impoe arquitetura própria |
| **LlamaIndex** | Foco em RAG, nao em portabilidade |
| **LiteLLM** | Normaliza chamadas, mas nao resolve contexto nem hot-swap |

Nenhum oferece a combinacao de:
- Normalizacao de Tool Calling
- Normalizacao de Context Management
- Hot-Swap em runtime
- AutoFallback configurável
- Mock para testes
- MCP Client integrado

---

## 6. Diferencial Estrategico

### Feature Matadora: LLM Hot-Swap em Runtime

Trocar de LLM durante a sessao **sem quebrar o contexto**.
Ninguém tem isso. Isso muda tudo.

### Diferenciais Combinados

1. **AutoFallback configurável** — alterna provedores em caso de erro/rate limit
2. **Normalizacao completa de Tool Calling** — formato interno único
3. **Normalizacao de Context Management** — histórico, truncamento, compressao
4. **Modelo Mock para DryRun** — testes sem tokens, CI/CD friendly
5. **Sistema de Eventos** — hooks em tudo (pré-prompt, pós-resposta, pré-tool, etc.)
6. **Hot-Swap** — troca de modelo preservando estado
7. **MCP Client nativo** — acesso ao ecossistema Model Context Protocol sem dependencias extras

#### O Forge **não**:

- orquestra agentes complexos,
- gerencia workflows de alto nível,
- tenta ser RAG framework,
- nem virar plataforma de UI.

Ele é **camada de cliente**. Ponto.

---

## 7. Metrica de Validacao Inicial

### Sinais de Validacao (3 meses)

| Métrica | Target |
|---------|--------|
| Empresa usando em producao | >= 1 |
| Downloads PyPI | >= 1.000 |
| Plugins de provedores externos | >= 5 |
| Caso real de fallback salvando producao | >= 1 (estudo de caso) |

### Sinais Qualitativos

- PRs espontâneas no GitHub
- Alguém criando plugin de provedor sem ser solicitado
- Mencoes orgânicas em comunidades dev

---

## 8. Horizonte de Desenvolvimento

### Fase 1: Core SDK
- Interface unificada de chat (com e sem streaming)
- Tool Calling
- Informar o consumo de tokens em cada requisição.
- Normalizacao básica de respostas
- Suporte a 2-3 provedores (OpenAI, Anthropic)

### Fase 2: Portabilidade
- AutoFallback configurável
- Hot-Swap em runtime
- Context Management normalizado

### Fase 3: Ecossistema
- Sistema de eventos/hooks
- Mock provider para testes
- Plugin system para provedores externos (OpenRouter, LLamaCPP (local), Gemini)

### Fase 4: Producao
- Observabilidade (métricas, logs, traces)
- Documentacao e exemplos
- Casos de uso reais

---

## 9. Palavras-Chave e Conceitos

`portabilidade` · `independencia` · `estabilidade` · `hot-swap` · `fallback` · `normalizacao` · `vendor-agnostic` · `leveza` · `controle` · `previsibilidade` · `soberania`

---

## 10. Tom Narrativo

**Direto, técnico e empoderador.**

A voz de quem entende a dor do dev e oferece uma solucao pragmática — sem mágica, sem frameworks pesados, sem promessas vazias.

> "O Forge nao é um framework. É um seguro contra a volatilidade do mercado de LLMs."

---

## 11. ValueTracks e SupportTracks

### ValueTracks (Valor Direto ao Usuario)

| Track | Descricao | Métrica de Valor |
|-------|-----------|------------------|
| **PortableChat** | Enviar mensagens para qualquer LLM com interface única (sync e streaming) | Tempo de migracao entre provedores < 1h |
| **AutoFallback** | Resiliencia automática em caso de falha | 0 downtime por indisponibilidade de provedor |
| **HotSwap** | Trocar modelo em runtime sem perder contexto | Custo reduzido em 30%+ com modelos hibridos |
| **UnifiedTools** | Tool Calling padronizado entre provedores | 0 retrabalho ao trocar provedor |
| **MCPClient** | Acesso nativo ao ecossistema MCP (tools, resources, prompts) | Integracao com MCP servers em < 5 min |

### SupportTracks (Sustentacao Técnica)

| Track | Descricao | Suporta |
|-------|-----------|---------|
| **ContextManager** | Normalizacao de histórico e limites | PortableChat, HotSwap |
| **MockProvider** | Testes sem tokens | Todos (CI/CD) |
| **EventSystem** | Hooks para instrumentacao | Observabilidade |
| **ProviderPlugins** | Sistema extensivel de provedores | PortableChat, AutoFallback |

---

*Documento gerado em colaboracao entre o stakeholder e o MDD Coach.*
*Data: 2025-12-03*
*Versao: 1.1*
