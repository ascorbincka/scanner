from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   
from pydantic import BaseModel
from typing import List, Set
import uvicorn

app = FastAPI(title="Blocklist Service")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

blocklist: Set[str] = set()


class BlockRequest(BaseModel):
    ip: str


@app.get("/blocklist", response_model=List[str])
def get_blocklist():
    return sorted(blocklist)


@app.post("/block")
def add_block(req: BlockRequest):
    if req.ip not in blocklist:
        blocklist.add(req.ip)
        print(f"BLOCK IP {req.ip}")
    return {"status": "ok", "ip": req.ip, "total": len(blocklist)}


if __name__ == "__main__":
    uvicorn.run("blocklist_service:app", host="127.0.0.1", port=8001, reload=True)
