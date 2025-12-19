# Proposta: Sistema de Plugins para ForgeBase

> "Extensibilidade sem modificar o núcleo."

Este documento propõe a incorporação de um **sistema genérico de plugins** ao ForgeBase, permitindo que qualquer projeto derivado (como forge\_llm) herde uma infraestrutura completa de composição e extensibilidade.

***

## Motivação

### Problema Atual

Cada projeto que estende ForgeBase precisa reimplementar:

1. **Composition Root** - Montagem do grafo de objetos
2. **Plugin Registry** - Mapeamento de tipos para classes
3. **BuildSpec** - Configuração declarativa
4. **BuildContext** - Contexto de resolução

Isso gera:

* Duplicação de código

* Padrões inconsistentes entre projetos

* Curva de aprendizado para cada projeto

### Solução Proposta

Incorporar ao ForgeBase uma **infraestrutura genérica de composição** que:

* Fornece classes base para Builder, Registry e Spec

* Mantém a filosofia "Quem usa não cria. Quem cria não usa."

* Permite extensão sem modificar o núcleo

* Suporta configuração declarativa (YAML/JSON)

***

## Hierarquia Proposta

```
ForgeBase (atual)                    ForgeBase (proposto)
─────────────────────────────────────────────────────────────────
domain/                              domain/
  EntityBase                           EntityBase
  ValueObjectBase                      ValueObjectBase
  exceptions.py                        exceptions.py

application/                         application/
  UseCaseBase                          UseCaseBase
  PortBase                             PortBase
  DTOBase                              DTOBase

adapters/                            adapters/
  AdapterBase                          AdapterBase
  CLIAdapter                           CLIAdapter

infrastructure/                      infrastructure/
  RepositoryBase                       RepositoryBase

observability/                       observability/
  LogService                           LogService
  TrackMetrics                         TrackMetrics

testing/                             testing/
  ForgeTestCase                        ForgeTestCase

                                     composition/          ← NOVO
                                       PluginRegistryBase
                                       BuilderBase
                                       BuildSpecBase
                                       BuildContextBase
```

***

## Componentes Genéricos Propostos

### 1. PluginRegistryBase

```python
# forgebase/composition/plugin_registry.py
"""Registro genérico de plugins."""

from typing import TypeVar, Generic, Type, Callable
from abc import ABC, abstractmethod

T = TypeVar("T")


class PluginRegistryBase(ABC, Generic[T]):
    """
    Registro central de extensibilidade.

    Mapeia (kind, type_id) → classe concreta ou factory.

    Exemplos de uso em projetos derivados:
    - forge_llm: ("provider", "openai") → OpenAIAdapter
    - forge_db: ("repository", "postgres") → PostgresRepository
    - forge_api: ("auth", "jwt") → JWTAuthAdapter

    Subclasses devem implementar register_defaults() para
    registrar os plugins padrão do projeto.
    """

    def __init__(self):
        self._registry: dict[str, dict[str, Type[T] | Callable[..., T]]] = {}

    def register(
        self,
        kind: str,
        type_id: str,
        cls_or_factory: Type[T] | Callable[..., T],
    ) -> None:
        """
        Registrar um plugin.

        :param kind: Categoria do plugin (ex: "provider", "agent", "repository")
        :param type_id: Identificador do tipo (ex: "openai", "chat", "postgres")
        :param cls_or_factory: Classe ou factory function
        """
        if kind not in self._registry:
            self._registry[kind] = {}

        self._registry[kind][type_id] = cls_or_factory

    def resolve(self, kind: str, type_id: str) -> Type[T] | Callable[..., T]:
        """
        Resolver um plugin pelo kind e type_id.

        :param kind: Categoria do plugin
        :param type_id: Identificador do tipo
        :return: Classe ou factory registrada
        :raises KeyError: Se não encontrado
        """
        if kind not in self._registry:
            raise KeyError(f"Plugin kind '{kind}' não registrado")

        if type_id not in self._registry[kind]:
            available = list(self._registry[kind].keys())
            raise KeyError(
                f"Plugin '{kind}/{type_id}' não encontrado. "
                f"Disponíveis: {available}"
            )

        return self._registry[kind][type_id]

    def list(self, kind: str) -> list[str]:
        """
        Listar plugins de uma categoria.

        :param kind: Categoria do plugin
        :return: Lista de type_ids registrados
        """
        if kind not in self._registry:
            return []
        return list(self._registry[kind].keys())

    def list_kinds(self) -> list[str]:
        """
        Listar todas as categorias registradas.

        :return: Lista de kinds
        """
        return list(self._registry.keys())

    def is_registered(self, kind: str, type_id: str) -> bool:
        """
        Verificar se um plugin está registrado.

        :param kind: Categoria do plugin
        :param type_id: Identificador do tipo
        :return: True se registrado
        """
        return kind in self._registry and type_id in self._registry[kind]

    @abstractmethod
    def register_defaults(self) -> None:
        """
        Registrar plugins padrão do projeto.

        Deve ser implementado por subclasses para registrar
        os plugins que vêm "de fábrica" com o projeto.

        Exemplo (forge_llm):
            def register_defaults(self):
                self.register("provider", "openai", OpenAIAdapter)
                self.register("provider", "anthropic", AnthropicAdapter)
                self.register("agent", "chat", ChatAgent)
                self.register("agent", "code", CodeAgent)
        """
        pass

    def to_dict(self) -> dict:
        """Serializar registro para debug/introspection."""
        return {
            kind: list(plugins.keys())
            for kind, plugins in self._registry.items()
        }
```

