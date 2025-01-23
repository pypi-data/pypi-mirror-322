import typer
import pyperclip
from rich import print
from rich.panel import Panel
from rich.syntax import Syntax
from rich.traceback import install
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from typing import Optional
from enum import Enum
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from catppuccin.extras.pygments import MochaStyle
import importlib.metadata
import time

# Install rich traceback handler
install(show_locals=True)

from .lib.curl_parser import CurlParser
from .lib.grab import GrabCodeWriter
from .lib.context import ContextCodeWriter

app = typer.Typer(
    help="Convert cURL commands to Python code for Grab/Context frameworks",
    add_completion=True,
    no_args_is_help=True
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
    """Interactive framework selection with autocomplete and syntax highlighting."""
    frameworks = [f.value for f in Framework]
    
    # Create styled completer
    style = Style.from_dict({
        'completion-menu.completion': 'bg:#1e1e2e #cdd6f4',
        'completion-menu.completion.current': 'bg:#313244 #cdd6f4',
        'completion-menu.meta.completion': 'bg:#1e1e2e #cdd6f4',
        'completion-menu.meta.completion.current': 'bg:#313244 #cdd6f4',
        'completion.grab': 'bg:#1e1e2e #89b4fa',  # Catppuccin Blue
        'completion.context': 'bg:#1e1e2e #f9e2af',  # Catppuccin Yellow
    })
    
    framework_completer = WordCompleter(
        frameworks,
        ignore_case=True,
        meta_dict={
            'grab': 'Grab framework',
            'context': 'Context framework'
        },
        style_dict={
            'grab': 'class:completion.grab',
            'context': 'class:completion.context'
        }
    )
    
    while True:
        try:
            selected = Prompt.ask(
                "[cyan]Choose framework[/cyan]",
                choices=frameworks,
                default=Framework.GRAB.value
            )
            return Framework(selected.lower())
        except ValueError:
            print("[red]Invalid framework. Please choose 'grab' or 'context'[/red]")

def display_code(code: str, language: str = "python"):
    """Display code with syntax highlighting using Catppuccin theme."""
    syntax = Syntax(
        code,
        language,
        theme=MochaStyle,
        line_numbers=True,
        word_wrap=True,
    )
    panel = Panel(
        syntax,
        expand=False,
        border_style="#89dceb",  # Catppuccin Sky
        title=f"Generated {language.capitalize()} Code",
        title_align="left",
    )
    print(panel)

def get_curl_command() -> str:
    """Get curl command from clipboard with loading animation."""
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]Waiting for curl command...[/cyan]"),
        transient=True,
    ) as progress:
        progress.add_task("waiting")
        input("Copy curl command to clipboard and press Enter...")
        
    curl_command = pyperclip.paste()
    
    if not curl_command.strip().startswith('curl '):
        raise ValueError("Invalid curl command. Please copy a valid curl command to clipboard.")
    
    return curl_command

def form_code(parsed_curl: dict, framework: Framework) -> str:
    """Generate framework-specific code from parsed curl command."""
    if framework == Framework.GRAB:
        writer = GrabCodeWriter(parsed_curl)
    else:
        writer = ContextCodeWriter(parsed_curl)
    
    code = writer.generate_code()
    
    # Syntax highlight the generated code
    return str(Syntax(code, "python", theme="monokai"))

def version_callback(value: bool):
    """Callback for --version flag."""
    if value:
        version = get_version()
        print(f"curl-to-context version: {version}")
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
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
    if ctx.invoked_subcommand is None:
        # If no subcommand provided, run convert without args
        ctx.invoke(convert)

@app.command()
def convert(
    framework: Optional[Framework] = typer.Option(
        None,
        "--framework",
        "-f",
        help="Framework to use (grab or context)"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v", 
        help="Display the converted code in terminal"
    )
):
    """Convert a cURL command from clipboard to Python code."""
    try:
        if not framework:
            framework = get_framework()
            print()  # Add spacing
        
        curl_command = get_curl_command()
        parsed_curl = CurlParser.parse_curl(curl_command)
        python_code = form_code(parsed_curl, framework=framework)
        
        # Copy plain text to clipboard
        pyperclip.copy(python_code)
        print(f"[green]✓[/green] Converted code has been copied to clipboard!")
        
        # If verbose, display with syntax highlighting
        if verbose:
            display_code(python_code)
            
    except Exception as e:
        print(f"[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

def curl_to_context():
    """Main entry point - same as running curl-to-context."""
    app()

# Aliases for backward compatibility
c2c = curl_to_context  # alias for curl-to-context
c2g = lambda: app(["convert", "--framework", "grab"])  # alias for grab framework
curl2context = lambda: app(["convert", "--framework", "context"])  # alias for context framework
curl2grab = lambda: app(["convert", "--framework", "grab"])  # alias for grab framework

if __name__ == "__main__":
    app()