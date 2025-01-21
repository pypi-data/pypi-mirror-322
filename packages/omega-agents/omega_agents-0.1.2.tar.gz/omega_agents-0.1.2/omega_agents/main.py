## src/omega_agents/main.py

"""
Optional command-line interface (CLI) entry point for the package.
You could also omit this if you prefer a pure library approach.
"""

import click
from .supervisor import Supervisor

@click.command()
@click.option("--base-url", required=True, help="LLM base URL (e.g. https://api.openai.com/v1)")
@click.option("--api-key", required=True, help="LLM API key or token.")
@click.option("--model-name", default="", help="Model name (e.g. gpt-4o-mini). If omitted, the default is used.")
@click.option("--verbose", is_flag=True, default=False, help="Enable verbose logs.")
@click.option("--debug", is_flag=True, default=False, help="Enable debug logs.")
def cli(base_url, api_key, model_name, verbose, debug):
    """
    Basic CLI to demonstrate the Supervisor usage.
    """
    sup = Supervisor(
        base_url=base_url,
        api_key=api_key,
        model_name=model_name if model_name else None,
        verbose=verbose,
        debug=debug
    )

    click.echo("[CLI] Supervisor created. Now you can integrate tools, create agents, etc.")