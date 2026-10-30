/* ══════════════════════════════════════════════════════════════════════
   MASTER CALIBRATION & SETTINGS LOGIC (settings.js)
══════════════════════════════════════════════════════════════════════ */

let settingsState = {
  orders: [],
  baselines: [],
  teams: [],
  filterStatus: 'all', // 'all', 'active', 'inactive'
  searchQuery: '',
  pendingOrderChanges: {}, // orderId -> boolean
  pendingBaselineChanges: {}, // ptId -> { easy, hard }
  pendingTeamChanges: {} // teamId -> count
};

document.addEventListener('DOMContentLoaded', () => {
  loadSettingsOverview();
  setupEventListeners();
});

function setupEventListeners() {
  const searchInput = document.getElementById('settings-order-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      settingsState.searchQuery = e.target.value.toLowerCase().trim();
      renderOrdersTable();
    });
  }
}

export async function loadSettingsOverview() {
  try {
    const res = await fetch('/api/settings/overview');
    if (!res.ok) throw new Error('Failed to load settings');
    const data = await res.json();

    settingsState.orders = data.orders || [];
    settingsState.baselines = data.baselines || [];
    settingsState.teams = data.teams || [];

    updateStatsBadge(data);
    renderOrdersTable();
    renderBaselinesTable();
    renderTeamsCards();
  } catch (err) {
    console.error('Error loading settings overview:', err);
    showToast('Tənzimləmələri yükləyərkən xəta baş verdi: ' + err.message, 'error');
  }
}

function updateStatsBadge(data) {
  const badgeEl = document.getElementById('settings-active-badge');
  if (badgeEl) {
    const activeCount = settingsState.orders.filter(o => 
      settingsState.pendingOrderChanges[o.orderId] !== undefined ? 
      settingsState.pendingOrderChanges[o.orderId] : o.isReservationActive
    ).length;
    badgeEl.textContent = `${activeCount} / ${settingsState.orders.length} Sifariş Xammal Bloklayır`;
  }
}

export function setOrderFilter(filter) {
  settingsState.filterStatus = filter;
  document.querySelectorAll('.settings-filter-pill').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === filter);
  });
  renderOrdersTable();
}

export function filterOrders() {
  return settingsState.orders.filter(o => {
    const isActive = settingsState.pendingOrderChanges[o.orderId] !== undefined ?
      settingsState.pendingOrderChanges[o.orderId] : o.isReservationActive;

    if (settingsState.filterStatus === 'active' && !isActive) return false;
    if (settingsState.filterStatus === 'inactive' && isActive) return false;

    if (settingsState.searchQuery) {
      const q = settingsState.searchQuery;
      const matchId = (o.orderId || '').toLowerCase().includes(q);
      const matchCust = (o.customerName || '').toLowerCase().includes(q);
      const matchProd = (o.productName || '').toLowerCase().includes(q);
      if (!matchId && !matchCust && !matchProd) return false;
    }
    return true;
  });
}

function renderOrdersTable() {
  const tbody = document.getElementById('settings-orders-tbody');
  if (!tbody) return;

  const filtered = filterOrders();
  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--t3);">Axtarışa uyğun sifariş tapılmadı</td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(o => {
    const isActive = settingsState.pendingOrderChanges[o.orderId] !== undefined ?
      settingsState.pendingOrderChanges[o.orderId] : o.isReservationActive;

    const remaining = Math.max(0, (o.quantity || 0) - (o.deliveredQuantity || 0));

    return `
      <tr style="${isActive ? '' : 'opacity:0.6; background:rgba(255,255,255,0.01);'}">
        <td style="width: 60px; text-align: center;">
          <label class="switch">
            <input type="checkbox" ${isActive ? 'checked' : ''} onchange="onOrderToggleChange('${o.orderId}', this.checked)">
            <span class="slider"></span>
          </label>
        </td>
        <td style="font-family:var(--font-mono); font-weight:600; color:var(--primary);">
          № ${o.orderId}
        </td>
        <td>
          <div style="font-weight:600; color:var(--t1);">${escapeHtml(o.customerName)}</div>
          <div style="font-size:11px; color:var(--t3);">${o.orderDate || 'Tarix yoxdur'}</div>
        </td>
        <td>
          <div style="font-size:12.5px; color:var(--t2);">${escapeHtml(o.productName)}</div>
          <span class="badge badge-neutral" style="font-size:10px;">${o.category || 'Workwear'}</span>
        </td>
        <td style="text-align:right; font-family:var(--font-mono);">
          <div>${o.quantity || 0} əd.</div>
          <div style="font-size:11px; color:var(--t3);">Təhvil: ${o.deliveredQuantity || 0} əd.</div>
        </td>
        <td style="text-align:right; font-family:var(--font-mono); font-weight:700; color:${remaining > 0 ? 'var(--warning)' : 'var(--success)'};">
          ${remaining} əd.
        </td>
        <td>
          <span class="badge ${isActive ? 'badge-blue' : 'badge-neutral'}">
            ${isActive ? 'Rezerv Edilib' : 'Deaktiv'}
          </span>
        </td>
      </tr>
    `;
  }).join('');
}

