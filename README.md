# Sistema de Aprovação de Aluno - Testes Unitários, Cobertura e Governança de IA
Afonso Luiz Soares Batista - DSM¨6
Projeto da **AT1 de Qualidade e Teste de Software (QTS)**: regras de negócio de aprovação de aluno em Python, validadas por uma suíte de testes unitários com **Pytest**, aplicando **Particionamento de Equivalência (EP)**, **Análise do Valor Limite (BVA)** e **Error Guessing**, com medição de cobertura de linhas e ramos via **pytest-cov** e documentação de governança de IA.

---

## Regras de Negócio (resumo)

| Condição | Resultado |
|---|---|
| Nota fora de 0 a 10, frequência fora de 0 a 100 ou tipo inválido | `ValueError` |
| Frequência < 75% | `REPROVADO` |
| Frequência >= 75% e nota >= 7 | `APROVADO` |
| Frequência >= 75% e 5 <= nota < 7 | `RECUPERACAO` |
| Frequência >= 75% e nota < 5 | `REPROVADO` |
| Em recuperação com nota de recuperação >= 5 | `APROVADO_EM_RECUPERACAO` |
| Em recuperação com nota de recuperação < 5 | `REPROVADO` |

Especificação completa e rastreabilidade em [`PRD.md`](PRD.md).

---

## Estrutura do Projeto

```text
sistema-aprovacao-aluno/
├── app/
│   ├── __init__.py
│   └── aprovacao.py                 # Regras de negocio (SUT) com type hints
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Fixtures de perfis de aluno
│   ├── test_validacoes_unit.py      # validar_nota e validar_frequencia
│   ├── test_classificacao_unit.py   # classificar_aluno
│   └── test_recuperacao_unit.py     # avaliar_recuperacao
├── AGENTS.md                        # Regras de contexto para IA
├── AI_USAGE.md                      # Relatorio de transparencia de IA
├── PRD.md                           # Especificacao das regras de negocio
├── pyproject.toml
├── .python-version
└── README.md
```

---

## Como Executar

### 1. Sincronizar Dependências com o `uv`

```bash
uv sync
```

### 2. Executar Todos os Testes

```bash
uv run pytest -v
```

### 3. Executar Apenas os Testes Marcados como Unitários

```bash
uv run pytest -m unit -v
```

### 4. Medir Cobertura de Código e Ramificações

```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

O resultado esperado é **100%** de cobertura (coluna `Cover`) e nenhuma linha na coluna `Missing` para `app/aprovacao.py`. O `pyproject.toml` também define `fail_under = 100`, então a execução com cobertura falha caso o valor caia abaixo disso.

### 5. Gerar Relatório de Cobertura em HTML (opcional)

```bash
uv run pytest --cov=app --cov-branch --cov-report=html
```

Abra `htmlcov/index.html` no navegador.

---

## Técnicas de Teste Aplicadas

| Técnica | Onde aparece |
|---|---|
| **Padrão AAA** | Todos os testes possuem comentários `# Arrange`, `# Act`, `# Assert` |
| **EP** | Uma classe por situação final e classes inválidas por parâmetro |
| **BVA** | Valores como 4,99 / 5 / 6,99 / 7 (nota), 74,99 / 75 / 75,01 (frequência), -0,01 / 10,01 (limites do domínio) |
| **Tabela de decisão** | `test_classificar_aluno_tabela_de_decisao` |
| **Error Guessing** | `None`, `""`, `"7"`, `True`, `NaN`, `inf`, `10**400`, `Decimal`, `complex`, listas, dicionários |
| **Parametrização** | `@pytest.mark.parametrize` com `pytest.param(..., id=...)` |
| **Marcação** | `@pytest.mark.unit` em todos os testes |

---

## Governança de IA

- [`PRD.md`](PRD.md): especificação e rastreabilidade das regras (RN01 a RN13).
- [`AGENTS.md`](AGENTS.md): regras de contexto que orientam qualquer assistente de IA no repositório.
- [`AI_USAGE.md`](AI_USAGE.md): ferramenta utilizada, como a IA foi empregada e como foi feita a auditoria.
