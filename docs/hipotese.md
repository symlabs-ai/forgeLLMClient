# Hipótese — ForgeLLMClient (SDK)

## Problema

ToolCalling não é padronizado entre provedores; a gestão de contexto varia em interface e limites; SDKs básicos não têm MCP client; e cada troca de fornecedor obriga reimplementar partes essenciais do fluxo de IA, gerando custo, perda de tempo e bugs. O cenário instável de APIs e modelos torna isso ainda mais crítico.

## Solução Proposta

O Forge é um SDK leve que fornece uma interface única e estável para qualquer LLM, eliminando o overhead de frameworks de agentes. Ele oferece:

1. **AutoFallback configurável**
   Quando `True`, alterna automaticamente entre provedores em caso de erro, rate limit, instabilidade ou indisponibilidade.

2. **Normalização completa de Tool Calling**
   Converte o formato nativo de ferramentas de cada modelo para um **formato interno único**, expondo um único padrão de ferramentas para o desenvolvedor, independentemente do provedor.

3. **Normalização total de Context Management**
   O dev envia o contexto *uma vez* e o Forge adapta ao modelo. Inclui:

   * histórico unificado
   * truncamento automático
   * compressão semântica
   * injeção de system functions
   * adequação ao limite de tokens do provedor
   * preservação de estado entre LLMs

4. **Modelo Mock interno para DryRun**
   Permite rodar testes sem tokens, simulando respostas de forma determinística. Fundamental para CI/CD e debugging.

5. **Sistema de Eventos e Extensões**
   Hooks em tudo:

   * pré-prompt
   * pós-resposta
   * pré-tool
   * pós-tool
   * pós-erro
     Permite instrumentação, auditoria, métricas, logs, monitoramento e customizações avançadas sem tocar no core.

6. **LLM Hot-Swap em Runtime**
   Troca de LLM durante a sessão **sem quebrar o contexto**.
   O santo graal da portabilidade: alternar entre modelos cloud, locais e híbridos em tempo real.

## Contexto

O ecossistema de LLMs está altamente volátil: provedores surgem e desaparecem, APIs mudam rápido, funcionalidades são renomeadas ou removidas, e os custos variam semanalmente. Sem uma camada de estabilidade, cada empresa vira refém dessa instabilidade.

## Sinal de Mercado

O aumento na quantidade de provedores, a pressão por redução de custos, e a crescente necessidade de flexibilidade indicam que empresas querem LLMs intercambiáveis — mas sem reconstruir integrações sempre que o mercado muda.

## Oportunidade Pressentida

Entregar para os devs uma camada fina, previsível e poderosa que permite trocar, combinar e evoluir provedores de LLM sem refazer código. Uma única interface para um mundo de APIs instáveis.

## Público-Alvo Inicial

Devs que querem controle fino sobre seus fluxos de IA sem adotar frameworks pesados, desejam flexibilidade de provedores e precisam garantir estabilidade operacional em longo prazo.

## Tese de Inevitabilidade

“Toda empresa que vive de LLM vai inevitavelmente precisar de uma camada estável sobre APIs instáveis.”

## Impacto Esperado

* Redução drástica do retrabalho ao trocar de modelo.
* Ganho de estabilidade em ambientes multi-LLM.
* Menor risco operacional com AutoFallback.
* Redução significativa de custos com Hot-Swap e modelos locais.
* Ciclo de desenvolvimento mais rápido com modelo mock e eventos.
* Portabilidade real: código que sobrevive à volatilidade do mercado.
