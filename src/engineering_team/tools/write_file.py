from __future__ import annotations
from pathlib import Path
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class WriteFileInput(BaseModel):
  path: str = Field(..., description="Relative file path under output/frontend/")
  content: str = Field(..., description="File contents")

class WriteFileTool(BaseTool):
  name: str = "write_file"
  description: str = "Write a file under output/frontend/. Use for creating a runnable Next.js project."
  args_schema: Type[BaseModel] = WriteFileInput

  def _run(self, path: str, content: str) -> str:
    # Must be inside output/frontend
    if path.startswith("/") or path.startswith("~"):
      raise ValueError("Absolute paths are not allowed.")
    p = Path(path)

    # block traversal
    if ".." in p.parts:
      raise ValueError("Path traversal '..' is not allowed.")

    # enforce output/frontend prefix
    prefix = Path("output/frontend")
    if not str(p).startswith(str(prefix)):
      raise ValueError("Path must start with output/frontend/")

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"Wrote {path}"