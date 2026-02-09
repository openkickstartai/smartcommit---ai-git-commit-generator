"""Git utilities for SmartCommit"""

from pathlib import Path
from typing import Optional
import git


class GitUtils:
    """Helper class for git operations."""
    
    def __init__(self, repo_path: Optional[Path] = None) -> None:
        self.repo_path = repo_path or Path.cwd()
        try:
            self.repo = git.Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError("Not a git repository")
    
    def get_diff(self, staged: bool = True) -> str:
        """Get git diff as string."""
        if staged:
            return self.repo.git.diff("--cached")
        return self.repo.git.diff()
    
    def get_history(self, limit: int = 10) -> list[str]:
        """Get recent commit messages."""
        commits = list(self.repo.iter_commits(max_count=limit))
        return [c.message.strip() for c in commits]
    
    def commit(self, message: str, staged: bool = True) -> None:
        """Create a commit with the given message."""
        if not staged:
            # Stage all changes
            self.repo.git.add("-A")
        
        self.repo.index.commit(message)
    
    def has_changes(self) -> bool:
        """Check if there are any changes."""
        return bool(self.repo.is_dirty() or self.repo.untracked_files)