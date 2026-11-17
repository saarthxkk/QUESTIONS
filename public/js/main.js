// ═══════════════════════════════════════════════════════════════
// CodeArena — Topic Explorer & Question Directory
// ═══════════════════════════════════════════════════════════════

let allQuestions = [];
let activeTrack = 'all';
let activeSubtopic = 'all';
let activeDifficulty = 'all';
let searchQuery = '';

document.addEventListener('DOMContentLoaded', async () => {
  // Check if URL has a track parameter (e.g. ?track=SQL)
  const urlParams = new URLSearchParams(window.location.search);
  const trackParam = urlParams.get('track');
  if (trackParam) {
    activeTrack = trackParam;
  }

  await loadQuestions();
  setupTrackCards();
  setupDifficultyFilters();
  setupSearch();
});

async function loadQuestions() {
  try {
    const res = await fetch('/api/questions');
    allQuestions = await res.json();
    
    updateTrackCounts();
    renderSubtopicChips();
    renderQuestions();
  } catch (err) {
    console.error('Failed to load questions:', err);
  }
}

function updateTrackCounts() {
  const total = allQuestions.length;
  const bstCount = allQuestions.filter(q => q.track === 'BST' || q.category === 'Trees').length;
  const avlCount = allQuestions.filter(q => q.track === 'AVL Trees' || q.category === 'AVL Trees').length;
  const sqlCount = allQuestions.filter(q => q.track === 'SQL' || q.category === 'SQL').length;

  document.getElementById('countAll').textContent = `${total} Qs`;
  document.getElementById('countBST').textContent = `${bstCount} Qs`;
  document.getElementById('countAVL').textContent = `${avlCount} Qs`;
  document.getElementById('countSQL').textContent = `${sqlCount} Qs`;

  const totalPoints = allQuestions.reduce((s, q) => s + (q.points || 0), 0);
  document.getElementById('totalScore').textContent = `${totalPoints} PTS TOTAL`;
}

// ─── Setup Track Cards ──────────────────────────────────────────

function setupTrackCards() {
  const cards = document.querySelectorAll('.track-card');
  cards.forEach(card => {
    if (card.dataset.track === activeTrack) {
      cards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
    }

    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      activeTrack = card.dataset.track;
      activeSubtopic = 'all'; // Reset subtopic when track changes
      renderSubtopicChips();
      renderQuestions();
    });
  });
}

// ─── Sub-Topic Chips (Dynamic per Track) ─────────────────────────

function renderSubtopicChips() {
  const container = document.getElementById('subtopicChips');
  const trackTitleEl = document.getElementById('activeTrackName');

  // Filter questions for the selected track
  let trackQuestions = allQuestions;
  if (activeTrack !== 'all') {
    trackQuestions = allQuestions.filter(q => q.track === activeTrack || q.category === activeTrack);
  }

  const trackLabels = {
    'all': 'All Tracks',
    'BST': 'Binary Search Trees (BST)',
    'AVL Trees': 'AVL Self-Balancing Trees',
    'SQL': 'SQL Database Intelligence'
  };
  trackTitleEl.textContent = `(${trackLabels[activeTrack] || activeTrack})`;

  // Extract distinct subtopics
  const subtopics = [...new Set(trackQuestions.map(q => q.subtopic).filter(Boolean))];

  let html = `
    <button class="subtopic-chip ${activeSubtopic === 'all' ? 'active' : ''}" data-sub="all">
      All ${activeTrack === 'all' ? 'Topics' : activeTrack} (${trackQuestions.length})
    </button>
  `;

  subtopics.forEach(sub => {
    const count = trackQuestions.filter(q => q.subtopic === sub).length;
    html += `
      <button class="subtopic-chip ${activeSubtopic === sub ? 'active' : ''}" data-sub="${sub}">
        ${sub} (${count})
      </button>
    `;
  });

  container.innerHTML = html;

  // Bind clicks
  container.querySelectorAll('.subtopic-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      container.querySelectorAll('.subtopic-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeSubtopic = chip.dataset.sub;
      renderQuestions();
    });
  });
}

// ─── Setup Difficulty Filters & Search ──────────────────────────

function setupDifficultyFilters() {
  document.querySelectorAll('.diff-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.diff-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeDifficulty = btn.dataset.filter;
      renderQuestions();
    });
  });
}

function setupSearch() {
  const searchEl = document.getElementById('searchInput');
  searchEl.addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderQuestions();
  });
}

// ─── Render Questions Table ─────────────────────────────────────

function renderQuestions() {
  const container = document.getElementById('questionList');
  
  let filtered = allQuestions;

  // 1. Filter by Track
  if (activeTrack !== 'all') {
    filtered = filtered.filter(q => q.track === activeTrack || q.category === activeTrack);
  }

  // 2. Filter by Subtopic
  if (activeSubtopic !== 'all') {
    filtered = filtered.filter(q => q.subtopic === activeSubtopic);
  }

  // 3. Filter by Difficulty
  if (activeDifficulty !== 'all') {
    filtered = filtered.filter(q => q.difficulty === activeDifficulty);
  }

  // 4. Search Filter
  if (searchQuery) {
    filtered = filtered.filter(q => {
      const matchTitle = q.title.toLowerCase().includes(searchQuery);
      const matchSub = (q.subtopic || '').toLowerCase().includes(searchQuery);
      const matchTags = (q.tags || []).some(t => t.toLowerCase().includes(searchQuery));
      return matchTitle || matchSub || matchTags;
    });
  }

  if (filtered.length === 0) {
    container.innerHTML = '<div class="empty-row">No problems match the selected track and filters. Try adjusting your filters.</div>';
    return;
  }

  container.innerHTML = filtered.map(q => {
    const diffClass = q.difficulty.toLowerCase();
    const isSolved = localStorage.getItem(`solved_${q.id}`) === 'true';

    return `
      <a class="question-row" href="/problem?id=${q.id}&track=${encodeURIComponent(q.track || q.category)}">
        <span class="col-id">${q.id}</span>
        <span class="col-title">${q.title}</span>
        <span class="col-subtopic"><span class="subtopic-tag">${q.subtopic || q.category}</span></span>
        <span class="col-diff"><span class="difficulty-pill ${diffClass}">${q.difficulty}</span></span>
        <span class="col-points">${q.points} pts</span>
        <span class="col-action">Solve ▶</span>
      </a>
    `;
  }).join('');
}
