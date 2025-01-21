from dataclasses import dataclass
from typing import Optional, Dict, Any

from .utils import pick_typed, pick_number

@dataclass
class PromptModelParameters:
    temperature: float
    top_k: float
    top_p: Optional[float]

    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]

    max_length: int
    response_format: str
    json_object: Optional[dict]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            temperature=pick_number(data, "temperature"),
            frequency_penalty=pick_number(data, 'frequencyPenalty') if data.get("frequencyPenalty") else None,
            presence_penalty=pick_number(data, "presencePenalty") if data.get("presencePenalty") else None,
            top_p=pick_number(data, "topP"),
            top_k=pick_number(data, "topK") if data.get("topK") else None,
            max_length=data["maxLength"],
            response_format=pick_typed(data, "responseFormat", str),
            json_object=data.get("jsonObject"),
        )

@dataclass(frozen=True)
class PromptModel:
    provider: str
    model: str
    version: str
    parameters: PromptModelParameters

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            provider=pick_typed(data, "provider", str),
            model=pick_typed(data, "model", str),
            version=pick_typed(data, "version", str),
            parameters=PromptModelParameters.from_dict(data.get("parameters")),
        )

@dataclass(frozen=True)
class PromptResponse:
    text: str
    model: PromptModel

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            text=pick_typed(data, "text", str),
            model=PromptModel.from_dict(data.get("model")),
        )

@dataclass(frozen=True)
class GetPromptDTO:
    slug: str
    tag: Optional[str] = None
    version: Optional[str] = None
