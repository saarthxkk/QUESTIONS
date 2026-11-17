// ═══════════════════════════════════════════════════════════════
// CodeArena — LeetCode-style Problem Workspace
// Pixel-accurate LeetCode workspace matching uploaded screenshot
// ═══════════════════════════════════════════════════════════════

let allQuestions = [];
let currentQuestion = null;
let boilerplate = '';
let cmEditor = null;
let currentTrack = 'all';
let activeCaseIdx = 0;
let lastRunResults = null;
let timerSeconds = 0;
let timerInterval = null;

document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  const id = parseInt(params.get('id'));
  currentTrack = params.get('track') || 'all';

  if (!id) {
    window.location.href = '/';
    return;
  }

  // Load all questions list for next/prev/random navigation
  await loadQuestionDirectory();

  // Load active question
  await loadProblem(id);

  setupCodeMirror();
  setupResizers();
  setupPanelTabs();
  setupDrawerTabs();
  setupNavigators();
  setupLeftFooter();
  setupPracticeTimer();
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
  const randomBtn = document.getElementById('randomProblemBtn');
  const backLink = document.getElementById('backToProblemList');

  // Back link preserves track
  if (currentTrack && currentTrack !== 'all') {
    backLink.href = `/?track=${encodeURIComponent(currentTrack)}`;
  } else {
    backLink.href = '/';
  }

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

  if (randomBtn) {
    randomBtn.onclick = () => {
      if (pool.length > 1) {
        let randIdx = Math.floor(Math.random() * pool.length);
        if (pool[randIdx].id === (currentQuestion ? currentQuestion.id : -1)) {
          randIdx = (randIdx + 1) % pool.length;
        }
        window.location.href = `/problem?id=${pool[randIdx].id}&track=${encodeURIComponent(currentTrack)}`;
      }
    };
  }
}

// ─── Practice Timer in Top Bar ──────────────────────────────────

function setupPracticeTimer() {
  const timerEl = document.getElementById('navTimer');
  if (!timerEl) return;

  timerSeconds = 0;
  if (timerInterval) clearInterval(timerInterval);

  timerInterval = setInterval(() => {
    timerSeconds++;
    const mins = String(Math.floor(timerSeconds / 60)).padStart(2, '0');
    const secs = String(timerSeconds % 60).padStart(2, '0');
    timerEl.innerHTML = `<span>⏱️</span> <span>${mins}:${secs}</span>`;
  }, 1000);
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

  // Top Title
  document.title = `${q.id}. ${q.title} — CodeArena`;

  // Left Pane Header Title
  document.getElementById('problemTitle').textContent = `${q.id}. ${q.title}`;

  // Check Solved Status
  const isSolved = localStorage.getItem(`solved_${q.id}`) === 'true';
  const solvedBadge = document.getElementById('solvedBadge');
  if (solvedBadge) {
    solvedBadge.style.display = isSolved ? 'inline-flex' : 'none';
  }

  // Difficulty Pill
  const diffPill = document.getElementById('problemDifficulty');
  diffPill.textContent = q.difficulty;
  diffPill.className = `difficulty-pill ${diffClass}`;

  // Meta Pills
  const topicPill = document.getElementById('problemTopic');
  topicPill.querySelector('span:last-child').textContent = q.subtopic || q.category;

  const catPill = document.getElementById('problemCategory');
  catPill.querySelector('span:last-child').textContent = q.track || q.category;

  document.getElementById('problemPointsBadge').textContent = `⭐ ${q.points} pts`;

  // Language selector badge in editor header
  const langBadge = document.getElementById('editorLangBadge');
  if (langBadge) {
    langBadge.textContent = isSql ? 'MySQL 8.0 ▾' : 'C++17 ▾';
  }

  // Description (Markdown)
  const descEl = document.getElementById('problemDescription');
  if (typeof marked !== 'undefined') {
    descEl.innerHTML = marked.parse(q.description);
  } else {
    descEl.textContent = q.description;
  }

  // Render LeetCode-style Examples
  renderExamplesSection(q);

  // Render Editorial & Solutions content
  renderEditorialAndSolutions(q);

  // Boilerplate
  boilerplate = q.boilerplate || '';

  // Setup Testcase Case Tabs (Case 1, Case 2, Case 3)
  setupCaseTabs(q);

  // If CodeMirror is already mounted, update value & mode
  if (cmEditor) {
    const savedCode = localStorage.getItem(`code_${q.id}`);
    cmEditor.setValue(savedCode || boilerplate);
    cmEditor.setOption('mode', isSql ? 'text/x-mysql' : 'text/x-c++src');
    cmEditor.clearHistory();
    updateCursorPos();
  }
}

