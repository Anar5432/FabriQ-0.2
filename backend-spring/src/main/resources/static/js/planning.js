import { CATEGORIES } from './config.js';
import { state } from './state.js';
import { isGhostOrder, matchCategory, showToast } from './utils.js';
import { checkMaterials, planForward } from './api.js';

let checkTimeout = null;
let lastCheckData = null;

/* ══════════════════════════════════════════════════════════════════════
   FORWARD PLANNING STUDIO LOGIC (Level 1 Category -> Level 2 Source)
══════════════════════════════════════════════════════════════════════ */

export function initPlanningStudio() {
  const startInput = document.getElementById('plan-input-start');
  const today = new Date().toISOString().split('T')[0];
  if (startInput && !startInput.value) startInput.value = today;

  state.selectedPlanSource = 'standard'; // 'standard' or 'existing'

  onPlanCategoryChange();
}

export function switchProductSource(source) {
  state.selectedPlanSource = source;
  const btnStd = document.getElementById('btn-source-standard');
  const btnExist = document.getElementById('btn-source-existing');

  if (source === 'standard') {
    if (btnStd) btnStd.classList.add('active');
    if (btnExist) btnExist.classList.remove('active');
  } else {
    if (btnStd) btnStd.classList.remove('active');
    if (btnExist) btnExist.classList.add('active');
  }

  populateProductDropdown();
}

export function onPlanCategoryChange() {
  populateProductDropdown();
}

export function onPlanItemSearch() {
  populateProductDropdown();
}

export function populateProductDropdown() {
  const catSelect = document.getElementById('plan-input-cat');
  const catId = catSelect ? catSelect.value : 'Workwear';
  const cat = CATEGORIES.find(c => c.id === catId) || CATEGORIES[0];
  const prodSelect = document.getElementById('plan-input-prod');
  const searchInput = document.getElementById('plan-item-search');
  const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

  if (!prodSelect) return;

  if (state.selectedPlanSource === 'standard') {
    // 1. Standard Products List
    let products = cat.products || [];
    if (query) {
      products = products.filter(p => p.name.toLowerCase().includes(query) || p.id.toLowerCase().includes(query));
    }

    if (products.length === 0) {
      prodSelect.innerHTML = '<option value="">-- Axtarışa uyğun standart məhsul tapılmadı --</option>';
    } else {
      prodSelect.innerHTML = products.map(p => `
        <option value="${p.id}" data-type="standard">
          ${p.name} (Norma: ${p.easyRate} asan / ${p.hardRate} çətin)
        </option>
      `).join('');
    }
  } else {
    // 2. Past Customer Orders in this Category
    let matchingOrders = (state.allOrders || []).filter(o => !isGhostOrder(o) && matchCategory(o, catId));

    if (query) {
      matchingOrders = matchingOrders.filter(o => 
        (o.id && o.id.toLowerCase().includes(query)) ||
        (o.customerName && o.customerName.toLowerCase().includes(query)) ||
        (o.productType && o.productType.name && o.productType.name.toLowerCase().includes(query))
      );
    }

    if (matchingOrders.length === 0) {
      prodSelect.innerHTML = '<option value="">-- Bu kateqoriyada uyğun sifariş tapılmadı --</option>';
    } else {
      prodSelect.innerHTML = matchingOrders.map(o => {
        const pId = o.productType && o.productType.id ? o.productType.id : 'kitel';
        const pName = o.productType && o.productType.name ? o.productType.name : 'Məhsul';
        const client = o.customerName || 'Müştəri';
        return `
          <option value="${pId}" data-order-id="${o.id}" data-qty="${o.quantity || 500}">
            № ${o.id} · ${client} (${pName} - ${o.quantity || 0} əd.)
          </option>
        `;
      }).join('');
    }
  }

  onProductSelectChange();
}

export function onProductSelectChange() {
  const prodSelect = document.getElementById('plan-input-prod');
  if (!prodSelect || prodSelect.selectedIndex < 0) return;

  const opt = prodSelect.options[prodSelect.selectedIndex];
  if (opt && opt.dataset.qty) {
    const qtyInput = document.getElementById('plan-input-qty');
    if (qtyInput) qtyInput.value = opt.dataset.qty;
  }

  triggerMaterialCheck();
}

export function triggerMaterialCheck() {
  clearTimeout(checkTimeout);
  checkTimeout = setTimeout(checkMaterialsAsync, 300);
}

