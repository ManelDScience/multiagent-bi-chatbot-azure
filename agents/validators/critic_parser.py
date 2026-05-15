def critic_requires_revision(critic_output: str) -> bool:
    text = critic_output.upper()

    if "NO CONCLUYENTE" in text:
        return True

    if "RECOMENDACIÓN" in text and "APROBADA" in text:
        return False

    if "APROBADA" in text or "APROBADO" in text:
        return False

    if "REQUIERE REVISIÓN" in text or "REQUIERE REVISION" in text:
        return True

    return True


def get_normalized_critic_decision(critic_output: str) -> str:
    return "REQUIERE REVISIÓN" if critic_requires_revision(critic_output) else "APROBADA"