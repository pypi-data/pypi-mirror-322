import typer
import pyperclip
from rich import print
from rich.panel import Panel
from rich.syntax import Syntax
from typing import Optional
from enum import Enum
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import importlib.metadata

from .lib.curl_parser import CurlParser
from .lib.grab import GrabCodeWriter
from .lib.context import ContextCodeWriter

app = typer.Typer(
    help="Convert cURL commands to Python code for Grab/Context frameworks",
    add_completion=False
)

def get_version():
    """Get package version from pyproject.toml."""
    try:
        return importlib.metadata.version("curl-to-context")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"

class Framework(str, Enum):
    GRAB = "grab"
    CONTEXT = "context"

def get_framework() -> Framework:
    """Interactive framework selection with autocomplete."""
    frameworks = [f.value for f in Framework]
    framework_completer = WordCompleter(frameworks, ignore_case=True)
    
    while True:
        try:
            selected = prompt(
                "Choose framework: ",
                completer=framework_completer,
                default=Framework.GRAB.value
            )
            return Framework(selected.lower())
        except ValueError:
            print("[red]Invalid framework. Please choose 'grab' or 'context'[/red]")

def form_code(parsed_curl: dict, framework: Framework) -> str:
    """Generate framework-specific code from parsed curl command."""
    if framework == Framework.GRAB:
        writer = GrabCodeWriter(parsed_curl)
    else:
        writer = ContextCodeWriter(parsed_curl)
    return writer.generate_code()

def version_callback(value: bool):
    """Callback for --version flag."""
    if value:
        version = get_version()
        print(f"curl-to-context version: {version}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Show the application's version and exit.",
        callback=version_callback,
        is_eager=True,
    )
):
    """Convert cURL commands to Python code for Grab/Context frameworks."""
    pass

@app.command()
def convert(
    framework: Optional[Framework] = typer.Option(
        None,
        "--framework", 
        "-f",
        help="Target framework (grab or context)",
        case_sensitive=False
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v", 
        help="Display the converted code in terminal (will still copy to clipboard)"
    )
):
    """Convert a cURL command from clipboard to Python code."""
    if not framework:
        framework = get_framework()

    # Get clipboard content
    curl_command = pyperclip.paste()
    
    if not curl_command.strip().startswith('curl '):
        print("[red]Error:[/red] Invalid curl command. Please copy a valid curl command to clipboard.")
        raise typer.Exit(1)
    
    try:
        # Parse curl command using the more robust parser
        parsed_curl = CurlParser.parse_curl(curl_command)
        
        # Generate code using the framework-specific writer
        python_code = form_code(parsed_curl, framework=framework)
        
        # Always copy to clipboard
        pyperclip.copy(python_code)
        print(f"[green]✓[/green] Converted code (for {framework.value}) has been copied to clipboard!")
        
        # If verbose, also display the code
        if verbose:
            syntax = Syntax(python_code, "python", theme="monokai")
            print(Panel(
                syntax,
                title=f"Converted Code ({framework.value})",
                border_style="blue"
            ))
            
    except Exception as e:
        print(f"[red]Error:[/red] Failed to convert curl command: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()