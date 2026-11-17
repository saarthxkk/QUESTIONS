// ═══════════════════════════════════════════════════════════════
// CodeArena — Main Page (Question List)
// ═══════════════════════════════════════════════════════════════

let allQuestions = [];
let activeFilter = 'all';
let activeCategory = 'all';

document.addEventListener('DOMContentLoaded', async () => {
  await loadQuestions();
  setupFilters();
});

async function loadQuestions() {
  try {
    const res = await fetch('/api/questions');
    allQuestions = await res.json();
    updateStats();
    populateCategories();
    renderQuestions();
  } catch (err) {
    console.error('Failed to load questions:', err);
  }
}

function updateStats() {
  document.getElementById('totalQ').textContent = allQuestions.length;
  document.getElementById('easyQ').textContent = allQuestions.filter(q => q.difficulty === 'Easy').length;
  document.getElementById('medQ').textContent = allQuestions.filter(q => q.difficulty === 'Medium').length;
  document.getElementById('hardQ').textContent = allQuestions.filter(q => q.difficulty === 'Hard').length;
}

function populateCategories() {
  const categories = [...new Set(allQuestions.map(q => q.category))];
  const select = document.getElementById('categoryFilter');
  categories.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    select.appendChild(opt);
  });
}

function setupFilters() {
  // Difficulty filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeFilter = btn.dataset.filter;
      renderQuestions();
    });
  });

  // Category select
  document.getElementById('categoryFilter').addEventListener('change', (e) => {
    activeCategory = e.target.value;
    renderQuestions();
  });
}

function renderQuestions() {
  const container = document.getElementById('questionList');
  
  let filtered = allQuestions;

  if (activeFilter !== 'all') {
    filtered = filtered.filter(q => q.difficulty === activeFilter);
  }

  if (activeCategory !== 'all') {
    filtered = filtered.filter(q => q.category === activeCategory);
  }

  if (filtered.length === 0) {
    container.innerHTML = '<div class="empty-row">No problems found. Start adding questions! 🚀</div>';
    return;
  }

  container.innerHTML = filtered.map(q => `
    <a class="question-row" href="/problem?id=${q.id}">
      <span class="col-status">${q.id}</span>
      <span class="col-title">${q.title}</span>
      <span class="col-category"><span class="category-tag ${q.category === 'SQL' ? 'cat-sql' : ''}">${q.category}</span></span>
      <span class="col-difficulty diff-${q.difficulty.toLowerCase()}">${q.difficulty}</span>
      <span class="col-points">${q.points} pts</span>
    </a>
  `).join('');
}