// ─── LeetCode Example Cards (Exact Screenshot Structure) ────────

function renderExamplesSection(q) {
  const container = document.getElementById('exampleSection');
  if (!container) return;

  const langLabel = q.type === 'sql' ? 'SQL' : 'C++';
  let html = '';

  // Primary Example 1 from sampleInput / sampleOutput
  html += `
    <div class="example-card">
      <div class="example-card-header">
        <span class="example-title">Example 1:</span>
        <div class="example-lang-toggles">
          <span class="example-toggle-pill active">Original</span>
          <span class="example-toggle-pill">${langLabel}</span>
        </div>
      </div>
      <div class="example-field">
        <span class="field-label">Input:</span>
        <div class="field-code">${escapeHtml(q.sampleInput || '(Standard table query)')}</div>
      </div>
      <div class="example-field">
        <span class="field-label">Output:</span>
        <div class="field-code">${escapeHtml(q.sampleOutput || '')}</div>
      </div>
      <div class="example-field">
        <span class="field-label">Explanation:</span>
        <div class="field-text">The output reflects the verified records adhering to the exact constraint predicates and ordering criteria.</div>
      </div>
    </div>
  `;

  // If multiple test cases exist, render Example 2
  if (q.testCases && q.testCases.length > 1) {
    const tc2 = q.testCases[1];
    html += `
      <div class="example-card">
        <div class="example-card-header">
          <span class="example-title">Example 2:</span>
        </div>
        <div class="example-field">
          <span class="field-label">Input:</span>
          <div class="field-code">${escapeHtml(tc2.input || tc2.description || 'Test case verification')}</div>
        </div>
        <div class="example-field">
          <span class="field-label">Output:</span>
          <div class="field-code">${escapeHtml(tc2.expectedOutput || '')}</div>
        </div>
      </div>
    `;
  }

  container.innerHTML = html;
}

// ─── Editorial & Reference Solutions ────────────────────────────

function renderEditorialAndSolutions(q) {
  const editorialEl = document.getElementById('editorialText');
  const solutionsEl = document.getElementById('solutionsText');
  const isSql = q.type === 'sql';

  if (editorialEl) {
    if (isSql) {
      editorialEl.innerHTML = `
        <div style="font-size: 13px; line-height: 1.6; color: var(--text-primary);">
          <h4 style="color: var(--lc-orange); margin-bottom: 8px;">Approach & Key SQL Principles</h4>
          <p style="margin-bottom: 10px;">
            This problem validates advanced relational algebra: proper join conditions, aggregate filtering with <code>HAVING</code>,
            conditional evaluation using <code>CASE WHEN</code>, and deterministic sorting.
          </p>
          <ul style="padding-left: 20px; margin-bottom: 12px; color: var(--text-secondary);">
            <li><strong>Filtering order:</strong> Filter row-level criteria before aggregation using <code>WHERE</code> clauses.</li>
            <li><strong>Group Aggregation:</strong> Every non-aggregated attribute in the <code>SELECT</code> must appear in the <code>GROUP BY</code>.</li>
            <li><strong>NULL Safety:</strong> Wrap nullable fields in <code>COALESCE(SUM(...), 0)</code> when performing outer joins.</li>
          </ul>
        </div>
      `;
    } else {
      editorialEl.innerHTML = `
        <div style="font-size: 13px; line-height: 1.6; color: var(--text-primary);">
          <h4 style="color: var(--lc-orange); margin-bottom: 8px;">Intuition & Complexity Analysis</h4>
          <p style="margin-bottom: 10px;">
            Apply recursive tree traversal or pointer restructuring to preserve tree properties in \(O(h)\) height time complexity.
          </p>
          <div style="background: #242424; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-top: 8px;">
            Time Complexity: O(N) or O(log N)<br>
            Space Complexity: O(H) recursion stack
          </div>
        </div>
      `;
    }
  }

  if (solutionsEl) {
    solutionsEl.innerHTML = `
      <div style="background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <strong style="color: var(--green);">Optimal Approach (${isSql ? 'MySQL' : 'C++17'})</strong>
          <span style="font-size: 11px; color: var(--text-muted);">Runtime: 100% Beats</span>
        </div>
        <pre style="background: #1a1a1a; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #eff1f6; white-space: pre-wrap; overflow-x: auto;">${escapeHtml(q.sampleOutput ? '-- Refer to sample output structure\n-- Run your query to compare against the validation suite' : '')}</pre>
      </div>
    `;
  }
}

