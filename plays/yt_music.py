from youtube_search import YoutubeSearch
import click
from enum import Enum, auto

import json
import subprocess as sp
from plays.utils import cmd
from os.path import expanduser, exists, join
from os import mkdir, name
import threading


class QueryType(Enum):
    URL = auto()
    TEXT = auto()
    PLAYLIST = auto()


class PlayStatus(Enum):
    STOPPED = auto()
    PLAYING = auto()
    PAUSED = auto()
    ERROR = auto()


class YTMusic:
    def __init__(self):
        self.url = None
        self.title = None

    def _text_or_url(self, query: str) -> str:
        if query.startswith("http"):
            if "list" in query:
                return QueryType.PLAYLIST
            return QueryType.URL
        else:
            return QueryType.TEXT

    def _extract_playlist(self, playlist_url: str):
        list_idx = playlist_url.find("list=")
        list_id = playlist_url[list_idx:]
        self.url = f"https://youtube.com/playlist?{list_id}"

    def search(self, query: str):
        click.echo("Searching...")
        qt = self._text_or_url(query)
        if qt == QueryType.TEXT:
            res = YoutubeSearch(query, max_results=10).to_json()
            data = json.loads(res)
            videos = data.get("videos", [])
            choices = [
                f"{i+1}) {video['title']} -> {video['channel']}-> {video['duration']}\n"
                for i, video in enumerate(videos)
            ]
            click.echo("\n".join(choices))

            choice = click.prompt(
                "Please select:",
                type=click.Choice([str(i + 1) for i in range(len(videos) + 1)]),
                default="1",
            )
            self.url = f'https://youtube.com{videos[int(choice)-1]["url_suffix"]}'
            click.clear()
            click.echo(
                f"Selected {videos[int(choice)-1]['title']} by {videos[int(choice)-1]['channel']}"
            )
            self.title = videos[int(choice) - 1]["title"]

        elif qt == QueryType.PLAYLIST:
            self._extract_playlist(query)
            click.clear()
            click.echo(f"Playing playlist: {self.url}")
            click.echo(f">: next, <: prev")
        else:
            self.url = query
            click.clear()
            click.echo(f"Playing {self.url}")

        return True

    def _play(self):
        home = expanduser("~")
        cache_dir = join(home, "plays")
        if not exists(cache_dir):
            mkdir(cache_dir)

        if name == "nt":
            mpv = "mpv.com"
        else:
            mpv = "mpv"

        player = sp.Popen(
            [
                mpv,
                self.url,
                "--no-video",
                "--window-minimized",
                "--cache=yes",
                "--cache-on-disk",
                f"--cache-dir={cache_dir}",
            ],
        ).wait()

    def play(self):
        if not self.url:
            raise Exception("Please Search before playing!!")

        self._play()
