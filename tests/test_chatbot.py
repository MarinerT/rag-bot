from unittest.mock import patch, MagicMock
import pytest

from chatbot import cbfs


@pytest.fixture
def mock_env(monkeypatch):
    # Mock environment variables if necessary
    monkeypatch.setenv("OPENAI_API_KEY", "testkey")


@patch("chatbot.load_db")
def test_cbfs_init(mock_load_db, mock_env):
    # Mock load_db to not perform any action
    mock_load_db.return_value = MagicMock()

    # Instantiate cbfs with a mock pdf document
    test_cbfs = cbfs(pdf_doc="resume.pdf")

    # Assertions
    assert test_cbfs.loaded_file == "resume.pdf"
    mock_load_db.assert_called_once_with("resume.pdf", "stuff", 10)
