from click import *
from cd.code import code
from fs.file import fs
from video.video import video
import pkg_resources

version = pkg_resources.require("poorkit")[0].version

help = f"""poorkit {version}\n
Reference: https://pypi.org/project/poorkit
"""


@group(help=help)
@version_option(version=version)
def cli() -> None:
    pass


cli.add_command(fs)
cli.add_command(video)
cli.add_command(code)
