from context_selectors.semantic_loader import load_semantic_context
from context_selectors.semantic_selector import select_semantic_context
from context_selectors.schema_selector import select_schema_context


def run_bi_workflow_maf_spike(user_question: str) -> None:
    full_semantic_context = load_semantic_context()

    semantic_context = select_semantic_context(
        user_question=user_question,
        semantic_context=full_semantic_context,
    )

    schema_context = select_schema_context(user_question)

    print("\n[MAF Spike]")
    print("User question:")
    print(user_question)

    print("\n[Semantic Context]")
    print(semantic_context)

    print("\n[Schema Context]")
    print(schema_context)