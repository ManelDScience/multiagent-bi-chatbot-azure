from maf_workflows.bi_workflow_maf import run_bi_workflow_maf_spike


def main():
    user_question = input("\nPregunta de negocio: ")
    run_bi_workflow_maf_spike(user_question)


if __name__ == "__main__":
    main()