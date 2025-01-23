from abc import ABC, abstractmethod
from typing import Dict, Literal, Optional, Union, TypeVar, Generic, List, Any, Callable

from pydantic import BaseModel, Field

from moatless.completion.schema import MessageContentListBlock

class Artifact(BaseModel, ABC):
    id: Optional[str] = Field(default=None, description="Unique identifier for the artifact")
    type: str = Field(description="Type of artifact (e.g., 'receipt')")
    name: Optional[str] = Field(default=None, description="Name of the artifact")

    @abstractmethod
    def to_prompt_message_content(self) -> MessageContentListBlock:
        pass


class ArtifactChange(BaseModel):
    artifact_id: str
    change_type: Literal["added", "updated", "removed"]
    diff_details: Optional[str] = None
    actor: Literal["user", "assistant"]


# Create a TypeVar for the specific Artifact type
T = TypeVar("T", bound="Artifact")


class SearchCriteria(BaseModel):
    """Base class for defining search criteria"""
    field: str
    value: Any
    operator: Literal["eq", "contains", "gt", "lt", "gte", "lte"] = "eq"
    case_sensitive: bool = False


class ArtifactHandler(ABC, BaseModel, Generic[T]):
    """
    Defines how to load, save, update, and delete artifacts of a certain type.
    The type parameter T specifies which Artifact subclass this handler manages.
    """

    type: str = Field(description="Type of artifact this handler manages")


    @abstractmethod
    def read(self, artifact_id: str) -> T:
        pass

    @abstractmethod
    def create(self, artifact: T) -> T:
        pass

    def update(self, artifact: T) -> None:
        raise NotImplementedError("Update is not supported for this artifact type")

    def delete(self, artifact_id: str) -> None:
        raise NotImplementedError("Delete is not supported for this artifact type")

    def search(self, criteria: List[SearchCriteria]) -> List[T]:
        """
        Search for artifacts based on the provided criteria.
        Each handler implements its own search logic.
        """
        raise NotImplementedError("Search is not supported for this artifact type")