import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.markdown import Markdown
from .api import DeepSeekClient
from .config import ConfigManager
from .formatter import format_stream, format_error

console = Console()
config = ConfigManager()

@click.group()
@click.version_option()
def cli():
    """DeepSeek CLI - Interactive AI-powered command line interface"""
    pass

@cli.command()
@click.option('--api-key', prompt=True, hide_input=True, help='Your DeepSeek API key')
def configure(api_key):
    """Configure API credentials"""
    config.save_api_key(api_key)
    console.print("[bold green]✓ Configuration saved successfully![/]")

@cli.command()
@click.argument('prompt', required=False)
@click.option('--model', default='deepseek-chat', help='Model to use for completion')
@click.option('--temperature', type=float, default=0.7, help='Creativity level (0.0-2.0)')
@click.option('--stream/--no-stream', default=True, help='Enable/disable streaming')
@click.option('--markdown/--no-markdown', default=True, help='Render markdown output')
def chat(prompt, model, temperature, stream, markdown):
    """Interactive chat with DeepSeek"""
    api_key = config.load_api_key()
    client = DeepSeekClient(api_key)
    
    messages = []
    if not prompt:
        console.print("[bold cyan]💬 DeepSeek Chat Mode (type 'exit' to quit)[/]")
    
    while True:
        try:
            user_input = prompt or click.prompt("[bold]You[/bold]", prompt_suffix=" ➜ ")
            if user_input.lower() == 'exit':
                break

            messages.append({"role": "user", "content": user_input})
            
            if stream:
                with console.status("[bold green]Generating...[/]", spinner="dots"):
                    response = client.stream_response(
                        messages=messages,
                        model=model,
                        temperature=temperature
                    )
                    assistant_response = format_stream(response, markdown)
            else:
                with Progress(transient=True) as progress:
                    task = progress.add_task("[cyan]Processing...", total=1)
                    response = client.chat_completion(
                        messages=messages,
                        model=model,
                        temperature=temperature
                    )
                    assistant_response = response.choices[0].message.content
                    progress.update(task, completed=1)

            messages.append({"role": "assistant", "content": assistant_response})
            
            if markdown:
                console.print(Panel(Markdown(assistant_response), title="[bold green]Assistant[/]", title_align="left"))
            else:
                console.print(Panel(assistant_response, title="[bold green]Assistant[/]", title_align="left"))
                
            prompt = None  # Reset prompt for subsequent interactions

        except Exception as e:
            console.print(format_error(str(e)))
            break

@cli.command()
@click.argument('prompt')
@click.option('--model', default='deepseek-chat', help='Model to use for completion')
@click.option('--temperature', type=float, default=0.7, help='Creativity level (0.0-2.0)')
def generate(prompt, model, temperature):
    """Generate content from a prompt"""
    api_key = config.load_api_key()
    client = DeepSeekClient(api_key)
    
    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=temperature
        )
        console.print(Panel(
            Markdown(response.choices[0].message.content),
            title="[bold blue]Generated Content[/]",
            title_align="left"
        ))
    except Exception as e:
        console.print(format_error(str(e)))

@cli.command()
def models():
    """List available models"""
    models = [
        {"name": "deepseek-chat", "description": "General purpose chat model"},
        {"name": "deepseek-coder", "description": "Code-specific model"},
        {"name": "deepseek-math", "description": "Math-focused model"}
    ]
    
    console.print("[bold]Available Models:[/]\n")
    for model in models:
        console.print(f"[cyan]▪ {model['name']}[/]")
        console.print(f"  {model['description']}\n")

if __name__ == '__main__':
    cli()