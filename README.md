# plays

Play music from your terminal

### Requirements

1. Python 3.8+
2. pip3
3. MPV (https://mpv.io)
   > Make sure to add it into Path variable. You can check if it is installed correctly by running `mpv` command.
4. youtube-dl (http://ytdl-org.github.io/youtube-dl/download.html)
5. Chromedriver (for playing charts only) [https://chromedriver.chromium.org/downloads]

### How to run

1. `python setup.py install`
2. After installation is complete

   - `plays <song name>`
   - `plays <youtube url>`

### Features:

1. Search and play songs from youtube:
   - `plays <song name>`
2. Play from youtube url:
   - `plays <yt_song_url>`
3. Play youtube playlist:
   - `plays <yt_playlist_url>`

> By adding flag `-r` or `--related` in above commands, it plays the first related song after completion. Eg: `plays -r <song name>`

4. Play youtube charts:
   - `plays -c` or `plays --charts`
   - `plays -c TOPSONGS_GLOBAL`
   - See more info by `plays -h`

> Note: Combining charts and query will result in weird behaviour. It's an intentional feature, 100%.
