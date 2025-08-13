# Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Version 1.3 - 2025-08-13

### Added

- Migrate from Spotify playlists to plaintext files with a script.

### Changed

- Set `.m4a` as the audio file format instead of `.mp3` for downloaded audio (pytubefix).

### Fixed

- Replace the unmaintained youtube-search 3rd party library for pytubefix search.

## [Version 1.2](https://github.com/jliottard/music-list-player/releases/tag/v1.2.0) - 2024-11-17

### Added

- Use a search function of a Python library.
- Add a selection menu when downloading music from Youtube (with video name, channel name, video duration, views count, release date).
- Jump forward or backward in the current audio timeline.
- Import automatically the playlist from configuration on application start.
- Create playlist dynamically based on tag(s) present on each audio name (line).
- Check remaining disk usage when downloading audios.
- Use directly a YouTube link if presents in the audio name (line).
- Parse author part of the audio line in plain text file.
- Provide an executable entry point file for Windows application per release.

### Changed

- Sanitize the audio's name with keywords and wildcard of filepath (like '/', '\', or '*').

### Fixed

- Handle errors on not finding a Youtube video for the given names of the playlist.

## [Version 1.1](https://github.com/jliottard/music-list-player/releases/tag/v1.1.0) - 2024-03-09

### Added

- Support Windows.
- Switch playlist profiles in app.
- Erase cached when quitting the application as a setting.
- Setup a continuous integration in GitHub with test on Linux platform.
- Change volume.
- Import the audios in background.
- Print music's lyrics matching music's audio.

## [Version 1.0](https://github.com/jliottard/music-list-player/releases/tag/v1.0.0) - 2024-02-04

### Added

- Command-line interface definition in-app.
- Play audio.
- Download musics from Internet.
- Python virtual environment usage.
- Shuffle the playlist order.
- Audio is cached.
- Stop and skip the music.
- Show the name of the current and the upcoming songs and as a status.
- Add some tests.
- Check end of list when using "next" command.
- Jump to another song in the playlist by name.
- Loop toggle option to restart the playlist from the start at the end.

### Changed

- Autoplay at the end of music.
- Change "pause" keyword to resume and its printing.

### Fixed

- Handle age restricted youtube video.
