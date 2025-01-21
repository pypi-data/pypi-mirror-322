import importlib.metadata
import pathlib
import sys

import click

from mdslides import Engines

__version__ = importlib.metadata.version("mdslides")


@click.command()
@click.option("--engine", "-e", default="pandoc:slidy", help="Slide engine to use.")
@click.option("--list-engines", is_flag=True, help="List available slide engines.")
@click.option("--version", is_flag=True, help="Print version number.")
@click.argument("input", type=click.Path(exists=True), nargs=-1)
def main(engine, list_engines, version, input):
    if version:
        print(f"version: {__version__}")
        sys.exit(0)

    if list_engines:
        print("Available Engines")
        print("  pandoc:slidy")
        print("  pandoc:powerpoint")
        print("  pandoc:revealjs")
        sys.exit(0)

    eng = None
    if engine.startswith("pandoc"):
        if engine.endswith(":slidy"):
            eng = Engines.PandocSlidy()
        if engine.endswith(":powerpoint") or engine.endswith(":ppt"):
            eng = Engines.PandocPowerPoint()
        if engine.endswith(":revealjs") or engine.endswith(":reveal"):
            eng = Engines.PandocRevealJS()

    if eng is None:
        print(f"Unreconized engine {engine}")
        sys.exit(1)

    for file in input:
        eng.build(click.format_filename(file))
