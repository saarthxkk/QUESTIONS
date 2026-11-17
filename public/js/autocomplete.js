// ═══════════════════════════════════════════════════════════════
// CodeArena — Auto-Fill & IntelliSense Engine
// VS Code & LeetCode Style Autocomplete for C++17 and MySQL
// ═══════════════════════════════════════════════════════════════

const CPP_DICTIONARY = [
  // ── Keywords ──
  { text: 'auto', kind: 'keyword', icon: '🔑', detail: 'auto type deduction' },
  { text: 'bool', kind: 'keyword', icon: '🔑', detail: 'boolean type' },
  { text: 'break', kind: 'keyword', icon: '🔑', detail: 'break loop / switch' },
  { text: 'case', kind: 'keyword', icon: '🔑', detail: 'switch case label' },
  { text: 'catch', kind: 'keyword', icon: '🔑', detail: 'exception catch block' },
  { text: 'char', kind: 'keyword', icon: '🔑', detail: 'character type' },
  { text: 'class', kind: 'keyword', icon: '🔑', detail: 'class declaration' },
  { text: 'const', kind: 'keyword', icon: '🔑', detail: 'const qualifier' },
  { text: 'constexpr', kind: 'keyword', icon: '🔑', detail: 'compile-time constant' },
  { text: 'continue', kind: 'keyword', icon: '🔑', detail: 'continue next iteration' },
  { text: 'default', kind: 'keyword', icon: '🔑', detail: 'default switch case' },
  { text: 'delete', kind: 'keyword', icon: '🔑', detail: 'deallocate memory' },
  { text: 'do', kind: 'keyword', icon: '🔑', detail: 'do-while loop' },
  { text: 'double', kind: 'keyword', icon: '🔑', detail: 'double precision float' },
  { text: 'else', kind: 'keyword', icon: '🔑', detail: 'else branch' },
  { text: 'enum', kind: 'keyword', icon: '🔑', detail: 'enumerated type' },
  { text: 'false', kind: 'keyword', icon: '🔑', detail: 'boolean literal' },
  { text: 'float', kind: 'keyword', icon: '🔑', detail: 'single precision float' },
  { text: 'for', kind: 'keyword', icon: '🔑', detail: 'for loop' },
  { text: 'if', kind: 'keyword', icon: '🔑', detail: 'if condition' },
  { text: 'inline', kind: 'keyword', icon: '🔑', detail: 'inline function' },
  { text: 'int', kind: 'keyword', icon: '🔑', detail: 'integer type' },
  { text: 'long', kind: 'keyword', icon: '🔑', detail: 'long integer' },
  { text: 'namespace', kind: 'keyword', icon: '🔑', detail: 'namespace declaration' },
  { text: 'new', kind: 'keyword', icon: '🔑', detail: 'allocate memory' },
  { text: 'nullptr', kind: 'keyword', icon: '🔑', detail: 'null pointer literal' },
  { text: 'public', kind: 'keyword', icon: '🔑', detail: 'public access specifier' },
  { text: 'private', kind: 'keyword', icon: '🔑', detail: 'private access specifier' },
  { text: 'protected', kind: 'keyword', icon: '🔑', detail: 'protected access specifier' },
  { text: 'return', kind: 'keyword', icon: '🔑', detail: 'return from function' },
  { text: 'sizeof', kind: 'keyword', icon: '🔑', detail: 'size in bytes' },
  { text: 'static', kind: 'keyword', icon: '🔑', detail: 'static storage duration' },
  { text: 'struct', kind: 'keyword', icon: '🔑', detail: 'struct declaration' },
  { text: 'switch', kind: 'keyword', icon: '🔑', detail: 'switch statement' },
  { text: 'template', kind: 'keyword', icon: '🔑', detail: 'template declaration' },
  { text: 'this', kind: 'keyword', icon: '🔑', detail: 'pointer to current object' },
  { text: 'true', kind: 'keyword', icon: '🔑', detail: 'boolean literal' },
  { text: 'typedef', kind: 'keyword', icon: '🔑', detail: 'type alias' },
  { text: 'using', kind: 'keyword', icon: '🔑', detail: 'using namespace / alias' },
  { text: 'void', kind: 'keyword', icon: '🔑', detail: 'empty / no return type' },
  { text: 'while', kind: 'keyword', icon: '🔑', detail: 'while loop' },

  // ── Common I/O & Objects ──
  { text: 'cout', kind: 'object', icon: '📤', detail: 'std::cout << ...' },
  { text: 'cin', kind: 'object', icon: '📥', detail: 'std::cin >> ...' },
  { text: 'cerr', kind: 'object', icon: '📤', detail: 'std::cerr << ...' },
  { text: 'endl', kind: 'object', icon: '↩️', detail: 'std::endl' },
  { text: 'getline', kind: 'function', icon: '⚡', detail: 'getline(cin, str)' },
  { text: 'printf', kind: 'function', icon: '⚡', detail: 'printf(format, ...)' },
  { text: 'scanf', kind: 'function', icon: '⚡', detail: 'scanf(format, ...)' },

  // ── STL Containers ──
  { text: 'vector', kind: 'class', icon: '📦', detail: 'std::vector<T>' },
  { text: 'string', kind: 'class', icon: '📦', detail: 'std::string' },
  { text: 'map', kind: 'class', icon: '📦', detail: 'std::map<K,V>' },
  { text: 'unordered_map', kind: 'class', icon: '📦', detail: 'std::unordered_map<K,V>' },
  { text: 'set', kind: 'class', icon: '📦', detail: 'std::set<T>' },
  { text: 'unordered_set', kind: 'class', icon: '📦', detail: 'std::unordered_set<T>' },
  { text: 'queue', kind: 'class', icon: '📦', detail: 'std::queue<T>' },
  { text: 'priority_queue', kind: 'class', icon: '📦', detail: 'std::priority_queue<T>' },
  { text: 'stack', kind: 'class', icon: '📦', detail: 'std::stack<T>' },
  { text: 'pair', kind: 'class', icon: '📦', detail: 'std::pair<A,B>' },

  // ── STL Algorithms & Math ──
  { text: 'sort', kind: 'function', icon: '⚡', detail: 'sort(v.begin(), v.end())' },
  { text: 'reverse', kind: 'function', icon: '⚡', detail: 'reverse(v.begin(), v.end())' },
  { text: 'max', kind: 'function', icon: '⚡', detail: 'max(a, b)' },
  { text: 'min', kind: 'function', icon: '⚡', detail: 'min(a, b)' },
  { text: 'swap', kind: 'function', icon: '⚡', detail: 'swap(a, b)' },
  { text: 'abs', kind: 'function', icon: '⚡', detail: 'abs(n)' },
  { text: 'lower_bound', kind: 'function', icon: '⚡', detail: 'lower_bound(beg, end, val)' },
  { text: 'upper_bound', kind: 'function', icon: '⚡', detail: 'upper_bound(beg, end, val)' },

  // ── Common Data Structure Elements ──
  { text: 'Node', kind: 'class', icon: '🌳', detail: 'struct Node' },
  { text: 'TreeNode', kind: 'class', icon: '🌳', detail: 'struct TreeNode' },
  { text: 'ListNode', kind: 'class', icon: '🔗', detail: 'struct ListNode' },
  { text: 'left', kind: 'field', icon: '🏷️', detail: 'Node* left' },
  { text: 'right', kind: 'field', icon: '🏷️', detail: 'Node* right' },
  { text: 'data', kind: 'field', icon: '🏷️', detail: 'int data / val' },
  { text: 'val', kind: 'field', icon: '🏷️', detail: 'int val' },
  { text: 'height', kind: 'field', icon: '🏷️', detail: 'int height' },
  { text: 'push_back', kind: 'function', icon: '⚡', detail: 'v.push_back(x)' },
  { text: 'size', kind: 'function', icon: '⚡', detail: 'c.size()' },
  { text: 'empty', kind: 'function', icon: '⚡', detail: 'c.empty()' },
  { text: 'begin', kind: 'function', icon: '⚡', detail: 'c.begin()' },
  { text: 'end', kind: 'function', icon: '⚡', detail: 'c.end()' },

  // ── C++ Snippets ──
  {
    text: 'fori',
    kind: 'snippet',
    icon: '✂️',
    detail: 'for (int i = 0; i < n; i++)',
    isSnippet: true,
    body: 'for (int i = 0; i < n; i++) {\n    \n}'
  },
  {
    text: 'fore',
    kind: 'snippet',
    icon: '✂️',
    detail: 'for (auto& x : container)',
    isSnippet: true,
    body: 'for (auto& x : v) {\n    \n}'
  },
  {
    text: 'node',
    kind: 'snippet',
    icon: '✂️',
    detail: 'struct Node declaration',
    isSnippet: true,
    body: 'struct Node {\n    int data;\n    Node* left;\n    Node* right;\n    Node(int val) : data(val), left(nullptr), right(nullptr) {}\n};'
  },
  {
    text: 'coutl',
    kind: 'snippet',
    icon: '✂️',
    detail: 'cout << ... << endl;',
    isSnippet: true,
    body: 'cout <<  << endl;'
  }
];