// ─── Setup Case Tabs in Testcase Drawer ──────────────────────────

function setupCaseTabs(q) {
  const tabsBar = document.getElementById('caseTabsBar');
  const customInputEl = document.getElementById('customInput');
  if (!tabsBar) return;

  const cases = (q.testCases && q.testCases.length > 0) 
    ? q.testCases 
    : [{ input: q.sampleInput || '' }];

  tabsBar.innerHTML = '';
  activeCaseIdx = 0;

  cases.slice(0, 3).forEach((tc, idx) => {
    const chip = document.createElement('button');
    chip.className = `case-chip ${idx === 0 ? 'active' : ''}`;
    chip.textContent = `Case ${idx + 1}`;
    chip.onclick = () => {
      document.querySelectorAll('.case-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCaseIdx = idx;
      if (customInputEl) {
        customInputEl.value = tc.input || '';
      }
    };
    tabsBar.appendChild(chip);
  });

  if (customInputEl) {
    customInputEl.value = cases[0].input || (q.type === 'sql' ? '' : q.sampleInput);
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

    // Auto-save & Status indicator
    const savedStatus = document.getElementById('savedStatus');
    let saveTimeout = null;

    cmEditor.on('change', () => {
      textarea.value = cmEditor.getValue();
      if (savedStatus) savedStatus.textContent = 'Saving...';

      if (saveTimeout) clearTimeout(saveTimeout);
      saveTimeout = setTimeout(() => {
        if (currentQuestion) {
          localStorage.setItem(`code_${currentQuestion.id}`, textarea.value);
        }
        if (savedStatus) savedStatus.textContent = 'Saved';
      }, 400);
    });

    // Cursor position indicator (Ln 1, Col 1)
    cmEditor.on('cursorActivity', updateCursorPos);

    // Auto-hints on typing
    cmEditor.on('inputRead', (cm, change) => {
      if (change.origin === '+input' && change.text && change.text[0]) {
        if (/[a-zA-Z_]/.test(change.text[0])) {
          if (CodeMirror.hint && CodeMirror.hint.codearena) {
            cm.showHint({ hint: CodeMirror.hint.codearena, completeSingle: false });
          }
        }
      }
    });

    setTimeout(() => {
      cmEditor.refresh();
      updateCursorPos();
    }, 100);
  }

  // Format Code button
  const formatBtn = document.getElementById('formatBtn');
  if (formatBtn) {
    formatBtn.addEventListener('click', () => {
      if (cmEditor) {
        const totalLines = cmEditor.lineCount();
        for (let i = 0; i < totalLines; i++) {
          cmEditor.indentLine(i, 'smart');
        }
      }
    });
  }

  // Bookmark button
  const bookmarkBtn = document.getElementById('bookmarkBtn');
  if (bookmarkBtn) {
    bookmarkBtn.addEventListener('click', () => {
      if (!currentQuestion) return;
      const key = `bookmarked_${currentQuestion.id}`;
      const isBookmarked = localStorage.getItem(key) === 'true';
      if (isBookmarked) {
        localStorage.removeItem(key);
        bookmarkBtn.style.color = 'var(--text-secondary)';
      } else {
        localStorage.setItem(key, 'true');
        bookmarkBtn.style.color = 'var(--lc-orange)';
      }
    });
  }

  // Reset button
  const resetBtn = document.getElementById('resetBtn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
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
}

function updateCursorPos() {
  const el = document.getElementById('cursorPos');
  if (!el || !cmEditor) return;
  const cursor = cmEditor.getCursor();
  el.textContent = `Ln ${cursor.line + 1}, Col ${cursor.ch + 1}`;
}

function getEditorCode() {
  if (cmEditor) return cmEditor.getValue();
  return document.getElementById('codeEditor').value;
}

// ─── Resizers (Vertical & Horizontal) ───────────────────────────

function setupResizers() {
  // Vertical split resizer (Left panel vs Right panel)
  const resizerV = document.getElementById('resizer');
  const leftPanel = document.getElementById('leftPanel');
  let isResizingV = false;

  if (resizerV && leftPanel) {
    resizerV.addEventListener('mousedown', () => {
      isResizingV = true;
      resizerV.classList.add('active');
      document.body.style.cursor = 'col-resize';
      document.body.style.userSelect = 'none';
    });

    document.addEventListener('mousemove', (e) => {
      if (!isResizingV) return;
      const containerWidth = document.querySelector('.split-layout').offsetWidth;
      const newWidth = (e.clientX / containerWidth) * 100;
      if (newWidth > 20 && newWidth < 80) {
        leftPanel.style.width = newWidth + '%';
        if (cmEditor) cmEditor.refresh();
      }
    });

    document.addEventListener('mouseup', () => {
      if (isResizingV) {
        isResizingV = false;
        resizerV.classList.remove('active');
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
        if (cmEditor) cmEditor.refresh();
      }
    });
  }

  // Horizontal resizer (Code Editor vs Test Drawer)
  const resizerH = document.getElementById('resizerH');
  const testDrawer = document.getElementById('testDrawer');
  let isResizingH = false;

  if (resizerH && testDrawer) {
    resizerH.addEventListener('mousedown', (e) => {
      isResizingH = true;
      resizerH.classList.add('active');
      document.body.style.cursor = 'row-resize';
      document.body.style.userSelect = 'none';
    });

    document.addEventListener('mousemove', (e) => {
      if (!isResizingH) return;
      const rightPanel = document.getElementById('rightPanel');
      const rightRect = rightPanel.getBoundingClientRect();
      const newHeight = rightRect.bottom - e.clientY;
      if (newHeight >= 60 && newHeight <= rightRect.height - 120) {
        testDrawer.style.height = newHeight + 'px';
        if (cmEditor) cmEditor.refresh();
      }
    });

    document.addEventListener('mouseup', () => {
      if (isResizingH) {
        isResizingH = false;
        resizerH.classList.remove('active');
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
        if (cmEditor) cmEditor.refresh();
      }
    });
  }
}

// ─── Left Panel Tabs ───────────────────────────────────────────

function setupPanelTabs() {
  document.querySelectorAll('.panel-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('#leftPanel .tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      const target = document.getElementById(tab.dataset.tab + 'Tab');
      if (target) target.classList.add('active');
    });
  });

  // Expand / Collapse buttons
  const expandBtn = document.getElementById('leftExpandBtn');
  const collapseBtn = document.getElementById('leftCollapseBtn');
  const leftPanel = document.getElementById('leftPanel');

  if (expandBtn && leftPanel) {
    expandBtn.onclick = () => {
      leftPanel.style.width = (leftPanel.style.width === '75%') ? '48%' : '75%';
      if (cmEditor) cmEditor.refresh();
    };
  }

  if (collapseBtn && leftPanel) {
    collapseBtn.onclick = () => {
      leftPanel.style.width = (leftPanel.style.width === '25%') ? '48%' : '25%';
      if (cmEditor) cmEditor.refresh();
    };
  }
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

  const drawerCollapseBtn = document.getElementById('drawerCollapseBtn');
  const testDrawer = document.getElementById('testDrawer');
  if (drawerCollapseBtn && testDrawer) {
    drawerCollapseBtn.onclick = () => {
      if (testDrawer.style.height === '40px') {
        testDrawer.style.height = '220px';
      } else {
        testDrawer.style.height = '40px';
      }
      if (cmEditor) cmEditor.refresh();
    };
  }
}

