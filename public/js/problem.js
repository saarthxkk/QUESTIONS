// ═══════════════════════════════════════════════════════════════
// CodeArena — Problem Workspace (CodeMirror + Compiler)
// ═══════════════════════════════════════════════════════════════

let currentQuestion = null;
let boilerplate = '';
let cmEditor = null;

document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'));

  if (!id) {
    window.location.href = '/';
    return;
  }

  await loadProblem(id);
  setupCodeMirror();
  setupResizer();
  setupTabs();
  setupCustomInput();
  setupActions();
});

// ─── Load Problem ───────────────────────────────────────────────

async function loadProblem(id) {
  try {
    const res = await fetch(`/api/questions/${id}`);
    if (!res.ok) throw new Error('Not found');
    currentQuestion = await res.json();
    window.currentQuestion = currentQuestion;
    renderProblem();
  } catch (err) {
    document.getElementById('problemTitle').textContent = 'Problem not found';
  }
}

function renderProblem() {
  const q = currentQuestion;
  const isSql = q.type === 'sql';
  const diffClass = q.difficulty.toLowerCase();

  // Navbar
  document.getElementById('navTitle').textContent = `${q.id}. ${q.title}`;
  const navDiff = document.getElementById('navDifficulty');
  navDiff.textContent = q.difficulty;
  navDiff.className = `difficulty-badge ${diffClass}`;
  document.getElementById('navPoints').textContent = `${q.points} PTS`;
  document.title = `${q.title} — CodeArena`;

  // Problem header
  document.getElementById('problemTitle').textContent = `${q.id}. ${q.title}`;
  
  const pill = document.getElementById('problemDifficulty');
  pill.textContent = q.difficulty;
  pill.className = `difficulty-pill ${diffClass}`;

  const catPill = document.getElementById('problemCategory');
  catPill.textContent = q.category;
  if (isSql) {
    catPill.classList.add('cat-sql');
  }

  // Language badge in editor header
  const langBadge = document.getElementById('editorLangBadge');
  if (langBadge) {
    langBadge.textContent = isSql ? 'MySQL 8.0' : 'C++17';
  }

  // Tags
  const tagsContainer = document.getElementById('problemTags');
  tagsContainer.innerHTML = q.tags.map(t => `<span class="tag">${t}</span>`).join('');

  // Description (Markdown)
  if (typeof marked !== 'undefined') {
    document.getElementById('problemDescription').innerHTML = marked.parse(q.description);
  } else {
    document.getElementById('problemDescription').textContent = q.description;
  }

  // Update sample headers
  const inHeader = document.getElementById('sampleInputHeader');
  const outHeader = document.getElementById('sampleOutputHeader');
  if (inHeader) inHeader.textContent = isSql ? 'Sample Database Specimen (student table)' : 'Sample Input';
  if (outHeader) outHeader.textContent = isSql ? 'Expected Query Result Table' : 'Expected Output';

  // Sample I/O
  document.getElementById('sampleInput').textContent = q.sampleInput;
  document.getElementById('sampleOutput').textContent = q.sampleOutput;

  // Boilerplate
  boilerplate = q.boilerplate || '';
  
  // Custom input placeholder & label
  const customHeader = document.querySelector('#toggleCustomInput span');
  const customInputEl = document.getElementById('customInput');
  if (customHeader) {
    customHeader.textContent = isSql ? '▶ Custom Query / Test' : '▶ Custom Input';
  }
  if (customInputEl) {
    customInputEl.placeholder = isSql 
      ? 'Enter custom SQL query (e.g. SELECT * FROM student;) or leave empty to test editor solution...'
      : 'Enter your custom test input here...';
    customInputEl.value = isSql ? '' : q.sampleInput;
  }

  // If CodeMirror is already mounted, set content and mode
  if (cmEditor) {
    const savedCode = localStorage.getItem(`code_${q.id}`);
    const initialCode = savedCode || boilerplate;
    cmEditor.setValue(initialCode);
    cmEditor.setOption('mode', isSql ? 'text/x-mysql' : 'text/x-c++src');
    cmEditor.clearHistory();
  }
}

// ─── CodeMirror Initialization ──────────────────────────────────

