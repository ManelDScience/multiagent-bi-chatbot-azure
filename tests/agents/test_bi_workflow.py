from unittest.mock import patch

from agents.workflows.bi_workflow import run_bi_workflow


def test_bi_workflow_runs_happy_path_without_revision():
    user_question = "¿Cuáles son los clientes con más ventas?"

    with patch("agents.workflows.bi_workflow.load_semantic_context") as mock_load_semantic_context, \
         patch("agents.workflows.bi_workflow.select_semantic_context") as mock_select_semantic_context, \
         patch("agents.workflows.bi_workflow.run_planner") as mock_run_planner, \
         patch("agents.workflows.bi_workflow.select_schema_context") as mock_select_schema_context, \
         patch("agents.workflows.bi_workflow.run_sql_agent") as mock_run_sql_agent, \
         patch("agents.workflows.bi_workflow.extract_sql_from_markdown") as mock_extract_sql, \
         patch("agents.workflows.bi_workflow.execute_sql") as mock_execute_sql, \
         patch("agents.workflows.bi_workflow.run_data_quality_agent") as mock_data_quality, \
         patch("agents.workflows.bi_workflow.run_analyst_agent") as mock_analyst, \
         patch("agents.workflows.bi_workflow.validate_table_coverage") as mock_table_validator, \
         patch("agents.workflows.bi_workflow.run_critic_agent") as mock_critic, \
         patch("agents.workflows.bi_workflow.get_normalized_critic_decision") as mock_decision, \
         patch("agents.workflows.bi_workflow.critic_requires_revision") as mock_requires_revision:

        mock_load_semantic_context.return_value = "full semantic context"
        mock_select_semantic_context.return_value = "selected semantic context"
        mock_run_planner.return_value = "planner output"
        mock_select_schema_context.return_value = "schema context"
        mock_run_sql_agent.return_value = "```sql\nSELECT TOP 10 * FROM agg.CustomerPerTotalSales;\n```"
        mock_extract_sql.return_value = "SELECT TOP 10 * FROM agg.CustomerPerTotalSales;"
        mock_execute_sql.return_value = '[{"CustomerName": "Tailspin Toys", "total_sales_perCustomer": 381585.35}]'
        mock_data_quality.return_value = "## Estado de calidad\n\nOK"
        mock_analyst.return_value = "Tailspin Toys: 381.585,35 €"
        mock_table_validator.return_value = "## Table Validator\n\nOK"
        mock_critic.return_value = "## Validación\n\nAPROBADA"
        mock_decision.return_value = "APROBADA"
        mock_requires_revision.return_value = False

        run_bi_workflow(user_question)

    mock_load_semantic_context.assert_called_once()
    mock_select_semantic_context.assert_called_once()
    mock_run_planner.assert_called_once()
    mock_select_schema_context.assert_called_once_with(user_question)
    mock_run_sql_agent.assert_called_once()
    mock_extract_sql.assert_called_once()
    mock_execute_sql.assert_called_once_with("SELECT TOP 10 * FROM agg.CustomerPerTotalSales;")
    mock_data_quality.assert_called_once()
    mock_analyst.assert_called_once()
    mock_table_validator.assert_called_once()
    mock_critic.assert_called_once()
    mock_requires_revision.assert_called_once()


def test_bi_workflow_approves_inconclusive_critic_when_table_validator_is_ok():
    user_question = "¿Cuáles son los clientes con más ventas?"

    with patch("agents.workflows.bi_workflow.load_semantic_context") as mock_load_semantic_context, \
         patch("agents.workflows.bi_workflow.select_semantic_context") as mock_select_semantic_context, \
         patch("agents.workflows.bi_workflow.run_planner") as mock_run_planner, \
         patch("agents.workflows.bi_workflow.select_schema_context") as mock_select_schema_context, \
         patch("agents.workflows.bi_workflow.run_sql_agent") as mock_run_sql_agent, \
         patch("agents.workflows.bi_workflow.extract_sql_from_markdown") as mock_extract_sql, \
         patch("agents.workflows.bi_workflow.execute_sql") as mock_execute_sql, \
         patch("agents.workflows.bi_workflow.run_data_quality_agent") as mock_data_quality, \
         patch("agents.workflows.bi_workflow.run_analyst_agent") as mock_analyst, \
         patch("agents.workflows.bi_workflow.validate_table_coverage") as mock_table_validator, \
         patch("agents.workflows.bi_workflow.run_critic_agent") as mock_critic, \
         patch("agents.workflows.bi_workflow.get_normalized_critic_decision") as mock_decision, \
         patch("agents.workflows.bi_workflow.critic_requires_revision") as mock_requires_revision:

        mock_load_semantic_context.return_value = "full semantic context"
        mock_select_semantic_context.return_value = "selected semantic context"
        mock_run_planner.return_value = "planner output"
        mock_select_schema_context.return_value = "schema context"
        mock_run_sql_agent.return_value = "```sql\nSELECT 1;\n```"
        mock_extract_sql.return_value = "SELECT 1;"
        mock_execute_sql.return_value = '[{"value": 1}]'
        mock_data_quality.return_value = "## Estado de calidad\n\nOK"
        mock_analyst.return_value = "Valor: 1"
        mock_table_validator.return_value = "## Table Validator\n\nOK"
        mock_critic.return_value = "Revisión no concluyente"
        mock_decision.return_value = "REQUIERE REVISIÓN"
        mock_requires_revision.return_value = True

        run_bi_workflow(user_question)

    assert mock_analyst.call_count == 1
    assert mock_table_validator.call_count == 1
    assert mock_critic.call_count == 1