async function checkMaterialsAsync() {
  const prodEl = document.getElementById('plan-input-prod');
  const qtyEl = document.getElementById('plan-input-qty');
  if (!prodEl || !qtyEl || !prodEl.value) return;

  const prodId = prodEl.value;
  const qty = parseInt(qtyEl.value) || 500;
  const badge = document.getElementById('gate-status-badge');
  const details = document.getElementById('gate-mat-details');
  const shortageBox = document.getElementById('gate-shortage-alert-box');

  try {
    const data = await checkMaterials(prodId, qty);
    lastCheckData = data;

    if (data.allMaterialsSufficient) {
      if (badge) {
        badge.className = 'gate-status-pill ok';
        badge.textContent = 'Kifayətdir (Sərbəst Qalıq Var)';
      }
      if (shortageBox) shortageBox.style.display = 'none';
      document.getElementById('plan-lead-sourcing').value = '0';
      document.getElementById('plan-lead-design').value = '0';
    } else {
      if (badge) {
        badge.className = 'gate-status-pill warn';
        badge.textContent = 'Çatışmır (Təchizat Lazımdır)';
      }
      if (shortageBox) shortageBox.style.display = 'block';
    }

    // Render Two-Tier Material Table
    if (details) {
      details.innerHTML = `
        <table class="two-tier-mat-table">
          <thead>
            <tr>
              <th>Xammal</th>
              <th style="text-align:right;">Tələb</th>
              <th style="text-align:right;">Ümumi Anbar</th>
              <th style="text-align:right; color:var(--warning);">Aktiv Rezerv</th>
              <th style="text-align:right; color:var(--primary);">Sərbəst Qalıq</th>
              <th style="text-align:center;">Vəziyyət</th>
            </tr>
          </thead>
          <tbody>
            ${data.materials.map(m => {
              const phys = m.totalPhysicalStock !== undefined ? m.totalPhysicalStock : m.availableQuantity;
              const comm = m.committedStock !== undefined ? m.committedStock : 0;
              const free = m.freeAvailableStock !== undefined ? m.freeAvailableStock : (phys - comm);

              return `
                <tr>
                  <td style="font-weight:600; color:var(--t1);">${m.materialName}</td>
                  <td style="text-align:right; font-family:var(--font-mono);">${m.neededQuantity.toFixed(1)} ${m.unit}</td>
                  <td style="text-align:right; font-family:var(--font-mono); color:var(--t2);">${phys.toFixed(0)}</td>
                  <td style="text-align:right; font-family:var(--font-mono); color:var(--warning);">${comm > 0 ? ('-' + comm.toFixed(0)) : '0'}</td>
                  <td style="text-align:right; font-family:var(--font-mono); font-weight:700; color:${m.isSufficient ? 'var(--success)' : 'var(--danger)'};">
                    ${free.toFixed(0)} ${m.unit}
                  </td>
                  <td style="text-align:center;">
                    <span class="badge ${m.isSufficient ? 'badge-green' : 'badge-red'}" style="font-size:10px; padding:2px 6px;">
                      ${m.isSufficient ? 'Çatır' : ('Çatışmır: -' + m.missingQuantity.toFixed(0))}
                    </span>
                  </td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      `;
    }
  } catch (e) {
    console.error('Material check failed', e);
  }
}

/* ══════════════════════════════════════
   SHORTAGE LEAD-TIME MODAL HANDLERS
══════════════════════════════════════ */
export function openShortageModal() {
  const modal = document.getElementById('shortage-modal');
  const tableContainer = document.getElementById('modal-shortage-items-table');
  if (!modal || !lastCheckData) return;

  const missingMaterials = lastCheckData.materials.filter(m => !m.isSufficient);

  if (tableContainer) {
    tableContainer.innerHTML = `
      <table class="table" style="background:var(--surface-2); border-radius:8px;">
        <thead>
          <tr>
            <th>Çatışmayan Xammal</th>
            <th style="text-align:right;">Tələb</th>
            <th style="text-align:right;">Sərbəst Qalıq</th>
            <th style="text-align:right; color:var(--danger);">Çatışmayan Miqdar</th>
          </tr>
        </thead>
        <tbody>
          ${missingMaterials.map(m => `
            <tr>
              <td style="font-weight:600; color:var(--t1);">${m.materialName}</td>
              <td style="text-align:right; font-family:var(--font-mono);">${m.neededQuantity.toFixed(1)} ${m.unit}</td>
              <td style="text-align:right; font-family:var(--font-mono);">${(m.freeAvailableStock || 0).toFixed(0)} ${m.unit}</td>
              <td style="text-align:right; font-family:var(--font-mono); font-weight:700; color:var(--danger);">
                -${m.missingQuantity.toFixed(1)} ${m.unit}
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  }

  modal.style.display = 'flex';
}

export function closeShortageModal(event) {
  if (event && event.target && event.target.id !== 'shortage-modal' && !event.target.classList.contains('modal-close')) return;
  const modal = document.getElementById('shortage-modal');
  if (modal) modal.style.display = 'none';
}

export function applyShortageModal() {
  const designDays = parseFloat(document.getElementById('modal-lead-design').value) || 0;
  const sourcingDays = parseFloat(document.getElementById('modal-lead-sourcing').value) || 0;

  document.getElementById('plan-lead-design').value = designDays;
  document.getElementById('plan-lead-sourcing').value = sourcingDays;

  closeShortageModal();
  showToast(`Təchizat müddəti (${sourcingDays} gün) və Dizayn (${designDays} gün) qrafikə daxil edildi.`, 'info');

  calculateActivePlan();
}

/* ══════════════════════════════════════
   FORWARD PLANNING EXECUTION
══════════════════════════════════════ */
export async function calculateActivePlan() {
  const prodEl = document.getElementById('plan-input-prod');
  if (!prodEl || !prodEl.value) {
    showToast('Zəhmət olmasa planlamaq üçün məhsul və ya sifariş seçin!', 'warning');
    return;
  }

  const prodId = prodEl.value;
  const qty = parseInt(document.getElementById('plan-input-qty').value) || 500;
  const catId = document.getElementById('plan-input-cat').value;
  const startDate = document.getElementById('plan-input-start').value;
  const workers = parseInt(document.getElementById('plan-input-workers').value) || 10;
  const diff = document.getElementById('plan-input-diff').value;

  const designDays = parseFloat(document.getElementById('plan-lead-design').value) || 0;
  const sourcingDays = parseFloat(document.getElementById('plan-lead-sourcing').value) || 0;

  try {
    const data = await planForward({
      productTypeId: prodId,
      quantity: qty,
      conveyorLine: catId,
      workers: workers,
      difficulty: diff,
      startDate: startDate,
      designDays: designDays,
      sourcingDays: sourcingDays
    });
    renderForwardResult(data);
  } catch (e) {
    showToast('Xəta: ' + e.message, 'error');
  }
}

export function renderForwardResult(data) {
  const container = document.getElementById('plan-result-container');
  if (!container) return;

  container.innerHTML = `
    <div class="result-header">
      <div>
        <div style="font-size:16px; font-weight:700; color:var(--t1);">${data.productName} — Təhvil Tarixi Hesablaması</div>
        <div style="font-size:12px; color:var(--t2); margin-top:3px;">
          Planlanan Miqdar: <b>${data.quantity} ədəd</b> · İşçi Heyəti: <b>${data.workers} nəfər</b> (${data.difficulty === 'HARD' ? 'Çətin Norma' : 'Asan Standart'})
        </div>
      </div>
      <div style="text-align:right;">
        <div style="display:flex; align-items:center; gap:8px; justify-content:flex-end; margin-bottom:4px;">
          <button class="btn btn-outline" style="font-size:11px; padding:3px 8px; gap:4px;" onclick="window.print()">
            <svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:2;"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            Çap / PDF
          </button>
        </div>
        <div style="font-size:11px; color:var(--t3); text-transform:uppercase; font-weight:600;">Planlanan Təhvil Tarixi</div>
        <div style="font-size:24px; font-weight:700; font-family:var(--font-mono); color:var(--success);">${data.deliveryDate}</div>
      </div>
    </div>

    <div class="result-metrics-grid">
      <div class="metric-box">
        <div class="metric-box-lbl">Kəsim / Hörgü Müddəti</div>
        <div class="metric-box-val">${data.cuttingDays.toFixed(1)} gün</div>
        <div class="metric-box-sub">Norma: ${data.dailyCuttingRate.toFixed(0)} əd/gün (+30%)</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Tikiş / Forma Müddəti</div>
        <div class="metric-box-val">${data.sewingDays.toFixed(1)} gün</div>
        <div class="metric-box-sub">Norma: ${data.dailySewingRate.toFixed(0)} əd/gün</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Təchizat & Dizayn Buferi</div>
        <div class="metric-box-val" style="color:${(data.designDays + data.sourcingDays) > 0 ? 'var(--warning)' : 'var(--t2)'};">
          ${(data.designDays + data.sourcingDays).toFixed(0)} gün
        </div>
        <div class="metric-box-sub">Gözləmə müddəti</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Ümumi İcra Müddəti</div>
        <div class="metric-box-val" style="color:var(--primary);">
          ${(data.totalManufacturingDays + data.designDays + data.sourcingDays).toFixed(1)} gün
        </div>
        <div class="metric-box-sub">Başlama: ${data.startDate}</div>
      </div>
    </div>

    <div style="font-size:12.5px; font-weight:700; color:var(--t1); margin-bottom:10px;">Mərhələlər Üzrə İcra Qrafiki</div>
    <div class="timeline-stages">
      ${data.stages.map((st, i) => `
        <div class="stage-bar-item">
          <div class="stage-bar-info">
            <div class="stage-num-box">${i+1}</div>
            <div>
              <div class="stage-name-text">${st.stageName}</div>
              <div style="font-size:10.5px; color:var(--t3);">${st.details || ''}</div>
            </div>
          </div>
          <div class="stage-dates-text">
            <span>${st.startDate}</span> &rarr; <span style="color:var(--t1); font-weight:600;">${st.endDate}</span> (${st.days.toFixed(1)} gün)
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

// Window attachments for inline HTML event attributes
window.switchProductSource = switchProductSource;
window.onPlanCategoryChange = onPlanCategoryChange;
window.onPlanItemSearch = onPlanItemSearch;
window.onProductSelectChange = onProductSelectChange;
window.triggerMaterialCheck = triggerMaterialCheck;
window.calculateActivePlan = calculateActivePlan;
window.openShortageModal = openShortageModal;
window.closeShortageModal = closeShortageModal;
window.applyShortageModal = applyShortageModal;
