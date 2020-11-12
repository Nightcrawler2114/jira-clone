from fastapi import APIRouter
from fastapi.responses import JSONResponse

from typing import List, Union

from app.functions.tasks import (
    TasksListHandler,
    CreateTaskHandler,
    UpdateTaskHandler,
    DeleteTaskHandler,
    CreateAttachmentHandler,
    DeleteAttachmentHandler
)

from app.schemas.tasks import Task, CreateUpdateTask, Attachment, CreateAttachment

from app.exceptions import (
    TaskDoesNotExistsException,
    TaskTitleDuplicateException,
    ReferenceUserDoesNotExistException,
    ReferenceProjectDoesNotExistException,
    AttachmentDoesNotExistException
)

router = APIRouter()


@router.get("/tasks", tags=["tasks"])
async def tasks_list() -> List[Task]:

    return await TasksListHandler().handle()


@router.post("/tasks", tags=["tasks"])
async def create_task(model: CreateUpdateTask) -> Union[Task, JSONResponse]:

    try:

        return await CreateTaskHandler().handle(model)

    except (
            TaskTitleDuplicateException,
            ReferenceUserDoesNotExistException,
            ReferenceProjectDoesNotExistException
    ) as e:

        if str(e) == 'Title is already taken':

            return JSONResponse(status_code=400, content={"message": str(e)})

        elif (
                str(e) == 'Reference project does not exist' or
                str(e) == 'Reference user does not exist'
        ):

            return JSONResponse(status_code=404, content={"message": str(e)})


@router.put("/tasks/{task_id}", tags=["tasks"])
async def update_task(task_id: int, model: CreateUpdateTask) -> Union[Task, JSONResponse]:

    try:

        return await UpdateTaskHandler().handle(task_id, model)

    except (
            TaskTitleDuplicateException,
            TaskDoesNotExistsException,
            ReferenceUserDoesNotExistException,
            ReferenceProjectDoesNotExistException
    ) as e:

        if str(e) == 'Title is already taken':

            return JSONResponse(status_code=400, content={"message": str(e)})

        elif (
                str(e) == 'Task does not exists' or
                str(e) == 'Reference project does not exist' or
                str(e) == 'Reference user does not exist'
        ):

            return JSONResponse(status_code=404, content={"message": str(e)})


@router.delete("/tasks/{task_id}", tags=["tasks"])
async def delete_task(task_id: int) -> Union[None, JSONResponse]:

    try:

        return await DeleteTaskHandler().handle(task_id)

    except TaskDoesNotExistsException as e:

        return JSONResponse(status_code=404, content={"message": str(e)})


@router.post("/tasks/{task_id}/attachments}", tags=["tasks"])
async def create_attachment(task_id: int, model: CreateAttachment):

    try:

        return await CreateAttachmentHandler().handle(model)

    except TaskDoesNotExistsException as e:

        return JSONResponse(status_code=404, content={"message": str(e)})


@router.delete("/tasks/{task_id}/attachments/{attachment_id}", tags=["tasks"])
async def delete_attachment(task_id: int, attachment_id: int):

    try:

        return await DeleteAttachmentHandler().handle(attachment_id)

    except AttachmentDoesNotExistException as e:

        return JSONResponse(status_code=404, content={"message": str(e)})

