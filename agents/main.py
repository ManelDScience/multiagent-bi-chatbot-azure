from workflows.bi_workflow import run_bi_workflow


def main():
    print("Multi-Agent BI Assistant")
    print("------------------------")

    user_question = input("\nPregunta de negocio: ")

    run_bi_workflow(user_question)


if __name__ == "__main__":
    main()