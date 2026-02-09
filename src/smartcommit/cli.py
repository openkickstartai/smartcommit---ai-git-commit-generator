"""Command-line interface for SmartCommit"""

import typer
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from smartcommit.commit_generator import CommitGenerator
from smartcommit.git_utils import GitUtils
from smartcommit.config import Config

app = typer.Typer(
    name="smartcommit",
    help="AI-powered git commit message generator",
    add_completion=False,
)
console = Console()


@app.command()
def main(
    unstaged: bool = typer.Option(False, "--unstaged", "-u", help="Analyze unstaged changes"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Interactive mode"),
    install_hook: bool = typer.Option(False, "--install-hook", help="Install as git pre-commit hook"),
    config_path: Path = typer.Option(
        None, "--config", "-c", help="Path to config file"
    ),
) -> None:
    """Generate AI-powered commit messages from git diff."""
    
    if install_hook:
        _install_hook()
        return
    
    # Load config
    config = Config.load(config_path)
    
    # Initialize components
    git = GitUtils()
    generator = CommitGenerator(config)
    
    # Get diff
    console.print("\n[bold blue]🔍 Analyzing changes...[/bold blue]\n")
    diff = git.get_diff(staged=not unstaged)
    
    if not diff:
        console.print("[yellow]No changes detected![/yellow]")
        return
    
    # Generate commit message
    console.print("[bold green]🤖 Generating commit message...[/bold green]\n")
    commit_msg = generator.generate(diff, git.get_history())
    
    # Display result
    console.print(
        Panel(
            commit_msg,
            title="[bold]Generated Commit Message[/bold]",
            border_style="green",
        )
    )
    
    if interactive:
        if typer.confirm("\nUse this commit message?", default=True):
            git.commit(commit_msg, staged=not unstaged)
            console.print("[green]✓ Committed successfully![/green]")
    else:
        console.print("\n[yellow]Run with --interactive to commit[/yellow]")


def _install_hook() -> None:
    """Install smartcommit as a git pre-commit hook."""
    git_dir = Path(".git/hooks")
    if not git_dir.exists():
        console.print("[red]Not in a git repository![/red]")
        raise typer.Exit(1)
    
    hook_path = git_dir / "pre-commit"
    hook_content = """#!/bin/bash
smartcommit --interactive || exit 1
"""
    
    hook_path.write_text(hook_content)
    hook_path.chmod(0o755)
    console.print("[green]✓ Pre-commit hook installed![/green]")


if __name__ == "__main__":
    app()