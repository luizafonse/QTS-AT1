"""Testes unitarios das funcoes de validacao (validar_nota e validar_frequencia).

Tecnicas aplicadas:
    - Particionamento de Equivalencia (EP): classes validas e invalidas.
    - Analise do Valor Limite (BVA): valores nas fronteiras 0 e 10 (nota),
      0 e 100 (frequencia), com valores imediatamente dentro e fora.
    - Error Guessing: tipos inesperados, NaN, infinito, booleanos, etc.
"""

from decimal import Decimal

import pytest

from app.aprovacao import validar_frequencia, validar_nota



@pytest.mark.unit
@pytest.mark.parametrize(
    "nota_entrada, nota_esperada",
    [
        pytest.param(0, 0.0, id="bva-limite-inferior-inteiro"),
        pytest.param(0.0, 0.0, id="bva-limite-inferior-float"),
        pytest.param(0.01, 0.01, id="bva-logo-acima-do-limite-inferior"),
        pytest.param(4.99, 4.99, id="ep-faixa-reprovado"),
        pytest.param(5, 5.0, id="ep-faixa-recuperacao-inicio"),
        pytest.param(6.9, 6.9, id="ep-faixa-recuperacao-fim"),
        pytest.param(7, 7.0, id="ep-faixa-aprovado-inicio"),
        pytest.param(9.99, 9.99, id="bva-logo-abaixo-do-limite-superior"),
        pytest.param(10, 10.0, id="bva-limite-superior-inteiro"),
        pytest.param(10.0, 10.0, id="bva-limite-superior-float"),
    ],
)
def test_validar_nota_aceita_valores_validos(nota_entrada: float, nota_esperada: float) -> None:

    resultado = validar_nota(nota_entrada)

    assert resultado == nota_esperada


@pytest.mark.unit
@pytest.mark.parametrize("nota_inteira", [0, 5, 7, 10])
def test_validar_nota_converte_inteiro_para_float(nota_inteira: int) -> None:

    resultado = validar_nota(nota_inteira)

    assert isinstance(resultado, float)




@pytest.mark.unit
@pytest.mark.parametrize(
    "nota_invalida",
    [
        pytest.param(-0.01, id="bva-logo-abaixo-do-limite-inferior"),
        pytest.param(-1, id="ep-negativa-pequena"),
        pytest.param(-100, id="ep-negativa-grande"),
        pytest.param(10.01, id="bva-logo-acima-do-limite-superior"),
        pytest.param(11, id="ep-acima-de-dez-inteiro"),
        pytest.param(100, id="ep-escala-percentual-por-engano"),
        pytest.param(1000.5, id="ep-muito-acima"),
    ],
)
def test_validar_nota_rejeita_fora_do_intervalo(nota_invalida: float) -> None:

    with pytest.raises(ValueError, match="nota deve estar entre 0 e 10"):
        validar_nota(nota_invalida)




@pytest.mark.unit
@pytest.mark.parametrize(
    "valor_inesperado",
    [
        pytest.param(None, id="none"),
        pytest.param("7", id="string-numerica"),
        pytest.param("", id="string-vazia"),
        pytest.param("abc", id="string-texto"),
        pytest.param([7], id="lista"),
        pytest.param((7,), id="tupla"),
        pytest.param({"nota": 7}, id="dicionario"),
        pytest.param(True, id="booleano-true"),
        pytest.param(False, id="booleano-false"),
        pytest.param(7 + 0j, id="complexo"),
        pytest.param(Decimal("7"), id="decimal"),
        pytest.param(object(), id="objeto-generico"),
        pytest.param(b"7", id="bytes"),
    ],
)
def test_validar_nota_rejeita_tipos_inesperados(valor_inesperado: object) -> None:

    with pytest.raises(ValueError, match="nota deve ser um numero"):
        validar_nota(valor_inesperado)


@pytest.mark.unit
@pytest.mark.parametrize(
    "valor_nao_finito",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="infinito-positivo"),
        pytest.param(float("-inf"), id="infinito-negativo"),
        pytest.param(10**400, id="inteiro-gigante-estoura-float"),
        pytest.param(-(10**400), id="inteiro-gigante-negativo"),
    ],
)
def test_validar_nota_rejeita_valores_nao_finitos(valor_nao_finito: float) -> None:

    with pytest.raises(ValueError, match="nota deve ser um numero finito"):
        validar_nota(valor_nao_finito)


