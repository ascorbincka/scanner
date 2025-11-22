from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Set
import uvicorn

app = FastAPI(title="Blocklist Service")

# позже заменить на SQLite, пока просто память
blocklist: Set[str] = set()


class BlockRequest(BaseModel):
    ip: str


@app.get("/blocklist", response_model=List[str])
def get_blocklist():
    """
    Вернуть все заблокированные IP.
    """
    return sorted(blocklist)


@app.post("/block")
def add_block(req: BlockRequest):
    """
    Добавить IP в blocklist.
    При добавлении — логируем в консоль.
    """
    if req.ip not in blocklist:
        blocklist.add(req.ip)
        print(f"BLOCK IP {req.ip}")
    return {"status": "ok", "ip": req.ip, "total": len(blocklist)}


if __name__ == "__main__":
    # Отдельный сервис крутится на 8001 порту
    uvicorn.run("blocklist_service:app", host="127.0.0.1", port=8001, reload=True)
