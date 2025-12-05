# language: pt
Funcionalidade: Observabilidade e Metricas
  Como desenvolvedor
  Quero ter visibilidade sobre as chamadas LLM
  Para monitorar, debugar e otimizar minha aplicacao

  Contexto:
    Dado um client configurado com observability

  @observability
  Cenario: LoggingObserver registra eventos de chat
    Dado um LoggingObserver configurado
    Quando eu fizer uma chamada de chat
    Entao o observer deve registrar evento de inicio
    E o observer deve registrar evento de conclusao

  @observability
  Cenario: MetricsObserver agrega metricas de uso
    Dado um MetricsObserver configurado
    Quando eu fizer 3 chamadas de chat
    Entao as metricas devem mostrar 3 requests totais
    E as metricas devem mostrar tokens consumidos
    E as metricas devem mostrar latencia media

  @observability
  Cenario: MetricsObserver agrupa por provider
    Dado um MetricsObserver configurado
    Quando eu fizer chamadas para diferentes providers
    Entao as metricas devem agrupar requests por provider
    E as metricas devem agrupar tokens por provider

  @observability
  Cenario: CallbackObserver executa funcoes customizadas
    Dado um CallbackObserver com callbacks registrados
    Quando eu fizer uma chamada de chat
    Entao o callback on_start deve ser executado
    E o callback on_complete deve ser executado

  @observability
  Cenario: Observability pode ser desabilitado
    Dado um ObservabilityManager desabilitado
    E um MockObserver configurado
    Quando eu fizer uma chamada de chat
    Entao o observer nao deve receber eventos

  @observability
  Cenario: Eventos de erro sao emitidos
    Dado um MetricsObserver configurado
    Quando ocorrer um erro na chamada
    Entao o observer deve registrar evento de erro
    E as metricas devem mostrar 1 erro total

  @observability
  Cenario: Multiplos observers recebem mesmo evento
    Dado multiplos observers configurados
    Quando eu fizer uma chamada de chat
    Entao todos os observers devem receber o evento

  @observability
  Cenario: Observer com erro nao afeta outros
    Dado um observer que falha
    E um observer normal
    Quando eu fizer uma chamada de chat
    Entao o observer normal deve receber o evento
    E a chamada deve completar com sucesso

  @observability
  Cenario: Metricas podem ser resetadas
    Dado um MetricsObserver com metricas existentes
    Quando eu resetar as metricas
    Entao todas as metricas devem estar zeradas

  @observability
  Cenario: Privacy - conteudo nao logado por default
    Dado um LoggingObserver configurado
    Quando eu fizer uma chamada de chat com conteudo sensivel
    Entao o log nao deve conter o conteudo da mensagem
