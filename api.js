const API_BASE = "http://127.0.0.1:8000"; 

async function getIncidents() {
    const resp = await fetch(`${API_BASE}/incidents`);
    return await resp.json();
}

async function getBlocklist() {
    const resp = await fetch(`${API_BASE}/blocklist`);
    return await resp.json();
}

async function blockIp(ip) {
    await fetch(`${API_BASE}/block-requests`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ ip })
    });
}