### 2. BuildSpecBase

```python
# forgebase/composition/build_spec.py
"""Especificação declarativa genérica."""

from typing import Any, TypeVar, Generic
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from pathlib import Path
import yaml
import json


T = TypeVar("T", bound="BuildSpecBase")


@dataclass
class BuildSpecBase(ABC):
    """
    Especificação declarativa para construção de objetos.

    Define O QUE deve ser construído, não COMO.
    O Builder é responsável por interpretar a spec.

    Subclasses devem definir os campos específicos do projeto.

    Exemplo (forge_llm):
        @dataclass
        class LLMBuildSpec(BuildSpecBase):
            agent: dict = field(default_factory=dict)
            provider: dict = field(default_factory=dict)
            model: dict = field(default_factory=dict)
            session: dict = field(default_factory=dict)
    """

    # Campos comuns a todos os projetos
    metadata: dict = field(default_factory=dict)
    observability: dict = field(default_factory=dict)

    @classmethod
    def from_yaml(cls: type[T], path: str | Path) -> T:
        """
        Carregar spec de arquivo YAML.

        :param path: Caminho do arquivo
        :return: Instância da spec
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Spec file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data)

    @classmethod
    def from_json(cls: type[T], path: str | Path) -> T:
        """
        Carregar spec de arquivo JSON.

        :param path: Caminho do arquivo
        :return: Instância da spec
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Spec file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

    @classmethod
    @abstractmethod
    def from_dict(cls: type[T], data: dict) -> T:
        """
        Criar spec a partir de dicionário.

        Deve ser implementado por subclasses.

        :param data: Dicionário com dados da spec
        :return: Instância da spec
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Serializar spec para dicionário.

        Deve ser implementado por subclasses.
        """
        pass

    def to_yaml(self) -> str:
        """Serializar para YAML."""
        return yaml.dump(self.to_dict(), default_flow_style=False)

    def to_json(self) -> str:
        """Serializar para JSON."""
        return json.dumps(self.to_dict(), indent=2)

    @abstractmethod
    def validate(self) -> None:
        """
        Validar a spec.

        Deve levantar ConfigurationError se inválida.
        """
        pass
```

### 3. BuildContextBase

