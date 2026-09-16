import { CATEGORIES } from './config.js';
import { state } from './state.js';
import { showToast } from './utils.js';
import { triggerSync } from './api.js';
import {
  loadOrders,
  selectCategory,
  selectStage,
  toggleArchiveView,
  openInspectModal,
  closeInspectModal,
  renderDashboardTable,
  loadMoreOrders
} from './dashboard.js';
import {
  initPlanningStudio,
  switchPlanningMode,
  onPlanCategoryChange,
  onExistingOrderSelect,
  triggerMaterialCheck,
  calculateActivePlan
} from './planning.js';

/* ══════════════════════════════════════
   NAVIGATION SWITCHING
══════════════════════════════════════ */
export function switchMainView(view) {
  const vDash = document.getElementById('view-dashboard');
  const vPlan = document.getElementById('view-planning');
  const btnDash = document.getElementById('btn-view-dash');
  const btnPlan = document.getElementById('btn-view-plan');

  if (!vDash || !vPlan || !btnDash || !btnPlan) return;

  if (view === 'planning') {
    vDash.style.display = 'none';
    vPlan.style.display = 'flex';
    btnDash.classList.remove('active');
    btnPlan.classList.add('active');
    initPlanningStudio();
  } else {
    vDash.style.display = 'flex';
    vPlan.style.display = 'none';
    btnDash.classList.add('active');
    btnPlan.classList.remove('active');
  }
}

export function openQuickPlan() {
  switchMainView('planning');
}

/* ══════════════════════════════════════
   SYNC OPERATION (MS SQL)
══════════════════════════════════════ */
export async function syncFromLegacy() {
  const btn = document.getElementById('btn-sync');
  if (btn) btn.textContent = 'Sinxronizasiya edilir...';
  try {
    const res = await triggerSync();
    showToast(res && res.message ? res.message : 'MS SQL serverindən sifarişlər uğurla yeniləndi.');
    await loadOrders();
  } catch (e) {
    showToast('MS SQL sinxronizasiya xətası: ' + e.message);
  } finally {
    if (btn) {
      btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg> MS SQL Sinxronizasiya`;
    }
  }
}

/* ══════════════════════════════════════
   GLOBAL WINDOW REGISTRATION
   Required for HTML onclick event handlers
══════════════════════════════════════ */
window.switchMainView = switchMainView;
window.openQuickPlan = openQuickPlan;
window.selectCategory = selectCategory;
window.selectStage = selectStage;
window.toggleArchiveView = toggleArchiveView;
window.openInspectModal = openInspectModal;
window.closeInspectModal = closeInspectModal;
window.renderDashboardTable = renderDashboardTable;
window.loadMoreOrders = loadMoreOrders;
window.switchPlanningMode = switchPlanningMode;
window.onPlanCategoryChange = onPlanCategoryChange;
window.onExistingOrderSelect = onExistingOrderSelect;
window.triggerMaterialCheck = triggerMaterialCheck;
window.calculateActivePlan = calculateActivePlan;
window.syncFromLegacy = syncFromLegacy;

/* ══════════════════════════════════════
   APPLICATION BOOTSTRAP
══════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-query');
  if (searchInput) {
    searchInput.addEventListener('input', renderDashboardTable);
  }

  const statusSelect = document.getElementById('filter-status');
  if (statusSelect) {
    statusSelect.addEventListener('change', renderDashboardTable);
  }

  // Initial orders load
  loadOrders();
});
