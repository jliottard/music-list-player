# Music list player

A python script that downloads and plays musics from a music list text file. So you can store your playlist in plain text.

## How to use

### How to install the application and the dependencies

The project uses `Python 3.10` and it is not developped nor tested for earlier Python version.

Python libraries are listed in the `requirements.txt` files. To import the dependencies in a virtual environment, run:
- On Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

- On Windows:
```shell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The `python-vlc` dependency requires the [VLC](https://www.videolan.org/vlc/) software to be installed on your computer. Please use the latest version of VLC:
- On Linux, VLC version 3.0.16 works.
- On Windows, VLC version 3.0.20 works.

### How to configure

Use the `configuration.toml` file to specify where is your playlist file(s), where to store audio files and other settings. Use the provided `configuration.toml` file as a reference and feel free to modify it on your local repository. But do not remove fields from the `[global-settings]` part, they are mandatory for the global application settings.

The playlist file must be a list of the songs to play, with one song name per line.

### How to run the application

In the virtual environment, run in the project root directory:
- On Linux:
```bash
.venv/bin/python main.py
```
- On Windows:
```shell
python main.py
```

Deactivate the virtual environment:
- On Linux and Windows:
```bash
deactivate
```

### How to test

To run the tests, use in the project root directory:
```bash
pytest
```

To run the linter check, execute in the project root directory:
```bash
pylint *
```

## Features

### Implemented in version 1.0

- [x] Command-line interface definition in-app
- [x] Play audio
- [x] Download musics from Internet
- [x] Python virtual environment usage
- [x] Shuffle the playlist order
- [x] Audio is cached
- [x] Autoplay at the end of music
- [x] Stop and skip the music
- [x] Show the name of the current and the upcoming songs and as a status
- [x] Add some tests
- [x] Check end of list when using "next" command
- [x] Jump to another song in the playlist by name
- [x] Loop toggle option to restart the playlist from the start at the end
- [x] Change "pause" keyword to resume and its printing
- [x] Handle age restricted youtube video

### Implemented in version 1.1

- [x] Support Windows
- [x] Switch playlist profiles in app
- [x] Erase cached when quitting the application as a setting
- [x] Setup a continuous integration in GitHub with test on Linux platform
- [x] Change volume
- [x] Import the audios in background
- [x] Print music's lyrics matching music's audio

### Implemented

- [x] Handle errors on not finding a Youtube video for the given names of the playlist
- [x] Use a search function of a Python library
- [x] Add a selection menu when downloading music from Youtube (with video name, channel name, video duration, views count, release date)
- [x] Jump forward or backward in the current audio timeline
- [x] Import automatically the playlist from configuration on application start

### Backlog

- [ ] Parse author part of the audio line in plain text file
- [ ] Sanitize the audio's name with keywords and wildcard of filepath (like '/', '\', or '*')
- [ ] Speed up or down audios
- [ ] Create playlist dynamically based on tag(s) present on each audio name (line)
- [ ] Use directly a YouTube link if presents in the audio name (line)
- [ ] Add a resume mechanism to restart playlist on the song where the application did quit
- [ ] Provide an executable entry point file for Windows application per release
- [ ] Spell check the command keywords and the audio name argument for the Play command, so we can use alias for command ("pl" or "pla" for "play")
- [ ] Add colors to the prints and use a log system
- [ ] Add a music recommendation feature