```python
# forgebase/composition/build_context.py
"""Contexto de build genérico."""

from typing import TypeVar, Generic, Any
from dataclasses import dataclass, field

from forgebase.composition.build_spec import BuildSpecBase
from forgebase.composition.plugin_registry import PluginRegistryBase


S = TypeVar("S", bound=BuildSpecBase)
R = TypeVar("R", bound=PluginRegistryBase)


@dataclass
class BuildContextBase(Generic[S, R]):
    """
    Contexto de construção.

    Mantém o estado durante o processo de build:
    - Referência à spec
    - Referência ao registry
    - Cache de objetos já construídos
    - Variáveis de ambiente resolvidas

    O cache permite reutilizar objetos (singleton por build).
    """

    spec: S
    registry: R
    cache: dict = field(default_factory=dict)
    env: dict = field(default_factory=dict)

    def get(self, path: str, default: Any = None) -> Any:
        """
        Obter valor da spec por path.

        Suporta notação de ponto: "provider.type", "model.temperature"

        :param path: Caminho no formato "key.subkey.subsubkey"
        :param default: Valor padrão se não encontrado
        :return: Valor encontrado ou default
        """
        spec_dict = self.spec.to_dict()
        keys = path.split(".")
        value = spec_dict

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def resolve(self, kind: str, type_id: str) -> Any:
        """
        Resolver plugin via registry.

        :param kind: Categoria do plugin
        :param type_id: Identificador do tipo
        :return: Classe ou factory
        """
        return self.registry.resolve(kind, type_id)

    def get_cached(self, key: str) -> Any | None:
        """
        Obter objeto do cache.

        :param key: Chave do cache
        :return: Objeto ou None
        """
        return self.cache.get(key)

    def set_cached(self, key: str, value: Any) -> None:
        """
        Armazenar objeto no cache.

        :param key: Chave do cache
        :param value: Objeto a armazenar
        """
        self.cache[key] = value

    def resolve_env(self, env_var: str, required: bool = True) -> str | None:
        """
        Resolver variável de ambiente.

        :param env_var: Nome da variável
        :param required: Se True, levanta erro se não definida
        :return: Valor da variável ou None
        """
        import os

        # Primeiro verifica cache local
        if env_var in self.env:
            return self.env[env_var]

        # Depois verifica ambiente do sistema
        value = os.getenv(env_var)

        if value is None and required:
            from forgebase.domain.exceptions import ConfigurationError
            raise ConfigurationError(f"Variável de ambiente '{env_var}' não definida")

        return value
```

### 4. BuilderBase

```python
# forgebase/composition/builder.py
"""Builder genérico (Composition Root)."""

from typing import TypeVar, Generic, Any
from abc import ABC, abstractmethod

from forgebase.observability import LogService, TrackMetrics
from forgebase.composition.build_spec import BuildSpecBase
from forgebase.composition.build_context import BuildContextBase
from forgebase.composition.plugin_registry import PluginRegistryBase


S = TypeVar("S", bound=BuildSpecBase)
R = TypeVar("R", bound=PluginRegistryBase)
C = TypeVar("C", bound=BuildContextBase)
T = TypeVar("T")  # Tipo do objeto final construído


class BuilderBase(ABC, Generic[S, R, C, T]):
    """
    Composition Root genérico.

    O único lugar onde objetos são criados.
    Segue a regra: "Quem usa não cria. Quem cria não usa."

    Responsabilidades:
    - Ler BuildSpec
    - Criar BuildContext
    - Resolver classes via PluginRegistry
    - Instanciar e conectar objetos
    - Retornar objeto raiz pronto para uso

    Subclasses devem implementar:
    - create_registry(): Criar registry específico do projeto
    - create_context(): Criar contexto específico do projeto
    - build(): Lógica de construção específica
    """

    def __init__(self, registry: R | None = None):
        """
        Inicializar builder.

        :param registry: Registry customizado (opcional)
        """
        self._registry = registry or self.create_registry()
        self._registry.register_defaults()
        self._log = LogService(service_name=self.__class__.__name__)
        self._metrics = TrackMetrics()

    @property
    def registry(self) -> R:
        """Acesso ao registry."""
        return self._registry

    @property
    def log(self) -> LogService:
        """Acesso ao logger."""
        return self._log

    @property
    def metrics(self) -> TrackMetrics:
        """Acesso às métricas."""
        return self._metrics

    @abstractmethod
    def create_registry(self) -> R:
        """
        Criar instância do registry.

        Deve ser implementado por subclasses.

        Exemplo:
            def create_registry(self) -> LLMPluginRegistry:
                return LLMPluginRegistry()
        """
        pass

    @abstractmethod
    def create_context(self, spec: S) -> C:
        """
        Criar contexto de build.

        Deve ser implementado por subclasses.

        Exemplo:
            def create_context(self, spec: LLMBuildSpec) -> LLMBuildContext:
                return LLMBuildContext(spec=spec, registry=self.registry)
        """
        pass

    @abstractmethod
    def build(self, spec: S) -> T:
        """
        Construir objeto raiz a partir da spec.

        Deve ser implementado por subclasses.

        Exemplo:
            def build(self, spec: LLMBuildSpec) -> AgentBase:
                ctx = self.create_context(spec)
                provider = self._build_provider(ctx)
                session = self._build_session(ctx)
                agent = self._build_agent(ctx, provider, session)
                return agent
        """
        pass

    def build_from_yaml(self, path: str, spec_class: type[S]) -> T:
        """
        Construir a partir de arquivo YAML.

        :param path: Caminho do arquivo YAML
        :param spec_class: Classe da spec para deserialização
        :return: Objeto construído
        """
        spec = spec_class.from_yaml(path)
        return self.build(spec)

    def build_from_json(self, path: str, spec_class: type[S]) -> T:
        """
        Construir a partir de arquivo JSON.

        :param path: Caminho do arquivo JSON
        :param spec_class: Classe da spec para deserialização
        :return: Objeto construído
        """
        spec = spec_class.from_json(path)
        return self.build(spec)

    def build_from_dict(self, data: dict, spec_class: type[S]) -> T:
        """
        Construir a partir de dicionário.

        :param data: Dicionário com dados da spec
        :param spec_class: Classe da spec para deserialização
        :return: Objeto construído
        """
        spec = spec_class.from_dict(data)
        return self.build(spec)

    def _build_observability(
        self,
        ctx: C,
    ) -> tuple[LogService, TrackMetrics]:
        """
        Construir serviços de observabilidade.

        Método utilitário que pode ser usado por subclasses.
        """
        obs_config = ctx.get("observability", {})

        log = LogService(
            service_name=obs_config.get("service_name", "forge"),
            environment=obs_config.get("environment", "development"),
        )

        if obs_config.get("console_logging", True):
            log.add_console_handler()

        if log_file := obs_config.get("log_file"):
            log.add_file_handler(log_file)

        metrics = TrackMetrics()

        return log, metrics
```

