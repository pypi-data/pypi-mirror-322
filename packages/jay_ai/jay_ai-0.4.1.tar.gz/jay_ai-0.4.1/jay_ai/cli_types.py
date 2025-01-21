from enum import Enum
from typing import Dict, List, Any, Literal, Tuple, Union
from typing_extensions import TypedDict
from pydantic import BaseModel
from typing import List
from jay_ai.plugins import azure, elevenlabs, openai, google, cartesia, deepgram
from openai.types.chat import ChatCompletionUserMessageParam


class ProviderEnvVarKey(BaseModel):
    env_var_key: str
    is_json: bool


class ProviderInfo(BaseModel):
    label: str
    display_label: str
    injection: str | None
    env_var_keys: list[ProviderEnvVarKey]


class TTSProvider(Enum):
    ELEVENLABS = ProviderInfo(
        display_label="ElevenLabs",
        label="elevenlabs",
        injection='TTS.ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])',
        env_var_keys=[
            ProviderEnvVarKey(env_var_key="ELEVENLABS_API_KEY", is_json=False)
        ],
    )
    GOOGLE = ProviderInfo(
        display_label="Google",
        label="google",
        injection='TTS.Google(credentials=json.loads(os.environ["GOOGLE_CREDENTIALS"]))',
        env_var_keys=[
            ProviderEnvVarKey(env_var_key="GOOGLE_CREDENTIALS", is_json=True)
        ],
    )
    OPENAI = ProviderInfo(
        display_label="OpenAI",
        label="openai",
        injection='TTS.OpenAI(api_key=os.environ["OPENAI_API_KEY"])',
        env_var_keys=[ProviderEnvVarKey(env_var_key="OPENAI_API_KEY", is_json=False)],
    )
    AZURE = ProviderInfo(
        display_label="Azure",
        label="azure",
        injection='TTS.Azure(api_key=os.environ["AZURE_API_KEY"], region=os.environ["AZURE_REGION"])',
        env_var_keys=[
            ProviderEnvVarKey(env_var_key="AZURE_API_KEY", is_json=False),
            ProviderEnvVarKey(env_var_key="AZURE_REGION", is_json=False),
        ],
    )
    CARTESIA = ProviderInfo(
        display_label="Cartesia",
        label="cartesia",
        injection='TTS.Cartesia(api_key=os.environ["CARTESIA_API_KEY"])',
        env_var_keys=[ProviderEnvVarKey(env_var_key="CARTESIA_API_KEY", is_json=False)],
    )
    DEEPGRAM = ProviderInfo(
        display_label="Deepgram",
        label="deepgram",
        injection='TTS.Deepgram(api_key=os.environ["DEEPGRAM_API_KEY"])',
        env_var_keys=[ProviderEnvVarKey(env_var_key="DEEPGRAM_API_KEY", is_json=False)],
    )


class STTProvider(Enum):
    DEEPGRAM = ProviderInfo(
        display_label="Deepgram",
        label="deepgram",
        injection='STT.Deepgram(api_key=os.environ["DEEPGRAM_API_KEY"])',
        env_var_keys=[ProviderEnvVarKey(env_var_key="DEEPGRAM_API_KEY", is_json=False)],
    )
    OPENAI = ProviderInfo(
        display_label="OpenAI",
        label="openai",
        injection='STT.OpenAI(api_key=os.environ["OPENAI_API_KEY"])',
        env_var_keys=[ProviderEnvVarKey(env_var_key="OPENAI_API_KEY", is_json=False)],
    )
    AZURE = ProviderInfo(
        display_label="Azure",
        label="azure",
        injection='STT.Azure(api_key=os.environ["AZURE_API_KEY"], region=os.environ["AZURE_REGION"])',
        env_var_keys=[
            ProviderEnvVarKey(env_var_key="AZURE_API_KEY", is_json=False),
            ProviderEnvVarKey(env_var_key="AZURE_REGION", is_json=False),
        ],
    )


