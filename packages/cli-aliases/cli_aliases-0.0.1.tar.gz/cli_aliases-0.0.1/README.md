# cli-aliases
cli-aliases is a simple implemention to set aliases for your Click CLI. 

# Installation
## Dependencies
- Click (>=8.1.8)

Install the package by entering `pip install cli-aliases` in your terminal.

# Usage: a simple example
```
import click
from cmd_aliases import AliasedGroup, AliasConfig

AliasConfig.add_alias("helloworld", "welcome")  # set a single alias entry in the form '(command, alias)'


@click.command(cls=AliasedGroup) # make sure to use the class, not an instance of it
def cli():
    pass


@cli.command()
def HelloWorld():
    click.echo("Hello World!")


if __name__ == "__main__":
    cli()
```

# TODO
- Add multiple alias comprehension