***

## Exemplo de Uso em Projetos

### forge\_llm (Acesso a LLMs)

```python
# forge_llm/composition/registry.py
from forgebase.composition import PluginRegistryBase
from forge_llm.infrastructure.providers import OpenAIAdapter, AnthropicAdapter
from forge_llm.application.agents import ChatAgent, CodeAgent


class LLMPluginRegistry(PluginRegistryBase):
    def register_defaults(self) -> None:
        # Providers
        self.register("provider", "openai", OpenAIAdapter)
        self.register("provider", "anthropic", AnthropicAdapter)
        self.register("provider", "ollama", OllamaAdapter)

        # Agents
        self.register("agent", "chat", ChatAgent)
        self.register("agent", "code", CodeAgent)
        self.register("agent", "tool", ToolAgent)
```

### forge\_db (Acesso a Bancos de Dados)

```python
# forge_db/composition/registry.py
from forgebase.composition import PluginRegistryBase
from forge_db.infrastructure.repositories import PostgresRepo, MongoRepo, RedisRepo


class DBPluginRegistry(PluginRegistryBase):
    def register_defaults(self) -> None:
        # Repositories
        self.register("repository", "postgres", PostgresRepo)
        self.register("repository", "mongodb", MongoRepo)
        self.register("repository", "redis", RedisRepo)

        # Migrations
        self.register("migration", "alembic", AlembicMigrator)
        self.register("migration", "raw", RawSQLMigrator)
```

### forge\_api (APIs REST)

```python
# forge_api/composition/registry.py
from forgebase.composition import PluginRegistryBase
from forge_api.adapters.auth import JWTAuth, OAuth2Auth, APIKeyAuth


class APIPluginRegistry(PluginRegistryBase):
    def register_defaults(self) -> None:
        # Auth
        self.register("auth", "jwt", JWTAuth)
        self.register("auth", "oauth2", OAuth2Auth)
        self.register("auth", "apikey", APIKeyAuth)

        # Serializers
        self.register("serializer", "json", JSONSerializer)
        self.register("serializer", "msgpack", MsgPackSerializer)
```

***

## Benefícios da Incorporação

### Para o ForgeBase

| Benefício            | Descrição                                                   |
| -------------------- | ----------------------------------------------------------- |
| **Padrão unificado** | Todos os projetos usam a mesma infraestrutura de composição |
| **Menos duplicação** | Código de registry/builder não é reimplementado             |
| **Testabilidade**    | Classes base já vêm com suporte a testes                    |
| **Documentação**     | Um único padrão para documentar                             |

### Para Projetos Derivados

| Benefício           | Descrição                                         |
| ------------------- | ------------------------------------------------- |
| **Produtividade**   | Herdar ao invés de reimplementar                  |
| **Consistência**    | Mesmo padrão em forge\_llm, forge\_db, forge\_api |
| **Extensibilidade** | Adicionar plugins sem modificar core              |
| **Configuração**    | YAML/JSON pronto para usar                        |

