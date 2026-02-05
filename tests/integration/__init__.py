from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _ensure_pydantic_stub() -> None:
    if "pydantic" in sys.modules:
        return
    if importlib.util.find_spec("pydantic") is not None:
        return

    class BaseModel:
        def __init__(self, **data):
            for key, value in data.items():
                setattr(self, key, value)

    def Field(default=None, description: str | None = None):
        return default

    stub = type(sys)("pydantic")
    stub.BaseModel = BaseModel
    stub.Field = Field
    sys.modules["pydantic"] = stub


def _ensure_crewai_stub() -> None:
    if "crewai.tools" in sys.modules:
        return
    if importlib.util.find_spec("crewai") is not None:
        return

    class BaseTool:
        pass

    tools_stub = type(sys)("crewai.tools")
    tools_stub.BaseTool = BaseTool
    sys.modules["crewai.tools"] = tools_stub


_ensure_pydantic_stub()
_ensure_crewai_stub()
