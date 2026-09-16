let allWorkers = [];
let currentOrder = null;
let currentAssignStageId = null;

document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(m => m.classList.remove('active'));
            item.classList.add('active');
            
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.getElementById(item.dataset.target).classList.add('active');
        });
    });

    // Initial Data Fetch
    fetchWorkers();
    fetchOrders();
});

// ========================
// WORKER PROFILES
// ========================
async function fetchWorkers() {
    try {
        const res = await fetch('/api/workers');
        allWorkers = await res.json();
        renderWorkers();
    } catch (err) {
        console.error("Error fetching workers", err);
    }
}

function renderWorkers() {
    const container = document.getElementById('workers-container');
    container.innerHTML = '';
    
    allWorkers.forEach(w => {
        const card = document.createElement('div');
        card.className = 'worker-card glass-card';
        
        let abilitiesHtml = w.abilities.map(a => `
            <div class="ability-tag">
                <span>Stage: ${a.stage_id}</span>
                <span class="cap">${a.daily_capacity}/day</span>
            </div>
        `).join('');

        card.innerHTML = `
            <div class="worker-header">
                <div class="avatar">${w.name.charAt(0)}</div>
                <div>
                    <h3>${w.name}</h3>
                    <p style="font-size: 0.85rem; color: var(--text-secondary)">ID: ${w.worker_id}</p>
                </div>
            </div>
            <div class="worker-abilities">
                ${abilitiesHtml || '<p style="font-size: 0.85rem; color: var(--text-secondary)">No specific abilities registered.</p>'}
            </div>
        `;
        container.appendChild(card);
    });
}

// ========================
// PLANNING DETAILS
// ========================
async function fetchOrders() {
    try {
        const res = await fetch('/api/orders');
        const orders = await res.json();
        
        const container = document.getElementById('orders-list');
        container.innerHTML = '';
        
        orders.forEach(o => {
            const item = document.createElement('div');
            item.className = 'order-item';
            item.onclick = () => selectOrder(o.id, item);
            item.innerHTML = `
                <h4>${o.id}</h4>
                <p>${o.product_type} - ${o.quantity} units</p>
                <div class="order-tags">
                    <span class="tag" style="background: ${o.color}20; color: ${o.color}">${o.status}</span>
                </div>
            `;
            container.appendChild(item);
        });
    } catch (err) {
        console.error("Error fetching orders", err);
    }
}

async function selectOrder(orderId, element) {
    document.querySelectorAll('.order-item').forEach(i => i.classList.remove('active'));
    element.classList.add('active');
    
    currentOrder = orderId;
    document.getElementById('order-details-container').style.display = 'flex';
    
    await fetchOrderDetails(orderId);
}

async function fetchOrderDetails(orderId) {
    try {
        const res = await fetch(`/api/planning/details/${orderId}`);
        const data = await res.json();
        
        // 1. Header
        document.getElementById('order-header').innerHTML = `
            <div>
                <h2>Order ${data.order.id} - ${data.order.product_type}</h2>
                <p style="color: var(--text-secondary); margin-top: 4px;">Quantity: ${data.order.quantity} | Deadline: ${data.order.deadline}</p>
            </div>
            <div class="order-tags">
                <span class="tag" style="background: ${data.order.color}20; color: ${data.order.color}">${data.order.status}</span>
            </div>
        `;
        
        // 2. Materials
        const matTbody = document.getElementById('materials-tbody');
        matTbody.innerHTML = '';
        data.materials.forEach(m => {
            const shortageClass = m.shortage > 0 ? 'shortage' : 'ok';
            const shortageText = m.shortage > 0 ? `Missing ${m.shortage}` : 'In Stock';
            matTbody.innerHTML += `
                <tr>
                    <td>${m.material_name}</td>
                    <td>${m.needed_for_this_order} ${m.unit}</td>
                    <td>${m.stock_in_warehouse + m.stock_in_production} ${m.unit}</td>
                    <td class="${shortageClass}">${shortageText}</td>
                </tr>
            `;
        });
        
        // 3. Timeline & Assignments
        const timeline = document.getElementById('timeline-container');
        timeline.innerHTML = '';
        data.assignments.forEach(a => {
            const isAssigned = a.assigned_worker !== 'Unassigned';
            const actionBtn = isAssigned ? 
                `<button class="btn btn-secondary" onclick="openAssignModal('${a.stage_id}')">Reassign</button>` : 
                `<button class="btn btn-primary" onclick="openAssignModal('${a.stage_id}')">Assign Worker</button>`;
                
            let datesHtml = '';
            if (isAssigned && a.start_date && a.end_date) {
                const s = new Date(a.start_date).toLocaleDateString();
                const e = new Date(a.end_date).toLocaleDateString();
                datesHtml = `<div class="date-badge">${s} ➔ ${e} (${a.days_required} days)</div>`;
            }
            
            timeline.innerHTML += `
                <div class="timeline-step">
                    <div class="step-info">
                        <h4>Step ${a.step_order}: Stage ${a.stage_id}</h4>
                        <p>Worker: <strong>${a.assigned_worker}</strong> ${isAssigned ? `(Goal: ${a.daily_goal}/day)` : ''}</p>
                    </div>
                    <div class="step-meta">
                        ${datesHtml}
                        ${actionBtn}
                    </div>
                </div>
            `;
        });
        
    } catch (err) {
        console.error("Error fetching details", err);
    }
}

// ========================
// ASSIGNMENT MODAL
// ========================
function openAssignModal(stageId) {
    currentAssignStageId = stageId;
    document.getElementById('assign-modal-stage-info').innerText = `Selecting worker for Stage: ${stageId}`;
    
    // Filter workers who have this stage ability
    const select = document.getElementById('worker-select');
    select.innerHTML = '';
    
    const capableWorkers = allWorkers.filter(w => w.abilities.some(a => a.stage_id === stageId));
    
    if (capableWorkers.length === 0) {
        select.innerHTML = `<option disabled selected>No workers found with this ability</option>`;
    } else {
        capableWorkers.forEach(w => {
            select.innerHTML += `<option value="${w.worker_id}">${w.name}</option>`;
        });
    }
    
    document.getElementById('assign-modal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('assign-modal').style.display = 'none';
}

async function submitAssignment() {
    const workerId = document.getElementById('worker-select').value;
    if (!workerId || !currentOrder || !currentAssignStageId) return;
    
    try {
        const res = await fetch('/api/planning/assign_worker', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                order_id: currentOrder,
                stage_id: currentAssignStageId,
                worker_id: workerId
            })
        });
        
        if (res.ok) {
            closeModal();
            // Refresh order details to see new timeline
            fetchOrderDetails(currentOrder);
        } else {
            const err = await res.json();
            alert("Error: " + err.detail);
        }
    } catch (err) {
        console.error("Assignment failed", err);
    }
}
