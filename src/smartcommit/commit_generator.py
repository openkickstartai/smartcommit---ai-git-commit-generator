"""AI-powered commit message generator"""

import os
from typing import Optional
from anthropic import Anthropic

from smartcommit.config import Config


class CommitGenerator:
    """Generate conventional commit messages using AI."""
    
    CONVENTIONAL_TYPES = [
        "feat", "fix", "docs", "style", "refactor", "test", "chore"
    ]
    
    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def generate(
        self,
        diff: str,
        history: Optional[list[str]] = None,
    ) -> str:
        """Generate a commit message from diff."""
        
        prompt = self._build_prompt(diff, history)
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        
        commit_msg = response.content[0].text.strip()
        
        # Ensure it follows conventional commit format
        return self._ensure_conventional(commit_msg)
    
    def _build_prompt(
        self,
        diff: str,
        history: Optional[list[str]] = None,
    ) -> str:
        """Build the prompt for the AI."""
        
        types_str = ", ".join(self.CONVENTIONAL_TYPES)
        
        prompt = f"""Generate a conventional commit message for this git diff.

Conventional commit types: {types_str}

Format: <type>(<scope>): <subject>

Rules:
- Use imperative mood ("add" not "added")
- Keep subject under {self.config.max_length} characters
- Be specific and descriptive
- Focus on WHAT changed, not WHY

Git diff:
```
{diff}
```
"""
        
        if history and self.config.learn_from_history:
            prompt += f"""\n
Recent commit messages for context:
{chr(10).join(history[-5:])}
"""
        
        return prompt
    
    def _ensure_conventional(self, commit_msg: str) -> str:
        """Ensure the commit message follows conventional format."""
        
        # Check if it already has a type
        for commit_type in self.CONVENTIONAL_TYPES:
            if commit_msg.startswith(f"{commit_type}(") or commit_msg.startswith(f"{commit_type}:"):
                return commit_msg
        
        # If not, prepend with chore:
        return f"chore: {commit_msg}"