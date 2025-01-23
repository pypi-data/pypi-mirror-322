import json
import os
import re
from typing import Any, Callable
from .data import JsonPathExpression, SnippetData
from .result import AssertionResult, Op, Severity


class Finding:
    def __init__(
        self,
        name: str,
        severity: Severity,
        data: SnippetData | None = None
    ):
        self.name = name

        if not isinstance(severity, Severity):
            raise ValueError(
                f"Severity must be a Severity enum, got {severity}"
            )
        self.severity = severity

        if data is None:
            try:
                path = os.environ["LUNAR_VAR_LUNAR_BUNDLE_PATH"]
                data = SnippetData(path)
            except KeyError:
                raise ValueError(
                    "LUNAR_VAR_LUNAR_BUNDLE_PATH is not set"
                )
            except ValueError as e:
                raise ValueError(
                    "invalid LUNAR_VAR_LUNAR_BUNDLE_PATH"
                ) from e
            except FileNotFoundError:
                raise ValueError(
                    f"LUNAR_VAR_LUNAR_BUNDLE_PATH does not exist: {path}"
                )

        if not isinstance(data, SnippetData):
            raise ValueError(
                f"Data must be a SnippetData instance, got {data}"
            )
        self.data = data

        self._accessed_paths = []
        self._used_vars = []
        self._results = []
        self._submitted = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.submit()

    def submit(self):
        if not self._submitted:
            results_json = [result.toJson() for result in self._results]
            print(json.dumps(results_json), end="")
            self._submitted = True

    def _make_assertion(
        self,
        op: Op,
        check_fn: Callable[[Any], bool],
        value: Any,
        error_message: str,
        success_message: str
    ) -> AssertionResult:
        path = None
        actual_value = value

        if isinstance(value, str) and value.startswith("."):
            try:
                jsonPath = JsonPathExpression(value)
                actual_value = self.data.get(jsonPath)
                path = jsonPath.full_path
            except ValueError:
                actual_value = value

        ok = check_fn(actual_value)
        self._results.append(
            AssertionResult(
                op=op,
                args=[actual_value],
                ok=ok,
                severity=Severity.OK if ok else self.severity,
                details=success_message if ok else error_message,
                path=path
            )
        )

    def get(self, path: str):
        try:
            jsonPath = JsonPathExpression(path)
            self._accessed_paths.append(jsonPath.full_path)
            return self.data.get(jsonPath)
        except ValueError:
            return path

    def assert_true(
        self,
        value: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.TRUE,
            lambda v: v is True,
            value,
            error_message or f"{value} is not true",
            success_message or f"{value} is true"
        )

    def assert_false(
        self,
        value: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.FALSE,
            lambda v: v is False,
            value,
            error_message or f"{value} is not false",
            success_message or f"{value} is false"
        )

    def assert_equals(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.EQUALS,
            lambda v: v == expected,
            value,
            error_message or f"{value} is not equal to {expected}",
            success_message or f"{value} is equal to {expected}"
        )

    def assert_contains(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.CONTAINS,
            lambda v: expected in v,
            value,
            error_message or f"{value} does not contain {expected}",
            success_message or f"{value} contains {expected}"
        )

    def assert_greater(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.GREATER,
            lambda v: v > expected,
            value,
            error_message or f"{value} is not greater than {expected}",
            success_message or f"{value} is greater than {expected}"
        )

    def assert_greater_or_equal(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.GREATER_OR_EQUAL,
            lambda v: v >= expected,
            value,
            error_message or
            f"{value} is not greater than or equal to {expected}",
            success_message or
            f"{value} is greater than or equal to {expected}"
        )

    def assert_less(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.LESS,
            lambda v: v < expected,
            value,
            error_message or f"{value} is not less than {expected}",
            success_message or f"{value} is less than {expected}"
        )

    def assert_less_or_equal(
        self,
        value: Any,
        expected: Any,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.LESS_OR_EQUAL,
            lambda v: v <= expected,
            value,
            error_message or
            f"{value} is not less than or equal to {expected}",
            success_message or
            f"{value} is less than or equal to {expected}"
        )

    def assert_match(
        self,
        value: Any,
        pattern: str,
        error_message: str | None = None,
        success_message: str | None = None
    ):
        self._make_assertion(
            Op.MATCH,
            lambda v: re.match(pattern, v) is not None,
            value,
            error_message or f"{value} does not match {pattern}",
            success_message or f"{value} matches {pattern}"
        )
