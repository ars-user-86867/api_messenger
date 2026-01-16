import datetime
from sqlalchemy import (
    String, text, inspect
)
from sqlalchemy.orm import (
    mapped_column
)
from typing import Annotated

created_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("timezone('utc', now())")
    )]

class ReprMixin:
    """Mixin для автоматического формирования __repr__ на основе колонок модели."""

    def __repr__(self) -> str:
        # Инспектор позволяет получить все атрибуты таблицы
        mapper = inspect(self.__class__)
        attrs = []
        for column in mapper.columns:
            name = column.key
            value = getattr(self, name)
            attrs.append(f"{name}={value!r}")
        return f"<{self.__class__.__name__}({', '.join(attrs)})>"

class SqlTypes:
    str_200 = Annotated[str, 200]
    str_5_000 = Annotated[str, 5_000]

    type_annotation_map = {
        str_200: String(200),
        str_5_000: String(5_000),
    }
