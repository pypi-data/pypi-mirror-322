from __future__ import annotations

import json
from datetime import datetime
from enum import Enum
from typing import Any, Union

from ..data_model import DataModel


def _str_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool, dict, list)):
        return json.dumps(value)
    return str(value)


class Parameter(DataModel):
    name: str

    def __str__(self) -> str:
        return f"@{self.name}"


class Ref(DataModel):
    path: str

    def __str__(self) -> str:
        return f"{{{{{self.path}}}}}"

    @staticmethod
    def parse(str: str) -> Ref:
        if str.startswith("{{") and str.endswith("}}"):
            return Ref(path=str[2:-2])
        raise ValueError("Ref format error")


class FunctionNamespace:
    BUILTIN = "builtin"


class Function(DataModel):
    name: str
    args: tuple = ()
    named_args: dict = dict()
    namespace: str = FunctionNamespace.BUILTIN

    def __str__(self) -> str:
        if self.namespace == FunctionNamespace.BUILTIN:
            str = f"{self.name}"
        else:
            str = f"{self.namespace}.{self.name}"
        str = str + self._str_args()
        return str

    def _str_args(self):
        if len(self.args) > 0:
            return f"({', '.join(_str_value(a) for a in self.args)})"
        elif len(self.named_args) > 0:
            str_args = []
            for k, v in self.named_args.items():
                str_args.append(f"{k}={_str_value(v)}")
            return f"({', '.join(a for a in str_args)})"
        else:
            return "()"


class Undefined(DataModel):
    pass


class Field(DataModel):
    path: str

    def __str__(self) -> str:
        return self.path


class Collection(DataModel):
    name: str

    def __str__(self) -> str:
        return self.name


class Comparison(DataModel):
    lexpr: Expression
    op: ComparisonOp
    rexpr: Expression

    def __str__(self) -> str:
        str = f"{_str_value(self.lexpr)} {self.op.value} "
        if self.op == ComparisonOp.BETWEEN and isinstance(self.rexpr, list):
            str = f"""{str}{_str_value(
                self.rexpr[0])} AND {_str_value(self.rexpr[1])}"""
        elif (
            self.op == ComparisonOp.IN or self.op == ComparisonOp.NIN
        ) and isinstance(self.rexpr, list):
            str = f"""{str}({', '.join(_str_value(i) for i in self.rexpr)})"""
        else:
            str = str + _str_value(self.rexpr)
        return str

    @staticmethod
    def reverse_op(op: ComparisonOp) -> ComparisonOp:
        if op == ComparisonOp.GT:
            return ComparisonOp.LT
        if op == ComparisonOp.GTE:
            return ComparisonOp.LTE
        if op == ComparisonOp.LT:
            return ComparisonOp.GT
        if op == ComparisonOp.LTE:
            return ComparisonOp.GTE
        return op


class ComparisonOp(str, Enum):
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    EQ = "="
    NEQ = "!="
    IN = "in"
    NIN = "not in"
    BETWEEN = "between"
    LIKE = "like"


class And(DataModel):
    lexpr: Expression
    rexpr: Expression

    def __str__(self) -> str:
        return f"({_str_value(self.lexpr)} AND {_str_value(self.rexpr)})"


class Or(DataModel):
    lexpr: Expression
    rexpr: Expression

    def __str__(self) -> str:
        return f"({_str_value(self.lexpr)} OR {_str_value(self.rexpr)})"


class Not(DataModel):
    expr: Expression

    def __str__(self) -> str:
        return f"NOT {_str_value(self.expr)}"


class Update(DataModel):
    operations: list[UpdateOperation] = []

    def put(self, field: str, value: Expression) -> Update:
        self.operations.append(
            UpdateOperation(
                field=field,
                op=UpdateOp.PUT,
                args=tuple([value]),
            )
        )
        return self

    def insert(self, field: str, value: Expression) -> Update:
        self.operations.append(
            UpdateOperation(
                field=field,
                op=UpdateOp.INSERT,
                args=tuple([value]),
            )
        )
        return self

    def delete(self, field: str) -> Update:
        self.operations.append(
            UpdateOperation(
                field=field,
                op=UpdateOp.DELETE,
            )
        )
        return self

    def increment(self, field: str, value: Expression) -> Update:
        self.operations.append(
            UpdateOperation(
                field=field,
                op=UpdateOp.INCREMENT,
                args=tuple([value]),
            )
        )
        return self

    def move(self, field: str, dest: str) -> Update:
        self.operations.append(
            UpdateOperation(
                field=field,
                op=UpdateOp.MOVE,
                args=tuple([dest]),
            )
        )
        return self

    def array_union(self, field: str, value: Expression) -> Update:
        self.operations.append(
            UpdateOperation(
                field=field,
                op=UpdateOp.ARRAY_UNION,
                args=tuple([value]),
            )
        )
        return self

    def array_remove(self, field: str, value: Expression) -> Update:
        self.operations.append(
            UpdateOperation(
                field=field,
                op=UpdateOp.ARRAY_REMOVE,
                args=tuple([value]),
            )
        )
        return self

    def __str__(self) -> str:
        return f"{', '.join(f'{str(o)}' for o in self.operations)}"


class UpdateOperation(DataModel):
    field: str
    op: UpdateOp
    args: tuple = ()

    def __str__(self) -> str:
        str_args = None
        if self.args is not None:
            str_args = f"{', '.join(_str_value(a) for a in self.args)}"
        if self.args is not None:
            return f"{self.field}={self.op.value}({str_args})"
        else:
            return f"{self.field}={self.op.value}()"


class UpdateOp(str, Enum):
    PUT = "put"
    """Added if it doesn't exist
    Replace if it exists
    Array element replaced at index"""

    INSERT = "insert"
    """Added if it doesn't exist.
    Replace if it exists
    Array element added at index
    Use index - to insert at the end"""

    DELETE = "delete"
    """Removes field
    Array element removed at index"""

    INCREMENT = "increment"
    """Increment or decrement number
    Creates field if it doesn't exist"""

    MOVE = "move"
    """Move value from source to destination field"""

    ARRAY_UNION = "array_union"
    """Union values with array without duplicates"""

    ARRAY_REMOVE = "array_remove"
    """Remove values from array"""


class Select(DataModel):
    terms: list[SelectTerm] = []

    def add_field(self, field: str, alias: str | None = None):
        self.terms.append(SelectTerm(field=field, alias=alias))

    def __str__(self) -> str:
        if len(self.terms) == 0:
            return "*"
        return f"{', '.join(str(t) for t in self.terms)}"


class SelectTerm(DataModel):
    field: str
    alias: str | None

    def __str__(self) -> str:
        str = self.field
        if self.alias is not None:
            str = f"{self.field} AS {self.alias}"
        return str


class OrderBy(DataModel):
    terms: list[OrderByTerm] = []

    def add_field(
        self,
        field: str,
        direction: OrderByDirection | None = None,
    ) -> OrderBy:
        self.terms.append(OrderByTerm(field=field, direction=direction))
        return self

    def __str__(self) -> str:
        return ", ".join([str(t) for t in self.terms])


class OrderByTerm(DataModel):
    field: str
    direction: OrderByDirection | None = None

    def __str__(self) -> str:
        str = self.field
        if self.direction:
            str = f"{str} {self.direction.value}"
        return str


class OrderByDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


Value = Union[
    str, int, float, bool, dict, list, bytes, datetime, DataModel, None
]
Expression = Union[
    Comparison, And, Or, Not, Function, Parameter, Ref, Field, Value
]
