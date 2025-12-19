# Proposta v3: Sistema de Plugins para ForgeBase

> "Extensibilidade sem modificar o núcleo."

Este documento é a versão refinada da proposta de sistema de plugins, incorporando feedback da revisão técnica.

---

## Changelog da v3

| Alteração | Motivo |
|-----------|--------|
| Renomeado `forgebase` → `forge_base` | Alinhamento com rename do módulo |
| Adicionado suporte a TOML | Python 3.11+ tem `tomllib` nativo |
| Removido `Generic[T]` do Registry | Não adicionava valor, simplifica código |
| Criado `protocols.py` | Baixo acoplamento com observability |
| Import de `os` movido para topo | Seguir padrão Python |
| Renomeado `env` → `env_overrides` | Clareza de propósito |
| Adicionado método `with_env()` | Imutabilidade e testabilidade |
| Adicionado `ConfigurationError` | Exception que faltava |
| Adicionado `from_file()` | Auto-detecção de formato |
| Adicionado `resolve_and_instantiate()` | Conveniência no registry |

---

## Estrutura Final

```
forge_base/
├── composition/                  ← NOVO MÓDULO
│   ├── __init__.py
│   ├── protocols.py              # Interfaces de baixo acoplamento
│   ├── plugin_registry.py        # PluginRegistryBase
│   ├── build_spec.py             # BuildSpecBase
│   ├── build_context.py          # BuildContextBase
│   └── builder.py                # BuilderBase
│
├── domain/
│   └── exceptions.py             # + ConfigurationError
│
└── ... (resto inalterado)
```

---

## Componentes

### 1. Protocols (NOVO)

```python
# forge_base/composition/protocols.py
"""
Protocols para composição - baixo acoplamento.

Define interfaces mínimas que o sistema de composição espera.
Permite injeção de implementações customizadas para logging e métricas.
"""

from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class LoggerProtocol(Protocol):
    """
    Interface mínima para logging.

    Qualquer objeto com estes métodos pode ser usado como logger.
    LogService do forge_base implementa esta interface.

    :Example:
        class MyLogger:
            def info(self, message: str, **kwargs): print(f"INFO: {message}")
            def warning(self, message: str, **kwargs): print(f"WARN: {message}")
            def error(self, message: str, **kwargs): print(f"ERROR: {message}")
            def debug(self, message: str, **kwargs): print(f"DEBUG: {message}")

        builder = MyBuilder(log=MyLogger())
    """

    def info(self, message: str, **kwargs: Any) -> None:
        """Log informativo."""
        ...

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log de aviso."""
        ...

    def error(self, message: str, **kwargs: Any) -> None:
        """Log de erro."""
        ...

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log de debug."""
        ...


@runtime_checkable
class MetricsProtocol(Protocol):
    """
    Interface mínima para métricas.

    Qualquer objeto com estes métodos pode ser usado para métricas.
    TrackMetrics do forge_base implementa esta interface.

    :Example:
        class MyMetrics:
            def increment(self, name: str, value: int = 1, **tags): pass
            def timing(self, name: str, value: float, **tags): pass

        builder = MyBuilder(metrics=MyMetrics())
    """

    def increment(self, name: str, value: int = 1, **tags: Any) -> None:
        """Incrementar contador."""
        ...

    def timing(self, name: str, value: float, **tags: Any) -> None:
        """Registrar tempo de execução."""
        ...
```

### 2. PluginRegistryBase

