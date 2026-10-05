# PRD - Sistema de Aprovação de Aluno

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Disciplina | Qualidade e Teste de Software (QTS) - AT1 |
| Módulo de negócio | `app/aprovacao.py` |
| Linguagem | Python 3.12+ (gerenciado com `uv`) |

---

## 1. Visão Geral

Biblioteca de regras de negócio que decide a **situação final de um aluno** a partir da **nota** e da **frequência**, incluindo o resultado da **prova de recuperação**. O módulo é puro e determinístico: não possui I/O, banco de dados, relógio, aleatoriedade ou estado global, o que o torna ideal para testes unitários.

## 2. Objetivos

1. Implementar as regras de aprovação de forma clara, rastreável e com tratamento defensivo de entradas.
2. Garantir que toda entrada inválida gere `ValueError` com mensagem descritiva.
3. Validar o comportamento com uma suíte de testes unitários (Pytest) aplicando EP, BVA e Error Guessing.
4. Atingir **100% de cobertura de linhas e de ramos** no módulo de negócio.

## 3. Fora de Escopo

- Cálculo da média a partir de várias avaliações (a nota final já é recebida pronta).
- Persistência, API HTTP, interface gráfica e autenticação.
- Arredondamento de notas (o valor recebido é comparado exatamente como informado).

## 4. Glossário

| Termo | Definição |
|---|---|
| Nota | Nota final do aluno, número real no intervalo fechado **[0, 10]**. |
| Frequência | Percentual de presença, número real no intervalo fechado **[0, 100]**. |
| Frequência mínima | 75 (%). Valores **< 75** reprovam o aluno. |
| Nota de recuperação | Nota da prova de recuperação, no intervalo fechado **[0, 10]**. |

## 5. Entradas e Saídas

### 5.1 Entradas

| Parâmetro | Tipo aceito | Domínio válido |
|---|---|---|
| `nota` | `int` ou `float` (nunca `bool`) | finito, 0 <= x <= 10 |
| `frequencia` | `int` ou `float` (nunca `bool`) | finito, 0 <= x <= 100 |
| `nota_recuperacao` | `int` ou `float` (nunca `bool`) | finito, 0 <= x <= 10 |

### 5.2 Saída - `SituacaoAluno` (`StrEnum`)

| Membro | Valor textual |
|---|---|
| `APROVADO` | `"aprovado"` |
| `RECUPERACAO` | `"recuperacao"` |
| `REPROVADO` | `"reprovado"` |
| `APROVADO_EM_RECUPERACAO` | `"aprovado_em_recuperacao"` |

## 6. Regras de Negócio

### 6.1 Validação de entrada

| ID | Regra |
|---|---|
| RN01 | A nota deve estar entre 0 e 10 (inclusive). Fora do intervalo gera `ValueError`. |
| RN02 | A frequência deve estar entre 0 e 100 (inclusive). Fora do intervalo gera `ValueError`. |
| RN03 | Somente `int` e `float` são aceitos. `None`, `str`, `bool`, `list`, `dict`, `complex`, `Decimal` etc. geram `ValueError`. |
| RN04 | Valores não finitos (`NaN`, `+inf`, `-inf`, inteiros grandes demais para `float`) geram `ValueError`. |
| RN05 | A validação de todas as entradas ocorre **antes** de qualquer regra de classificação. |

### 6.2 Classificação

| ID | Regra | Resultado |
|---|---|---|
| RN06 | Frequência **< 75** (precede a nota) | `REPROVADO` |
| RN07 | Frequência >= 75 **e** nota >= 7 | `APROVADO` |
| RN08 | Frequência >= 75 **e** 5 <= nota < 7 (faixa 5 a 6,9) | `RECUPERACAO` |
| RN09 | Frequência >= 75 **e** nota < 5 | `REPROVADO` |

### 6.3 Recuperação

| ID | Regra | Resultado |
|---|---|---|
| RN10 | Nota de recuperação >= 5 | `APROVADO_EM_RECUPERACAO` |
| RN11 | Nota de recuperação < 5 | `REPROVADO` |
| RN12 | Somente alunos na situação `RECUPERACAO` podem ser avaliados na recuperação. Caso contrário gera `ValueError`. |
| RN13 | A nota de recuperação é validada **antes** da checagem de elegibilidade (RN05 estendida). |

> **Decisão de especificação (RN12):** o enunciado define que o aluno é aprovado em recuperação se a nota da recuperação for >= 5, mas não diz o que ocorre com quem não está em recuperação. Adotou-se tratar essa chamada como entrada inválida (`ValueError`), pois um aluno já aprovado ou já reprovado não realiza a prova.

## 7. Tabela de Decisão

| Frequência | Nota | Situação |
|---|---|---|
| < 75 | qualquer (válida) | `REPROVADO` |
| >= 75 | >= 7 | `APROVADO` |
| >= 75 | 5 <= nota < 7 | `RECUPERACAO` |
| >= 75 | < 5 | `REPROVADO` |

