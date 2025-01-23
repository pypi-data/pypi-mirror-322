import json
from pathlib import Path
import pytest
from src.lunar_snippets import (
    Finding,
    Severity
)


class TestFinding():
    @pytest.fixture(autouse=True)
    def setup_lunar_bundle(self, monkeypatch):
        monkeypatch.setenv(
            'LUNAR_VAR_LUNAR_BUNDLE_PATH',
            str(Path(__file__).parent / "sample.json")
        )
        yield

    def test_simple_value_finding(self, capsys):
        with Finding("test", Severity.OK) as f:
            f.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)[0]

        assert result["op"] == "true"
        assert result["args"] == [True]
        assert result["ok"] is True
        assert result["severity"] == "ok"
        assert result["details"] == "True is true"
        assert result["path"] is None

    def test_simple_path_finding(self, capsys):
        with Finding("test", Severity.OK) as f:
            f.assert_true(".test_true")

        captured = capsys.readouterr()
        result = json.loads(captured.out)[0]

        assert result["op"] == "true"
        assert result["args"] == [True]
        assert result["ok"] is True
        assert result["severity"] == "ok"
        assert result["details"] == ".test_true is true"
        assert result["path"] == "$.test_true"

    def test_multiple_assertions_in_finding(self, capsys):
        with Finding("test", Severity.OK) as f:
            f.assert_true(True)
            f.assert_true(".test_true")

        captured = capsys.readouterr()
        results = json.loads(captured.out)
        assert all(result["ok"] for result in results)

    def test_all_value_assertions_in_finding(self, capsys):
        with Finding("test", Severity.OK) as f:
            f.assert_true(True)
            f.assert_false(False)
            f.assert_equals(1, 1)
            f.assert_greater(2, 1)
            f.assert_greater_or_equal(2, 1)
            f.assert_greater_or_equal(1, 1)
            f.assert_less(1, 2)
            f.assert_less_or_equal(1, 1)
            f.assert_contains("hello", "e")
            f.assert_match("hello", ".*ell.*")

        captured = capsys.readouterr()
        results = json.loads(captured.out)
        assert all(result["ok"] for result in results)
