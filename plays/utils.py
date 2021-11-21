import subprocess as sp

Charts = dict(
    TOPSONGS_GLOBAL="TopSongs/global",
    TOPSONGS_US="TopSongs/us",
    TOPARTISTS_GLOBAL="TopArtists/global",
    TOPARTISTS_US="TopArtists/us",
    TRENDING_US="TrendingVideos/us",
)


def cmd(c):
    output, err = sp.Popen(
        c,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
    ).communicate()

    output = output.decode("utf-8").strip()
    err = err.decode("utf-8").strip()

    return output, err