| Situação inicial | Nota de recuperação | Situação final |
|---|---|---|
| `RECUPERACAO` | >= 5 | `APROVADO_EM_RECUPERACAO` |
| `RECUPERACAO` | < 5 | `REPROVADO` |
| qualquer outra | - | `ValueError` |

## 8. API Pública (`app/aprovacao.py`)

| Função | Assinatura | Descrição |
|---|---|---|
| `validar_nota` | `(nota: object, nome: str = "nota") -> float` | Valida RN01, RN03, RN04. |
| `validar_frequencia` | `(frequencia: object) -> float` | Valida RN02, RN03, RN04. |
| `classificar_aluno` | `(nota: float, frequencia: float) -> SituacaoAluno` | Aplica RN05 a RN09. |
| `avaliar_recuperacao` | `(nota: float, frequencia: float, nota_recuperacao: float) -> SituacaoAluno` | Aplica RN10 a RN13. |

## 9. Requisitos Não Funcionais

| ID | Requisito |
|---|---|
| RNF01 | Python 3.12+ com *type hints* em todas as funções públicas. |
| RNF02 | Tratamento defensivo: nenhuma entrada inválida pode produzir resultado silencioso ou exceção diferente de `ValueError`. |
| RNF03 | Projeto gerenciado com `uv` (`pyproject.toml`). |
| RNF04 | Testes com Pytest, padrão AAA, `@pytest.mark.parametrize` e `@pytest.mark.unit`. |
| RNF05 | Cobertura de **100%** de linhas e ramos (`--cov-branch`) no pacote `app`. |
| RNF06 | Módulo determinístico: mesma entrada produz sempre a mesma saída. |

## 10. Estratégia de Testes

| Técnica | Aplicação |
|---|---|
| **Particionamento de Equivalência (EP)** | Uma classe por situação final e uma classe inválida por parâmetro (abaixo do mínimo, acima do máximo, tipo errado). |
| **Análise do Valor Limite (BVA)** | Nota: -0,01 / 0 / 0,01 / 4,99 / 5 / 5,01 / 6,9 / 6,99 / 7 / 9,99 / 10 / 10,01. Frequência: -0,01 / 0 / 74,99 / 75 / 75,01 / 100 / 100,01. |
| **Tabela de decisão** | Combinação nota (alta, média, baixa) x frequência (ok, baixa). |
| **Error Guessing** | `None`, `""`, `"7"`, `"80%"`, `True`, `NaN`, `inf`, `10**400`, `Decimal`, `complex`, listas, dicionários, escala errada (0-100 na nota), ordem de validação. |

## 11. Rastreabilidade (Regra -> Testes)

| Regra | Arquivo de teste | Testes principais |
|---|---|---|
| RN01 | `tests/test_validacoes_unit.py` | `test_validar_nota_aceita_valores_validos`, `test_validar_nota_rejeita_fora_do_intervalo` |
| RN02 | `tests/test_validacoes_unit.py` | `test_validar_frequencia_aceita_valores_validos`, `test_validar_frequencia_rejeita_fora_do_intervalo` |
| RN03 | `tests/test_validacoes_unit.py` | `test_validar_nota_rejeita_tipos_inesperados`, `test_validar_frequencia_rejeita_tipos_inesperados` |
| RN04 | `tests/test_validacoes_unit.py` | `test_validar_nota_rejeita_valores_nao_finitos`, `test_validar_frequencia_rejeita_valores_nao_finitos` |
| RN05 | `tests/test_classificacao_unit.py` | `test_classificar_aluno_valida_nota_antes_de_aplicar_regra_de_frequencia`, `test_classificar_aluno_valida_frequencia_mesmo_com_nota_reprovada` |
| RN06 | `tests/test_classificacao_unit.py` | `test_classificar_aluno_reprovado_por_frequencia` |
| RN07 | `tests/test_classificacao_unit.py` | `test_classificar_aluno_aprovado` |
| RN08 | `tests/test_classificacao_unit.py` | `test_classificar_aluno_recuperacao` |
| RN09 | `tests/test_classificacao_unit.py` | `test_classificar_aluno_reprovado_por_nota` |
| RN06 a RN09 | `tests/test_classificacao_unit.py` | `test_classificar_aluno_tabela_de_decisao` |
| RN10 | `tests/test_recuperacao_unit.py` | `test_avaliar_recuperacao_aprovado` |
| RN11 | `tests/test_recuperacao_unit.py` | `test_avaliar_recuperacao_reprovado` |
| RN12 | `tests/test_recuperacao_unit.py` | `test_avaliar_recuperacao_rejeita_aluno_fora_da_recuperacao` |
| RN13 | `tests/test_recuperacao_unit.py` | `test_avaliar_recuperacao_valida_nota_recuperacao_antes_da_elegibilidade` |

## 12. Critérios de Aceite

- [ ] `uv run pytest -v` executa todos os testes sem falhas.
- [ ] `uv run pytest --cov=app --cov-branch --cov-report=term-missing` reporta **100%** (linhas e ramos) em `app/aprovacao.py`.
- [ ] Toda regra RN01 a RN13 possui ao menos um teste rastreável (seção 11).
- [ ] Nenhuma entrada inválida resulta em exceção diferente de `ValueError`.
