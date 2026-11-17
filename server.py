from flask import Flask, send_from_directory, request, jsonify
import subprocess
import os
import json
import uuid
import tempfile
import shutil
import urllib.request
from compiler_util import prepare_submission_code

app = Flask(__name__, static_folder='public', static_url_path='')

QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'questions.json')
TEMP_DIR = os.path.join(os.path.dirname(__file__), 'temp')

os.makedirs(TEMP_DIR, exist_ok=True)

HAS_LOCAL_GCC = shutil.which('g++') is not None
if HAS_LOCAL_GCC:
    print("⚡ C++ Engine: Using local g++ compiler (-std=c++17)")
else:
    print("☁️ C++ Engine: g++ not found locally — using Cloud C++17 Compiler Engine (Vercel-ready)")


def load_questions():
    with open(QUESTIONS_FILE, 'r') as f:
        return json.load(f)

def save_questions(questions):
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f, indent=2)

# ─── Pages ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/problem')
def problem_page():
    return send_from_directory('public', 'problem.html')

# ─── API: Questions ──────────────────────────────────────────────────────────

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = load_questions()
    # Return summary (no test cases or boilerplate)
    summary = []
    for q in questions:
        summary.append({
            'id': q['id'],
            'title': q['title'],
            'difficulty': q['difficulty'],
            'points': q['points'],
            'category': q['category'],
            'tags': q['tags']
        })
    return jsonify(summary)

@app.route('/api/questions/<int:qid>', methods=['GET'])
def get_question(qid):
    questions = load_questions()
    for q in questions:
        if q['id'] == qid:
            # Return full question with sample test cases only
            result = dict(q)
            result['testCases'] = [tc for tc in q['testCases'] if tc.get('isSample', False)]
            result['totalTestCases'] = len(q['testCases'])
            return jsonify(result)
    return jsonify({'error': 'Question not found'}), 404

@app.route('/api/questions', methods=['POST'])
def add_question():
    questions = load_questions()
    data = request.json
    # Auto-assign ID
    max_id = max((q['id'] for q in questions), default=0)
    data['id'] = max_id + 1
    # Auto-assign points
    diff = data.get('difficulty', 'Easy')
    points_map = {'Easy': 25, 'Medium': 50, 'Hard': 100}
    data['points'] = points_map.get(diff, 25)
    questions.append(data)
    save_questions(questions)
    return jsonify({'message': 'Question added', 'id': data['id']}), 201

# ─── API: Compile & Run ─────────────────────────────────────────────────────

@app.route('/api/run', methods=['POST'])
def run_code():
    """Run code against a single custom input with automatic boilerplate merging."""
    data = request.json or {}
    code = data.get('code', '')
    stdin_input = data.get('input', '')
    qid = data.get('questionId')

    boilerplate = ''
    if qid:
        questions = load_questions()
        for q in questions:
            if q['id'] == qid:
                boilerplate = q.get('boilerplate', '')
                break

    # Validate and merge code with boilerplate if function-only
    ok, final_code, merge_err = prepare_submission_code(code, boilerplate)
    if not ok:
        return jsonify({
            'success': False,
            'compilationError': f"Pre-validation / Merge Error:\n{merge_err}",
            'output': ''
        })

    result = compile_and_run(final_code, stdin_input)
    return jsonify(result)