### Para a Comunidade

| Benefício                | Descrição                                        |
| ------------------------ | ------------------------------------------------ |
| **Curva de aprendizado** | Aprender uma vez, usar em qualquer projeto Forge |
| **Interoperabilidade**   | Plugins de um projeto podem inspirar outros      |
| **Ecossistema**          | Base sólida para família de frameworks           |

***

## Estrutura Final do ForgeBase

```
forgebase/
├── __init__.py
│
├── domain/
│   ├── __init__.py
│   ├── entity_base.py
│   ├── value_object_base.py
│   └── exceptions.py
│
├── application/
│   ├── __init__.py
│   ├── usecase_base.py
│   ├── port_base.py
│   └── dto_base.py
│
├── adapters/
│   ├── __init__.py
│   ├── adapter_base.py
│   └── cli_adapter.py
│
├── infrastructure/
│   ├── __init__.py
│   └── repository_base.py
│
├── composition/                  ← NOVO
│   ├── __init__.py
│   ├── plugin_registry.py       # PluginRegistryBase
│   ├── build_spec.py            # BuildSpecBase
│   ├── build_context.py         # BuildContextBase
│   └── builder.py               # BuilderBase
│
├── observability/
│   ├── __init__.py
│   ├── log_service.py
│   └── track_metrics.py
│
└── testing/
    ├── __init__.py
    ├── forge_test_case.py
    └── fakes/
        └── __init__.py
```

***

## API Pública

```python
# forgebase/__init__.py

# Domain
from forgebase.domain import EntityBase, ValueObjectBase, DomainException

# Application
from forgebase.application import UseCaseBase, PortBase, DTOBase

# Adapters
from forgebase.adapters import AdapterBase, CLIAdapter

# Infrastructure
from forgebase.infrastructure import RepositoryBase

# Composition (NOVO)
from forgebase.composition import (
    PluginRegistryBase,
    BuildSpecBase,
    BuildContextBase,
    BuilderBase,
)

# Observability
from forgebase.observability import LogService, TrackMetrics

# Testing
from forgebase.testing import ForgeTestCase
```

***

## Exemplo Completo: Projeto Derivado

```python
# meu_projeto/composition/spec.py
from dataclasses import dataclass, field
from forgebase.composition import BuildSpecBase


@dataclass
class MeuBuildSpec(BuildSpecBase):
    """Spec específica do meu projeto."""

    servico: dict = field(default_factory=dict)
    database: dict = field(default_factory=dict)
    cache: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "MeuBuildSpec":
        return cls(
            servico=data.get("servico", {}),
            database=data.get("database", {}),
            cache=data.get("cache", {}),
            metadata=data.get("metadata", {}),
            observability=data.get("observability", {}),
        )

    def to_dict(self) -> dict:
        return {
            "servico": self.servico,
            "database": self.database,
            "cache": self.cache,
            "metadata": self.metadata,
            "observability": self.observability,
        }

    def validate(self) -> None:
        if not self.servico.get("type"):
            raise ConfigurationError("servico.type é obrigatório")


# meu_projeto/composition/registry.py
from forgebase.composition import PluginRegistryBase


class MeuPluginRegistry(PluginRegistryBase):
    def register_defaults(self) -> None:
        self.register("servico", "api", APIService)
        self.register("servico", "worker", WorkerService)
        self.register("database", "postgres", PostgresAdapter)
        self.register("cache", "redis", RedisAdapter)


# meu_projeto/composition/builder.py
from forgebase.composition import BuilderBase, BuildContextBase


class MeuBuilder(BuilderBase[MeuBuildSpec, MeuPluginRegistry, BuildContextBase, ServiceBase]):
    def create_registry(self) -> MeuPluginRegistry:
        return MeuPluginRegistry()

    def create_context(self, spec: MeuBuildSpec) -> BuildContextBase:
        return BuildContextBase(spec=spec, registry=self.registry)

    def build(self, spec: MeuBuildSpec) -> ServiceBase:
        spec.validate()
        ctx = self.create_context(spec)

        log, metrics = self._build_observability(ctx)
        database = self._build_database(ctx, log)
        cache = self._build_cache(ctx, log)
        service = self._build_service(ctx, database, cache, log, metrics)

        return service
```

***

## Conclusão

A incorporação do sistema de plugins ao ForgeBase:

