from setuptools import setup, find_packages
from plays.__version__ import __version__

setup(
    name="plays",
    packages=find_packages(),
    author="Dark Vapour",
    author_email="ashishsubedi10@gmail.com",
    description="Play songs from terminal.",
    long_description="Play songs from terminal.",
    entry_points={"console_scripts": ["plays = plays.main:main"]},
    version=__version__,
    license="MIT",
    install_requires=["requests", "youtube_search", "click", "youtube-dl", "selenium"],
)
