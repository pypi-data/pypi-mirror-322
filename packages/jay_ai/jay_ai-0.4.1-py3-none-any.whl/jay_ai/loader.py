import os
import importlib.util
import sys
import inspect
from jay_ai.config import (
    Agent,
    _default_on_agent_started_speaking,
    _default_on_user_started_speaking,
    _default_on_user_stopped_speaking,
    _default_on_agent_started_speaking,
    _default_on_agent_stopped_speaking,
    _default_on_user_speech_committed,
    _default_on_agent_speech_committed,
    _default_on_agent_speech_interrupted,
    _default_on_function_calls_collected,
    _default_on_function_calls_finished,
)


def load_agent(agent_path: str) -> Agent:
    agent_dir = os.path.dirname(agent_path)
    if agent_dir not in sys.path:
        sys.path.insert(0, agent_dir)

    try:
        functions_module = load_functions_module(agent_path)
    except Exception as e:
        print(f"Error loading functions module: {e}")
        sys.exit(1)

    # Build the list of tools from any functions that have _is_llm_function = True
    tools = []
    for name, member in inspect.getmembers(functions_module):
        if (
            inspect.isfunction(member)
            and getattr(member, "_is_llm_function", False) is True
        ):
            tools.append(member)

    # Required fields
    config = getattr(functions_module, "config", None)
    if not config:
        raise ValueError("Missing required top-level 'config = AgentConfig(id=...)'.")

    start_session = getattr(functions_module, "start_session", None)
    if not start_session:
        raise ValueError("Missing required top-level 'start_session' function.")

    agent_response_handler = getattr(functions_module, "agent_response_handler", None)
    if not agent_response_handler:
        raise ValueError(
            "Missing required top-level 'agent_response_handler' function."
        )

    # Optional fields, with defaults if missing
    on_user_started_speaking = getattr(
        functions_module, "on_user_started_speaking", _default_on_user_started_speaking
    )
    on_user_stopped_speaking = getattr(
        functions_module, "on_user_stopped_speaking", _default_on_user_stopped_speaking
    )
    on_agent_started_speaking = getattr(
        functions_module,
        "on_agent_started_speaking",
        _default_on_agent_started_speaking,
    )
    on_agent_stopped_speaking = getattr(
        functions_module,
        "on_agent_stopped_speaking",
        _default_on_agent_stopped_speaking,
    )
    on_user_speech_committed = getattr(
        functions_module, "on_user_speech_committed", _default_on_user_speech_committed
    )
    on_agent_speech_committed = getattr(
        functions_module,
        "on_agent_speech_committed",
        _default_on_agent_speech_committed,
    )
    on_agent_speech_interrupted = getattr(
        functions_module,
        "on_agent_speech_interrupted",
        _default_on_agent_speech_interrupted,
    )
    on_function_calls_collected = getattr(
        functions_module,
        "on_function_calls_collected",
        _default_on_function_calls_collected,
    )
    on_function_calls_finished = getattr(
        functions_module,
        "on_function_calls_finished",
        _default_on_function_calls_finished,
    )

    # Construct and return the Agent
    return Agent(
        id=config.id,
        start_session=start_session,
        agent_response_handler=agent_response_handler,
        tools=tools,
        on_user_started_speaking=on_user_started_speaking,
        on_user_stopped_speaking=on_user_stopped_speaking,
        on_agent_started_speaking=on_agent_started_speaking,
        on_agent_stopped_speaking=on_agent_stopped_speaking,
        on_user_speech_committed=on_user_speech_committed,
        on_agent_speech_committed=on_agent_speech_committed,
        on_agent_speech_interrupted=on_agent_speech_interrupted,
        on_function_calls_collected=on_function_calls_collected,
        on_function_calls_finished=on_function_calls_finished,
    )


def load_functions_module(module_path):
    spec = importlib.util.spec_from_file_location("", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
