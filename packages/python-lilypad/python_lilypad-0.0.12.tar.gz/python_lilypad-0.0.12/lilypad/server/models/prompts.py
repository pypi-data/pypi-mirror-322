"""Prompts table and models."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any
from uuid import UUID

from mirascope.core.base import CommonCallParams
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from .base_organization_sql_model import BaseOrganizationSQLModel
from .base_sql_model import get_json_column
from .table_names import PROJECT_TABLE_NAME, PROMPT_TABLE_NAME

if TYPE_CHECKING:
    from .generations import GenerationTable
    from .projects import ProjectTable
    from .spans import SpanTable


class Provider(str, Enum):
    """Provider name enum"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"
    GEMINI = "gemini"


class _PromptBase(SQLModel):
    """Base Prompt Model."""

    project_uuid: UUID | None = Field(
        default=None, foreign_key=f"{PROJECT_TABLE_NAME}.uuid", ondelete="CASCADE"
    )
    version_num: int | None = Field(default=None)
    name: str = Field(nullable=False, index=True, min_length=1)
    signature: str = Field(nullable=False)
    code: str = Field(nullable=False)
    hash: str = Field(nullable=False, index=True)
    dependencies: dict[str, str] = Field(
        sa_column=get_json_column(), default_factory=dict
    )
    template: str
    is_default: bool = Field(default=False)
    call_params: CommonCallParams = Field(
        sa_column=get_json_column(), default_factory=dict
    )
    arg_types: dict[str, str] = Field(sa_column=get_json_column(), default_factory=dict)
    archived: datetime | None = Field(default=None, index=True)


class PromptPublic(_PromptBase):
    """Prompt public model."""

    uuid: UUID


class PromptCreate(_PromptBase):
    """Prompt create model."""


class PromptUpdate(SQLModel):
    """Prompt update model"""

    is_default: bool | None = None


class PromptTable(_PromptBase, BaseOrganizationSQLModel, table=True):
    """Prompt table."""

    __tablename__ = PROMPT_TABLE_NAME  # type: ignore

    project: "ProjectTable" = Relationship(back_populates="prompts")
    spans: list["SpanTable"] = Relationship(
        back_populates="prompt", cascade_delete=True
    )
    generations: list["GenerationTable"] = Relationship(
        back_populates="prompt", cascade_delete=True
    )


class PlaygroundParameters(BaseModel):
    """Playground parameters model."""

    arg_values: dict[str, Any]
    provider: Provider
    model: str
    prompt: PromptCreate | None = None
