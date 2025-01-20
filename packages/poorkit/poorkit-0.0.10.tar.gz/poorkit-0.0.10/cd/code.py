import os
from click import *
from .util import extract_code_from_directory


@group()
def code() -> None:
    pass


@command(help="collect code")
@option("--dirs", help="list of directories", required=True, multiple=True, type=str)
@option(
    "--langs",
    help="list of languages",
    multiple=True,
    type=str,
)
@option("--output", help="output file", required=True)
def collect(dirs, langs, output) -> None:
    print(f"dirs: {dirs}, langs: {langs}, output: {output}")
    extract_code_from_directory(dirs, langs, output)


code.add_command(collect)