```python
# forge_base/composition/plugin_registry.py
"""
Registro genérico de plugins.

Mapeia (kind, type_id) → classe concreta ou factory.
Permite extensibilidade sem modificar código existente.
"""

from typing import Any, Callable
from abc import ABC, abstractmethod


# Type aliases para clareza
PluginClass = type
PluginFactory = Callable[..., Any]
PluginEntry = PluginClass | PluginFactory


class PluginRegistryBase(ABC):
    """
    Registro central de extensibilidade.

    Mapeia (kind, type_id) → classe concreta ou factory.

    Exemplos de uso em projetos derivados:
    - forge_llm: ("provider", "openai") → OpenAIAdapter
    - forge_db: ("repository", "postgres") → PostgresRepository
    - forge_api: ("auth", "jwt") → JWTAuthAdapter

    Subclasses devem implementar register_defaults() para
    registrar os plugins padrão do projeto.

    :Example:
        class LLMRegistry(PluginRegistryBase):
            def register_defaults(self) -> None:
                self.register("provider", "openai", OpenAIProvider)
                self.register("provider", "anthropic", AnthropicProvider)

        registry = LLMRegistry()
        provider_cls = registry.resolve("provider", "openai")
        provider = provider_cls(api_key="sk-...")
    """

    def __init__(self) -> None:
        self._registry: dict[str, dict[str, PluginEntry]] = {}

    def register(
        self,
        kind: str,
        type_id: str,
        plugin: PluginEntry,
    ) -> None:
        """
        Registrar um plugin.

        :param kind: Categoria do plugin (ex: "provider", "agent", "repository")
        :param type_id: Identificador do tipo (ex: "openai", "chat", "postgres")
        :param plugin: Classe ou factory function
        """
        if kind not in self._registry:
            self._registry[kind] = {}
        self._registry[kind][type_id] = plugin

    def unregister(self, kind: str, type_id: str) -> bool:
        """
        Remover um plugin do registro.

        :param kind: Categoria do plugin
        :param type_id: Identificador do tipo
        :return: True se removido, False se não existia
        """
        if kind in self._registry and type_id in self._registry[kind]:
            del self._registry[kind][type_id]
            return True
        return False

    def resolve(self, kind: str, type_id: str) -> PluginEntry:
        """
        Resolver um plugin pelo kind e type_id.

        :param kind: Categoria do plugin
        :param type_id: Identificador do tipo
        :return: Classe ou factory registrada
        :raises KeyError: Se não encontrado
        """
        if kind not in self._registry:
            available_kinds = list(self._registry.keys())
            raise KeyError(
                f"Plugin kind '{kind}' não registrado. "
                f"Kinds disponíveis: {available_kinds}"
            )

        if type_id not in self._registry[kind]:
            available = list(self._registry[kind].keys())
            raise KeyError(
                f"Plugin '{kind}/{type_id}' não encontrado. "
                f"Disponíveis para '{kind}': {available}"
            )

        return self._registry[kind][type_id]

    def resolve_and_instantiate(
        self,
        kind: str,
        type_id: str,
        **kwargs: Any,
    ) -> Any:
        """
        Resolver e instanciar plugin com argumentos.

        Conveniência para casos onde você quer resolver e criar
        o objeto em uma única chamada.

        :param kind: Categoria do plugin
        :param type_id: Identificador do tipo
        :param kwargs: Argumentos para o construtor/factory
        :return: Instância do plugin

        :Example:
            provider = registry.resolve_and_instantiate(
                "provider", "openai",
                api_key="sk-...",
                log=log_service,
            )
        """
        plugin = self.resolve(kind, type_id)
        return plugin(**kwargs)

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

        :Example:
            def register_defaults(self) -> None:
                self.register("provider", "openai", OpenAIAdapter)
                self.register("provider", "anthropic", AnthropicAdapter)
                self.register("agent", "chat", ChatAgent)
        """
        pass

    def to_dict(self) -> dict[str, list[str]]:
        """
        Serializar registro para debug/introspection.

        :return: Dicionário {kind: [type_ids]}
        """
        return {
            kind: list(plugins.keys())
            for kind, plugins in self._registry.items()
        }

    def __repr__(self) -> str:
        total = sum(len(plugins) for plugins in self._registry.values())
        return f"<{self.__class__.__name__} kinds={len(self._registry)} plugins={total}>"
```

### 3. BuildSpecBase

```python
# forge_base/composition/build_spec.py
"""
Especificação declarativa genérica.

Define O QUE deve ser construído, não COMO.
Suporta YAML, JSON e TOML como formatos de entrada.
"""

from typing import TypeVar
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from pathlib import Path
import json

import yaml

# TOML é stdlib no Python 3.11+
import tomllib


T = TypeVar("T", bound="BuildSpecBase")


@dataclass
class BuildSpecBase(ABC):
    """
    Especificação declarativa para construção de objetos.

    Define O QUE deve ser construído, não COMO.
    O Builder é responsável por interpretar a spec.

    Subclasses devem definir os campos específicos do projeto.

    :Example:
        @dataclass
        class LLMBuildSpec(BuildSpecBase):
            agent: dict = field(default_factory=dict)
            provider: dict = field(default_factory=dict)
            model: dict = field(default_factory=dict)

        spec = LLMBuildSpec.from_file("config.yaml")
    """

    # Campos comuns a todos os projetos
    metadata: dict = field(default_factory=dict)
    observability: dict = field(default_factory=dict)

    @classmethod
    def from_file(cls: type[T], path: str | Path) -> T:
        """
        Carregar spec detectando formato pela extensão.

        Formatos suportados: .yaml, .yml, .json, .toml

        :param path: Caminho do arquivo
        :return: Instância da spec
        :raises ValueError: Se formato não suportado
        :raises FileNotFoundError: Se arquivo não existe
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo de spec não encontrado: {path}")

        suffix = path.suffix.lower()

        loaders: dict[str, callable] = {
            ".yaml": cls.from_yaml,
            ".yml": cls.from_yaml,
            ".json": cls.from_json,
            ".toml": cls.from_toml,
        }

        if suffix not in loaders:
            supported = ", ".join(loaders.keys())
            raise ValueError(
                f"Formato '{suffix}' não suportado. "
                f"Use: {supported}"
            )

        return loaders[suffix](path)

    @classmethod
    def from_yaml(cls: type[T], path: str | Path) -> T:
        """
        Carregar spec de arquivo YAML.

        :param path: Caminho do arquivo
        :return: Instância da spec
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data or {})

    @classmethod
    def from_json(cls: type[T], path: str | Path) -> T:
        """
        Carregar spec de arquivo JSON.

        :param path: Caminho do arquivo
        :return: Instância da spec
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)

    @classmethod
    def from_toml(cls: type[T], path: str | Path) -> T:
        """
        Carregar spec de arquivo TOML.

        Disponível nativamente no Python 3.11+.

        :param path: Caminho do arquivo
        :return: Instância da spec
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        with open(path, "rb") as f:
            data = tomllib.load(f)

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
        """Serializar para string YAML."""
        return yaml.dump(self.to_dict(), default_flow_style=False, allow_unicode=True)

    def to_json(self, indent: int = 2) -> str:
        """Serializar para string JSON."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @abstractmethod
    def validate(self) -> None:
        """
        Validar a spec.

        Deve levantar ConfigurationError se inválida.

        :raises ConfigurationError: Se spec inválida
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} metadata={self.metadata}>"
```