@pytest.mark.unit
def test_validar_nota_usa_nome_personalizado_na_mensagem_de_erro() -> None:
    nome_campo = "nota_recuperacao"

    with pytest.raises(ValueError, match="nota_recuperacao deve estar entre 0 e 10"):
        validar_nota(11, nome=nome_campo)


@pytest.mark.unit
def test_validar_nota_mensagem_informa_o_valor_recebido() -> None:
    nota_invalida = 12.5

    with pytest.raises(ValueError, match="recebido: 12.5"):
        validar_nota(nota_invalida)


@pytest.mark.unit
def test_validar_nota_mensagem_de_tipo_informa_o_tipo_recebido() -> None:
    valor = "7"

    with pytest.raises(ValueError, match="recebido: str"):
        validar_nota(valor)




@pytest.mark.unit
@pytest.mark.parametrize(
    "frequencia_entrada, frequencia_esperada",
    [
        pytest.param(0, 0.0, id="bva-limite-inferior-inteiro"),
        pytest.param(0.0, 0.0, id="bva-limite-inferior-float"),
        pytest.param(0.01, 0.01, id="bva-logo-acima-do-limite-inferior"),
        pytest.param(50, 50.0, id="ep-faixa-insuficiente"),
        pytest.param(74.99, 74.99, id="bva-logo-abaixo-do-minimo-de-aprovacao"),
        pytest.param(75, 75.0, id="bva-minimo-de-aprovacao"),
        pytest.param(75.01, 75.01, id="bva-logo-acima-do-minimo-de-aprovacao"),
        pytest.param(99.99, 99.99, id="bva-logo-abaixo-do-limite-superior"),
        pytest.param(100, 100.0, id="bva-limite-superior-inteiro"),
        pytest.param(100.0, 100.0, id="bva-limite-superior-float"),
    ],
)
def test_validar_frequencia_aceita_valores_validos(frequencia_entrada: float, frequencia_esperada: float) -> None:

    resultado = validar_frequencia(frequencia_entrada)

    assert resultado == frequencia_esperada
    assert isinstance(resultado, float)




@pytest.mark.unit
@pytest.mark.parametrize(
    "frequencia_invalida",
    [
        pytest.param(-0.01, id="bva-logo-abaixo-do-limite-inferior"),
        pytest.param(-1, id="ep-negativa-pequena"),
        pytest.param(-75, id="ep-negativa-simetrica-ao-minimo"),
        pytest.param(100.01, id="bva-logo-acima-do-limite-superior"),
        pytest.param(101, id="ep-acima-de-cem-inteiro"),
        pytest.param(750, id="ep-erro-de-digitacao"),
        pytest.param(1e6, id="ep-muito-acima"),
    ],
)
def test_validar_frequencia_rejeita_fora_do_intervalo(frequencia_invalida: float) -> None:

    with pytest.raises(ValueError, match="frequencia deve estar entre 0 e 100"):
        validar_frequencia(frequencia_invalida)




@pytest.mark.unit
@pytest.mark.parametrize(
    "valor_inesperado",
    [
        pytest.param(None, id="none"),
        pytest.param("80", id="string-numerica"),
        pytest.param("80%", id="string-com-percentual"),
        pytest.param("", id="string-vazia"),
        pytest.param([80], id="lista"),
        pytest.param({"frequencia": 80}, id="dicionario"),
        pytest.param(True, id="booleano-true"),
        pytest.param(False, id="booleano-false"),
        pytest.param(80 + 0j, id="complexo"),
        pytest.param(Decimal("80"), id="decimal"),
        pytest.param(object(), id="objeto-generico"),
    ],
)
def test_validar_frequencia_rejeita_tipos_inesperados(valor_inesperado: object) -> None:

    with pytest.raises(ValueError, match="frequencia deve ser um numero"):
        validar_frequencia(valor_inesperado)


@pytest.mark.unit
@pytest.mark.parametrize(
    "valor_nao_finito",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="infinito-positivo"),
        pytest.param(float("-inf"), id="infinito-negativo"),
        pytest.param(10**400, id="inteiro-gigante-estoura-float"),
    ],
)
def test_validar_frequencia_rejeita_valores_nao_finitos(valor_nao_finito: float) -> None:

    with pytest.raises(ValueError, match="frequencia deve ser um numero finito"):
        validar_frequencia(valor_nao_finito)
