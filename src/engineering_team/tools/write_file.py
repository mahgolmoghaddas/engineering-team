from __future__ import annotations

from pathlib import Path
from typing import Type

from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class WriteFileInput(BaseModel):
    path: str = Field(
        ...,
        description="Relative path to write (e.g. 'output/frontend/app/page.tsx'). "
                    "Must not be absolute and must not use '..'."
    )
    content: str = Field(..., description="Full file contents to write.")


class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = (
        "Write a file to disk inside the project. "
        "Use this to create real runnable project files (code/config). "
        "Only write to relative paths and never use '..' or absolute paths."
    )
    args_schema: Type[BaseModel] = WriteFileInput

    def _run(self, path: str, content: str) -> str:
        # Guardrails against path traversal
        if path.startswith("/") or path.startswith("~") or ".." in Path(path).parts:
            raise ValueError("Invalid path. Use a safe relative path without '..' or absolute prefixes.")

        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Wrote {path} ({len(content)} chars)"