1. **Generaliza** padrões que serão repetidos em todo projeto derivado
2. **Padroniza** a forma de criar Composition Roots
3. **Simplifica** o desenvolvimento de novos projetos na família Forge
4. **Mantém** a regra de ouro: "Quem usa não cria. Quem cria não usa."

Recomendo fortemente essa adição ao ForgeBase como parte do módulo `forgebase.composition`.

***

## Exemplo Prático: forge\_llm usando ForgeBase Composition

Este exemplo mostra exatamente como o forge\_llm usaria o sistema de plugins do ForgeBase.

### 1. Arquivo de Configuração YAML

```yaml
# configs/chat_agent.yaml
agent:
  type: chat
  system_prompt: "Você é um assistente útil."

provider:
  type: openai
  api_key_env: OPENAI_API_KEY

model:
  name: gpt-4o
  temperature: 0.7
  max_tokens: 2000

session:
  max_tokens: 8000
  strategy: truncate

observability:
  service_name: forge_llm
  console_logging: true
```

### 2. BuildSpec do forge\_llm

```python
# forge_llm/composition/spec.py
from dataclasses import dataclass, field
from forgebase.composition import BuildSpecBase
from forge_llm.domain.exceptions import ConfigurationError


@dataclass
class LLMBuildSpec(BuildSpecBase):
    """Especificação para construir agentes LLM."""

    agent: dict = field(default_factory=dict)
    provider: dict = field(default_factory=dict)
    model: dict = field(default_factory=dict)
    session: dict = field(default_factory=dict)
    tools: list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "LLMBuildSpec":
        return cls(
            agent=data.get("agent", {}),
            provider=data.get("provider", {}),
            model=data.get("model", {}),
            session=data.get("session", {}),
            tools=data.get("tools", []),
            metadata=data.get("metadata", {}),
            observability=data.get("observability", {}),
        )

    def to_dict(self) -> dict:
        return {
            "agent": self.agent,
            "provider": self.provider,
            "model": self.model,
            "session": self.session,
            "tools": self.tools,
            "metadata": self.metadata,
            "observability": self.observability,
        }

    def validate(self) -> None:
        if not self.agent.get("type"):
            raise ConfigurationError("agent.type é obrigatório")
        if not self.provider.get("type"):
            raise ConfigurationError("provider.type é obrigatório")
        if not self.model.get("name"):
            raise ConfigurationError("model.name é obrigatório")
```

### 3. Plugin Registry do forge\_llm

```python
# forge_llm/composition/registry.py
from forgebase.composition import PluginRegistryBase

# Imports dos componentes do forge_llm
from forge_llm.infrastructure.providers.openai import OpenAIProvider
from forge_llm.infrastructure.providers.anthropic import AnthropicProvider
from forge_llm.infrastructure.providers.ollama import OllamaProvider
from forge_llm.application.agents.chat_agent import ChatAgent
from forge_llm.application.agents.code_agent import CodeAgent
from forge_llm.application.agents.tool_agent import ToolAgent


class LLMPluginRegistry(PluginRegistryBase):
    """Registry de plugins do forge_llm."""

    def register_defaults(self) -> None:
        """Registrar plugins padrão."""
        # Providers de LLM
        self.register("provider", "openai", OpenAIProvider)
        self.register("provider", "anthropic", AnthropicProvider)
        self.register("provider", "ollama", OllamaProvider)

        # Tipos de Agentes
        self.register("agent", "chat", ChatAgent)
        self.register("agent", "code", CodeAgent)
        self.register("agent", "tool", ToolAgent)

        # Estratégias de sessão
        self.register("session_strategy", "truncate", TruncateStrategy)
        self.register("session_strategy", "summarize", SummarizeStrategy)
```

### 4. Builder do forge\_llm

