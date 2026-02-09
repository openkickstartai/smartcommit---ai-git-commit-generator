"""Configuration management for SmartCommit"""

import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    """SmartCommit configuration."""
    
    commit_types: list[str] = Field(
        default=["feat", "fix", "docs", "style", "refactor", "test", "chore"],
        description="Allowed commit types",
    )
    max_length: int = Field(
        default=72,
        description="Maximum commit message length",
    )
    interactive: bool = Field(
        default=True,
        description="Enable interactive mode",
    )
    learn_from_history: bool = Field(
        default=True,
        description="Learn from project commit history",
    )
    
    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Config":
        """Load config from file or use defaults."""
        if path is None:
            path = Path.cwd() / ".smartcommit.json"
        
        if not path.exists():
            return cls()
        
        with open(path) as f:
            data = json.load(f)
        
        return cls(**data)