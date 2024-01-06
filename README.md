# Music list player
A python script that downloads and plays musics from a music list text file.
## How to use
### Dependencies
Python libraries are listed in the `requirements.txt` files. To import the dependencies in a virtual environment, run:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
LC dependency requires the `vlc` software to be installed on your computer.
### Configuration
Use the `configuration.toml` file to specify where is your playlist file and where to store audios.
### Run the application
In the virtual environment, run:
```bash
.venv/bin/python main.py
```
Deactivate the virtual environment:
```bash
deactivate
```
## Features
### Implemented
- [x] Python virtual environment usage
- [x] Shuffle the playlist order
- [x] Audio is cached
- [x] Autoplay at the end of music
- [x] Command-line interface definition in-app
- [x] Stop and skip the music
- [x] Play audio
- [x] Download musics from Internet
### Incoming
- [ ] Handle age restricted youtube video (/audio/download.py", line 25: exceptions.AgeRestrictedError)
- [ ] Support Windows 10
- [ ] Switch playlist profiles on the fly (playlist file as input)
- [ ] Add some tests
- [ ] Import the songs in background to play early the first song while it finishes downloading the rest
- [ ] Loop toggle option to restart the playlist from the start at the end
- [ ] Jump to another song in the playlist by name
- [ ] Show the name of the current and the upcoming songs and as a status
- [ ] Add a volume changer
- [ ] Handle errors on not finding a Youtube video for the given names of the playlist
- [ ] Print lyrics as the music is playing
