import pprint
import click
import threading
from plays.yt_music import YTMusic
import json


@click.command()
@click.argument("query")
def plays(query: str):
    """Searches the name/url and plays"""
    click.echo(query)
    music = YTMusic()

    if music.search(query):
        music.play()
    click.echo("Exiting...")