class VADProvider(Enum):
    SILERO = ProviderInfo(
        display_label="Silero", label="silero", injection=None, env_var_keys=[]
    )


class LLMProvider(Enum):
    OPENAI = ProviderInfo(
        display_label="OpenAI",
        label="openai",
        injection='AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])',
        env_var_keys=[ProviderEnvVarKey(env_var_key="OPENAI_API_KEY", is_json=False)],
    )
    OPENAI_COMPATIBLE = ProviderInfo(
        display_label="OpenAI Compatible",
        label="openai_compatible",
        injection='AsyncOpenAI(api_key=os.environ["OPENAI_COMPATIBLE_API_KEY"])',
        env_var_keys=[
            ProviderEnvVarKey(env_var_key="OPENAI_COMPATIBLE_API_KEY", is_json=False)
        ],
    )


class Message(TypedDict):
    content: str
    role: Literal["system", "user", "assistant", "tool"]
    name: str | None = None
    tool_call_id: str | None = None


class TTS:
    class ElevenLabs(BaseModel):
        api_key: str
        voice: elevenlabs.Voice = elevenlabs.DEFAULT_VOICE
        model: elevenlabs.TTSModels | str = "eleven_turbo_v2_5"
        encoding: elevenlabs.TTSEncoding = "mp3_22050_32"
        streaming_latency: int = 3
        enable_ssml_parsing: bool = False
        chunk_length_schedule: list[int] = [80, 120, 200, 260]  # range is [50, 500]

    class OpenAI(BaseModel):
        api_key: str
        model: openai.TTSModels | str = "tts-1"
        voice: openai.TTSVoices | str = "alloy"
        speed: float = 1.0

    class Google(BaseModel):
        credentials: dict
        language: google.SpeechLanguages | str = "en-US"
        gender: google.Gender | str = "neutral"
        voice_name: str = ""  # Not required
        encoding: google.AudioEncoding | str = "linear16"
        sample_rate: int = 24000
        pitch: int = 0
        effects_profile_id: str = ""
        speaking_rate: float = 1.0

    class Azure(BaseModel):
        api_key: str
        region: str
        sample_rate: int = 24000
        voice: str | None = None
        language: str | None = None
        prosody: azure.ProsodyConfig | None = None
        endpoint_id: str | None = None

    class Deepgram(BaseModel):
        api_key: str
        model: str = "aura-asteria-en"
        encoding: str = "linear16"
        sample_rate: int = 24000

    class Cartesia(BaseModel):
        api_key: str
        model: cartesia.TTSModels | str = "sonic-english"
        language: cartesia.TTSLanguages | str = "en"
        encoding: cartesia.TTSEncoding = "pcm_s16le"
        voice: str | list[float] = cartesia.TTSDefaultVoiceId
        speed: cartesia.TTSVoiceSpeed | float | None = None
        emotion: list[cartesia.TTSVoiceEmotion | str] | None = None
        sample_rate: int = 24000


class STT:
    class Deepgram(BaseModel):
        api_key: str
        model: deepgram.DeepgramModels = "nova-2-general"
        language: deepgram.DeepgramLanguages = "en-US"
        interim_results: bool = True
        punctuate: bool = True
        smart_format: bool = True
        sample_rate: int = 16000
        no_delay: bool = True
        endpointing_ms: int = 25
        # enable filler words by default to improve turn detector accuracy
        filler_words: bool = True
        keywords: list[Tuple[str, float]] = []
        profanity_filter: bool = False

    class Azure(BaseModel):
        api_key: str
        region: str
        sample_rate: int = 16000
        num_channels: int = 1
        # Azure handles multiple languages and can auto-detect the language used. It requires the candidate set to be set.
        languages: list[str] = ["en-US"]

    class OpenAI(BaseModel):
        api_key: str
        language: str = "en"
        detect_language: bool = False
        model: openai.WhisperModels | str = "whisper-1"


class VAD:
    class Silero(BaseModel):
        min_speech_duration: float = 0.05
        min_silence_duration: float = 0.55
        prefix_padding_duration: float = 0.5
        max_buffered_speech: float = 60.0
        activation_threshold: float = 0.5
        sample_rate: Literal[8000, 16000] = 16000


