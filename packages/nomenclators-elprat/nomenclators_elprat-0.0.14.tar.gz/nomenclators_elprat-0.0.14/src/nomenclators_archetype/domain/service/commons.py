# type: ignore
"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from abc import abstractmethod
from typing import Optional, TypeVar, Protocol, List
from nomenclators_archetype.domain.repository.builders import Pageable

D = TypeVar('D', bound=object)  # Domain class representation
I = TypeVar('I', bound=object)  # Intentifier class representation
R = TypeVar('R', bound=object)  # Repository class representation
M = TypeVar('M', bound=object)  # Mapper class representation


class NomenclatorService(Protocol[D, R, M]):
    """NomenclatorService class"""

    @abstractmethod
    def get_mapper(self) -> M:
        """Get mapper for nomenclator service class"""
        raise NotImplementedError

    @abstractmethod
    def get_repository(self) -> R:
        """Get repository for nomenclator service class"""

    def get_item_by_id(self, _id: I) -> D:
        """Get item by id"""

        return self.get_mapper().map_from_entity_to_domain(
            self.get_repository().get_by_id(_id)
        )

    def list_items(self, pageable: Optional[Pageable] = None, filters: Optional[dict] = None,
                   group_by: Optional[list] = None, group_by_id: Optional[str] = None) -> List[D]:
        """Get all items"""

        return [
            self.get_mapper().map_from_entity_to_domain(entity)
            for entity in self.get_repository().get_all(pageable, filters, group_by, group_by_id)
        ]

    def create_item(self, item: D) -> D:
        """Create a new item"""

        return self.get_mapper().map_from_entity_to_domain(
            self.get_repository().create(
                self.get_mapper().map_from_domain_to_entity(item)
            )
        )

    def update_item(self, _id: I, item: D) -> D:
        """Update an item"""

        return self.get_mapper().map_from_entity_to_domain(
            self.get_repository().update(
                _id, self.get_mapper().map_from_domain_to_entity(item)
            )
        )

    def delete_item(self, _id: I):
        """Delete an item"""
        return self.get_repository().delete_by_id(_id)
