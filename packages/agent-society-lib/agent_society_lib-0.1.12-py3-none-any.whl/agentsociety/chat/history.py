"""
Contains the chat history
"""
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
from copy import copy, deepcopy
import json
from langchain.schema import SystemMessage, AIMessage, HumanMessage, BaseMessage
from agentsociety.chat.utils import HistoryArtifactCompatible

from agentsociety.log import logger

class Actor(Enum):
    SYSTEM = "system"
    USER = "user"
    AGENT = "ai"

    def to_exportable_name(self) -> str:
        match self.name:
            case 'SYSTEM':
                return 'SYSTEM'
            case 'AGENT':
                return 'AGENT'
            case 'USER':
                return 'USER'
            case _:
                raise RuntimeError(f'weird user name {self.name}')

    @classmethod
    def from_exportable_name(cls, name: str):
        match name:
            case 'SYSTEM':
                return cls.SYSTEM
            case 'AGENT':
                return cls.AGENT
            case 'USER':
                return cls.USER


class ContentType(Enum):
    UNDEFINED = 0
    TASK = 1
    REFINE_TASK = 2
    PLAN = 3
    TRANSLATE = 4
    FORMALIZE = 5
    EXPANSION = 6
    PARAMETERIZE = 7
    SOLVE = 8
    ABORT = 9
    START = 10
    RE_FORMALIZE = 11
    RE_EXPANSION = 12
    RE_PARAMETERIZE = 13
    EXPANSION_OPTIONS = 14
    PARAMETERIZE_OPTIONS = 15
    FORMALIZE_OPTIONS = 16
    SOLVE_OPTIONS = 17
    FATAL_ERROR = 18

    @classmethod
    def from_int(cls, value: Optional[int]) -> 'ContentType':
        if value is None:
            return ContentType.UNDEFINED
        return ContentType(value)


class HistoryContent:

    def __init__(self, content: str, sender: Actor, content_type: ContentType, user_input_required: bool = False, annotations: Dict[str, str] = None, artifacts: List['HistoryArtifact'] = None) -> None:
        self.content: str = content
        self.sender: Actor = sender
        self.content_type = content_type
        self.annotations: Dict[str, str] = {} if annotations is None else annotations
        self.artifacts: List[HistoryArtifact] = [] if artifacts is None else artifacts
        self.user_input_required: bool = user_input_required

    def render(self) -> str:
        return f"<{self.sender.name}>: {self.content}\n"
    
    def render_tuple(self) -> Tuple[str, str]:
        return (self.sender.value, self.content)
    
    def render_langchain(self, simple: bool) -> BaseMessage:
        match self.sender:
            case Actor.SYSTEM:
                if not simple:
                    return SystemMessage(self.content)
                else:
                    return HumanMessage(self.content)
            case Actor.USER:
                return HumanMessage(self.content)
            case Actor.AGENT:
                return AIMessage(self.content)
            case _:
                raise RuntimeError(f"Unknown role for message: '{self.sender}'")

    def clone(self) -> 'HistoryContent':
        return HistoryContent(copy(self.content), copy(self.sender), copy(self.content_type), self.user_input_required, deepcopy(self.annotations))
    
    def to_json(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "sender": self.sender.to_exportable_name(),
            "content_type": self.content_type.value,
            "user_input_required": self.user_input_required,
            "annotations": self.annotations,
            "artifacts": {a.ref: a.content for a in self.artifacts}
        }
    
    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> 'HistoryContent':
        content = HistoryContent(content=payload['content'], sender=Actor.from_exportable_name(payload['sender']), content_type=ContentType.from_int(payload['content_type']), annotations=payload["annotations"])
        content.user_input_required = payload.get('user_input_required', False)
        if "artifacts" in payload:
            logger.info(payload["artifacts"])
            artifact_list = [HistoryArtifact(k, v) for k, v in payload["artifacts"].items()]
            content.artifacts = artifact_list

        return content
    
    def add_artifact(self, artifact: 'HistoryArtifact'):
        self.artifacts.append(artifact)

_FALSE = 'false'
_TRUE = 'true'

