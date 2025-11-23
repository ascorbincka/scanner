from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, IPvAnyAddress
from typing import List, Optional
from datetime import datetime
import itertools

app = FastAPI(
    title="Система защиты от атаки сканирования сетевых портов (Port Scan Protection)",
)

_incident_id_gen = itertools.count(1)
_block_request_id_gen = itertools.count(1)

EVENTS = []         
INCIDENTS = []       
BLOCK_REQUESTS = []  

SCAN_STATE = {}      

PORT_SCAN_THRESHOLD = 3

class Event(BaseModel):
    source_ip: IPvAnyAddress
    dest_ip: IPvAnyAddress
    dest_port: int
    protocol: str = "TCP"
    timestamp: Optional[datetime] = None


class Incident(BaseModel):
    id: int
    source_ip: IPvAnyAddress
    ports: List[int]
    created_at: datetime
    status: str = "open"  


class BlockRequest(BaseModel):
    id: int
    incident_id: int
    source_ip: IPvAnyAddress
    reason: str
    created_at: datetime


class BlockRequestCreate(BaseModel):
    incident_id: int
    reason: str


def detect_port_scan(event: Event) -> Optional[Incident]:

    ip = str(event.source_ip)
    port = event.dest_port

    ports = SCAN_STATE.setdefault(ip, set())
    ports.add(port)

    if len(ports) >= PORT_SCAN_THRESHOLD:
        incident_id = next(_incident_id_gen)
        incident = Incident(
            id=incident_id,
            source_ip=event.source_ip,
            ports=sorted(list(ports)),
            created_at=datetime.utcnow(),
            status="open",
        )
        INCIDENTS.append(incident.dict())

        SCAN_STATE[ip] = set()

        return incident

    return None


@app.post("/events")
def create_event(event: Event):
    """
    Приём события от сенсора/системы мониторинга.
    """
    # Добавим timestamp, если не передали
    if event.timestamp is None:
        event.timestamp = datetime.utcnow()

    EVENTS.append(event.dict())

    incident = detect_port_scan(event)

    if incident:
        return {"status": "incident_created", "incident": incident}

    return {"status": "ok"}


@app.get("/incidents", response_model=List[Incident])
def list_incidents(status: Optional[str] = None):
   
    if status:
        return [Incident(**i) for i in INCIDENTS if i.get("status") == status]
    return [Incident(**i) for i in INCIDENTS]


@app.post("/block-requests", response_model=BlockRequest)
def create_block_request(body: BlockRequestCreate):
 
    incident = next((i for i in INCIDENTS if i["id"] == body.incident_id), None)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    block_id = next(_block_request_id_gen)

    block_req = BlockRequest(
        id=block_id,
        incident_id=body.incident_id,
        source_ip=incident["source_ip"],
        reason=body.reason,
        created_at=datetime.utcnow(),
    )

    BLOCK_REQUESTS.append(block_req.dict())
    
    incident["status"] = "blocked"

    return block_req


@app.get("/")
def root():
    return {"message": "Port Scan Protection Backend is running"}
