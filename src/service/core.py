import logging
from sqlalchemy import desc, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import (
    BodyChatsModel, BodyTextMessageModel
)
from src.db.models import Chat, Message
from src.service import exc

logger = logging.getLogger(__name__)

def trim_text(text: str):
    return text.strip()

async def find_chat(
    chat_id: int,
    db: AsyncSession,
):
    logger.debug(f"find {chat_id = }")
    query = select(Chat).where(Chat.id == chat_id)
    result = await db.execute(query)
    chat = result.scalar_one_or_none()

    if not chat:
        logger.error(f"Chat not found: chat_id - {chat_id}")
        raise exc.ChatNotFound("Chat not found")
    return chat

async def add_chat(
    title: BodyChatsModel,
    db: AsyncSession,
):
    logger.debug(f"Chat name - {title}")
    chat = Chat(title=title)
    try:
        db.add(chat)
        await db.commit()
    except Exception as e:
        msg = (
            "Не удалось добавить чат!\n"
            f"Детали:\n{e}"
        )
        logger.error(msg)
        raise exc.AddChatCoreError(msg)
    return chat

async def add_message(
    chat_id: int,
    text: BodyTextMessageModel,
    db: AsyncSession,
):
    logger.debug(f"{text = }")
    _ = await find_chat(chat_id, db)
    cleared_text = trim_text(text)
    new_message = Message(
        chat_id=chat_id,
        text=cleared_text,
    )
    try:
        db.add(new_message)
        await db.commit()
    except Exception as e:
        msg = (
            "Не удалось добавить сообщение!\n"
            f"Детали:\n{e}"
        )
        logger.error(msg)
        raise exc.AddMessageCoreError(msg)
    return new_message

async def get_messages(
    chat_id: int,
    count: int,
    db: AsyncSession,
):
    logger.debug(f"{count = }")
    chat = await find_chat(chat_id, db)
    
    query_msgs = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(desc(Message.created_at)) 
        .limit(count)
    )
    result_msgs = await db.execute(query_msgs)
    messages = result_msgs.scalars().all()
    count_msg = len(messages)
    logger.debug(f"count messages from chat_id - {chat_id} = {count_msg}")
    if count_msg == 0:
        ...
    # разворот от старых к новым
    sorted_messages = sorted(messages, key=lambda x: x.created_at)
    # приклеить сообщения к чату
    chat.messages = sorted_messages 
    return chat
    
async def delete_chat(
    chat_id: int,
    db: AsyncSession,
):
    logger.debug(f"delete {chat_id = }")
    _ = await find_chat(chat_id, db)
    
    query = (
        delete(Chat)
        .where(Chat.id == chat_id)
    )
    await db.execute(query)
    await db.commit()
