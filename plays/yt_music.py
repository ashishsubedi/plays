from youtube_search import YoutubeSearch
import click
from enum import Enum, auto

import json
import subprocess as sp
from plays.utils import cmd
from os.path import expanduser, exists, join
from os import mkdir, name


class QueryType(Enum):
    URL = auto()
    TEXT = auto()


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
            return QueryType.URL
        else:
            return QueryType.TEXT

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

        else:
            output, err = cmd(["youtube-dl", "-g", "-e", query])
            print(output, err)
            if err:
                raise Exception(err)

            audio_url = output.split("\n")
            try:
                self.url = audio_url[2]
            except Exception:
                raise Exception("No audio found!")

            click.clear()
            click.echo(f"Selected {audio_url[0]}")
            self.title = audio_url[0]

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

        sp.Popen(
            [
                mpv,
                self.url,
                "--no-video",
                "--window-minimized",
                "--cache=",
                "yes",
                "--cache-on-disk=",
                "yes",
                f"--cache-dir={cache_dir}",
            ]
        ).wait()

    def play(self):
        if not self.url:
            raise Exception("Please Search before playing!!")

        self._play()
