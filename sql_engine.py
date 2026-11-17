import sqlite3
import calendar
import re

def create_connection(schema_sql="", data_sql=""):
    """
    Creates an in-memory SQLite database populated with custom MySQL-compatible functions
    and pre-loaded with the specified schema and dataset.
    """
    conn = sqlite3.connect(":memory:")
    
    # Register MySQL date functions
    conn.create_function("YEAR", 1, lambda d: int(str(d).split("-")[0]) if d else None)
    conn.create_function("MONTH", 1, lambda d: int(str(d).split("-")[1]) if d else None)
    conn.create_function("MONTHNAME", 1, lambda d: calendar.month_name[int(str(d).split("-")[1])] if d else None)
    
    # Register MySQL ROUND function if custom precision is needed
    conn.create_function("ROUND_MYSQL", 2, lambda val, prec: round(float(val), int(prec)) if val is not None else None)

    cursor = conn.cursor()

    # Clean MySQL-specific non-SQLite syntax:
    # 1. Ignore CREATE DATABASE, USE statements
    # 2. SQLite supports CHECK, but remove unsupported clauses if any
    all_sql = f"{schema_sql}\n{data_sql}"
    
    statements = []
    current_stmt = []
    in_str = False
    quote_char = ''

    for line in all_sql.splitlines():
        line_clean = line.strip()
        if not line_clean or line_clean.startswith('--') or line_clean.startswith('/*'):
            continue
        if line_clean.upper().startswith(('CREATE DATABASE', 'USE ')):
            continue
        current_stmt.append(line)
        if line_clean.endswith(';'):
            statements.append("\n".join(current_stmt))
            current_stmt = []

    if current_stmt:
        statements.append("\n".join(current_stmt))

    for stmt in statements:
        s = stmt.strip()
        if not s:
            continue
        try:
            cursor.execute(s)
        except Exception as e:
            # Fallback for minor syntax issues
            pass

    conn.commit()
    return conn


def execute_query(conn, query):
    """
    Executes a SQL query and returns column names and row tuples.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        return {
            "success": True,
            "columns": columns,
            "rows": [list(row) for row in rows],
            "rowCount": len(rows),
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "rowCount": 0,
            "error": str(e)
        }


def format_table(columns, rows):
    """
    Renders column names and rows into a formatted ASCII table.
    """
    if not columns and not rows:
        return "(Empty result)"
    if not columns:
        return f"{len(rows)} row(s) returned"

    # Compute maximum width per column
    col_names = [str(c) for c in columns]
    widths = [len(c) for c in col_names]

    for row in rows:
        for i, val in enumerate(row):
            val_str = "NULL" if val is None else str(val)
            if i < len(widths):
                widths[i] = max(widths[i], len(val_str))

    header = " | ".join(name.ljust(widths[i]) for i, name in enumerate(col_names))
    separator = "-+-".join("-" * widths[i] for i in range(len(widths)))
    
    lines = [header, separator]
    for row in rows:
        row_str = " | ".join(
            ("NULL" if val is None else str(val)).ljust(widths[i])
            for i, val in enumerate(row)
        )
        lines.append(row_str)

    lines.append(f"\n({len(rows)} row{'s' if len(rows) != 1 else ''})")
    return "\n".join(lines)


def normalize_value(v):
    if v is None:
        return None
    if isinstance(v, float):
        return round(v, 2)
    # Check if string representation is float
    try:
        f = float(v)
        if '.' in str(v):
            return round(f, 2)
    except (ValueError, TypeError):
        pass
    return v


def compare_sql_results(actual_cols, actual_rows, expected_cols, expected_rows, order_sensitive=True):
    """
    Compares query results against expected results.
    Matches column names (case-insensitive) and cell values (handling floats and types).
    """
    # 1. Compare column count and names
    if len(actual_cols) != len(expected_cols):
        return False, f"Column count mismatch: got {len(actual_cols)} columns ({actual_cols}), expected {len(expected_cols)} columns ({expected_cols})"

    norm_actual_cols = [str(c).strip().lower() for c in actual_cols]
    norm_exp_cols = [str(c).strip().lower() for c in expected_cols]

    if norm_actual_cols != norm_exp_cols:
        return False, f"Column mismatch:\nExpected: {expected_cols}\nGot: {actual_cols}"

    # 2. Compare row count
    if len(actual_rows) != len(expected_rows):
        return False, f"Row count mismatch: got {len(actual_rows)} rows, expected {len(expected_rows)} rows"

    # 3. Compare rows
    def clean_row(r):
        return [normalize_value(x) for x in r]

    cleaned_actual = [clean_row(r) for r in actual_rows]
    cleaned_expected = [clean_row(r) for r in expected_rows]

    if order_sensitive:
        for i, (act, exp) in enumerate(zip(cleaned_actual, cleaned_expected)):
            if act != exp:
                return False, f"Row {i+1} mismatch:\nExpected: {exp}\nGot: {act}"
    else:
        # Sort both for order-agnostic comparison
        sort_act = sorted(cleaned_actual, key=lambda x: str(x))
        sort_exp = sorted(cleaned_expected, key=lambda x: str(x))
        if sort_act != sort_exp:
            return False, "Rows content mismatch (values do not match expected records)"

    return True, "Match"