const SQL_DICTIONARY = [
  // ── SQL Core Keywords ──
  { text: 'SELECT', kind: 'keyword', icon: '🔑', detail: 'SELECT col1, col2' },
  { text: 'FROM', kind: 'keyword', icon: '🔑', detail: 'FROM table_name' },
  { text: 'WHERE', kind: 'keyword', icon: '🔑', detail: 'WHERE condition' },
  { text: 'GROUP BY', kind: 'keyword', icon: '🔑', detail: 'GROUP BY col1, col2' },
  { text: 'HAVING', kind: 'keyword', icon: '🔑', detail: 'HAVING condition' },
  { text: 'ORDER BY', kind: 'keyword', icon: '🔑', detail: 'ORDER BY col ASC|DESC' },
  { text: 'LIMIT', kind: 'keyword', icon: '🔑', detail: 'LIMIT count' },
  { text: 'AND', kind: 'keyword', icon: '🔑', detail: 'Logical AND' },
  { text: 'OR', kind: 'keyword', icon: '🔑', detail: 'Logical OR' },
  { text: 'NOT', kind: 'keyword', icon: '🔑', detail: 'Logical NOT' },
  { text: 'BETWEEN', kind: 'keyword', icon: '🔑', detail: 'BETWEEN low AND high' },
  { text: 'IN', kind: 'keyword', icon: '🔑', detail: 'col IN (val1, val2)' },
  { text: 'NOT IN', kind: 'keyword', icon: '🔑', detail: 'col NOT IN (val1, val2)' },
  { text: 'LIKE', kind: 'keyword', icon: '🔑', detail: "LIKE 'pattern%'" },
  { text: 'DISTINCT', kind: 'keyword', icon: '🔑', detail: 'COUNT(DISTINCT col)' },
  { text: 'AS', kind: 'keyword', icon: '🔑', detail: 'expression AS alias' },
  { text: 'ASC', kind: 'keyword', icon: '🔑', detail: 'Ascending sort' },
  { text: 'DESC', kind: 'keyword', icon: '🔑', detail: 'Descending sort' },
  { text: 'IS NULL', kind: 'keyword', icon: '🔑', detail: 'Check for NULL' },
  { text: 'IS NOT NULL', kind: 'keyword', icon: '🔑', detail: 'Check for NOT NULL' },
  { text: 'JOIN', kind: 'keyword', icon: '🔑', detail: 'JOIN table ON ...' },
  { text: 'INNER JOIN', kind: 'keyword', icon: '🔑', detail: 'INNER JOIN table ON ...' },
  { text: 'LEFT JOIN', kind: 'keyword', icon: '🔑', detail: 'LEFT JOIN table ON ...' },
  { text: 'RIGHT JOIN', kind: 'keyword', icon: '🔑', detail: 'RIGHT JOIN table ON ...' },
  { text: 'COALESCE', kind: 'function', icon: '⚡', detail: 'COALESCE(val, fallback)' },
  { text: 'CASE', kind: 'keyword', icon: '🔑', detail: 'CASE WHEN .. THEN .. END' },

  // ── Aggregate & Date Functions ──
  { text: 'COUNT(*)', kind: 'function', icon: '⚡', detail: 'COUNT(*) — all rows' },
  { text: 'COUNT', kind: 'function', icon: '⚡', detail: 'COUNT(column)' },
  { text: 'SUM', kind: 'function', icon: '⚡', detail: 'SUM(column)' },
  { text: 'AVG', kind: 'function', icon: '⚡', detail: 'AVG(column)' },
  { text: 'MAX', kind: 'function', icon: '⚡', detail: 'MAX(column)' },
  { text: 'MIN', kind: 'function', icon: '⚡', detail: 'MIN(column)' },
  { text: 'ROUND', kind: 'function', icon: '⚡', detail: 'ROUND(value, 2)' },
  { text: 'YEAR', kind: 'function', icon: '⚡', detail: 'YEAR(dob)' },
  { text: 'MONTH', kind: 'function', icon: '⚡', detail: 'MONTH(dob)' },
  { text: 'MONTHNAME', kind: 'function', icon: '⚡', detail: 'MONTHNAME(dob)' },

  // ── Database Schema Table & Columns ──
  { text: 'student', kind: 'class', icon: '🗄️', detail: 'Table: student' },
  { text: 'student_id', kind: 'field', icon: '🏷️', detail: 'student.student_id' },
  { text: 'department', kind: 'class', icon: '🗄️', detail: 'Table: department' },
  { text: 'employee', kind: 'class', icon: '🗄️', detail: 'Table: employee' },
  { text: 'dept_id', kind: 'field', icon: '🏷️', detail: 'department.dept_id' },
  { text: 'dept_name', kind: 'field', icon: '🏷️', detail: 'department.dept_name' },
  { text: 'location', kind: 'field', icon: '🏷️', detail: 'department.location' },
  { text: 'emp_id', kind: 'field', icon: '🏷️', detail: 'employee.emp_id' },
  { text: 'emp_name', kind: 'field', icon: '🏷️', detail: 'employee.emp_name' },
  { text: 'name', kind: 'field', icon: '🏷️', detail: 'name' },
  { text: 'age', kind: 'field', icon: '🏷️', detail: 'age' },
  { text: 'gender', kind: 'field', icon: '🏷️', detail: "gender ('M'/'F')" },
  { text: 'city', kind: 'field', icon: '🏷️', detail: 'city' },
  { text: 'email', kind: 'field', icon: '🏷️', detail: 'email' },
  { text: 'marks', kind: 'field', icon: '🏷️', detail: 'marks' },
  { text: 'dob', kind: 'field', icon: '🏷️', detail: 'dob' },
  { text: 'salary', kind: 'field', icon: '🏷️', detail: 'employee.salary' },
  { text: 'performance', kind: 'field', icon: '🏷️', detail: 'employee.performance' },
  { text: 'joining_date', kind: 'field', icon: '🏷️', detail: 'employee.joining_date' },

  // ── Common Problem Aliases ──
  { text: 'employee_name', kind: 'field', icon: '🏷️', detail: 'emp_name AS employee_name' },
  { text: 'employee_salary', kind: 'field', icon: '🏷️', detail: 'salary AS employee_salary' },
  { text: 'department_location', kind: 'field', icon: '🏷️', detail: 'd.location AS department_location' },
  { text: 'staffing_status', kind: 'field', icon: '🏷️', detail: 'staffing_status' },
  { text: 'departments_represented', kind: 'field', icon: '🏷️', detail: 'COUNT(DISTINCT d.dept_id) AS departments_represented' },
  { text: 'excellent_count', kind: 'field', icon: '🏷️', detail: 'excellent_count' },
  { text: 'good_count', kind: 'field', icon: '🏷️', detail: 'good_count' },
  { text: 'average_count', kind: 'field', icon: '🏷️', detail: 'average_count' },
  { text: 'poor_count', kind: 'field', icon: '🏷️', detail: 'poor_count' },
  { text: 'high_salary_count', kind: 'field', icon: '🏷️', detail: 'high_salary_count' },
  { text: 'low_salary_count', kind: 'field', icon: '🏷️', detail: 'low_salary_count' },
  { text: 'performance_score', kind: 'field', icon: '🏷️', detail: 'performance AS performance_score' },
  { text: 'salary_difference', kind: 'field', icon: '🏷️', detail: 'salary_difference' },
  { text: 'female_total_salary', kind: 'field', icon: '🏷️', detail: 'female_total_salary' },
  { text: 'high_performer_avg_salary', kind: 'field', icon: '🏷️', detail: 'high_performer_avg_salary' },
  { text: 'average_performance', kind: 'field', icon: '🏷️', detail: 'average_performance' },
  { text: 'highest_performance', kind: 'field', icon: '🏷️', detail: 'highest_performance' },
  { text: 'total_departments', kind: 'field', icon: '🏷️', detail: 'total_departments' },
  { text: 'performance_category', kind: 'field', icon: '🏷️', detail: 'performance_category' },
  { text: 'salary_category', kind: 'field', icon: '🏷️', detail: 'salary_category' },
  { text: 'age_category', kind: 'field', icon: '🏷️', detail: 'age_category' },
  { text: 'joining_year', kind: 'field', icon: '🏷️', detail: 'joining_year' },
  { text: 'joining_month', kind: 'field', icon: '🏷️', detail: 'joining_month' },
  { text: 'high_performers', kind: 'field', icon: '🏷️', detail: 'high_performers' },
  { text: 'low_performers', kind: 'field', icon: '🏷️', detail: 'low_performers' },
  { text: 'female_employees', kind: 'field', icon: '🏷️', detail: 'female_employees' },
  { text: 'high_performer_percentage', kind: 'field', icon: '🏷️', detail: 'high_performer_percentage' },
  { text: 'female_percentage', kind: 'field', icon: '🏷️', detail: 'female_percentage' },
  { text: 'high_salary_employees', kind: 'field', icon: '🏷️', detail: 'high_salary_employees' },
  { text: 'low_salary_employees', kind: 'field', icon: '🏷️', detail: 'low_salary_employees' },
  { text: 'earliest_joining_date', kind: 'field', icon: '🏷️', detail: 'earliest_joining_date' },
  { text: 'latest_joining_date', kind: 'field', icon: '🏷️', detail: 'latest_joining_date' },
  { text: 'department_category', kind: 'field', icon: '🏷️', detail: 'department_category' },
  { text: 'student_name', kind: 'field', icon: '🏷️', detail: 'name AS student_name' },
  { text: 'student_marks', kind: 'field', icon: '🏷️', detail: 'marks AS student_marks' },
  { text: 'total_students', kind: 'field', icon: '🏷️', detail: 'COUNT(*) AS total_students' },
  { text: 'total_salary', kind: 'field', icon: '🏷️', detail: 'SUM(salary) AS total_salary' },
  { text: 'average_salary', kind: 'field', icon: '🏷️', detail: 'ROUND(AVG(salary), 2) AS average_salary' },
  { text: 'highest_salary', kind: 'field', icon: '🏷️', detail: 'MAX(salary) AS highest_salary' },
  { text: 'lowest_salary', kind: 'field', icon: '🏷️', detail: 'MIN(salary) AS lowest_salary' },
  { text: 'birth_year', kind: 'field', icon: '🏷️', detail: 'YEAR(dob) AS birth_year' },
  { text: 'birth_month_number', kind: 'field', icon: '🏷️', detail: 'MONTH(dob) AS birth_month_number' },
  { text: 'birth_month_name', kind: 'field', icon: '🏷️', detail: 'MONTHNAME(dob) AS birth_month_name' },
  { text: 'average_age', kind: 'field', icon: '🏷️', detail: 'ROUND(AVG(age), 2) AS average_age' },
  { text: 'unique_cities', kind: 'field', icon: '🏷️', detail: 'COUNT(DISTINCT city) AS unique_cities' },
  { text: 'unique_ages', kind: 'field', icon: '🏷️', detail: 'COUNT(DISTINCT age) AS unique_ages' },
  { text: 'unique_marks', kind: 'field', icon: '🏷️', detail: 'COUNT(DISTINCT marks) AS unique_marks' },

  // ── SQL Snippets ──
  {
    text: 'sel',
    kind: 'snippet',
    icon: '✂️',
    detail: 'SELECT * FROM student;',
    isSnippet: true,
    body: 'SELECT * FROM student;'
  },
  {
    text: 'selgroup',
    kind: 'snippet',
    icon: '✂️',
    detail: 'SELECT ... GROUP BY ...',
    isSnippet: true,
    body: 'SELECT city, COUNT(*) AS total_students\nFROM student\nGROUP BY city\nHAVING COUNT(*) >= 2\nORDER BY total_students DESC;'
  }
];