window.onOrderToggleChange = function(orderId, checked) {
  settingsState.pendingOrderChanges[orderId] = checked;
  updateStatsBadge();
  markUnsavedChanges();
};

window.bulkToggleAllOrders = function(enable) {
  settingsState.orders.forEach(o => {
    settingsState.pendingOrderChanges[o.orderId] = enable;
  });
  renderOrdersTable();
  updateStatsBadge();
  markUnsavedChanges();
};

function renderBaselinesTable() {
  const container = document.getElementById('settings-baselines-container');
  if (!container) return;

  const categories = ['Workwear', 'Underwear-boxer', 'Socks'];
  const catTitles = {
    'Workwear': 'İş Geyimi (Workwear - Bant 1)',
    'Underwear-boxer': 'Alt Geyim (Underwear - Bant 2)',
    'Socks': 'Corab İstehsalatı (Socks - Bant 3)'
  };

  container.innerHTML = categories.map(cat => {
    const catBaselines = settingsState.baselines.filter(b => (b.category || '').toLowerCase() === cat.toLowerCase());
    if (catBaselines.length === 0) return '';

    return `
      <div style="margin-bottom: 24px;">
        <div style="font-size:13.5px; font-weight:700; color:var(--primary); margin-bottom:10px; display:flex; align-items:center; gap:8px;">
          <span>${catTitles[cat] || cat}</span>
          <span class="badge badge-neutral">${catBaselines.length} məhsul növü</span>
        </div>
        <table class="table" style="background:var(--surface-2); border-radius:8px;">
          <thead>
            <tr>
              <th>Məhsul Növü</th>
              <th style="width: 160px; text-align: center;">Asan Norma (ədəd/gün)</th>
              <th style="width: 160px; text-align: center;">Çətin Norma (ədəd/gün)</th>
              <th style="width: 140px;">Təyin Edilmiş Briqada</th>
            </tr>
          </thead>
          <tbody>
            ${catBaselines.map(b => {
              const pending = settingsState.pendingBaselineChanges[b.productTypeId] || {};
              const easyVal = pending.easy !== undefined ? pending.easy : b.dailyTargetEasy;
              const hardVal = pending.hard !== undefined ? pending.hard : b.dailyTargetHard;

              return `
                <tr>
                  <td style="font-weight:600; color:var(--t1);">
                    ${escapeHtml(b.productName)}
                    <span style="font-size:11px; color:var(--t3); font-family:var(--font-mono); margin-left:6px;">(${b.productTypeId})</span>
                  </td>
                  <td style="text-align: center;">
                    <input type="number" class="form-input" style="width:110px; text-align:center; display:inline-block;"
                      value="${easyVal}" min="10" step="10"
                      onchange="onBaselineChange('${b.productTypeId}', 'easy', this.value)">
                  </td>
                  <td style="text-align: center;">
                    <input type="number" class="form-input" style="width:110px; text-align:center; display:inline-block;"
                      value="${hardVal}" min="10" step="10"
                      onchange="onBaselineChange('${b.productTypeId}', 'hard', this.value)">
                  </td>
                  <td style="font-size:12px; color:var(--t2);">
                    ${escapeHtml(b.teamName || 'Briqada')} (${b.workerCount || 10} işçi)
                  </td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      </div>
    `;
  }).join('');
}

window.onBaselineChange = function(productTypeId, mode, value) {
  if (!settingsState.pendingBaselineChanges[productTypeId]) {
    const existing = settingsState.baselines.find(b => b.productTypeId === productTypeId) || {};
    settingsState.pendingBaselineChanges[productTypeId] = {
      easy: existing.dailyTargetEasy,
      hard: existing.dailyTargetHard
    };
  }
  settingsState.pendingBaselineChanges[productTypeId][mode] = parseInt(value) || 0;
  markUnsavedChanges();
};

function renderTeamsCards() {
  const container = document.getElementById('settings-teams-container');
  if (!container) return;

  container.innerHTML = settingsState.teams.map(t => {
    const pendingVal = settingsState.pendingTeamChanges[t.id] !== undefined ?
      settingsState.pendingTeamChanges[t.id] : t.workerCount;

    return `
      <div style="background:var(--surface-2); border:1px solid var(--b2); border-radius:8px; padding:16px; flex:1; min-width:240px;">
        <div style="font-weight:700; color:var(--t1); margin-bottom:4px;">${escapeHtml(t.departmentName)}</div>
        <div style="font-size:11.5px; color:var(--t3); margin-bottom:12px;">Bant standart briqada heyəti</div>
        <div style="display:flex; align-items:center; gap:10px;">
          <input type="number" class="form-input" style="width:100px; font-family:var(--font-mono); font-weight:700; font-size:14px;"
            value="${pendingVal}" min="1" max="50"
            onchange="onTeamCountChange(${t.id}, this.value)">
          <span style="font-size:12px; color:var(--t2);">nəfər işçi</span>
        </div>
      </div>
    `;
  }).join('');
}

window.onTeamCountChange = function(teamId, value) {
  settingsState.pendingTeamChanges[teamId] = parseInt(value) || 1;
  markUnsavedChanges();
};

function markUnsavedChanges() {
  const saveBtn = document.getElementById('btn-save-settings');
  const alertEl = document.getElementById('settings-unsaved-alert');
  if (saveBtn) saveBtn.classList.remove('btn-outline');
  if (saveBtn) saveBtn.classList.add('btn-primary');
  if (alertEl) alertEl.style.display = 'inline-flex';
}

export async function saveAllSettings() {
  const saveBtn = document.getElementById('btn-save-settings');
  if (saveBtn) {
    saveBtn.disabled = true;
    saveBtn.innerHTML = 'Saxlanılır...';
  }

  try {
    // 1. Save Order Toggles
    const orderEntries = Object.entries(settingsState.pendingOrderChanges);
    if (orderEntries.length > 0) {
      const activeIds = [];
      const inactiveIds = [];
      orderEntries.forEach(([id, active]) => {
        if (active) activeIds.push(id);
        else inactiveIds.push(id);
      });

      if (activeIds.length > 0) {
        await fetch('/api/settings/orders/bulk-toggle', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ orderIds: activeIds, active: true })
        });
      }
      if (inactiveIds.length > 0) {
        await fetch('/api/settings/orders/bulk-toggle', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ orderIds: inactiveIds, active: false })
        });
      }
    }

    // 2. Save Baselines
    const baselineUpdates = Object.entries(settingsState.pendingBaselineChanges).map(([ptId, vals]) => ({
      productTypeId: ptId,
      dailyTargetEasy: vals.easy,
      dailyTargetHard: vals.hard
    }));

    if (baselineUpdates.length > 0) {
      await fetch('/api/settings/baselines', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(baselineUpdates)
      });
    }

    // 3. Save Teams
    const teamUpdates = Object.entries(settingsState.pendingTeamChanges).map(([teamId, count]) => ({
      teamId: parseInt(teamId),
      workerCount: count
    }));

    if (teamUpdates.length > 0) {
      await fetch('/api/settings/teams', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(teamUpdates)
      });
    }

    showToast('Tənzimləmələr uğurla yadda saxlanıldı və istehsalata tətbiq edildi!', 'success');

    // Reset pending changes and reload
    settingsState.pendingOrderChanges = {};
    settingsState.pendingBaselineChanges = {};
    settingsState.pendingTeamChanges = {};

    const alertEl = document.getElementById('settings-unsaved-alert');
    if (alertEl) alertEl.style.display = 'none';

    await loadSettingsOverview();
  } catch (err) {
    console.error('Error saving settings:', err);
    showToast('Xəta baş verdi: ' + err.message, 'error');
  } finally {
    if (saveBtn) {
      saveBtn.disabled = false;
      saveBtn.innerHTML = `
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Dəyişiklikləri Yadda Saxla və Tətbiq Et
      `;
    }
  }
}

function showToast(msg, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.style.cssText = `
    position: fixed; top: 24px; right: 24px; padding: 12px 20px; border-radius: 8px;
    background: ${type === 'success' ? '#059669' : type === 'error' ? '#dc2626' : '#2563eb'};
    color: #fff; font-weight: 600; font-size: 13px; z-index: 9999; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  `;
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

window.loadSettingsOverview = loadSettingsOverview;
window.setOrderFilter = setOrderFilter;
window.saveAllSettings = saveAllSettings;
