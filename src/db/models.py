from typing import Annotated
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.build import Base
from src.db.sql_obj import created_at, SqlTypes as ST

intpk = Annotated[int, mapped_column(primary_key=True)]

class Plug:
    ...
    
class Chat(Base):
    __tablename__ = 'chats'
    
    id: Mapped[intpk]
    title: Mapped[ST.str_200] = mapped_column()
    created_at: Mapped[created_at]

class Message(Base):
    __tablename__ = 'messages'
    
    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"))
    text: Mapped[ST.str_5_000]
    created_at: Mapped[created_at]