```python
# forge_llm/composition/builder.py
from forgebase.composition import BuilderBase, BuildContextBase
from forgebase.observability import LogService, TrackMetrics

from forge_llm.composition.spec import LLMBuildSpec
from forge_llm.composition.registry import LLMPluginRegistry
from forge_llm.application.agents.base import AgentBase
from forge_llm.application.session import ChatSession
from forge_llm.domain.entities import LLMModelConfig


class ForgeBuilder(BuilderBase[LLMBuildSpec, LLMPluginRegistry, BuildContextBase, AgentBase]):
    """
    Composition Root do forge_llm.

    Monta agentes LLM a partir de configuração declarativa.
    """

    def create_registry(self) -> LLMPluginRegistry:
        return LLMPluginRegistry()

    def create_context(self, spec: LLMBuildSpec) -> BuildContextBase:
        return BuildContextBase(spec=spec, registry=self.registry)

    def build(self, spec: LLMBuildSpec) -> AgentBase:
        """Construir agente completo."""
        spec.validate()
        ctx = self.create_context(spec)

        # 1. Observabilidade
        log, metrics = self._build_observability(ctx)

        # 2. Provider (OpenAI, Anthropic, etc.)
        provider = self._build_provider(ctx, log, metrics)

        # 3. Sessão de chat
        session = self._build_session(ctx)

        # 4. Configuração do modelo
        model_config = self._build_model_config(ctx)

        # 5. Agente final
        agent = self._build_agent(ctx, provider, session, model_config, log, metrics)

        self.log.info(
            "Agent built",
            agent_type=spec.agent["type"],
            provider=spec.provider["type"],
            model=model_config.model_name,
        )

        return agent

    def _build_provider(self, ctx: BuildContextBase, log: LogService, metrics: TrackMetrics):
        """Construir provider de LLM."""
        provider_type = ctx.get("provider.type")
        provider_cls = ctx.resolve("provider", provider_type)

        # Resolver API key
        api_key = ctx.resolve_env(
            ctx.get("provider.api_key_env", "OPENAI_API_KEY")
        )

        return provider_cls(
            api_key=api_key,
            log=log,
            metrics=metrics,
        )

    def _build_session(self, ctx: BuildContextBase) -> ChatSession:
        """Construir sessão de chat."""
        max_tokens = ctx.get("session.max_tokens", 8000)
        strategy_type = ctx.get("session.strategy", "truncate")

        strategy_cls = ctx.resolve("session_strategy", strategy_type)

        return ChatSession(
            max_tokens=max_tokens,
            compaction_strategy=strategy_cls(),
        )

    def _build_model_config(self, ctx: BuildContextBase) -> LLMModelConfig:
        """Construir configuração de modelo."""
        return LLMModelConfig(
            model_name=ctx.get("model.name"),
            temperature=ctx.get("model.temperature", 0.7),
            max_tokens=ctx.get("model.max_tokens", 2000),
        )

    def _build_agent(
        self,
        ctx: BuildContextBase,
        provider,
        session: ChatSession,
        model_config: LLMModelConfig,
        log: LogService,
        metrics: TrackMetrics,
    ) -> AgentBase:
        """Construir agente."""
        agent_type = ctx.get("agent.type")
        agent_cls = ctx.resolve("agent", agent_type)

        return agent_cls(
            provider=provider,
            session=session,
            model_config=model_config,
            system_prompt=ctx.get("agent.system_prompt"),
            log=log,
            metrics=metrics,
        )
```

### 5. Uso Final (O que o desenvolvedor escreve)

```python
# main.py - Exemplo de uso simples
from forge_llm.composition import ForgeBuilder, LLMBuildSpec


# Opção 1: Via YAML
builder = ForgeBuilder()
agent = builder.build_from_yaml("configs/chat_agent.yaml", LLMBuildSpec)

response = agent.chat("Olá, como você está?")
print(response)


# Opção 2: Via dicionário (programático)
spec_dict = {
    "agent": {"type": "chat", "system_prompt": "Seja conciso."},
    "provider": {"type": "openai", "api_key_env": "OPENAI_API_KEY"},
    "model": {"name": "gpt-4o", "temperature": 0.5},
}

agent = builder.build_from_dict(spec_dict, LLMBuildSpec)
response = agent.chat("Resuma o que é Python em uma frase.")
print(response)


# Opção 3: Streaming
for chunk in agent.stream_chat("Conte uma história curta."):
    print(chunk, end="", flush=True)
```

### 6. CLI First - Testando via Terminal

```python
# forge_llm/cli.py
import sys
from forge_llm.composition import ForgeBuilder, LLMBuildSpec


def main():
    if len(sys.argv) < 3:
        print("Uso: python -m forge_llm.cli <spec.yaml> <mensagem>")
        sys.exit(1)

    spec_path = sys.argv[1]
    message = " ".join(sys.argv[2:])

    builder = ForgeBuilder()
    agent = builder.build_from_yaml(spec_path, LLMBuildSpec)

    print(f"Agent: {agent.__class__.__name__}")
    print(f"Model: {agent.model_config.model_name}")
    print("-" * 40)

    for chunk in agent.stream_chat(message):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
```

