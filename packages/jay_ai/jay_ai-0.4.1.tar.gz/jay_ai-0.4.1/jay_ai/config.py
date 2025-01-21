import os
import logging
import json
import requests
import inspect
import sentry_sdk
from pydantic import BaseModel
from logging import Logger
from typing import Awaitable, Callable, List, Any, Union
from dataclasses import field
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from inspect import iscoroutinefunction
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from jay_ai.token import generate_token
from jay_ai.cli_types import (
    OnAgentStartedSpeakingInput,
    OnAgentStoppedSpeakingInput,
    OnUserStartedSpeakingInput,
    OnUserStoppedSpeakingInput,
    OnAgentSpeechCommittedInput,
    OnAgentSpeechInterruptedInput,
    OnFunctionCallsCollectedInput,
    OnFunctionCallsFinishedInput,
    OnUserSpeechCommittedInput,
    AgentResponseHandlerPayload,
    OnAgentSpeechCommittedPayload,
    OnAgentSpeechInterruptedPayload,
    OnAgentStartedSpeakingPayload,
    OnAgentStoppedSpeakingPayload,
    OnFunctionCallsCollectedPayload,
    OnFunctionCallsFinishedPayload,
    OnUserSpeechCommittedPayload,
    OnUserStartedSpeakingPayload,
    OnUserStoppedSpeakingPayload,
    OnAgentStartedSpeakingPayload,
    StartSessionPayload,
    OnAgentSpeechCommittedInput,
    OnAgentSpeechInterruptedInput,
    OnFunctionCallsCollectedInput,
    OnFunctionCallsFinishedInput,
    OnUserSpeechCommittedInput,
    AgentResponseHandlerInput,
)
from jay_ai.cli_types import (
    SessionConfig,
    StartSessionInput,
)
from jay_ai.utils import fetch_site_url, fetch_headers

logger = logging.getLogger(__name__)


async def _default_on_user_started_speaking(input: OnUserStartedSpeakingInput) -> None:
    pass


async def _default_on_user_stopped_speaking(input: OnUserStoppedSpeakingInput) -> None:
    pass


async def _default_on_agent_started_speaking(
    input: OnAgentStartedSpeakingInput,
) -> None:
    pass


async def _default_on_agent_stopped_speaking(
    input: OnAgentStoppedSpeakingInput,
) -> None:
    pass


async def _default_on_user_speech_committed(input: OnUserSpeechCommittedInput) -> None:
    pass


async def _default_on_agent_speech_committed(
    input: OnAgentSpeechCommittedInput,
) -> None:
    pass


async def _default_on_agent_speech_interrupted(
    input: OnAgentSpeechInterruptedInput,
) -> None:
    pass


async def _default_on_function_calls_collected(
    input: OnFunctionCallsCollectedInput,
) -> None:
    pass


async def _default_on_function_calls_finished(
    input: OnFunctionCallsFinishedInput,
) -> None:
    pass


