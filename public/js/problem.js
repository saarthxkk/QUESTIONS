// ═══════════════════════════════════════════════════════════════
// CodeArena — Problem Page (Editor + Compiler)
// ═══════════════════════════════════════════════════════════════

let currentQuestion = null;
let boilerplate = '';

document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'));

  if (!id) {
    window.location.href = '/';
    return;
  }

  await loadProblem(id);
  setupEditor();
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
    renderProblem();
  } catch (err) {
    document.getElementById('problemTitle').textContent = 'Problem not found';
  }
}

function renderProblem() {
  const q = currentQuestion;
  const diffClass = q.difficulty.toLowerCase();

  // Navbar
  document.getElementById('navTitle').textContent = `${q.id}. ${q.title}`;
  const navDiff = document.getElementById('navDifficulty');
  navDiff.textContent = q.difficulty;
  navDiff.className = `difficulty-badge ${diffClass}`;
  document.getElementById('navPoints').textContent = `${q.points} pts`;
  document.title = `${q.title} — CodeArena`;

  // Problem header
  document.getElementById('problemTitle').textContent = `${q.id}. ${q.title}`;
  
  const pill = document.getElementById('problemDifficulty');
  pill.textContent = q.difficulty;
  pill.className = `difficulty-pill ${diffClass}`;

  document.getElementById('problemCategory').textContent = q.category;
  
  // Tags
  const tagsContainer = document.getElementById('problemTags');
  tagsContainer.innerHTML = q.tags.map(t => `<span class="tag">${t}</span>`).join('');

  // Description (Markdown)
  if (typeof marked !== 'undefined') {
    document.getElementById('problemDescription').innerHTML = marked.parse(q.description);
  } else {
    document.getElementById('problemDescription').textContent = q.description;
  }

  // Sample I/O
  document.getElementById('sampleInput').textContent = q.sampleInput;
  document.getElementById('sampleOutput').textContent = q.sampleOutput;

  // Boilerplate
  boilerplate = q.boilerplate || '';
  const editor = document.getElementById('codeEditor');
  
  // Load saved code or use boilerplate
  const savedCode = localStorage.getItem(`code_${q.id}`);
  editor.value = savedCode || boilerplate;
  updateLineNumbers();

  // Set custom input to sample
  document.getElementById('customInput').value = q.sampleInput;
}

// ─── Editor Setup ───────────────────────────────────────────────

function setupEditor() {
  const editor = document.getElementById('codeEditor');
  
  // Line numbers
  editor.addEventListener('input', () => {
    updateLineNumbers();
    // Auto-save
    if (currentQuestion) {
      localStorage.setItem(`code_${currentQuestion.id}`, editor.value);
    }
  });

  editor.addEventListener('scroll', () => {
    document.getElementById('lineNumbers').scrollTop = editor.scrollTop;
  });

  // Tab support
  editor.addEventListener('keydown', (e) => {
    // If autocomplete popup is active, let autocomplete handle navigation and selection keys
    if (window.autocomplete && window.autocomplete.visible) {
      if (['Tab', 'Enter', 'ArrowUp', 'ArrowDown', 'Escape'].includes(e.key)) {
        return;
      }
    }

    if (e.key === 'Tab') {
      e.preventDefault();
      const start = editor.selectionStart;
      const end = editor.selectionEnd;

      if (e.shiftKey) {
        // Shift+Tab: remove indent
        const beforeCursor = editor.value.substring(0, start);
        const lastNewline = beforeCursor.lastIndexOf('\n');
        const lineStart = lastNewline + 1;
        const line = editor.value.substring(lineStart);
        
        if (line.startsWith('    ')) {
          editor.value = editor.value.substring(0, lineStart) + line.substring(4);
          editor.selectionStart = editor.selectionEnd = Math.max(start - 4, lineStart);
        } else if (line.startsWith('\t')) {
          editor.value = editor.value.substring(0, lineStart) + line.substring(1);
          editor.selectionStart = editor.selectionEnd = Math.max(start - 1, lineStart);
        }
      } else {
        // Tab: insert 4 spaces
        editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + 4;
      }
      updateLineNumbers();
    }

    // Auto-close brackets
    const pairs = { '(': ')', '{': '}', '[': ']', '"': '"', "'": "'" };
    if (pairs[e.key]) {
      const start = editor.selectionStart;
      const end = editor.selectionEnd;
      if (start !== end) {
        e.preventDefault();
        const selected = editor.value.substring(start, end);
        editor.value = editor.value.substring(0, start) + e.key + selected + pairs[e.key] + editor.value.substring(end);
        editor.selectionStart = start + 1;
        editor.selectionEnd = end + 1;
      }
    }

    // Enter: auto-indent
    if (e.key === 'Enter') {
      const start = editor.selectionStart;
      const beforeCursor = editor.value.substring(0, start);
      const currentLine = beforeCursor.split('\n').pop();
      const indent = currentLine.match(/^\s*/)[0];
      const lastChar = beforeCursor.trim().slice(-1);
      
      let extra = '';
      if (lastChar === '{') {
        extra = '    ';
      }

      e.preventDefault();
      const insertion = '\n' + indent + extra;
      editor.value = editor.value.substring(0, start) + insertion + editor.value.substring(start);
      editor.selectionStart = editor.selectionEnd = start + insertion.length;
      updateLineNumbers();
    }
  });

  // Reset button
  document.getElementById('resetBtn').addEventListener('click', () => {
    if (confirm('Reset code to the original boilerplate?')) {
      editor.value = boilerplate;
      updateLineNumbers();
      if (currentQuestion) {
        localStorage.removeItem(`code_${currentQuestion.id}`);
      }
    }
  });
}

