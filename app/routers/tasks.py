from fastapi import APIRouter
from fastapi.responses import JSONResponse

from typing import List, Union

from app.functions.tasks import TasksListHandler, CreateTaskHandler, UpdateTaskHandler, DeleteTaskHandler

from app.schemas.tasks import Task, CreateUpdateTask, Attachment

from app.exceptions import TaskDoesNotExistsException, TaskTitleDuplicateException

router = APIRouter()


@router.get("/tasks", tags=["tasks"])
async def tasks_list() -> List[Task]:

    return await TasksListHandler().handle()


@router.post("/tasks", tags=["tasks"])
async def create_task(model: CreateUpdateTask) -> Union[Task, JSONResponse]:

    try:

        return await CreateTaskHandler().handle(model)

    except TaskTitleDuplicateException:

        return JSONResponse(status_code=400, content={"message": "Title is already taken"})


@router.put("/tasks/{task_id}", tags=["tasks"])
async def update_task(task_id: int, model: CreateUpdateTask) -> Union[Task, JSONResponse]:

    try:

        return await UpdateTaskHandler().handle(task_id, model)

    except (TaskTitleDuplicateException, TaskDoesNotExistsException) as e:

        if e == TaskTitleDuplicateException:

            return JSONResponse(status_code=400, content={"message": "Title is already taken"})

        elif e == TaskDoesNotExistsException:

            return JSONResponse(status_code=404, content={"message": "Task does not exist"})


@router.delete("/tasks/{task_id}", tags=["tasks"])
async def delete_task(task_id: int) -> Union[None, JSONResponse]:

    try:

        return await DeleteTaskHandler().handle(task_id)

    except TaskDoesNotExistsException:

        return JSONResponse(status_code=404, content={"message": "Task does not exist"})


@router.post("/tasks/{task_id}/attachments}", tags=["tasks"])
async def create_attachment(task_id: int):
    return


@router.delete("/tasks/{task_id}/attachments/{attachment_id}", tags=["tasks"])
async def delete_attachment(task_id: int, attachment_id: int):
    return
