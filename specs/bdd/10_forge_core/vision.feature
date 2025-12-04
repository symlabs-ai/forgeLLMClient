@vision @multimodal
Feature: Vision/Image Support
  Como desenvolvedor
  Quero enviar imagens junto com mensagens
  Para usar modelos com capacidade de visao

  Background:
    Given um cliente configurado com provider "mock"

  @image-url
  Scenario: Enviar imagem por URL
    Given uma imagem com URL "https://example.com/image.jpg"
    When eu envio a mensagem "O que ha nesta imagem?" com a imagem
    Then a resposta deve conter conteudo
    And a mensagem enviada deve conter a imagem

  @image-base64
  Scenario: Enviar imagem em base64
    Given uma imagem em base64 com media type "image/png"
    When eu envio a mensagem "Descreva esta imagem" com a imagem
    Then a resposta deve conter conteudo
    And a mensagem enviada deve conter a imagem em base64

  @image-validation
  Scenario: Imagem requer URL ou base64
    When eu tento criar uma imagem sem URL e sem base64
    Then deve lancar ValidationError com mensagem "URL ou base64_data obrigatorio"

  @image-validation-both
  Scenario: Imagem nao aceita URL e base64 juntos
    When eu tento criar uma imagem com URL e base64
    Then deve lancar ValidationError com mensagem "Usar URL ou base64_data, nao ambos"

  @mixed-content
  Scenario: Mensagem com texto e multiplas imagens
    Given uma imagem com URL "https://example.com/img1.jpg"
    And outra imagem com URL "https://example.com/img2.jpg"
    When eu envio a mensagem "Compare estas duas imagens" com as imagens
    Then a resposta deve conter conteudo
    And a mensagem enviada deve conter 2 imagens

  @image-media-types
  Scenario Outline: Suporte a diferentes tipos de midia
    Given uma imagem em base64 com media type "<media_type>"
    When eu envio a mensagem "Analise esta imagem" com a imagem
    Then a imagem deve ter media type "<media_type>"

    Examples:
      | media_type |
      | image/jpeg |
      | image/png  |
      | image/gif  |
      | image/webp |