function setupCodeMirror() {
  const textarea = document.getElementById('codeEditor');
  const isSql = currentQuestion && currentQuestion.type === 'sql';
  const savedCode = currentQuestion ? localStorage.getItem(`code_${currentQuestion.id}`) : null;
  const initialCode = savedCode || boilerplate;
  textarea.value = initialCode;

  if (typeof CodeMirror !== 'undefined') {
    cmEditor = CodeMirror.fromTextArea(textarea, {
      lineNumbers: true,
      mode: isSql ? 'text/x-mysql' : 'text/x-c++src',
      theme: 'costar',
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      matchBrackets: true,
      autoCloseBrackets: true,
      lineWrapping: false,
      extraKeys: {
        "Tab": function(cm) {
          if (cm.somethingSelected()) {
            cm.indentSelection("add");
          } else {
            cm.replaceSelection("    ", "end");
          }
        },
        "Shift-Tab": function(cm) {
          cm.indentSelection("subtract");
        },
        "Ctrl-Space": function(cm) {
          if (CodeMirror.hint && CodeMirror.hint.codearena) {
            cm.showHint({ hint: CodeMirror.hint.codearena, completeSingle: false });
          }
        }
      }
    });

    // Synchronize textarea & save to localStorage
    cmEditor.on('change', () => {
      textarea.value = cmEditor.getValue();
      if (currentQuestion) {
        localStorage.setItem(`code_${currentQuestion.id}`, textarea.value);
      }
    });

    // Auto-trigger hints while typing (VS Code Style)
    cmEditor.on('inputRead', (cm, change) => {
      if (change.origin === '+input' && change.text && change.text[0]) {
        const curChar = change.text[0];
        // Trigger on letter or underscore
        if (/[a-zA-Z_]/.test(curChar)) {
          if (CodeMirror.hint && CodeMirror.hint.codearena) {
            cm.showHint({ hint: CodeMirror.hint.codearena, completeSingle: false });
          }
        }
      }
    });

    // Refresh layout after render
    setTimeout(() => cmEditor.refresh(), 100);
  }

  // Reset button logic
  document.getElementById('resetBtn').addEventListener('click', () => {
    if (confirm('Reset code to the original specimen boilerplate?')) {
      if (cmEditor) {
        cmEditor.setValue(boilerplate);
        cmEditor.focus();
      } else {
        textarea.value = boilerplate;
      }
      if (currentQuestion) {
        localStorage.removeItem(`code_${currentQuestion.id}`);
      }
    }
  });
}

function getEditorCode() {
  if (cmEditor) {
    return cmEditor.getValue();
  }
  return document.getElementById('codeEditor').value;
}

// ─── Resizer ────────────────────────────────────────────────────

function setupResizer() {
  const resizer = document.getElementById('resizer');
  const left = document.getElementById('leftPanel');
  let isResizing = false;

  resizer.addEventListener('mousedown', () => {
    isResizing = true;
    resizer.classList.add('active');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  });

  document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    const containerWidth = document.querySelector('.split-layout').offsetWidth;
    const newWidth = (e.clientX / containerWidth) * 100;
    if (newWidth > 20 && newWidth < 75) {
      left.style.width = newWidth + '%';
      if (cmEditor) cmEditor.refresh();
    }
  });

  document.addEventListener('mouseup', () => {
    isResizing = false;
    resizer.classList.remove('active');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
    if (cmEditor) cmEditor.refresh();
  });
}

// ─── Tabs ───────────────────────────────────────────────────────

function setupTabs() {
  document.querySelectorAll('.panel-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tab.dataset.tab + 'Tab').classList.add('active');
    });
  });
}

// ─── Custom Input Toggle ────────────────────────────────────────

function setupCustomInput() {
  document.getElementById('toggleCustomInput').addEventListener('click', () => {
    const input = document.getElementById('customInput');
    input.classList.toggle('open');
    const header = document.getElementById('toggleCustomInput').querySelector('span');
    const isSql = currentQuestion && currentQuestion.type === 'sql';
    const label = isSql ? 'Custom Query / Test' : 'Custom Input';
    header.textContent = input.classList.contains('open') ? `▼ ${label}` : `▶ ${label}`;
    if (input.classList.contains('open')) {
      input.focus();
    }
  });
}

// ─── Run & Submit Actions ───────────────────────────────────────

function setupActions() {
  document.getElementById('runBtn').addEventListener('click', runCode);
  document.getElementById('submitBtn').addEventListener('click', submitCode);
  document.getElementById('clearConsole').addEventListener('click', () => {
    document.getElementById('consoleOutput').textContent = 'Console cleared.';
  });
}