function switchToResultDrawer() {
  document.querySelectorAll('.test-drawer-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.drawer-pane').forEach(p => p.classList.remove('active'));
  document.querySelector('.tab-result').classList.add('active');
  document.getElementById('paneResult').classList.add('active');
}

// ─── Left Footer Actions (Likes, Stars, Online Ticker) ──────────

function setupLeftFooter() {
  const likeBtn = document.getElementById('likeBtn');
  const dislikeBtn = document.getElementById('dislikeBtn');
  const starBtn = document.getElementById('starBtn');
  const onlineCount = document.getElementById('onlineCount');

  if (likeBtn) {
    likeBtn.onclick = () => {
      likeBtn.classList.toggle('active');
      if (dislikeBtn) dislikeBtn.classList.remove('active');
    };
  }

  if (dislikeBtn) {
    dislikeBtn.onclick = () => {
      dislikeBtn.classList.toggle('active');
      if (likeBtn) likeBtn.classList.remove('active');
    };
  }

  if (starBtn) {
    starBtn.onclick = () => {
      starBtn.classList.toggle('active');
    };
  }

  // Live online users jitter (800 - 815)
  if (onlineCount) {
    setInterval(() => {
      const delta = Math.floor(Math.random() * 5) - 2;
      const current = parseInt(onlineCount.textContent) || 804;
      const next = Math.max(790, Math.min(840, current + delta));
      onlineCount.textContent = `${next} Online`;
    }, 8000);
  }
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

  const wrapper = document.getElementById('testResultWrapper');
  wrapper.style.display = 'flex';
  document.getElementById('resultStatusPill').className = 'result-status-pill';
  document.getElementById('resultStatusPill').textContent = 'Running...';
  document.getElementById('resultRuntime').textContent = 'Runtime: calculating...';
  document.getElementById('resultCaseTabs').innerHTML = '';
  document.getElementById('resultCaseDetails').innerHTML = '<div style="color: var(--text-secondary); font-size: 12px;">Executing code in sandboxed engine...</div>';

  btn.disabled = true;
  const startTime = performance.now();

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
    const duration = Math.round(performance.now() - startTime);

    renderRunResult(result, duration);
  } catch (err) {
    document.getElementById('resultStatusPill').className = 'result-status-pill wrong-answer';
    document.getElementById('resultStatusPill').textContent = 'Execution Error';
    document.getElementById('resultCaseDetails').innerHTML = `<div class="result-box" style="color: var(--red);">${escapeHtml(err.message)}</div>`;
  } finally {
    btn.disabled = false;
  }
}

