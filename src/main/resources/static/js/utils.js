import { CATEGORIES } from './config.js';
import { state } from './state.js';

/* ──────────────────────────────────────────
   GHOST ORDER DETECTION (3-Month / 90-Day Rule)
   An order is a ghost/remnant if BOTH conditions are true:
   1. orderDate is older than 90 days (3 months)
   2. deliveredQuantity/quantity >= 98% OR remaining <= 2 pieces
   These orders clutter active production and distort planning.
   ────────────────────────────────────────── */
export function isGhostOrder(o) {
  const NINETY_DAYS_MS = 90 * 24 * 60 * 60 * 1000;
  const orderDateMs = o.orderDate ? new Date(o.orderDate).getTime() : 0;
  const isOldOrder = orderDateMs > 0 && (Date.now() - orderDateMs) > NINETY_DAYS_MS;
  if (!isOldOrder) return false; // Recent orders are NEVER ghosts, regardless of delivery %

  const totalQty = o.quantity || 0;
  const delivered = o.deliveredQuantity != null ? o.deliveredQuantity : 0;
  const remaining = totalQty - delivered;
  const deliveryPct = totalQty > 0 ? delivered / totalQty : 0;

  return deliveryPct >= 0.98 || remaining <= 2;
}

export function matchCategory(o, catId) {
  const cLine = o.conveyorLine || (o.productType ? o.productType.category : 'Workwear');
  if (catId === 'Underwear-boxer') return cLine.toLowerCase().includes('underwear');
  if (catId === 'Socks') return cLine.toLowerCase().includes('sock');
  return !cLine.toLowerCase().includes('underwear') && !cLine.toLowerCase().includes('sock');
}

export function matchStage(o, stageName) {
  const p = (o.currentPhase || 'Dizayn & Sifariş').toLowerCase();
  const s = stageName.toLowerCase();
  if (s.includes('paket') || s.includes('hazır') || s.includes('anbar')) {
    return p.includes('paket') || p.includes('hazır') || p.includes('anbar');
  }
  if (s.includes('dizayn') || s.includes('sifariş')) {
    return p.includes('dizayn') || p.includes('sifariş');
  }
  if (s.includes('material') || s.includes('təchizat') || s.includes('techizat')) {
    return p.includes('material') || p.includes('təchizat') || p.includes('techizat');
  }
  if (s.includes('kəsim') || s.includes('kesim')) {
    return p.includes('kəsim') || p.includes('kesim');
  }
  if (s.includes('hörgü') || s.includes('knitting') || s.includes('horgu')) {
    return p.includes('hörgü') || p.includes('knitting') || p.includes('horgu');
  }
  if (s.includes('forma') || s.includes('boarding')) {
    return p.includes('forma') || p.includes('boarding');
  }
  if (s.includes('tikiş') || s.includes('tikis') || s.includes('sewing') || s.includes('closing')) {
    return p.includes('tikiş') || p.includes('tikis') || p.includes('sewing') || p.includes('closing');
  }
  return p.includes(s) || s.includes(p);
}

export function getActiveCat() {
  return CATEGORIES.find(c => c.id === state.activeCategoryId) || CATEGORIES[0];
}

export function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.style.display = 'block';
  setTimeout(() => { t.style.display = 'none'; }, 3500);
}

export function normalizeAz(str) {
  if (!str) return '';
  return str.toString().normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/ə/g, 'e')
    .replace(/ı/g, 'i')
    .replace(/\s+/g, ' ')
    .trim();
}
