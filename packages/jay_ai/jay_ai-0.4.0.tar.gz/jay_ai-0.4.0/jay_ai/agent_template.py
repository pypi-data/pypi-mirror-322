from jay_ai.cli_types import LLMProvider, STTProvider, TTSProvider


AGENT_CONFIG_TEMPLATE = """import os
from openai import AsyncOpenAI
from jay_ai.cli_types import (
    VAD,
    STT,
    TTS,
    StartSessionInput,
    SessionConfig,
    AgentResponseHandlerInput,
    AgentConfig,
)

async def start_session(input: StartSessionInput):
    return SessionConfig(
        messages=[],
        vad=VAD.Silero(),
        stt={stt_injection},
        tts={tts_injection},
    )


async def agent_response_handler(input: AgentResponseHandlerInput):
    client = {llm_injection}
    messages = input["messages"]
    completion = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
    )
    return completion


config = AgentConfig(id="{agent_id}")
"""


def get_agent_template(
    agent_id: str,
    stt_provider: STTProvider,
    llm_provider: LLMProvider,
    tts_provider: TTSProvider,
) -> str:
    env_var_keys = tts_provider.value.env_var_keys + stt_provider.value.env_var_keys
    import_json = any(env_var.is_json for env_var in env_var_keys)

    file = AGENT_CONFIG_TEMPLATE.format(
        agent_id=agent_id,
        stt_injection=stt_provider.value.injection,
        llm_injection=llm_provider.value.injection,
        tts_injection=tts_provider.value.injection,
    )

    if import_json:
        file = "import json\n" + file

    return file
