from src.planner_agent import run_planner
from src.sql_agent import run_sql_agent
from src.schema_selector import select_schema_context
from src.mcp_client import execute_sql
from src.sql_parser import extract_sql_from_markdown
from src.analyst_agent import run_analyst_agent
from src.critic_agent import run_critic_agent

def main():
    print("Multi-Agent BI Assistant")
    print("------------------------")

    user_question = input("\nPregunta de negocio: ")

    planner_output = run_planner(user_question)

    print("\n[Planner Agent]")
    print(planner_output)

    schema_context = select_schema_context(user_question)

    print("\n[Schema Selector]")
    print(schema_context)

    sql_output = run_sql_agent(
        user_question=user_question,
        planner_output=planner_output,
        schema_available=True,
        schema_context=schema_context,
    )

    print("\n[SQL Agent]")
    sql_query = extract_sql_from_markdown(sql_output)

    print("\n[SQL Ejecutada]")
    print(sql_query)

    query_result = execute_sql(sql_query)

    print("\n[Resultado MCP]")
    print(query_result)

    analyst_output = run_analyst_agent(
    user_question=user_question,
    query_result=query_result,
    )

    print("\n[Analyst Agent]")
    print(analyst_output)

    critic_output = run_critic_agent(
    user_question=user_question,
    query_result=query_result,
    analyst_output=analyst_output,
    )


    if "REQUIERE REVISIÓN" in critic_output.upper():
        print("\n[Revisión automática]")
        print("El Critic Agent ha pedido revisión. Reformulando respuesta...")

        analyst_output = run_analyst_agent(
            user_question=user_question,
            query_result=query_result,
            critic_feedback=critic_output,
        )

        print("\n[Analyst Agent - Revisado]")
        print(analyst_output)

        critic_output = run_critic_agent(
            user_question=user_question,
            query_result=query_result,
            analyst_output=analyst_output,
        )

        print("\n[Critic Agent - Revisión final]")
        print(critic_output)


if __name__ == "__main__":
    main()