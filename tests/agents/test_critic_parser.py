from agents.validators.critic_parser import (
    critic_requires_revision,
    get_normalized_critic_decision,
)


def test_critic_approved_when_recommendation_is_approved():
    text = """
## Validación

REQUIERE REVISIÓN

## Recomendación

APROBADA
"""

    assert critic_requires_revision(text) is False
    assert get_normalized_critic_decision(text) == "APROBADA"


def test_critic_requires_revision_when_no_approval_present():
    text = """
## Validación

REQUIERE REVISIÓN

## Recomendación

Corregir cifras incorrectas.
"""

    assert critic_requires_revision(text) is True
    assert get_normalized_critic_decision(text) == "REQUIERE REVISIÓN"


def test_critic_approved_directly():
    text = """
## Validación

APROBADA
"""

    assert critic_requires_revision(text) is False
    assert get_normalized_critic_decision(text) == "APROBADA"


def test_critic_requires_revision_when_inconclusive():
    text = "Revisión no concluyente"

    assert critic_requires_revision(text) is True
    assert get_normalized_critic_decision(text) == "REQUIERE REVISIÓN"