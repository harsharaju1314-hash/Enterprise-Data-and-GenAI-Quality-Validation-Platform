// Enterprise Web Application & Dashboard Interaction Script

document.addEventListener('DOMContentLoaded', () => {
  // Check auth
  const token = localStorage.getItem('auth_token');
  const username = localStorage.getItem('username') || 'User';
  const role = localStorage.getItem('role') || 'Admin';

  const userDisplay = document.getElementById('user-display');
  const roleDisplay = document.getElementById('role-display');
  const btnLogout = document.getElementById('btn-logout');

  if (userDisplay) userDisplay.textContent = username;
  if (roleDisplay) {
    roleDisplay.textContent = role;
    if (role === 'Admin') roleDisplay.className = 'badge badge-platinum';
    else if (role === 'Analyst') roleDisplay.className = 'badge badge-gold';
    else roleDisplay.className = 'badge badge-silver';
  }

  if (btnLogout) {
    btnLogout.addEventListener('click', () => {
      localStorage.clear();
      window.location.href = 'index.html';
    });
  }

  // Dashboard logic
  if (document.getElementById('customers-table')) {
    initDashboard();
  }

  // RAG Assistant logic
  if (document.getElementById('chat-form')) {
    initRagAssistant();
  }
});

async function initDashboard() {
  await loadMetrics();
  await loadCustomers();

  document.getElementById('btn-apply-filters')?.addEventListener('click', () => {
    loadCustomers();
  });

  document.getElementById('btn-reset-filters')?.addEventListener('click', () => {
    document.getElementById('filter-tier').value = '';
    document.getElementById('filter-region').value = '';
    document.getElementById('search-input').value = '';
    const badge = document.getElementById('drilldown-badge');
    if (badge) badge.style.display = 'none';
    loadCustomers();
  });

  document.getElementById('btn-refresh')?.addEventListener('click', () => {
    loadMetrics();
    loadCustomers();
  });

  document.getElementById('btn-export')?.addEventListener('click', () => {
    exportToCsv();
  });

  document.getElementById('search-input')?.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') loadCustomers();
  });
}

async function loadMetrics() {
  try {
    const res = await fetch('/api/metrics');
    const data = await res.json();
    if (res.ok) {
      document.getElementById('kpi-gross-volume').textContent = `$${Number(data.gross_transaction_volume || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
      document.getElementById('kpi-total-txns').textContent = data.total_transactions || 0;
      document.getElementById('kpi-open-requests').textContent = data.open_service_requests || 0;
      document.getElementById('kpi-closed-requests').textContent = data.closed_service_requests || 0;
      document.getElementById('kpi-avg-csat').textContent = data.avg_csat ? `${data.avg_csat} / 5.0` : 'N/A';
    }
  } catch (err) {
    console.error('Failed to load metrics:', err);
  }
}

async function loadCustomers() {
  const tier = document.getElementById('filter-tier')?.value || '';
  const region = document.getElementById('filter-region')?.value || '';
  const query = document.getElementById('search-input')?.value.toLowerCase().trim() || '';

  const tbody = document.getElementById('customers-tbody');
  const emptyState = document.getElementById('empty-state');
  const recordCount = document.getElementById('record-count');

  let url = '/api/customers?';
  if (tier) url += `tier=${encodeURIComponent(tier)}&`;
  if (region) url += `region=${encodeURIComponent(region)}&`;

  try {
    const res = await fetch(url);
    const result = await res.json();
    let data = result.data || [];

    // Client search filter
    if (query) {
      data = data.filter(c => 
        c.full_name.toLowerCase().includes(query) ||
        c.customer_id.toLowerCase().includes(query) ||
        c.email.toLowerCase().includes(query)
      );
    }

    recordCount.textContent = data.length;
    tbody.innerHTML = '';

    if (data.length === 0) {
      emptyState.style.display = 'block';
      return;
    }

    emptyState.style.display = 'none';

    data.forEach(c => {
      const tr = document.createElement('tr');
      const badgeClass = `badge-${c.tier.toLowerCase()}`;
      tr.innerHTML = `
        <td><strong>${c.customer_id}</strong></td>
        <td>${c.full_name}</td>
        <td>${c.email}</td>
        <td><span class="badge ${badgeClass}">${c.tier}</span></td>
        <td>${c.region}</td>
        <td>${c.account_created_date}</td>
        <td><span style="color: ${c.status === 'Active' ? '#006644' : '#de350b'}">${c.status}</span></td>
        <td>
          <button class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.78rem;" onclick="drillDownCustomer('${c.customer_id}', '${c.tier}')">Drill-Down</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error('Failed to fetch customers:', err);
  }
}

function drillDownCustomer(customerId, tier) {
  const badge = document.getElementById('drilldown-badge');
  if (badge) {
    badge.textContent = `Drill-down: ${customerId} (${tier})`;
    badge.style.display = 'inline-block';
  }
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.value = customerId;
    loadCustomers();
  }
}

function exportToCsv() {
  const role = localStorage.getItem('role') || 'Admin';
  if (role === 'Support') {
    alert('Access Denied: Support role is not authorized for bulk data exports.');
    return;
  }
  alert('Export initiated: Generating verified analytical CSV snapshot...');
}

function initRagAssistant() {
  const form = document.getElementById('chat-form');
  const input = document.getElementById('chat-input');
  const messagesContainer = document.getElementById('chat-messages');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    // Append user message
    const userMsg = document.createElement('div');
    userMsg.className = 'message message-user';
    userMsg.textContent = question;
    messagesContainer.appendChild(userMsg);
    input.value = '';
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Show typing state
    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'message message-ai';
    loadingMsg.textContent = 'Analyzing verified knowledge base...';
    messagesContainer.appendChild(loadingMsg);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    try {
      const res = await fetch('/api/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await res.json();

      loadingMsg.innerHTML = `
        <div>${data.answer}</div>
        ${data.source_document ? `<div class="evidence-tag"><strong>Source:</strong> ${data.source_document} ${data.confidence > 0 ? `| Confidence: ${(data.confidence * 100).toFixed(0)}%` : ''}</div>` : ''}
        ${data.evidence ? `<div style="font-size: 0.75rem; color: #6b778c; margin-top: 0.2rem;"><em>Evidence:</em> ${data.evidence}</div>` : ''}
      `;
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } catch (err) {
      loadingMsg.textContent = 'Error connecting to RAG backend. Please try again.';
    }
  });
}
