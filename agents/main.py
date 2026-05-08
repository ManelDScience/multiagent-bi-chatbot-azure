from src.planner_agent import run_planner
from src.sql_agent import run_sql_agent 


def main():
    print("Multi-Agent BI Assistant")
    print("------------------------")

    user_question = input("\nPregunta de negocio: ")

    planner_output = run_planner(user_question)

    print("\n[Planner Agent]")
    print(planner_output)

    sql_output = run_sql_agent(user_question, planner_output)

    print("\n[SQL Agent]")
    print(sql_output)


if __name__ == "__main__":
    main()