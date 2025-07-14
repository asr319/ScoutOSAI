from __future__ import annotations

from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    """Track active WebSocket connections by user."""

    def __init__(self) -> None:
        self.connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        await websocket.accept()
        self.connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int) -> None:
        conns = self.connections.get(user_id)
        if conns and websocket in conns:
            conns.remove(websocket)
            if not conns:
                del self.connections[user_id]

    async def send_personal_message(self, message: Dict, user_id: int) -> None:
        for ws in self.connections.get(user_id, []):
            await ws.send_json(message)

    async def broadcast(self, message: Dict) -> None:
        for user_id in list(self.connections.keys()):
            await self.send_personal_message(message, user_id)


manager = ConnectionManager()
