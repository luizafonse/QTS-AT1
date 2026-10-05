import pytest


@pytest.fixture
def aluno_em_recuperacao() -> dict[str, float]:
    """Aluno tipico em recuperacao: nota entre 5 e 6,9 e frequencia suficiente."""
    return {"nota": 6.0, "frequencia": 80.0}


@pytest.fixture
def aluno_aprovado() -> dict[str, float]:
    """Aluno tipico aprovado direto: nota >= 7 e frequencia >= 75."""
    return {"nota": 8.5, "frequencia": 90.0}


@pytest.fixture
def aluno_reprovado_por_nota() -> dict[str, float]:
    """Aluno tipico reprovado por nota < 5 com frequencia suficiente."""
    return {"nota": 3.0, "frequencia": 90.0}


@pytest.fixture
def aluno_reprovado_por_frequencia() -> dict[str, float]:
    """Aluno tipico reprovado por frequencia < 75, mesmo com nota alta."""
    return {"nota": 9.0, "frequencia": 60.0}
