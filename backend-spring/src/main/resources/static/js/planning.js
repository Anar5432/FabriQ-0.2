import { CATEGORIES } from './config.js';
import { state } from './state.js';
import { isGhostOrder, matchCategory, showToast } from './utils.js';
import { checkMaterials, planForward, planBackward } from './api.js';

let checkTimeout = null;

/* ══════════════════════════════════════
   PLANNING STUDIO LOGIC (2 MODES)
══════════════════════════════════════ */

export function initPlanningStudio() {
  const startInput = document.getElementById('plan-input-start');
  const deadInput = document.getElementById('plan-input-deadline');
  const today = new Date().toISOString().split('T')[0];
  if (startInput && !startInput.value) startInput.value = today;

  if (deadInput && !deadInput.value) {
    const future = new Date();
    future.setDate(future.getDate() + 20);
    deadInput.value = future.toISOString().split('T')[0];
  }

  onPlanCategoryChange();
}

export function switchPlanningMode(mode) {
  state.currentPlanningMode = mode;
  const btn1 = document.getElementById('tab-btn-opt1');
  const btn2 = document.getElementById('tab-btn-opt2');
  const fwdInputs = document.getElementById('forward-only-inputs');
  const backInputs = document.getElementById('backward-only-inputs');
  const title = document.getElementById('form-mode-title');

  if (mode === 'forward') {
    if (btn1) btn1.classList.add('active');
    if (btn2) btn2.classList.remove('active');
    if (fwdInputs) fwdInputs.style.display = 'block';
    if (backInputs) backInputs.style.display = 'none';
    if (title) title.textContent = 'Rejim 1: Mövcud Resurslarla Təhvil Tarixi Hesablaması';
  } else {
    if (btn1) btn1.classList.remove('active');
    if (btn2) btn2.classList.add('active');
    if (fwdInputs) fwdInputs.style.display = 'none';
    if (backInputs) backInputs.style.display = 'block';
    if (title) title.textContent = 'Rejim 2: Hədəf Tarixə (Deadline) Uyğun Resurs Hesablaması';
  }
}

export function populateExistingOrdersDropdown() {
  const sel = document.getElementById('plan-input-existing-order');
  if (!sel) return;
  // Strictly only show ACTIVE non-ghost orders for planning:
  const activeOrders = state.allOrders.filter(o => !isGhostOrder(o));
  sel.innerHTML = '<option value="">-- Yeni Fərdi Sifariş Planlaması --</option>' +
    activeOrders.map(o => {
      const client = o.customerName || 'Müştəri';
      const prod = o.productType ? o.productType.name : 'Məhsul';
      return `<option value="${o.id}">№ ${o.id} · ${client} (${prod} - ${o.quantity || 0} əd.)</option>`;
    }).join('');
}

export function onExistingOrderSelect() {
  const orderId = document.getElementById('plan-input-existing-order').value;
  if (!orderId) return;
  const o = state.allOrders.find(x => x.id === orderId);
  if (!o) return;

  // Determine Category
  const cat = CATEGORIES.find(c => matchCategory(o, c.id)) || CATEGORIES[0];
  const catSelect = document.getElementById('plan-input-cat');
  if (catSelect) catSelect.value = cat.id;
  onPlanCategoryChange();

  // Set product
  if (o.productType && o.productType.id) {
    const prodSelect = document.getElementById('plan-input-prod');
    if (prodSelect) prodSelect.value = o.productType.id;
  }
  // Set quantity
  if (o.quantity) {
    const qtyInput = document.getElementById('plan-input-qty');
    if (qtyInput) qtyInput.value = o.quantity;
  }

  // Set smart future deadline (never allow ancient past dates like 2019):
  const todayStr = new Date().toISOString().split('T')[0];
  const deadlineInput = document.getElementById('plan-input-deadline');
  if (deadlineInput) {
    if (o.deadline && o.deadline >= todayStr) {
      deadlineInput.value = o.deadline;
    } else {
      const d = new Date();
      d.setDate(d.getDate() + 20);
      deadlineInput.value = d.toISOString().split('T')[0];
    }
  }

  triggerMaterialCheck();
}

