# Music list player

An audio player that uses text file to define your music playlist. It downloads audio files, plays musics, navigates through playlists and display song's lyrics.

The idea is to write your musics line by line in a simple plaintext file, so you can save your favorite songs anywhere.

Contents:

- [Installation](#installation)
- [Run the app in your terminal](#run-the-app-in-your-terminal)
- [Run the portable .exe app on Windows](#run-the-portable-exe-app-on-windows)
- [App settings](#app-settings)
- [Playlists](#playlists)
- [Importing your Spotify playlists](#importing-your-spotify-playlists)
- [For developers](#for-developers)
- [Project's history and features](#projects-history-and-features)

## Installation

You must have [VLC](https://www.videolan.org/vlc/) installed on your machine (version 3.0.16 or later) and added to the PATH.

## Run the app in your terminal

- Clone this project;
- With `Python 3.10` (or later), install the `pip` dependencies listed in `python_requirements/requirements.txt`;
- Run the `main.py`.

## Run the portable .exe app on Windows

- Download and extract the project from the lastest `.zip` archive from this project's Github Releases page.
- Run the `.exe` file.

## App settings

You can change the app's settings by editing the `configuration.toml` file:

- playlist file and audio files storage location;
- lyrics usage and so on.

Use the provided `configuration.toml` file as a reference and feel free to modify it on your local repository. But do not remove fields from the `[global-settings]` section.

A recommanded configuration is:

```toml
[my_profile]                                     # select this profile in the app : 'profile my_profile`
"playlist-file-relative-path" = "playlist.txt"   # this file must exist on your machine
"download-directory-relative-path" = ".cache"    # this directory must exist on your machine
"audio-source-selection-on-import" = false       # it will download the first YouTube result as the audio file
"persistant-audio-cache" = true                  # it keeps audio and lyric files in cache after leaving the application
"music-lyrics-search-on-import" = false          # it will not download lyrics, nor use cached lyrics
```

## Playlists

For the playlist, the playlist file must be a list of the songs to play, with one song name per line (ending with a carriage return). Thanks to metadata parsing, you can add hashtags followed by a word to a line in order to tag the line. So in one profile you can import and play audios only with a specific tag you chose. In a way, it is like a tagged playlist inside your playlist.

An example is for one line, the music name "etude op 10 number 4", the author "Frédéric Chopin", the tagged playlists "chopin" and "piano" that can be used as `import #chopin` or `import #piano` and the YouTube video source `(https://www.youtube.com/watch?v=oy0IgI_qewg)` that will be directly downloaded from:

```txt
etude op 10 no 4 by frédéric chopin #chopin #piano (https://www.youtube.com/watch?v=oy0IgI_qewg)
```

## Importing your Spotify playlists

- Install the `pip` dependencies listed in `python_requirements/spotify_import_requirements.txt`;
- Get your credentials from [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) to setup the [spotify_credentials.json](./playlist_migration/from_spotify/spotify_credentials.json) file;
- Fill the "CHANGE ME" data of the [spotify_playlists.json](./playlist_migration/from_spotify/spotify_playlists.json) file;
- Run `playlist_from_spotify.py` from its directory path.

## For developers

You must install the `pip` dependencies listed in `python_requirements/requirements.txt` and `python_requirements/dev_requirements.txt`.

### Testing

- Run `pytest` in the project root directory for unit testing;
- Run `pylint *` for the linter check.

### Build an .exe on Windows

- Check that VLC is installed on your Windows machine at the `C:\Program Files\VideoLAN\VLC` location, or modify the build script;
- Run the `build` script `.\scripts\build.ps1` or `scripts/build.sh` from the project root directory.

The executable's result is located in the `dist\music-list-player` directory.

To clean the reposity of the build artefacts, remove the builds from the repository directory with:

```powershell
.\scripts\clean.ps1
```

## Project's history and features

You can refer to the [change log](/CHANGELOG.md) for feature per app's version.

### Potential future features

- [ ] Add a music recommendation feature
