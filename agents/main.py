from src.planner_agent import run_planner


def main():
    print("Multi-Agent BI Assistant")
    print("------------------------")

    user_question = input("\nPregunta de negocio: ")

    planner_output = run_planner(user_question)

    print("\n[Planner Agent]")
    print(planner_output)


if __name__ == "__main__":
    main()