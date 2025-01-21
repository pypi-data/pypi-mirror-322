from dataclasses import dataclass
from typing import Any

from agi_med_common.models import ChatItem
from agi_med_protos.dto import RequestWithHeaders
from google.protobuf.json_format import ParseDict

from . import TextHeaders
from .. import DigitalAssistantTextRequest


@dataclass
class TextRequest(RequestWithHeaders[TextHeaders]):
    text: str
    chat: ChatItem

    def to_grpc_request(self) -> DigitalAssistantTextRequest:
        grpc_request = DigitalAssistantTextRequest()
        req_dict: dict[str, Any] = {"Text": self.text, "Chat": self.chat.model_dump(by_alias=True)}
        ParseDict(req_dict, grpc_request, ignore_unknown_fields=True)
        return grpc_request

    @classmethod
    def build(cls, text: str, chat: ChatItem, uuid: str) -> "TextRequest":
        headers: TextHeaders = {
            "extra_uuid": uuid,
            "outer_context": chat.outer_context.create_id(short=True)
        }
        return cls(
            text=text,
            chat=chat,
            headers=headers
        )