### 4. BuildContextBase

```python
# forge_base/composition/build_context.py
"""
Contexto de build genérico.

Mantém estado durante o processo de construção.
"""

import os
from typing import TypeVar, Generic, Any
from dataclasses import dataclass, field

from forge_base.composition.build_spec import BuildSpecBase
from forge_base.composition.plugin_registry import PluginRegistryBase
from forge_base.domain.exceptions import ConfigurationError


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
    - Overrides de variáveis de ambiente

    O cache permite reutilizar objetos (singleton por build).

    :Example:
        ctx = BuildContextBase(spec=my_spec, registry=my_registry)

        # Com overrides de ambiente (útil para testes)
        ctx = ctx.with_env(API_KEY="test-key")
    """

    spec: S
    registry: R
    cache: dict[str, Any] = field(default_factory=dict)
    env_overrides: dict[str, str] = field(default_factory=dict)

    def get(self, path: str, default: Any = None) -> Any:
        """
        Obter valor da spec por path.

        Suporta notação de ponto: "provider.type", "model.temperature"

        :param path: Caminho no formato "key.subkey.subsubkey"
        :param default: Valor padrão se não encontrado
        :return: Valor encontrado ou default

        :Example:
            provider_type = ctx.get("provider.type")
            temperature = ctx.get("model.temperature", 0.7)
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

        Ordem de precedência:
        1. env_overrides (passado via with_env ou construtor)
        2. os.environ (sistema)

        :param env_var: Nome da variável
        :param required: Se True, levanta erro se não definida
        :return: Valor da variável ou None
        :raises ConfigurationError: Se required=True e variável não existe
        """
        # 1. Verifica overrides locais (útil para testes)
        if env_var in self.env_overrides:
            return self.env_overrides[env_var]

        # 2. Verifica ambiente do sistema
        value = os.environ.get(env_var)

        if value is None and required:
            raise ConfigurationError(
                f"Variável de ambiente '{env_var}' não definida. "
                f"Defina-a no sistema ou passe via with_env()."
            )

        return value

    def with_env(self, **env_vars: str) -> "BuildContextBase[S, R]":
        """
        Criar novo contexto com variáveis de ambiente adicionais.

        Retorna uma nova instância, preservando imutabilidade.
        Útil para testes e configuração programática.

        :param env_vars: Variáveis de ambiente como kwargs
        :return: Novo contexto com os overrides

        :Example:
            # Para testes
            test_ctx = ctx.with_env(
                OPENAI_API_KEY="sk-test-123",
                DATABASE_URL="sqlite:///:memory:"
            )
        """
        new_overrides = {**self.env_overrides, **env_vars}
        return BuildContextBase(
            spec=self.spec,
            registry=self.registry,
            cache=self.cache.copy(),
            env_overrides=new_overrides,
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"spec={self.spec.__class__.__name__} "
            f"cached={len(self.cache)} "
            f"env_overrides={len(self.env_overrides)}>"
        )
```

### 5. BuilderBase

