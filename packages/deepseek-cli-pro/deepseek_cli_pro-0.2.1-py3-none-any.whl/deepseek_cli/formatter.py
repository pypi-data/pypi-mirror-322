from markdown import Markdown
from rich.text import Text
from rich.syntax import Syntax
from rich.panel import Panel

def format_stream(stream, markdown: bool = True) -> str: # type: ignore
    full_response = []
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        full_response.append(content)
        yield content if not markdown else Markdown(content)

def format_error(message: str) -> Panel:
    error_text = Text(f"ERROR: {message}", style="bold red")
    return Panel(
        error_text,
        title="[reverse] Error [/]",
        title_align="left",
        border_style="red",
        padding=(1, 2)
    )

def format_code(code: str, language: str = "python") -> Syntax:
    return Syntax(code, language, theme="monokai", line_numbers=True)