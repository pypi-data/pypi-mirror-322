__version__ = "4.1.0"

from .DigitalAssistantChatManager_pb2 import (
    DigitalAssistantChatManagerRequest,
    DigitalAssistantChatManagerResponse,
    OuterContextItem,
)
from .DigitalAssistantChatManager_pb2_grpc import (
    DigitalAssistantChatManagerStub,
    DigitalAssistantChatManager,
    DigitalAssistantChatManagerServicer,
)

from .dto import ChatHeaders, ChatRequest
from .client import ChatManagerClient
