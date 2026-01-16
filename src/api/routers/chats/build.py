import logging
from typing import Annotated
from fastapi import (
    APIRouter, Depends, HTTPException, Path, Query, Response,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.build import get_async_db
from src.schemas import (
    BodyChatsModel, BodyTextMessageModel, CountMessageModel,
    ChatMessageResponse
)
from src.service.core import add_chat, add_message, get_messages, delete_chat
from src.service import exc

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chats/")
async def _add_chat(
    payload: BodyChatsModel, 
    db: AsyncSession = Depends(get_async_db)
):
    print(f"DEBUG: dbc.get_async_db ID is {id(get_async_db)}")
    title = payload.title
    try:
        result = await add_chat(title, db)
    except exc.AddChatCoreError as e:
        raise HTTPException(status_code=500, detail="Failed to add chat")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.debug(str(result))
    return result

@router.post("/chats/{id}/messages/")
async def _add_message(
    payload: BodyTextMessageModel, 
    id: int = Path(..., description="ID чата"), # Получаем id из URL
    db: AsyncSession = Depends(get_async_db)    
):
    text = payload.text
    try:
        result = await add_message(id, text, db)
    except exc.ChatNotFound as e:
        raise HTTPException(status_code=404, detail="Chat not found")
    except exc.AddMessageCoreError as e:
        raise HTTPException(status_code=404, detail="Failed to add message")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.debug(str(result))
    return result

@router.get("/chats/{id}", response_model=ChatMessageResponse)
async def _get_messages(
    id: int = Path(..., description="ID чата"), # Получаем id из URL
    params: Annotated[CountMessageModel, Query()] = CountMessageModel(),
    db: AsyncSession = Depends(get_async_db)    
):
    count = params.count
    try:
        result = await get_messages(id, count, db)
    except exc.ChatNotFound as e:
        raise HTTPException(status_code=404, detail="Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    logger.debug(str(result))
    return result

@router.delete("/chats/{id}")
async def _delete_chat(
    id: int = Path(..., description="ID чата"), # Получаем id из URL
    db: AsyncSession = Depends(get_async_db)    
):
    try:
        await delete_chat(id, db)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except exc.ChatNotFound as e:
        raise HTTPException(status_code=404, detail="Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
