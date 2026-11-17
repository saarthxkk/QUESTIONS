// ═══════════════════════════════════════════════════════════════
// CodeArena — LeetCode-style Problem Workspace
// ═══════════════════════════════════════════════════════════════

let allQuestions = [];
let currentQuestion = null;
let boilerplate = '';
let cmEditor = null;
let currentTrack = 'all';

document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'));
  currentTrack = params.get('track') || 'all';

  if (!id) {
    window.location.href = '/';
    return;
  }

  // Load all questions list for next/prev navigation
  await loadQuestionDirectory();

  // Load active question
  await loadProblem(id);

  setupCodeMirror();
  setupResizer();
  setupPanelTabs();
  setupDrawerTabs();
  setupNavigators();
  setupActions();
});

// ─── Question Directory & Navigation ────────────────────────────

async function loadQuestionDirectory() {
  try {
    const res = await fetch('/api/questions');
    allQuestions = await res.json();
  } catch (e) {
    console.error('Could not load directory:', e);
  }
}

function setupNavigators() {
  const prevBtn = document.getElementById('prevProblemBtn');
  const nextBtn = document.getElementById('nextProblemBtn');
  const backLink = document.getElementById('backToProblemList');

  // Set back link
  if (currentTrack && currentTrack !== 'all') {
    backLink.href = `/?track=${encodeURIComponent(currentTrack)}`;
  } else {
    backLink.href = '/';
  }

  // Filter pool for next/prev:
  let pool = allQuestions;
  if (currentTrack && currentTrack !== 'all') {
    pool = allQuestions.filter(q => q.track === currentTrack || q.category === currentTrack);
  }
  if (!pool || pool.length === 0) pool = allQuestions;

  const currentIdx = pool.findIndex(q => q.id === (currentQuestion ? currentQuestion.id : -1));

  if (prevBtn) {
    prevBtn.disabled = currentIdx <= 0;
    prevBtn.onclick = () => {
      if (currentIdx > 0) {
        const prevQ = pool[currentIdx - 1];
        window.location.href = `/problem?id=${prevQ.id}&track=${encodeURIComponent(currentTrack)}`;
      }
    };
  }

  if (nextBtn) {
    nextBtn.disabled = currentIdx >= pool.length - 1;
    nextBtn.onclick = () => {
      if (currentIdx < pool.length - 1) {
        const nextQ = pool[currentIdx + 1];
        window.location.href = `/problem?id=${nextQ.id}&track=${encodeURIComponent(currentTrack)}`;
      }
    };
  }
}

// ─── Load Problem ───────────────────────────────────────────────

async function loadProblem(id) {
  try {
    const res = await fetch(`/api/questions/${id}`);
    if (!res.ok) throw new Error('Not found');
    currentQuestion = await res.json();
    window.currentQuestion = currentQuestion;
    renderProblem();
    setupNavigators();
  } catch (err) {
    document.getElementById('problemTitle').textContent = 'Problem not found';
  }
}

function renderProblem() {
  const q = currentQuestion;
  const isSql = q.type === 'sql';
  const diffClass = q.difficulty.toLowerCase();

  // Top Navbar Title
  document.getElementById('navTitle').textContent = `${q.id}. ${q.title}`;
  document.getElementById('navPoints').textContent = `${q.points} PTS`;
  document.title = `${q.title} — CodeArena`;

  // Left Pane Header
  document.getElementById('problemTitle').textContent = `${q.id}. ${q.title}`;
  
  const diffPill = document.getElementById('problemDifficulty');
  diffPill.textContent = q.difficulty;
  diffPill.className = `difficulty-pill ${diffClass}`;

  const topicPill = document.getElementById('problemTopic');
  topicPill.textContent = `🏷️ ${q.subtopic || q.category}`;

  const catPill = document.getElementById('problemCategory');
  catPill.textContent = q.track || q.category;

  document.getElementById('problemPointsBadge').textContent = `⭐ ${q.points} pts`;

  // Language badge in editor header
  const langBadge = document.getElementById('editorLangBadge');
  if (langBadge) {
    langBadge.textContent = isSql ? 'MySQL 8.0' : 'C++17';
  }

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

  // Custom Input
  const customInputEl = document.getElementById('customInput');
  if (customInputEl) {
    customInputEl.placeholder = isSql 
      ? 'Enter custom SQL query (e.g. SELECT * FROM student;) or leave empty to test editor solution...'
      : 'Enter your custom testcase stdin input here...';
    customInputEl.value = isSql ? '' : q.sampleInput;
  }

  // If CodeMirror is already mounted, update value & mode
  if (cmEditor) {
    const savedCode = localStorage.getItem(`code_${q.id}`);
    cmEditor.setValue(savedCode || boilerplate);
    cmEditor.setOption('mode', isSql ? 'text/x-mysql' : 'text/x-c++src');
    cmEditor.clearHistory();
  }
}

// ─── CodeMirror Initialization ──────────────────────────────────

function setupCodeMirror() {
  const textarea = document.getElementById('codeEditor');
  const isSql = currentQuestion && currentQuestion.type === 'sql';
  const savedCode = currentQuestion ? localStorage.getItem(`code_${currentQuestion.id}`) : null;
  textarea.value = savedCode || boilerplate;

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

    cmEditor.on('change', () => {
      textarea.value = cmEditor.getValue();
      if (currentQuestion) {
        localStorage.setItem(`code_${currentQuestion.id}`, textarea.value);
      }
    });

    // Auto-hints on input
    cmEditor.on('inputRead', (cm, change) => {
      if (change.origin === '+input' && change.text && change.text[0]) {
        if (/[a-zA-Z_]/.test(change.text[0])) {
          if (CodeMirror.hint && CodeMirror.hint.codearena) {
            cm.showHint({ hint: CodeMirror.hint.codearena, completeSingle: false });
          }
        }
      }
    });

    setTimeout(() => cmEditor.refresh(), 100);
  }

  // Reset button
  document.getElementById('resetBtn').addEventListener('click', () => {
    if (confirm('Reset code to original starter template?')) {
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
  if (cmEditor) return cmEditor.getValue();
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

// ─── Left Panel Tabs ───────────────────────────────────────────

function setupPanelTabs() {
  document.querySelectorAll('.panel-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('#leftPanel .tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tab.dataset.tab + 'Tab').classList.add('active');
    });
  });
}