class Agent(BaseModel):
    id: str
    start_session: Callable[
        [StartSessionInput], Union[SessionConfig, Awaitable[SessionConfig]]
    ]
    agent_response_handler: Callable[
        [AgentResponseHandlerInput], Union[Any, Awaitable[Any]]
    ]
    tools: List[Callable[..., Union[Any, Awaitable[Any]]]] = field(default_factory=list)
    on_user_started_speaking: Callable[
        [OnUserStartedSpeakingInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_user_started_speaking)
    on_user_stopped_speaking: Callable[
        [OnUserStoppedSpeakingInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_user_stopped_speaking)
    on_agent_started_speaking: Callable[
        [OnAgentStartedSpeakingInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_agent_started_speaking)
    on_agent_stopped_speaking: Callable[
        [OnAgentStoppedSpeakingInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_agent_stopped_speaking)
    on_user_speech_committed: Callable[
        [OnUserSpeechCommittedInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_user_speech_committed)
    on_agent_speech_committed: Callable[
        [OnAgentSpeechCommittedInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_agent_speech_committed)
    on_agent_speech_interrupted: Callable[
        [OnAgentSpeechInterruptedInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_agent_speech_interrupted)
    on_function_calls_collected: Callable[
        [OnFunctionCallsCollectedInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_function_calls_collected)
    on_function_calls_finished: Callable[
        [OnFunctionCallsFinishedInput], Union[None, Awaitable[None]]
    ] = field(default=_default_on_function_calls_finished)

    def __post_init__(self) -> None:
        # Throw an error if any of the functions in `tools` is a lambda function. Named functions
        # are required because we use the function names to create API endpoints.
        for tool in self.tools:
            if inspect.isfunction(tool) and tool.__name__ == "<lambda>":
                raise ValueError(
                    "Lambda functions are not allowed in `tools`. Please define a named function instead."
                )

        # Find any duplicate function names
        tool_names = [tool.__name__ for tool in self.tools]
        duplicates = {name for name in tool_names if tool_names.count(name) > 1}
        if duplicates:
            raise ValueError(f"Duplicate tool names found: {', '.join(duplicates)}")

    def create_api(
        self, report_status: bool, skip_security_check: bool, deployment_id: str
    ):
        app = FastAPI()
        api_router = self.create_api_router()

        @app.middleware("http")
        async def middleware(request: Request, call_next):
            excluded_paths = ["/", "/health"]
            if request.url.path not in excluded_paths and skip_security_check == False:
                # Validate Agent API Key
                x_api_key = request.headers.get("X-API-Key")
                if x_api_key != os.getenv("JAY_INTERNAL__AGENT_API_KEY"):
                    raise HTTPException(status_code=401, detail="Invalid API key")
                # Report status
                if report_status:
                    report_service_status(deployment_id)
            response = await call_next(request)
            return response

        # Include our router
        app.include_router(api_router)

        # We only need this because we're calling /startSession directly from the react app, but in production we should be calling
        # into the platform api which then forwards the request to the agent.
        # When we have that setup, we can remove this
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        return app

    def create_production_api(self):
        deployment_id = os.getenv("JAY_INTERNAL__DEPLOYMENT_ID")
        sentry_dsn = os.getenv("SENTRY_DSN")
        sentry_env = os.getenv("SENTRY_ENVIRONMENT")
        if sentry_dsn and sentry_env:
            logger.info("Sentry integration initialized!")
            sentry_sdk.init(
                dsn=sentry_dsn,
                environment=sentry_env,
                # Sample rate for transactions (performance).
                traces_sample_rate=1.0,
                # Sample rate for exceptions / crashes.
                sample_rate=1.0,
                max_request_body_size="always",
                integrations=[
                    AsyncioIntegration(),
                    LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
                ],
            )
        else:
            logger.warning(
                "Sentry integration disabled due to missing Sentry configuration. Error logging with Sentry is highly recommended: https://docs.jay.so/error-monitoring"
            )

        return self.create_api(
            report_status=True, skip_security_check=False, deployment_id=deployment_id
        )

    def create_api_router(self):
        router = APIRouter()
        agent = self

        @router.get("/")
        def root():
            return {"message": "Service running"}

        @router.head("/")
        def root_head():
            return {"message": "Service running"}

        @router.get("/health")
        def health():
            return {"status": "healthy"}

        @router.post("/startSession")
        async def start_session_handler(payload: StartSessionPayload):
            try:
                input_data = StartSessionInput({"custom_data": payload.custom_data})
                if iscoroutinefunction(agent.start_session):
                    session_config = await agent.start_session(input_data)
                else:
                    session_config = agent.start_session(input_data)
                token = await generate_token(
                    session_config=session_config, agent_api_url=payload.agent_api_url
                )
                return {"token": token}
            except Exception as e:
                logger.exception("Error in /startSession endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )

        @router.post("/agentResponse")
        async def agent_response_handler_endpoint(payload: AgentResponseHandlerPayload):
            try:
                input_data = AgentResponseHandlerInput(
                    {"custom_data": payload.custom_data, "messages": payload.messages}
                )

                if iscoroutinefunction(agent.agent_response_handler):
                    response_stream = await agent.agent_response_handler(input_data)

                    async def response_generator():
                        async for chunk in response_stream:
                            yield json.dumps(jsonable_encoder(chunk)).encode(
                                "utf-8"
                            ) + b"\n"

                else:
                    response_stream = agent.agent_response_handler(input_data)

                    async def response_generator():
                        for chunk in response_stream:
                            yield json.dumps(jsonable_encoder(chunk)).encode(
                                "utf-8"
                            ) + b"\n"

                return StreamingResponse(
                    response_generator(), media_type="application/json"
                )
            except Exception as e:
                logger.exception("Error in /agentResponse endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )

        @router.post("/userStartedSpeaking")
        async def user_started_speaking_endpoint(payload: OnUserStartedSpeakingPayload):
            input_data = OnUserStartedSpeakingInput(
                {"custom_data": payload.custom_data}
            )
            try:
                if iscoroutinefunction(agent.on_user_started_speaking):
                    await agent.on_user_started_speaking(input_data)
                else:
                    agent.on_user_started_speaking(input_data)
            except Exception as e:
                logger.exception("Error in /userStartedSpeaking endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/userStoppedSpeaking")
        async def user_stopped_speaking_endpoint(payload: OnUserStoppedSpeakingPayload):
            input_data = OnUserStoppedSpeakingInput(
                {"custom_data": payload.custom_data}
            )
            try:
                if iscoroutinefunction(agent.on_user_stopped_speaking):
                    await agent.on_user_stopped_speaking(input_data)
                else:
                    agent.on_user_stopped_speaking(input_data)
            except Exception as e:
                logger.exception("Error in /userStoppedSpeaking endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/agentStartedSpeaking")
        async def agent_started_speaking_endpoint(
            payload: OnAgentStartedSpeakingPayload,
        ):
            input_data = OnAgentStartedSpeakingInput(
                {"custom_data": payload.custom_data}
            )
            try:
                if iscoroutinefunction(agent.on_agent_started_speaking):
                    await agent.on_agent_started_speaking(input_data)
                else:
                    agent.on_agent_started_speaking(input_data)
            except Exception as e:
                logger.exception("Error in /agentStartedSpeaking endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/agentStoppedSpeaking")
        async def agent_stopped_speaking_endpoint(
            payload: OnAgentStoppedSpeakingPayload,
        ):
            input_data = OnAgentStoppedSpeakingInput(
                {"custom_data": payload.custom_data}
            )
            try:
                if iscoroutinefunction(agent.on_agent_stopped_speaking):
                    await agent.on_agent_stopped_speaking(input_data)
                else:
                    agent.on_agent_stopped_speaking(input_data)
            except Exception as e:
                logger.exception("Error in /agentStoppedSpeaking endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/userSpeechCommitted")
        async def user_speech_committed_endpoint(payload: OnUserSpeechCommittedPayload):
            try:
                input_data = OnUserSpeechCommittedInput(
                    {
                        "custom_data": payload.custom_data,
                        "message": payload.message,
                    }
                )

                if iscoroutinefunction(agent.on_user_speech_committed):
                    await agent.on_user_speech_committed(input_data)
                else:
                    agent.on_user_speech_committed(input_data)
            except Exception as e:
                logger.exception("Error in /userSpeechCommitted endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/agentSpeechCommitted")
        async def agent_speech_committed_endpoint(
            payload: OnAgentSpeechCommittedPayload,
        ):
            try:
                input_data = OnAgentSpeechCommittedInput(
                    {
                        "custom_data": payload.custom_data,
                        "message": payload.message,
                    }
                )

                if iscoroutinefunction(agent.on_agent_speech_committed):
                    await agent.on_agent_speech_committed(input_data)
                else:
                    agent.on_agent_speech_committed(input_data)
            except Exception as e:
                logger.exception("Error in /agentSpeechCommitted endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/agentSpeechInterrupted")
        async def agent_speech_interrupted_endpoint(
            payload: OnAgentSpeechInterruptedPayload,
        ):
            try:
                input_data = OnAgentSpeechInterruptedInput(
                    {
                        "custom_data": payload.custom_data,
                        "message": payload.message,
                    }
                )

                if iscoroutinefunction(agent.on_agent_speech_interrupted):
                    await agent.on_agent_speech_interrupted(input_data)
                else:
                    agent.on_agent_speech_interrupted(input_data)
            except Exception as e:
                logger.exception("Error in /agentSpeechInterrupted endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/functionCallsCollected")
        async def function_calls_collected_endpoint(
            payload: OnFunctionCallsCollectedPayload,
        ):
            try:
                input_data = OnFunctionCallsCollectedInput(
                    {
                        "custom_data": payload.custom_data,
                        "function_calls": payload.function_calls,
                    }
                )

                if iscoroutinefunction(agent.on_function_calls_collected):
                    await agent.on_function_calls_collected(input_data)
                else:
                    agent.on_function_calls_collected(input_data)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        @router.post("/functionCallsFinished")
        async def function_calls_finished_endpoint(
            payload: OnFunctionCallsFinishedPayload,
        ):
            try:
                input_data = OnFunctionCallsFinishedInput(
                    {"custom_data": payload.custom_data, "results": payload.results}
                )

                if iscoroutinefunction(agent.on_function_calls_finished):
                    await agent.on_function_calls_finished(input_data)
                else:
                    agent.on_function_calls_finished(input_data)
            except Exception as e:
                logger.exception("Error in /agentSpeechInterrupted endpoint")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
                )
            return {"status": "ok"}

        def create_tool_endpoint(tool_func):
            async def _endpoint(payload: dict):
                try:
                    if iscoroutinefunction(tool_func):
                        result = await tool_func(**payload)
                    else:
                        result = tool_func(**payload)
                    return {"result": result}
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User logic error: {str(e)}",
                    )

            return _endpoint

        for tool_func in self.tools:
            func_name = tool_func.__name__
            endpoint_path = f"/tool/{func_name}"
            router.add_api_route(
                endpoint_path,
                create_tool_endpoint(tool_func),
                methods=["POST"],
                name=func_name,
            )

        return router


def fetch_report_status_payload(deployment_id: str):
    headers = fetch_headers(os.getenv("JAY_INTERNAL__AGENT_API_KEY"))
    url = f"{fetch_site_url()}/api/serviceStatus/report"
    payload = {
        "deployment_id": deployment_id,
    }

    return url, payload, headers


# Calls an API endpoint to report status of the service.
# This is used to implement smooth upgrade logic by decommissioning the agent api only after it has not received
# any requests after some time.
def report_service_status(deployment_id: str):
    url, payload, headers = fetch_report_status_payload(deployment_id)

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response data: {response.json()}")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        logger.error(f"Response: {response.text}")
    except Exception as err:
        logger.exception(f"An unexpected error occurred: {err}")
