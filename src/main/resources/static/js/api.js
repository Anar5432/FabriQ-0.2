/* ══════════════════════════════════════
   REST API CLIENT
══════════════════════════════════════ */

export async function fetchOrders() {
  const res = await fetch('/api/orders');
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return await res.json();
}

export async function checkMaterials(productTypeId, quantity) {
  const res = await fetch('/api/planning/check-materials', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ productTypeId, quantity })
  });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return await res.json();
}

export async function planForward(payload) {
  const res = await fetch('/api/planning/forward', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return await res.json();
}

export async function planBackward(payload) {
  const res = await fetch('/api/planning/backward', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return await res.json();
}

export async function triggerSync() {
  const res = await fetch('/api/sync');
  if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  return await res.json();
}

export async function fetchOrderItems(orderId) {
  try {
    const res = await fetch(`/api/orders/${encodeURIComponent(orderId)}/items`);
    if (!res.ok) return [];
    return await res.json();
  } catch (e) {
    console.error('Failed to fetch order items:', e);
    return [];
  }
}
