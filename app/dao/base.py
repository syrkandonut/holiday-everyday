from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import ColumnExpressionArgument, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base

ModelType = TypeVar("ModelType", bound=Base)


class MixinStub(Generic[ModelType]):
    model: type[ModelType]
    session: AsyncSession


class BaseDao(MixinStub[ModelType], Generic[ModelType]):
    @classmethod
    async def get_by_id(
        cls,
        id: int,
        session: AsyncSession,
    ) -> ModelType | None:
        stmt = select(cls.model).filter(
            cls.model.id == id,
        )
        result = await session.execute(stmt)

        return result.scalars().first()

    @classmethod
    async def get_where(
        cls,
        session: AsyncSession,
        filters: tuple[ColumnExpressionArgument[bool], ...] | None = None,
    ) -> ModelType | None:
        stmt = select(cls.model)
        if filters:
            stmt = stmt.filter(*filters)

        result = await session.execute(stmt)

        return result.scalars().first()

    @classmethod
    async def insert(
        cls,
        create_schema: BaseModel,
    ) -> ModelType:
        stmt = (
            insert(cls.model).values(**create_schema.model_dump()).returning(cls.model)
        )

        result = await cls.session.execute(stmt)
        await cls.session.commit()

        return result.scalars().one()

    @classmethod
    async def update_by_id(
        cls,
        update_schema: BaseModel,
    ) -> ModelType:
        stmt = (
            update(cls.model).values(**update_schema.model_dump()).returning(cls.model)
        )

        result = await cls.session.execute(stmt)
        await cls.session.commit()

        return result.scalars().one()

    @classmethod
    async def delete_by_id(cls, id: int) -> None:
        stmt = delete(cls.model).where(cls.model.id == id)

        await cls.session.execute(stmt)
        await cls.session.commit()
