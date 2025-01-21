"""
----------------------------------------------------------------------------------------------------
Written by:
  - Yovany Dominico Girón (y.dominico.giron@elprat.cat)
  - Enrique Martinez Alcantara (e.martinez.alcantara@elprat.cat)

for Ajuntament del Prat de Llobregat
----------------------------------------------------------------------------------------------------

----------------------------------------------------------------------------------------------------
"""
from abc import ABC
from typing import Union, Optional

NomenclatorId = Union[int, str, None]


class BaseSimpleNomenclator(ABC):
    """Classe base para los nomencladores"""

    def __init__(self, identifier: Optional[NomenclatorId] = None, name: Optional[str] = None):
        if not name:
            raise ValueError(
                "The 'name' field of the nomenclator is mandatory")

        self.id = identifier
        self.name = name

    def __composite_values__(self) -> tuple:
        return (
            self.id, self.name
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(\n"
            f"  id={self.id}, name={self.name} \n"
            f")"
        )


class BaseNomenclator(BaseSimpleNomenclator):
    """Classe base para los nomencladores con descripción"""

    def __init__(self, identifier: NomenclatorId, name: str, description: Optional[str] = None):
        super().__init__(identifier, name)

        self.description = description

    def __composite_values__(self) -> tuple:
        return (
            self.id, self.name, self.description
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(\n"
            f"  id={self.id}, name={self.name}, \n"
            f"  description={self.description} \n"
            f")"
        )


class TreeNomenclator(BaseSimpleNomenclator):
    """Classe base para los nomencladores jerárquicos."""

    def __init__(self, identifier: Optional[NomenclatorId] = None,
                 name: Optional[str] = None, parent: Optional[NomenclatorId] = None,
                 level: Optional[int] = None, path: Optional[str] = None):
        super().__init__(identifier, name)
        self.parent = parent
        self.level = level
        self.path = path

    def __composite_values__(self) -> tuple:
        return (
            self.id, self.name, self.parent, self.level, self.path
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(\n"
            f"  id={self.id}, name={self.name}, \n"
            f"  parent={self.parent}, level={self.level}, \n"
            f"  path={self.path} \n"
            f")"
        )
