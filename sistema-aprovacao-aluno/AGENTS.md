# AGENTS.md - Regras de Contexto para IA

## 1. Contexto do Projeto

- Domínio: Sistema de Aprovação de Aluno (nota, frequência, recuperação).
- Linguagem: Python 3.12+. Gerenciador: `uv`. Testes: Pytest + pytest-cov.
- Módulo de negócio: `app/aprovacao.py` (puro e determinístico, sem I/O).
- Testes: pasta `tests/`, arquivos `test_*_unit.py`.

## 2. Estrutura de Pastas (não alterar sem necessidade)

```text
app/            # Regras de negocio (SUT)
tests/          # conftest.py + testes unitarios
PRD.md          # Especificacao
AGENTS.md       # Este arquivo
AI_USAGE.md     # Relatorio de transparencia
```

## 3. Regras de Código

1. Usar *type hints* em todas as funções e constantes públicas.
2. Entradas inválidas **sempre** geram `ValueError` com mensagem descritiva. Nunca retornar `None`, `False` ou valor padrão para esconder erro.
4. Não usar `print`, I/O, rede, `random`, `datetime` ou estado global no módulo de negócio.
5. Não usar valores "mágicos": limites ficam em constantes nomeadas no topo do módulo.
6. Proibido `# pragma: no cover`, `# type: ignore` e `except Exception` genérico para forçar cobertura ou silenciar erros.

## 4. Regras de Testes

1. Todo teste segue o padrão **AAA** `# Arrange`, `# Act`, `# Assert`.
2. Todo teste leva o marcador `@pytest.mark.unit`.
3. Usar `@pytest.mark.parametrize` com `pytest.param(..., id="...")` sempre que houver variação apenas de dados.
4. Cobrir obrigatoriamente: **EP** (classes válidas e inválidas), **BVA** (valor no limite, imediatamente abaixo e acima) e **Error Guessing** (None, string, bool, NaN, inf, tipos inesperados).
5. Asserções de exceção devem usar `pytest.raises(ValueError, match="...")` verificando a mensagem.
6. Meta: **100% de cobertura de linhas e ramos** (`--cov-branch`) no pacote `app`.
7. Proibido enfraquecer, remover ou ajustar um teste apenas para fazê-lo passar. Se um teste falha, corrigir o código ou, se a regra mudou, atualizar primeiro o `PRD.md`.

## 5. Fluxo de Trabalho Obrigatório

1. Ler o `PRD.md` antes de qualquer alteração.
2. Se a regra de negócio mudar: atualizar `PRD.md` -> atualizar testes -> atualizar código.
3. Rodar os comandos de validação (seção 6) antes de considerar a tarefa concluída.
4. Registrar no `AI_USAGE.md` qualquer uso relevante de IA.

## 6. Comandos de Validação

```bash
uv sync
uv run pytest -v
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

## 7. Definição de Pronto

- Todos os testes passam.
- Cobertura de 100% (linhas e ramos) em `app/aprovacao.py`.
- Cada regra do `PRD.md` possui teste rastreável.
- Nenhuma regra desta página foi violada.