export function onPlanCategoryChange() {
  const catSelect = document.getElementById('plan-input-cat');
  const catId = catSelect ? catSelect.value : 'Workwear';
  const cat = CATEGORIES.find(c => c.id === catId) || CATEGORIES[0];
  const prodSelect = document.getElementById('plan-input-prod');

  if (prodSelect) {
    prodSelect.innerHTML = cat.products.map(p => `
      <option value="${p.id}">${p.name} (Norma: ${p.easyRate} asan / ${p.hardRate} çətin)</option>
    `).join('');
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
  if (!prodEl || !qtyEl) return;

  const prodId = prodEl.value;
  const qty = parseInt(qtyEl.value) || 500;
  const badge = document.getElementById('gate-status-badge');
  const details = document.getElementById('gate-mat-details');
  const prompts = document.getElementById('gate-lead-prompts');

  try {
    const data = await checkMaterials(prodId, qty);
    if (data.allMaterialsSufficient) {
      if (badge) {
        badge.className = 'gate-status-pill ok';
        badge.textContent = 'Kifayətdir (Anbarda Var)';
      }
      if (prompts) prompts.style.display = 'none';
    } else {
      if (badge) {
        badge.className = 'gate-status-pill warn';
        badge.textContent = 'Çatışmır (Təchizat Lazımdır)';
      }
      if (prompts) prompts.style.display = 'block';
    }

    if (details) {
      details.innerHTML = data.materials.map(m => `
        <div style="display:flex; justify-content:space-between;">
          <span>${m.materialName}</span>
          <span style="font-family:var(--font-mono); color:${m.isSufficient ? 'var(--success)' : 'var(--danger)'};">
            ${m.availableQuantity.toFixed(0)} / ${m.neededQuantity.toFixed(0)} ${m.unit}
          </span>
        </div>
      `).join('');
    }
  } catch (e) {
    console.error('Material check failed', e);
  }
}

export async function calculateActivePlan() {
  const prodId = document.getElementById('plan-input-prod').value;
  const qty = parseInt(document.getElementById('plan-input-qty').value) || 500;
  const catId = document.getElementById('plan-input-cat').value;
  const startDate = document.getElementById('plan-input-start').value;

  const promptEl = document.getElementById('gate-lead-prompts');
  const isPromptVisible = promptEl && promptEl.style.display !== 'none';
  const designDays = isPromptVisible ? parseFloat(document.getElementById('plan-lead-design').value) || 0 : 0;
  const sourcingDays = isPromptVisible ? parseFloat(document.getElementById('plan-lead-sourcing').value) || 0 : 0;

  if (state.currentPlanningMode === 'forward') {
    const workers = parseInt(document.getElementById('plan-input-workers').value) || 10;
    const diff = document.getElementById('plan-input-diff').value;

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
      showToast('Xəta: ' + e.message);
    }
  } else {
    // Backward Mode
    const deadline = document.getElementById('plan-input-deadline').value;
    const baseWorkers = parseInt(document.getElementById('plan-input-baseworkers').value) || 10;
    const diff = document.getElementById('plan-input-backdiff').value;

    if (deadline && startDate && deadline < startDate) {
      showToast('Xəta: Müştəri hədəf deadline tarixi başlama tarixindən əvvəl ola bilməz!');
      return;
    }

    try {
      const data = await planBackward({
        productTypeId: prodId,
        quantity: qty,
        conveyorLine: catId,
        customerDeadline: deadline,
        startDate: startDate,
        baseWorkers: baseWorkers,
        difficulty: diff,
        designDays: designDays,
        sourcingDays: sourcingDays
      });
      renderBackwardResult(data);
    } catch (e) {
      showToast('Xəta: ' + e.message);
    }
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
          Miqdar: ${data.quantity} ədəd · İşçi Heyəti: ${data.workers} nəfər (${data.difficulty === 'HARD' ? 'Çətin Norma' : 'Asan Norma'})
        </div>
      </div>
      <div style="text-align:right;">
        <div style="display:flex; align-items:center; gap:8px; justify-content:flex-end; margin-bottom:4px;">
          <button class="btn btn-outline" style="font-size:11px; padding:3px 8px; gap:4px;" onclick="window.print()">
            <svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:2;"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            Çap / PDF
          </button>
        </div>
        <div style="font-size:11px; color:var(--t3); text-transform:uppercase; font-weight:600;">Planlanan Bitiş Tarixi</div>
        <div style="font-size:22px; font-weight:700; font-family:var(--font-mono); color:var(--success);">${data.deliveryDate}</div>
      </div>
    </div>

    <div class="result-metrics-grid">
      <div class="metric-box">
        <div class="metric-box-lbl">Kəsim Müddəti (+30%)</div>
        <div class="metric-box-val">${data.cuttingDays.toFixed(1)} gün</div>
        <div class="metric-box-sub">Norma: ${data.dailyCuttingRate.toFixed(0)} əd/gün</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Tikiş Müddəti</div>
        <div class="metric-box-val">${data.sewingDays.toFixed(1)} gün</div>
        <div class="metric-box-sub">Norma: ${data.dailySewingRate.toFixed(0)} əd/gün</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Dizayn & Təchizat</div>
        <div class="metric-box-val">${(data.designDays + data.sourcingDays).toFixed(0)} gün</div>
        <div class="metric-box-sub">İlkin hazırlıq</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Cəmi İstehsalat Vaxtı</div>
        <div class="metric-box-val" style="color:var(--primary);">${(data.totalManufacturingDays + data.designDays + data.sourcingDays).toFixed(1)} gün</div>
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

export function renderBackwardResult(data) {
  const container = document.getElementById('plan-result-container');
  if (!container) return;

  const isInvalidDate = data.status === 'INVALID_DEADLINE_IN_PAST';
  const isOk = data.isFeasible && !isInvalidDate;
  const statusColor = isInvalidDate ? 'var(--danger)' : (isOk ? 'var(--success)' : 'var(--danger)');
  const statusBadge = isInvalidDate ? 'TARİX XƏTASI (DEADLINE KEÇMİŞDƏDİR)' : (isOk ? 'ÇATDIRILIR (MÖVCUD RESURSLAR KİFAYƏTDİR)' : 'GECİKMƏ TƏHLÜKƏSİ — ƏLAVƏ İŞÇİ LAZIMDIR');
  const accelText = data.accelerationFactor > 0 ? (data.accelerationFactor.toFixed(2) + 'x') : 'Qeyri-mümkün';
  const netDaysText = data.netManufacturingDays > 0 ? (data.netManufacturingDays + ' gün') : '0 gün (Müddət Çatmır)';

  container.innerHTML = `
    <div class="result-header">
      <div>
        <div style="font-size:16px; font-weight:700; color:var(--t1);">${data.productName} — Hədəf Deadline Təhlili</div>
        <div style="font-size:12px; color:var(--t2); margin-top:3px;">
          Hədəf Deadline: <b style="color:var(--warning); font-family:var(--font-mono);">${data.customerDeadline}</b> · Miqdar: ${data.quantity} ədəd
        </div>
      </div>
      <div style="text-align:right; display:flex; align-items:center; gap:8px; justify-content:flex-end;">
        <span class="badge ${isOk ? 'badge-green' : 'badge-red'}" style="font-size:12px; padding:6px 12px;">
          <span class="badge-dot"></span>${statusBadge}
        </span>
        <button class="btn btn-outline" style="font-size:11px; padding:4px 8px; gap:4px;" onclick="window.print()">
          <svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:2;"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          Çap / PDF
        </button>
      </div>
    </div>

    <div style="background:${isOk ? 'var(--success-bg)' : 'var(--danger-bg)'}; border:1px solid ${statusColor}; border-radius:8px; padding:14px; margin-bottom:18px; font-size:13px; font-weight:500; color:${statusColor};">
      ${data.recommendation}
    </div>

    <div class="result-metrics-grid">
      <div class="metric-box">
        <div class="metric-box-lbl">Mövcud Briqada</div>
        <div class="metric-box-val">${data.baseWorkers} işçi</div>
        <div class="metric-box-sub">Standart tərkib</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Tələb Olunan Heyət</div>
        <div class="metric-box-val" style="color:${isOk ? 'var(--t1)' : 'var(--danger)'};">${data.requiredWorkers} işçi</div>
        <div class="metric-box-sub">${data.extraWorkersNeeded > 0 ? '+' + data.extraWorkersNeeded + ' əlavə işçi' : 'Əlavə işçi tələb olunmur'}</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Net İstehsalat Vaxtı</div>
        <div class="metric-box-val">${netDaysText}</div>
        <div class="metric-box-sub">Dizayn/Təchizat çıxıldıqdan sonra</div>
      </div>
      <div class="metric-box">
        <div class="metric-box-lbl">Sürətləndirmə Əmsalı</div>
        <div class="metric-box-val" style="color:${data.accelerationFactor > 1 ? 'var(--warning)' : (isOk ? 'var(--success)' : 'var(--danger)')};">${accelText}</div>
        <div class="metric-box-sub">${data.accelerationFactor > 1 ? 'Overtime / Əlavə xətt' : (data.accelerationFactor > 0 ? 'Standart sürət' : 'Tarix çatışmır')}</div>
      </div>
    </div>

    <div style="font-size:12.5px; font-weight:700; color:var(--t1); margin-bottom:10px;">Tələb Olunan İstehsal Qrafiki</div>
    ${(data.stages && data.stages.length > 0) ? `
    <div class="timeline-stages">
      ${data.stages.map((st, i) => `
        <div class="stage-bar-item">
          <div class="stage-bar-info">
            <div class="stage-num-box">${i+1}</div>
            <div class="stage-name-text">${st.stageName}</div>
          </div>
          <div class="stage-dates-text">
            <span>${st.startDate}</span> &rarr; <span style="color:var(--t1); font-weight:600;">${st.endDate}</span> (${st.days.toFixed(1)} gün)
          </div>
        </div>
      `).join('')}
    </div>` : `<div style="color:var(--t3); font-size:12.5px; padding:14px; background:rgba(255,255,255,0.02); border-radius:6px; border:1px dashed var(--b2);">Qrafik hesablanması üçün zəhmət olmasa gələcək tarixli deadline seçin.</div>`}
  `;
}
