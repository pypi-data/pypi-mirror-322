from typing import ClassVar, Generic, TypeVar
from typing_extensions import Self


T = TypeVar("T", bound="ParentModel", covariant=True)


class ParentManager(Generic[T]):
    pass


class ParentModel:
    objects: ClassVar[ParentManager[Self]] = ParentManager()


class ChildManager(ParentManager[T]):
    pass


class ChildModel(ParentModel):
    objects: ClassVar[ChildManager[Self]] = ChildManager()
