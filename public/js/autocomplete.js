// ═══════════════════════════════════════════════════════════════
// CodeArena — C++ Autocomplete Engine (VS Code Style)
// ═══════════════════════════════════════════════════════════════

class CppAutocomplete {
  constructor(editor) {
    this.editor = editor;
    this.dropdown = null;
    this.selectedIndex = -1;
    this.visible = false;
    this.suggestions = [];
    
    this.initDropdown();
    this.bindEvents();
    this.buildDictionary();
  }

  // ─── Dictionary ─────────────────────────────────────────────

  buildDictionary() {
    this.dictionary = [
      // ── Keywords ──
      { text: 'auto', kind: 'keyword', icon: '🔑' },
      { text: 'bool', kind: 'keyword', icon: '🔑' },
      { text: 'break', kind: 'keyword', icon: '🔑' },
      { text: 'case', kind: 'keyword', icon: '🔑' },
      { text: 'catch', kind: 'keyword', icon: '🔑' },
      { text: 'char', kind: 'keyword', icon: '🔑' },
      { text: 'class', kind: 'keyword', icon: '🔑' },
      { text: 'const', kind: 'keyword', icon: '🔑' },
      { text: 'constexpr', kind: 'keyword', icon: '🔑' },
      { text: 'continue', kind: 'keyword', icon: '🔑' },
      { text: 'default', kind: 'keyword', icon: '🔑' },
      { text: 'delete', kind: 'keyword', icon: '🔑' },
      { text: 'do', kind: 'keyword', icon: '🔑' },
      { text: 'double', kind: 'keyword', icon: '🔑' },
      { text: 'else', kind: 'keyword', icon: '🔑' },
      { text: 'enum', kind: 'keyword', icon: '🔑' },
      { text: 'extern', kind: 'keyword', icon: '🔑' },
      { text: 'false', kind: 'keyword', icon: '🔑' },
      { text: 'float', kind: 'keyword', icon: '🔑' },
      { text: 'for', kind: 'keyword', icon: '🔑' },
      { text: 'friend', kind: 'keyword', icon: '🔑' },
      { text: 'goto', kind: 'keyword', icon: '🔑' },
      { text: 'if', kind: 'keyword', icon: '🔑' },
      { text: 'inline', kind: 'keyword', icon: '🔑' },
      { text: 'int', kind: 'keyword', icon: '🔑' },
      { text: 'long', kind: 'keyword', icon: '🔑' },
      { text: 'namespace', kind: 'keyword', icon: '🔑' },
      { text: 'new', kind: 'keyword', icon: '🔑' },
      { text: 'nullptr', kind: 'keyword', icon: '🔑' },
      { text: 'operator', kind: 'keyword', icon: '🔑' },
      { text: 'override', kind: 'keyword', icon: '🔑' },
      { text: 'private', kind: 'keyword', icon: '🔑' },
      { text: 'protected', kind: 'keyword', icon: '🔑' },
      { text: 'public', kind: 'keyword', icon: '🔑' },
      { text: 'return', kind: 'keyword', icon: '🔑' },
      { text: 'short', kind: 'keyword', icon: '🔑' },
      { text: 'signed', kind: 'keyword', icon: '🔑' },
      { text: 'sizeof', kind: 'keyword', icon: '🔑' },
      { text: 'static', kind: 'keyword', icon: '🔑' },
      { text: 'static_cast', kind: 'keyword', icon: '🔑' },
      { text: 'struct', kind: 'keyword', icon: '🔑' },
      { text: 'switch', kind: 'keyword', icon: '🔑' },
      { text: 'template', kind: 'keyword', icon: '🔑' },
      { text: 'this', kind: 'keyword', icon: '🔑' },
      { text: 'throw', kind: 'keyword', icon: '🔑' },
      { text: 'true', kind: 'keyword', icon: '🔑' },
      { text: 'try', kind: 'keyword', icon: '🔑' },
      { text: 'typedef', kind: 'keyword', icon: '🔑' },
      { text: 'typename', kind: 'keyword', icon: '🔑' },
      { text: 'unsigned', kind: 'keyword', icon: '🔑' },
      { text: 'using', kind: 'keyword', icon: '🔑' },
      { text: 'virtual', kind: 'keyword', icon: '🔑' },
      { text: 'void', kind: 'keyword', icon: '🔑' },
      { text: 'volatile', kind: 'keyword', icon: '🔑' },
      { text: 'while', kind: 'keyword', icon: '🔑' },

      // ── I/O ──
      { text: 'cout', kind: 'object', icon: '📤', detail: 'std::cout' },
      { text: 'cin', kind: 'object', icon: '📥', detail: 'std::cin' },
      { text: 'cerr', kind: 'object', icon: '📤', detail: 'std::cerr' },
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
      { text: 'stack', kind: 'class', icon: '📦', detail: 'std::stack<T>' },
      { text: 'queue', kind: 'class', icon: '📦', detail: 'std::queue<T>' },
      { text: 'priority_queue', kind: 'class', icon: '📦', detail: 'std::priority_queue<T>' },
      { text: 'deque', kind: 'class', icon: '📦', detail: 'std::deque<T>' },
      { text: 'list', kind: 'class', icon: '📦', detail: 'std::list<T>' },
      { text: 'pair', kind: 'class', icon: '📦', detail: 'std::pair<A,B>' },
      { text: 'tuple', kind: 'class', icon: '📦', detail: 'std::tuple<T...>' },
      { text: 'array', kind: 'class', icon: '📦', detail: 'std::array<T,N>' },
      { text: 'bitset', kind: 'class', icon: '📦', detail: 'std::bitset<N>' },

      // ── STL Algorithms ──
      { text: 'sort', kind: 'function', icon: '⚡', detail: 'sort(begin, end)' },
      { text: 'reverse', kind: 'function', icon: '⚡', detail: 'reverse(begin, end)' },
      { text: 'find', kind: 'function', icon: '⚡', detail: 'find(begin, end, val)' },
      { text: 'count', kind: 'function', icon: '⚡', detail: 'count(begin, end, val)' },
      { text: 'lower_bound', kind: 'function', icon: '⚡', detail: 'lower_bound(begin, end, val)' },
      { text: 'upper_bound', kind: 'function', icon: '⚡', detail: 'upper_bound(begin, end, val)' },
      { text: 'binary_search', kind: 'function', icon: '⚡', detail: 'binary_search(begin, end, val)' },
      { text: 'max_element', kind: 'function', icon: '⚡', detail: 'max_element(begin, end)' },
      { text: 'min_element', kind: 'function', icon: '⚡', detail: 'min_element(begin, end)' },
      { text: 'accumulate', kind: 'function', icon: '⚡', detail: 'accumulate(begin, end, init)' },
      { text: 'next_permutation', kind: 'function', icon: '⚡', detail: 'next_permutation(begin, end)' },
      { text: 'prev_permutation', kind: 'function', icon: '⚡', detail: 'prev_permutation(begin, end)' },
      { text: 'unique', kind: 'function', icon: '⚡', detail: 'unique(begin, end)' },
      { text: 'fill', kind: 'function', icon: '⚡', detail: 'fill(begin, end, val)' },
      { text: 'swap', kind: 'function', icon: '⚡', detail: 'swap(a, b)' },
      { text: 'min', kind: 'function', icon: '⚡', detail: 'min(a, b)' },
      { text: 'max', kind: 'function', icon: '⚡', detail: 'max(a, b)' },
      { text: 'abs', kind: 'function', icon: '⚡', detail: 'abs(x)' },
      { text: 'pow', kind: 'function', icon: '⚡', detail: 'pow(base, exp)' },
      { text: 'sqrt', kind: 'function', icon: '⚡', detail: 'sqrt(x)' },
      { text: 'log', kind: 'function', icon: '⚡', detail: 'log(x)' },
      { text: 'ceil', kind: 'function', icon: '⚡', detail: 'ceil(x)' },
      { text: 'floor', kind: 'function', icon: '⚡', detail: 'floor(x)' },
      { text: 'to_string', kind: 'function', icon: '⚡', detail: 'to_string(val)' },
      { text: 'stoi', kind: 'function', icon: '⚡', detail: 'stoi(str)' },
      { text: 'stol', kind: 'function', icon: '⚡', detail: 'stol(str)' },
      { text: 'stoll', kind: 'function', icon: '⚡', detail: 'stoll(str)' },

      // ── Member Methods ──
      { text: 'push_back', kind: 'method', icon: '🔧', detail: '.push_back(val)' },
      { text: 'pop_back', kind: 'method', icon: '🔧', detail: '.pop_back()' },
      { text: 'push_front', kind: 'method', icon: '🔧', detail: '.push_front(val)' },
      { text: 'pop_front', kind: 'method', icon: '🔧', detail: '.pop_front()' },
      { text: 'begin', kind: 'method', icon: '🔧', detail: '.begin()' },
      { text: 'end', kind: 'method', icon: '🔧', detail: '.end()' },
      { text: 'size', kind: 'method', icon: '🔧', detail: '.size()' },
      { text: 'empty', kind: 'method', icon: '🔧', detail: '.empty()' },
      { text: 'clear', kind: 'method', icon: '🔧', detail: '.clear()' },
      { text: 'insert', kind: 'method', icon: '🔧', detail: '.insert(pos, val)' },
      { text: 'erase', kind: 'method', icon: '🔧', detail: '.erase(pos)' },
      { text: 'front', kind: 'method', icon: '🔧', detail: '.front()' },
      { text: 'back', kind: 'method', icon: '🔧', detail: '.back()' },
      { text: 'top', kind: 'method', icon: '🔧', detail: '.top()' },
      { text: 'push', kind: 'method', icon: '🔧', detail: '.push(val)' },
      { text: 'pop', kind: 'method', icon: '🔧', detail: '.pop()' },
      { text: 'length', kind: 'method', icon: '🔧', detail: '.length()' },
      { text: 'substr', kind: 'method', icon: '🔧', detail: '.substr(pos, len)' },
      { text: 'resize', kind: 'method', icon: '🔧', detail: '.resize(n)' },
      { text: 'reserve', kind: 'method', icon: '🔧', detail: '.reserve(n)' },
      { text: 'emplace_back', kind: 'method', icon: '🔧', detail: '.emplace_back(args...)' },
      { text: 'make_pair', kind: 'function', icon: '⚡', detail: 'make_pair(a, b)' },
      { text: 'first', kind: 'property', icon: '🏷️', detail: '.first' },
      { text: 'second', kind: 'property', icon: '🏷️', detail: '.second' },

      // ── Preprocessor ──
      { text: '#include', kind: 'preprocessor', icon: '📎', detail: '#include <header>' },
      { text: '#define', kind: 'preprocessor', icon: '📎', detail: '#define NAME value' },
      { text: '#ifndef', kind: 'preprocessor', icon: '📎', detail: '#ifndef GUARD' },
      { text: '#endif', kind: 'preprocessor', icon: '📎', detail: '#endif' },
      { text: '#pragma', kind: 'preprocessor', icon: '📎', detail: '#pragma once' },

      // ── Common Headers ──
      { text: 'iostream', kind: 'header', icon: '📄', detail: '<iostream>' },
      { text: 'algorithm', kind: 'header', icon: '📄', detail: '<algorithm>' },
      { text: 'cmath', kind: 'header', icon: '📄', detail: '<cmath>' },
      { text: 'cstring', kind: 'header', icon: '📄', detail: '<cstring>' },
      { text: 'climits', kind: 'header', icon: '📄', detail: '<climits>' },
      { text: 'numeric', kind: 'header', icon: '📄', detail: '<numeric>' },
      { text: 'functional', kind: 'header', icon: '📄', detail: '<functional>' },
      { text: 'cassert', kind: 'header', icon: '📄', detail: '<cassert>' },
      { text: 'iomanip', kind: 'header', icon: '📄', detail: '<iomanip>' },
      { text: 'sstream', kind: 'header', icon: '📄', detail: '<sstream>' },

      // ── Common Types ──
      { text: 'INT_MAX', kind: 'constant', icon: '🔢', detail: '2147483647' },
      { text: 'INT_MIN', kind: 'constant', icon: '🔢', detail: '-2147483648' },
      { text: 'LLONG_MAX', kind: 'constant', icon: '🔢', detail: '9223372036854775807' },
      { text: 'LLONG_MIN', kind: 'constant', icon: '🔢', detail: '-9223372036854775808' },
      { text: 'long long', kind: 'keyword', icon: '🔑', detail: '64-bit integer' },
      { text: 'size_t', kind: 'keyword', icon: '🔑', detail: 'unsigned size type' },
    ];

    // ── Snippets (insert multi-line templates) ──
    this.snippets = [
      {
        trigger: 'fori',
        label: 'for (int i = 0; i < n; i++)',
        kind: 'snippet',
        icon: '✂️',
        detail: 'For loop with index i',
        body: 'for (int i = 0; i < n; i++) {\n    \n}'
      },
      {
        trigger: 'forj',
        label: 'for (int j = 0; j < m; j++)',
        kind: 'snippet',
        icon: '✂️',
        detail: 'For loop with index j',
        body: 'for (int j = 0; j < m; j++) {\n    \n}'
      },
      {
        trigger: 'forr',
        label: 'for (int i = n-1; i >= 0; i--)',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Reverse for loop',
        body: 'for (int i = n - 1; i >= 0; i--) {\n    \n}'
      },
      {
        trigger: 'fore',
        label: 'for (auto& x : container)',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Range-based for loop',
        body: 'for (auto& x : container) {\n    \n}'
      },
      {
        trigger: 'while',
        label: 'while (condition) { }',
        kind: 'snippet',
        icon: '✂️',
        detail: 'While loop',
        body: 'while (condition) {\n    \n}'
      },
      {
        trigger: 'ife',
        label: 'if ... else ...',
        kind: 'snippet',
        icon: '✂️',
        detail: 'If-else block',
        body: 'if (condition) {\n    \n} else {\n    \n}'
      },
      {
        trigger: 'main',
        label: 'int main() { ... }',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Main function',
        body: 'int main() {\n    \n    return 0;\n}'
      },
      {
        trigger: 'cout',
        label: 'cout << val << endl;',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Print with newline',
        body: 'cout << '
      },
      {
        trigger: 'cin',
        label: 'cin >> variable;',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Read input',
        body: 'cin >> '
      },
      {
        trigger: 'vec',
        label: 'vector<int> v(n);',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Vector declaration',
        body: 'vector<int> v(n);'
      },
      {
        trigger: 'veci',
        label: 'vector<int> v;',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Empty int vector',
        body: 'vector<int> v;'
      },
      {
        trigger: 'vec2d',
        label: 'vector<vector<int>> grid(n, vector<int>(m));',
        kind: 'snippet',
        icon: '✂️',
        detail: '2D vector',
        body: 'vector<vector<int>> grid(n, vector<int>(m, 0));'
      },
      {
        trigger: 'readn',
        label: 'Read N integers into vector',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Input loop pattern',
        body: 'int n;\ncin >> n;\nvector<int> v(n);\nfor (int i = 0; i < n; i++) cin >> v[i];'
      },
      {
        trigger: 'printv',
        label: 'Print vector elements',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Output loop pattern',
        body: 'for (int i = 0; i < v.size(); i++) {\n    cout << v[i];\n    if (i < v.size() - 1) cout << " ";\n}\ncout << endl;'
      },
      {
        trigger: 'sorta',
        label: 'sort(v.begin(), v.end());',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Sort ascending',
        body: 'sort(v.begin(), v.end());'
      },
      {
        trigger: 'sortd',
        label: 'sort descending',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Sort descending',
        body: 'sort(v.begin(), v.end(), greater<int>());'
      },
      {
        trigger: 'node',
        label: 'struct Node { ... }',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Tree node struct',
        body: 'struct Node {\n    int data;\n    Node* left;\n    Node* right;\n    Node(int val) : data(val), left(nullptr), right(nullptr) {}\n};'
      },
      {
        trigger: 'lnode',
        label: 'struct ListNode { ... }',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Linked list node',
        body: 'struct ListNode {\n    int val;\n    ListNode* next;\n    ListNode(int x) : val(x), next(nullptr) {}\n};'
      },
      {
        trigger: 'incall',
        label: '#include all common headers',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Include bits/stdc++.h',
        body: '#include <bits/stdc++.h>\nusing namespace std;'
      },
      {
        trigger: 'incio',
        label: '#include <iostream>',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Include iostream',
        body: '#include <iostream>\nusing namespace std;'
      },
      {
        trigger: 'fastio',
        label: 'Fast I/O setup',
        kind: 'snippet',
        icon: '✂️',
        detail: 'ios_base::sync_with_stdio(false)',
        body: 'ios_base::sync_with_stdio(false);\ncin.tie(NULL);'
      },
      {
        trigger: 'dfs',
        label: 'DFS template',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Depth-first search',
        body: 'void dfs(int node, vector<vector<int>>& adj, vector<bool>& visited) {\n    visited[node] = true;\n    for (int neighbor : adj[node]) {\n        if (!visited[neighbor]) {\n            dfs(neighbor, adj, visited);\n        }\n    }\n}'
      },
      {
        trigger: 'bfs',
        label: 'BFS template',
        kind: 'snippet',
        icon: '✂️',
        detail: 'Breadth-first search',
        body: 'void bfs(int start, vector<vector<int>>& adj) {\n    vector<bool> visited(adj.size(), false);\n    queue<int> q;\n    q.push(start);\n    visited[start] = true;\n    while (!q.empty()) {\n        int node = q.front();\n        q.pop();\n        for (int neighbor : adj[node]) {\n            if (!visited[neighbor]) {\n                visited[neighbor] = true;\n                q.push(neighbor);\n            }\n        }\n    }\n}'
      },
    ];
  }