**Uso no terminal:**

```bash
# Testar agente via CLI (CLI First!)
python -m forge_llm.cli configs/chat_agent.yaml "Olá, tudo bem?"

# Listar plugins disponíveis
python -c "from forge_llm.composition import ForgeBuilder; b = ForgeBuilder(); print(b.registry.to_dict())"
# Output: {'provider': ['openai', 'anthropic', 'ollama'], 'agent': ['chat', 'code', 'tool'], ...}
```

### 7. Adicionando Novo Provider (Extensibilidade)

```python
# Terceiro cria um novo provider
# meu_provider/gemini.py
from forge_llm.application.ports import ILLMProviderPort


class GeminiProvider(ILLMProviderPort):
    """Provider para Google Gemini."""

    def __init__(self, api_key: str, log, metrics):
        self.api_key = api_key
        self.log = log
        self.metrics = metrics

    def chat(self, messages, model_config, call_config=None):
        # implementação...
        pass

    def stream_chat(self, messages, model_config, call_config=None):
        # implementação...
        pass


# Registrar o plugin
from forge_llm.composition import ForgeBuilder

builder = ForgeBuilder()
builder.registry.register("provider", "gemini", GeminiProvider)

# Agora funciona!
agent = builder.build_from_dict({
    "agent": {"type": "chat"},
    "provider": {"type": "gemini", "api_key_env": "GEMINI_API_KEY"},  # ← novo!
    "model": {"name": "gemini-pro"},
}, LLMBuildSpec)
```

### 8. Teste Unitário do Builder

```python
# tests/test_builder.py
import pytest
from forge_llm.composition import ForgeBuilder, LLMBuildSpec
from tests.fakes import FakeProvider


def test_build_agent_from_dict():
    """Builder deve criar agente a partir de dicionário."""
    builder = ForgeBuilder()

    # Registrar fake provider para testes
    builder.registry.register("provider", "fake", FakeProvider)

    spec_dict = {
        "agent": {"type": "chat", "system_prompt": "Test"},
        "provider": {"type": "fake"},
        "model": {"name": "test-model"},
    }

    agent = builder.build_from_dict(spec_dict, LLMBuildSpec)

    assert agent is not None
    assert agent.model_config.model_name == "test-model"


def test_resolve_unknown_provider_raises():
    """Resolver provider desconhecido deve falhar."""
    builder = ForgeBuilder()

    spec_dict = {
        "agent": {"type": "chat"},
        "provider": {"type": "nao_existe"},
        "model": {"name": "test"},
    }

    with pytest.raises(KeyError, match="nao_existe"):
        builder.build_from_dict(spec_dict, LLMBuildSpec)


def test_registry_lists_plugins():
    """Registry deve listar plugins registrados."""
    builder = ForgeBuilder()

    providers = builder.registry.list("provider")
    agents = builder.registry.list("agent")

    assert "openai" in providers
    assert "anthropic" in providers
    assert "chat" in agents
    assert "code" in agents
```

***

## Diagrama de Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│                         DESENVOLVEDOR                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  chat_agent.yaml                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ agent:                                                   │   │
│  │   type: chat                                             │   │
│  │ provider:                                                │   │
│  │   type: openai                                           │   │
│  │ model:                                                   │   │
│  │   name: gpt-4o                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ForgeBuilder.build_from_yaml("chat_agent.yaml", LLMBuildSpec)  │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ LLMBuildSpec    │ │ LLMPluginRegistry│ │ BuildContext    │
│ .from_yaml()    │ │ .resolve()       │ │ .get()          │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ OpenAIProvider  │ │ ChatSession     │ │ LLMModelConfig  │
│ (from registry) │ │ (built)         │ │ (built)         │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ChatAgent(provider, session, model_config, log, metrics)       │
│  ← Pronto para uso!                                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  agent.chat("Olá!")  →  "Olá! Como posso ajudar?"              │
└─────────────────────────────────────────────────────────────────┘
```

***

## Próximos Passos

1. **Review** desta proposta pela equipe ForgeBase
2. **Implementação** das classes base em `forgebase/composition/`
3. **Testes** unitários e de integração
4. **Documentação** no guia de usuários
5. **Migração** do forge\_llm para usar as novas classes base
6. **Publicação** de nova versão do ForgeBase (v0.2.0?)
