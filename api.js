// api.js — ES module
const BACKEND_URL = "http://127.0.0.1:8000";

// допустимые роли (должны совпадать с main.py)
const VALID_ROLES = ["admin", "analyst", "observer"];
const ROLE_KEY = "psp_role";

function getRole() {
  const raw = (localStorage.getItem(ROLE_KEY) || "observer").toLowerCase();
  return VALID_ROLES.includes(raw) ? raw : "observer";
}

async function apiRequest(path, options = {}) {
  const url = `${BACKEND_URL}${path}`;

  const headers = {
    "Content-Type": "application/json",
    "X-Role": getRole(), // 🔥 КРИТИЧНО
    ...(options.headers || {}),
  };

  const resp = await fetch(url, {
    ...options,
    headers,
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`HTTP ${resp.status}: ${text}`);
  }

  if (resp.status === 204) return null;
  return resp.json();
}

// ===== Incidents =====
export async function getIncidents(status = null) {
  const qs = status ? `?status=${encodeURIComponent(status)}` : "";
  return apiRequest(`/incidents${qs}`, { method: "GET" });
}

export async function updateIncidentStatus(incidentId, newStatus) {
  return apiRequest(`/incidents/${incidentId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status: newStatus }),
  });
}

// ===== Blocklist / Block Requests =====
export async function createBlockRequest(incidentId, reason, ttl_seconds = undefined) {
  const body = { incident_id: incidentId, reason };
  if (ttl_seconds !== undefined) body.ttl_seconds = ttl_seconds;

  return apiRequest(`/block-requests`, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function executeBlockRequest(requestId) {
  return apiRequest(`/block-requests/${requestId}/execute`, {
    method: "POST",
  });
}

export async function getBlockRequests() {
  return apiRequest(`/block-requests`, { method: "GET" });
}

// ===== Events =====
export async function getRecentEvents() {
  return apiRequest(`/events`, { method: "GET" });
}

// ===== Analytics =====
export async function getAnalyticsSummary(period = "day") {
  return apiRequest(`/analytics/summary?period=${encodeURIComponent(period)}`, {
    method: "GET",
  });
}

export async function getAnalyticsTimeseries(period = "day") {
  return apiRequest(`/analytics/timeseries?period=${encodeURIComponent(period)}`, {
    method: "GET",
  });
}

