"""Testes unitarios de classificar_aluno (aprovado, recuperacao, reprovado).

Tecnicas aplicadas:
    - Particionamento de Equivalencia (EP): uma classe por situacao final.
    - Analise do Valor Limite (BVA): nota em 4.99/5/6.9/7 e frequencia em
      74.99/75/75.01.
    - Tabela de decisao: combinacao nota x frequencia.
    - Error Guessing: entradas invalidas e ordem de validacao.
"""

import pytest

from app.aprovacao import SituacaoAluno, classificar_aluno

@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, frequencia",
    [
        pytest.param(7.0, 75.0, id="bva-nota-minima-e-frequencia-minima"),
        pytest.param(7, 75, id="bva-limites-inteiros"),
        pytest.param(7.01, 75.01, id="bva-logo-acima-dos-dois-limites"),
        pytest.param(7.0, 100.0, id="nota-minima-frequencia-maxima"),
        pytest.param(10.0, 75.0, id="nota-maxima-frequencia-minima"),
        pytest.param(10.0, 100.0, id="nota-e-frequencia-maximas"),
        pytest.param(8.5, 90.0, id="ep-caso-tipico"),
        pytest.param(9.99, 99.99, id="bva-logo-abaixo-dos-maximos"),
    ],
)
def test_classificar_aluno_aprovado(nota: float, frequencia: float) -> None:

    situacao = classificar_aluno(nota, frequencia)

    assert situacao is SituacaoAluno.APROVADO

@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, frequencia",
    [
        pytest.param(5.0, 75.0, id="bva-nota-minima-e-frequencia-minima"),
        pytest.param(5, 75, id="bva-limites-inteiros"),
        pytest.param(5.01, 75.01, id="bva-logo-acima-dos-limites-inferiores"),
        pytest.param(6.9, 75.0, id="bva-ultima-nota-de-recuperacao-informada"),
        pytest.param(6.99, 75.0, id="bva-logo-abaixo-da-nota-de-aprovacao"),
        pytest.param(6.9999, 100.0, id="bva-precisao-extra-abaixo-de-sete"),
        pytest.param(5.0, 100.0, id="nota-minima-frequencia-maxima"),
        pytest.param(6.0, 80.0, id="ep-caso-tipico"),
    ],
)
def test_classificar_aluno_recuperacao(nota: float, frequencia: float) -> None:

    situacao = classificar_aluno(nota, frequencia)

    assert situacao is SituacaoAluno.RECUPERACAO




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, frequencia",
    [
        pytest.param(4.99, 75.0, id="bva-logo-abaixo-da-recuperacao"),
        pytest.param(4.9999, 100.0, id="bva-precisao-extra-abaixo-de-cinco"),
        pytest.param(4.0, 90.0, id="ep-caso-tipico"),
        pytest.param(0.01, 80.0, id="bva-logo-acima-do-zero"),
        pytest.param(0.0, 75.0, id="bva-nota-zero-frequencia-minima"),
        pytest.param(0, 100, id="bva-nota-zero-frequencia-maxima"),
    ],
)
def test_classificar_aluno_reprovado_por_nota(nota: float, frequencia: float) -> None:

    situacao = classificar_aluno(nota, frequencia)

    assert situacao is SituacaoAluno.REPROVADO




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, frequencia",
    [
        pytest.param(10.0, 74.99, id="bva-nota-maxima-logo-abaixo-do-minimo"),
        pytest.param(7.0, 74.9999, id="bva-precisao-extra-abaixo-de-75"),
        pytest.param(7.0, 74, id="bva-nota-de-aprovacao-frequencia-inteira"),
        pytest.param(6.0, 74.99, id="nota-de-recuperacao-frequencia-insuficiente"),
        pytest.param(5.0, 50.0, id="nota-minima-recuperacao-frequencia-baixa"),
        pytest.param(4.0, 74.99, id="nota-e-frequencia-insuficientes"),
        pytest.param(10.0, 0.0, id="bva-frequencia-zero-nota-maxima"),
        pytest.param(0.0, 0.0, id="bva-nota-e-frequencia-zero"),
        pytest.param(9.0, 60.0, id="ep-caso-tipico"),
    ],
)
def test_classificar_aluno_reprovado_por_frequencia(nota: float, frequencia: float) -> None:

    situacao = classificar_aluno(nota, frequencia)

    assert situacao is SituacaoAluno.REPROVADO




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota, frequencia, situacao_esperada",
    [
        pytest.param(8.0, 80.0, SituacaoAluno.APROVADO, id="nota-alta-freq-ok"),
        pytest.param(8.0, 70.0, SituacaoAluno.REPROVADO, id="nota-alta-freq-baixa"),
        pytest.param(6.0, 80.0, SituacaoAluno.RECUPERACAO, id="nota-media-freq-ok"),
        pytest.param(6.0, 70.0, SituacaoAluno.REPROVADO, id="nota-media-freq-baixa"),
        pytest.param(3.0, 80.0, SituacaoAluno.REPROVADO, id="nota-baixa-freq-ok"),
        pytest.param(3.0, 70.0, SituacaoAluno.REPROVADO, id="nota-baixa-freq-baixa"),
    ],
)
def test_classificar_aluno_tabela_de_decisao(
    nota: float, frequencia: float, situacao_esperada: SituacaoAluno
) -> None:
#arrange
    situacao = classificar_aluno(nota, frequencia)
