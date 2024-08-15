import json
from typing import Generator, Iterator, Optional

from fastapi import APIRouter, Body, Depends, Request, Response
from fastapi.responses import StreamingResponse

from kontext_copilot import ollama
from kontext_copilot.copilot import Planner
from kontext_copilot.data.schemas import (
    ChatRequestModel,
    LlmModelListResponse,
    RunSqlRequestModel,
    SessionInitRequestModel,
    SessionInitResponseModel,
)
from kontext_copilot.services import SettingsService, get_settings_service
from kontext_copilot.utils import get_logger

router = APIRouter(
    tags=["copilot"],
    prefix="/api/copilot",
    responses={
        404: {"description": "Not found"},
    },
)

logger = get_logger()


def _get_planner(
    model: str,
    data_source_id: Optional[int] = None,
    tables: Optional[list[str]] = None,
    schema: Optional[str] = None,
    session_id: Optional[int] = None,
):
    """
    Get planner
    """
    planner = Planner()
    planner.init_session(
        model,
        data_source_id,
        tables=tables,
        schema=schema,
        session_id=session_id,
    )
    return planner


@router.post("/init_session", response_model=SessionInitResponseModel)
def init_session(
    request: SessionInitRequestModel = Body(None),
) -> SessionInitResponseModel:
    """
    Init session with system prompt
    """
    logger.debug("Request: %s", request)
    planner = _get_planner(
        model=request.model,
        data_source_id=request.data_source_id,
        tables=request.tables,
        schema=request.schema_name,
        session_id=request.session_id,
    )

    prompt = planner.get_system_prompt()

    logger.debug("System prompt: %s", prompt)

    session = planner.get_session_model()
    return SessionInitResponseModel(
        system_prompt=prompt,
        session_id=session.id,
        title=session.title,
        schema_name=session.schema_name,
        tables=session.tables,
        model=session.model,
        data_source_id=session.data_source_id,
    )


@router.post("/run-sql")
def run_sql(request: RunSqlRequestModel = Body(None)):
    """
    Run SQL
    """
    planner = _get_planner(
        model="copilot",
        data_source_id=request.data_source_id,
        schema=request.schema_name,
        session_id=request.session_id,
    )
    return StreamingResponse(
        planner.run_sql(request=request), media_type="application/x-ndjson"
    )


@router.post("/chat")
async def chat(
    request: ChatRequestModel, settings: SettingsService = Depends(get_settings_service)
):
    """
    Run SQL
    """
    logger.info("Chat API invoked: %s", request)

    planner = _get_planner(
        model=request.model,
        session_id=request.session_id,
    )

    chat_response = planner.chat(
        settings.get_settings_obj().llm_ollama_endpoint, request=request
    )

    if isinstance(chat_response, Generator):
        return StreamingResponse(chat_response, media_type="application/x-ndjson")
    else:
        return Response(chat_response)


def _get_client(settings_service: SettingsService) -> ollama.Client:
    settings = settings_service.get_settings_obj()
    return ollama.Client(
        host=settings.llm_ollama_endpoint,
    )


@router.get("/tags")
def list_models(
    settings_service: SettingsService = Depends(get_settings_service),
) -> LlmModelListResponse:
    """
    Get a list of available models.
    """
    logger.info("Getting list of models")
    response = _get_client(settings_service=settings_service).list()
    return response


@router.post("/generate")
async def generate(
    request: Request, settings_service: SettingsService = Depends(get_settings_service)
):
    params = await request.json()
    logger.debug("Generate API invoked: %s", params)

    client = _get_client(settings_service=settings_service)
    response = client.generate(**params)

    # Always return as streaming
    if isinstance(response, Iterator):

        def generate_response():
            for res in iter(response):
                yield json.dumps(res) + "\n"

        return StreamingResponse(generate_response(), media_type="application/x-ndjson")

    if response is not None:
        return json.dumps(response)


@router.post("/embeddings")
async def generate_embeddings(
    request: Request, settings_service: SettingsService = Depends(get_settings_service)
):
    params = await request.json()
    logger.debug("Embeddings API invoked: %s", params)

    client = _get_client(settings_service=settings_service)
    response = client.embeddings(**params)
    return response
