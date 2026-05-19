const API_BASE = window.API_BASE || 'http://127.0.0.1:8000';

const classForm = document.getElementById('classForm');
const assignmentForm = document.getElementById('assignmentForm');
const submissionForm = document.getElementById('submissionForm');
const classList = document.getElementById('classList');
const assignmentList = document.getElementById('assignmentList');
const gradeList = document.getElementById('gradeList');
const classSelect = document.getElementById('classSelect');
const assignmentSelect = document.getElementById('assignmentSelect');
const classFilter = document.getElementById('classFilter');
const avgScore = document.getElementById('avgScore');

let classes = [];
let assignments = [];
let grades = [];

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || 'API error');
  }
  if (response.status === 204) return null;
  return response.json();
}

function findClassName(classId) {
  return classes.find((c) => c.id === classId)?.name ?? 'Không xác định';
}

function render() {
  classList.innerHTML = classes
    .map((c) => `<li><strong>${c.name}</strong> - ${c.subject}<button type="button" onclick="removeClass('${c.id}')">Xóa</button></li>`)
    .join('');

  classSelect.innerHTML = `<option value="">-- chọn lớp --</option>` + classes.map((c) => `<option value="${c.id}">${c.name}</option>`).join('');

  const classFilterValue = classFilter.value;
  classFilter.innerHTML = `<option value="">Tất cả lớp</option>` + classes.map((c) => `<option value="${c.id}">${c.name}</option>`).join('');
  classFilter.value = classFilterValue;

  assignmentList.innerHTML = assignments
    .map((a) => `<li>${a.title} - ${findClassName(a.classId)} (hạn: ${new Date(a.dueAt).toLocaleString('vi-VN')})<button type="button" onclick="removeAssignment('${a.id}')">Xóa</button></li>`)
    .join('');

  assignmentSelect.innerHTML = `<option value="">-- chọn bài --</option>` + assignments.map((a) => `<option value="${a.id}">${a.title}</option>`).join('');

  const filteredGrades = classFilter.value ? grades.filter((g) => g.classId === classFilter.value) : grades;
  gradeList.innerHTML = filteredGrades
    .map((g) => `<li>${g.studentName}: <strong>${g.score}</strong> điểm - ${(assignments.find((a) => a.id === g.assignmentId) || {}).title || ''}<button type="button" onclick="removeGrade('${g.id}')">Xóa</button></li>`)
    .join('');

  const avg = filteredGrades.length === 0 ? 0 : filteredGrades.reduce((sum, item) => sum + Number(item.score), 0) / filteredGrades.length;
  avgScore.textContent = `Điểm trung bình: ${avg.toFixed(2)} (${filteredGrades.length} bài)`;
}

async function loadAll() {
  classes = await api('/api/classes');
  assignments = await api('/api/assignments');
  const classId = classFilter.value;
  const gradeResp = await api(`/api/grades${classId ? `?class_id=${classId}` : ''}`);
  grades = gradeResp.items;
  render();
}

async function removeClass(classId) { await api(`/api/classes/${classId}`, { method: 'DELETE' }); await loadAll(); }
async function removeAssignment(id) { await api(`/api/assignments/${id}`, { method: 'DELETE' }); await loadAll(); }
async function removeGrade(id) { await api(`/api/grades/${id}`, { method: 'DELETE' }); await loadAll(); }
window.removeClass = removeClass;
window.removeAssignment = removeAssignment;
window.removeGrade = removeGrade;

classForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  await api('/api/classes', {
    method: 'POST',
    body: JSON.stringify({
      name: document.getElementById('className').value.trim(),
      subject: document.getElementById('subject').value.trim(),
    }),
  });
  classForm.reset();
  await loadAll();
});

assignmentForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  await api('/api/assignments', {
    method: 'POST',
    body: JSON.stringify({
      class_id: classSelect.value,
      title: document.getElementById('assignmentTitle').value.trim(),
      due_at: new Date(document.getElementById('dueAt').value).toISOString(),
    }),
  });
  assignmentForm.reset();
  await loadAll();
});

submissionForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  await api('/api/grades', {
    method: 'POST',
    body: JSON.stringify({
      assignment_id: assignmentSelect.value,
      student_name: document.getElementById('studentName').value.trim(),
      score: Number(document.getElementById('score').value),
    }),
  });
  submissionForm.reset();
  await loadAll();
});

classFilter.addEventListener('change', loadAll);

document.getElementById('seedDataBtn').addEventListener('click', async () => {
  await api('/api/seed', { method: 'POST' });
  await loadAll();
});

document.getElementById('clearDataBtn').addEventListener('click', async () => {
  if (!confirm('Bạn có chắc muốn xóa toàn bộ dữ liệu demo?')) return;
  await api('/api/reset', { method: 'DELETE' });
  await loadAll();
});

loadAll().catch((err) => {
  alert(`Không kết nối được API backend (${API_BASE}): ${err.message}`);
});
