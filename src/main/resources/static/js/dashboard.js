import { CATEGORIES } from './config.js';
import { state } from './state.js';
import { isGhostOrder, matchCategory, matchStage, getActiveCat, normalizeAz } from './utils.js';
import { fetchOrders, fetchOrderItems } from './api.js';
import { populateExistingOrdersDropdown } from './planning.js';

/* ══════════════════════════════════════
   DASHBOARD DATA & RENDERING
══════════════════════════════════════ */

export async function loadOrders() {
  try {
    state.allOrders = await fetchOrders();
    renderSidebar();
    renderStageStrip();
    renderDashboardTable();
    populateExistingOrdersDropdown();
  } catch (e) {
    console.error('Failed to load orders:', e);
  }
}

export function selectCategory(catId) {
  state.activeCategoryId = catId;
  state.batchLimit = 50;
  state.activeStageId = null; // Reset stage filter when switching category
  const titleEl = document.getElementById('title-cat-name');
  if (titleEl) titleEl.textContent = getActiveCat().name;
  renderSidebar();
  renderStageStrip();
  renderDashboardTable();
}

export function selectStage(stageId) {
  state.activeStageId = stageId;
  state.batchLimit = 50;
  renderStageStrip();
  renderDashboardTable();
}

export function toggleArchiveView() {
  state.showArchive = !state.showArchive;
  state.batchLimit = 50;
  const btn = document.getElementById('archive-toggle-btn');
  const lbl = document.getElementById('filter-mode-label');
  if (state.showArchive) {
    if (btn) {
      btn.style.background = 'var(--warning, #fbbf24)';
      btn.style.color = '#000';
      btn.style.borderColor = 'var(--warning, #fbbf24)';
      btn.textContent = 'Aktiv İstehsalat';
    }
    if (lbl) {
      lbl.textContent = '· Arxiv və Qalıqlar';
      lbl.style.color = 'var(--warning, #fbbf24)';
    }
  } else {
    if (btn) {
      btn.style.background = 'var(--s2)';
      btn.style.color = 'var(--t2)';
      btn.style.borderColor = 'var(--b1)';
      btn.textContent = 'Arxiv / Qalıqlar';
    }
    if (lbl) {
      lbl.textContent = '· Aktiv İstehsalat';
      lbl.style.color = 'var(--t3)';
    }
  }
  renderStageStrip();
  renderDashboardTable();
}

export function renderSidebar() {
  // 1. Factory Load Box — count ONLY active (non-ghost) orders
  const activeOrders = state.allOrders.filter(o => !isGhostOrder(o));
  const total = activeOrders.length;
  const approved = activeOrders.filter(o => o.status === 'APPROVED_IN_PRODUCTION' || o.status === 'TAMAMLANDI').length;
  const pct = total > 0 ? Math.round((approved / total) * 100) : 0;
  const ghostCount = state.allOrders.length - total;

  const kpiEl = document.getElementById('kpi-box-factory');
  if (kpiEl) {
    kpiEl.innerHTML = `
      <div class="kpi-row">
        <span class="kpi-label">Aktiv Yük</span>
        <span class="kpi-val">${pct}%</span>
      </div>
      <div class="prog-track">
        <div class="prog-bar" style="width:${pct}%;"></div>
      </div>
      <div class="kpi-subs">
        <span>Aktiv: ${total} sifariş</span>
        <span>Arxivdə: ${ghostCount} qalıq</span>
      </div>
    `;
  }

  // 2. Category Nav Cards
  const nav = document.getElementById('cat-nav-list');
  if (nav) {
    nav.innerHTML = CATEGORIES.map(c => {
      const ords = state.allOrders.filter(o => matchCategory(o, c.id)).filter(o => !isGhostOrder(o));
      const isAct = c.id === state.activeCategoryId;
      return `
        <div class="cat-card ${isAct ? 'active' : ''}" style="--cat-color: ${c.color};" onclick="selectCategory('${c.id}')">
          <div class="cat-top">
            <div class="cat-badge-icon">${c.iconSvg}</div>
            <div class="cat-info">
              <div class="cat-title">${c.name}</div>
              <div class="cat-orders">${ords.length} aktiv sifariş (${c.code})</div>
            </div>
          </div>
          <div class="cat-tags">
            ${c.stages.map(s => `<span class="cat-tag">${s.name}</span>`).join('')}
          </div>
        </div>
      `;
    }).join('');
  }
}

