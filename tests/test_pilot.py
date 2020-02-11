# tests/test_pilot.py
import click.testing
import pytest
import requests

from newsroom import pilot


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("newsroom.wikipedia.random_page")


def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(pilot.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with("pl")


def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(pilot.main)
    assert result.exit_code == 0


def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(pilot.main)
    assert "Lorem Ipsum" in result.output


def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    runner.invoke(pilot.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(pilot.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(pilot.main)
    assert "Error" in result.output


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    result = runner.invoke(pilot.main)
    assert result.exit_code == 0