class AgentConfig(BaseModel):
    id: str


class SessionConfig(BaseModel):
    messages: List[Message]
    vad: VAD.Silero
    stt: Union[STT.OpenAI, STT.Azure, STT.Deepgram]
    tts: Union[
        TTS.OpenAI,
        TTS.ElevenLabs,
        TTS.Google,
        TTS.Azure,
        TTS.Deepgram,
        TTS.Cartesia,
    ]
    custom_data: dict[str, Any] = {}
    first_message: str | None = None
    allow_interruptions: bool = True
    interrupt_speech_duration: float = 0.5
    interrupt_min_words: int = 0
    min_endpointing_delay: float = 0.5
    max_nested_fnc_calls: int = 1


class Function(TypedDict):
    arguments: str
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: str
    """The name of the function to call."""


class FunctionCallInput(TypedDict):
    id: str
    """The ID of the tool call."""

    function: Function
    """The function that the model called."""

    type: Literal["function"]
    """The type of the tool. Currently, only `function` is supported."""


class FunctionCallResult(TypedDict):
    content: str
    """The contents of the tool message."""

    role: Literal["tool"]
    """The role of the messages author, in this case `tool`."""

    function: Function
    """The function that the model called."""

    tool_call_id: str
    """Tool call that this message is responding to."""


class StartSessionInput(TypedDict):
    custom_data: dict


class AgentResponseHandlerInput(TypedDict):
    messages: List[Message]
    custom_data: dict[str, Any]


class OnUserStartedSpeakingInput(TypedDict):
    custom_data: dict[str, Any]


class OnUserStoppedSpeakingInput(TypedDict):
    custom_data: dict[str, Any]


class OnAgentStartedSpeakingInput(TypedDict):
    custom_data: dict[str, Any]


class OnAgentStoppedSpeakingInput(TypedDict):
    custom_data: dict[str, Any]


class OnUserSpeechCommittedInput(TypedDict):
    message: Message
    custom_data: dict[str, Any]


class OnAgentSpeechCommittedInput(TypedDict):
    message: Message
    custom_data: dict[str, Any]


class OnAgentSpeechInterruptedInput(TypedDict):
    message: Message
    custom_data: dict[str, Any]


class OnFunctionCallsCollectedInput(TypedDict):
    function_calls: List[FunctionCallInput]
    custom_data: dict[str, Any]


class OnFunctionCallsFinishedInput(TypedDict):
    results: List[FunctionCallResult]
    custom_data: dict[str, Any]


class AgentResponseHandlerPayload(BaseModel):
    custom_data: dict[str, Any]
    messages: List[Dict[str, Any]]


class StartSessionPayload(BaseModel):
    custom_data: dict[str, Any]
    agent_api_url: str


class OnUserStartedSpeakingPayload(BaseModel):
    custom_data: dict[str, Any]


class OnUserStoppedSpeakingPayload(BaseModel):
    custom_data: dict[str, Any]


class OnAgentStartedSpeakingPayload(BaseModel):
    custom_data: dict[str, Any]


class OnAgentStoppedSpeakingPayload(BaseModel):
    custom_data: dict[str, Any]


class OnUserSpeechCommittedPayload(BaseModel):
    custom_data: dict[str, Any]
    message: Message


class OnAgentSpeechCommittedPayload(BaseModel):
    custom_data: dict[str, Any]
    message: Message


class OnAgentSpeechInterruptedPayload(BaseModel):
    custom_data: dict[str, Any]
    message: Message


class OnFunctionCallsCollectedPayload(BaseModel):
    custom_data: dict[str, Any]
    function_calls: List[FunctionCallInput]


class OnFunctionCallsFinishedPayload(BaseModel):
    custom_data: dict[str, Any]
    results: List[FunctionCallResult]


class ToolCallPayload(BaseModel):
    function_arguments: dict[str, Any]