window.CodeArenaDictionary = {
  cpp: CPP_DICTIONARY,
  sql: SQL_DICTIONARY
};

// ─── CodeMirror Hint Helper ─────────────────────────────────────────

if (typeof CodeMirror !== 'undefined') {
  CodeMirror.registerHelper('hint', 'codearena', function(cm) {
    const isSql = window.currentQuestion && window.currentQuestion.type === 'sql';
    const dict = isSql ? SQL_DICTIONARY : CPP_DICTIONARY;

    const cur = cm.getCursor();
    const token = cm.getTokenAt(cur);
    const line = cm.getLine(cur.line);

    // Compute word range
    let start = cur.ch;
    let end = cur.ch;
    while (start > 0 && /[a-zA-Z0-9_#]/.test(line.charAt(start - 1))) --start;
    while (end < line.length && /[a-zA-Z0-9_#]/.test(line.charAt(end))) ++end;

    const word = line.slice(start, cur.ch);
    if (!word || word.length < 1) return null;

    const lower = word.toLowerCase();
    const matches = dict.filter(item => {
      return item.text.toLowerCase().includes(lower);
    }).sort((a, b) => {
      const aStarts = a.text.toLowerCase().startsWith(lower);
      const bStarts = b.text.toLowerCase().startsWith(lower);
      if (aStarts && !bStarts) return -1;
      if (!aStarts && bStarts) return 1;
      return a.text.localeCompare(b.text);
    }).slice(0, 12);

    if (matches.length === 0) return null;

    return {
      from: CodeMirror.Pos(cur.line, start),
      to: CodeMirror.Pos(cur.line, end),
      list: matches.map(item => ({
        text: item.isSnippet ? item.body : item.text,
        displayText: item.text,
        className: `cm-hint-${item.kind || 'keyword'}`,
        render: function(el) {
          el.innerHTML = `
            <span class="hint-label"><span class="hint-icon">${item.icon || '▪'}</span><strong>${item.text}</strong></span>
            <span class="hint-detail">${item.detail || item.kind || ''}</span>
          `;
        }
      }))
    };
  });
}
