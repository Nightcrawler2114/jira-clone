from fastapi import APIRouter

router = APIRouter()


@router.get("/tasks", tags=["tasks"])
async def tasks_list():
    return


@router.post("/tasks", tags=["tasks"])
async def create_task():
    return


@router.put("/tasks/{task_id}", tags=["tasks"])
async def update_task(task_id: int):
    return


@router.delete("/tasks/{task_id}", tags=["tasks"])
async def delete_task(task_id: int):
    return


@router.get("/tasks/{task_id}/attachments", tags=["tasks"])
async def attachments_list(task_id: int):
    return


@router.post("/tasks/{task_id}/attachments}", tags=["tasks"])
async def create_attachment(task_id: int):
    return


@router.delete("/tasks/{task_id}/attachments/{attachment_id}", tags=["tasks"])
async def delete_attachment(task_id: int, attachment_id: int):
    return
