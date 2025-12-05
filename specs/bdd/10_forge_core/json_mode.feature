@json-mode @structured-output
Feature: JSON Mode / Structured Output
  Como desenvolvedor usando ForgeLLM
  Eu quero controlar o formato de resposta do LLM
  Para obter dados estruturados em JSON

  Background:
    Given um cliente ForgeLLM configurado

  # ============================================
  # Text Mode (Default)
  # ============================================

  @text-mode
  Scenario: Formato texto eh o padrao
    When eu envio uma mensagem sem especificar response_format
    Then a resposta deve ser texto livre
    And nao deve haver restricao de formato

  @text-mode
  Scenario: Formato texto explicito
    Given response_format configurado como "text"
    When eu envio uma mensagem
    Then a resposta deve ser texto livre

  # ============================================
  # JSON Object Mode
  # ============================================

  @json-object
  Scenario: JSON object mode retorna JSON valido
    Given response_format configurado como "json_object"
    When eu envio uma mensagem pedindo dados em JSON
    Then a resposta deve ser JSON valido
    And a resposta deve ser parseavel como dict

  @json-object
  Scenario: JSON object mode sem schema definido
    Given response_format configurado como "json_object"
    When eu envio uma mensagem
    Then a resposta JSON pode ter qualquer estrutura
    And nao ha validacao de schema

  # ============================================
  # JSON Schema Mode
  # ============================================

  @json-schema
  Scenario: JSON schema mode com schema simples
    Given um schema JSON:
      """
      {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "age": {"type": "integer"}
        },
        "required": ["name", "age"],
        "additionalProperties": false
      }
      """
    And response_format configurado com esse schema
    When eu envio uma mensagem pedindo dados de uma pessoa
    Then a resposta deve ser JSON valido
    And a resposta deve conter a propriedade "name"
    And a resposta deve conter a propriedade "age"

  @json-schema
  Scenario: JSON schema mode com nome customizado
    Given um schema JSON com nome "PersonData"
    And response_format configurado com esse schema
    When eu envio uma mensagem
    Then o schema deve ser identificado como "PersonData"

  @json-schema
  Scenario: JSON schema mode strict por padrao
    Given um schema JSON qualquer
    When eu crio ResponseFormat.json_with_schema com strict padrao
    Then strict deve ser True

  @json-schema
  Scenario: JSON schema mode pode ser non-strict
    Given um schema JSON qualquer
    When eu crio ResponseFormat.json_with_schema com strict=False
    Then strict deve ser False

  # ============================================
  # Pydantic Integration
  # ============================================

  @pydantic
  Scenario: Criar ResponseFormat de modelo Pydantic
    Given uma classe Pydantic "Person" com campos name e age
    When eu crio ResponseFormat.from_pydantic(Person)
    Then o type deve ser "json_schema"
    And o schema_name deve ser "Person"
    And o json_schema deve conter as propriedades do modelo

  @pydantic
  Scenario: Pydantic adiciona additionalProperties false em strict mode
    Given uma classe Pydantic "Person"
    When eu crio ResponseFormat.from_pydantic(Person) com strict=True
    Then o json_schema deve conter "additionalProperties": false

  @pydantic
  Scenario: Pydantic nao adiciona additionalProperties em non-strict
    Given uma classe Pydantic "Person"
    When eu crio ResponseFormat.from_pydantic(Person) com strict=False
    Then o json_schema nao deve conter "additionalProperties"

  @pydantic @error
  Scenario: Rejeitar classe que nao e Pydantic
    Given uma classe Python comum (nao Pydantic)
    When eu tento criar ResponseFormat.from_pydantic com essa classe
    Then deve lancar ValidationError
    And a mensagem deve mencionar "pydantic.BaseModel"

  @pydantic @error
  Scenario: Rejeitar instancia ao inves de classe
    Given uma instancia de modelo Pydantic
    When eu tento criar ResponseFormat.from_pydantic com essa instancia
    Then deve lancar ValidationError

  # ============================================
  # Validation
  # ============================================

  @validation @error
  Scenario: Rejeitar tipo de formato invalido
    When eu tento criar ResponseFormat com type="invalid"
    Then deve lancar ValidationError
    And a mensagem deve mencionar "Tipo de formato invalido"

  @validation @error
  Scenario: Rejeitar json_schema sem schema fornecido
    When eu tento criar ResponseFormat com type="json_schema" sem json_schema
    Then deve lancar ValidationError
    And a mensagem deve mencionar "json_schema obrigatorio"

  @validation @error
  Scenario: Rejeitar schema com tipo errado
    When eu tento criar ResponseFormat com type="json_object" e json_schema fornecido
    Then deve lancar ValidationError
    And a mensagem deve mencionar "json_schema so pode ser usado"

  # ============================================
  # Immutability
  # ============================================

  @immutability
  Scenario: ResponseFormat deve ser imutavel
    Given um ResponseFormat criado
    When eu tento modificar o atributo type
    Then deve lancar AttributeError

  # ============================================
  # Equality
  # ============================================

  @equality
  Scenario: ResponseFormats identicos sao iguais
    Given dois ResponseFormat.json() criados separadamente
    Then eles devem ser iguais
    And eles devem ter o mesmo hash

  @equality
  Scenario: ResponseFormats diferentes nao sao iguais
    Given um ResponseFormat.text()
    And um ResponseFormat.json()
    Then eles nao devem ser iguais

  # ============================================
  # Serialization
  # ============================================

  @serialization
  Scenario: Serializar formato texto para dict
    Given um ResponseFormat.text()
    When eu chamo to_dict()
    Then o resultado deve conter chave "type" com valor "text"
    And o resultado deve conter chave "strict" com valor true

  @serialization
  Scenario: Serializar formato json_schema para dict
    Given um ResponseFormat com json_schema
    When eu chamo to_dict()
    Then o resultado deve conter chave "type" com valor "json_schema"
    And o resultado deve conter chave "json_schema"
    And o resultado deve conter chave "schema_name"
    And o resultado deve conter chave "strict"

  # ============================================
  # Provider-Specific Behavior
  # ============================================

  @provider @openai
  Scenario: OpenAI usa text.format para JSON mode
    Given provider OpenAI configurado
    And response_format configurado como "json_object"
    When eu envio uma mensagem
    Then a requisicao deve usar parametro text.format

  @provider @anthropic
  Scenario: Anthropic usa prompt engineering para JSON mode
    Given provider Anthropic configurado
    And response_format configurado como "json_object"
    When eu envio uma mensagem
    Then o system prompt deve conter instrucoes de JSON

  @provider @anthropic
  Scenario: Anthropic usa tool forcado para JSON schema
    Given provider Anthropic configurado
    And response_format configurado com json_schema
    When eu envio uma mensagem
    Then deve haver um tool com o schema
    And o system prompt deve instruir uso do tool