async function runCode() {
  const isSql = currentQuestion && currentQuestion.type === 'sql';
  const customQuery = document.getElementById('customInput').value.trim();
  const editorCode = getEditorCode();
  const code = (isSql && customQuery) ? customQuery : editorCode;
  const input = document.getElementById('customInput').value;
  const btn = document.getElementById('runBtn');

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Running...';
  document.getElementById('consoleOutput').textContent = isSql ? 'Executing query against in-memory database...\n' : 'Compiling and running against specimen input...\n';

  try {
    const res = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code,
        input: isSql ? '' : input,
        questionId: currentQuestion ? currentQuestion.id : null
      })
    });
    const result = await res.json();
    
    let output = '';
    if (result.compilationError) {
      output = `❌ ${isSql ? 'SQL Error' : 'Compilation Error'}:\n${result.compilationError}`;
    } else if (result.timeout) {
      output = `⏱ Time Limit Exceeded`;
    } else if (result.error && !result.success) {
      output = `❌ Execution Error:\n${result.error}`;
    } else {
      output = `✅ Result:\n${result.output}`;
      if (result.error) {
        output += `\n⚠ Stderr:\n${result.error}`;
      }
    }
    document.getElementById('consoleOutput').textContent = output;
  } catch (err) {
    document.getElementById('consoleOutput').textContent = `Execution fault: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '▶ Run';
  }
}

async function submitCode() {
  const code = getEditorCode();
  const btn = document.getElementById('submitBtn');

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Judging...';

  try {
    const res = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, questionId: currentQuestion.id })
    });
    const result = await res.json();
    renderResults(result);

    // Switch to submissions tab
    document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector('[data-tab="submissions"]').classList.add('active');
    document.getElementById('submissionsTab').classList.add('active');
  } catch (err) {
    document.getElementById('consoleOutput').textContent = `Submission fault: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Submit Solution';
  }
}

function renderResults(result) {
  const container = document.getElementById('resultsContainer');
  const isAccepted = result.status === 'Accepted';

  let html = `
    <div class="result-header">
      <span class="result-status ${isAccepted ? 'accepted' : 'failed'}">
        ${isAccepted ? '✓ Accepted' : '✗ ' + result.status}
      </span>
      <div class="result-score">
        <strong>${result.points}</strong> / ${currentQuestion.points} PTS
        &nbsp;•&nbsp;
        ${result.passed}/${result.total} test cases satisfied
      </div>
    </div>
    <div class="test-case-list">
  `;

  result.results.forEach((tc) => {
    const icon = tc.passed ? '✓' : '✗';
    const iconClass = tc.passed ? 'pass' : 'fail';

    html += `
      <div class="test-case-item">
        <div class="test-case-header" onclick="this.nextElementSibling.classList.toggle('open')">
          <div class="tc-left">
            <span class="tc-icon ${iconClass}">${icon}</span>
            <span class="tc-name">Case ${tc.testCaseId}${tc.description ? ' — ' + tc.description : ''}</span>
            ${tc.isSample ? '<span class="category-tag">Specimen</span>' : ''}
          </div>
          <span class="tc-badge ${iconClass}">${tc.passed ? 'Passed' : 'Failed'}</span>
        </div>
        <div class="test-case-detail">
    `;

    if (tc.compilationError) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Judgement Diagnostic / Error</div>
          <div class="detail-value">${escapeHtml(tc.compilationError)}</div>
        </div>
      `;
    } else if (tc.error) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Diagnostic Output</div>
          <div class="detail-value">${escapeHtml(tc.error)}</div>
        </div>
      `;
    }

    if (tc.input !== null && tc.input !== undefined) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Input Parameters</div>
          <div class="detail-value">${escapeHtml(tc.input)}</div>
        </div>
      `;
    }

    if (tc.expectedOutput !== null && tc.expectedOutput !== undefined) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Expected Output</div>
          <div class="detail-value">${escapeHtml(tc.expectedOutput)}</div>
        </div>
      `;
    }

    if (tc.actualOutput !== null && tc.actualOutput !== undefined) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Actual Solution Output</div>
          <div class="detail-value" style="${tc.passed ? '' : 'color: var(--red);'}">${escapeHtml(tc.actualOutput)}</div>
        </div>
      `;
    }

    html += `
        </div>
      </div>
    `;
  });

  html += '</div>';
  container.innerHTML = html;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
