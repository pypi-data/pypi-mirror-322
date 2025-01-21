__version__ = "3.1.0"

from .DigitalAssistantText_pb2 import DigitalAssistantTextRequest, DigitalAssistantTextResponse
from .DigitalAssistantText_pb2_grpc import DigitalAssistantTextStub, DigitalAssistantText, DigitalAssistantTextServicer
from .dto import TextRequest, TextHeaders
from .client import TextClient
