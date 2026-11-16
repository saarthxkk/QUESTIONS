"""
compiler_util.py — Intelligent C++ Code Merger and Validator for CodeArena
Handles:
- Complete programs (with main())
- Function-only submissions (with signature)
- Function body-only submissions (without signature)
- LeetCode-style class Solution submissions
- Mismatched braces detection
- Missing return statement validation
- Header and namespace preservation
- Duplicate function prevention
"""

import re

REQUIRED_HEADERS = [
    '<iostream>',
    '<vector>',
    '<string>',
    '<algorithm>',
    '<cmath>',
    '<climits>',
    '<queue>',
    '<stack>',
    '<map>',
    '<set>',
    '<utility>'
]


def clean_comments_strings(code: str) -> str:
    """
    Replaces comments and string literals with spaces.
    Preserves exact character offsets and line breaks.
    """
    res = []
    i = 0
    n = len(code)
    in_str = False
    str_ch = None
    in_lc = False
    in_bc = False

    while i < n:
        if in_lc:
            if code[i] == '\n':
                in_lc = False
                res.append('\n')
            else:
                res.append(' ')
            i += 1
        elif in_bc:
            if i + 1 < n and code[i] == '*' and code[i + 1] == '/':
                in_bc = False
                res.append('  ')
                i += 2
            else:
                res.append(' ')
                i += 1
        elif in_str:
            if code[i] == '\\':
                res.append('  ')
                i += 2
            elif code[i] == str_ch:
                in_str = False
                res.append(' ')
                i += 1
            else:
                res.append(' ')
                i += 1
        else:
            if i + 1 < n and code[i] == '/' and code[i + 1] == '/':
                in_lc = True
                res.append('  ')
                i += 2
            elif i + 1 < n and code[i] == '/' and code[i + 1] == '*':
                in_bc = True
                res.append('  ')
                i += 2
            elif code[i] in ('"', "'"):
                in_str = True
                str_ch = code[i]
                res.append(' ')
                i += 1
            else:
                res.append(code[i])
                i += 1

    return ''.join(res)


def check_braces(code: str):
    """
    Verifies that curly braces { and } are balanced, ignoring braces in comments/strings.
    """
    clean = clean_comments_strings(code)
    open_b = clean.count('{')
    close_b = clean.count('}')
    if open_b != close_b:
        return False, f"Mismatched braces: found {open_b} opening '{{' and {close_b} closing '}}'. Please check your brackets."
    return True, ""


def find_functions(code: str):
    """
    Finds top-level and member function definitions in C++ code.
    Returns list of dicts with function metadata and offsets.
    """
    clean = clean_comments_strings(code)
    pattern = re.compile(
        r'([a-zA-Z_][a-zA-Z0-9_*&<>\s:]*?)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{',
        re.MULTILINE
    )
    functions = []
    control_flow = {'if', 'while', 'for', 'switch', 'catch', 'do'}

    for m in pattern.finditer(clean):
        ret_type = m.group(1).strip()
        name = m.group(2).strip()

        if name in control_flow:
            continue

        args = m.group(3).strip()
        brace_start = m.end() - 1
        count = 1
        i = brace_start + 1
        n = len(clean)

        while i < n and count > 0:
            if clean[i] == '{':
                count += 1
            elif clean[i] == '}':
                count -= 1
            i += 1

        if count == 0:
            functions.append({
                'name': name,
                'ret_type': ret_type,
                'args': args,
                'start': m.start(),
                'end': i,
                'full': code[m.start():i],
                'body': code[brace_start + 1:i - 1]
            })

    return functions


def has_main_function(code: str) -> bool:
    """Checks whether the code contains an int main(...) entry point."""
    clean = clean_comments_strings(code)
    return bool(re.search(r'\bint\s+main\s*\(|\bvoid\s+main\s*\(|\bmain\s*\(', clean))


def unwrap_solution_class(code: str) -> str:
    """If code is wrapped in class Solution { public: ... }; unwrap it."""
    match = re.search(r'class\s+Solution\s*\{(?:\s*public\s*:)?([\s\S]*?)\}\s*;', code)
    if match:
        return match.group(1).strip()
    return code


