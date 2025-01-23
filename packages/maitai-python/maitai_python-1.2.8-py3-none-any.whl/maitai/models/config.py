# codegen: frontend, sdk
from enum import IntEnum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal


class InferenceLocations(IntEnum):
    CLIENT = 0
    SERVER = 1


class FallbackConfig(BaseModel):
    model: Optional[str] = None
    strategy: Optional[Union[Literal["reactive", "first_response", "timeout"], str]] = (
        "reactive"
    )
    timeout: Optional[float] = None


class Config(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    inference_location: InferenceLocations = InferenceLocations.SERVER
    evaluation_enabled: bool = True
    apply_corrections: bool = False
    model: str = "gpt-4o"
    temperature: float = 1
    streaming: bool = False
    response_format: str = "text"
    stop: Optional[Union[str, List[str]]] = None
    logprobs: bool = False
    max_tokens: Optional[int] = None
    n: int = 1
    presence_penalty: float = 0
    frequency_penalty: float = 0
    timeout: float = 0
    context_retrieval_enabled: bool = False
    fallback_model: Optional[str] = None
    intent_stability: Optional[str] = None
    safe_mode: bool = False
    feedback: List[str] = Field(default_factory=list)
    generating_sentinels: bool = False
    sentinel_regeneration_enabled: bool = False
    fallback_config: Optional[FallbackConfig] = None
    extract_request_metadata: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ModelConfig(BaseModel):
    all_models: List[str] = Field(default_factory=list)
    client_models: List[str] = Field(default_factory=list)
    server_models: List[str] = Field(default_factory=list)
    default_client_model: str
