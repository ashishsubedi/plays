import argparse
import click

# from plays.subcommands.youtube import play_chart, plays

from plays.yt_music import YTMusic
from plays.utils import Charts
from plays.extractors import YTChartsExtractor, YTRelatedExtractor

# TODO: Use argparse


def parse():

    parser = argparse.ArgumentParser(
        description="Search and play music from the terminal."
    )

    parser.add_argument(
        "query",
        default=None,
        type=str,
        nargs="*",
        help="Song name, youtube song url or playlist url",
    )
    parser.add_argument(
        "-r",
        "--related",
        action="store_true",
        default=False,
        help="Flag to play next related song",
    )
    charts_group = parser.add_argument_group("charts")
    charts_group.add_argument(
        "-c",
        "--charts",
        default="TOPSONGS_GLOBAL",
        choices=list(Charts.keys()),
        help="Play from youtube charts",
        nargs="?",
    )
    args = parser.parse_args()
    return args


def main():
    """Main entry point for cli"""
    args = parse()
    charts = None

    if args.query:
        query = " ".join(args.query)
        click.echo(query)

    elif args.charts is None:
        charts = YTChartsExtractor()

    elif args.charts:
        charts = YTChartsExtractor(args.charts)
    else:
        click.echo("Not valid input. Try again")
        return

    if charts:
        click.echo(f"Extracting chart: {charts.chart}. Please wait few seconds...")
        charts.extract()
        query = charts.url

    music = YTMusic()
    if args.related:
        related_extractor = YTRelatedExtractor()

    while True:
        if found := music.search(query):
            music.play()
        if found and args.related:
            related_extractor.add_url(music.url)
            query = related_extractor.extract()
        else:
            break

    print("Exiting...")
