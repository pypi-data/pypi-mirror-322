"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseUseCase(ABC):
    """Base class for use cases"""

    @abstractmethod
    def invoke(self, data: Any) -> Any:
        """Invoke the use case"""
        raise NotImplementedError


class UnitOfWork(ABC):
    """UnitOfWork class for database transactions"""

    def __init__(self, session_factory: callable):  # type: ignore
        self._session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the session and manager commit or rollback transaction

        :param exc_type: Exception type if occurs an exception
        :param exc_value: Exception value
        :param traceback: Traceback of the exception
        """

        if exc_type is None:
            self.session.commit()  # type: ignore
        else:
            self.session.rollback()  # type: ignore
        self.session.close()  # type: ignore

    def commit(self):
        """Force the commit over the transaction"""
        if self.session:
            self.session.commit()

    def rollback(self):
        """Force the rollback over the transaction"""
        if self.session:
            self.session.rollback()
