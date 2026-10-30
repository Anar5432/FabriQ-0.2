import { CATEGORIES } from './config.js';
import { state } from './state.js';
import { showToast } from './utils.js';
import { triggerSync, fetchSyncStatus } from './api.js';
import {
  loadOrders,
  selectCategory,
  selectStage,
  toggleArchiveView,
  openInspectModal,
  closeInspectModal,
  renderDashboardTable,
  loadMoreOrders,
  toggleModalFullscreen,
  toggleInspectHeader,
  setSuborderDensity,
  filterSubordersList,
  clearSuborderFilter,
  scrollSuborders
} from './dashboard.js';
import {
  initPlanningStudio,
  switchProductSource,
  onPlanCategoryChange,
  onPlanItemSearch,
  onProductSelectChange,
  triggerMaterialCheck,
  calculateActivePlan,
  openShortageModal,
  closeShortageModal,
  applyShortageModal
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
window.loadOrders = loadOrders;
window.selectCategory = selectCategory;
window.selectStage = selectStage;
window.toggleArchiveView = toggleArchiveView;
window.openInspectModal = openInspectModal;
window.closeInspectModal = closeInspectModal;
window.renderDashboardTable = renderDashboardTable;
window.loadMoreOrders = loadMoreOrders;
window.switchProductSource = switchProductSource;
window.onPlanCategoryChange = onPlanCategoryChange;
window.onPlanItemSearch = onPlanItemSearch;
window.onProductSelectChange = onProductSelectChange;
window.triggerMaterialCheck = triggerMaterialCheck;
window.calculateActivePlan = calculateActivePlan;
window.openShortageModal = openShortageModal;
window.closeShortageModal = closeShortageModal;
window.applyShortageModal = applyShortageModal;
window.syncFromLegacy = syncFromLegacy;
window.toggleModalFullscreen = toggleModalFullscreen;
window.toggleInspectHeader = toggleInspectHeader;
window.setSuborderDensity = setSuborderDensity;
window.filterSubordersList = filterSubordersList;
window.clearSuborderFilter = clearSuborderFilter;
window.scrollSuborders = scrollSuborders;

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeInspectModal();
  }
});

/* ══════════════════════════════════════
   APPLICATION BOOTSTRAP
══════════════════════════════════════ */
let currentDataVersion = null;

async function checkLiveSync() {
  try {
    const status = await fetchSyncStatus();
    if (!status || status.version === undefined) return;

    const indText = document.getElementById('live-sync-text');
    if (indText) {
      indText.textContent = `Canlı: 81.17.85.185 (${status.totalOrders})`;
    }

    if (currentDataVersion === null) {
      currentDataVersion = status.version;
      return;
    }

    if (status.version !== currentDataVersion) {
      console.log(`⚡ Real-Time ERP update: Data version updated (${currentDataVersion} -> ${status.version}). Refreshing dashboard...`);
      currentDataVersion = status.version;
      await loadOrders();

      // If the inspect modal is currently open, smoothly refresh open order details too!
      const modal = document.getElementById('inspect-modal');
      if (modal && modal.style.display !== 'none' && state.inspectedOrder) {
        const refreshedOrder = state.allOrders.find(o => o.id === state.inspectedOrder.id);
        if (refreshedOrder) {
          openInspectModal(refreshedOrder);
        }
      }

      showToast(`⚡ ERP bazasından yeni məlumat daxil oldu (Versiya: ${status.version}). İdarəetmə paneli canlı yeniləndi.`);
    }
  } catch (e) {
    // Retried automatically on next cycle
  }
}

function bootstrapApp() {
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

  // Trigger initial live check and start fast 3-second cycle
  checkLiveSync();
  setInterval(checkLiveSync, 3000);
}

// In ES6 module architecture, DOMContentLoaded may have already fired before this script executes.
// Check readyState to ensure reliable initialization under all circumstances.
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrapApp);
} else {
  bootstrapApp();
}
