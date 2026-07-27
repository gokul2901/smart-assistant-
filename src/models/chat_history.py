from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum



class MessageRole(str, Enum):
    """
    Who sent the message
    """

    user = "user"
    assistant = "assistant"
    system = "system"



class ConversationType(str, Enum):
    """
    Type of conversation
    """

    voice_call = "voice_call"
    chatbot = "chatbot"
    admin_chat = "admin_chat"



class ChatMessage(BaseModel):
    """
    Individual conversation message
    """

    role: MessageRole

    content: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow
    )



class ChatHistory(BaseModel):
    """
    Complete customer conversation history
    """

    chat_id: Optional[str] = None


    customer_id: Optional[str] = None


    customer_phone: Optional[str] = None


    session_id: Optional[str] = None


    conversation_type: ConversationType


    messages: List[ChatMessage] = []


    language: Optional[str] = "en"


    order_id: Optional[str] = None


    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )


    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )