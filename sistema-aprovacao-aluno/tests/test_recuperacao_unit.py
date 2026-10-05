"""Testes unitarios de avaliar_recuperacao.

Tecnicas aplicadas:
    - Particionamento de Equivalencia (EP): aprovado em recuperacao x reprovado.
    - Analise do Valor Limite (BVA): nota de recuperacao em 4.99/5/5.01 e
      nota original em 4.99/5/6.99/7 (fronteiras da elegibilidade).
    - Error Guessing: entradas invalidas e alunos nao elegiveis.
"""

import pytest

from app.aprovacao import SituacaoAluno, avaliar_recuperacao



@pytest.mark.unit
@pytest.mark.parametrize(
    "nota_recuperacao",
    [
        pytest.param(5.0, id="bva-limite-exato-float"),
        pytest.param(5, id="bva-limite-exato-inteiro"),
        pytest.param(5.01, id="bva-logo-acima-do-limite"),
        pytest.param(6.9, id="ep-faixa-intermediaria"),
        pytest.param(7.0, id="ep-nota-de-aprovacao"),
        pytest.param(9.99, id="bva-logo-abaixo-do-maximo"),
        pytest.param(10.0, id="bva-nota-maxima"),
    ],
)
def test_avaliar_recuperacao_aprovado(nota_recuperacao: float) -> None:
    nota, frequencia = 6.0, 80.0

    situacao = avaliar_recuperacao(nota, frequencia, nota_recuperacao)

    assert situacao is SituacaoAluno.APROVADO_EM_RECUPERACAO




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota_recuperacao",
    [
        pytest.param(4.99, id="bva-logo-abaixo-do-limite"),
        pytest.param(4.9999, id="bva-precisao-extra-abaixo-de-cinco"),
        pytest.param(4, id="ep-faixa-intermediaria-inteiro"),
        pytest.param(0.01, id="bva-logo-acima-do-zero"),
        pytest.param(0.0, id="bva-nota-zero-float"),
        pytest.param(0, id="bva-nota-zero-inteiro"),
    ],
)
def test_avaliar_recuperacao_reprovado(nota_recuperacao: float) -> None:
    nota, frequencia = 6.0, 80.0

    situacao = avaliar_recuperacao(nota, frequencia, nota_recuperacao)

    assert situacao is SituacaoAluno.REPROVADO




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, frequencia",
    [
        pytest.param(5.0, 75.0, id="bva-menor-nota-elegivel-e-frequencia-minima"),
        pytest.param(6.99, 75.0, id="bva-maior-nota-elegivel"),
        pytest.param(6.0, 100.0, id="frequencia-maxima"),
    ],
)
def test_avaliar_recuperacao_aceita_alunos_elegiveis_nas_fronteiras(nota: float, frequencia: float) -> None:
    nota_recuperacao = 5.0

    situacao = avaliar_recuperacao(nota, frequencia, nota_recuperacao)

    assert situacao is SituacaoAluno.APROVADO_EM_RECUPERACAO


@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, frequencia, situacao_atual",
    [
        pytest.param(7.0, 75.0, "aprovado", id="bva-aprovado-direto-no-limite"),
        pytest.param(10.0, 100.0, "aprovado", id="aprovado-direto-maximo"),
        pytest.param(4.99, 75.0, "reprovado", id="bva-reprovado-por-nota-no-limite"),
        pytest.param(0.0, 100.0, "reprovado", id="reprovado-por-nota-zero"),
        pytest.param(6.0, 74.99, "reprovado", id="bva-reprovado-por-frequencia-no-limite"),
        pytest.param(9.0, 0.0, "reprovado", id="reprovado-por-frequencia-zero"),
    ],
)
def test_avaliar_recuperacao_rejeita_aluno_fora_da_recuperacao(
    nota: float, frequencia: float, situacao_atual: str
) -> None:
    nota_recuperacao_alta = 10.0

    with pytest.raises(ValueError, match=f"apenas alunos em recuperacao.*situacao atual: {situacao_atual}"):
        avaliar_recuperacao(nota, frequencia, nota_recuperacao_alta)




@pytest.mark.unit
def test_avaliar_recuperacao_com_fixture_de_aluno_em_recuperacao(aluno_em_recuperacao: dict[str, float]) -> None:
    nota_recuperacao = 8.0

    situacao = avaliar_recuperacao(**aluno_em_recuperacao, nota_recuperacao=nota_recuperacao)

    assert situacao is SituacaoAluno.APROVADO_EM_RECUPERACAO


