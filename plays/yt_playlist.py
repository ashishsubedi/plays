import sys
from youtube_search import YoutubeSearch
import click
from enum import Enum, auto

import json
import subprocess as sp
from plays.utils import cmd
from os.path import expanduser, exists, join
from os import mkdir, name
import threading


class Playlist:
    def __init__(self, url):
        self.playlist_url = url
        self.idx = 0
        self.num = 0
        self.titles = []
        self.ids = []
        self.play_playlist()

    def _extract_playlist_titles_ids(self):
        click.echo("Extracting titles and urls")
        output, err = cmd(["youtube-dl", "-j", "--flat-playlist", self.playlist_url])
        counter = 0
        songs = output.split("\n")
        for song in songs:
            song_json = json.loads(song)
            self.ids.append(song_json["id"])
            self.titles.append(song_json["title"])
        self.num = len(songs)
        click.echo(f"Extraction complete. Found {self.num} songs...")

    def _play(self):
        home = expanduser("~")
        cache_dir = join(home, "plays")
        if not exists(cache_dir):
            mkdir(cache_dir)

        if name == "nt":
            mpv = "mpv.com"
        else:
            mpv = "mpv"
        while len(self.ids) == 0:
            pass

        self.url = f"https://youtube.com/watch?v={self.ids[self.idx]}"
        try:
            player = sp.Popen(
                [
                    mpv,
                    self.url,
                    "--no-video",
                    "--window-minimized",
                    "--audio-display=no",
                    "--cache=yes",
                    "--cache-on-disk",
                    f"--cache-dir={cache_dir}",
                ],
            )

            player.wait()
        finally:
            player.kill()

    def _play_v2(self):
        home = expanduser("~")
        cache_dir = join(home, "plays")
        if not exists(cache_dir):
            mkdir(cache_dir)

        if name == "nt":
            mpv = "mpv.com"
        else:
            mpv = "mpv"
        list_idx = self.playlist_url.find("list=")
        list_id = self.playlist_url[list_idx:]
        self.url = f"https://youtube.com/playlist?{list_id}"
        click.echo(self.url)
        player = None
        try:
            player = sp.Popen(
                [
                    mpv,
                    self.url,
                    "--no-video",
                    "--window-minimized",
                    "--audio-display=no",
                    "--cache=yes",
                    "--cache-on-disk",
                    f"--cache-dir={cache_dir}",
                ],
            )

            player.wait()
        except Exception as e:
            click.echo(e)
        finally:
            if player:
                player.kill()

    def play_playlist(self):
        # self._extract_playlist_titles_ids()
        self._play_v2()

    def next(self):
        pass


if __name__ == "__main__":
    pl = Playlist(
        "https://www.youtube.com/watch?v=Il0S8BoucSA&list=RDCLAK5uy_kmPRjHDECIcuVwnKsx2Ng7fyNgFKWNJFs&index=2"
    )
