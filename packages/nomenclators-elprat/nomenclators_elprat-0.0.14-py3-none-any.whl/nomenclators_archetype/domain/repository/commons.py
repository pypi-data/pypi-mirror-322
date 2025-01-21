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
from nomenclators_archetype.domain.repository.builders import Pageable, RequiredElementError

D = TypeVar('D', bound=object)  # Domain class representation
I = TypeVar('I', bound=object)  # Intentifier class representation
P = TypeVar('P', bound=object)  # Persistence class representation
S = TypeVar('S', bound=object)  # Session class representation
Q = TypeVar('Q', bound=object)  # Query class representation


class RepositoryOperationError(Exception):
    """RepositoryOperationError exception Class"""


class CrudRepository(Protocol[D, I, P, S, Q]):
    """CrudRepository Class"""

    @abstractmethod
    def get_builder(self) -> Q:
        """Get query builder operator for repository class"""

    @abstractmethod
    def get_session(self) -> S:
        """Get query session operator for repository class"""

    @abstractmethod
    def get_peristence_model(self) -> P:
        """Get persistence class"""

    def save(self, entity: P) -> P:
        """Save an entity (create or update)."""
        session = self.get_session()
        try:
            session.add(entity)
            return entity
        except Exception as e:
            raise RepositoryOperationError("Error on save entity") from e

    def update(self, entity: P) -> P:
        """Update an entity."""
        session = self.get_session()
        try:
            session.merge(entity)
            return entity
        except Exception as e:
            raise RepositoryOperationError("Error on update entity") from e

    def delete(self, entity: P):
        """Remove of an entity."""
        session = self.get_session()
        session.delete(entity)

    def delete_by_id(self, _id: I):
        """Removes an entity by its id."""
        entity = self.get_by_id(_id)
        if entity:
            self.delete(entity)

    def delete_all(self):
        """Removes all entities."""
        query = self.create_builder().build()
        query.delete()

    def create_builder(self):
        """Create a new query builder instance"""
        return self.get_builder().set_session(self.get_session()).set_model(self.get_peristence_model())

    def get_by_id(self, _id: I) -> P:
        """Get domain element by ID"""
        return self.get_session().get(self.get_peristence_model(), _id)

    def exists_by_id(self,  _id: I) -> P:
        """Checks if an entity exists by its id."""
        query = self.create_builder().build()
        return query.filter_by(id=_id).first()

    def get_all(self) -> List[P]:
        """Retrieves all entities."""
        query = self.create_builder().build()
        return query.filter_by(active=True).all()

    def get_garbage_all(self) -> List[P]:
        """Retrieves all entities deleted that exist on garbage collector."""
        query = self.create_builder().build()
        return query.filter_by(active=False).all()

    def garbage_recover(self, entity: P):
        """Recover an entity from garbage collector."""
        if not entity.active:
            entity.active = True
            self.update(entity)
        else:
            raise RequiredElementError(
                f"The entity ID {entity.id} is not deleted")

    def garbage_recover_by_id(self, _id: I):
        """Recover an entity from garbage collector by its id."""
        entity = self.get_by_id(_id)
        if entity:
            self.garbage_recover(entity)


class PagingAndSortingRepository(CrudRepository[D, I, P, S, Q]):
    """PagingAndSortingRepository Class"""

    @abstractmethod
    def get_peristence_model(self) -> P:
        """Get persistence class"""

    def get_all(self, pageable: Optional[Pageable] = None) -> List[P]:
        """Retrieves pageable and sorted entities."""
        query = self.create_builder().set_options(pageable).build()
        return query.filter_by(active=True).all()


class JpaRepository(PagingAndSortingRepository[D, I, P, S, Q]):
    """JpaRepository Class"""

    @abstractmethod
    def get_peristence_model(self) -> P:
        """Get persistence class"""

    def get_all(self, pageable: Optional[Pageable] = None, filters: Optional[dict] = None,
                group_by: Optional[list] = None, group_by_id: Optional[str] = None) -> List[P]:
        """Retrieves pageable and sorted entities."""

        query = self.create_builder().set_filter({'active': True}).set_filter(filters).set_group(
            group_by, group_by_id).set_options(pageable).build()

        return query.all()

    def save_and_flush(self, entity: P) -> P:
        """Save an entity and sync immediately."""
        self.save(entity)
        self.get_session().flush()
        return entity

    def create(self, entity: P) -> P:
        """Create a new entity."""
        return self.save_and_flush(entity)

    def delete_all_in_batch(self):
        """Removes all entities in a single operation."""
        query = self.create_builder().build()
        query.delete(synchronize_session=False)

    def delete_all_by_id_in_batch(self, ids):
        """Removes multiple entities by their ids in a single operation."""
        query = self.create_builder().build()
        query.filter(self.get_peristence_model().id.in_(ids)).delete(
            synchronize_session=False)

    def find_by_spec(self, spec, pageable: Optional[Pageable] = None) -> List[P]:
        """Allows dynamic queries based on criteria."""
        query = self.create_builder().set_options(pageable).build()
        return query.filter(spec).all()
