from unittest.mock import patch

from agents import main


def test_main_delegates_to_bi_workflow():
    with patch("builtins.input", return_value="¿Cuáles son los clientes con más ventas?"):
        with patch("agents.main.run_bi_workflow") as mock_run_bi_workflow:
            main.main()

    mock_run_bi_workflow.assert_called_once_with(
        "¿Cuáles son los clientes con más ventas?"
    )