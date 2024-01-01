# Music list player
A python script that downloads and plays musics from a music list text file.
## Features
### To do
- [ ] Add a command in Usage to create a Python virtual environment
- [ ] Switch playlist profiles on the fly (playlist file as input)
- [ ] Add some tests
- [ ] Import the songs in background to play early the first song while it finishes downloading the rest
- [ ] Loop toggle option to restart the playlist from the start at the end
- [ ] Jump to another song in the playlist by name
- [ ] Show the name of the current and the upcoming songs and as a status
- [ ] Add a volume changer
- [ ] Shuffle the musics order of the playlist
- [ ] Handle errors on not finding a Youtube video for the given names of the playlist
- [ ] Print lyrics as the music is playing
### Done
- [x] Check local storage if the audios have already been downloaded
- [x] Play next song in the playlist at the end of the current music
- [x] Define a command line interface
- [x] Add stop and skip actions to an audio being played
- [x] Play audio files
- [x] Download music's audio from name and author
## Dependencies
Python libraries are listed in the `requirements.txt` files. To import via `pip`, run:
```bash
make init
```
The VLC dependency requires the `vlc` software to be installed on your computer.
## How to use
### Configuration
Use the `configuration.toml` file to specify where is your playlist file and where to store audios.
### Usage
Run:
```bash
./main.py
```
