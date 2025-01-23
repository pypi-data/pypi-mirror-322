from collections import defaultdict
from typing import List, Dict, Any

from pydantic import BaseModel, Field, PrivateAttr

from moatless.artifacts.artifact import Artifact, ArtifactHandler, SearchCriteria


class Workspace(BaseModel):
    artifacts: List[Artifact] = Field(default_factory=list)
    artifact_handlers: Dict[str, ArtifactHandler] = Field(default_factory=dict, exclude=True)

    _artifacts_by_id: Dict[str, Artifact] = PrivateAttr(default_factory=dict)
    _artifacts_by_type: Dict[str, List[Artifact]] = PrivateAttr(default_factory=lambda: defaultdict(list))

    def __init__(self, artifact_handlers: List[ArtifactHandler], **data):
        super().__init__(**data)
        self.artifact_handlers = {handler.type: handler for handler in artifact_handlers}

    def create_artifact(self, artifact: Artifact) -> Artifact:
        if artifact.type in self.artifact_handlers:
            handler = self.artifact_handlers[artifact.type]
            artifact = handler.create(artifact)

        self.artifacts.append(artifact)
        self._artifacts_by_id[artifact.id] = artifact
        self._artifacts_by_type[artifact.type].append(artifact)
        return artifact

    def get_artifact_by_id(self, artifact_id: str) -> Artifact | None:
        artifact = self._artifacts_by_id.get(artifact_id)
        if artifact:
            handler = self._get_handler(artifact.type)
            artifact = handler.read(artifact_id)
        return artifact

    def get_artifacts_by_type(self, artifact_type: str) -> List[Artifact]:
        return self._artifacts_by_type[artifact_type]

    def update_artifact(self, artifact: Artifact) -> None:
        handler = self.artifact_handlers[artifact.type]
        handler.update(artifact)

    def _get_handler(self, artifact_type: str) -> ArtifactHandler:
        return self.artifact_handlers[artifact_type]

    def model_post_init(self, __context) -> None:
        """Rebuild lookup dictionaries and handlers after loading from JSON"""
        self._artifacts_by_id.clear()
        self._artifacts_by_type.clear()
        for artifact in self.artifacts:
            self._artifacts_by_id[artifact.id] = artifact
            self._artifacts_by_type[artifact.type].append(artifact)

        self.artifact_handlers = {handler.type: handler for handler in self.artifact_handlers.values()}

    def dump_handlers(self) -> Dict[str, Any]:
        """Dump artifact handlers to a serializable format"""
        return {key: handler.model_dump() for key, handler in self.artifact_handlers.items()}

    def clone(self):
        cloned_workspace = Workspace(artifact_handlers=list(self.artifact_handlers.values()), artifacts=self.artifacts)
        return cloned_workspace

    def search(self, artifact_type: str, criteria: List[SearchCriteria]) -> List[Artifact]:
        """
        Search for artifacts of a specific type using the provided criteria
        """
        if artifact_type not in self.artifact_handlers:
            raise ValueError(f"No handler found for artifact type: {artifact_type}")
            
        handler = self.artifact_handlers[artifact_type]
        return handler.search(criteria)