// ─── Bottom Drawer Tabs (Testcase & Test Result) ────────────────

function setupDrawerTabs() {
  document.querySelectorAll('.test-drawer-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.test-drawer-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.drawer-pane').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');

      if (tab.dataset.drawer === 'testcase') {
        document.getElementById('paneTestcase').classList.add('active');
      } else {
        document.getElementById('paneResult').classList.add('active');
      }
    });
  });
}

function switchToResultDrawer() {
  document.querySelectorAll('.test-drawer-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.drawer-pane').forEach(p => p.classList.remove('active'));
  document.querySelector('.tab-result').classList.add('active');
  document.getElementById('paneResult').classList.add('active');
}

// ─── Run & Submit Actions ───────────────────────────────────────

function setupActions() {
  document.getElementById('runBtn').addEventListener('click', runCode);
  document.getElementById('submitBtn').addEventListener('click', submitCode);
}

async function runCode() {
  const isSql = currentQuestion && currentQuestion.type === 'sql';
  const customQuery = document.getElementById('customInput').value.trim();
  const editorCode = getEditorCode();
  const code = (isSql && customQuery) ? customQuery : editorCode;
  const input = document.getElementById('customInput').value;
  const btn = document.getElementById('runBtn');

  // Switch to result tab and show running state
  switchToResultDrawer();
  document.getElementById('emptyResultMsg').style.display = 'none';
  const consoleEl = document.getElementById('consoleOutput');
  consoleEl.style.display = 'block';
  consoleEl.textContent = 'Running testcase...';

  btn.disabled = true;

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
      output = `❌ Error:\n${result.error}`;
    } else {
      output = `Output:\n${result.output}`;
      if (result.error) {
        output += `\nStderr:\n${result.error}`;
      }
    }
    consoleEl.textContent = output;
  } catch (err) {
    consoleEl.textContent = `Execution fault: ${err.message}`;
  } finally {
    btn.disabled = false;
  }
}

async function submitCode() {
  const code = getEditorCode();
  const btn = document.getElementById('submitBtn');

  btn.disabled = true;
  btn.textContent = 'Judging...';

  try {
    const res = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, questionId: currentQuestion.id })
    });
    const result = await res.json();
    renderJudgementResults(result);

    // Switch to Judgement tab on the left panel
    document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('#leftPanel .tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector('[data-tab="submissions"]').classList.add('active');
    document.getElementById('submissionsTab').classList.add('active');

    if (result.status === 'Accepted') {
      localStorage.setItem(`solved_${currentQuestion.id}`, 'true');
    }
  } catch (err) {
    alert(`Submission error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span>☁ Submit</span>';
  }
}

function renderJudgementResults(result) {
  const container = document.getElementById('resultsContainer');
  const isAccepted = result.status === 'Accepted';

  let html = `
    <div class="judgement-status">
      <div class="status-badge ${isAccepted ? 'accepted' : 'failed'}">
        <span>${isAccepted ? '✓' : '✗'}</span>
        <span>${result.status}</span>
      </div>
      <div style="font-size: 13px; color: var(--text-secondary);">
        <strong style="color: var(--lc-orange);">${result.points}</strong> / ${currentQuestion.points} PTS
        &nbsp;•&nbsp;
        ${result.passed}/${result.total} test cases passed
      </div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 8px;">
  `;

  result.results.forEach((tc) => {
    const icon = tc.passed ? '✓' : '✗';
    const iconClass = tc.passed ? 'diff-easy' : 'diff-hard';

    html += `
      <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 12px 14px; font-size: 13px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
          <span style="font-weight: 600;">
            <span class="${iconClass}" style="margin-right: 6px;">${icon}</span>
            Case ${tc.testCaseId}${tc.description ? ' — ' + tc.description : ''}
          </span>
          <span class="difficulty-pill ${tc.passed ? 'easy' : 'hard'}">${tc.passed ? 'Passed' : 'Failed'}</span>
        </div>
    `;

    if (tc.compilationError) {
      html += `
        <div style="margin-top: 6px; color: var(--red); font-family: 'JetBrains Mono', monospace; font-size: 12px; white-space: pre-wrap;">
          ${escapeHtml(tc.compilationError)}
        </div>
      `;
    }

    if (tc.expectedOutput) {
      html += `
        <div style="margin-top: 6px; font-size: 12px; color: var(--text-secondary);">
          Expected: <pre style="background: #1a1a1a; padding: 6px; border-radius: 4px; margin-top: 2px;">${escapeHtml(tc.expectedOutput)}</pre>
        </div>
      `;
    }

    if (tc.actualOutput) {
      html += `
        <div style="margin-top: 6px; font-size: 12px; color: ${tc.passed ? 'var(--text-secondary)' : 'var(--red)'};">
          Your Output: <pre style="background: #1a1a1a; padding: 6px; border-radius: 4px; margin-top: 2px;">${escapeHtml(tc.actualOutput)}</pre>
        </div>
      `;
    }

    html += `</div>`;
  });

  html += `</div>`;
  container.innerHTML = html;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
