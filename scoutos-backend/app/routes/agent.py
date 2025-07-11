from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def agent_status():
    return {"status": "Agent module placeholder"}
