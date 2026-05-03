from config import get_model_config


def main():
    model_config = get_model_config()

    print("Multi-Agent BI Assistant")
    print("------------------------")
    print(f"Modelo configurado: {model_config['model']}")

    user_question = input("\nPregunta de negocio: ")

    print("\n[Planner Agent]")
    print(f"Analizaría la pregunta: {user_question}")

    print("\n[SQL Agent]")
    print("Generaría una consulta SQL basada en el plan.")

    print("\n[Critic Agent]")
    print("Validaría si la consulta responde a la pregunta.")


if __name__ == "__main__":
    main()