```python
# forge_base/composition/builder.py
"""
Builder genérico (Composition Root).

O único lugar onde objetos são criados.
Segue a regra: "Quem usa não cria. Quem cria não usa."
"""

from typing import TypeVar, Generic, Any
from abc import ABC, abstractmethod

from forge_base.composition.protocols import LoggerProtocol, MetricsProtocol
from forge_base.composition.build_spec import BuildSpecBase
from forge_base.composition.build_context import BuildContextBase
from forge_base.composition.plugin_registry import PluginRegistryBase


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

    :Example:
        class LLMBuilder(BuilderBase[LLMSpec, LLMRegistry, BuildContextBase, Agent]):
            def create_registry(self) -> LLMRegistry:
                return LLMRegistry()

            def create_context(self, spec: LLMSpec) -> BuildContextBase:
                return BuildContextBase(spec=spec, registry=self.registry)

            def build(self, spec: LLMSpec) -> Agent:
                ctx = self.create_context(spec)
                provider = self._build_provider(ctx)
                return self._build_agent(ctx, provider)
    """

    def __init__(
        self,
        registry: R | None = None,
        log: LoggerProtocol | None = None,
        metrics: MetricsProtocol | None = None,
    ):
        """
        Inicializar builder.

        :param registry: Registry customizado (opcional)
        :param log: Logger customizado (opcional, usa LogService por padrão)
        :param metrics: Métricas customizadas (opcional, usa TrackMetrics por padrão)
        """
        self._registry = registry or self.create_registry()
        self._registry.register_defaults()
        self._log = log or self._create_default_logger()
        self._metrics = metrics or self._create_default_metrics()

    def _create_default_logger(self) -> LoggerProtocol:
        """Criar logger padrão via lazy import."""
        from forge_base.observability.log_service import LogService
        return LogService(service_name=self.__class__.__name__)

    def _create_default_metrics(self) -> MetricsProtocol:
        """Criar métricas padrão via lazy import."""
        from forge_base.observability.track_metrics import TrackMetrics
        return TrackMetrics()

    @property
    def registry(self) -> R:
        """Acesso ao registry."""
        return self._registry

    @property
    def log(self) -> LoggerProtocol:
        """Acesso ao logger."""
        return self._log

    @property
    def metrics(self) -> MetricsProtocol:
        """Acesso às métricas."""
        return self._metrics

    @abstractmethod
    def create_registry(self) -> R:
        """
        Criar instância do registry.

        Deve ser implementado por subclasses.

        :Example:
            def create_registry(self) -> LLMPluginRegistry:
                return LLMPluginRegistry()
        """
        pass

    @abstractmethod
    def create_context(self, spec: S) -> C:
        """
        Criar contexto de build.

        Deve ser implementado por subclasses.

        :Example:
            def create_context(self, spec: LLMBuildSpec) -> BuildContextBase:
                return BuildContextBase(spec=spec, registry=self.registry)
        """
        pass

    @abstractmethod
    def build(self, spec: S) -> T:
        """
        Construir objeto raiz a partir da spec.

        Deve ser implementado por subclasses.

        :Example:
            def build(self, spec: LLMBuildSpec) -> AgentBase:
                spec.validate()
                ctx = self.create_context(spec)
                provider = self._build_provider(ctx)
                session = self._build_session(ctx)
                agent = self._build_agent(ctx, provider, session)
                return agent
        """
        pass

    def build_from_file(self, path: str, spec_class: type[S]) -> T:
        """
        Construir a partir de arquivo (auto-detecta formato).

        Suporta: .yaml, .yml, .json, .toml

        :param path: Caminho do arquivo
        :param spec_class: Classe da spec para deserialização
        :return: Objeto construído
        """
        spec = spec_class.from_file(path)
        return self.build(spec)

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

    def build_from_toml(self, path: str, spec_class: type[S]) -> T:
        """
        Construir a partir de arquivo TOML.

        :param path: Caminho do arquivo TOML
        :param spec_class: Classe da spec para deserialização
        :return: Objeto construído
        """
        spec = spec_class.from_toml(path)
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
    ) -> tuple[LoggerProtocol, MetricsProtocol]:
        """
        Construir serviços de observabilidade.

        Método utilitário que pode ser usado por subclasses.
        Usa as instâncias injetadas no construtor ou cria novas
        baseado na configuração da spec.

        :param ctx: Contexto de build
        :return: Tuple (logger, metrics)
        """
        obs_config = ctx.get("observability", {})

        # Se não há config específica, usa os defaults do builder
        if not obs_config:
            return self._log, self._metrics

        # Cria novos baseado na config
        from forge_base.observability.log_service import LogService
        from forge_base.observability.track_metrics import TrackMetrics

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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} registry={self._registry}>"
```

### 6. ConfigurationError (Adição ao exceptions.py)