@app.route('/api/submit', methods=['POST'])
def submit_code():
    """Run code against all test cases for a question with automatic boilerplate merging."""
    data = request.json or {}
    code = data.get('code', '')
    qid = data.get('questionId')

    questions = load_questions()
    question = None
    for q in questions:
        if q['id'] == qid:
            question = q
            break

    if not question:
        return jsonify({'error': 'Question not found'}), 404

    boilerplate = question.get('boilerplate', '')
    # Validate and merge code with boilerplate if function-only
    ok, final_code, merge_err = prepare_submission_code(code, boilerplate)
    if not ok:
        return jsonify({
            'status': 'Compilation Error',
            'passed': 0,
            'total': len(question.get('testCases', [])),
            'points': 0,
            'results': [{
                'testCaseId': 1,
                'description': 'Code Pre-validation / Merge',
                'passed': False,
                'isSample': True,
                'compilationError': f"Pre-validation / Merge Error:\n{merge_err}"
            }]
        })

    test_cases = question['testCases']
    results = []
    passed = 0
    total = len(test_cases)

    for tc in test_cases:
        result = compile_and_run(final_code, tc['input'])
        actual_output = result.get('output', '').strip()
        expected_output = tc['expectedOutput'].strip()
        is_passed = actual_output == expected_output

        if is_passed:
            passed += 1

        results.append({
            'testCaseId': tc['id'],
            'description': tc.get('description', ''),
            'isSample': tc.get('isSample', False),
            'passed': is_passed,
            'input': tc['input'] if tc.get('isSample', False) else None,
            'expectedOutput': tc['expectedOutput'] if tc.get('isSample', False) or not is_passed else None,
            'actualOutput': actual_output if tc.get('isSample', False) or not is_passed else None,
            'error': result.get('error', ''),
            'compilationError': result.get('compilationError', ''),
            'timeout': result.get('timeout', False)
        })

        # Stop on compilation error
        if result.get('compilationError'):
            break

    status = 'Accepted' if passed == total else 'Wrong Answer'
    if results and results[-1].get('compilationError'):
        status = 'Compilation Error'
    if any(r.get('timeout') for r in results):
        status = 'Time Limit Exceeded'

    return jsonify({
        'status': status,
        'passed': passed,
        'total': total,
        'points': question['points'] if passed == total else 0,
        'results': results
    })


def compile_cloud(code, stdin_input='', timeout=15):
    """Compile and run C++ code via Cloud Compiler API (used when running on Vercel/serverless)."""
    try:
        payload = {
            'compiler': 'gcc-13.2.0',
            'code': code,
            'options': 'c++17',
            'stdin': stdin_input or ''
        }
        req = urllib.request.Request(
            'https://wandbox.org/api/compile.json',
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'CodeArena-Platform/1.0 (Mozilla/5.0)'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as res:
            data = json.loads(res.read().decode('utf-8'))
            comp_err = data.get('compiler_error', '') or data.get('compiler_message', '')
            status = str(data.get('status', '0'))

            if status != '0' and not data.get('program_output'):
                return {
                    'success': False,
                    'compilationError': comp_err or 'Compilation Error',
                    'output': ''
                }

            return {
                'success': True,
                'output': data.get('program_output', ''),
                'error': data.get('program_error', '')
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'Cloud compiler error: {str(e)}',
            'output': ''
        }


def compile_and_run(code, stdin_input, timeout=5):
    """Compile C++ code and run it with the given input (local g++ if available, else Cloud)."""
    if not HAS_LOCAL_GCC:
        return compile_cloud(code, stdin_input, timeout=12)

    run_id = str(uuid.uuid4())[:8]
    work_dir = os.path.join(TEMP_DIR, run_id)
    os.makedirs(work_dir, exist_ok=True)

    src_file = os.path.join(work_dir, 'solution.cpp')
    bin_file = os.path.join(work_dir, 'solution')

    try:
        # Write source
        with open(src_file, 'w') as f:
            f.write(code)

        # Compile
        compile_proc = subprocess.run(
            ['g++', '-std=c++17', '-O2', '-o', bin_file, src_file],
            capture_output=True, text=True, timeout=15
        )

        if compile_proc.returncode != 0:
            return {
                'success': False,
                'compilationError': compile_proc.stderr,
                'output': ''
            }

        # Run
        run_proc = subprocess.run(
            [bin_file],
            input=stdin_input,
            capture_output=True, text=True, timeout=timeout
        )

        if run_proc.returncode != 0:
            return {
                'success': False,
                'error': run_proc.stderr or f'Runtime error (exit code {run_proc.returncode})',
                'output': run_proc.stdout
            }

        return {
            'success': True,
            'output': run_proc.stdout,
            'error': run_proc.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'timeout': True,
            'error': 'Time Limit Exceeded (5 seconds)',
            'output': ''
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'output': ''
        }
    finally:
        # Cleanup
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == '__main__':
    print("\n🚀 CodeArena is running at http://localhost:8080\n")
    app.run(debug=False, port=8080)
