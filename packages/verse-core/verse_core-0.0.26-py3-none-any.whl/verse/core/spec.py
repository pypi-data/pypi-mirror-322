from __future__ import annotations

from enum import Enum

from ._yaml_loader import YamlLoader
from .constants import ROOT_PACKAGE_NAME
from .data_model import DataModel
from .exceptions import NotFoundError

__all__ = [
    "Kind",
    "ComponentSpec",
    "ContentModal",
    "OperationArgSpec",
    "OperationExceptionSpec",
    "OperationReturnSpec",
    "OperationSpec",
    "ParameterOptionSpec",
    "ParameterSpec",
    "ProviderMode",
    "ProviderSpec",
    "PySpec",
    "TypePropertySpec",
    "TypeSpec",
]


class Kind(str, Enum):
    BASE = "base"
    CUSTOM = "custom"


class ContentModal(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    MULTI = "multi"


class ProviderMode(str, Enum):
    MIXED = "mixed"
    LOCAL = "local"
    SERVICE = "service"


class ParameterOptionSpec(DataModel):
    label: str
    value: str | int | float | bool | None


class ParameterSpec(DataModel):
    name: str
    type: str
    description: str | None = None
    required: bool = True
    default: str | int | float | bool | dict | list | None = None
    options: list[ParameterOptionSpec] = []


class OperationArgSpec(DataModel):
    name: str
    type: str
    description: str | None = None
    required: bool = True
    default: str | int | float | bool | dict | list | None = None


class OperationReturnSpec(DataModel):
    type: str
    description: str | None = None


class OperationExceptionSpec(DataModel):
    type: str
    description: str | None = None


class OperationSpec(DataModel):
    name: str
    args: list[OperationArgSpec] = []
    description: str | None = None
    ret: OperationReturnSpec | None = None
    exceptions: list[OperationExceptionSpec] = []


class TypePropertySpec(DataModel):
    name: str
    type: str
    description: str | None = None
    required: bool | None = True
    default: str | int | float | bool | dict | list | None = None


class TypeSpec(DataModel):
    name: str
    description: str | None = None
    properties: list[TypePropertySpec] = []


class PySpec(DataModel):
    package: str | None = None
    path: str | None = None
    requirements: list[str] = []


class ProviderSpec(DataModel):
    name: str
    version: str | None = None
    title: str | None = None
    description: str | None = None
    logo: str | None = None
    author: str | None = None
    readme: str | None = None
    link: str | None = None
    kind: Kind = Kind.BASE
    mode: ProviderMode = ProviderMode.MIXED
    parameters: list[ParameterSpec] = []
    py: PySpec | None = None


class ComponentSpec(DataModel):
    name: str
    version: str | None = None
    title: str | None = None
    description: str | None = None
    logo: str | None = None
    author: str | None = None
    readme: str | None = None
    link: str | None = None
    category: str | None = None
    modals: list[ContentModal] = []
    kind: Kind = Kind.BASE
    parameters: list[ParameterSpec] = []
    operations: list[OperationSpec] = []
    providers: list[ProviderSpec] = []
    types: list[TypeSpec] = []
    py: PySpec | None = None

    @staticmethod
    def parse(path: str) -> ComponentSpec:
        obj = YamlLoader.load(path=path)
        manifest = ComponentSpec.from_dict(obj)
        return manifest

    def get_provider(self, name: str) -> ProviderSpec:
        for provider in self.providers:
            if name == provider.name:
                return provider
        raise NotFoundError("Provider not found")

    def get_py_path(self) -> str | None:
        if self.py is not None and self.py.path is not None:
            return self.py.path
        if self.kind == Kind.CUSTOM:
            return "./component.py"
        namespace = f"{ROOT_PACKAGE_NAME}.components.{self.name}"
        return f"{namespace}.component"

    def get_provider_py_path(self, name: str) -> str:
        provider_spec = self.get_provider(name=name)
        if provider_spec.py is not None and provider_spec.py.path is not None:
            return provider_spec.py.path
        if self.kind == Kind.CUSTOM or provider_spec.kind == Kind.CUSTOM:
            return f"./providers/{provider_spec.name}.py"
        namespace = f"{ROOT_PACKAGE_NAME}.components.{self.name}"
        return f"{namespace}.providers.{provider_spec.name}"