#act
    assert situacao is situacao_esperada




@pytest.mark.unit
def test_classificar_aluno_perfil_aprovado(aluno_aprovado: dict[str, float]) -> None:

    situacao = classificar_aluno(**aluno_aprovado)

    assert situacao is SituacaoAluno.APROVADO


@pytest.mark.unit
def test_classificar_aluno_perfil_recuperacao(aluno_em_recuperacao: dict[str, float]) -> None:

    situacao = classificar_aluno(**aluno_em_recuperacao)

    assert situacao is SituacaoAluno.RECUPERACAO


@pytest.mark.unit
def test_classificar_aluno_perfil_reprovado_por_nota(aluno_reprovado_por_nota: dict[str, float]) -> None:

    situacao = classificar_aluno(**aluno_reprovado_por_nota)

    assert situacao is SituacaoAluno.REPROVADO


@pytest.mark.unit
def test_classificar_aluno_perfil_reprovado_por_frequencia(
    aluno_reprovado_por_frequencia: dict[str, float],
) -> None:

    situacao = classificar_aluno(**aluno_reprovado_por_frequencia)

    assert situacao is SituacaoAluno.REPROVADO




@pytest.mark.unit
def test_classificar_aluno_retorna_enum_com_valor_textual() -> None:
    nota, frequencia = 8.0, 90.0

    situacao = classificar_aluno(nota, frequencia)

    assert isinstance(situacao, SituacaoAluno)
    assert situacao == "aprovado"


@pytest.mark.unit
def test_classificar_aluno_e_deterministico() -> None:
    nota, frequencia = 6.5, 80.0

    resultados = {classificar_aluno(nota, frequencia) for _ in range(20)}

    assert resultados == {SituacaoAluno.RECUPERACAO}


@pytest.mark.unit
def test_situacao_aluno_possui_exatamente_quatro_valores() -> None:
    valores_esperados = {"aprovado", "recuperacao", "reprovado", "aprovado_em_recuperacao"}

    valores_reais = {situacao.value for situacao in SituacaoAluno}

    assert valores_reais == valores_esperados




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota_invalida",
    [
        pytest.param(-0.01, id="bva-abaixo-de-zero"),
        pytest.param(10.01, id="bva-acima-de-dez"),
        pytest.param(-5, id="negativa"),
        pytest.param(70, id="escala-errada-0-a-100"),
        pytest.param(None, id="none"),
        pytest.param("7", id="string-numerica"),
        pytest.param(True, id="booleano"),
        pytest.param([7.0], id="lista"),
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="infinito"),
    ],
)
def test_classificar_aluno_rejeita_nota_invalida(nota_invalida: object) -> None:
    frequencia_valida = 90.0

    with pytest.raises(ValueError, match="nota deve"):
        classificar_aluno(nota_invalida, frequencia_valida)


@pytest.mark.unit
@pytest.mark.parametrize(
    "frequencia_invalida",
    [
        pytest.param(-0.01, id="bva-abaixo-de-zero"),
        pytest.param(100.01, id="bva-acima-de-cem"),
        pytest.param(-10, id="negativa"),
        pytest.param(750, id="erro-de-digitacao"),
        pytest.param(None, id="none"),
        pytest.param("90", id="string-numerica"),
        pytest.param("90%", id="string-com-percentual"),
        pytest.param(False, id="booleano"),
        pytest.param({}, id="dicionario-vazio"),
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("-inf"), id="infinito-negativo"),
    ],
)
def test_classificar_aluno_rejeita_frequencia_invalida(frequencia_invalida: object) -> None:
    nota_valida = 8.0

    with pytest.raises(ValueError, match="frequencia deve"):
        classificar_aluno(nota_valida, frequencia_invalida)


@pytest.mark.unit
def test_classificar_aluno_valida_nota_antes_de_aplicar_regra_de_frequencia() -> None:
    nota_invalida = 11.0
    frequencia_baixa = 10.0

    with pytest.raises(ValueError, match="nota deve estar entre 0 e 10"):
        classificar_aluno(nota_invalida, frequencia_baixa)


@pytest.mark.unit
def test_classificar_aluno_valida_frequencia_mesmo_com_nota_reprovada() -> None:
    
    nota_baixa = 1.0
    frequencia_invalida = 101.0

    with pytest.raises(ValueError, match="frequencia deve estar entre 0 e 100"):
        classificar_aluno(nota_baixa, frequencia_invalida)


@pytest.mark.unit
def test_classificar_aluno_com_ambas_entradas_invalidas_gera_value_error() -> None:
    nota_invalida, frequencia_invalida = -1.0, 200.0

    with pytest.raises(ValueError):
        classificar_aluno(nota_invalida, frequencia_invalida)