```python
# Adicionar ao forge_base/domain/exceptions.py

class ConfigurationError(DomainException):
    """
    Raised when configuration is invalid or missing.

    Use this for configuration-related errors such as missing
    environment variables, invalid spec files, or malformed settings.

    :Example:
        if not config.get("api_key"):
            raise ConfigurationError("API key is required")

        if port < 1 or port > 65535:
            raise ConfigurationError(f"Invalid port: {port}")
    """
    pass
```

### 7. Module __init__.py

```python
# forge_base/composition/__init__.py
"""
Composition module for ForgeBase.

Provides infrastructure for building extensible applications using
the Composition Root pattern. Allows declarative configuration
and plugin-based extensibility.

Key components:
- PluginRegistryBase: Registry for plugins (classes/factories)
- BuildSpecBase: Declarative specification for building objects
- BuildContextBase: Context during build process
- BuilderBase: Composition Root that assembles objects

Philosophy:
    "Quem usa não cria. Quem cria não usa."
    (Who uses doesn't create. Who creates doesn't use.)

Example:
    from forge_base.composition import (
        PluginRegistryBase,
        BuildSpecBase,
        BuildContextBase,
        BuilderBase,
    )

    # 1. Define your registry
    class MyRegistry(PluginRegistryBase):
        def register_defaults(self) -> None:
            self.register("service", "api", APIService)

    # 2. Define your spec
    @dataclass
    class MySpec(BuildSpecBase):
        service: dict = field(default_factory=dict)

        @classmethod
        def from_dict(cls, data: dict) -> "MySpec":
            return cls(service=data.get("service", {}))

        def to_dict(self) -> dict:
            return {"service": self.service}

        def validate(self) -> None:
            if not self.service.get("type"):
                raise ConfigurationError("service.type required")

    # 3. Define your builder
    class MyBuilder(BuilderBase[MySpec, MyRegistry, BuildContextBase, Service]):
        def create_registry(self) -> MyRegistry:
            return MyRegistry()

        def create_context(self, spec: MySpec) -> BuildContextBase:
            return BuildContextBase(spec=spec, registry=self.registry)

        def build(self, spec: MySpec) -> Service:
            spec.validate()
            ctx = self.create_context(spec)
            service_cls = ctx.resolve("service", ctx.get("service.type"))
            return service_cls()

    # 4. Use it
    builder = MyBuilder()
    service = builder.build_from_file("config.yaml", MySpec)
"""

from forge_base.composition.protocols import LoggerProtocol, MetricsProtocol
from forge_base.composition.plugin_registry import PluginRegistryBase
from forge_base.composition.build_spec import BuildSpecBase
from forge_base.composition.build_context import BuildContextBase
from forge_base.composition.builder import BuilderBase

__all__ = [
    # Protocols
    "LoggerProtocol",
    "MetricsProtocol",
    # Core classes
    "PluginRegistryBase",
    "BuildSpecBase",
    "BuildContextBase",
    "BuilderBase",
]
```

---

## Exemplo Prático: forge_llm usando v3

### config.yaml

```yaml
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

observability:
  service_name: forge_llm
  console_logging: true
```

### Uso

```python
from forge_llm.composition import ForgeBuilder, LLMBuildSpec

# Via arquivo (auto-detecta formato)
builder = ForgeBuilder()
agent = builder.build_from_file("config.yaml", LLMBuildSpec)

# Via dicionário
agent = builder.build_from_dict({
    "agent": {"type": "chat"},
    "provider": {"type": "openai"},
    "model": {"name": "gpt-4o"},
}, LLMBuildSpec)

# Usar o agente
response = agent.chat("Olá!")
print(response)
```

### Testes com Mocks

```python
import pytest
from forge_llm.composition import ForgeBuilder, LLMBuildSpec


class FakeLogger:
    """Logger fake para testes."""
    def __init__(self):
        self.messages = []

    def info(self, msg, **kwargs):
        self.messages.append(("info", msg, kwargs))

    def warning(self, msg, **kwargs):
        self.messages.append(("warning", msg, kwargs))

    def error(self, msg, **kwargs):
        self.messages.append(("error", msg, kwargs))

    def debug(self, msg, **kwargs):
        self.messages.append(("debug", msg, kwargs))


class FakeMetrics:
    """Métricas fake para testes."""
    def __init__(self):
        self.counters = {}
        self.timings = {}

    def increment(self, name, value=1, **tags):
        self.counters[name] = self.counters.get(name, 0) + value

    def timing(self, name, value, **tags):
        self.timings[name] = value


def test_builder_with_fake_observability():
    """Builder aceita logger e metrics customizados."""
    fake_log = FakeLogger()
    fake_metrics = FakeMetrics()

    builder = ForgeBuilder(log=fake_log, metrics=fake_metrics)

    # Registrar fake provider para evitar chamadas reais
    builder.registry.register("provider", "fake", FakeProvider)

    spec = LLMBuildSpec.from_dict({
        "agent": {"type": "chat"},
        "provider": {"type": "fake"},
        "model": {"name": "test"},
    })

    agent = builder.build(spec)

    assert agent is not None
    assert len(fake_log.messages) > 0  # Builder logou algo


def test_context_with_env_overrides():
    """Contexto permite override de variáveis de ambiente."""
    spec = LLMBuildSpec.from_dict({"agent": {"type": "chat"}})
    registry = LLMRegistry()

    ctx = BuildContextBase(spec=spec, registry=registry)

    # Criar contexto com API key fake (não precisa variável real)
    test_ctx = ctx.with_env(OPENAI_API_KEY="sk-fake-for-testing")

    api_key = test_ctx.resolve_env("OPENAI_API_KEY")
    assert api_key == "sk-fake-for-testing"
```

