"""Regras de negocio do Sistema de Aprovacao de Aluno.

Modulo puro e deterministico: nao ha I/O, relogio, aleatoriedade nem estado
global. Toda entrada invalida gera ``ValueError`` com mensagem descritiva.
"""

import math
from enum import StrEnum

NOTA_MINIMA: float = 0.0
NOTA_MAXIMA: float = 10.0
NOTA_APROVACAO: float = 7.0
NOTA_RECUPERACAO_MINIMA: float = 5.0

FREQUENCIA_MINIMA_VALIDA: float = 0.0
FREQUENCIA_MAXIMA_VALIDA: float = 100.0
FREQUENCIA_MINIMA_APROVACAO: float = 75.0


class SituacaoAluno(StrEnum):
    """Situacoes finais possiveis de um aluno."""

    APROVADO = "aprovado"
    RECUPERACAO = "recuperacao"
    REPROVADO = "reprovado"
    APROVADO_EM_RECUPERACAO = "aprovado_em_recuperacao"


def _converter_para_numero(valor: object, nome: str) -> float:
    """Garante que o valor e um numero real finito (int ou float, nunca bool).

    Raises:
        ValueError: se o tipo nao for numerico, se for booleano ou se o valor
            nao for finito (NaN, infinito ou inteiro grande demais).
    """
    if isinstance(valor, bool) or not isinstance(valor, int | float):
        raise ValueError(f"{nome} deve ser um numero (int ou float), recebido: {type(valor).__name__}")

    try:
        numero = float(valor)
    except OverflowError:
        raise ValueError(f"{nome} deve ser um numero finito") from None

    if not math.isfinite(numero):
        raise ValueError(f"{nome} deve ser um numero finito")

    return numero


def validar_nota(nota: object, nome: str = "nota") -> float:
    """Valida que a nota esta no intervalo fechado [0, 10] e a devolve como float.

    Raises:
        ValueError: se a nota nao for numerica ou estiver fora de 0 a 10.
    """
    valor = _converter_para_numero(nota, nome)

    if not NOTA_MINIMA <= valor <= NOTA_MAXIMA:
        raise ValueError(f"{nome} deve estar entre 0 e 10, recebido: {valor}")

    return valor


def validar_frequencia(frequencia: object) -> float:
    """Valida que a frequencia (%) esta no intervalo fechado [0, 100].

    Raises:
        ValueError: se a frequencia nao for numerica ou estiver fora de 0 a 100.
    """
    valor = _converter_para_numero(frequencia, "frequencia")

    if not FREQUENCIA_MINIMA_VALIDA <= valor <= FREQUENCIA_MAXIMA_VALIDA:
        raise ValueError(f"frequencia deve estar entre 0 e 100, recebido: {valor}")

    return valor


def classificar_aluno(nota: float, frequencia: float) -> SituacaoAluno:
    """Classifica o aluno a partir da nota final e da frequencia (%).

    Ordem de decisao (a frequencia tem precedencia sobre a nota):
        1. frequencia < 75            -> REPROVADO
        2. nota >= 7                  -> APROVADO
        3. 5 <= nota < 7              -> RECUPERACAO
        4. nota < 5                   -> REPROVADO

    Raises:
        ValueError: se nota ou frequencia forem invalidas.
    """
    nota_valida = validar_nota(nota)
    frequencia_valida = validar_frequencia(frequencia)

    if frequencia_valida < FREQUENCIA_MINIMA_APROVACAO:
        return SituacaoAluno.REPROVADO

    if nota_valida >= NOTA_APROVACAO:
        return SituacaoAluno.APROVADO

    if nota_valida >= NOTA_RECUPERACAO_MINIMA:
        return SituacaoAluno.RECUPERACAO

    return SituacaoAluno.REPROVADO


def avaliar_recuperacao(nota: float, frequencia: float, nota_recuperacao: float) -> SituacaoAluno:
    """Avalia o resultado final de um aluno que estava em recuperacao.

    Regras:
        - nota_recuperacao >= 5 -> APROVADO_EM_RECUPERACAO
        - nota_recuperacao <  5 -> REPROVADO

    Raises:
        ValueError: se qualquer entrada for invalida ou se o aluno nao estiver
            na situacao RECUPERACAO (apenas quem esta em recuperacao pode fazer
            a prova de recuperacao).
    """
    nota_rec_valida = validar_nota(nota_recuperacao, nome="nota_recuperacao")
    situacao_atual = classificar_aluno(nota, frequencia)

    if situacao_atual is not SituacaoAluno.RECUPERACAO:
        raise ValueError(
            f"apenas alunos em recuperacao podem ser avaliados na recuperacao, situacao atual: {situacao_atual.value}"
        )

    if nota_rec_valida >= NOTA_RECUPERACAO_MINIMA:
        return SituacaoAluno.APROVADO_EM_RECUPERACAO

    return SituacaoAluno.REPROVADO