function updateLineNumbers() {
  const editor = document.getElementById('codeEditor');
  const lines = editor.value.split('\n').length;
  const numbers = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
  document.getElementById('lineNumbers').textContent = numbers;
}

// ─── Resizer ────────────────────────────────────────────────────

function setupResizer() {
  const resizer = document.getElementById('resizer');
  const left = document.getElementById('leftPanel');
  let isResizing = false;

  resizer.addEventListener('mousedown', (e) => {
    isResizing = true;
    resizer.classList.add('active');
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  });

  document.addEventListener('mousemove', (e) => {
    if (!isResizing) return;
    const containerWidth = document.querySelector('.split-layout').offsetWidth;
    const newWidth = (e.clientX / containerWidth) * 100;
    if (newWidth > 20 && newWidth < 70) {
      left.style.width = newWidth + '%';
    }
  });

  document.addEventListener('mouseup', () => {
    isResizing = false;
    resizer.classList.remove('active');
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
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
    header.textContent = input.classList.contains('open') ? '▼ Custom Input' : '▶ Custom Input';
  });
}

// ─── Run & Submit ───────────────────────────────────────────────

function setupActions() {
  document.getElementById('runBtn').addEventListener('click', runCode);
  document.getElementById('submitBtn').addEventListener('click', submitCode);
  document.getElementById('clearConsole').addEventListener('click', () => {
    document.getElementById('consoleOutput').textContent = '';
  });
}

async function runCode() {
  const code = document.getElementById('codeEditor').value;
  const input = document.getElementById('customInput').value;
  const btn = document.getElementById('runBtn');

  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span> Running...';
  document.getElementById('consoleOutput').textContent = 'Compiling and running...\n';

  try {
    const res = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code,
        input,
        questionId: currentQuestion ? currentQuestion.id : null
      })
    });
    const result = await res.json();
    
    let output = '';
    if (result.compilationError) {
      output = `❌ Compilation Error:\n${result.compilationError}`;
    } else if (result.timeout) {
      output = `⏱ Time Limit Exceeded`;
    } else if (result.error && !result.success) {
      output = `❌ Runtime Error:\n${result.error}`;
    } else {
      output = `✅ Output:\n${result.output}`;
      if (result.error) {
        output += `\n⚠ Stderr:\n${result.error}`;
      }
    }
    document.getElementById('consoleOutput').textContent = output;
  } catch (err) {
    document.getElementById('consoleOutput').textContent = `Error: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = '▶ Run';
  }
}

async function submitCode() {
  const code = document.getElementById('codeEditor').value;
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

    // Switch to results tab
    document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector('[data-tab="submissions"]').classList.add('active');
    document.getElementById('submissionsTab').classList.add('active');
  } catch (err) {
    document.getElementById('consoleOutput').textContent = `Submission error: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = 'Submit';
  }
}

function renderResults(result) {
  const container = document.getElementById('resultsContainer');
  const isAccepted = result.status === 'Accepted';

  let html = `
    <div class="result-header">
      <span class="result-status ${isAccepted ? 'accepted' : 'failed'}">
        ${isAccepted ? '✅ Accepted' : '❌ ' + result.status}
      </span>
      <div class="result-score">
        <strong>${result.points}</strong> / ${currentQuestion.points} points
        &nbsp;•&nbsp;
        ${result.passed}/${result.total} test cases passed
      </div>
    </div>
    <div class="test-case-list">
  `;

  result.results.forEach((tc, idx) => {
    const icon = tc.passed ? '✓' : '✗';
    const iconClass = tc.passed ? 'pass' : 'fail';

    html += `
      <div class="test-case-item">
        <div class="test-case-header" onclick="this.nextElementSibling.classList.toggle('open')">
          <div class="tc-left">
            <span class="tc-icon ${iconClass}">${icon}</span>
            <span class="tc-name">Test Case ${tc.testCaseId}${tc.description ? ' — ' + tc.description : ''}</span>
            ${tc.isSample ? '<span class="tag">Sample</span>' : ''}
          </div>
          <span class="tc-badge ${iconClass}">${tc.passed ? 'Passed' : 'Failed'}</span>
        </div>
        <div class="test-case-detail">
    `;

    if (tc.compilationError) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Compilation Error</div>
          <div class="detail-value">${escapeHtml(tc.compilationError)}</div>
        </div>
      `;
    } else if (tc.error) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Error</div>
          <div class="detail-value">${escapeHtml(tc.error)}</div>
        </div>
      `;
    }

    if (tc.input !== null && tc.input !== undefined) {
      html += `
        <div class="detail-row">
          <div class="detail-label">Input</div>
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
          <div class="detail-label">Your Output</div>
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