  // ─── Dropdown UI ────────────────────────────────────────────

  initDropdown() {
    this.dropdown = document.createElement('div');
    this.dropdown.className = 'autocomplete-dropdown';
    this.dropdown.style.display = 'none';
    document.body.appendChild(this.dropdown);

    // Info tooltip
    this.tooltip = document.createElement('div');
    this.tooltip.className = 'autocomplete-tooltip';
    this.tooltip.style.display = 'none';
    document.body.appendChild(this.tooltip);
  }

  // ─── Events ─────────────────────────────────────────────────

  bindEvents() {
    this.editor.addEventListener('input', () => this.onInput());
    this.editor.addEventListener('keydown', (e) => this.onKeyDown(e), true);
    this.editor.addEventListener('blur', () => {
      // Delay hide so click on dropdown works
      setTimeout(() => this.hide(), 200);
    });
    this.editor.addEventListener('scroll', () => this.hide());

    // Click on dropdown item
    this.dropdown.addEventListener('mousedown', (e) => {
      e.preventDefault(); // Prevent blur
      const item = e.target.closest('.ac-item');
      if (item) {
        const idx = parseInt(item.dataset.index);
        this.accept(idx);
      }
    });

    // Hover on dropdown item
    this.dropdown.addEventListener('mouseover', (e) => {
      const item = e.target.closest('.ac-item');
      if (item) {
        const idx = parseInt(item.dataset.index);
        this.selectItem(idx);
      }
    });
  }