class HistoryArtifact:

    def __init__(self, ref: str, content: str) -> None:
        self.ref: str = ref
        self.content: str = content

    def clone(self) -> 'HistoryArtifact':
        return HistoryArtifact(self.ref, self.content)
    
    @classmethod
    def from_object(cls, ref: str, obj: HistoryArtifactCompatible) -> 'HistoryArtifact':
        dict_form = obj.to_json()
        text_form = json.dumps(dict_form)
        return cls(
            ref, text_form
        )

    @classmethod
    def from_bool_flag(cls, name: Enum, bool_val: bool) -> 'HistoryArtifact':
        str_name = name.value
        str_val = _TRUE if bool_val else _FALSE

        return cls(str_name, str_val)


class HistoryDelta:

    def __init__(self, content: List[HistoryContent]) -> None:
        self.content: List[HistoryContent] = content
    
    def to_json(self) -> Dict[str, Any]:
        return {
            "content": [c.to_json() for c in self.content]
        }


class History:

    def __init__(self, content: Optional[List[HistoryContent]] = None) -> None:
        self.content: List[HistoryContent] = [] if content is None else content
        self.artifacts: Dict[str, HistoryArtifact] = {}
        # stores all changes to artifacts
        self.delta_content: List[HistoryContent] = []

        self._setup_artifact_cache()

    def _setup_artifact_cache(self):
        for c in self.content:
            self._update_artifact_cache_from_content(c)

    def _update_artifact_cache_from_content(self, content: HistoryContent):
        artifacts = content.artifacts

        for a in artifacts:
            self.artifacts[a.ref] = a

    def render(self) -> str:
        return "\n".join([m.render() for m in self.content])
    
    def render_tuples(self) -> List[Tuple[str, str]]:
        return [m.render_tuple() for m in self.content]

    def render_langchain(self, simple: bool) -> List[BaseMessage]:
        return [m.render_langchain(simple) for m in self.content]

    def clone(self) -> 'History':
        return History([m.clone() for m in self.content])

    def get_delta(self) -> HistoryDelta:
        return HistoryDelta(
            self.delta_content
        )

    def add_delta(self, delta: HistoryDelta):
        for c in delta.content:
            self.add_content(c)

    def add_content(self, content: HistoryContent):
        self.content.append(content)
        self.delta_content.append(content)

        self._update_artifact_cache_from_content(content)

    def get_artifact(self, artifact_ref: str) -> Optional[HistoryArtifact]:
        return self.artifacts.get(artifact_ref)

    def get_artifact_bool_flag(self, artifact_ref: Enum) -> bool:
        return self.get_artifact_content(artifact_ref.value, _FALSE) == _TRUE

    def get_artifact_content(self, artifact_ref: str, default: Optional[str] = None) -> Optional[str]:
        if (artifact := self.get_artifact(artifact_ref)) is not None:
            return artifact.content
        return default

    def get_latest_system_instruction_content_type(self) -> Optional[ContentType]:
        for c in reversed(self.content):
            if c.sender == Actor.SYSTEM:
                return c.content_type
        return None

    def get_system_instruction_type_stack(self) -> List[ContentType]:
        system_instructions = [c for c in self.content if c.sender == Actor.SYSTEM]
        return [m.content_type for m in system_instructions]

    def get_latest_agent_message(self) -> Optional[HistoryContent]:
        for c in reversed(self.content):
            if c.sender == Actor.AGENT:
                return c
        return None
    
    def get_latest_non_user_message(self) -> Optional[HistoryContent]:
        for c in reversed(self.content):
            if c.sender in [Actor.AGENT, Actor.SYSTEM]:
                return c
        return None

    def get_latest_message(self) -> Optional[HistoryContent]:
        if len(self.content) == 0:
            return None
        return self.content[-1]

    def is_last_message_choice(self) -> bool:
        content_type = self.get_latest_system_instruction_content_type()
        return content_type in [ContentType.FORMALIZE_OPTIONS, ContentType.EXPANSION_OPTIONS, ContentType.PARAMETERIZE_OPTIONS]

    def to_json(self) -> Dict[str, Any]:
        return {
            "content": [c.to_json() for c in self.content]
        }

    @classmethod
    def from_json(cls, payload: List[Dict[str, Any]]) -> 'History':
        logger.info(payload)
        messages = [HistoryContent.from_json(p) for p in payload["content"]]

        return History(messages)
