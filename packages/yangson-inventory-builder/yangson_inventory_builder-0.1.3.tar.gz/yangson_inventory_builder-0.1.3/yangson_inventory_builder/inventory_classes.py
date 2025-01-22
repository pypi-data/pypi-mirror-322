from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel, field_validator
from pathlib import Path
import logging
logger = logging.getLogger("yang_parser_app")


def exception_wrapper(errors=(Exception,), default_value=None):
    def decorator(func):
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                logger.error(f'Function "{func.__name__}", with parameters: "{args, kwargs}",'
                             f'failed with exception: "{e}"')
                return default_value

        return new_func

    return decorator


class ModuleType(str, Enum):
    MODULE = "module"
    SUBMODULE = "submodule"


class ModelType(Enum):
    NOKIA = "nokia"
    JUNIPER = "juniper"


class RevisionNotFound(Exception):
    pass


class InvalidRequest(Exception):
    pass


@dataclass
class YangNode:
    name: str = ""
    description: str = ""


@dataclass
class YangContainerNode(YangNode):
    children: list = field(default_factory=list)


@dataclass
class YangLeafListNode(YangNode):
    max_elements: int = field(default_factory=int)
    type: str = ""


@dataclass
class YangListNode(YangNode):
    children: list = field(default_factory=list)


@dataclass
class YangLeafNode(YangNode):
    type: str = ""


@dataclass
class YangChoiceNode(YangNode):
    children: list = field(default_factory=list)


@dataclass
class YangCaseNode(YangNode):
    children: list = field(default_factory=list)

@dataclass
class YangModuleInventory:
    is_part_of_root_module: bool = False
    module_type: str = ""
    file_name: str = ""
    name: str = ""
    revision: str = ""
    conformance_type: str = ""
    namespace: str = ""
    submodule: list[dict] = field(default_factory=list)
    imported_modules: list[str] = field(default_factory=list)
    included_modules: list[str] = field(default_factory=list)

    def __hash__(self):
        return hash(self.file_name)

    def as_module(self) -> dict:
        """
        Representation for the YANGson inventory file
        """
        return {
            "name": self.name,
            "revision": self.revision,
            "conformance-type": self.conformance_type,
            "namespace": self.namespace,
            "submodule": self.submodule,
        }

    def as_submodule(self) -> dict:
        return {
            "name": self.name,
            "revision": self.revision,
        }


class YangsonInventoryRequest(BaseModel):
    yang_directory: Path
    root_config_module: Path | None
    target_inventory_file_name: Path

    @field_validator("yang_directory")
    @classmethod
    def validate_yang_directory(cls, value: Path) -> Path:
        if value.exists():
            return value.absolute()
        raise InvalidRequest(f'Can not find provided YANG Model directory: "{value}"')

    @field_validator("root_config_module")
    @classmethod
    def validate_root_config_module(cls, value: Path) -> Path | None:
        if not value:
            logger.info(f"Root config module is not provided")
            return
        if not value.is_file():
            raise InvalidRequest(f'Can not find provided root YANG module: "{value}"')
        return value.absolute()
