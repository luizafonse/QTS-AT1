# Relatório de Transparência — Uso de IA

## 1. Ferramentas Utilizadas
------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude (Anthropic)** | Revisão, otimização e validação do código após a implementação principal, além de apoio em verificações de qualidade e health checks. |
| **ChatGPT (OpenAI)**   | Apoio na escolha de um tema simples e adequado aos requisitos da atividade.                                                           |

## 2. Autoria e Desenvolvimento

A estrutura básica do projeto, a definição do funcionamento do sistema, a lógica principal das regras de negócio e a implementação inicial do código foram desenvolvidas sem suporte de IA.
A utilização de IA ocorreu como mecanismo de revisão, otimização e conferência da implementação já realizada.

## 3. Como a IA Foi Empregada

### 3.1 ChatGPT

O ChatGPT foi utilizado durante a etapa inicial de definição do tema, com o objetivo de identificar um domínio que fosse:

* simples de implementar;
* adequado para regras de negócio determinísticas;
* capaz de permitir a aplicação de Particionamento de Equivalência (EP);
* adequado para Análise do Valor Limite (BVA);
* adequado para Error Guessing;
* capaz de gerar diferentes caminhos de decisão para atingir 100% de cobertura de branches.

### 3.2 Claude

O Claude foi utilizado **após a finalização da implementação principal**, atuando principalmente como ferramenta de revisão técnica.

Entre as atividades realizadas com apoio do Claude estão:

* análise do código já desenvolvido;
* identificação de possíveis melhorias;
* otimização da implementação;
* conferência da consistência das regras;
* revisão da suíte de testes;
* verificação da cobertura dos diferentes caminhos lógicos;
* análise de possíveis entradas inválidas ou inesperadas;
* revisão dos mecanismos de validação defensiva;
* realização de health checks e verificações estruturais;
* confirmação dos acertos e da consistência da implementação.

As alterações sugeridas pelo Claude foram analisadas pelo autor antes de serem incorporadas ao projeto.

## 4. Auditoria e Validação

A utilização das ferramentas de IA foi acompanhada de revisão humana.

O código e os testes foram analisados para verificar:

* correspondência entre implementação e `PRD.md`;
* funcionamento das regras de negócio;
* tratamento de entradas inválidas;
* cobertura dos caminhos de decisão;
* utilização de testes parametrizados;
* aplicação de EP e BVA;
* presença de testes de Error Guessing;
* utilização da estrutura AAA;
* utilização de `@pytest.mark.unit`;
* ausência de alterações que simplesmente enfraquecessem os testes para obter cobertura.

### Verificações automatizadas realizadas durante a revisão

| Verificação                | Resultado                                         |
| -------------------------- | ------------------------------------------------- |
| Execução repetida da suíte | 192 cenários passando nas execuções realizadas    |
| Cobertura de linhas        | Todas as instruções executáveis cobertas          |
| Cobertura de branches      | 18 de 18 ramos de decisão cobertos                |
| Teste de mutação manual    | 46 de 46 mutantes detectados pela suíte           |
| Auditoria estrutural       | 43 de 43 funções de teste com `@pytest.mark.unit` |
| Testes parametrizados      | 23 testes/casos parametrizados identificados      |

## 5. Validação pós revisão técnica

A validação oficial deve ser feita utilizando:

```bash
uv sync --all-extras
```

seguido de:

```bash
uv run pytest -v
```

e:

```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```
