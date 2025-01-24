import ast
import inspect
from collections.abc import Sequence
from typing import TypeVar, cast, List

import pyarrow as pa

V = TypeVar("V")


def promote_list(val: V | Sequence[V]) -> list[V]:
    """Ensure that the value is a list.

    Parameters
    ----------
    val
        Value to promote

    Returns
    -------
    list

    """
    if isinstance(val, list):
        return val
    elif isinstance(val, dict):
        return [val]
    elif val is None:
        return []
    else:
        return [val]


def risingwave_type_to_pyarrow(type: str):
    """
    Convert a SQL data type string to `pyarrow.DataType`.
    """
    t = type.upper()
    if t.endswith("[]"):
        return pa.list_(risingwave_type_to_pyarrow(type[:-2]))
    elif t.startswith("STRUCT"):
        return _parse_struct(t)
    return _simple_type(t)


def _parse_struct(type: str):
    # extract 'STRUCT<a:INT, b:VARCHAR, c:STRUCT<d:INT>, ...>'
    type_list = type[7:-1]  # strip "STRUCT<>"
    fields = []
    start = 0
    depth = 0
    for i, c in enumerate(type_list):
        if c == "<":
            depth += 1
        elif c == ">":
            depth -= 1
        elif c == "," and depth == 0:
            name, t = type_list[start:i].split(":", maxsplit=1)
            name = name.strip()
            t = t.strip()
            fields.append(pa.field(name, risingwave_type_to_pyarrow(t)))
            start = i + 1
    if ":" in type_list[start:].strip():
        name, t = type_list[start:].split(":", maxsplit=1)
        name = name.strip()
        t = t.strip()
        fields.append(pa.field(name, risingwave_type_to_pyarrow(t)))
    return pa.struct(fields)


def _simple_type(t: str):
    type_map = {
        "NULL": pa.null,
        "BOOLEAN": pa.bool_,
        "BOOL": pa.bool_,
        "TINYINT": pa.int8,
        "INT8": pa.int8,
        "SMALLINT": pa.int16,
        "INT16": pa.int16,
        "INT": pa.int32,
        "INTEGER": pa.int32,
        "INT32": pa.int32,
        "BIGINT": pa.int64,
        "INT64": pa.int64,
        "UINT8": pa.uint8,
        "UINT16": pa.uint16,
        "UINT32": pa.uint32,
        "UINT64": pa.uint64,
        "FLOAT32": pa.float32,
        "REAL": pa.float32,
        "FLOAT64": pa.float64,
        "DOUBLE PRECISION": pa.float64,
        "DOUBLE": pa.float64,
        "DATE32": pa.date32,
        "DATE": pa.date32,
        "TIME64": lambda: pa.time64("us"),
        "TIME": lambda: pa.time64("us"),
        "TIME WITHOUT TIME ZONE": lambda: pa.time64("us"),
        "TIMESTAMP": lambda: pa.timestamp("us"),
        "TIMESTAMP WITHOUT TIME ZONE": lambda: pa.timestamp("us"),
        "INTERVAL": pa.month_day_nano_interval,
        "STRING": pa.string,
        "VARCHAR": pa.string,
        "LARGE_STRING": pa.large_string,
        "BINARY": pa.binary,
        "BYTEA": pa.binary,
        "LARGE_BINARY": pa.large_binary,
    }

    if t in type_map:
        return type_map[t]()

    raise ValueError(f"Unsupported type: {t}")


def _is_running_ipython() -> bool:
    """Checks if we are currently running in IPython"""
    try:
        return get_ipython() is not None  # type: ignore[name-defined]
    except NameError:
        return False


def _get_ipython_cell_sources() -> list[str]:
    """Returns the source code of all cells in the running IPython session.
    See https://github.com/wandb/weave/pull/1864
    """
    shell = get_ipython()  # type: ignore[name-defined]  # noqa: F821
    if not hasattr(shell, "user_ns"):
        raise AttributeError("Cannot access user namespace")
    cells = cast(list[str], shell.user_ns["In"])
    # First cell is always empty
    return cells[1:]


def _extract_relevant_imports(
    import_statements: List[ast.AST], used_names: set
) -> List[str]:
    """Filter and format relevant import statements based on used names."""
    relevant_imports = []
    for node in import_statements:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname in used_names or alias.name in used_names:
                    relevant_imports.append(
                        f"import {alias.name}"
                        + (f" as {alias.asname}" if alias.asname else "")
                    )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.asname in used_names or alias.name in used_names:
                    relevant_imports.append(
                        f"from {node.module} import {alias.name}"
                        + (f" as {alias.asname}" if alias.asname else "")
                    )
    return relevant_imports


def _find_imports_and_used_names(source_code: str, func_source: str) -> List[str]:
    """Find imports and their relevance to the function source code."""
    module_ast = ast.parse(source_code)
    func_ast = ast.parse(func_source).body[0]

    import_statements = [
        node
        for node in ast.walk(module_ast)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]

    used_names = {node.id for node in ast.walk(func_ast) if isinstance(node, ast.Name)}

    return _extract_relevant_imports(import_statements, used_names)


def get_imports_used_in_function(func) -> str:
    """Get all relevant imports used in a function."""
    if _is_running_ipython():
        cell_sources = _get_ipython_cell_sources()
        imports = []
        for cell_source in cell_sources:
            try:
                imports.extend(
                    _find_imports_and_used_names(cell_source, inspect.getsource(func))
                )
            except Exception:
                continue
        return "\n".join(set(imports))

    else:
        module_source_code = inspect.getsource(inspect.getmodule(func))
        func_source = inspect.getsource(func)
        return "\n".join(_find_imports_and_used_names(module_source_code, func_source))