def ensure_headers(code: str) -> str:
    """Ensures standard C++ library headers and using namespace std are present."""
    missing = []
    for h in REQUIRED_HEADERS:
        if h not in code:
            missing.append(f"#include {h}")

    header_block = ""
    if missing:
        header_block += "\n".join(missing) + "\n"

    if "using namespace std;" not in code:
        header_block += "using namespace std;\n"

    return header_block + "\n" + code if header_block else code


def prepare_submission_code(user_code: str, boilerplate: str):
    """
    Validates and merges user submission with boilerplate code when needed.

    Returns:
        (success: bool, final_code: str, error_message: str or None)
    """
    user_code = user_code.strip()
    if not user_code:
        return False, "", "Submitted code is empty."

    # Step 1: Validate brace balance on user code
    ok, err = check_braces(user_code)
    if not ok:
        return False, "", err

    # Step 2: Unwrap LeetCode-style class Solution if present
    processed_user_code = unwrap_solution_class(user_code)

    # Step 3: Check if this is already a complete program
    if has_main_function(processed_user_code):
        final_code = ensure_headers(processed_user_code)
        return True, final_code, None

    # Step 4: Function-only submission — Requires boilerplate
    if not boilerplate or not boilerplate.strip():
        return False, "", "Platform could not find the problem's boilerplate, and no main() function was provided."

    bp_fns = find_functions(boilerplate)
    user_fns = find_functions(processed_user_code)

    # Locate the target function in the boilerplate
    target_bp_fn = None
    user_fn_names = {f['name'] for f in user_fns}

    # Strategy A: User defined a function that exists in boilerplate (e.g. insert, insertAndFindDepth)
    for f in bp_fns:
        if f['name'] != 'main' and f['name'] in user_fn_names:
            target_bp_fn = f
            break

    # Strategy B: Look for function with TODO or 'Your code here'
    if not target_bp_fn:
        for f in bp_fns:
            if f['name'] != 'main' and ('Your code here' in f['body'] or not f['body'].strip()):
                target_bp_fn = f
                break

    # Strategy C: First non-main function in boilerplate
    if not target_bp_fn:
        non_main = [f for f in bp_fns if f['name'] != 'main']
        if non_main:
            target_bp_fn = non_main[0]

    if not target_bp_fn:
        return False, "", "Could not locate target function stub in boilerplate."

    # Validate non-void return statement
    clean_user = clean_comments_strings(processed_user_code)
    if target_bp_fn['ret_type'] not in ('void', '') and 'return' not in clean_user:
        return False, "", (
            f"Function '{target_bp_fn['name']}' has return type '{target_bp_fn['ret_type']}', "
            f"but no 'return' statement was found in your submission."
        )

    # Perform the merge
    if user_fns:
        # User supplied function(s) with full signature
        # Remove any functions from boilerplate that the user also redefined to prevent duplicate definitions
        cleaned_bp = boilerplate
        for uf in user_fns:
            for bf in bp_fns:
                if bf['name'] == uf['name'] and bf['name'] != target_bp_fn['name']:
                    # Clear out duplicate definition in boilerplate
                    cleaned_bp = (
                        cleaned_bp[:bf['start']]
                        + (' ' * (bf['end'] - bf['start']))
                        + cleaned_bp[bf['end']:]
                    )

        # Replace target function stub with user's full code (including any helper functions)
        merged = (
            cleaned_bp[:target_bp_fn['start']]
            + "\n" + processed_user_code + "\n"
            + cleaned_bp[target_bp_fn['end']:]
        )
    else:
        # User provided only the function body
        body_start = target_bp_fn['full'].find('{') + 1
        fn_header = target_bp_fn['full'][:body_start]
        fn_replaced = f"{fn_header}\n    {processed_user_code}\n}}"
        merged = (
            boilerplate[:target_bp_fn['start']]
            + "\n" + fn_replaced + "\n"
            + boilerplate[target_bp_fn['end']:]
        )

    # Step 5: Final brace balance check on merged source
    ok, err = check_braces(merged)
    if not ok:
        return False, "", f"Error after merging boilerplate: {err}"

    final_code = ensure_headers(merged)
    return True, final_code, None

