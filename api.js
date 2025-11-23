// frontend/api.js
const API_BASE = "http://127.0.0.1:8000";   // main.py
const BLOCKLIST_API = "http://127.0.0.1:8001"; // blocklist_service.py

// список инцидентов
async function getIncidents() {
    const resp = await fetch(`${API_BASE}/incidents`);
    if (!resp.ok) {
        throw new Error("Ошибка при запросе /incidents: " + resp.status);
    }
    return await resp.json();
}

// создать запрос на блокировку по id инцидента
async function createBlockRequest(incidentId) {
    const body = {
        incident_id: incidentId,
        reason: "Blocked from UI",
    };

    const resp = await fetch(`${API_BASE}/block-requests`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    if (!resp.ok) {
        const text = await resp.text();
        throw new Error("Ошибка /block-requests: " + resp.status + " " + text);
    }

    return await resp.json();
}

// список заблокированных ip из blocklist-сервиса
async function getBlocklist() {
    const resp = await fetch(`${BLOCKLIST_API}/blocklist`);
    if (!resp.ok) {
        throw new Error("Ошибка /blocklist: " + resp.status);
    }
    return await resp.json();
}
