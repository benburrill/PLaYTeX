import click
import contextlib
from playtex.files import file_render

def silent_echo(*args, **kwargs):
    # Suppress erroneous OSErrors
    with contextlib.suppress(OSError):
        return click.echo(*args, **kwargs)

@click.command()
@click.argument("renderer")
@click.argument("player")
@click.option("--encoding", default="utf-8")
@click.option("--player-file", default="playtex-players.yaml")
@click.option("--cache/--no-cache", default=True)
def main(renderer, player, *, encoding, player_file, cache):
    latex = file_render(renderer, player, player_file, do_cache=cache)
    silent_echo(latex.encode(encoding), nl=False)

if __name__ == "__main__":
    main()
