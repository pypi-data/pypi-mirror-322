from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional
from dataclasses import asdict


class Severity(Enum):
    OK = "ok"
    WARN = "warn"
    CRITICAL = "critical"


class Op(Enum):
    CONTAINS = "contains"
    EQUALS = "equals"
    TRUE = "true"
    FALSE = "false"
    GREATER = "greater"
    GREATER_OR_EQUAL = "greater_or_equal"
    LESS = "less"
    LESS_OR_EQUAL = "less_or_equal"
    MATCH = "match"


@dataclass
class AssertionResult:
    op: Op
    args: list[Any]
    ok: bool
    severity: Severity
    details: str
    path: Optional[str] = None

    def toJson(self):
        result = asdict(self)
        # Convert enum values to their string representations
        result['op'] = self.op.value
        result['severity'] = self.severity.value
        return result