export function renderStageStrip() {
  const cat = getActiveCat();
  // Apply same ghost filter as the table so card counts match what manager sees
  const catOrders = state.allOrders
    .filter(o => matchCategory(o, cat.id))
    .filter(o => state.showArchive ? isGhostOrder(o) : !isGhostOrder(o));
  const container = document.getElementById('stage-row-container');
  if (!container) return;

  // "Hamısı" Card
  let html = `
    <div class="stage-card ${state.activeStageId === null ? 'active' : ''}" onclick="selectStage(null)">
      <div class="stage-card-top">
        <span class="stage-card-name">Hamısı</span>
        <span class="stage-card-count">${catOrders.length}</span>
      </div>
      <div class="stage-card-bar">
        <div class="stage-card-fill" style="width: 100%;"></div>
      </div>
      <div class="stage-card-bot">
        <span>Bütün mərhələlər</span>
        <b>${catOrders.length}</b>
      </div>
    </div>
  `;

  // Specific stages for this category
  cat.stages.forEach(st => {
    const inStage = catOrders.filter(o => matchStage(o, st.name));
    const count = inStage.length;
    const pct = catOrders.length > 0 ? Math.round((count / catOrders.length) * 100) : 0;
    const isAct = state.activeStageId === st.name;

    html += `
      <div class="stage-card ${isAct ? 'active' : ''}" onclick="selectStage('${st.name}')">
        <div class="stage-card-top">
          <span class="stage-card-name">${st.name}</span>
          <span class="stage-card-count">${count}</span>
        </div>
        <div class="stage-card-bar">
          <div class="stage-card-fill" style="width: ${pct}%;"></div>
        </div>
        <div class="stage-card-bot">
          <span>Yük: ${pct}%</span>
          <b>${count} sif.</b>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

export function renderDashboardTable() {
  const cat = getActiveCat();
  const searchInput = document.getElementById('search-query');
  const query = (searchInput ? searchInput.value : '').toLowerCase().trim();


  let list = state.allOrders.filter(o => matchCategory(o, cat.id));

  // Ghost / Archive Filter
  if (state.showArchive) {
    list = list.filter(o => isGhostOrder(o));
  } else {
    list = list.filter(o => !isGhostOrder(o));
  }

  // Strict Stage Filtering
  if (state.activeStageId !== null) {
    list = list.filter(o => matchStage(o, state.activeStageId));
  }



  // Smart Search: matches raw (004411), unpadded (4411), customer name (flexible az/en), product
  if (query) {
    const normQuery = normalizeAz(query);
    const unpadded = query.replace(/^0+/, '');
    list = list.filter(o => {
      const id = (o.id || '').toLowerCase();
      const unpaddedId = id.replace(/^0+/, '');
      const custNorm = normalizeAz(o.customerName);
      const pNameNorm = normalizeAz(o.productType && o.productType.name ? o.productType.name : '');
      const pIdNorm = normalizeAz(o.productType && o.productType.id ? o.productType.id : '');

      return id.includes(query) ||
             (unpadded.length > 0 && (id.includes(unpadded) || unpaddedId.includes(unpadded))) ||
             custNorm.includes(normQuery) ||
             pNameNorm.includes(normQuery) ||
             pIdNorm.includes(normQuery);
    });
  }

  const tbody = document.getElementById('dashboard-table-body');
  if (!tbody) return;

  if (list.length === 0) {
    const msg = state.showArchive
      ? 'Bu kateqoriyada arxiv / qalıq sifariş tapılmadı.'
      : 'Bu kateqoriyada aktiv sifariş tapılmadı. Arxiv / Qalıqlar bölməsinə baxın.';
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color: var(--t3);">${msg}</td></tr>`;
    return;
  }

  // Encapsulated Batching: render page chunks to prevent DOM overload
  const totalCount = list.length;
  const limit = query ? totalCount : (state.batchLimit || 50);
  const displayedList = list.slice(0, limit);

  let rowsHtml = displayedList.map(o => {
    const client = o.customerName || 'B2B Sifarişçi';
    const prod = o.productType ? o.productType.name : 'Standart Məhsul';
    const prodCode = o.productType ? o.productType.id : '';
    const totalQty = o.quantity || 500;
    const delivered = o.deliveredQuantity !== null && o.deliveredQuantity !== undefined ? o.deliveredQuantity : 0;
    const pct = Math.min(100, Math.round((delivered / totalQty) * 100));
    const stage = o.currentPhase || 'Dizayn & Sifariş';
    const ghost = isGhostOrder(o);



    const rowStyle = (ghost && state.showArchive) ? 'opacity:0.7;' : '';
    return `
      <tr onclick="openInspectModal('${o.id}')" style="${rowStyle}">
        <td><span style="font-family:var(--font-mono); font-size:11.5px; font-weight:600; color:var(--primary);">${o.id}</span></td>
        <td>
          <div style="font-weight:600; color:var(--t1);">${client}</div>
        </td>
        <td>
          <div style="color:var(--t1); font-weight:500;">${prod}</div>
          ${prodCode ? `<div style="font-family:var(--font-mono); font-size:10.5px; color:var(--t3);">${prodCode}</div>` : ''}
        </td>
        <td><span style="font-family:var(--font-mono); font-size:11.5px;">${totalQty} əd.</span></td>
        <td>
          <div class="qty-cell">
            <div class="qty-numbers">
              <span style="color:var(--t2);">${delivered} / ${totalQty}</span>
              <span style="color:var(--t3); font-size:10px;">${pct}%</span>
            </div>
            <div class="qty-track"><div class="qty-fill" style="width:${pct}%;"></div></div>
          </div>
        </td>


        <td><span style="font-family:var(--font-mono); font-size:11px; color:var(--t3);">${o.orderDate || '—'}</span></td>
        <td style="text-align: right;" onclick="event.stopPropagation()">
          <button class="btn btn-outline" style="padding: 3px 8px; font-size: 11px;" onclick="openInspectModal('${o.id}')">Bax</button>
        </td>
      </tr>
    `;
  }).join('');

  if (totalCount > displayedList.length) {
    rowsHtml += `
      <tr>
        <td colspan="7" style="text-align:center; padding: 16px; background: var(--s2);">
          <span style="color:var(--t2); font-size:12.5px; margin-right:12px;">Cəmi ${totalCount} sifarişdən ${displayedList.length} ədədi göstərilir.</span>
          <button class="btn btn-secondary" onclick="window.loadMoreOrders()" style="padding: 5px 14px; font-size:12px; cursor:pointer;">Daha 50 sifariş göstər ▾</button>
        </td>
      </tr>
    `;
  }

  tbody.innerHTML = rowsHtml;
}

export function loadMoreOrders() {
  state.batchLimit = (state.batchLimit || 50) + 50;
  renderDashboardTable();
}

export async function openInspectModal(orderId) {
  let o = state.allOrders.find(x => x.id === orderId);
  if (!o) {
    try {
      const res = await fetch(`/api/orders/${encodeURIComponent(orderId)}`);
      if (res.ok) {
        o = await res.json();
      }
    } catch (e) {}
  }
  if (!o) return;

  const client = o.customerName || 'Müştəri Məlumatı';
  const prod = o.productType ? o.productType.name : 'Məhsul';
  const totalQty = o.quantity || 500;
  const delivered = o.deliveredQuantity !== null && o.deliveredQuantity !== undefined ? o.deliveredQuantity : 0;
  const totalPct = totalQty > 0 ? Math.min(100, Math.round((delivered / totalQty) * 100)) : 0;

  const titleEl = document.getElementById('m-inspect-title');
  if (titleEl) titleEl.textContent = `Sifariş № ${o.id} — ${client}`;

  // Fetch or retrieve sub-orders
  let items = o.subItems || [];
  if (!items || items.length === 0) {
    try {
      items = await fetchOrderItems(orderId);
      o.subItems = items;
    } catch (err) {
      console.warn('Could not fetch sub-items for', orderId, err);
      items = [];
    }
  }

  const gridEl = document.getElementById('m-inspect-grid');
  if (gridEl) {
    gridEl.innerHTML = `
      <div class="modal-kv"><div class="modal-kv-k">Müştəri Təşkilat</div><div class="modal-kv-v" style="font-family:var(--font-main); font-size:12.5px; font-weight:600;">${client}</div></div>
      <div class="modal-kv"><div class="modal-kv-k">Məhsul Qrupu</div><div class="modal-kv-v" style="font-family:var(--font-main); font-size:12.5px;">${prod}</div></div>
      <div class="modal-kv"><div class="modal-kv-k">Ümumi Sifariş Həcmi</div><div class="modal-kv-v">${totalQty} ədəd</div></div>
      <div class="modal-kv"><div class="modal-kv-k">Təhvil Verilən Cəmi</div><div class="modal-kv-v" style="color:var(--success); font-weight:600;">${delivered} ədəd (${totalPct}%)</div></div>
      <div class="modal-kv"><div class="modal-kv-k">Konveyer / Xətt</div><div class="modal-kv-v" style="font-family:var(--font-main);">${o.conveyorLine || 'Standart'}</div></div>
      <div class="modal-kv"><div class="modal-kv-k">Sifariş Tarixi</div><div class="modal-kv-v">${o.orderDate || '—'}</div></div>
      <div class="modal-kv"><div class="modal-kv-k">Hədəf Təhvil Tarixi (Deadline)</div><div class="modal-kv-v" style="color:var(--warning); font-weight:600;">${o.deadline || '—'}</div></div>
      <div class="modal-kv"><div class="modal-kv-k">Xammal Təminatı (BOM)</div><div class="modal-kv-v" style="font-size:11.5px; font-family:var(--font-main); color:${o.materialShortage ? 'var(--danger)' : 'var(--success)'}; font-weight:600;">${o.materialShortage ? 'Xammal çatışmazlığı var' : 'Tam Təmin Olunub (100%)'}</div></div>
    `;
  }

  const countBadgeEl = document.getElementById('m-suborders-count');
  if (countBadgeEl) {
    countBadgeEl.textContent = `${items.length} alt-sifariş / növ`;
  }

  // Populate Suborders Table with each sub-order's individual stage
  const subTbody = document.getElementById('m-suborders-table-body');
  if (subTbody) {
    if (!items || items.length === 0) {
      subTbody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align:center; padding: 25px; color: var(--t3);">
            Bu sifariş üçün alt-məhsul qeydiyyatı tapılmadı.
          </td>
        </tr>
      `;
    } else {
      subTbody.innerHTML = items.map((item, idx) => {
        const lineNo = item.lineNum || (idx + 1);
        const pName = item.productName || prod;
        const pCode = item.productCode || '';
        const variant = item.variantDetails || 'Standart';
        const qty = item.quantity || 0;
        const deliv = (item.deliveredQuantity !== null && item.deliveredQuantity !== undefined) ? item.deliveredQuantity : 0;
        const itemPct = qty > 0 ? Math.min(100, Math.round((deliv / qty) * 100)) : 0;
        const phase = item.currentPhase || o.currentPhase || 'Dizayn & Sifariş';
        const status = item.status || (deliv >= qty ? 'TAMAMLANDI' : 'PROSESDƏ');

        let stageBadgeClass = 'badge-blue';
        const lowerPhase = phase.toLowerCase();
        if (lowerPhase.includes('kəsim') || lowerPhase.includes('kesim')) {
          stageBadgeClass = 'badge-amber';
        } else if (lowerPhase.includes('tikiş') || lowerPhase.includes('tikis')) {
          stageBadgeClass = 'badge-blue';
        } else if (lowerPhase.includes('ütü') || lowerPhase.includes('paket') || lowerPhase.includes('tamam')) {
          stageBadgeClass = 'badge-green';
        }

        let statusBadgeClass = 'badge-blue';
        if (status === 'TAMAMLANDI' || deliv >= qty) {
          statusBadgeClass = 'badge-green';
        } else if (status === 'GÖZLƏYİR' || status === 'PLAN') {
          statusBadgeClass = 'badge-neutral';
        }

        return `
          <tr>
            <td style="color:var(--t3); font-family:var(--font-mono); font-size:11px;">${lineNo}</td>
            <td>
              <div style="font-weight:600; color:var(--t1); font-size:12px;">${pName}</div>
              ${pCode ? `<div style="font-family:var(--font-mono); font-size:10px; color:var(--t3);">${pCode}</div>` : ''}
            </td>
            <td><span class="suborder-variant">${variant}</span></td>
            <td style="text-align:right; font-family:var(--font-mono); font-weight:600; font-size:12px;">${qty} əd.</td>
            <td>
              <div class="qty-cell">
                <div class="qty-numbers">
                  <span style="color:var(--t2);">${deliv} / ${qty}</span>
                  <span style="color:var(--t3); font-size:9.5px;">${itemPct}%</span>
                </div>
                <div class="qty-track"><div class="qty-fill" style="width:${itemPct}%;"></div></div>
              </div>
            </td>
            <td>
              <span class="badge ${stageBadgeClass}"><span class="badge-dot"></span>${phase}</span>
            </td>
            <td>
              <span class="badge ${statusBadgeClass}"><span class="badge-dot"></span>${status}</span>
            </td>
          </tr>
        `;
      }).join('');
    }
  }

  const modal = document.getElementById('inspect-modal');
  if (modal) modal.classList.add('open');
}

export function closeInspectModal(e) {
  if (e && e.target.id !== 'inspect-modal') return;
  const modal = document.getElementById('inspect-modal');
  if (modal) modal.classList.remove('open');
}
