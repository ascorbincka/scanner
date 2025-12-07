const BACKEND_URL = "http://127.0.0.1:8000";

async function apiRequest(path, options = {}) {
  const url = `${BACKEND_URL}${path}`;
  const resp = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`HTTP ${resp.status}: ${text}`);
  }

  if (resp.status === 204) {
    return null;
  }

  return resp.json();
}

export async function getIncidents(status = null) {
  const qs = status ? `?status=${encodeURIComponent(status)}` : "";
  return apiRequest(`/incidents${qs}`, {
    method: "GET",
  });
}

// Обновление статуса инцидента
export async function updateIncidentStatus(incidentId, newStatus) {
  return apiRequest(`/incidents/${incidentId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status: newStatus }),
  });
}

// Создать запрос на блокировку по инциденту
export async function createBlockRequest(incidentId, reason) {
  return apiRequest(`/block-requests`, {
    method: "POST",
    body: JSON.stringify({
      incident_id: incidentId,
      reason: reason,
    }),
  });
}

// Выполнить запрос блокировки 
export async function executeBlockRequest(requestId) {
  return apiRequest(`/block-requests/${requestId}/execute`, {
    method: "POST",
  });
}

// Получить список всех запросов на блокировку
export async function getBlockRequests() {
  return apiRequest(`/block-requests`, {
    method: "GET",
  });
}

// Ожидается backend-эндпоинт
export async function getRecentEvents(limit = 50) {
  const qs = `?limit=${limit}`;
  return apiRequest(`/events${qs}`, {
    method: "GET",
  });
}
