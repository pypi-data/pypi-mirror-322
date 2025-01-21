"""
----------------------------------------------------------------------------------------------------
Written by Yovany Dominico Girón (y.dominico.giron@elprat.cat) for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from abc import abstractmethod
from typing import Union

from sqlalchemy import event
from sqlalchemy.orm import Session

from nomenclators_archetype.domain.commons import BaseSimpleNomenclator, BaseNomenclator
from nomenclators_archetype.infrastructure.db.commons import BaseSimpleNomenclator as BaseSimpleNomenclatorEntity
from nomenclators_archetype.infrastructure.db.commons import BaseNomenclator as BaseNomenclatorEntity

from nomenclators_archetype.domain.repository.commons import JpaRepository

from nomenclators_archetype.domain.repository.builders import QueryBuilder
from nomenclators_archetype.infrastructure.db.builders import QueryBuilderImpl

NomenclatorId = Union[int, str]


class BaseSimpleNomenclatorRepository(JpaRepository[BaseSimpleNomenclator, NomenclatorId, BaseSimpleNomenclatorEntity, Session, QueryBuilder]):
    """BaseSimpleNomenclator Repository Class"""

    def __init__(self, session: Session):
        self._session = session

    def get_builder(self) -> QueryBuilder:
        return QueryBuilderImpl()

    def get_session(self) -> Session:
        return self._session

    @abstractmethod
    def get_peristence_model(self) -> BaseSimpleNomenclatorEntity:
        """Get persistence class"""


class BaseNomenclatorRepository(JpaRepository[BaseNomenclator, NomenclatorId, BaseNomenclatorEntity, Session, QueryBuilder]):
    """BaseNomenclator Repository Class"""

    def __init__(self, session: Session):
        self._session = session

    def get_builder(self):
        return QueryBuilderImpl()

    def get_session(self):
        return self._session

    @abstractmethod
    def get_peristence_model(self) -> BaseNomenclatorEntity:
        """Get persistence class"""


@event.listens_for(Session, "before_flush")
def soft_delete_listener(session, flush_context, instances):  # pylint: disable=unused-argument
    """Soft delete listener"""

    for obj in session.deleted:
        if (isinstance(obj, BaseSimpleNomenclatorEntity) or isinstance(obj, BaseNomenclatorEntity)) and obj.active:
            obj.active = False
            session.add(obj)
