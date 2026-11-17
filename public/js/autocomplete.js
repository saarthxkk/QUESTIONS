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
  { text: 'name', kind: 'field', icon: '🏷️', detail: 'student.name' },
  { text: 'age', kind: 'field', icon: '🏷️', detail: 'student.age' },
  { text: 'gender', kind: 'field', icon: '🏷️', detail: "student.gender ('M'/'F')" },
  { text: 'city', kind: 'field', icon: '🏷️', detail: 'student.city' },
  { text: 'email', kind: 'field', icon: '🏷️', detail: 'student.email' },
  { text: 'marks', kind: 'field', icon: '🏷️', detail: 'student.marks' },
  { text: 'dob', kind: 'field', icon: '🏷️', detail: 'student.dob' },

  // ── Common Problem Aliases ──
  { text: 'student_name', kind: 'field', icon: '🏷️', detail: 'name AS student_name' },
  { text: 'student_marks', kind: 'field', icon: '🏷️', detail: 'marks AS student_marks' },
  { text: 'total_students', kind: 'field', icon: '🏷️', detail: 'COUNT(*) AS total_students' },
  { text: 'total_marks', kind: 'field', icon: '🏷️', detail: 'SUM(marks) AS total_marks' },
  { text: 'average_marks', kind: 'field', icon: '🏷️', detail: 'ROUND(AVG(marks), 2) AS average_marks' },
  { text: 'highest_marks', kind: 'field', icon: '🏷️', detail: 'MAX(marks) AS highest_marks' },
  { text: 'lowest_marks', kind: 'field', icon: '🏷️', detail: 'MIN(marks) AS lowest_marks' },
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
