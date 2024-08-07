from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ....api.v1.schemas.chat_schemas import ChatMessage, CreateChatMessage
from ....api.v1.services.chat_service import ChatService
from ....api.dependencies import get_current_user

router = APIRouter()


@router.get("/messages", response_model=List[ChatMessage])
def get_chat_messages(skip: int = 0, limit: int = 10, service: ChatService = Depends(ChatService)):
    """
    Retrieve a list of chat messages.
    """
    return service.get_messages(skip=skip, limit=limit)


@router.post("/messages", response_model=ChatMessage, status_code=201)
def create_chat_message(
        message: CreateChatMessage,
        service: ChatService = Depends(ChatService),
        user=Depends(get_current_user)
):
    """
    Create a new chat message.
    """
    return service.create_message(message, user)


@router.delete("/messages/{message_id}", status_code=204)
def delete_chat_message(
        message_id: int,
        service: ChatService = Depends(ChatService),
        user=Depends(get_current_user)
):
    """
    Delete a chat message.
    """
    service.delete_message(message_id, user)
