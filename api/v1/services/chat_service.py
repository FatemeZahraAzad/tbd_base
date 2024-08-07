from typing import List
from app.api.v1.schemas.chat_schemas import ChatMessage, CreateChatMessage
from app.models.chat import ChatModel
from app.db.session import db_session

class ChatService:
    def get_messages(self, skip: int = 0, limit: int = 10) -> List[ChatMessage]:
        messages = ChatModel.query.offset(skip).limit(limit).all()
        return [ChatMessage.from_orm(message) for message in messages]

    def create_message(self, message: CreateChatMessage, user) -> ChatMessage:
        new_message = ChatModel(user_id=user.id, content=message.content)
        db_session.add(new_message)
        db_session.commit()
        return ChatMessage.from_orm(new_message)

    def delete_message(self, message_id: int, user) -> None:
        message = ChatModel.query.get(message_id)
        if message and message.user_id == user.id:
            db_session.delete(message)
            db_session.commit()