@pytest.mark.unit
def test_avaliar_recuperacao_fixture_aprovado_nao_pode_recuperar(aluno_aprovado: dict[str, float]) -> None:
    nota_recuperacao = 10.0

    with pytest.raises(ValueError, match="apenas alunos em recuperacao"):
        avaliar_recuperacao(**aluno_aprovado, nota_recuperacao=nota_recuperacao)


@pytest.mark.unit
def test_avaliar_recuperacao_fixture_reprovado_por_nota_nao_pode_recuperar(
    aluno_reprovado_por_nota: dict[str, float],
) -> None:
    nota_recuperacao = 10.0

    with pytest.raises(ValueError, match="apenas alunos em recuperacao"):
        avaliar_recuperacao(**aluno_reprovado_por_nota, nota_recuperacao=nota_recuperacao)


@pytest.mark.unit
def test_avaliar_recuperacao_fixture_reprovado_por_frequencia_nao_pode_recuperar(
    aluno_reprovado_por_frequencia: dict[str, float],
) -> None:
    nota_recuperacao = 10.0

    with pytest.raises(ValueError, match="apenas alunos em recuperacao"):
        avaliar_recuperacao(**aluno_reprovado_por_frequencia, nota_recuperacao=nota_recuperacao)




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota_recuperacao_invalida",
    [
        pytest.param(-0.01, id="bva-abaixo-de-zero"),
        pytest.param(10.01, id="bva-acima-de-dez"),
        pytest.param(-3, id="negativa"),
        pytest.param(50, id="escala-errada"),
        pytest.param(None, id="none"),
        pytest.param("5", id="string-numerica"),
        pytest.param("", id="string-vazia"),
        pytest.param(True, id="booleano"),
        pytest.param([5], id="lista"),
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="infinito"),
    ],
)
def test_avaliar_recuperacao_rejeita_nota_recuperacao_invalida(
    nota_recuperacao_invalida: object, aluno_em_recuperacao: dict[str, float]
) -> None:

    with pytest.raises(ValueError, match="nota_recuperacao deve"):
        avaliar_recuperacao(**aluno_em_recuperacao, nota_recuperacao=nota_recuperacao_invalida)


@pytest.mark.unit
@pytest.mark.parametrize(
    "nota_invalida",
    [
        pytest.param(-1, id="negativa"),
        pytest.param(10.01, id="bva-acima-de-dez"),
        pytest.param(None, id="none"),
        pytest.param("6", id="string-numerica"),
        pytest.param(False, id="booleano"),
    ],
)
def test_avaliar_recuperacao_rejeita_nota_original_invalida(nota_invalida: object) -> None:
    frequencia_valida, nota_recuperacao_valida = 80.0, 8.0

    with pytest.raises(ValueError, match="nota deve"):
        avaliar_recuperacao(nota_invalida, frequencia_valida, nota_recuperacao_valida)


@pytest.mark.unit
@pytest.mark.parametrize(
    "frequencia_invalida",
    [
        pytest.param(-0.01, id="bva-abaixo-de-zero"),
        pytest.param(100.01, id="bva-acima-de-cem"),
        pytest.param(None, id="none"),
        pytest.param("80", id="string-numerica"),
        pytest.param(True, id="booleano"),
    ],
)
def test_avaliar_recuperacao_rejeita_frequencia_invalida(frequencia_invalida: object) -> None:
    nota_valida, nota_recuperacao_valida = 6.0, 8.0

    with pytest.raises(ValueError, match="frequencia deve"):
        avaliar_recuperacao(nota_valida, frequencia_invalida, nota_recuperacao_valida)


@pytest.mark.unit
def test_avaliar_recuperacao_valida_nota_recuperacao_antes_da_elegibilidade() -> None:
    nota, frequencia, nota_recuperacao_invalida = 9.0, 90.0, 11.0

    with pytest.raises(ValueError, match="nota_recuperacao deve estar entre 0 e 10"):
        avaliar_recuperacao(nota, frequencia, nota_recuperacao_invalida)


@pytest.mark.unit
def test_avaliar_recuperacao_com_todas_as_entradas_invalidas_gera_value_error() -> None:
    entradas = (None, "x", float("nan"))

    with pytest.raises(ValueError):
        avaliar_recuperacao(*entradas)


@pytest.mark.unit
def test_avaliar_recuperacao_e_deterministico(aluno_em_recuperacao: dict[str, float]) -> None:
    nota_recuperacao = 5.0

    resultados = {avaliar_recuperacao(**aluno_em_recuperacao, nota_recuperacao=nota_recuperacao) for _ in range(20)}

    assert resultados == {SituacaoAluno.APROVADO_EM_RECUPERACAO}