---

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FORGE_BASE v0.2.0                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        composition/ (NOVO)                          │   │
│  │                                                                     │   │
│  │   ┌─────────────────┐    ┌─────────────────┐    ┌───────────────┐  │   │
│  │   │   protocols.py  │    │ plugin_registry │    │  build_spec   │  │   │
│  │   │                 │    │      .py        │    │     .py       │  │   │
│  │   │ LoggerProtocol  │    │                 │    │               │  │   │
│  │   │ MetricsProtocol │    │ PluginRegistry  │    │ BuildSpecBase │  │   │
│  │   │                 │    │     Base        │    │               │  │   │
│  │   └────────┬────────┘    └────────┬────────┘    └───────┬───────┘  │   │
│  │            │                      │                     │          │   │
│  │            │              ┌───────┴───────┐             │          │   │
│  │            │              │               │             │          │   │
│  │            ▼              ▼               ▼             ▼          │   │
│  │   ┌─────────────────────────────────────────────────────────────┐ │   │
│  │   │                      builder.py                              │ │   │
│  │   │                                                              │ │   │
│  │   │  BuilderBase[S, R, C, T]                                     │ │   │
│  │   │    - log: LoggerProtocol                                     │ │   │
│  │   │    - metrics: MetricsProtocol                                │ │   │
│  │   │    - registry: R (PluginRegistryBase)                        │ │   │
│  │   │    + build(spec: S) → T                                      │ │   │
│  │   │    + build_from_file(path, spec_class) → T                   │ │   │
│  │   │                                                              │ │   │
│  │   └─────────────────────────────────────────────────────────────┘ │   │
│  │                              │                                     │   │
│  │                              ▼                                     │   │
│  │   ┌─────────────────────────────────────────────────────────────┐ │   │
│  │   │                   build_context.py                           │ │   │
│  │   │                                                              │ │   │
│  │   │  BuildContextBase[S, R]                                      │ │   │
│  │   │    - spec: S                                                 │ │   │
│  │   │    - registry: R                                             │ │   │
│  │   │    - cache: dict                                             │ │   │
│  │   │    - env_overrides: dict                                     │ │   │
│  │   │    + get(path) → Any                                         │ │   │
│  │   │    + resolve_env(var) → str                                  │ │   │
│  │   │    + with_env(**vars) → BuildContextBase                     │ │   │
│  │   │                                                              │ │   │
│  │   └─────────────────────────────────────────────────────────────┘ │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   domain/    │  │ application/ │  │  adapters/   │  │observability/│    │
│  │              │  │              │  │              │  │              │    │
│  │ EntityBase   │  │ UseCaseBase  │  │ AdapterBase  │  │ LogService   │    │
│  │ ValueObject  │  │ PortBase     │  │ CLIAdapter   │  │ TrackMetrics │    │
│  │ exceptions   │  │ DTOBase      │  │ HTTPAdapter  │  │              │    │
│  │ +ConfigError │  │              │  │              │  │              │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROJETO DERIVADO (ex: forge_llm)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         composition/                                  │  │
│  │                                                                       │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │  LLMRegistry    │  │  LLMBuildSpec   │  │    ForgeBuilder     │   │  │
│  │  │  (extends       │  │  (extends       │  │    (extends         │   │  │
│  │  │   PluginRegistry│  │   BuildSpecBase)│  │     BuilderBase)    │   │  │
│  │  │   Base)         │  │                 │  │                     │   │  │
│  │  │                 │  │  - agent: dict  │  │  + build() → Agent  │   │  │
│  │  │  + register_    │  │  - provider:dict│  │  + _build_provider()│   │  │
│  │  │    defaults()   │  │  - model: dict  │  │  + _build_session() │   │  │
│  │  │                 │  │                 │  │                     │   │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │  │
│  │                                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama de Fluxo: Build de um Agente

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DESENVOLVEDOR                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 1. Cria arquivo de configuração
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  config.yaml / config.json / config.toml                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ agent:                                                                 │  │
│  │   type: chat                                                           │  │
│  │   system_prompt: "Você é um assistente útil."                          │  │
│  │                                                                        │  │
│  │ provider:                                                              │  │
│  │   type: openai                                                         │  │
│  │   api_key_env: OPENAI_API_KEY                                          │  │
│  │                                                                        │  │
│  │ model:                                                                 │  │
│  │   name: gpt-4o                                                         │  │
│  │   temperature: 0.7                                                     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 2. Chama builder
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  builder = ForgeBuilder()                                                   │
│  agent = builder.build_from_file("config.yaml", LLMBuildSpec)               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│  BuildSpecBase  │     │  PluginRegistryBase │     │ BuildContextBase│
│  .from_file()   │     │                     │     │                 │
│                 │     │  resolve("provider",│     │  .get("model.   │
│  Auto-detecta:  │     │          "openai")  │     │    temperature")│
│  .yaml → YAML   │     │         ↓           │     │        ↓        │
│  .json → JSON   │     │  OpenAIProvider     │     │      0.7        │
│  .toml → TOML   │     │                     │     │                 │
└─────────────────┘     └─────────────────────┘     └─────────────────┘
          │                         │                         │
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                                    │ 3. Builder monta o grafo
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ForgeBuilder.build()                                                       │
│                                                                             │
│    ┌─────────────────────────────────────────────────────────────────────┐  │
│    │  1. spec.validate()           # Valida configuração                 │  │
│    │  2. ctx = create_context()    # Cria contexto                       │  │
│    │  3. log, metrics = _build_observability(ctx)                        │  │
│    │  4. provider = _build_provider(ctx, log, metrics)                   │  │
│    │  5. session = _build_session(ctx)                                   │  │
│    │  6. model_config = _build_model_config(ctx)                         │  │
│    │  7. agent = _build_agent(ctx, provider, session, model_config)      │  │
│    │  8. return agent                                                    │  │
│    └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 4. Retorna objeto pronto
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  ChatAgent                                                                  │
│    ├── provider: OpenAIProvider                                             │
│    ├── session: ChatSession                                                 │
│    ├── model_config: LLMModelConfig                                         │
│    ├── log: LogService                                                      │
│    └── metrics: TrackMetrics                                                │
│                                                                             │
│  Pronto para uso!                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 5. Desenvolvedor usa o agente
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  response = agent.chat("Olá!")                                              │
│  # → "Olá! Como posso ajudar você hoje?"                                    │
│                                                                             │
│  for chunk in agent.stream_chat("Conte uma história"):                      │
│      print(chunk, end="")                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama de Dependências

```
                    ┌─────────────────────────────┐
                    │      protocols.py           │
                    │                             │
                    │  - LoggerProtocol           │
                    │  - MetricsProtocol          │
                    │                             │
                    │  (sem dependências)         │
                    └─────────────────────────────┘
                                  ▲
                                  │ usa
                    ┌─────────────┴───────────────┐
                    │                             │
    ┌───────────────┴───────┐         ┌──────────┴────────────┐
    │  plugin_registry.py   │         │     builder.py        │
    │                       │         │                       │
    │  - PluginRegistryBase │         │  - BuilderBase        │
    │                       │         │                       │
    │  (sem dependências)   │         │  usa:                 │
    └───────────────────────┘         │  - protocols          │
              ▲                       │  - plugin_registry    │
              │                       │  - build_spec         │
              │                       │  - build_context      │
              │                       └───────────────────────┘
              │                                   ▲
              │                                   │ usa
    ┌─────────┴─────────────┐         ┌──────────┴────────────┐
    │   build_spec.py       │         │   build_context.py    │
    │                       │         │                       │
    │  - BuildSpecBase      │         │  - BuildContextBase   │
    │                       │         │                       │
    │  usa:                 │◄────────│  usa:                 │
    │  - yaml               │         │  - build_spec         │
    │  - json               │         │  - plugin_registry    │
    │  - tomllib            │         │  - exceptions         │
    └───────────────────────┘         └───────────────────────┘
                                                  │
                                                  │ usa
                                                  ▼
                              ┌─────────────────────────────┐
                              │   domain/exceptions.py      │
                              │                             │
                              │  + ConfigurationError       │
                              │                             │
                              └─────────────────────────────┘
```

---

## Plano de Implementação

### Fase 1: Preparação

| # | Tarefa | Arquivo | Descrição |
|---|--------|---------|-----------|
| 1.1 | Criar diretório | `src/forge_base/composition/` | Criar estrutura de pastas |
| 1.2 | Adicionar exception | `domain/exceptions.py` | Adicionar `ConfigurationError` |

### Fase 2: Implementação Core (ordem de dependência)

| # | Tarefa | Arquivo | Dependências |
|---|--------|---------|--------------|
| 2.1 | Implementar protocols | `composition/protocols.py` | Nenhuma |
| 2.2 | Implementar registry | `composition/plugin_registry.py` | Nenhuma |
| 2.3 | Implementar spec | `composition/build_spec.py` | Nenhuma |
| 2.4 | Implementar context | `composition/build_context.py` | 2.2, 2.3, 1.2 |
| 2.5 | Implementar builder | `composition/builder.py` | 2.1, 2.2, 2.3, 2.4 |
| 2.6 | Implementar __init__ | `composition/__init__.py` | 2.1-2.5 |

### Fase 3: Integração

| # | Tarefa | Arquivo | Descrição |
|---|--------|---------|-----------|
| 3.1 | Atualizar exports | `forge_base/__init__.py` | Exportar novos módulos |
| 3.2 | Verificar imports | - | Garantir que tudo importa corretamente |

### Fase 4: Testes

| # | Tarefa | Arquivo | Descrição |
|---|--------|---------|-----------|
| 4.1 | Testes protocols | `tests/unit/composition/test_protocols.py` | Testar structural typing |
| 4.2 | Testes registry | `tests/unit/composition/test_plugin_registry.py` | Testar register/resolve |
| 4.3 | Testes spec | `tests/unit/composition/test_build_spec.py` | Testar YAML/JSON/TOML |
| 4.4 | Testes context | `tests/unit/composition/test_build_context.py` | Testar get/resolve_env |
| 4.5 | Testes builder | `tests/unit/composition/test_builder.py` | Testar build flow |
| 4.6 | Teste integração | `tests/integration/test_composition_integration.py` | Fluxo completo |

### Fase 5: Documentação e Release

| # | Tarefa | Descrição |
|---|--------|-----------|
| 5.1 | Atualizar README | Mencionar novo módulo composition |
| 5.2 | Criar guia | `docs/usuarios/composition-guide.md` |
| 5.3 | Atualizar CHANGELOG | Documentar mudanças da v0.2.0 |
| 5.4 | Bump version | Atualizar para 0.2.0 no pyproject.toml |
| 5.5 | Tag release | `git tag v0.2.0` |

---

## Ordem de Execução (Sequencial)

```
1. Criar diretório composition/
2. Adicionar ConfigurationError
3. protocols.py (sem deps)
4. plugin_registry.py (sem deps)
5. build_spec.py (sem deps)
6. build_context.py (deps: 4, 5, 2)
7. builder.py (deps: 3, 4, 5, 6)
8. __init__.py (deps: todos)
9. Atualizar forge_base/__init__.py
10. Testes unitários
11. Testes integração
12. Documentação
13. Release
```

---

## Checklist de Implementação

### Fase 1: Preparação
- [ ] 1.1 Criar `src/forge_base/composition/`
- [ ] 1.2 Adicionar `ConfigurationError` ao `exceptions.py`

### Fase 2: Core
- [ ] 2.1 Implementar `protocols.py`
- [ ] 2.2 Implementar `plugin_registry.py`
- [ ] 2.3 Implementar `build_spec.py`
- [ ] 2.4 Implementar `build_context.py`
- [ ] 2.5 Implementar `builder.py`
- [ ] 2.6 Implementar `__init__.py`

### Fase 3: Integração
- [ ] 3.1 Atualizar `forge_base/__init__.py`
- [ ] 3.2 Verificar imports funcionam

### Fase 4: Testes
- [ ] 4.1 `test_protocols.py`
- [ ] 4.2 `test_plugin_registry.py`
- [ ] 4.3 `test_build_spec.py`
- [ ] 4.4 `test_build_context.py`
- [ ] 4.5 `test_builder.py`
- [ ] 4.6 `test_composition_integration.py`

### Fase 5: Documentação e Release
- [ ] 5.1 Atualizar README.md
- [ ] 5.2 Criar `docs/usuarios/composition-guide.md`
- [ ] 5.3 Atualizar CHANGELOG.md
- [ ] 5.4 Bump version para 0.2.0
- [ ] 5.5 Criar tag v0.2.0

---

## Critérios de Aceite

1. **Funcional**: Todos os componentes funcionam conforme especificado
2. **Testado**: Cobertura de testes > 90% no módulo composition
3. **Documentado**: Guia de uso disponível em docs/
4. **Integrado**: Exportado via `from forge_base.composition import ...`
5. **Validado**: forge_llm pode migrar para usar as novas classes