  onInput() {
    const word = this.getCurrentWord();
    if (word.length < 2) {
      this.hide();
      return;
    }
    this.updateSuggestions(word);
  }

  onKeyDown(e) {
    if (!this.visible) {
      // Ctrl+Space to trigger manually
      if (e.key === ' ' && e.ctrlKey) {
        e.preventDefault();
        const word = this.getCurrentWord();
        if (word.length >= 1) {
          this.updateSuggestions(word);
        }
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        this.selectItem(Math.min(this.selectedIndex + 1, this.suggestions.length - 1));
        break;

      case 'ArrowUp':
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        this.selectItem(Math.max(this.selectedIndex - 1, 0));
        break;

      case 'Tab':
      case 'Enter':
        if (this.selectedIndex >= 0) {
          e.preventDefault();
          e.stopPropagation();
          e.stopImmediatePropagation();
          this.accept(this.selectedIndex);
        }
        break;

      case 'Escape':
        e.preventDefault();
        e.stopPropagation();
        e.stopImmediatePropagation();
        this.hide();
        break;
    }
  }

  // ─── Word Extraction ───────────────────────────────────────

  getCurrentWord() {
    const pos = this.editor.selectionStart;
    const text = this.editor.value;
    
    // Walk backwards from cursor to find word start
    let start = pos;
    while (start > 0) {
      const ch = text[start - 1];
      if (/[a-zA-Z0-9_#]/.test(ch)) {
        start--;
      } else {
        break;
      }
    }
    
    return text.substring(start, pos);
  }

  getWordStart() {
    const pos = this.editor.selectionStart;
    const text = this.editor.value;
    let start = pos;
    while (start > 0) {
      const ch = text[start - 1];
      if (/[a-zA-Z0-9_#]/.test(ch)) {
        start--;
      } else {
        break;
      }
    }
    return start;
  }

  // ─── Filtering ─────────────────────────────────────────────

  updateSuggestions(word) {
    const lower = word.toLowerCase();

    // High frequency programmer essentials to boost to the top
    const highPriority = {
      'cout': 50,
      'cin': 49,
      'endl': 45,
      'vector': 40,
      'int': 35,
      'string': 34,
      'return': 33,
      'bool': 30,
      'auto': 29,
      'for': 28,
      'if': 27,
      'while': 26,
      'push_back': 25,
      'Node': 24,
      'nullptr': 23,
      '#include': 22
    };

    let matches = [];

    // Snippet matches (prioritize)
    for (const s of this.snippets) {
      const trigLower = s.trigger.toLowerCase();
      if (trigLower.startsWith(lower) || s.label.toLowerCase().includes(lower)) {
        let baseScore = trigLower === lower ? 30 : (trigLower.startsWith(lower) ? 20 : 10);
        if (highPriority[s.trigger]) baseScore += highPriority[s.trigger];
        matches.push({
          text: s.trigger,
          displayText: s.label,
          kind: s.kind,
          icon: s.icon,
          detail: s.detail,
          isSnippet: true,
          body: s.body,
          score: baseScore
        });
      }
    }

    // Dictionary matches
    for (const d of this.dictionary) {
      const textLower = d.text.toLowerCase();
      if (textLower.startsWith(lower)) {
        let baseScore = textLower === lower ? 30 : 15;
        if (highPriority[d.text]) baseScore += highPriority[d.text];
        matches.push({
          text: d.text,
          displayText: d.text,
          kind: d.kind,
          icon: d.icon,
          detail: d.detail || '',
          isSnippet: false,
          score: baseScore
        });
      }
    }

    // Sort: higher score first, then alphabetical
    matches.sort((a, b) => b.score - a.score || a.displayText.localeCompare(b.displayText));

    // Deduplicate by displayText
    const seen = new Set();
    matches = matches.filter(m => {
      if (seen.has(m.displayText)) return false;
      seen.add(m.displayText);
      return true;
    });

    // Limit to 8 items
    matches = matches.slice(0, 8);

    this.suggestions = matches;

    if (matches.length === 0) {
      this.hide();
      return;
    }

    // Don't show if only match is exactly what's typed
    if (matches.length === 1 && matches[0].text.toLowerCase() === lower && !matches[0].isSnippet) {
      this.hide();
      return;
    }

    this.render();
    this.selectItem(0);
    this.show();
  }

  // ─── Rendering ─────────────────────────────────────────────

  render() {
    this.dropdown.innerHTML = this.suggestions.map((s, i) => `
      <div class="ac-item ${i === this.selectedIndex ? 'selected' : ''}" data-index="${i}">
        <span class="ac-icon">${s.icon}</span>
        <span class="ac-text">${this.highlightMatch(s.displayText)}</span>
        <span class="ac-kind">${s.kind}</span>
      </div>
    `).join('');

    this.positionDropdown();
  }

  highlightMatch(text) {
    const word = this.getCurrentWord().toLowerCase();
    const idx = text.toLowerCase().indexOf(word);
    if (idx === -1) return text;
    return text.substring(0, idx) +
           '<strong>' + text.substring(idx, idx + word.length) + '</strong>' +
           text.substring(idx + word.length);
  }

  positionDropdown() {
    const pos = this.editor.selectionStart;
    const text = this.editor.value.substring(0, pos);
    const lines = text.split('\n');
    const lineNum = lines.length;
    const colNum = lines[lines.length - 1].length;

    // Get editor position and styles
    const editorRect = this.editor.getBoundingClientRect();
    const lineHeight = 19.5; // 13px font * 1.5
    const charWidth = 7.82;  // JetBrains Mono 13px character width

    let top = editorRect.top + 12 + (lineNum * lineHeight) - this.editor.scrollTop + 4;
    let left = editorRect.left + 16 + (colNum * charWidth) - this.editor.scrollLeft;

    // Boundary constraints
    if (left < editorRect.left + 16) left = editorRect.left + 16;
    if (left + 300 > window.innerWidth) left = window.innerWidth - 310;
    if (top + 220 > window.innerHeight) {
      top = top - 220 - lineHeight;
    }

    this.dropdown.style.top = `${top}px`;
    this.dropdown.style.left = `${left}px`;
  }

  selectItem(idx) {
    this.selectedIndex = idx;
    const items = this.dropdown.querySelectorAll('.ac-item');
    items.forEach((item, i) => {
      item.classList.toggle('selected', i === idx);
    });

    // Scroll selected into view
    if (items[idx]) {
      items[idx].scrollIntoView({ block: 'nearest' });
    }

    // Show tooltip
    if (this.suggestions[idx]) {
      const s = this.suggestions[idx];
      if (s.detail) {
        this.tooltip.textContent = s.detail;
        this.tooltip.style.display = 'block';
        const rect = this.dropdown.getBoundingClientRect();
        this.tooltip.style.top = rect.top + 'px';
        this.tooltip.style.left = (rect.right + 6) + 'px';
      } else {
        this.tooltip.style.display = 'none';
      }
    }
  }

  // ─── Accept ─────────────────────────────────────────────────

  accept(idx) {
    const suggestion = this.suggestions[idx];
    if (!suggestion) return;

    const wordStart = this.getWordStart();
    const pos = this.editor.selectionStart;
    const before = this.editor.value.substring(0, wordStart);
    const after = this.editor.value.substring(pos);

    const insertText = suggestion.isSnippet ? suggestion.body : suggestion.text;
    
    this.editor.value = before + insertText + after;
    
    const newPos = wordStart + insertText.length;
    this.editor.selectionStart = this.editor.selectionEnd = newPos;
    
    this.editor.focus();
    this.hide();

    // Trigger input event for line numbers update
    this.editor.dispatchEvent(new Event('input'));
  }

  // ─── Show/Hide ─────────────────────────────────────────────

  show() {
    this.dropdown.style.display = 'block';
    this.visible = true;
  }

  hide() {
    this.dropdown.style.display = 'none';
    this.tooltip.style.display = 'none';
    this.visible = false;
    this.selectedIndex = -1;
    this.suggestions = [];
  }
}

// Initialize when problem page loads
document.addEventListener('DOMContentLoaded', () => {
  // Wait a bit for editor to be ready
  setTimeout(() => {
    const editor = document.getElementById('codeEditor');
    if (editor) {
      window.autocomplete = new CppAutocomplete(editor);
    }
  }, 500);
});

