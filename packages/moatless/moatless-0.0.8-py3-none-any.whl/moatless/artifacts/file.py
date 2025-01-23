from abc import ABC, abstractmethod
import base64
import io
import logging
import mimetypes
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageEnhance
import pymupdf as fitz

from dataclasses import dataclass

from pydantic import Field

from moatless.artifacts.artifact import (
    Artifact,
    ArtifactHandler
)
from moatless.completion.schema import ChatCompletionImageUrlObject, ChatCompletionTextObject, MessageContentListBlock


logger = logging.getLogger(__name__)

class FileArtifact(Artifact):
    type: str = "file"
    file_path: str = Field(description="Path on disk where the artifact is stored")
    mime_type: Optional[str] = Field(default=None, description="MIME type of the file content")
    content: Optional[bytes] = Field(default=None, description="Content of the file")

    def to_prompt_message_content(self) -> MessageContentListBlock:
        return ChatCompletionTextObject(type="text", text=self.content)
    
class TextFileArtifact(FileArtifact):

    content: str = Field(exclude=True)

    def to_prompt_message_content(self) -> MessageContentListBlock:
        return ChatCompletionTextObject(type="text", text=self.content)
    
class ImageFileArtifact(FileArtifact):

    base64_image: str = Field(exclude=True)

    def to_prompt_message_content(self) -> MessageContentListBlock:
        return ChatCompletionImageUrlObject(
            type="image_url",
            image_url={"url": f"data:{self.mime_type};base64,{self.base64_image}"}
        )


class FileArtifactHandler(ArtifactHandler[FileArtifact]):
    type: str = "file"
    directory_path: Path = Field(description="Base directory path for storing artifacts")

    max_image_size: Tuple[int, int] = Field(default=(1024, 1024), description="Maximum size of the image to save")
    quality: int = Field(default=85, description="Quality of the image to save")

    def _detect_mime_type(self, file_path: str) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"

    def read(self, artifact_id: str) -> FileArtifact:
        file_path = self.directory_path / artifact_id

        mime_type = self._detect_mime_type(str(file_path))
        logger.info(f"Loading artifact {artifact_id} with MIME type {mime_type}")

        if mime_type.startswith("image/"):
            return ImageFileArtifact(
                id=artifact_id,
                type=self.type,
                name=file_path.name,
                file_path=str(file_path),
                mime_type=mime_type,
                base64_image=self.encode_image(file_path.read_bytes())
            )
        elif mime_type.startswith("application/pdf"):
            content = self.read_pdf(str(file_path), file_path.read_bytes())
        else:
            # read content as text
            content = file_path.read_text()

        return TextFileArtifact(
            id=artifact_id,
            type=self.type,
            name=file_path.name,
            file_path=str(file_path),
            mime_type=mime_type,
            content=content
            )

    def create(self, artifact: FileArtifact) -> Artifact:
        file_path = self.directory_path / artifact.file_path
        if artifact.content:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving artifact {artifact.id} to {file_path}")
            file_path.write_bytes(artifact.content)

        return artifact

    def update(self, artifact: FileArtifact) -> None:
        self.save(artifact)

    def delete(self, artifact_id: str) -> None:
        file_path = self.directory_path / artifact_id
        if file_path.exists():
            file_path.unlink()

    def encode_image(self, file_content: bytes) -> str:
        """Encodes image bytes to base64 string"""
        return base64.b64encode(file_content).decode('utf-8')

    def preprocess_image(self, file_content: bytes) -> bytes:
        """Enhance image for document processing with focus on text clarity"""
        image = Image.open(io.BytesIO(file_content))
        image = image.convert('L')
        
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        if image.size[0] > self.max_image_size[0] or image.size[1] > self.max_image_size[1]:
            image.thumbnail(self.max_image_size, Image.Resampling.LANCZOS)
        
        image = image.convert('RGB')
        
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=self.quality, optimize=True)
        return output.getvalue()

    def read_pdf(self, file_path: str, file_content: bytes):
        """Extract text content from PDF"""
        pdf_content = f"Contents of file {file_path}:\n"
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                pdf_content += page.get_text()

        return pdf_content
