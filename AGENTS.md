# Symbiotas e Agents — Guia Rápido

## Sobre o repositório

forgellmClient é um SDK python leve que fornece uma interface única e estável para qualquer LLM, eliminando o overhead de frameworks de agentes.

## Referências Obrigatórias

### Guias do ForgeLLMClient (SDK)
- Uso do Client: `docs/guides/client-usage.md` (como usar o SDK, chat, streaming, tools, vision).
- Modelo de Domínio: `docs/guides/domain-model.md` (ChatResponse, Message, TokenUsage, ImageContent).
- Tratamento de Erros: `docs/guides/error-handling.md` (exceções, retry, mapeamento de erros por provider).
- Criação de Providers: `docs/guides/creating-providers.md` (como implementar novos providers).

### Guias do ForgeBase (Framework)
- Guia de agentes do ForgeBase: `docs/guides/forgebase_guides/agentes-ia/` (início rápido, descoberta, ecossistema).
- Regras do ForgeBase: `docs/guides/forgebase_guides/usuarios/forgebase-rules.md` (Clean/Hex, CLI-first, offline, persistência YAML + auto-commit Git).
- Prompts de cada symbiota: `process/symbiotes/<nome>/prompt.md`.
- Contexto MDD/BDD: `docs/`, `specs/bdd/`, `specs/adr/`. #pode ainda não existir

## Defaults para qualquer symbiota

- Clean/Hex: domínio é puro; adapters só via ports/usecases; nunca colocar I/O no domínio.
- CLI-first e offline: validar via CLI; evitar HTTP/TUI no MVP; sem rede externa por padrão.
- Persistência: sessões/estados em YAML; auto-commit Git por step/fase quando habilitado.
- Plugins: só executar se houver manifesto claro; respeitar permissões (rede=false por padrão).
- Documentar sessões/handoffs em `project/docs/sessions/` quando aplicável.

## Symbiotas de Código/Tests (TDD)

- Consultar: `docs/guides/forgebase_guides/agentes-ia/guia-completo.md`, `docs/guides/forgebase_guides/usuarios/forgebase-rules.md`, prompts em `process/symbiotes/tdd_coder/` e `process/symbiotes/test_writer/`.
- Seguir BDD → TDD: features em `specs/bdd/`, steps em `tests/bdd/`, código em `src/` seguindo camadas ForgeBase.
- Usar exceções específicas, logging/métricas do ForgeBase; Rich apenas para UX em CLI.

## Outros Symbiotas

- Sempre ler o prompt do symbiota em `process/symbiotes/<nome>/prompt.md` e aplicar as regras gerais acima quando interagirem com runtime/processos/artefatos.

## Outras observações

- Sempre que o usuário pedir para carregar, impersonar, interpretar uma persona de symbiota ou agente. Responda a ele sempre com o nome do symbiota na cor verde entre chaves: [bill_review] diz: Estou começando a analisar ....
