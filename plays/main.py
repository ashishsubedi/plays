import click
from plays.yt_music import YTMusic


@click.command()
@click.argument("query", nargs=-1)
def plays(query: str):
    """Searches the name/url and plays"""
    query = " ".join(query)
    click.echo(query)
    music = YTMusic()

    if music.search(query):
        music.play()
    click.echo("Exiting...")
