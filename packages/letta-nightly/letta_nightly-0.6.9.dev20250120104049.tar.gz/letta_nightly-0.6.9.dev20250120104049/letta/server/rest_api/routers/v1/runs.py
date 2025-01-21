from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from letta.orm.enums import JobType
from letta.orm.errors import NoResultFound
from letta.schemas.enums import JobStatus, MessageRole
from letta.schemas.letta_message import LettaMessageUnion
from letta.schemas.openai.chat_completion_response import UsageStatistics
from letta.schemas.run import Run
from letta.server.rest_api.utils import get_letta_server
from letta.server.server import SyncServer

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("/", response_model=List[Run], operation_id="list_runs")
def list_runs(
    server: "SyncServer" = Depends(get_letta_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from header, default to None if not present
):
    """
    List all runs.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    return [Run.from_job(job) for job in server.job_manager.list_jobs(actor=actor, job_type=JobType.RUN)]


@router.get("/active", response_model=List[Run], operation_id="list_active_runs")
def list_active_runs(
    server: "SyncServer" = Depends(get_letta_server),
    user_id: Optional[str] = Header(None, alias="user_id"),  # Extract user_id from header, default to None if not present
):
    """
    List all active runs.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    active_runs = server.job_manager.list_jobs(actor=actor, statuses=[JobStatus.created, JobStatus.running], job_type=JobType.RUN)

    return [Run.from_job(job) for job in active_runs]


@router.get("/{run_id}", response_model=Run, operation_id="get_run")
def get_run(
    run_id: str,
    user_id: Optional[str] = Header(None, alias="user_id"),
    server: "SyncServer" = Depends(get_letta_server),
):
    """
    Get the status of a run.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    try:
        job = server.job_manager.get_job_by_id(job_id=run_id, actor=actor)
        return Run.from_job(job)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Run not found")


@router.get("/{run_id}/messages", response_model=List[LettaMessageUnion], operation_id="get_run_messages")
async def get_run_messages(
    run_id: str,
    server: "SyncServer" = Depends(get_letta_server),
    user_id: Optional[str] = Header(None, alias="user_id"),
    cursor: Optional[str] = Query(None, description="Cursor for pagination"),
    limit: Optional[int] = Query(100, description="Maximum number of messages to return"),
    ascending: bool = Query(True, description="Sort order by creation time"),
    role: Optional[MessageRole] = Query(None, description="Filter by role"),
):
    """
    Get messages associated with a run with filtering options.

    Args:
        run_id: ID of the run
        cursor: Cursor for pagination
        limit: Maximum number of messages to return
        ascending: Sort order by creation time
        role: Filter by role (user/assistant/system/tool)
        return_message_object: Whether to return Message objects or LettaMessage objects
        user_id: ID of the user making the request

    Returns:
        A list of messages associated with the run. Default is List[LettaMessage].
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    try:
        messages = server.job_manager.get_run_messages_cursor(
            run_id=run_id,
            actor=actor,
            limit=limit,
            cursor=cursor,
            ascending=ascending,
            role=role,
        )
        return messages
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{run_id}/usage", response_model=UsageStatistics, operation_id="get_run_usage")
def get_run_usage(
    run_id: str,
    user_id: Optional[str] = Header(None, alias="user_id"),
    server: "SyncServer" = Depends(get_letta_server),
):
    """
    Get usage statistics for a run.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    try:
        usage = server.job_manager.get_job_usage(job_id=run_id, actor=actor)
        return usage
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")


@router.delete("/{run_id}", response_model=Run, operation_id="delete_run")
def delete_run(
    run_id: str,
    user_id: Optional[str] = Header(None, alias="user_id"),
    server: "SyncServer" = Depends(get_letta_server),
):
    """
    Delete a run by its run_id.
    """
    actor = server.user_manager.get_user_or_default(user_id=user_id)

    try:
        job = server.job_manager.delete_job_by_id(job_id=run_id, actor=actor)
        return Run.from_job(job)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Run not found")