function renderRunResult(result, duration) {
  const statusPill = document.getElementById('resultStatusPill');
  const runtimeEl = document.getElementById('resultRuntime');
  const detailsEl = document.getElementById('resultCaseDetails');

  runtimeEl.textContent = `Runtime: ${duration} ms`;

  if (result.compilationError) {
    statusPill.className = 'result-status-pill wrong-answer';
    statusPill.textContent = 'Compilation / SQL Error';
    detailsEl.innerHTML = `<div class="result-box" style="color: var(--red);">${escapeHtml(result.compilationError)}</div>`;
    return;
  }

  if (result.timeout) {
    statusPill.className = 'result-status-pill wrong-answer';
    statusPill.textContent = 'Time Limit Exceeded';
    detailsEl.innerHTML = `<div class="result-box" style="color: var(--red);">Process execution timed out (> 5.0 seconds).</div>`;
    return;
  }

  if (result.error && !result.success) {
    statusPill.className = 'result-status-pill wrong-answer';
    statusPill.textContent = 'Runtime Error';
    detailsEl.innerHTML = `<div class="result-box" style="color: var(--red);">${escapeHtml(result.error)}</div>`;
    return;
  }

  statusPill.className = 'result-status-pill accepted';
  statusPill.textContent = 'Output Generated';

  let html = `
    <div>
      <div class="result-box-label">Output</div>
      <div class="result-box">${escapeHtml(result.output || '(No stdout produced)')}</div>
    </div>
  `;

  if (result.error) {
    html += `
      <div>
        <div class="result-box-label" style="color: var(--yellow);">Standard Error / Warnings</div>
        <div class="result-box">${escapeHtml(result.error)}</div>
      </div>
    `;
  }

  detailsEl.innerHTML = html;
}

async function submitCode() {
  const code = getEditorCode();
  const btn = document.getElementById('submitBtn');

  btn.disabled = true;
  btn.innerHTML = '<span>Judging...</span>';

  try {
    const res = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, questionId: currentQuestion.id })
    });
    const result = await res.json();
    renderJudgementResults(result);

    // Switch to Submissions tab on the left panel
    document.querySelectorAll('.panel-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('#leftPanel .tab-content').forEach(c => c.classList.remove('active'));
    document.querySelector('[data-tab="submissions"]').classList.add('active');
    document.getElementById('submissionsTab').classList.add('active');

    if (result.status === 'Accepted') {
      localStorage.setItem(`solved_${currentQuestion.id}`, 'true');
      const solvedBadge = document.getElementById('solvedBadge');
      if (solvedBadge) solvedBadge.style.display = 'inline-flex';
    }
  } catch (err) {
    alert(`Submission error: ${err.message}`);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V10.4a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V10.4a.5.5 0 0 1 .5-.5z"/><path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V10.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/></svg>
      <span>Submit</span>
    `;
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
  if (str === null || str === undefined) return '';
  const div = document.createElement('div');
  div.textContent = String(str);
  return div.innerHTML;
}
